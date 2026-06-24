from django.test import TestCase, Client
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.urls import reverse
from library.models import Author, Book, Member, Issue

class LibraryTests(TestCase):
    def setUp(self):
        # Create a user to log in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create test data
        self.author = Author.objects.create(name='Test Author')
        
        # Create a book with 2 copies
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            isbn='1234567890123',
            copies_total=2,
            copies_available=2
        )
        
        # Create a member
        self.member = Member.objects.create(name='Test Member', email='test@example.com')
        
        self.client = Client()

    def test_book_is_available_property(self):
        self.assertTrue(self.book.is_available)
        self.book.copies_available = 0
        self.book.save()
        self.assertFalse(self.book.is_available)

    def test_issue_fine_calculation(self):
        # Create an issue due 3 days ago
        past_date = date.today() - timedelta(days=3)
        issue = Issue.objects.create(
            book=self.book,
            member=self.member,
            due_date=past_date
        )
        # Should be 3 days overdue, fine = 3 * 5 = 15
        self.assertEqual(issue.days_overdue, 3)
        self.assertEqual(issue.fine, 15)
        
        # Return the book, fine should drop to 0
        issue.returned = True
        issue.save()
        self.assertEqual(issue.fine, 0)

    def test_issue_book_view(self):
        self.client.login(username='testuser', password='testpassword')
        due_date = date.today() + timedelta(days=7)
        
        response = self.client.post(reverse('library:issue_book', args=[self.book.pk]), {
            'member': self.member.pk,
            'due_date': due_date.strftime('%Y-%m-%d')
        })
        
        # Should redirect to book detail
        self.assertRedirects(response, reverse('library:book_detail', args=[self.book.pk]))
        
        # Check database updates
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_available, 1) # Decreased by 1
        self.assertEqual(Issue.objects.count(), 1)
        
        issue = Issue.objects.first()
        self.assertEqual(issue.book, self.book)
        self.assertEqual(issue.member, self.member)

    def test_cannot_issue_out_of_stock_book(self):
        self.book.copies_available = 0
        self.book.save()
        
        self.client.login(username='testuser', password='testpassword')
        due_date = date.today() + timedelta(days=7)
        
        response = self.client.post(reverse('library:issue_book', args=[self.book.pk]), {
            'member': self.member.pk,
            'due_date': due_date.strftime('%Y-%m-%d')
        })
        
        # Should stay on the same page with an error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No copies available.')
        self.assertEqual(Issue.objects.count(), 0)

    def test_return_book_view(self):
        # Setup an issue
        issue = Issue.objects.create(
            book=self.book,
            member=self.member,
            due_date=date.today() + timedelta(days=7)
        )
        self.book.copies_available -= 1
        self.book.save()
        
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('library:return_book', args=[issue.pk]))
        
        # Should redirect to member detail
        self.assertRedirects(response, reverse('library:member_detail', args=[self.member.pk]))
        
        # Check database updates
        issue.refresh_from_db()
        self.assertTrue(issue.returned)
        self.assertEqual(issue.return_date, date.today())
        
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_available, 2) # Increased by 1

    def test_overdue_report_view(self):
        # Create an overdue issue
        past_date = date.today() - timedelta(days=3)
        Issue.objects.create(
            book=self.book,
            member=self.member,
            due_date=past_date
        )
        # Create a non-overdue issue
        future_date = date.today() + timedelta(days=3)
        Issue.objects.create(
            book=self.book,
            member=self.member,
            due_date=future_date
        )
        
        response = self.client.get(reverse('library:overdue_report'))
        self.assertEqual(response.status_code, 200)
        # Only 1 issue should be in the context
        self.assertEqual(len(response.context['issues']), 1)

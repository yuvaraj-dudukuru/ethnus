# ============================================================================
#  tests.py — automated checks that the API behaves correctly
# ----------------------------------------------------------------------------
#  Run every test with:   python manage.py test
#
#  APITestCase spins up a temporary, EMPTY database, runs each test, then
#  throws the database away. So tests never touch your real data. Each method
#  whose name starts with "test_" is one independent check.
# ============================================================================
from rest_framework.test import APITestCase


class StudentAPITest(APITestCase):

    def test_public_can_list(self):
        # Anyone (not logged in) should be able to READ the student list.
        # 200 means "OK / success".
        self.assertEqual(self.client.get('/api/students/').status_code, 200)

    def test_anonymous_cannot_create(self):
        # An anonymous (not-logged-in) user must NOT be able to create a
        # student. 401 means "Unauthorized — you need to log in first".
        r = self.client.post('/api/students/', {'roll': 9})
        self.assertEqual(r.status_code, 401)

from django.contrib import admin
from .models import Exam, Question, Choice, Attempt, Answer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ["title", "duration", "question_count", "max_marks"]
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "exam", "marks"]
    inlines = [ChoiceInline]


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ["student", "exam", "score", "started", "submitted"]
    list_filter = ["exam"]


admin.site.register(Answer)

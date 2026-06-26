# ============================================================================
#  api_views.py — list exams, start an attempt, submit + auto-grade, results.
# ----------------------------------------------------------------------------
#  Anti-cheating measures that live on the SERVER (never trust the browser):
#    * one Attempt per (student, exam)  -> no re-attempts
#    * grading compares against is_correct in the DB -> answer key never leaves
#    * the deadline is computed from the server's started timestamp -> a hacked
#      client clock can't buy extra time; late answers are discarded.
# ============================================================================
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .models import Exam, Question, Choice, Attempt, Answer
from .serializers import (
    ExamSerializer, ExamDetailSerializer, QuestionSerializer,
    ChoiceSerializer, AttemptSerializer,
)


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    search_fields = ["title"]

    def get_serializer_class(self):
        if self.action in ("retrieve", "start"):
            return ExamDetailSerializer
        return ExamSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminUser()]            # only instructors build exams
        if self.action in ("start", "submit", "results"):
            return [IsAuthenticated()]
        return super().get_permissions()      # list/retrieve public

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        """POST /api/exams/<id>/start/ — begin the single allowed attempt."""
        exam = self.get_object()
        attempt, created = Attempt.objects.get_or_create(
            student=request.user, exam=exam)
        if not created:
            return Response(
                {"detail": "You have already attempted this exam."}, status=400)
        data = ExamDetailSerializer(exam).data
        return Response({
            "attempt_id": attempt.id,
            "deadline": attempt.deadline,
            "duration": exam.duration,
            "questions": data["questions"],
        }, status=201)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        """POST /api/exams/<id>/submit/  body: {"answers":[{"question":1,"choice":3}]}."""
        exam = self.get_object()
        attempt = Attempt.objects.filter(student=request.user, exam=exam).first()
        if attempt is None:
            return Response({"detail": "Start the exam first."}, status=400)
        if attempt.submitted is not None:
            return Response({"detail": "You already submitted this exam."}, status=400)

        now = timezone.now()
        expired = now > attempt.deadline
        # Time's up -> auto-submit: late answers are discarded (score them as none).
        answers = [] if expired else request.data.get("answers", [])

        score = 0
        for a in answers:
            q = exam.questions.filter(pk=a.get("question")).first()
            if q is None:
                continue
            choice = q.choices.filter(pk=a.get("choice")).first()
            Answer.objects.update_or_create(
                attempt=attempt, question=q, defaults={"choice": choice})
            if choice is not None and choice.is_correct:
                score += q.marks

        attempt.score = score
        attempt.submitted = now
        attempt.save()
        return Response({"score": score, "total": exam.max_marks, "expired": expired})

    @action(detail=True, methods=["get"])
    def results(self, request, pk=None):
        """GET /api/exams/<id>/results/ — the current student's graded result."""
        exam = self.get_object()
        attempt = Attempt.objects.filter(student=request.user, exam=exam).first()
        if attempt is None or attempt.submitted is None:
            return Response({"detail": "No submitted attempt found."}, status=404)
        return Response({
            "score": attempt.score, "total": exam.max_marks,
            "submitted": attempt.submitted,
        })


class QuestionViewSet(viewsets.ModelViewSet):
    """Build exam questions (instructors/admins only)."""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ["exam"]


class ChoiceViewSet(viewsets.ModelViewSet):
    """Build the choices + answer key (instructors/admins only)."""
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ["question"]


class AttemptViewSet(viewsets.ReadOnlyModelViewSet):
    """A student's own attempt history."""
    serializer_class = AttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Attempt.objects.select_related("exam").filter(
            student=self.request.user)

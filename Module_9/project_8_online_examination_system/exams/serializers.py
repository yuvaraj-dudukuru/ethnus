# ============================================================================
#  serializers.py — note the TWO question shapes:
#    * "Take"  serializers HIDE is_correct (so students can't cheat).
#    * "Admin" serializers EXPOSE is_correct (for building exams).
# ============================================================================
from rest_framework import serializers
from .models import Exam, Question, Choice, Attempt


# ---- Take-the-exam shapes (no answer key leaked) ---------------------------
class ChoiceTakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "text"]          # deliberately NO is_correct


class QuestionTakeSerializer(serializers.ModelSerializer):
    choices = ChoiceTakeSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "marks", "choices"]


class ExamSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True)
    max_marks = serializers.IntegerField(read_only=True)

    class Meta:
        model = Exam
        fields = ["id", "title", "duration", "total_marks", "max_marks",
                  "question_count", "created"]


class ExamDetailSerializer(ExamSerializer):
    questions = QuestionTakeSerializer(many=True, read_only=True)

    class Meta(ExamSerializer.Meta):
        fields = ExamSerializer.Meta.fields + ["questions"]


# ---- Admin/management shapes (answer key visible) --------------------------
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "question", "text", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "exam", "text", "marks"]


class AttemptSerializer(serializers.ModelSerializer):
    exam_title = serializers.CharField(source="exam.title", read_only=True)

    class Meta:
        model = Attempt
        fields = ["id", "exam", "exam_title", "score", "started", "submitted"]
        read_only_fields = fields

from django.db import models
from django.utils import timezone

class Forms(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10,
        choices=[
            ("peer", "Peer"),
            ("review", "Review"),
            ("feedback", "Feedback"),
        ],
        default="peer",
    )
    period = models.CharField(max_length=20, default="monthly")
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[("open", "Open"), ("closed", "Closed")],
        default="open",
    )

    class Meta:
        db_table = "forms"

    def __str__(self):
        return self.name

class FormQuestions(models.Model):
    form = models.ForeignKey("evaluations.Forms", on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=10,
        choices=[("rating", "Rating"), ("text", "Text")],
        default="text",
    )
    max_score = models.IntegerField(null=True, blank=True)  # For rating questions

    class Meta:
        db_table = "form_questions"

    def __str__(self):
        return self.question_text[:50]

class FormResponses(models.Model):
    form = models.ForeignKey("evaluations.Forms", on_delete=models.CASCADE)
    question = models.ForeignKey("evaluations.FormQuestions", on_delete=models.CASCADE)
    user = models.ForeignKey(
        "users.Users", on_delete=models.CASCADE, related_name="responses_given"
    )
    target_user = models.ForeignKey(
        "users.Users", on_delete=models.CASCADE, related_name="responses_received"
    )
    answer = models.TextField()
    answer_type = models.CharField(
        max_length=10,
        choices=[("numeric", "Numeric"), ("text", "Text")],
        default="text",
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "form_responses"

    def __str__(self):
        return f"{self.user.username} -> {self.target_user.username} ({self.form.name})"
    
    
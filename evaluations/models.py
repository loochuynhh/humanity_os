from django.db import models


class Forms(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10, choices=[("self", "Self"), ("peer", "Peer")], default="self"
    )
    period = models.CharField(max_length=20, default="monthly")

    class Meta:
        db_table = "forms"

    def __str__(self):
        return self.name


class FormQuestions(models.Model):
    form = models.ForeignKey("evaluations.Forms", on_delete=models.CASCADE)
    question_text = models.TextField()

    class Meta:
        db_table = "form_questions"

    def __str__(self):
        return self.question_text[:50]


class FormResponses(models.Model):
    form = models.ForeignKey("evaluations.Forms", on_delete=models.CASCADE)
    user = models.ForeignKey(
        "users.Users", on_delete=models.CASCADE, related_name="responses_given"
    )
    target_user = models.ForeignKey(
        "users.Users", on_delete=models.CASCADE, related_name="responses_received"
    )
    answer = models.TextField()

    class Meta:
        db_table = "form_responses"

    def __str__(self):
        return f"{self.user.username} -> {self.target_user.username} ({self.form.name})"

from django.db import models


class Teams(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    manager = models.ForeignKey(
        "users.Users",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_teams",
    )
    members = models.ManyToManyField("users.Users", through="TeamMembers")

    class Meta:
        db_table = "teams"

    def __str__(self):
        return self.name


class TeamMembers(models.Model):
    team = models.ForeignKey("companies.Teams", on_delete=models.CASCADE)
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE)

    class Meta:
        db_table = "team_members"
        unique_together = ("team", "user")

    def __str__(self):
        return f"{self.team.name} - {self.user.username}"

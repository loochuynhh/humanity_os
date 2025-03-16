from django.db import models


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "company"

    def __str__(self):
        return self.name


class Teams(models.Model):
    team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE)
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

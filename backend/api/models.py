from django.db import models


class Email(models.Model):
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.email}"

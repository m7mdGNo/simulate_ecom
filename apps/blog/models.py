from django.db import models


class Blog(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="blogs")
    name = models.CharField(max_length=255)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to="blogs/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

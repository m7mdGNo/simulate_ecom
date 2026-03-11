from django.db import models


class Cart(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="carts")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="carts")
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.quantity})"

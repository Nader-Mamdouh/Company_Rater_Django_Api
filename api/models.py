from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class StockCompany(models.Model):
    name = models.CharField(max_length=255, unique=True)
    industry = models.CharField(max_length=100)
    market_cap = models.BigIntegerField()
    description = models.TextField(blank=True, null=True)
    average_rating = models.FloatField(
        default=0.0)  # Average rating calculation
    created_at = models.DateTimeField(auto_now_add=True)

    def update_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            self.average_rating = sum(
                r.rating for r in ratings) / ratings.count()
        else:
            self.average_rating = 0.0
        self.save()

    def __str__(self):
        return f"{self.name} ({self.average_rating:.1f} ⭐)"


class StockRating(models.Model):
    company = models.ForeignKey(
        StockCompany, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])  # Rating from 1-5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('company', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.company.name} ({self.rating})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically update the company's average rating
        self.company.update_average_rating()

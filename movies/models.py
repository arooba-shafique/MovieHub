from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    rating = models.FloatField()
    poster_url = models.URLField()
    tmdb_id = models.IntegerField(unique=True)
    trailer_url = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tmdb_id = models.IntegerField()
    title = models.CharField(max_length=255)
    poster_url = models.CharField(max_length=255, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tmdb_id')

    def __str__(self):
        return f"{self.user.username} - {self.title}"

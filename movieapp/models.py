from django.db import models
from django.core.validators import MinValueValidator

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    total_reviews = models.IntegerField(default=0)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username

class Director(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MovieCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Actor(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.CharField(max_length=50) 
    poster = models.ImageField(upload_to='movie_posters/', blank=True, null=True)
    category = models.ForeignKey(MovieCategory, on_delete=models.CASCADE, related_name='movies')
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
    actor = models.ManyToManyField(Actor, related_name='movies')

def __str__(self):
        if self.title:
            return self.title
        return f"Κριτική χωρίς τίτλο (ID: {self.id})"


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField()
    rating = models.IntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True) 
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews', blank=True, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews', blank=True, null=True)

    def __str__(self):
        if self.user:
            return self.user.get_username()
        return f"Κριτική (ID: {self.id})"
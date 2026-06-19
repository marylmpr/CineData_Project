from django.contrib import admin
from .models import UserProfile, Director, MovieCategory, Movie, Review, Actor

admin.site.register(UserProfile)
admin.site.register(Director)
admin.site.register(MovieCategory)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Actor)


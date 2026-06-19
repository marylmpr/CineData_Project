from django.shortcuts import render, redirect
from .models import Review, Movie


def catalog_view(request):
    return render(request, 'catalog.html')

def signup_view(request):
    return render(request, 'signup.html')
def login_view(request):
    return render(request, 'login.html')
def logout_view(request):
    return render(request, 'logout.html')
def profile_view(request):
    return render(request, 'profile.html')


def search_view(request):
    return render(request, 'search.html')


from django.shortcuts import render, redirect
from .models import Movie, Review, UserProfile


def reviews_view(request):
    movies = Movie.objects.all()

    if request.method == 'POST':
        movie_id = request.POST.get('review_movie')
        rating = request.POST.get('review_rating')
        comment = request.POST.get('review_comment')
        chosen_movie = Movie.objects.get(id=movie_id)
        default_user = UserProfile.objects.first()
        if not default_user:
            default_user = UserProfile.objects.create(username="mary", email="mary@test.com")

        Review.objects.create(
            movie=chosen_movie,
            user=default_user,
            rating=int(rating),
            comment=comment
        )
        return redirect('reviews_history')

    return render(request, 'reviews.html', {'movies': movies})
        
    all_movies = Movie.objects.all()
    return render(request, 'reviews.html', {'movies': all_movies})

def reviews_history(request):
    all_reviews = Review.objects.all().order_by('-id')
    return render(request, 'reviews_history.html', {'reviews': all_reviews})


def details_view(request):
    return render(request, 'details.html')
 
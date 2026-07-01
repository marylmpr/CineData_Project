from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review, Movie, UserProfile
from django.db.models import Q
from .models import Movie, MovieCategory


def catalog_view(request):
    all_movies = Movie.objects.all()
    return render(request, 'catalog.html', {'movies': all_movies})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        terms = request.POST.get('terms') 

        errors = {}

        if not username or not email or not password or not password_confirm:
            errors['general'] = "Παρακαλώ συμπληρώστε όλα τα πεδία."

        if email and User.objects.filter(email=email).exists():
            errors['email'] = "Η διεύθυνση Email χρησιμοποιείται ήδη."
        
        if email and '@' not in email:
            errors['email'] = "Παρακαλώ εισάγετε μια έγκυρη διεύθυνση email."

        if password and len(password) < 6:
            errors['password'] = "Ο κωδικός πρόσβασης πρέπει να είναι τουλάχιστον 6 χαρακτήρες."
            
        if password != password_confirm:
            errors['password_confirm'] = "Οι κωδικοί πρόσβασης δεν ταιριάζουν."

        if not terms:
            errors['terms'] = "Πρέπει να αποδεχτείτε τους Όρους Χρήσης."

        if username and User.objects.filter(username=username).exists():
            errors['username'] = "Το όνομα χρήστη χρησιμοποιείται ήδη."

        if errors:
            return render(request, 'signup.html', {
                'errors': errors,
                'username_value': username, 
                'email_value': email
            })  

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)
        messages.success(request, "Η εγγραφή σας ολοκληρώθηκε επιτυχώς.")
        return redirect('profile') 
        
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Λανθασμένο Όνομα Χρήστη ή Κωδικός.")
    
    return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)  
        return redirect('logout') 
    
    return render(request, 'logout.html')

@login_required(login_url='/login/') 
def profile_view(request):
    user = request.user
    total_reviews = 0
    
    if user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(username=user.username)
            total_reviews = Review.objects.filter(user=user_profile).count()
        except UserProfile.DoesNotExist:
            total_reviews = 0
        
    return render(request, 'profile.html', {
        'user': user,
        'total_reviews': total_reviews
    })



def search_view(request):
    query = request.GET.get('q', '')
    genre_id = request.GET.get('genre', '')
    
    categories = MovieCategory.objects.all()
    results = Movie.objects.all()
    
    if query:
        results = results.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        
    if genre_id:
        results = results.filter(category_id=genre_id)
        
    if not query and not genre_id:
        results = None

    return render(request, 'search.html', {
        'results': results,
        'query': query,
        'genre_id': genre_id,
        'categories': categories
    })

def reviews_view(request):
    movies = Movie.objects.all()

    if request.method == 'POST':
        movie_id = request.POST.get('review_movie')
        rating = request.POST.get('review_rating')
        comment = request.POST.get('review_comment')
        chosen_movie = Movie.objects.get(id=movie_id)
        if request.user.is_authenticated:
            default_user = UserProfile.objects.filter(username=request.user.username).first()
        else:
            default_user = None
        
        if not default_user:
            default_user = UserProfile.objects.first()

        Review.objects.create(
            movie=chosen_movie,
            user=default_user,
            rating=int(rating),
            comment=comment
        )
        return redirect('reviews_history', movie_id=movie_id)

    return render(request, 'reviews.html', {'movies': movies})


def reviews_history(request, movie_id):
    all_reviews = Review.objects.filter(movie_id=movie_id).order_by('-id')

    return render(request, 'reviews_history.html', {'reviews': all_reviews})


@login_required(login_url='login')
def details_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'details.html', {'movie': movie})
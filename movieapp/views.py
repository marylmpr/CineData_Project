from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review, Movie, UserProfile


def catalog_view(request):
    return render(request, 'catalog.html')



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
    return render(request, 'login.html')

def logout_view(request):
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
    return render(request, 'search.html')



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
 
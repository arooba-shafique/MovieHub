from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Movie, Favorite
from .serializers import MovieSerializer

import requests

TMDB_API_KEY = "1626150bba732e6e21e7b85b16466d61"
BLOCKED_TITLES = ["Together", "Fall for Me", "F1", "The Naked Gun"]


# User Authentication
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can log in now.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'movies/signup.html', {'form': form})


# Movie CRUD API
class MovieList(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetail(APIView):
    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


class MovieSearch(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        movies = Movie.objects.filter(title__icontains=query)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


# TMDB API Integrations
class TMDBPopularMovies(APIView):
    def get(self, request):
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={settings.TMDB_API_KEY}&language=en-US&page=1"
        response = requests.get(url)
        movies = response.json().get("results", [])
        filtered_movies = [m for m in movies if m["title"] not in BLOCKED_TITLES]
        return Response(filtered_movies)


class TMDBMovieDetail(APIView):
    def get(self, request, pk):
        movie_url = f"https://api.themoviedb.org/3/movie/{pk}?api_key={settings.TMDB_API_KEY}"
        movie_resp = requests.get(movie_url).json()

        videos_url = f"https://api.themoviedb.org/3/movie/{pk}/videos?api_key={settings.TMDB_API_KEY}"
        videos_resp = requests.get(videos_url).json()

        trailer = None
        for vid in videos_resp.get('results', []):
            if vid['site'] == 'YouTube' and vid['type'] == 'Trailer':
                trailer = f"https://www.youtube.com/embed/{vid['key']}"
                break

        movie_resp['trailer'] = trailer
        return Response(movie_resp)


class TMDBMovieSearch(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return Response([])

        url = f"https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&query={query}&language=en-US&page=1"
        response = requests.get(url)
        if response.status_code != 200:
            return Response({'error': 'Failed to fetch movies'}, status=response.status_code)

        movies = response.json().get('results', [])
        return Response(movies)


# Pages / Templates
def home(request):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={settings.TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    movies = response.json().get("results", [])
    filtered_movies = [m for m in movies if m["title"] not in BLOCKED_TITLES]
    return render(request, "movies/home.html", {"movies": filtered_movies})


def landing(request):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url).json()
    movies = response.get("results", [])
    return render(request, "movies/landing.html", {"popular_movies": movies})


def movie_list_page(request):
    return render(request, 'movies/movie_list.html')


def movie_detail_page(request, pk):
    return render(request, 'movies/movie_detail.html', {'movie_id': pk})


def tmdb_movie_detail_page(request, pk):
    url = f"https://api.themoviedb.org/3/movie/{pk}?api_key={settings.TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    movie = response.json()
    videos_url = f"https://api.themoviedb.org/3/movie/{pk}/videos?api_key={settings.TMDB_API_KEY}&language=en-US"
    videos_response = requests.get(videos_url)
    videos_data = videos_response.json()

    trailer = None
    for video in videos_data.get("results", []):
        if video["site"] == "YouTube" and video["type"] == "Trailer" and not trailer:
            trailer = video["key"]

    movie_title_for_search = movie.get("title", "").replace(" ", "+")
    full_movie_search_url = f"https://www.youtube.com/results?search_query={movie_title_for_search}+full+movie"

    return render(request, "movies/tmdb_detail.html", {
        "movie": movie,
        "trailer": trailer,
        "full_movie_search_url": full_movie_search_url
    })


# Favorites
@login_required
def add_favorite(request, tmdb_id):
    if request.method == "POST":
        movie, created = Movie.objects.get_or_create(tmdb_id=tmdb_id)
        if created or not movie.poster_url:
            response = requests.get(
                f"https://api.themoviedb.org/3/movie/{tmdb_id}",
                params={"api_key": settings.TMDB_API_KEY, "language": "en-US"}
            )
            if response.status_code == 200:
                data = response.json()
                movie.title = data.get("title", "")
                movie.description = data.get("overview", "")
                movie.genre = ",".join([g["name"] for g in data.get("genres", [])]) if data.get("genres") else ""
                movie.release_date = data.get("release_date") or None
                movie.rating = data.get("vote_average") or 0
                movie.poster_url = f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get("poster_path") else ""
                movie.save()

        fav, created = Favorite.objects.get_or_create(user=request.user, movie=movie)
        if not created:
            fav.delete()
            return JsonResponse({"status": "removed", "message": "Removed from favorites"})
        return JsonResponse({"status": "added", "message": "Added to favorites"})

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def toggle_favorite(request, tmdb_id):
    if request.method == "POST":
        title = request.POST.get("title")
        poster_url = request.POST.get("poster_url", "")

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            tmdb_id=tmdb_id,
            defaults={"title": title, "poster_url": poster_url},
        )

        if not created:
            favorite.delete()
            return JsonResponse({"status": "removed"})
        return JsonResponse({"status": "added"})
    return JsonResponse({"status": "error"}, status=400)


@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).order_by('-added_at')
    return render(request, "movies/favorites.html", {"favorite_movies": favorites})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    serializer = MovieSerializer([f.movie for f in favorites], many=True)
    return Response(serializer.data)

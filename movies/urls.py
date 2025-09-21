from django.urls import path
from .views import (
    MovieList, MovieDetail, MovieSearch,
    TMDBPopularMovies, TMDBMovieDetail,
    TMDBMovieSearch, add_favorite, list_favorites
)

urlpatterns = [
    path('movies/list/', MovieList.as_view(), name='movie-list'),
    path('movies/<int:pk>/detail/', MovieDetail.as_view(), name='movie-detail'),
    path('movies/search/', MovieSearch.as_view(), name='movie-search'),
    path('movies/tmdb/search/', TMDBMovieSearch.as_view(), name='tmdb-movie-search'),
    path('movies/tmdb/', TMDBPopularMovies.as_view(), name='tmdb-popular'),
    path('movies/tmdb/<int:pk>/', TMDBMovieDetail.as_view(), name='tmdb-movie-detail'),
    path("favorites/add/<int:tmdb_id>/", add_favorite, name="add-favorite"),
    path('favorites/list/', list_favorites, name='list-favorites'),
]

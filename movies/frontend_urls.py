from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
path('', views.landing, name='landing'),  
    path('home/', views.home, name='home'),     path('movies/', views.movie_list_page, name='movie-list-page'),
    path('movies/<int:pk>/', views.movie_detail_page, name='movie-detail-page'),
    path('movies/tmdb/<int:pk>/', views.tmdb_movie_detail_page, name='tmdb-movie-detail-page'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/toggle/<int:tmdb_id>/', views.toggle_favorite, name='toggle-favorite'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='movies/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='movies/logout.html'), name='logout'),
]

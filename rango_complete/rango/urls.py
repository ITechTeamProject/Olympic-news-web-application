from os import name
from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('team/', views.team, name='team'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    #path('register/', views.register, name='register'),
    #path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    #path('logout/', views.user_logout, name='logout'),
    #path('search/', views.search, name='search')
    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('suggest/', views.CategorySuggestionView.as_view(), name='suggest'),
    #path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),
    path('search_add_page/', views.SearchAddPageView.as_view(), name='search_add_page'),
    path('goto/', views.goto_url, name='goto'),
]


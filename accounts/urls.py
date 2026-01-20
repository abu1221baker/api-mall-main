from django.urls import path
from .views import *


urlpatterns = [
    path('profiles/', profile_list_create, name='profile-list-create'),
    path('profiles/<int:pk>/', profile_detail, name='profile-detail'),
    path('login/', login_view, name='login'),
]

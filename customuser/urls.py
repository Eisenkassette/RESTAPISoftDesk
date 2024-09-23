from django.urls import path
from .views import CustomUserListCreate, CustomUserRetrieveUpdateDestroy

urlpatterns = [
    path('users/', CustomUserListCreate.as_view(), name='user-list-create'),
    path('users/<str:username>/', CustomUserRetrieveUpdateDestroy.as_view(), name='user-retrieve-update-delete'),
]
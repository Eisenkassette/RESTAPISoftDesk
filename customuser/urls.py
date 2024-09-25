from django.urls import path
from .views import CustomUserListCreate, CustomUserRetrieveUpdateDestroy, anonymize_user

urlpatterns = [
    path('users/', CustomUserListCreate.as_view(), name='user-list-create'),
    path('users/<str:username>/', CustomUserRetrieveUpdateDestroy.as_view(), name='user-retrieve-update-delete'),

    path('users/anonymize/<int:user_id>/', anonymize_user, name='anonymize-user'),
]
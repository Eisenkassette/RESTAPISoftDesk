from .models import CustomUser
from .serializers import CustomUserSerializer
from .permissions import IsAuthorOrReadOnly, IsAuthenticatedOrCreateOnly
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
import string
import random


class CustomUserListCreate(ListCreateAPIView):
    '''
    customuser VIEW that provides:
    A GET list users method, can be used by Authenticated users.
    A POST method to create a new user, can be used by anyone.
    '''
    permission_classes = [IsAuthenticatedOrCreateOnly]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        username = response.data['username']
        return Response({'username': username}, status=status.HTTP_201_CREATED)


class CustomUserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    '''
    customuser VIEW that provides:
    A GET method to show details of a specfic user, can be used by authenticated user
    '''
    permission_classes = [IsAuthorOrReadOnly]
    http_method_names = ['get', 'patch', 'delete']
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        username = instance.username
        self.perform_destroy(instance)
        return Response({'username': username}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def anonymize_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    new_username = f"Anon_{random_string}"
    
    user.username = new_username
    user.birth_date = '1000-01-01'
    user.is_active = False
    user.save()
    
    return Response({"message": f"User {user_id} has been anonymized."}, status=status.HTTP_200_OK)
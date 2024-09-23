from .models import CustomUser
from .serializers import CustomUserSerializer
from .permissions import IsAuthorOrReadOnly, IsAuthenticatedOrCreateOnly
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status


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


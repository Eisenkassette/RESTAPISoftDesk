from .models import Project, Contributor, Issues, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssuesSerializer, CommentSerializer
from .permissions import IsProjectAuthorOrReadOnly, IsContributor, IsAuthorOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status


class ProjectListCreate(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        title = response.data['title']
        return Response({'title': title}, status=status.HTTP_201_CREATED)

class ProjectRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectAuthorOrReadOnly]
    lookup_field = 'title'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = instance.title
        self.perform_destroy(instance)
        return Response({'title': title}, status=status.HTTP_200_OK)


class ContributorListCreate(ListCreateAPIView):
    serializer_class = ContributorSerializer
    permission_classes = [IsProjectAuthorOrReadOnly]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        return Contributor.objects.filter(project=project)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(self.request, project)
        serializer.save(project=project)

class ContributorDestroy(DestroyAPIView):
    serializer_class = ContributorSerializer
    permission_classes = [IsProjectAuthorOrReadOnly]

    def get_object(self):
        project_id = self.kwargs.get('project_id')
        user_id = self.kwargs.get('user_id')
        project = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(self.request, project)
        return get_object_or_404(Contributor, project=project, user__id=user_id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user.username
        self.perform_destroy(instance)
        return Response({'username': user}, status=status.HTTP_200_OK)



class IssueListCreate(ListCreateAPIView):
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Issues.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        serializer.save(author=self.request.user, project=project)

class IssueRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        issue_name = instance.name
        self.perform_destroy(instance)
        return Response({'issue_name': issue_name}, status=status.HTTP_200_OK)


class CommentList(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        issue_id = self.kwargs.get('issue_id')
        return Comment.objects.filter(project_id=project_id, issue_id=issue_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        issue_id = self.kwargs.get('issue_id')
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issues, id=issue_id, project=project)
        serializer.save(author=self.request.user, project=project, issue=issue)

class CommentRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        issue_id = self.kwargs.get('issue_id')
        return Comment.objects.filter(project_id=project_id, issue_id=issue_id)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        comment_uuid = str(instance.id)
        self.perform_destroy(instance)
        return Response({'comment_uuid': comment_uuid}, status=status.HTTP_200_OK)
from django.urls import path
from . import views

urlpatterns = [
    # Project URLs
    path('projects/', views.ProjectListCreate.as_view(), name='project-list-create'),
    path('projects/<str:title>/', views.ProjectRetrieveUpdateDestroy.as_view(), name='project-retrieve-update-delete'),
    
    # Contributor URLs
    path('projects/<str:project_id>/contributors/', views.ContributorListCreate.as_view(), name='contributor-list-create'),
    path('projects/<str:project_id>/contributors/<int:user_id>/', views.ContributorDestroy.as_view(), name='contributor-delete'),
    
    # Issue URLs
    path('projects/<str:project_id>/issues/', views.IssueListCreate.as_view(), name='issue-list-create'),
    path('projects/<str:project_id>/issues/<int:id>/', views.IssueRetrieveUpdateDestroy.as_view(), name='issue-retrieve-update-delete'),
    
    # Comment URLs
    path('projects/<str:project_id>/issues/<int:issue_id>/comments/', views.CommentList.as_view(), name='comment-list'),
    path('projects/<str:project_id>/issues/<int:issue_id>/comments/<uuid:pk>/', views.CommentRetrieveUpdateDestroy.as_view(), name='comment-retrieve-update-delete'),
]
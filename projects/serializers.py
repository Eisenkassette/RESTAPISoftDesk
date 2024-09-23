from rest_framework import serializers
from .models import Project, Contributor, Issues, Comment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'creation_date']
        read_only_fields = ['author', 'creation_date']
        extra_kwargs = {
            'title': {'required': True},
            'type': {'required': True},
        }
    
    def create(self, validated_data):
        author = self.context['request'].user
        return Project.objects.create(author=author, **validated_data)


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'creation_date']
        read_only_fields = ['project', 'creation_date']
        extra_kwargs = {
            'user': {'required': True},
        }
        ordering = ['user', 'creation_date']


class IssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ['id', 'name', 'description', 'priority', 'type', 'status', 'project', 'author', 'assignees', 'creation_date']
        read_only_fields = ['author', 'project', 'creation_date']
        extra_kwargs = {
            'name': {'required': True},
            'priority': {'required': True},
            'type': {'required': True},
            'status': {'required': True},
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'project', 'issue', 'author', 'description', 'creation_date']
        read_only_fields = ['id', 'author', 'issue', 'creation_date']
        extra_kwargs = {
            'description': {'required': True},
        }
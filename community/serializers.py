from rest_framework import serializers

from universities.models import University
from users.models import InterestedProgram, UserProfile
from .models import Post
from rest_framework import pagination, serializers
from .pagination import CustomPostPagination


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username']


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    posted_by = ProfileSerializer()

    class Meta:
        model = Post
        fields = ['content', 'ctime', 'likes_count', 'comments_count', 'posted_by', 'tags', 'is_liked']

    def get_likes_count(self, post):
        return post.liked_by.count()

    def get_comments_count(self, post):
        return post.comments.count()

    def get_is_liked(self, post):
        request = self.context.get('request')
        user = request.user
        if post.liked_by.filter(id=user.id):
            return True
        return False


class CommunitySerializer(serializers.ModelSerializer):
    university_id = serializers.IntegerField(source='id')
    university = serializers.CharField(source='name')
    posts = PostSerializer(many=True)
    posts_count = serializers.SerializerMethodField()
    interested_count  = serializers.SerializerMethodField()
    class Meta:
        model = University
        fields  = ['university_id', 'university', 'posts', 'posts_count', 'interested_count']

    def get_posts_count(self, instance):
        return instance.posts.count()

    def get_interested_count(self, instance):
        return InterestedProgram.objects.filter(intake__program__university=instance).values_list('profile').distinct().count()

    def to_representation(self, instance):
        # Pass the context to the related ProgramSerializer
        context = self.context
        request =  self.context['request']
        tag = request.GET.get("tag", None)
        posts = instance.posts.all()
        if tag:
            posts = posts.filter(tags__contains=tag)
        paginator = CustomPostPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        posts_serializer = PostSerializer(page, many=True, context=context)

        pagination_info = {
            'page_number': paginator.page.number,
            'next_page': paginator.get_next_link(),
            'previous_page': paginator.get_previous_link(),
            'total_pages': paginator.page.paginator.num_pages,
        }

        # Create the representation for the UniversitySerializer
        representation = super().to_representation(instance)
        representation['posts'] = posts_serializer.data
        representation['pagination'] = pagination_info  # Include pagination info in the response

        return representation


class AddPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'tags']


from django.urls import path
from .views import Community, LikePost, CommentAPIView, CommentView, PostView


urlpatterns = [
    path('<int:university_id>/', Community.as_view(), name='community'),
    path('post/<int:post_id>/', PostView.as_view(), name="post_id"),
    path('post/<int:post_id>/like/', LikePost.as_view(), name="like_post"),
    path('post/<int:post_id>/comment/', CommentAPIView.as_view(), name="comments"),
    path('comment/<int:comment_id>/', CommentView.as_view(), name="comment_id"),

]

from django.urls import path, register_converter
from . import views


class ReactionTypeConverter:
    regex = "like|dislike"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(ReactionTypeConverter, "reaction")


urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/create/", views.PostCreateView.as_view(), name="create_post"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="update_post"),
    path(
        "post/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="delete_post"
    ),
    # reactions (validated at URL level)
    path(
        "post/<slug:slug>/react/<reaction:reaction_type>/",
        views.TogglePostReactionView.as_view(),
        name="toggle_post_reaction",
    ),
    path(
        "post/<slug:slug>/comment/create/",
        views.CreateCommentView.as_view(),
        name="create_comment",
    ),
    path(
        "comment/<int:pk>/edit/",
        views.UpdateCommentView.as_view(),
        name="update_comment",
    ),
    path(
        "comment/<int:pk>/delete/",
        views.DeleteCommentView.as_view(),
        name="delete_comment",
    ),
    path(
        "comment/<int:pk>/react/<reaction:reaction_type>/",
        views.ToggleCommentReactionView.as_view(),
        name="toggle_comment_reaction",
    ),
]

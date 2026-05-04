from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import BlogPost, Comment, PostReaction, CommentReaction
from .forms import BlogPostForm, CommentForm, CommentUpdateForm
from typing import cast

# --------------------
# Posts
# --------------------


class PostListView(ListView):
    model = BlogPost
    template_name = "list_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return (
            BlogPost.objects.select_related("user")
            .annotate(
                comment_count=Count("comments"),
                likes_count=Count(
                    "reactions", filter=Q(reactions__reaction_type="like")
                ),
                dislikes_count=Count(
                    "reactions", filter=Q(reactions__reaction_type="dislike")
                ),
            )
            .order_by("-created_at")
        )


class PostDetailView(DetailView):
    model = BlogPost
    template_name = "post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return BlogPost.objects.select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        context["comments"] = (
            post.comments.select_related("user")
            .annotate(
                likes_count=Count(
                    "reactions", filter=Q(reactions__reaction_type="like")
                ),
                dislikes_count=Count(
                    "reactions", filter=Q(reactions__reaction_type="dislike")
                ),
            )
            .order_by("-created_at")
        )

        context["comment_form"] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "create_post.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Post created")
        return super().form_valid(form)

    def get_success_url(self):
        post = cast(BlogPost, self.object)
        return reverse_lazy("post_detail", kwargs={"slug": post.slug})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "update_post.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Not allowed")
        return redirect("post_detail", slug=self.get_object().slug)

    def get_success_url(self):
        messages.success(self.request, "Post updated")
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = "delete_post.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("post_list")

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Not allowed")
        return redirect("post_detail", slug=self.get_object().slug)


# --------------------
# Comments
# --------------------


class CreateCommentView(LoginRequiredMixin, View):
    def post(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added")
        else:
            messages.error(request, "Invalid comment")

        return redirect("post_detail", slug=slug)


class UpdateCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.user != request.user:
            messages.error(request, "Not allowed")
            return redirect("post_detail", slug=comment.post.slug)

        form = CommentUpdateForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated")
        else:
            messages.error(request, "Invalid data")

        return redirect("post_detail", slug=comment.post.slug)


class DeleteCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        slug = comment.post.slug

        if comment.user == request.user:
            comment.delete()
            messages.success(request, "Comment deleted")
        else:
            messages.error(request, "Not allowed")

        return redirect("post_detail", slug=slug)


# --------------------
# Reactions (POST only)
# --------------------


class TogglePostReactionView(LoginRequiredMixin, View):
    def post(self, request, slug, reaction_type):
        post = get_object_or_404(BlogPost, slug=slug)

        obj, created = PostReaction.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={"reaction_type": reaction_type},
        )

        if not created:
            if obj.reaction_type == reaction_type:
                obj.delete()
            else:
                obj.reaction_type = reaction_type
                obj.save()

        return redirect("post_detail", slug=slug)


class ToggleCommentReactionView(LoginRequiredMixin, View):
    def post(self, request, pk, reaction_type):
        comment = get_object_or_404(Comment, pk=pk)
        slug = comment.post.slug

        obj, created = CommentReaction.objects.get_or_create(
            user=request.user,
            comment=comment,
            defaults={"reaction_type": reaction_type},
        )

        if not created:
            if obj.reaction_type == reaction_type:
                obj.delete()
            else:
                obj.reaction_type = reaction_type
                obj.save()

        return redirect("post_detail", slug=slug)

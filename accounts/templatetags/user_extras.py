from django import template

register = template.Library()


@register.filter
def is_owner(obj, user):
    return hasattr(obj, "user") and obj.user == user


@register.simple_tag
def avatar_url(user):
    if user.avatar:
        return user.avatar.url
    return "/static/default-avatar.png"

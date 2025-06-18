from django.contrib import admin
from .models import Lead, Post


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = (
        "reddit_post_id",
        "post_title",
        "post_category",
        "subreddit",
    )
    readonly_fields = (
        "reddit_post_id",
        "post_title",
        "post_category",
        "subreddit",
    )


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "reddit_username",
        "email",
        "lead_status",
        "created_at",
    )
    list_filter = ("lead_status",)
    search_fields = ("reddit_username", "email")
    readonly_fields = ("id", "created_at", "updated_at")
    fields = (
        "id",
        "reddit_username",
        "first_name",
        "last_name",
        "email",
        "phone",
        "company_name",
        "lead_status",
        "created_at",
        "updated_at",
    )
    inlines = [PostInline]
    list_per_page = 25


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "post_title",
        "reddit_post_id",
        "post_owner",
        "subreddit",
        "post_time",
    )
    list_filter = ("subreddit", "post_category")
    search_fields = (
        "post_title",
        "reddit_post_id",
        "subreddit",
        "post_owner__reddit_username",
    )
    readonly_fields = ("id",)
    fields = (
        "id",
        "reddit_post_id",
        "post_title",
        "post_url",
        "post_owner",
        "subreddit",
        "post_category",
        "post_time",
    )
    list_per_page = 25

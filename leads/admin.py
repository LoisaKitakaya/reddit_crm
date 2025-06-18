from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.management import call_command
from django.template.response import TemplateResponse
from .models import Lead, Post


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = (
        "reddit_post_id",
        "post_title",
        "post_category",
        "subreddit",
        "post_trigger",
    )
    readonly_fields = (
        "reddit_post_id",
        "post_title",
        "post_category",
        "subreddit",
        "post_trigger",
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "generate-leads/",
                self.admin_site.admin_view(self.generate_leads_view),
                name="generate_leads",
            ),
        ]
        return custom_urls + urls

    def generate_leads_view(self, request):
        if request.method == "POST":
            try:
                posts_limit = int(request.POST.get("posts_limit", 10))
                call_command("generate_leads", posts_limit=posts_limit)
                self.message_user(
                    request,
                    f"Successfully generated leads with posts_limit={posts_limit}",
                    level=messages.SUCCESS,
                )
            except Exception as e:
                self.message_user(
                    request, f"Error generating leads: {str(e)}", level=messages.ERROR
                )
            return HttpResponseRedirect("../")
        context = {
            **self.admin_site.each_context(request),
            "title": "Generate Leads",
            "opts": self.model._meta,
            "posts_limit": 10,
        }
        return TemplateResponse(
            request, "admin/leads/lead/generate_leads.html", context
        )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "post_title",
        "reddit_post_id",
        "post_owner",
        "subreddit",
        "post_trigger",
        "post_time",
    )
    list_filter = ("subreddit", "post_category", "post_trigger")
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
        "post_trigger",
        "post_time",
    )
    list_per_page = 25

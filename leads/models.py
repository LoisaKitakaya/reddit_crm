import uuid
from django.db import models
from django.utils import timezone


class Lead(models.Model):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    LOST = "lost"

    LEAD_STATUS = [
        (NEW, "New"),
        (CONTACTED, "Contacted"),
        (QUALIFIED, "Qualified"),
        (CONVERTED, "Converted"),
        (LOST, "Lost"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    reddit_username = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    company_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    lead_status = models.CharField(
        max_length=20,
        choices=LEAD_STATUS,
        default=NEW,
    )
    created_at = models.DateTimeField(
        default=timezone.now,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "leads"
        ordering = ["-created_at"]
        verbose_name = "Lead Profile"
        verbose_name_plural = "Lead Profiles"

    def __str__(self):
        return f"{self.reddit_username}"


class Post(models.Model):
    TASK = "task"
    OFFER = "offer"

    TRIGGER = [
        (TASK, "Task"),
        (OFFER, "Offer"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    post_owner = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    reddit_post_id = models.CharField(
        max_length=20,
        unique=True,
    )
    post_url = models.URLField(
        max_length=200,
    )
    post_title = models.CharField(
        max_length=300,
    )
    post_category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    post_trigger = models.CharField(
        max_length=20,
        choices=TRIGGER,
        blank=True,
        null=True,
    )
    subreddit = models.CharField(
        max_length=100,
        db_index=True,
    )
    post_time = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        db_table = "posts"
        ordering = ["-post_time"]
        verbose_name = "Reddit Post"
        verbose_name_plural = "Reddit Posts"

    def __str__(self):
        return f"{self.post_title}"

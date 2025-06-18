from django.core.management.base import BaseCommand
import praw
import datetime
from google import genai
from django.conf import settings
from django.db import IntegrityError
from leads.models import Lead, Post

CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET
USER_AGENT = settings.USER_AGENT
REFRESH_TOKEN = settings.REFRESH_TOKEN
GEMINI_API_KEY = settings.GEMINI_API_KEY
GEMINI_MODEL = settings.GEMINI_MODEL
TARGET_SUBS = settings.TARGET_SUBS
OFFER_TRIGGER_PHRASES = settings.OFFER_TRIGGER_PHRASES
TASK_TRIGGER_PHRASES = settings.TASK_TRIGGER_PHRASES
JOB_CATEGORIES = settings.JOB_CATEGORIES


def categorize_title(title):
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"Here is a job title: {title}. Here is a list of job categories and their descriptions: {JOB_CATEGORIES}. Categorize the job title into one of the provided categories. Return only the category you have settled on."
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        return "Uncategorized"


class Command(BaseCommand):
    help = "Generate leads from Reddit posts"

    def add_arguments(self, parser):
        parser.add_argument(
            "--posts_limit",
            type=int,
            default=10,
            help="Number of posts to fetch per subreddit.",
        )

    def handle(self, *args, **options):
        posts_limit = options["posts_limit"]
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            refresh_token=REFRESH_TOKEN,
            user_agent=USER_AGENT,
        )
        current_time = datetime.datetime.now(datetime.timezone.utc).timestamp()
        one_day_ago = current_time - 86400
        self.stdout.write("=" * 50)
        self.stdout.write("🚀 Starting Reddit Leads Generation...")
        self.stdout.write("=" * 50)
        for target_sub in TARGET_SUBS:
            subreddit = reddit.subreddit(target_sub)
            self.stdout.write(f"📥 Compiling from: {subreddit.display_name}")
            try:
                for submission in subreddit.new(limit=posts_limit):
                    if submission.created_utc < one_day_ago:
                        continue
                    title = submission.title
                    post_trigger = None
                    for trigger in OFFER_TRIGGER_PHRASES:
                        if trigger in title:
                            post_trigger = Post.OFFER
                            break
                    for trigger in TASK_TRIGGER_PHRASES:
                        if trigger in title:
                            post_trigger = Post.TASK
                            break
                    if not post_trigger:
                        continue
                    post_data = {
                        "reddit_post_id": submission.id,
                        "post_title": title,
                        "post_url": submission.url,
                        "subreddit": subreddit.display_name,
                        "post_time": datetime.datetime.fromtimestamp(
                            submission.created_utc, tz=datetime.timezone.utc
                        ),
                        "post_category": categorize_title(title),
                        "post_trigger": post_trigger,
                    }
                    username = submission.author.name if submission.author else None
                    if not username:
                        continue
                    try:
                        lead, created = Lead.objects.get_or_create(
                            reddit_username=username, defaults={"lead_status": Lead.NEW}
                        )
                        Post.objects.create(post_owner=lead, **post_data)
                        self.stdout.write(
                            f"{'Created' if created else 'Updated'} lead: {username}, Post: {submission.id}"
                        )
                    except IntegrityError as e:
                        self.stdout.write(f"Error saving lead/post for {username}: {e}")
            except Exception as e:
                self.stdout.write(
                    f"Error processing subreddit {subreddit.display_name}: {e}"
                )
        self.stdout.write("=" * 50)

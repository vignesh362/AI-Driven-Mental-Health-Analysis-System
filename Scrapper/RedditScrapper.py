import praw

# Reddit Post Class to store properties of a particular post
class RedditPost:
    def __init__(self, title, url, content, comments):
        self.title = title
        self.url = url
        self.content = content
        self.comments = comments

    def __str__(self):
        return f"Title: {self.title}\nURL: {self.url}\nContent: {self.content[:100]}...\nComments: {len(self.comments)} comments"

# Reddit Crawler Class
class RedditCrawler:
    def __init__(self, reddit_client, subreddit_links):
        self.reddit_client = reddit_client
        self.to_visit = subreddit_links  # List of subreddit links to crawl
        self.visited = set()  # To track processed subreddits

    def crawl(self):
        while self.to_visit:
            subreddit_url = self.to_visit.pop(0)  # Fetch the next subreddit link

            # Skip if already visited
            if subreddit_url in self.visited:
                continue
            self.visited.add(subreddit_url)

            # Extract subreddit name from URL
            subreddit_name = self.extract_subreddit_name(subreddit_url)
            print(f"\nCrawling subreddit: {subreddit_name}\n{'='*50}")
            self.crawl_subreddit(subreddit_name)

    def crawl_subreddit(self, subreddit_name):
        try:
            subreddit = self.reddit_client.subreddit(subreddit_name)
            for post in subreddit.new(limit=None):  # Adjust limit as needed
                reddit_post = self.crawl_post(post)
                print(reddit_post)

                # Check for linked subreddits in comments and queue them
                for comment in reddit_post.comments:
                    linked_subreddit = self.extract_subreddit_from_comment(comment)
                    if linked_subreddit and linked_subreddit not in self.visited:
                        self.to_visit.append(f"https://www.reddit.com/r/{linked_subreddit}")
        except Exception as e:
            print(f"Failed to crawl subreddit {subreddit_name}: {e}")

    def crawl_post(self, post):
        post.comments.replace_more(limit=0)  # Flatten comment threads
        comments = [comment.body for comment in post.comments.list()]
        return RedditPost(title=post.title, url=post.url, content=post.selftext, comments=comments)

    def extract_subreddit_name(self, url):
        return url.split('/r/')[-1].strip('/')

    def extract_subreddit_from_comment(self, comment):
        try:
            if "r/" in comment:
                start_idx = comment.index("r/")
                subreddit = comment[start_idx:].split()[0].strip(',.')
                return subreddit
        except Exception:
            return None

# Set up Reddit API client
reddit_client = praw.Reddit(
    client_id="xxxx",
    client_secret="xxxx",
    user_agent="xxxx"
)

# Seed subreddit URLs
seed_subreddits = [
    "https://www.reddit.com/r/depression/",
    "https://www.reddit.com/r/mentalhealth/"
]

# Initialize and start the crawler
reddit_crawler = RedditCrawler(reddit_client, seed_subreddits)
reddit_crawler.crawl()
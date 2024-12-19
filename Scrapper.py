import praw
import time
from datetime import datetime
from kafka import KafkaProducer
import json
import logging

# Rate limits
RATE_LIMITER_PER_MINUTE = 99
REQUEST_INTERVAL = 60 / RATE_LIMITER_PER_MINUTE  # Calculate time between requests
rateLimiterPerKeyword=10 #for each keyword how many subreddit is fetched
rateLimiterPerSubreddit=None

logging.basicConfig(
    filename="systemLogs.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.ERROR
)
# logging.debug("Harmless debug Message")
# logging.info("Just an information")
# logging.warning("Its a Warning")
# logging.error("Did you try to divide by zero")
# logging.critical("Internet is down")
def push_data_to_kafka(data):
    kafka_broker='localhost:29092'
    topic='scraped-data'
    try:
        # Create a Kafka producer instance
        producer = KafkaProducer(
            bootstrap_servers=kafka_broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data to JSON
        )

        producer.send(topic, value=data)


        # Close the producer connection
        producer.flush()
        producer.close()
        logging.info(f"All data successfully sent to Kafka topic '{topic}'")

    except Exception as e:
        logging.error(f"Error while sending data to Kafka: {e}")

# Reddit Post Class to store properties of a particular post
class RedditPost:
    def __init__(self, title, url, content, author, comments, created_utc):
        self.title = title
        self.url = url
        self.content = content
        self.author = author  # Post author
        self.comments = comments
        self.created_utc = created_utc  # Time of the post

    def __str__(self):
        post_time = datetime.utcfromtimestamp(self.created_utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        comments_preview = "\n".join(
            [f"{comment['author']} ({comment['time']}): {comment['body']}" for comment in self.comments[:5]]
        )
        return (f"Title: {self.title}\n"
                f"URL: {self.url}\n"
                f"Author: {self.author}\n"
                f"Posted At: {post_time}\n"
                f"Content: {self.content[:100]}...\n"
                f"Comments: {len(self.comments)} comments\n"
                f"Sample Comments:\n{comments_preview}")


# Reddit Crawler Class
class RedditCrawler:
    def __init__(self, reddit_client, subreddit_links):
        self.reddit_client = reddit_client
        self.to_visit = subreddit_links  # List of subreddit links to crawl
        self.visited = set()  # To track processed subreddits
        self.requests_made = 0  # Track requests to enforce rate limit
        self.last_request_time = time.time()

    def enforce_rate_limit(self):
        if self.requests_made >= RATE_LIMITER_PER_MINUTE:
            time_since_last_request = time.time() - self.last_request_time
            if time_since_last_request < 60:
                sleep_time = 60 - time_since_last_request
                logging.critical(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds...")

                time.sleep(sleep_time)
            self.requests_made = 0  # Reset counter after sleeping
        self.last_request_time = time.time()
        self.requests_made += 1

    def crawl(self):
        while self.to_visit:
            subreddit_url = self.to_visit.pop(0)  # Fetch the next subreddit link

            # Skip if already visited
            if subreddit_url in self.visited:
                continue
            self.visited.add(subreddit_url)

            # Extract subreddit name from URL
            subreddit_name = self.extract_subreddit_name(subreddit_url)
            logging.info(f"\nCrawling subreddit: {subreddit_name}\n{'='*50}")
            self.crawl_subreddit(subreddit_name)

    def crawl_subreddit(self, subreddit_name):
        try:
            subreddit = self.reddit_client.subreddit(subreddit_name)
            for post in subreddit.new(limit=rateLimiterPerSubreddit):  # Adjust limit as needed
                self.enforce_rate_limit()
                reddit_post = self.crawl_post(post)
                # print(reddit_post)
                push_data_to_kafka({"url":reddit_post.url,"content":reddit_post.content,"author":reddit_post.author,"created_utc":reddit_post.created_utc,"type":"post","from":"reddit"})

                # Check for linked subreddits in comments and queue them
                for comment in reddit_post.comments:
                    push_data_to_kafka(comment)
        except Exception as e:
            logging.error(f"Failed to crawl subreddit {subreddit_name}: {e}")

    def crawl_post(self, post):
        post.comments.replace_more(limit=0)  # Flatten comments/ or remove load moreß
        comments = [{
            "url":post.url,
            "content": comment.body,
            "type":"comment",
            "from":"reddit",
            "author": str(comment.author) if comment.author else "Deleted",
            "created_utc": datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        } for comment in post.comments.list()]
        return RedditPost(
            title=post.title,
            url=post.url,
            content=post.selftext,
            author=str(post.author) if post.author else "Deleted",
            comments=comments,
            created_utc=post.created_utc
            )

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
    client_id="IVbyFluVv38VHU_GcU9xbA",
    client_secret="RsZPzB1RcktthdibGALZD_DJDg_OJg",
    user_agent="Maximuzz"
)


def search_subreddits(keyword):
    subreddit_list = []
    subreddits = reddit_client.subreddits.search(keyword, limit=rateLimiterPerKeyword)  # Adjust limit as needed
    for subreddit in subreddits:
        subreddit_list.append("https://www.reddit.com/r/" + subreddit.display_name)
        time.sleep(REQUEST_INTERVAL)  # Enforce rate limit
    return subreddit_list


keyword = "depression"
seed_subreddits = search_subreddits(keyword)
print(seed_subreddits)

# Initialize and start the crawler
reddit_crawler = RedditCrawler(reddit_client, seed_subreddits)
reddit_crawler.crawl()
import praw
import pandas as pd
from datetime import datetime
from src.data_collection.tickers import TickerExtractor

class RedditScrapper():
    def __init__(self, reddit: praw.Reddit, subreddits: list[str]):
        self.reddit = reddit
        self.subreddits = subreddits
        self.ticker_extractor = TickerExtractor()
        
    def collect_subreddit_posts(self, subreddit_name, limit: int = 100) -> pd.DataFrame:
        subreddit = self.reddit.subreddit(subreddit_name)
        posts_data = []
        
        for post in subreddit.hot(limit = limit):
            if post.stickied:
                continue
            
            post_data = {
                'id': post.id,
                'title': post.title,
                'text': post.selftext,
                'score': post.score,
                'upvote_ratio': post.upvote_ratio,
                'num_comments': post.num_comments,
                'created_utc': datetime.fromtimestamp(post.created_utc),
                'subreddit': subreddit_name,
                'url': post.url,
                'tickers': self.ticker_extractor.extract_tickers(post.title + ' ' + post.selftext)
            }
            
            post.comments.replace_more(limit=0)
            comments_text = []
            for comment in post.comments[:10]:
                if hasattr(comment, 'body'):
                    comments_text.append(comment.body)
            
            post_data['top_comments'] = ' '.join(comments_text)
            post_data['comment_tickers'] = self.ticker_extractor.extract_tickers(' '.join(comments_text))
            
            posts_data.append(post_data)
        
        return pd.DataFrame(posts_data)
    
    def extract_tickers(self, text: str):
        if not text:
            return []
    

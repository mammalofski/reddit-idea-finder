
import json
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
   
scraper_api_key = os.getenv('SCRAPER_API_KEY')
   
def fetch_comments_from_post(post_data):
   payload = { 'api_key': scraper_api_key, 'url': 'https://www.reddit.com//r/valheim/comments/15o9jfh/shifte_chest_reason_for_removal_from_valheim/' }
   r = requests.get('https://api.scraperapi.com/', params=payload)
   soup = BeautifulSoup(r.content, 'html.parser')
       # Find all comment elements
   comment_elements = soup.find_all('div', class_='thing', attrs={'data-type': 'comment'})
   # Initialize a list to store parsed comments
   parsed_comments = []
   for comment_element in comment_elements:
       try:
           # Extract relevant information from the comment element, handling potential NoneType errors
           author = comment_element.find('a', class_='author').text.strip() if comment_element.find('a', class_='author') else None
           dislikes = comment_element.find('span', class_='score dislikes').text.strip() if comment_element.find('span', class_='score dislikes') else None
           unvoted = comment_element.find('span', class_='score unvoted').text.strip() if comment_element.find('span', class_='score unvoted') else None
           likes = comment_element.find('span', class_='score likes').text.strip() if comment_element.find('span', class_='score likes') else None
           timestamp = comment_element.find('time')['datetime'] if comment_element.find('time') else None
           text = comment_element.find('div', class_='md').find('p').text.strip() if comment_element.find('div', class_='md') else None
           # Skip comments with missing text
           if not text:
               continue  # Skip to the next comment in the loop
           # Append the parsed comment to the list
           parsed_comments.append({
               'author': author,
               'dislikes': dislikes,
               'unvoted': unvoted,
               'likes': likes,
               'timestamp': timestamp,
               'text': text
           })
       except Exception as e:
           print(f"Error parsing comment: {e}")
   return parsed_comments
   
reddit_query = f"https://www.reddit.com/t/valheim/"
scraper_api_url = f'http://api.scraperapi.com/?api_key={scraper_api_key}&url={reddit_query}'
r = requests.get(scraper_api_url)
soup = BeautifulSoup(r.content, 'html.parser')
articles = soup.find_all('article', class_='m-0')
# Initialize a list to store parsed posts
parsed_posts = []
for article in articles:
   post = article.find('shreddit-post')
   # Extract post details
   post_title = post['post-title']
   post_permalink = post['permalink']
   content_href = post['content-href']
   comment_count = post['comment-count']
   score = post['score']
   
   author_id = post.get('author-id', 'N/A')
   author_name = post['author']
   
   # Extract subreddit details
   subreddit_id = post['subreddit-id']
   post_id = post["id"]
   subreddit_name = post['subreddit-prefixed-name']
   comments = fetch_comments_from_post(post)
   
# Append the parsed post to the list
   parsed_posts.append({
       'post_title': post_title,
       'post_permalink': post_permalink,
       'content_href': content_href,
       'comment_count': comment_count,
       'score': score,
       'author_id': author_id,
       'author_name': author_name,
       'subreddit_id': subreddit_id,
       'post_id': post_id,
       'subreddit_name': subreddit_name,
       'comments': comments
   })
# Save the parsed posts to a JSON file
output_file_path = 'parsed_posts.json'
with open(output_file_path, 'w', encoding='utf-8') as json_file:
   json.dump(parsed_posts, json_file, ensure_ascii=False, indent=2)
    
print(f"Data has been saved to {output_file_path}")
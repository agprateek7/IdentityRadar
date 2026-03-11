import requests

def crawl_reddit(subreddit: str, limit: int = 25) -> list:
    headers = {'User-Agent': 'identity-monitor/1.0'}
    url = f'https://www.reddit.com/r/{subreddit}/new.json?limit={limit}'
    
    response = requests.get(url, headers=headers)
    data = response.json()
    posts = data['data']['children']
    
    results = []
    for post in posts:
        p = post['data']
        # filter only image posts
        if p.get('post_hint') != 'image':
            continue
        image_url = p.get('url_overridden_by_dest', '')
        if not image_url.endswith(('.jpg', '.jpeg', '.png')):
            continue
        results.append({
            'image_url': image_url,
            'page_url': f"https://reddit.com{p['permalink']}"
        })
    return results
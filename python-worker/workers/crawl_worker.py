from crawlers.reddit_crawler import crawl_reddit
from bullmq import Worker
import requests
import asyncio

async def process(job, job_token):
    subreddit = job.data['subreddit']
    site_url = job.data['site_url']
    print(f'[Worker] Picked up job — subreddit: {subreddit}, site: {site_url}')

    images = crawl_reddit(subreddit, limit=25)
    print(f'[Worker] Found {len(images)} images to scan')

    for image in images:
        results = requests.post('http://localhost:8000/search', json={'image_url': image['image_url']})

        for result in results.json():
            print(f'[Worker] Score: {result["score"]:.2f} for image: {image["image_url"]}')
            if result['score'] > 0.6:
                print(f'[Worker] MATCH FOUND! Posting to backend...')
                requests.post('http://localhost:3000/internal/matches', json={
                    'identity_id': result['identity_id'],
                    'image_url': image['image_url'],
                    'page_url': image['page_url'],
                    'score': result['score'],
                    'site_url': site_url
                })

worker = Worker('site-scan', process, {'connection': 'redis://localhost:6379'})

asyncio.get_event_loop().run_forever()
import asyncpraw as praw
import asyncio
import time

async def main():
    reddit = praw.Reddit(
        client_id="bmGuDTdLdtHxQp3E50YezA",
        client_secret="wUjqaisuKEv9DcDM2OtNvbcKOye1NQ",
        #password="PASSWORD",
        user_agent="reddit_gamepost",
        #username="USERNAME",
    )
    
    # 获取 'Genshin_Impact' subreddit 的热门帖子
    subreddit = await reddit.subreddit('Genshin_Impact') 
    new_posts = subreddit.new(limit=10000)
    now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    with open(f"./data/genshin_impact_{now}.txt", "w", encoding="utf-8") as f:
        async for post in new_posts:
            f.write(post.title+"|"+str(post.score)+"\n")
            f.write(post.selftext+"\n")
    
    await reddit.close()

if __name__ == "__main__":
    asyncio.run(main())
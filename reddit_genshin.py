import asyncpraw as praw
import asyncio
import time,json,sys
import threading
import codecs


async def download_post(subreddit_obj:praw.reddit.Subreddit, post_record:dict,lock:threading.Lock):
    random_post = await subreddit_obj.random()
    #print(random_post.id)
    with lock:
        if random_post.id not in post_record.keys():
            post_record.update({random_post.id:random_post.title})
            with open(f"./data/genshin_impact.txt", "a", encoding="utf-8") as f:
                f.write(random_post.title+"||"+str(random_post.score)+"\n")
                f.write(random_post.selftext+"\n")
                f.close()


async def main():
    reddit = praw.Reddit(
        client_id="bmGuDTdLdtHxQp3E50YezA",
        client_secret="wUjqaisuKEv9DcDM2OtNvbcKOye1NQ",
        #password="PASSWORD",
        user_agent="reddit",
        #username="USERNAME",
    )
    
    post_record_lock=threading.Lock()

    # 获取 'Genshin_Impact' subreddit 的热门帖子
    subreddit = await reddit.subreddit('Genshin_Impact') 

    tasks = []

    while True:
        try:
            post_record = json.load(open("./data/post_record.json", "r", encoding="utf-8"))
            for _ in range(20):
                task = asyncio.create_task(download_post(subreddit, post_record, post_record_lock))
                tasks.append(task)
            for task in tasks:
                await task
            #print(post_record)
            with open("./data/post_record.json", "w", encoding="utf-8") as f:
                json.dump(post_record, f)
                f.close()
            print(post_record)
        except Exception as e:
            print("Exception!! "+e.__str__())
            time.sleep(120)
            continue


if __name__ == "__main__":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    asyncio.run(main())
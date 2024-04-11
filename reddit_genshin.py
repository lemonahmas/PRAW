import asyncpraw
import asyncio
import time,json,sys
import codecs


async def download_post(subreddit_obj:asyncpraw.reddit.Subreddit, post_record:dict):
    random_post = await subreddit_obj.random()
    #print(random_post.id)
    if random_post.id not in post_record.keys():
        post_record.update({random_post.id:random_post.title})
        with open(f"./data/genshin_impact.txt", "a", encoding="utf-8") as f:
            f.write(random_post.title+"||"+str(random_post.score)+"\n")
            f.write(random_post.selftext+"\n")


async def main():
    reddit = asyncpraw.Reddit(
        client_id="bmGuDTdLdtHxQp3E50YezA",
        client_secret="wUjqaisuKEv9DcDM2OtNvbcKOye1NQ",
        #password="PASSWORD",
        user_agent="reddit",
        #username="USERNAME",
    )
    

    # 获取 'Genshin_Impact' subreddit 的热门帖子
    subreddit = await reddit.subreddit('Genshin_Impact') 
    post_record = json.load(open("./data/post_record.json", "r", encoding="utf-8"))

    while True:
        try:
            tasks = []
            for _ in range(5):
                task = asyncio.create_task(download_post(subreddit, post_record))
                tasks.append(task)
            await asyncio.gather(*tasks)
            #print(post_record)
            with open("./data/post_record.json", "w", encoding="utf-8") as f:
                json.dump(post_record, f)
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+str(post_record)+"\n")
        except Exception as e:
            print("Exception!! "+e.__str__()+" | let's sleep 10 minutes")
            await asyncio.sleep(600)


if __name__ == "__main__":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    asyncio.run(main())
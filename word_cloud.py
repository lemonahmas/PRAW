import matplotlib.pyplot as plt
from wordcloud import WordCloud

with open('./data/genshin_impact_2024-04-09_17-40-55.txt', 'r', encoding='utf-8') as f:
    words = f.read()
#words = 'one two three four five'

wordcloud = WordCloud(width = 1920, height = 1080).generate(words)

wordcloud.to_file('word_cloud.png')
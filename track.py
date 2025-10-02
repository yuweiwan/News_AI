from datetime import datetime
import os
import json
from collections import defaultdict
from llm.processor import NewsProcessor

def track_entity_news(track_words, all_news):
    """
    track_words: dict, key: entity, value: list of indicator words
    all_news: list of news dicts, each news dict has at least 'title', 'summary', 'time'
    Returns: dict, key: entity, value: list of news dicts (sorted by time desc)
    """

    result = {}
    for entity, indicators in track_words.items():
        matched_news = []
        used_titles = []
        for item in all_news:
            title = item.get('title', '') or ''
            summary = item.get('summary', '') or ''
            # 检查指示词是否出现在title或summary中（区分大小写/不区分？这里不区分）
            for word in indicators:
                if word in title:
                    if item not in matched_news and title not in used_titles:
                        matched_news.append(item)
                        used_titles.append(title)
                        break  # 一条新闻只需匹配一次
        # 按time倒序排列
        matched_news_sorted = sorted(
            matched_news,
            key=lambda x: x.get('time', ''),
            reverse=True
        )
        result[entity] = matched_news_sorted
    return result




def load_all_today_news(data_dir="data"):
    """
    从data目录下每个子文件夹的today_news.json中读取新闻，合并成一个大的list of dict
    """
    all_news = []
    if not os.path.exists(data_dir):
        return all_news
    for subdir in os.listdir(data_dir):
        subdir_path = os.path.join(data_dir, subdir)
        if os.path.isdir(subdir_path):
            news_path = os.path.join(subdir_path, "today_news.json")
            if os.path.exists(news_path):
                try:
                    with open(news_path, "r", encoding="utf-8") as f:
                        news_list = json.load(f)
                        if isinstance(news_list, list):
                            # INSERT_YOUR_CODE
                            # 只保留title和summary两个key
                            '''
                            news_list = [
                                {
                                    "title": news.get("title", ""),
                                    "summary": news.get("summary", "")
                                }
                                for news in news_list
                                if isinstance(news, dict)
                            ]
                            '''
                            all_news.extend(news_list)
                except Exception:
                    pass  # 忽略无法解析的文件
    # print(all_news)
    return all_news

with open("tracking/track_words.json", "r", encoding="utf-8") as f:
    test_dict = json.load(f)

all_news = load_all_today_news()
json_str = json.dumps(all_news, ensure_ascii=False, indent=4)
with open('all.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_str)

'''
ali_api_key = "sk-f346edcf0c5b441487fb8056e2b5aa50"
processor = NewsProcessor(ali_api_key)
extract_ = processor.process_subpage(str(all_news))
print(extract_)
json_str = json.dumps(extract_, ensure_ascii=False, indent=4)
with open('tracking/track_words.json', 'w') as json_file:
    json_file.write(json_str)
'''

track_result = track_entity_news(test_dict, all_news)
json_str = json.dumps(track_result, ensure_ascii=False, indent=4)
with open('track_result.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_str)
print(track_result)

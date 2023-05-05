import requests
import json
from bs4 import BeautifulSoup as bs
from pprint import pprint

session = requests.Session()
user_agent = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'

def get_problems():
    url = "https://leetcode.com/api/problems/all/"

    headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    resp = session.get(url, headers = headers, timeout = 10)
    q_list = []
    question_list = json.loads(resp.content.decode('utf-8'))

    for question in question_list['stat_status_pairs']:
        if question['paid_only']:
            continue
        question_id = question['stat']['question_id']
        question_slug = question['stat']['question__title_slug']
        question_status = question['status']

        level = question['difficulty']['level']
        q_list.append({"id": question_id, "slug": question_slug, "status": question_status, "level": level})
    
    return q_list
get_problems()
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

        level = question['difficulty']['level']
        q_list.append({"id": question_id, "slug": question_slug, "level": level})
    
    return q_list



def get_details(q_list):
    items = []

    for q in q_list:
        data = {"operationName":"questionData","variables":{"titleSlug":q["slug"]},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}
        r = requests.post('https://leetcode.com/graphql', json = data).json()
        soup = bs(r['data']['question']['content'], 'lxml')
        title = r['data']['question']['title']
        solution = r['data']['question']['solution']
        print(f"Fetched {title}.")
        question =  soup.get_text().replace('\n',' ')
        item = {"id": q['id'], "level": q['level'], "title":title, "question":question, "solution":solution}
        items.append(item)
    return items
q_list = get_problems()
data = get_details(q_list)

with open("leetcode.json", "w") as outfile:
    json.dump(data, outfile)


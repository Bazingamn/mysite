import json
import requests
import pymysql
import re

header = {
        'User-Agent': 'Mozilla/5.0(compatible;MSIE7.0;WindowsNT5.1)',
        'Connection': 'keep - alive',
        }

def parse_context(url):
    data = requests.get(url)
    if data.status_code == 200:
        context = data.text
    pattern = re.compile('<.*?id="endText".*?>(.*?)</div>', re.S)
    divs = re.findall(pattern, context)
    pattern = re.compile('(?<=<p>)[\s\S]*?(?=</p>)', re.S)
    items = re.findall(pattern, str(divs))
    text = '\n\n'.join(items)
    # print(text)
    # print(len(text))
    return text

def parse(url):
    wbdata = requests.get(url, headers=header).text
    data = json.loads(wbdata)
    news = data['T1348647853363']
    for item in news:
        digest = item['digest']
        mtime = item['mtime']
        title = item['title']
        source = item['source']
        imgsrc = item['imgsrc']
        try:
            texturl = item['url_3w']
            url = item['url']
            context = parse_context(texturl)
        except:
            url = ''
            texturl = ''
            context = ''
        news_data ={
            'title': title,
            'source': source,
            'digest': digest,
            'content': context,
            'pub_time': mtime,
            'avatar': imgsrc,
        }
        print(news_data)
        write_to_mysql(news_data)

def write_to_mysql(data):
    db = pymysql.connect(host='localhost', user='root', password='123456', db='mysite', charset='utf8')
    cur = db.cursor()
    sqlc = '''
        insert into news_news
        values(null,%s,%s,%s,%s,%s,%s)
    '''
    try:
        if cur.execute(sqlc, (
                data["title"],
                data["source"],
                data["content"],
                data["pub_time"],
                data["avatar"],
                data["digest"],
                )):
            print('Successful')
            db.commit()
    except  Exception as e:
        print(e)
        print('Failed')
        db.rollback()
    cur.close()
    db.close()

def main():
    url = 'http://c.m.163.com/nc/article/headline/T1348647853363/0-100.html'
    parse(url)

if __name__ == '__main__':
    main()
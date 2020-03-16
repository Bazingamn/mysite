import requests
import re


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}

def parse_context(url):
    data = requests.get(url)
    if data.status_code == 200:
        context = data.text
    # html = etree.HTML(context)
    # # html = etree.parse(context, etree.HTMLParser())
    # result = etree.tostring(html)
    # print(result.decode('utf-8'))
    pattern = re.compile('<.*?id="endText".*?>(.*?)</div>', re.S)
    divs = re.findall(pattern, context)
    pattern = re.compile('(?<=<p>)[\s\S]*?(?=</p>)',re.S)
    items = re.findall(pattern, str(divs))
    content = '\n\n'.join(items)
    print(content)
    print(len(content))

def main():
    url = 'https://news.163.com/20/0313/20/F7KHU6CH00019B3E.html'
    parse_context(url)

if __name__ == '__main__':
    main()
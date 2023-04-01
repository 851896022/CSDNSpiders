import os
import re
import weasyprint
import requests
from bs4 import BeautifulSoup
# 创建新文件夹的路径
savedir = "CSDN"


def sanitize_filename(filename):
    # 匹配不能用作文件名的字符
    illegal_chars = r'[\/\\\:\*\?"<>\|]'
    # 将文件名中的非法字符替换为空格
    sanitized = re.sub(illegal_chars, ' ', filename)
    return sanitized

def getarticle(url='null'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    # print(response.url)
    # print(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')
    element = soup.find(id='article_content')
    tittle = soup.find(id='articleContentId').get_text()
    #太短的不存
    if len(str(element.text)) > 100:
        pdf_bytes = weasyprint.HTML(string=str(element)).write_pdf()
        # 将PDF保存到文件
        with open(str(savedir+'/'+sanitize_filename(tittle)+'.pdf'), 'wb') as f:
            f.write(pdf_bytes)
        print(tittle)


def getUrls():
    payload = {'componentIds': 'www-blog-recommend'}
    cookies = dict(dc_session_id="10_1678689479262.609164", dc_sid="a596e9ba75cdcd367f6b9f86e020dcbc",
                   uuid_tt_dd="10_19709270910-1678689479262-743868")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get('https://cms-api.csdn.net/v1/web_home/select_content', params=payload, headers=headers,
                            cookies=cookies)
    data = response.json()
    infolist = data["data"]["www-blog-recommend"]["info"]
    for info in infolist:
        url = info["extend"]["url"]
        try:
            getarticle(url)
        except:
            pass

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # 如果路径不存在，创建新路径
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    for i in range(0, 1):
        getUrls()

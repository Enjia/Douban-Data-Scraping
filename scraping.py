from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import argparse

base_url_suffix = "&sort=time&rating=all&mode=grid&type=all&filter=all"

findMoviesTitle = re.compile(r'<em>(.*)</em>')
findMoviesLink = re.compile(r'<a class="" href="(.*?)">')
findMoviesInfo = re.compile(r'<li class="intro">(.*)</li>')

findBookTitle = re.compile(r'<a href="(.*?)" title="(.*?)">')
findBookSubTitle = re.compile(r'<span style="font-size:12px;">(.*)</span>')
findPubInfo = re.compile(r'<div class="pub">((?:.|\n)*?)</div>')

def scrape_douban_data(base_url, agent, cookie, num_items, data_type, save_path):
    if data_type == "books":
        print("Scraping books information which you tagged...")
        data_list = getBooksData(base_url, agent, cookie, num_items)
    elif data_type == "movies":
        print("Scraping movies information which you tagged...")
        data_list = getMoviesData(base_url, agent, cookie, num_items)
    else:
        raise ValueError("Input data_type is not supported")

    saveData(data_list, num_items, save_path, data_type)
 
def getMoviesData(base_url, agent, cookie, num_items):
    data_list = []
    for i in range(0, num_items // 15 + 1):
        url = base_url + str(i * 15) + base_url_suffix
        html = askURL(url, agent, cookie)

        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item comment-item"):
            data = []
            item = str(item)
            movie_title = re.findall(findMoviesTitle, item)
            if movie_title:
                if " / " in movie_title[0]:
                    res = movie_title[0].split("/")
                    chinese_title = res[0]
                    foreign_title = res[1]
                    data.append(chinese_title)
                    data.append(foreign_title)
                else:
                    data.append(movie_title[0])
                    data.append(' ')
            else:
                data.append(' ')
            
            movie_link = re.findall(findMoviesLink, item)
            if movie_link:
                data.append(movie_link[0])
            else:
                data.append(' ')

            movie_info = re.findall(findMoviesInfo, item)
            if movie_info:
                data.append(movie_info[0])
            else:
                data.append(' ')
            
            data_list.append(data)
    return data_list

def getBooksData(base_url, agent, cookie, num_items):
    data_list = []
    for i in range(0, num_items // 15 + 1):
        url = base_url + str(i * 15) + base_url_suffix
        html = askURL(url, agent, cookie)

        soup = BeautifulSoup(html,"html.parser")
        for item_book in soup.find_all('li', class_="subject-item"):
            data = []
            item_book = str(item_book)
 
            book_title = re.findall(findBookTitle, item_book)
            data.append(book_title[0][1])

            subtitle = re.findall(findBookSubTitle, item_book)
            if subtitle:
                data.append(subtitle[0].replace(" : ", ""))
            else:
                data.append(" ")
            
            Link = str(book_title[0]).split(" ")[0].strip("('").strip('"')
            data.append(Link)
            
            pub_info = re.findall(findPubInfo, item_book)
            pub_info = str(pub_info[0]).strip().replace("\n", "")
            data.append(pub_info)

            data_list.append(data)
    return data_list

def askURL(url, agent, cookie):
    '''
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "cookie": 'douban-fav-remind=1; __yadk_uid=9oXAsFrLQ5kHof4ieaA27h6IMpl3uP5M; push_doumail_num=0; _vwo_uuid_v2=D03A37D34AB21532F519D1879F0F65864|25d2dbf833ef434cf48ee75f41788714; ll="118172"; __utmc=30149280; __utmv=30149280.9170; _ga_PRH9EWN86K=GS1.2.1728278109.1.0.1728278109.0.0.0; bid=LWVguVbLCfY; _ga_Y4GN1R87RG=GS1.1.1733056614.4.1.1733056672.0.0.0; viewed="36759548_35879791"; dbcl2="91701019:gx2j2JdTcO0"; ck=uKSx; frodotk_db="19bbdf47b309c6204d339dd7191d5260"; _ga=GA1.1.558226193.1669946499; _ga_RXNMP372GL=GS1.1.1734255801.18.0.1734255803.58.0.0; push_noty_num=0; _pk_id.100001.8cb4=13b90b8bddf255eb.1734592702.; __utma=30149280.558226193.1669946499.1735612732.1735624294.191; __utmz=30149280.1735624294.191.37.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1735626936%2C%22https%3A%2F%2Fbook.douban.com%2Fsubject%2F35241192%2F%22%5D; _pk_ses.100001.8cb4=1; __utmt=1; __utmb=30149280.4.10.1735624294'
    }
    '''
    head = {
        "User-Agent": agent,
        "cookie": cookie
    }
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html
 
def saveData(data_list, num_items, save_path, data_type):
    print("Saving info to sheet....")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet(save_path, cell_overwrite_ok=True)
    
    if data_type == "books":
        col = ("书名/Title", "副标题/Subtitle", "链接/Link", "出版信息(作者/译者/出版社/出版时间/页数/价格)/Pub info(/Author/Translator/Press/Pub time/Pages/Price)")
    elif data_type == "movies":
        col = ("影片中文名/Chinese name", "影片其他名/Other name", "影片链接/Link", "影片信息/Info")
    else:
        raise ValueError("Input data_type is not supported")
    
    for i in range(0, 4):
        sheet.write(0, i, col[i])
    for i in range(0, num_items):
        data = data_list[i]
        for j in range(0, 4):
            sheet.write(i + 1, j, data[j])
    book.save(save_path)

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Scraping movies and books information from douban')
    parse.add_argument('--data_type', type=str, help='movies or books') 
    parse.add_argument('--num_items', type=int, help='amount of your movies or books in to-watch-list')
    parse.add_argument('--base_url', type=str, help='base url of your douban home page about books or movies')
    parse.add_argument('--save_path', type=str, help='path of xxx.xls to save scraping result')
    parse.add_argument('--agent', type=str, help='agent of your web brownser')
    parse.add_argument('--cookie', type=str, help='cookie of your web brownser')
    args = parse.parse_args()

    print("=" * 60)
    print("Start scraping...")
    scrape_douban_data(
        args.base_url, 
        args.agent, 
        args.cookie, 
        args.num_items, 
        args.data_type,
        args.save_path)
    print("Finish scraping...")
    print("=" * 60)

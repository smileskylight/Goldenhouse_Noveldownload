# 下載套件
def download():
    import subprocess
    import sys
    from time import sleep

    # 要檢查的套件列表
    required_packages = [
        "re",
        "requests",
        "json",
        "os",
        "pprint",
        "bs4",
        "fake_useragent",
        "lxml",
        "ffmpeg",
        "asyncio",
        "aiohttp"
        # 添加其他套件的名稱
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"缺少套件: {', '.join(missing_packages)}")
        req = input("是否下載套件 y/n : ")
        if req.lower() == "y":
            subprocess.call(["pip", "install"] + missing_packages)
        elif req.lower() == "n":
            print("拒絕下載即將關閉程式")
            sleep(5)
            sys.exit()
    else:
        return


import json
import os
import re
import subprocess
import sys
from pprint import pprint
from time import sleep
import asyncio
import aiohttp
import lxml
import requests as rq
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent


# 聲明
def declare():
    print(
        " 本產品僅供學術交流使用\n",
        "請勿連續不間斷輸入指令,造成被鎖ip,如有違反後果自負",
    )
    print(
        ' 為避免造成網站癱瘓,nl小說編號列表會預先下載成"小說編號列表.txt"檔案再做判讀'
    )


# 指令查詢
def start():
    print("=" * 30)
    print(" 欲查詢指令請輸入 help")


# 操作列表
def sutch():
    enter = input(" 請輸入指令 : ")
    if enter == "help":  # 指令表
        help()
        print()
        sutch()
    elif enter == "nl":  # 小說編號列表
        check = input(" 是否更新列表y/n :")
        if check == "y" or check == "Y":
            nl()
            nl_read()
            print()
            sutch()
        elif check == "n" or check == "N":
            if os.path.isfile("小說編號列表.txt"):
                nl_read()
                print()
                sutch()
            else:
                nl()
                nl_read()
                print()
                sutch()
    elif enter == "nh":  # 查詢小說編號
        txt_file_path = os.path.join(".", "小說編號列表.txt")
        if os.path.exists(txt_file_path):
            nh()
            print()
            sutch()
        else:
            nl()
            nh()
            print()
            sutch()
    elif enter == "nt":  # 小說目錄
        nt()
        print()
        sutch()
    elif enter == "ntnu":  # 小說章節連結
        ntnu()
        print()
        sutch()
    elif enter == "nva":  # 小說全本觀看
        nva()
        print()
        sutch()
    elif enter == "nd":  # 全本下載
        nd()
        print()
        sutch()
    # elif enter == "ndv":  # 全本下載影片專用
    #     nd()
    #     print()
    #     sutch()
    elif enter == "nsd":  # 全本下載有聲書
        nsd()
        print()
        sutch()
    elif enter == "close" or enter =="CLOSE":  # 關閉程式
        close()
    else:
        print("輸入錯誤,查詢指令請輸入help")
        print()
        sutch()


# 指令表
def help():
    print(
        " nl:小說編號列表\n",
        "nh:查詢小說編號\n",
        "nt:小說目錄\n",
        "ntnu:小說章節連結\n",
        "nva:小說全本觀看\n",
        "nd:全本下載\n",
        "ndv:全本下載製作有聲書專用(與nd工能合併暫不提供服務)\n",
        "nsd:全本下載有聲書(待開發)\n",
        "colse:關閉程式",
    )
    print("=" * 30)
    print(" 如無法執行請確認https://tw.hjwzw.com是否可以訪問")


# nl:小說編號列表
def nl():
    novel_list_pages = range(1, 1450)
    loop = asyncio.get_event_loop()

    async def send_req(url):
        res = await loop.run_in_executor(None, rq.get, url)
        return res.text

    async def main():
        tasks = []
        ua = UserAgent()
        for page in novel_list_pages:
            url = f"https://tw.hjwzw.com/List/all__{page}"
            headers = {"user-agent": ua.random}
            task = loop.create_task(send_req(url))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        with open("小說編號列表.txt", "w", encoding="utf-8") as output_file:
            for result in results:
                root = bs(result, 'lxml')
                title_spans = root.find_all("span", class_="wd10")

                novel_list = []
                href_list = []

                for span in title_spans:
                    a_tag = span.find("a")
                    if a_tag:
                        novel_list.append(a_tag.text)
                        href_list.append(a_tag["href"])

                href_numbers = [re.search(r"/Book/(\d+)", href).group(1) for href in href_list]

                formatted_data = [
                    f"書籍名稱: {title.ljust(20)}\n書籍編號: {number}\n"
                    for title, number in zip(novel_list, href_numbers)
                ]

                for data in formatted_data:
                    output_file.write(data)
                    output_file.write("\n")
                    print(data)
                    
        print("列表更新完畢")

    loop.run_until_complete(main())


# 讀取小說資料
def nl_read():
    with open("小說編號列表.txt", "r", encoding="utf-8") as file:
        novel_read = file.read()
        print(novel_read)


# 查詢小說編號


def nh():
    with open("小說編號列表.txt", "r", encoding="utf-8") as file:
        novel_read = file.read()
        bookname = input(" 請輸入書籍名稱: ")

        # 修改正則表達式，使用圓括號捕獲書名和編號
        matches = re.findall(
            f"書籍名稱: ({bookname}.*?)書籍編號: (\\d+)", novel_read, re.DOTALL
        )

        if matches:
            # 輸出所有匹配的小說及編號
            for match in matches:
                book_title = match[0].strip()  # 取得捕獲的書名，清理空白字符
                book_number = match[1].strip()  # 取得捕獲的編號，清理空白字符
                print(f"書籍名稱: {book_title}\n書籍編號: {book_number}")
        else:
            print(f"未收錄本書")


# nt:小說目錄
def nt():
    novel_numbers = input(" 請輸入小說編號 : ")
    # 使用假UA
    ua = UserAgent()
    my_header = {"user-agent": ua.random}
    url = f"https://tw.hjwzw.com/Book/Chapter/{novel_numbers}"

    # get方法 加上 假UA 取得 html
    ans = rq.get(url, headers=my_header)

    # #匯入beautiful soup ,使用lxml 編譯器
    root = bs(ans.text, "lxml")

    # 抓標題
    pattern = re.compile(r"/Book/Read/(\d+),(\d+)")
    title = root.find_all("a", href=pattern)
    titles = [title.string for title in root.find_all("a", href=pattern)]
    pprint(titles)


# ntnu:小說章節連結
def ntnu():
    novel_numbers = input(" 請輸入小說編號 : ")
    # 使用假UA
    ua = UserAgent()
    my_header = {"user-agent": ua.random}
    url = f"https://tw.hjwzw.com/Book/Chapter/{novel_numbers}"

    # get方法 加上 假UA 取得 html
    ans = rq.get(url, headers=my_header)

    # #匯入beautiful soup ,使用lxml 編譯器
    root = bs(ans.text, "lxml")

    # 抓標題
    pattern = re.compile(r"/Book/Read/(\d+),(\d+)")
    title = root.find_all("a", href=pattern)
    titles = [title.string for title in root.find_all("a", href=pattern)]

    # 抓網址

    href = ["https://tw.hjwzw.com" + tag["href"] for tag in title]
    pprint(list(zip(titles, href)))


# nva:小說全本觀看
def nva():
    novel_numbers = input(" 請輸入小說編號 : ")
    # 使用假 ua
    ua = UserAgent()
    my_header = {"user-agent": ua.random}
    # get方法 加上 假UA 取得 html
    url = f"https://tw.hjwzw.com/Book/Chapter/{novel_numbers}"
    ans = rq.get(url, headers=my_header)

    root = bs(ans.text, "lxml")
    # 抓標題
    pattern = re.compile(r"/Book/Read/(\d+),(\d+)")
    title = root.find_all("a", href=pattern)
    # 抓網址
    hrefs = ["https://tw.hjwzw.com" + tag["href"] for tag in title]

    for href in hrefs:

        # 使用假 ua 和 get 方法抓取網站並印出 text
        response = rq.get(href, headers=my_header)
        root = bs(response.text, "lxml")

        # 抓標題
        title = root.find("h1").string
        print(title)

        # 抓內容
        novel = root.find_all(
            "div",
            style="font-size: 20px; line-height: 30px; word-wrap: break-word; table-layout: fixed; word-break: break-all; width: 750px; margin: 0 auto; text-indent: 2em;",
        )

        pattern = re.compile(r"[\d\u4e00-\u9fff，,。?!“”]+")

        for tag in novel:
            text = tag.get_text()  # 提取標籤中的文本
            matches = pattern.findall(text)
            print(type(matches))
            for match in matches:
                print(match)
                sleep(0.02)


# nd:全本下載
def nd():
    async def fetch(session, url, headers, max_retries=3):
        for attempt in range(max_retries):
            try:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.text()
            except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
                if attempt < max_retries - 1:
                    print(f"下載 {url} 失敗，重試中... ({attempt+1}/{max_retries})")
                else:
                    print(f"下載 {url} 失敗，已重試 {max_retries} 次。")
                    raise e

    async def download_chapter(session, href, headers, words_to_delete, novel_name, max_retries=3):
        retry_count = 0
        while retry_count < max_retries:
            try:
                html = await fetch(session, href, headers)
                root = bs(html, "lxml")

                # 抓標題
                title = root.find("h1")
                if title is None:
                    raise AttributeError("'NoneType' object has no attribute 'string'")
                chapter_title = title.string.strip()
                
                success_message = f"{chapter_title} 下載成功"
                print(success_message)

                # 抓內容
                content_divs = root.find_all(
                    "div",
                    style="font-size: 20px; line-height: 30px; word-wrap: break-word; table-layout: fixed; word-break: break-all; width: 750px; margin: 0 auto; text-indent: 2em;",
                )

                chapter_content = []
                for tag in content_divs:
                    text = tag.get_text()  # 提取標籤中的文本

                    for word in words_to_delete + [chapter_title, novel_name]:
                        text = text.replace(word, "")

                    pattern = re.compile(r"[\d\u4e00-\u9fff…，,。?!、！《》“”？：]+")
                    matches = pattern.findall(text)
                    chapter_content.extend(matches)
                    chapter_content.append("")  # 每章節之間空一行

                return chapter_content

            except (aiohttp.ClientError, aiohttp.ClientResponseError, AttributeError) as e:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"下載 {href} 失敗，重試中... ({retry_count}/{max_retries})")
                else:
                    print(f"下載 {href} 失敗，已重試 {max_retries} 次，將跳過該章節。")
                    break  # 跳出重試循環，進行下一章節的下載
        return []

    async def download():
        words_to_delete = ["請記住本站域名", "黃金屋","辰迷書友官方","2579","最穩定，給力文學網","《沸騰文學網》網花","沸騰文學網歡迎您,","為了方便您閱讀，請記住“89文學網”","《沸騰文學網》網7","《沸騰文學網》網","大文學"]
        novel_numbers = input("請輸入小說編號: ")

        ua = UserAgent()
        headers = {"user-agent": ua.random}
        url = f"https://tw.hjwzw.com/Book/Chapter/{novel_numbers}"

        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url, headers)
            root = bs(html, "lxml")
            novel_name = root.find("h1").string

            pattern = re.compile(r"/Book/Read/(\d+),(\d+)")
            title_tags = root.find_all("a", href=pattern)
            hrefs = ["https://tw.hjwzw.com" + tag["href"] for tag in title_tags]
            chapter_titles = [tag.get_text(strip=True) for tag in title_tags]

            chapters_content = await asyncio.gather(*[
                download_chapter(session, href, headers, words_to_delete, novel_name)
                for href in hrefs
            ])

            with open(f"{novel_name}.txt", "w", encoding="utf-8") as output_file:
                for title, content in zip(chapter_titles, chapters_content):
                    if content:
                        output_file.write(f"{title}\n\n")
                        output_file.write("\n".join(content) + "\n")
                        output_file.write("=" * 30 + "\n")

    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download())

# # ndv:全本下載做影片用
# def ndv():
#     words_to_delete = ["請記住本站域名", "黃金屋"]
#     novel_numbers = input(" 請輸入小說編號 : ")
#     # 使用假 ua
#     ua = UserAgent()
#     my_header = {"user-agent": ua.random}
#     url = f"https://tw.hjwzw.com/Book/Chapter/{novel_numbers}"
#     # get方法 加上 假UA 取得 html
#     ans = rq.get(url, headers=my_header)

#     root = bs(ans.text, "lxml")
#     # 抓小說名
#     novel_name = root.find("h1").string

#     # 抓標題
#     pattern = re.compile(r"/Book/Read/(\d+),(\d+)")
#     title = root.find_all("a", href=pattern)
#     # 抓網址
#     hrefs = ["https://tw.hjwzw.com" + tag["href"] for tag in title]

#     # 打開檔案以寫入模式
#     with open(f"{novel_name}vidio.txt", "w", encoding="utf-8") as output_file:
#         for href in hrefs:
#             # 使用假 ua 和 get 方法抓取網站並印出 text
#             response = rq.get(href, headers=my_header)
#             root = bs(response.text, "html.parser")

#             # 抓標題
#             h1_tag = root.find("h1")
#             if h1_tag and h1_tag.string:
#                 chapter_title = h1_tag.string.strip()
#                 # 將章節標題添加到需要删除的詞列表中
#                 dynamic_words_to_delete = words_to_delete + [chapter_title,novel_name]
#                 print(f"{chapter_title} 下載成功")

#                 # 抓內容
#                 content_divs = root.find_all(
#                     "div",
#                     style="font-size: 20px; line-height: 30px; word-wrap: break-word; table-layout: fixed; word-break: break-all; width: 750px; margin: 0 auto; text-indent: 2em;",
#                 )

#                 for tag in content_divs:
#                     text = tag.get_text()  # 提取標籤中的文本

#                     # 刪除匹配 dynamic_words_to_delete 的詞
#                     for word in dynamic_words_to_delete:
#                         text = text.replace(word, "")

#                     pattern = re.compile(r"[\d\u4e00-\u9fff…，,。?!、！《》“”？：]+")
#                     matches = pattern.findall(text)
#                     for match in matches:
#                         output_file.write(f"{match}\n")
#                     output_file.write("\n")  # 每章節之間空一行

#                 sleep(0.2)
#                 output_file.write("=" * 30 + "\n")  # 每章小說之間用等號分隔

def close():
    sys.exit()


# 主程式
if __name__ == "__main__":
    download()
    declare()
    start()
    sutch()

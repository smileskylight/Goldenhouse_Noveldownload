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
        "ffmpeg"
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


download()
import json
import os
import re
import subprocess
import sys
from pprint import pprint
from time import sleep

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
    elif enter == "ndv":  # 全本下載影片專用
        nd()
        print()
        sutch()
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
        "ndv:全本下載製作有聲書專用\n",
        "nsd:全本下載有聲書(待開發)\n",
        "colse:關閉程式",
    )
    print("=" * 30)
    print(" 如無法執行請確認https://tw.hjwzw.com是否可以訪問")


# nl:小說編號列表
def nl():
    # 使用假UA
    ua = UserAgent()
    my_header = {"user-agent": ua.random}
    novel_list_pages = range(1, 1412)

    # 疊代每個頁面
    for novel_list_page in novel_list_pages:
        url = f"https://tw.hjwzw.com/List/all__{novel_list_page}"

        # get方法 加上 假UA 取得 html
        ans = rq.get(url, headers=my_header)

        # print(ans.encoding)
        # print(ans.text)

        # 匯入beautiful soup ,使用lxml 編譯器
        root = bs(ans.text, "lxml")

        # 抓標題
        title = root.find_all("span", class_="wd10")
        novel_list = []
        for span in title:
            a_tag = span.find("a")
            if a_tag:
                novel_list.append(a_tag.text)

        # 抓網址

        # 提取<a>標籤中的href屬性
        href_attributes = [span.find("a")["href"] for span in title if span.find("a")]
        # 使用正規表達式匹配數字
        href = [re.search(r"/Book/(\d+)", href).group(1) for href in href_attributes]
        formatted_data = [
            f"書籍名稱: {title.ljust(20)}\n書籍編號: {number}\n"
            for title, number in zip(novel_list, href)
        ]

        # 印出結果
        for item in formatted_data:
            with open("小說編號列表.txt", "a", encoding="utf-8") as output_file:
                output_file.write(item)
                output_file.write("\n")
    print("列表更新完畢")


# 讀取小說資料
def nl_read():
    with open("小說編號列表.txt", "r", encoding="utf-8") as file:
        novel_read = file.read()
        print(novel_read)


# 查詢小說編號
import re


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
    words_to_delete = ["請記住本站域名", "黃金屋"]
    novel_numbers = input(" 請輸入小說編號 : ")
    # 使用假 ua
    ua = UserAgent()
    my_header = {"user-agent": ua.random}
    url = f"https://tw.hjwzw.com/Book/Chapter/{novel_numbers}"
    # get方法 加上 假UA 取得 html
    ans = rq.get(url, headers=my_header)

    root = bs(ans.text, "lxml")
    # 抓小說名
    novel_name = root.find("h1").string

    # 抓標題
    pattern = re.compile(r"/Book/Read/(\d+),(\d+)")
    title = root.find_all("a", href=pattern)
    # 抓網址
    hrefs = ["https://tw.hjwzw.com" + tag["href"] for tag in title]

    # 打開檔案以寫入模式
    with open(f"{novel_name}.txt", "w", encoding="utf-8") as output_file:
        for href in hrefs:

            # 使用假 ua 和 get 方法抓取網站並印出 text
            response = rq.get(href, headers=my_header)
            root = bs(response.text, "lxml")

            # 抓標題
            title = root.find("h1").string
            output_file.write(f"{title}\n")
            # print(f"{title}下載成功")
            if title and title.string:
                chapter_title = title.string.strip()
                # 将章节标题添加到需要删除的词列表中
                dynamic_words_to_delete = words_to_delete + [chapter_title,novel_name]
                print(f"{chapter_title} 下載成功")

                # 抓內容
                content_divs = root.find_all(
                    "div",
                    style="font-size: 20px; line-height: 30px; word-wrap: break-word; table-layout: fixed; word-break: break-all; width: 750px; margin: 0 auto; text-indent: 2em;",
                )

                for tag in content_divs:
                    text = tag.get_text()  # 提取標籤中的文本

                    # 刪除匹配 dynamic_words_to_delete 的詞
                    for word in dynamic_words_to_delete:
                        text = text.replace(word, "")

                    pattern = re.compile(r"[\d\u4e00-\u9fff…，,。?!、！《》“”？：]+")
                    matches = pattern.findall(text)
                    for match in matches:
                        output_file.write(f"{match}\n")
                    output_file.write("\n")  # 每章節之間空一行

                sleep(0.2)
                output_file.write("=" * 30 + "\n")  # 每章小說之間用等號分隔

# ndv:全本下載做影片用
def ndv():
    words_to_delete = ["請記住本站域名", "黃金屋"]
    novel_numbers = input(" 請輸入小說編號 : ")
    # 使用假 ua
    ua = UserAgent()
    my_header = {"user-agent": ua.random}
    url = f"https://tw.hjwzw.com/Book/Chapter/{novel_numbers}"
    # get方法 加上 假UA 取得 html
    ans = rq.get(url, headers=my_header)

    root = bs(ans.text, "lxml")
    # 抓小說名
    novel_name = root.find("h1").string

    # 抓標題
    pattern = re.compile(r"/Book/Read/(\d+),(\d+)")
    title = root.find_all("a", href=pattern)
    # 抓網址
    hrefs = ["https://tw.hjwzw.com" + tag["href"] for tag in title]

    # 打開檔案以寫入模式
    with open(f"{novel_name}vidio.txt", "w", encoding="utf-8") as output_file:
        for href in hrefs:
            # 使用假 ua 和 get 方法抓取網站並印出 text
            response = rq.get(href, headers=my_header)
            root = bs(response.text, "html.parser")

            # 抓標題
            h1_tag = root.find("h1")
            if h1_tag and h1_tag.string:
                chapter_title = h1_tag.string.strip()
                # 将章节标题添加到需要删除的词列表中
                dynamic_words_to_delete = words_to_delete + [chapter_title,novel_name]
                print(f"{chapter_title} 下載成功")

                # 抓內容
                content_divs = root.find_all(
                    "div",
                    style="font-size: 20px; line-height: 30px; word-wrap: break-word; table-layout: fixed; word-break: break-all; width: 750px; margin: 0 auto; text-indent: 2em;",
                )

                for tag in content_divs:
                    text = tag.get_text()  # 提取標籤中的文本

                    # 刪除匹配 dynamic_words_to_delete 的詞
                    for word in dynamic_words_to_delete:
                        text = text.replace(word, "")

                    pattern = re.compile(r"[\d\u4e00-\u9fff…，,。?!、！《》“”？：]+")
                    matches = pattern.findall(text)
                    for match in matches:
                        output_file.write(f"{match}\n")
                    output_file.write("\n")  # 每章節之間空一行

                sleep(0.2)
                output_file.write("=" * 30 + "\n")  # 每章小說之間用等號分隔

def close():
    sys.exit()


# 主程式
declare()
start()
sutch()

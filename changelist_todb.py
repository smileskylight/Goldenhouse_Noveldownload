import re
import json

# 讀取文件，並將內容存儲在變數中
with open('小說編號列表.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# 使用正則表達式將文本轉換為字典列表
book_list = re.findall(r'書籍名稱: (.*?)\s*書籍編號: (\d+)', text)

# 將字典列表轉換為JSON格式
json_output = json.dumps([{"書籍名稱": name.strip(), "書籍編號": number.strip()} for name, number in book_list], ensure_ascii=False, indent=2)

# 將JSON結果輸出到文件中
with open('小說編號列表.json', 'w', encoding='utf-8') as output_file:
    output_file.write(json_output)

print("已將文本轉換為JSON並保存到小說編號列表.json文件中。")

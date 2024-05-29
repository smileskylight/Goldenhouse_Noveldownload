# 前言
此程式是依託request所生成的網路爬蟲
可擷取黃金屋中文網上的所有小說
https://tw.hjwzw.com/

## 先決條件
- Python >= 3.7
- 依附套件 re, requests, json, os, pprint, bs4, fake_useragent, lxml, ffmpeg
## 教學
### 下載
- 請直接在CMD中存放目標位置執行
```bash
git colne https://github.com/smileskylight/Goldenhouse_Nevildownload.git
```
### 套件
- 請直接執行主程式,會自動偵測套件安裝情形,如缺少套件會詢問是否安裝補齊套件

### 使用
- 本程式暫不提供python argparse 請直接在CMD中執行檔案
```bash
python Nevil_goldenhouse_0.3.4.py
```

### 指令
- nl:小說編號列表
- nh:查詢小說編號
- nt:小說目錄
- ntnu:小說章節連結
- nva:小說全本觀看
- nd:全本下載
- ndv:全本下載製作有聲書專用
- nsd:全本下載有聲書(待開發)
- colse:關閉程式

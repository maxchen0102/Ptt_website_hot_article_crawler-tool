###### tags: `github專案ReadMD`

# PPT熱門文章取得工具爬蟲



- [PPT熱門文章取得工具爬蟲](#PPT熱門文章取得工具爬蟲)
    - [程式主要目標以及預期成果](#程式主要目標以及預期成果)
    -   [檔案結構🛠](#檔案結構)
    -    [setting.py 參數檔案設定 🛠](#settingpy參數檔案設定)
    -    [程式碼說明](#程式碼說明)




## 程式主要目標以及預期成果
這個程式完成以下目標以及有以下特點
1.  程式執行完後，會產生一個csv檔案，會存下下圖中標題的資訊
2.  B欄位即為在我們搜尋範圍內推文數最高的文章，依序往下。
3. 我們的搜尋範圍為頁數，可在setting.py 檔案中做調整，例如:尋找100頁或是1000頁中推文數前N名的文章
4. 上述N值可以在setting.py做調整，例如：篩選前100名或是前10名的文章
5. 使用者可以點選文章連結直接連到網站

![](https://i.imgur.com/opnMNqt.png)





## 檔案結構🛠

主要檔案為兩個
1. main.py 為主程式，我們需要去執行他，下載後在同個資料夾路徑下，開起終端機，然後輸入
`python main.py` 執行後即可進行爬蟲
2. setting.py 為我們參數值的設定用的檔案。
3. PTT\_tool\_env.yml 這個檔案是這個程式的執行環境，大家可以下載後放到anaconda，讓後再去執行他。至於要怎麼放，大家可以參考這篇文章，或者是直接手動import 因為相關的特別套件也不多，所以因該不會太麻煩。
https://medium.com/qiubingcheng/%E5%A6%82%E4%BD%95%E5%AE%89%E8%A3%9Danaconda-%E4%B8%A6%E4%B8%94%E5%8C%AF%E5%85%A5conda%E8%99%9B%E6%93%AC%E7%92%B0%E5%A2%83-ba2e140706a3

![](https://i.imgur.com/qpXYWpw.png)


## setting.py參數檔案設定
打開檔案後，小弟有把相關參數的註解下下來 ，
相關參數功能，可以參考註解上的內容，然後這個setting.py檔案會被main.py 主程式引入做說鞥
```python=
url="https://www.ptt.cc/bbs/studyabroad/index.html"  # 你要爬取的網站的網址，預設為ptt 留學版


page=5 # 為你要往後爬取的頁數

sort_number=10 # 為你要取出的push數最多的前幾篇文章，預設為前10名

file_name="result.csv" #為產生的csv檔案路徑以及名稱，預設為在同個資料夾

```
![](https://i.imgur.com/DTbyQYy.png)

## 程式碼說明 

主程式碼內容都有做逐行註解，所以理解上因該不會太困難。
![](https://i.imgur.com/0ZuxhYk.png)


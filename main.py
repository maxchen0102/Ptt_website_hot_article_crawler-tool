#載入模組 

import requests
import bs4 
import csv
import time 
import datetime #載入python基本的日期和時間類型的模組
import setting 
from setting import url


#datetime.timedelta物件代表兩個時間之間的時間差，並將兩個date物件相減

time1 = datetime.timedelta(days = 1)
today = datetime.date.today() #透過此函式取得當天的日期
yesterday = today - time1
time_yesterday = yesterday.strftime("%m/%d")
time_today = today.strftime("%m/%d")#用strftime()方法, 將datetime及date轉成字串.


#這邊使用payload 去向server傳送請求 並且使用headers 讓我們在抓取資料的時候不要被系統發現是用程式去抓的

#可以看到表單是以POST的形式傳送，確認預設的值是'yes'，
#所以接下來我們要帶著建立的session，以POST的方式帶著參數登入，再用cookie以GET的方式帶著參數進入主頁。

payload = {"from": "https://www.ptt.cc/bbs/Gossiping/index.html","yes": "yes"} 
my_headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

rs = requests.Session() 
rs.post("https://www.ptt.cc/", data = payload, headers = my_headers) 


#起始頁面網址為11/14和11/15日間的那個頁面(會往前開始抓)
#url="https://www.ptt.cc/bbs/studyabroad/index.html" 


#取出每個文章的資料  
link = [] #建立link[]串列 去儲存所抓出來的網址


def get_date(url): 
    response = rs.get(url, headers=my_headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")           #透過BeautifulSoup並用"html.parser"去解析此網站
    titles = soup.find_all("div", class_ = "title")          #抓取每篇文章連結
    #print(titles)
    dates = soup.find_all("div", class_="date")       #抓取日期
    #print(dates)
    print(" 爬蟲進行中....")
    for i in range(len(titles)):                         #用title當文章數量的計數器 去一一檢視日期 
            if(titles[i].a):                           #使用.a是避免已經被刪除的文章
                #print(i)
                link.append("https://www.ptt.cc/" + titles[i].find("a").get("href")) # 得到a標籤下的href 
                
    nextlink_2=soup.select('div.btn-group > a')           # 由籤div.btn.group 到標籤a 
    up_page_href = nextlink_2[3]['href'] #在標籤div.btn.group下[0]是看板連結 [1]是精華區連結[2]是最舊[3]是上頁[4]是下頁[5]是最新
    return  up_page_href  #回傳上一頁的網址 讓遞迴成功
    
  

page =5 #設定要往後抓取的頁數 



#print("OK")
#print(link)
    

for i in range(1,page):
    url = "https://www.ptt.cc/"+get_date(url)  #設定一個遞迴 去把上一頁的網址再丟入函式中 去抓取






push = [] #設定一個push的串列 去儲存蓋樓數
#score[j]是亂開的數量 score[j][0] 和score[j][1] 是存放蓋樓數量 還有此網頁的link

score = [[0 for j in range(2)] for k in range(300)] #設定一個雙重陣列去儲存排序的網址和蓋樓數 方便去比對
for j in range(len(link)):  #把迴圈的range設定成我們擁有的網址的數量  
    response = rs.get(str(link[j]), headers = my_headers) # 針對link中每一篇文章，從心再去訪問一次
    soup = bs4.BeautifulSoup(response.text, "html.parser") #得到文章內頁的原始碼存到soup
    push = soup.find_all("div", class_ = "push") #把蓋樓的數量存到變數push中 所有push的標籤都會被抓出來，所以可以用len(push)看總數量
    
    score[j][0] = len(push) #取出蓋樓數量 並存入score list的0位置
    score[j][1] = link[j] #把link存入score list的1位置
    score.sort(key=lambda x:x[0], reverse =True) #使用python的串列排序的函式sort ，根據蓋樓數量排序好   

    
    


#file_name="result.csv"

with open(setting.file_name, "a", newline="", encoding='utf-8-sig')as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['爬蟲爬取時間',"推文數", "標題","文章連結","作者:", "內文","發布時間"])
    sort_number=10
    for n in range(sort_number): #用迴圈印出抓取之前10個推需文數最多的文章
        response = rs.get(score[n][1], headers = my_headers)  # n是文章數量，1 是網址儲存格，0 是push數量。
        soup = bs4.BeautifulSoup (response.text, "html.parser") #再對網站做一次解析
        header = soup.find_all("span", "article-meta-value") #這邊get value 的定義是指把所有的article-meta-value標籤都抓下來存成list 

        author = header[0].text #存入作者  這邊分別使用header[]是因為他分別存在article-meta-value下 
        title = header[2].text #存入標題
        date = header[3].text #存入日期

        main_container = soup.find(id = "main-container",) #抓出內文
        #print(main_container)
        content = main_container.text.replace("\u6ca1", "  ") 
        #print(content)
   
        all_content = content
        pre_content = all_content.split("--")[0]
        texts = pre_content.split('\n')
        contents = texts[2:]
        final_contents = "\n".join(contents)

        writer.writerow([time_today,score[n][0], title,score[n][1],author, final_contents,date]) #寫入csv檔
        print(score[n][1])
print("恭喜完成文章爬蟲,請去result.csv觀看結果")
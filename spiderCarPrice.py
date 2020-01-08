# coding=gbk
import requests
from bs4 import BeautifulSoup
import time
import pymysql
import csv

def get_urls(url):  # ��ȡĿ��url
    res = requests.get(url)
    res.encoding = 'utf-8'
    html = res.text
    soup = BeautifulSoup(html,'html.parser')
    urls = []
    for detail_url in soup.select('.model-a'):
        detail_url = 'https:' + detail_url['href']
        urls.append(detail_url)
    return urls

class down_mysql:   # �������ݿⲢ��������
    def __init__(self,ImagUrl,Title,LPrice,HPrice,Emission,Consum,Gearbox,SalesNum):
        self.ImagUrl = ImagUrl
        self.Title = Title
        self.LPrice = LPrice
        self.HPrice = HPrice
        self.Emission = Emission
        self.Consum = Consum
        self.Gearbox = Gearbox
        self.SalesNum = SalesNum
        self.connect = pymysql.connect(host='localhost', db='car_price', port=3306, user='root', passwd='CZach', charset='utf8', use_unicode=False)
        self.cursor = self.connect.cursor()

    def save_mysql(self):
        sql = "insert into auto_price(ImagUrl,Title,LPrice,HPrice,Emission,Consum,Gearbox,SalesNum) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.cursor.execute(sql, (self.ImagUrl, self.Title, self.LPrice, self.HPrice,self.Emission, self.Consum, self.Gearbox,self.SalesNum))
            self.connect.commit()
            print('���ݲ���ɹ�')
        except:
            print('���ݲ������')

def mysql(ImagUrl,Title,LPrice,HPrice,Emission,Consum,Gearbox,SalesNum):
    down = down_mysql(ImagUrl,Title,LPrice,HPrice,Emission,Consum,Gearbox,SalesNum)
    down.save_mysql()

def main():
    url = 'https://db.auto.sohu.com/home/'
    urls = get_urls(url)
    csv_file = open('car_price2.csv', 'w', encoding="utf-8", newline='')
    writer = csv.writer(csv_file)
    writer.writerow(["ͼƬ����","����","��ͼ�","��߼�","����","�ܺ�","������","����"])
    for detail_url in urls: # ��ȡ���ݣ�������������ϴ
        res = requests.get(detail_url)
        res.encoding = 'utf-8'
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        ImagUrl = soup.select('.fi02_1 img')  # ͼƬ����
        ImagUrl = 'https://' + ImagUrl[0].get('src').strip('//')
        Title = soup.select('.top_tit a')  # ����
        Title = Title[1].string + Title[2].string
        price = soup.select('.info-val ')
        LPrice = price[1].string[0:price[1].string.find('-')].strip('-')  # ��ͼ�
        HPrice = price[1].string[price[1].string.find('-')+1:].strip('-')  # ��߼�
        if ((LPrice == '��')|(HPrice == '����')):
            LPrice=HPrice='---'
        if (LPrice) == 0:
            LPrice = '---'
        parameter = soup.select('.config-val')
        Emission = parameter[0].string  # ����
        Consum = parameter[1].string  # �ܺ�
        Gearbox = parameter[2].string  # ������
        if Consum == None:
            parameter = soup.select('.config-val a')
            Consum = parameter[1].string
        MarketPerform = soup.select('.present-list h3')
        SalesNum = MarketPerform[0].string  #����
        if SalesNum == '--��':
            SalesNum = '---'
        print('ͼƬ����:{}, ����:{},  ��ͼ�:{},  ��߼�:{},  ����or����:{},  �ͺ�or���:{},  ������:{},  ����:{}'.format(ImagUrl,Title.strip('����').strip(),LPrice,HPrice.strip('��'),Emission,Consum.strip(),Gearbox,SalesNum.strip('��')))
        mysql(ImagUrl, Title.strip('����').strip(),LPrice,HPrice.strip('��'),Emission,Consum.strip(),Gearbox,SalesNum.strip('��'))  # �������ݿ�
        writer.writerow([ImagUrl,Title.strip('����').strip(),LPrice,HPrice.strip('��'),Emission,Consum.strip(),Gearbox,SalesNum.strip('��')])  # д��CSV�ļ�
        time.sleep(0.1)
    csv_file.close()
    print("write_finished!")


if __name__ == '__main__':
    main()


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_one_page(url):
    response = requests.get(url)
    response.encoding = "gbk"
    soup = BeautifulSoup(response.text,"html.parser")
    return soup
def find_page(soup):
    grid = soup.find('div', attrs={'class': 'dw_table'})
    page_info = grid.find('div',attrs={'class':'rt'}).get_text().strip()
    num = re.findall('\d+', page_info)  #正则表达式匹配数字
    num2 = []
    for i in num:
        num2.append(int(i))
    if num2[0] % 50 == 0:
        page_num = num2[0]/50
    else:
        page_num = (num2[0]//50)+1
    return page_num
def parse_page(soup,len):
      #判断是否传完页数的依据
    add_info = []
    company_info = []
    workjob_info = []
    salary_info = []
    grid = soup.find('div',attrs={'class':'dw_table'})  #起始位置
    if grid:
        job_list = soup.find_all('div',attrs = {"class":"el"}) #找到所有的岗位列表
        for job in job_list: #匹配各项内容
            try:
                salary = job.find("span",attrs={"class":"t4"}).get_text()
            except AttributeError:
                continue
            try:
                workjob = job.find('p', attrs={'class': 't1'}).find('span').find('a').get_text().strip()
            except AttributeError:
                continue
            company = job.find('span', attrs={'class': 't2'}).find('a').get_text()
            address = job.find("span", attrs={"class": "t3"}).get_text().strip()
            add_info.append(address)
            company_info.append(company)
            workjob_info.append(workjob)
            salary_info.append(salary)
        df = pd.DataFrame(data=[add_info, company_info, workjob_info, salary_info]).T
        df.columns = ['公司地址', '公司名', '工作名', '工资']
        df.to_csv('Pdoc/bigdata_job.csv', encoding='gbk', mode='a+', header=len, index=False)

if __name__ == '__main__':
    job_find = input("请输入您要找的职业:")
    url_page  = "https://search.51job.com/list/140000,000000,0000,00,9,99,"+job_find+",2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
    soup = get_one_page(url_page)
    page_num = find_page(soup)
    parse_page(soup,eval('True'))
    if page_num >= 2:
        for i in range(2,page_num+1):
            url  = "https://search.51job.com/list/140000,000000,0000,00,9,99,"+job_find+",2,"+str(i)+".html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
            sp = get_one_page(url)
            parse_page(sp,eval('False'))
        print('爬取结束')
    else:
        print('爬取结束')

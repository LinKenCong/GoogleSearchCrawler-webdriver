from tools import operate_excel
from selenium import webdriver
from bs4 import BeautifulSoup
import random
import time

OperateExcel = operate_excel


class SearchResult:
    def __init__(self):
        self.url = ''
        self.title = ''

    def getUrl(self):
        return self.url

    def setUrl(self, url):
        self.url = url

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getAllStr(self):
        result = ''
        return result

    def printIt(self, prefix=''):
        print('\nurl\t->', self.url)
        print('title\t->', self.title)


class GoogleAPI:
    def __init__(self):
        self.driver = None
        self.timeSleep = 5
        self.searchUrl = 'https://www.google.com'
        self.HMInspectionTips = '该流量可能是由恶意软件'

    def firstOpenUrl(self, driver):
        self.driver = driver
        driver.get(self.searchUrl)
        input("\nWaiting for cookies")
        driver.get_cookies()
        print('\nCookies\t->', driver.get_cookies())

    def pageSearchResults(self, keyword, num):
        driver = self.driver
        driver.get('{}/search?q={}&start={}'.format(self.searchUrl, keyword, num))
        if self.HMInspectionTips in driver.page_source:
            input('Whether human-machine verification continues?')
            driver.get_cookies()
        page = BeautifulSoup(driver.page_source, 'html.parser')
        divList = list(page.find_all('div', class_="tF2Cxc"))
        return divList

    def whileGetPage(self, keyword, count=20):
        num = 0
        result = list()
        result += GoogleAPI.pageSearchResults(self, keyword, num)
        time.sleep(self.timeSleep)
        return result[0:count]
        while(len(result) <= count):
            result += GoogleAPI.pageSearchResults(self, keyword, num)
            time.sleep(self.timeSleep)
            num += 10

    def extractSearchResults(self, resultList):
        results = list()
        for div in resultList:
            url = div.find('a', href=True)['href']
            title = div.find('h3').text
            result = SearchResult()
            result.setUrl(url)
            result.setTitle(title)
            results.append(result)
            # result.printIt()
        return results


class UserParameter:
    def __init__(self):
        self.keywords = None

    def getkeywords(self, url):
        keylist = list()
        keywords = open(url, 'r')
        keyword = keywords.readline()
        while(keyword):
            if(keyword):
                keylist.append(keyword.strip('\n'))
                keyword = keywords.readline()
            else:
                print('\nerror keyword:', keyword)
                return
        print('\nkeyword\t->', keylist)
        self.keywords = keylist
        keywords.close()
        return keylist


def crawler():
    user = UserParameter()
    keywords = user.getkeywords('./keywords')
    driver = webdriver.Chrome()
    driver.implicitly_wait(15)
    api = GoogleAPI()
    api.firstOpenUrl(driver)
    # return
    search_results = list()
    results = list()
    try:
        for index, key in enumerate(keywords):
            print('\nCrawlingProgress\t->', f"{index+1}/{len(keywords)}")
            page = api.whileGetPage(key, 50)
            results.append(api.extractSearchResults(page))
    except:
        print('\nERROR FUNC\t->crawler()')
        pass

    search_results.extend(results)

    results_key = list()
    results_url = list()
    results_title = list()
    for index, item in enumerate(search_results):
        for it in item:
            results_key.append(str(keywords[index]))
            results_url.append(str(it.getUrl()))
            results_title.append(str(it.getTitle()))

    driver.quit()
    return [results_key, results_url, results_title]


def writeExecel(data):
    print(data)
    filepath = r'C:\Users\apuser\Desktop\crawResult-50(2022-2-21).xlsx'
    app = OperateExcel.init_data()
    wb1 = OperateExcel.get_wb(app, filepath)
    sht1 = OperateExcel.get_sht(wb1, 'Sheet1')
    OperateExcel.write_td(sht1, data, 'a2')
    wb1.save()
    app.quit()


if __name__ == '__main__':
    data = crawler()
    writeExecel(data)
    print('\n->Finish<-')

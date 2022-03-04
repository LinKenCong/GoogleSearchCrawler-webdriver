from tools import operate_excel
from selenium import webdriver
from bs4 import BeautifulSoup
import time

OperateExcel = operate_excel

file_path = r'C:\Users\apuser\Desktop\crawResult.xlsx'
table_name = 'Sheet1'
table_cell = 'a2'
required_quantity = 50


class SearchResult:
    def __init__(self):
        self.url = ''
        self.alt = ''
        self.title = ''

    def getUrl(self):
        return self.url

    def setUrl(self, url):
        self.url = url

    def getAlt(self):
        return self.alt

    def setAlt(self, alt):
        self.alt = alt

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
        self.time_sleep = 5
        self.search_domain = 'https://www.google.com'
        self.HMInspectionTips = '该流量可能是由恶意软件'

    def firstOpenUrl(self, driver, needcookies=False):
        self.driver = driver
        if(needcookies):
            driver.get(self.search_domain)
            input("\nSetting up Driver Browser")
            driver.get_cookies()
            print('\nCookies\t->', driver.get_cookies())

    def pageSearchResults(self, keyword, num):
        driver = self.driver
        driver.get(
            '{}/search?q={}&start={}'.format(self.search_domain, keyword, num))
        if(self.HMInspectionTips in driver.page_source):
            input('Whether human-machine verification continues?')
            driver.get_cookies()
        page = BeautifulSoup(driver.page_source, 'html.parser')
        divList = list(page.find_all('div', class_="tF2Cxc"))
        return divList

    def whileGetPage(self, keyword, count=20):
        num = 0
        result = list()
        result += GoogleAPI.pageSearchResults(self, keyword, num)
        time.sleep(self.time_sleep)
        return result[0:count]

    def extractSearchResults(self, result_list):
        results = list()
        for div in result_list:
            url = div.find('a', href=True)['href']
            title = div.find('h3').text
            result = SearchResult()
            result.setUrl(url)
            result.setTitle(title)
            results.append(result)
        return results

    def returnAllResults(self, results, keys):
        results_key = list()
        results_url = list()
        results_title = list()
        for index, item in enumerate(results):
            for it in item:
                results_key.append(str(keys[index]))
                results_url.append(str(it.getUrl()))
                results_title.append(str(it.getTitle()))
        return [results_key, results_url, results_title]


class PageImgCrawlerAPI:
    # keyword need URL
    def __init__(self):
        self.driver = None
        self.time_sleep = 1
        self.search_domain = '//www.xxxxxx.com/'

    def firstOpenUrl(self, driver, needcookies=False):
        self.driver = driver
        if(needcookies):
            driver.get(self.search_domain)
            input("\nSetting up Driver Browser")
            driver.get_cookies()
            print('\nCookies\t->', driver.get_cookies())

    def pageSearchResults(self, keyword):
        driver = self.driver
        driver.get('{}'.format(keyword))
        page = BeautifulSoup(driver.page_source, 'html.parser')
        divList = list()
        for find_key in page.find_all('img'):
            if(find_key.get('src').find(self.search_domain) != -1):
                divList.append(find_key)
        return divList

    def extractSearchResults(self, result_list):
        results = list()
        for div in result_list:
            url = div.get('src')
            alt = div.get('alt')
            title = div.get('title')
            print('url\t->', url)
            result = SearchResult()
            result.setUrl(url)
            result.setAlt(alt)
            result.setTitle(title)
            results.append(result)
        return results

    def returnAllResults(self, results, keys):
        results_key = list()
        results_url = list()
        results_alt = list()
        results_title = list()
        for index, item in enumerate(results):
            for it in item:
                results_key.append(str(keys[index]))
                results_url.append(str(it.getUrl()))
                results_alt.append(str(it.getAlt()))
                results_title.append(str(it.getTitle()))
        return [results_key, results_url, results_alt, results_title]


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
    api.firstOpenUrl(driver, True)
    search_results = list()
    results = list()
    try:
        for index, key in enumerate(keywords):
            print('\nCrawling Progress\t->', f"{index+1}/{len(keywords)}")
            page = api.whileGetPage(key, required_quantity)
            results.append(api.extractSearchResults(page))
    except:
        print('\nERROR FUNC\t->crawler()')
        pass
    driver.quit()
    search_results.extend(results)
    return api.returnAllResults(search_results, keywords)


def writeExecel(data):
    app = OperateExcel.init_data()
    wb1 = OperateExcel.get_wb(app, file_path)
    sht1 = OperateExcel.get_sht(wb1, table_name)
    OperateExcel.write_td(sht1, data, table_cell)
    wb1.save()
    app.quit()


if __name__ == '__main__':
    data = crawler()
    writeExecel(data)
    print('\n->Finish<-')

'''
Playwright 是一个开源的自动化框架，它可以让你模拟真实用户操作网页，帮助开发者和测试者自动化网页交互和测试。
用简单的话说，它就像一个“机器人”，可以按照你给的指令去浏览网页、点击按钮、填写表单、读取页面内容等等，就像一个真实的用户在使用浏览器一样
pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple
playwright install chromium

https://playwright.dev/python/docs/locators
'''

from playwright.sync_api import sync_playwright
import os
from datetime import datetime

date = datetime.now()
today_date = date.strftime('%Y-%m-%d')

request_url = 'https://wvpn.ahu.edu.cn/http/77726476706e69737468656265737421a1a013d2766726012e50c7fec8/iot-manage-web/#'

car_device_list = [
    '新区南门东入口',
    '新区西外围出口',
    '新区西外围入口',
    '新区东外围入口',
    '新区东外围出口',
    '新区东门西入口',
    '新区东门西出口',
    '新区南门东出口',
    '新区南门西入口',
    '新区东门东出口',
    '新区东门东入口',
    '新区北门出口',
    '新区北门入口',
    '新区南门西出口',
    '老区南门西出口',
    '老区南门东出口',
    '老区南门入口'
]
person_device_list = [
    '磬苑-西门出入口-通道2-QET-5301L-W-172-22-2-195', 
    '磬苑-南门出入口-主道西侧-QET-5301L-W-172-22-28-182', 
    '磬苑-北门出入口-通道1-QET-5301L-W-172-22-17-40', 
    '磬苑-西门出入口-通道1-QET-5301L-W-172-22-2-186', 
    '磬苑-北门出入口-通道2-QET-5301L-W-172-22-17-42', 
    '磬苑-西门出入口-通道2-QET-5301L-W-172-22-2-194', 
    '磬苑-南门出入口-主道西侧-QET-5301L-W-172-22-28-181', 
    '磬苑-南门出入口-辅道东侧偏西-QET-5301L-W-172-22-28-95', 
    '磬苑-东门出入口-东门-北侧-QET-5301L-W-172-22-17-39', 
    '磬苑-南门出入口-辅道东侧偏东-QET-5301L-W-172-22-28-94', 
    '磬苑-北门出入口-通道1-QET-5301L-W-172-22-17-41', 
    '磬苑-西门出入口-通道1-QET-5301L-W-172-22-2-187', 
    '磬苑-东门出入口-东门-北侧-QET-5301L-W-172-22-17-38', 
    '磬苑-东门出入口-东门-南侧-QET-5301L-W-172-22-17-37', 
    '磬苑-东门出入口-东门-南侧-QET-5301L-W-172-22-17-36', 
    '龙河-南门东出入口-通道2-EG131-HF-172_22_30_194', 
    '龙河-南门东出入口-通道1-EG131-HF-172_22_30_195'
]

screen_shot_save_path_car = '/Users/louisliu/Downloads/car' 
screen_shot_save_path_person = '/Users/louisliu/Downloads/person'

def get_data():
    # 使用Playwright上下文管理器
    with sync_playwright() as p:
        # 使用Chromium，但你也可以选择firefox或webkit
        browser = p.chromium.launch(headless=False, args=['--start-maximized'])
        
        # 创建一个新的页面
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        
        # 导航到指定的URL
        page.goto(request_url)
        page.wait_for_timeout(10000)
        
        page.goto(request_url)
        page.wait_for_timeout(1000)
        # 获取并打印页面标题
        page.click("text=登录")
        page.get_by_placeholder("请输入用户名").fill("eduadmin")
        page.get_by_placeholder("请输入密码").fill("edu@adzhgl")
        page.locator('//*[@id="app"]/div/div/div/div[2]/form/div/div[3]/button').click()
        # 等待登录
        page.wait_for_timeout(5000)

        get_car_data(page)
        get_person_data(page)

        # 关闭浏览器
        browser.close()

# 获取车行数据
def get_car_data(page):
    page.goto(f'{request_url}/chexing/envdata')
    page.evaluate("document.body.style.zoom=0.55")
    page.wait_for_timeout(1000)
    page.get_by_placeholder("结束日期").fill(f"{today_date} 14:00:00")


    for idx, d in enumerate(car_device_list):
        page.locator('//*[@id="app"]/div/div[3]/section/div[2]/div/div/div[2]/div[1]/form/div/div[3]/div/div/div/input').fill(d)
        page.locator('//*[@id="app"]/div/div[3]/section/div[2]/div/div/div[2]/div[1]/form/div/div[4]/div/div/div/button[2]').click()
        page.wait_for_timeout(3000)
        num_ele = page.query_selector('//*[@id="app"]/div/div[3]/section/div[2]/div/div/div[2]/div[2]/div/div[3]/div/span[2]')
        number = '共 0 条'
        if (num_ele):
            number = num_ele.text_content()
        page.locator('//*[@id="app"]/div/div[3]/section/div[2]').screenshot(path=os.path.join(screen_shot_save_path_car, f'{idx + 1}-{d}({number}).png'))
        page.wait_for_timeout(1000)


# 获取门禁数据
def get_person_data(page):
    page.goto(f'{request_url}/menjin/envdata')
    page.evaluate("document.body.style.zoom=0.55")
    page.wait_for_timeout(1000)
    page.get_by_placeholder("结束日期").fill(f"{today_date} 15:00:00")
    page.locator('//*[@id="app"]/div/div[3]/section/div[2]/div/div/div[2]/div[1]/form/div/div[4]/div/div/div/button[3]/span').click()

    for idx, d in enumerate(person_device_list):
        page.locator('//*[@id="app"]/div/div[3]/section/div[2]/div/div/div[2]/div[1]/form/div/div[5]/div/div/div/input').fill(d)
        page.locator('//*[@id="app"]/div/div[3]/section/div[2]/div/div/div[2]/div[1]/form/div/div[7]/div/div/div/button[2]').click()
        page.wait_for_timeout(3000)
        num_ele = page.query_selector('//*[@id="app"]/div/div[3]/section/div[2]/div/div/div[2]/div[2]/div/div[3]/div/span[2]')
        number = '共 0 条'
        if (num_ele):
            number = num_ele.text_content()
        page.locator('//*[@id="app"]/div/div[3]/section/div[2]').screenshot(path=os.path.join(screen_shot_save_path_person, f'{idx + 1}-{d}({number}).png'))
        page.wait_for_timeout(1000)


if __name__ == "__main__":
    get_data()
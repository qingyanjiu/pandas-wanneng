'''
Playwright 是一个开源的自动化框架，它可以让你模拟真实用户操作网页，帮助开发者和测试者自动化网页交互和测试。
用简单的话说，它就像一个“机器人”，可以按照你给的指令去浏览网页、点击按钮、填写表单、读取页面内容等等，就像一个真实的用户在使用浏览器一样
pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple
playwright install chromium

https://playwright.dev/python/docs/locators
'''

from playwright._impl._page import Page
from playwright.sync_api import sync_playwright
import os
from datetime import datetime

date = datetime.now()
today_date = date.strftime('%Y-%m-%d')

request_url = 'http://stage.3d.com:5173/iot-screen/#'

car_device_list_qy = {
    '新区南门东入口': 'zhaji-c-nan-21',
    # '新区西外围出口': '286737408',
    # '新区西外围入口': '289347328',
    # '新区东外围入口': '218067968',
    # '新区东外围出口': '218047488',
    '新区西外围出口': '',
    '新区西外围入口': '',
    '新区东外围入口': '',
    '新区东外围出口': '',
    '新区东门西入口': 'zhaji-c-dong-23',
    '新区东门西出口': 'zhaji-c-dong-22',
    '新区南门东出口': 'zhaji-c-nan-20',
    '新区南门西入口': 'zhaji-c-nan-2',
    '新区东门东出口': 'zhaji-c-dong-4',
    '新区东门东入口': 'zhaji-c-dong-3',
    '新区北门出口': 'zhaji-c-bei-19',
    '新区北门入口': 'zhaji-c-bei-18',
    '新区南门西出口': 'zhaji-c-nan-1'
}

car_device_list_lh = {
    '老区南门西出口': 'zhaji-c-nan-lh-1',
    '老区南门东出口': 'zhaji-c-nan-lh-2',
    '老区南门入口': 'zhaji-c-nan-lh-3'
}

person_device_list_qy = {
    '磬苑-西门出入口-通道2-QET-5301L-W-172-22-2-195': 'zhaji-p-xi-12',
    '磬苑-南门出入口-主道西侧-QET-5301L-W-172-22-28-182': 'zhaji-p-nan-5',
    '磬苑-北门出入口-通道1-QET-5301L-W-172-22-17-40': 'zhaji-p-bei-16',
    '磬苑-西门出入口-通道1-QET-5301L-W-172-22-2-186': 'zhaji-p-xi-14',
    '磬苑-北门出入口-通道2-QET-5301L-W-172-22-17-42': 'zhaji-p-bei-24',
    '磬苑-西门出入口-通道2-QET-5301L-W-172-22-2-194': 'zhaji-p-xi-13',
    '磬苑-南门出入口-主道西侧-QET-5301L-W-172-22-28-181': 'zhaji-p-nan-25',
    '磬苑-南门出入口-辅道东侧偏西-QET-5301L-W-172-22-28-95': 'zhaji-p-nan-6',
    '磬苑-东门出入口-东门-北侧-QET-5301L-W-172-22-17-39': 'zhaji-p-dong-11',
    '磬苑-南门出入口-辅道东侧偏东-QET-5301L-W-172-22-28-94': 'zhaji-p-nan-7',
    '磬苑-北门出入口-通道1-QET-5301L-W-172-22-17-41': 'zhaji-p-bei-17',
    '磬苑-西门出入口-通道1-QET-5301L-W-172-22-2-187': 'zhaji-p-xi-15',
    '磬苑-东门出入口-东门-北侧-QET-5301L-W-172-22-17-38': 'zhaji-p-dong-10',
    '磬苑-东门出入口-东门-南侧-QET-5301L-W-172-22-17-37': 'zhaji-p-dong-8',
    '磬苑-东门出入口-东门-南侧-QET-5301L-W-172-22-17-36': 'zhaji-p-dong-9'
}

person_device_list_lh = {
    '龙河-南门东出入口-通道2-EG131-HF-172_22_30_194': 'zhaji-p-nan-lh-11',
    '龙河-南门东出入口-通道1-EG131-HF-172_22_30_195': 'zhaji-p-nan-lh-10'
}

campus_map = dict({
    'qy': {
        'name': 'qingyuan',
        'car_list_data': car_device_list_qy,
        'person_list_data': person_device_list_qy
    },
    'lh': {
        'name': 'longhe',
        'car_list_data': car_device_list_lh,
        'person_list_data': person_device_list_lh
    }
})

screen_shot_save_path_car_3d = '/Users/louisliu/Downloads/car-3d' 
screen_shot_save_path_person_3d = '/Users/louisliu/Downloads/person-3d'

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
        page.wait_for_timeout(1000)
        
        # 获取并打印页面标题
        page.click("text=登录")
        page.locator('//*[@id="username"]').fill("eduadmin")
        page.locator('//*[@id="password"]').fill("edu@adzhgl")
        page.locator('//*[@id="app"]/div/div[2]/div[2]/button').click()
        # 等待登录
        page.wait_for_timeout(20000)

        for campus_id in ['qy', 'lh']:
            get_car_data(page, campus_id)
            get_person_data(page, campus_id)

        # 关闭浏览器
        browser.close()

# 获取车行数据
# campus_id: qy 或者 lh
def get_car_data(page: Page, campus_id):
    page.goto(f'{request_url}/visual/{campus_map[campus_id]["name"]}/anFang/tingChe/school')
    page.wait_for_timeout(10000)
    number = ''
    car_device_list = campus_map[campus_id]['car_list_data']
    for idx, device_name in enumerate([key for key in car_device_list]):
        device_tag = car_device_list[device_name]
        # value不为空，说明打了点，可以点到点位
        if (device_tag != ''):
            # 模拟点击图标
            page.evaluate(f"window.hxhtApp.emit('onClick', hxhtApp.dm.getDataByTag('{device_tag}'))")
            # 点击条件筛选
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div/span').click()
            # 设置时间
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[1]/div/div/div[3]/div/div/div[2]/div[3]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[1]/div/input[2]')\
                .fill(f"{today_date} 14:00:00")
            # 点击查询
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[1]/div/div/div[3]/div/div/div[2]/div[3]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/div/span[1]')\
                .click()
            page.wait_for_timeout(2000)
            # 获取总数
            number = page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[1]/div/div/div[3]/div/div/div[2]/div[3]/div/div[2]/div/div/div[2]/div[3]/span[1]')\
                .text_content()
            page.screenshot(path=os.path.join(screen_shot_save_path_car_3d, f'{idx + 1}-{device_name}({number}).png'))
            # 关闭窗口
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[1]/div/div/div[3]/div/div/div[2]/div[3]/div/div[2]/div/div/div[1]/i')\
                .click()
        # 为空说明点不到点位，只能直接查了
        else:
            page.reload()
            page.wait_for_timeout(10000)
            page.goto(f'{request_url}/visual/{campus_map[campus_id]["name"]}/anFang/tingChe/school')
            page.wait_for_timeout(10000)
            # 点击展开按钮
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[2]/div[2]/div/div[1]/div[3]').click()
            page.wait_for_timeout(100)
            # 点击条件筛选
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div/span').click()
            # 设置时间
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[1]/div/input[2]')\
                .fill(f"{today_date} 14:00:00")
            # 填入设备名称
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div')\
                .click()
            page.get_by_placeholder('设备名称').fill(device_name)
            # 点击查询
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[3]/div/span[1]')\
                .click()
            page.wait_for_timeout(2000)
            number = page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[2]/div[3]/span[1]')\
                .text_content()
            page.screenshot(path=os.path.join(screen_shot_save_path_car_3d, f'{idx + 1}-{device_name}({number}).png'))
        page.wait_for_timeout(1000)


# 获取门禁数据
# campus_id: qy 或者 lh
def get_person_data(page: Page, campus_id):
    page.goto(f'{request_url}/visual/{campus_map[campus_id]["name"]}/anFang/menJin/school')
    page.wait_for_timeout(10000)
    number = ''
    person_device_list = campus_map[campus_id]['person_list_data']
    for idx, device_name in enumerate([key for key in person_device_list]):
        device_tag = person_device_list[device_name]
        # value不为空，说明打了点，可以点到点位
        if (device_tag != ''):
            # 模拟点击图标
            page.evaluate(f"window.hxhtApp.emit('onClick', hxhtApp.dm.getDataByTag('{device_tag}'))")
            # 点击条件筛选
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div/span').click()
            # 设置日期
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[1]/div/div/div[3]/div/div/div[2]/div[3]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[1]/div/input[2]')\
                .fill(f"{today_date} 15:00:00")
            # 点击查询
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[1]/div/div/div[3]/div/div/div[2]/div[3]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[3]/div/span[1]').click()
            page.wait_for_timeout(2000)
            # 获取总数
            number = page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[1]/div/div/div[3]/div/div/div[2]/div[3]/div/div[2]/div/div/div[2]/div[3]/span[1]')\
                .text_content()
            page.screenshot(path=os.path.join(screen_shot_save_path_person_3d, f'{idx + 1}-{device_name}({number}).png'))
            page.locator('//*[@id="pageContent"]/div[7]/div[1]/div[1]/div/div/div[3]/div/div/div[2]/div[3]/div/div[2]/div/div/div[1]/i')\
                .click()
        page.wait_for_timeout(1000)


if __name__ == "__main__":
    get_data()
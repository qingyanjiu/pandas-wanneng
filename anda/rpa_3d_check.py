'''
Playwright 是一个开源的自动化框架，它可以让你模拟真实用户操作网页，帮助开发者和测试者自动化网页交互和测试。
用简单的话说，它就像一个“机器人”，可以按照你给的指令去浏览网页、点击按钮、填写表单、读取页面内容等等，就像一个真实的用户在使用浏览器一样
pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple
playwright install chromium

https://playwright.dev/python/docs/locators

获取所有关键页面截图
'''

from playwright._impl._page import Page
from playwright.sync_api import sync_playwright
import os
from datetime import datetime

date = datetime.now()
today_date = date.strftime('%Y-%m-%d')

request_url = 'http://172.17.108.19/iot-screen/#'

doorlist_qy = {
    '磬苑-东门': 'BUILD_QY_DONGMEN',
    '磬苑-西门': 'BUILD_QY_XIMEN',
    '磬苑-南门': 'BUILD_QY_NANMEN',
    '磬苑-北门': 'BUILD_QY_BEIMEN',
}

doorlist_lh = {
    '龙河-南门': 'BUILD_LH_NANMEN',
}

campus_map = dict({
    'qy': {
        'name': 'qingyuan',
        'door_data': doorlist_qy
    },
    'lh': {
        'name': 'longhe',
        'door_data': doorlist_lh
    }
})

screen_shot_save_path_3d_check = r'C:\Users\hp\Desktop\fb\3d-check'

def get_data():
    # 使用Playwright上下文管理器
    with sync_playwright() as p:
        # 使用Chromium，但你也可以选择firefox或webkit
        browser = p.chromium.launch(channel="msedge", headless=False, args=['--start-maximized'])
        
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
            check_door(page, campus_id)

        # 关闭浏览器
        browser.close()

# 获取大门数据
# campus_id: qy 或者 lh
def check_door(page: Page, campus_id):
    page.goto(f'{request_url}/visual/{campus_map[campus_id]["name"]}/index/school')
    page.wait_for_timeout(30000)
    door_list = campus_map[campus_id]['door_data']
    for idx, door_name in enumerate([key for key in door_list]):
        door_tag = door_list[door_name]
        # value不为空，说明打了点，可以点到点位
        if (door_tag != ''):
            # 模拟点击图标
            page.evaluate(f"window.hxhtApp.emit('onClick', hxhtApp.dm.getDataByTag('{door_tag}'))")
            page.wait_for_timeout(10000)
            page.screenshot(path=os.path.join(screen_shot_save_path_3d_check, f'{idx + 1}-{door_name}.png'))
            page.goto(f'{request_url}/visual/{campus_map[campus_id]["name"]}/index/school')
            page.wait_for_timeout(5000)
        page.wait_for_timeout(1000)


if __name__ == "__main__":
    get_data()
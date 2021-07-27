import uiautomator2 as u2

try:
    d = u2.connect('192.168.2.4:5555')
except RuntimeError as r:
    if 'offline' in r.args[0]:
        t = os.popen('adb connect 192.168.2.4')
        print(t.readlines())
        d = u2.connect('192.168.2.4:5555')

print(u2.Device)
print(d.info)
#   试客巴包名：com.yc.apps.shikeba
#   淘宝包名：com.taobao.taobao
#   点击免费试用
task = 'tb'
d(resourceId="apply_sub").click()
#   获取搜索词
search_text = d(resourceId="keywords").get_text(timeout=10)
#   获取店铺名称
shop_name = d.xpath(
    '//*[@resource-id="section"]/android.view.View[2]/android.view.View[4]/android.widget.TextView').get_text()
print(search_text, shop_name)
#   复制搜索词
d.set_clipboard(search_text)
if task == 'tb':
    #   启动淘宝
    d.app_start('com.taobao.taobao', wait=True)
    #   循环查找搜索框并点击搜索按钮
    while True:
        # 首页的搜索框
        ele = d.xpath(
            '//*[@resource-id="com.taobao.taobao:id/sv_search_view"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.View[1]')
        if ele.exists:
            ele.click()
        # 搜索框
        elif d.xpath('//*[@resource-id="com.taobao.taobao:id/searchEdit"]').exists:
            d.xpath('//*[@resource-id="com.taobao.taobao:id/searchEdit"]').click()
            break
        else:
            d.press('back')
            d.press('back')
            #   查找商品详情页面的搜索框是否存在，如果存在就点击置焦点，并输入搜索词，否则点击返回
            ele = d(resourceId="com.taobao.taobao:id/ll_action_bar_search_container")
            if ele.exists():
                ele.click()
                break
            else:
                d.press('back')
    #   输入搜索词
    d.xpath('//*[@resource-id="com.taobao.taobao:id/searchEdit"]').set_text(search_text)
    #   开始搜索
    d.xpath('//*[@resource-id="com.taobao.taobao:id/searchbtn"]').click()
    #   排序
    d(resourceId="com.taobao.taobao:id/styleBtn").click()
elif task == 'pdd':
    # 定位搜索框
    d(text="").click()

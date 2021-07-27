import uiautomator2 as u2
import os

try:
    d = u2.connect('192.168.2.4:5555')
except RuntimeError as r:
    if 'offline' in r.args[0]:
        t = os.popen('adb connect 192.168.2.4')
        print(t.readlines())
        d = u2.connect('192.168.2.4:5555')

while True:
    # 新闻页面
    if d(textContains="领金币").exists:
        d(textContains="领金币").click(timeout=1)
    elif d(text="已领取").exists:
        d.press('back')
        # 进入任务页面
        d(resourceId="com.ss.android.article.lite:id/ad1").click_exists(timeout=1)
        d(text="开宝箱得金币").click_exists(timeout=3)
    # 看新闻赚金币
    if d(textContains='金币').exists or d(descriptionContains='金币').exists or d(textContains='视频再领').exists or d(
            description='关闭').click_exists():
        if d(textContains='金币').click_exists():
            print('text带有金币2个字')
            ele = d(resourceId="com.ss.android.article.lite:id/f8")
            if ele.click_exists(timeout=1):
                print('id f8点击了。')
            else:
                # 签到后领取
                if d(textContains="视频再领").exists:
                    info = d(textContains="视频再领").info
                    d(text=info['text']).click()
                    print('视频再领')
        # 走路奖励，判断的文字有点少，需要多一些字以确定唯一性

        elif d(textContains="再看一个获得").exists:
            info = d(textContains="再看一个获得").info
            d(text=info['text']).click()
            print(info['text'] + '被点击')

        else:
            d(descriptionContains="金币").click_exists()
            print('description带有金币2个字')

        # 进入广告视频页面
        # 静音
        d.sleep(1)
        try:
            d(descriptionContains="广告").right(className='android.widget.ImageView').click_exists(timeout=3)
            # 检测到有读秒节点
            while d(descriptionContains="s").exists:
                time = d(descriptionContains="s").info
                try:
                    time = int(time['contentDescription'].replace('s', ''))
                    if time > 1:
                        d.sleep(time - 1)
                    time = d(descriptionContains="s").info
                    print('需要等待大约%s秒' % time['contentDescription'])
                except Exception as e:
                    print(e)
                    pass
            d(description="关闭").click()
            d.sleep(1)
        except Exception as e:
            print(e)

    # 这则新闻没有金币收益了，需要退出了
    else:
        d(description="坚持退出").click_exists(timeout=2)

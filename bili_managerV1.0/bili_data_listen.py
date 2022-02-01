import asyncio
from bilibili_api import video,user
import time

async def main(last_info):
    bvid_list =[]
    num = 1
    #uid = 641721563
    uid = input("请输入您的uid：")
    #实例化user类
    u = user.User(uid=int(uid), credential=None)
    #获取视频列表
    msg = await u.get_videos()
    for i in msg['list']['vlist']:
        print(num,i['bvid'], i['title'])
        bvid_list.append(i['bvid'])
        num += 1
    sel = input("选择需要监控视频的序号：")
    # 实例化 Video 类
    v = video.Video(bvid=bvid_list[int(sel)-1])
    # 获取视频标题
    title = (await v.get_info())['title']
    print(title)
    # 循环监听数据发生变化
    while True:
        # 获取信息
        info = (await v.get_info())['stat']
        # 获取粉丝数
        follower = (await u.get_relation_info())['follower']
        #获取本地时间
        localtime = time.strftime("%H:%M:%S", time.localtime())
        # 判断变化
        if not follower == last_info['follower']:
            print("["+str(localtime)+"]"+"粉丝变化"+str(follower))
            last_info['follower'] = follower
        if not info['view'] == last_info['view']:
            print("["+str(localtime)+"]"+"浏览变化"+str(info['view']))
            last_info['view'] = info['view']
        if not info['reply'] == last_info['reply']:
            print("["+str(localtime)+"]"+"回复变化" + str(info['reply']))
            last_info['reply'] = info['reply']
        if not info['like'] == last_info['like']:
            print("["+str(localtime)+"]"+"点赞变化" + str(info['like']))
            last_info['like'] = info['like']
        if not info['favorite'] == last_info['favorite']:
            print("["+str(localtime)+"]"+"收藏变化" + str(info['favorite']))
            last_info['favorite'] = info['favorite']
        if not info['coin'] == last_info['coin']:
            print("["+str(localtime)+"]"+"硬币变化" + str(info['coin']))
            last_info['coin'] = info['coin']
        if not info['share'] == last_info['share']:
            print("["+str(localtime)+"]"+"分享变化" + str(info['share']))
            last_info['share'] = info['share']
        #print()
        await asyncio.sleep(20)
if __name__ == '__main__':

    last_info = {'view': 0, 'reply': 0, 'like': 0, 'favorite': 0, 'coin': 0, 'share': 0, 'follower': 0}
    asyncio.get_event_loop().run_until_complete(main(last_info))
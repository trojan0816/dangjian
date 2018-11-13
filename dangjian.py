import requests
import time
from PIL import Image
import io
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

API_HOST = 'https://capi.dangjianwang.com'

s = requests.session()
# 通用headers
headers = {
    'Host': 'capi.dangjianwang.com',
    'Connection': 'keep-alive',
    # 'Content-Length': '1467',
    # 'Accept': 'application/json, text/plain, */*',
    'Appid': '33beba686fd8333e',  # 无此项无法获取cookies
    'Origin': 'https://www.dangjianwang.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 \
    Safari/537.36 Core/1.63.6735.400 QQBrowser/10.2.2614.400',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

# =====================================================
# 验证码 
# =====================================================

def get_captcha():

    url = API_HOST + '/official/ucenter/login/preCaptcha'
    # headers = {
    #     'Host': 'capi.dangjianwang.com',
    #     'Connection': 'keep-alive',
    #     'Accept': 'application/json, text/javascript, */*; q=0.01',
    #     'Origin': 'https://www.dangjianwang.com',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
    #     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 \
    #     Safari/537.36 Core/1.63.6735.400 QQBrowser/10.2.2614.400',
    #     'Referer': 'https://www.dangjianwang.com/login',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'zh-CN,zh;q=0.9'
    # }
    rs = s.get(url, headers= headers)
    # data={
    #     'captcha_token' : 'Ch62d1vosN'
    #     'captcha_url' : 'https://capi.dangjianwang.com/official/ucenter/login/getCaptcha?captcha_token=Ch62d1vosN'
    # }
    data = rs.json()['data']
    # headers = {
    #     'Host': 'capi.dangjianwang.com',
    #     'Connection': 'keep-alive',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
    #     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 \
    #     Safari/537.36 Core/1.63.6735.400 QQBrowser/10.2.2614.400',
    #     'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    #     'Referer': 'https://www.dangjianwang.com/login',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'zh-CN,zh;q=0.9'
    # }
    rs = s.get(data['captcha_url'], headers= headers)
    logger.info('获取验证码成功')
    Image.open(io.BytesIO(rs.content)).show()
    captcha_code = input('请输入图片中验证码：')
    return captcha_code, data['captcha_token']

# =====================================================
# 登陆 
# =====================================================

def login():

    name = input('手机号码/用户名：')
    print()
    pwd = input('请输入密码：')
    print()
    captcha, ctoken = get_captcha()
    url = API_HOST + '/official/ucenter/login/index'
    # headers ={
    #     'Host': 'capi.dangjianwang.com',
    #     'Connection': 'keep-alive',
    #     'Content-Length': '85',
    #     'Accept': 'application/json, text/javascript, */*; q=0.01',
    #     'Origin': 'https://www.dangjianwang.com',
    #     'Appid': '33beba686fd8333e',  # 无此项无法获取cookies
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
    #     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 \
    #     Safari/537.36 Core/1.63.6735.400 QQBrowser/10.2.2614.400',
    #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #     'Referer': 'https://www.dangjianwang.com/login',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'zh-CN,zh;q=0.9'
    # }
    data = {
        'username' : name,
        'password' : pwd,
        'captcha_code' : captcha,
        'captcha_token' : ctoken
    }
    rs = s.post(url, data , headers= headers)
    logger.info('登陆成功')
    cookies = rs.cookies.get_dict()
    logger.info('cookies : {}'.format(cookies))
    return cookies


# =====================================================
# 首页评论
# =====================================================
def cms():

    url = API_HOST+'/official/cms/article/list'  # 获取article_id的url
    data = {
        'menu_id' :	'90d0ac07a626a7a6b39c246d6532f7bd',  # 首页时政标签id,不会变化
        'page_index' :	'1',
        'page_size' : '10',
        'system_id' : '5d8e26a0798913e5117584c21a18d76a'  # 党建云系统id,不会变化
    }
    ids = get_id(url, data)
    url = API_HOST+'/official/cms/comment/add'  # 评论url
    for id in ids:
        data = {
            'article_id' : id,
            'content' : '关注',
            'img' : []
        }
        submit(url, data)
    logger.info('首页评论已完成')


# =====================================================
# 党员论坛
# =====================================================

def bbs():

    url = API_HOST+'/official/bbs/home/listBySys'  # 获取pid的url      
    data = {
        'page_index' :	'1',
        'page_size' : '2',
        'system_id' : '21888'  # 市直机关工委党建云id,不变
    }
    ids = get_id(url, data)
    url = API_HOST+'/official/bbs/comment/add'  # 回帖url
    for id in ids:
        data = {
            'content' : '关注',
            'img' : [],
            'pid' : id,
            'system_id' : '21888' 
        }
        submit(url, data)
    logger.info('党员论坛回复已完成')


# =====================================================
# 党员视角
# =====================================================

def view():
    url = API_HOST+'/official/view/View/publish'
    data = {
        'auth' : '0',
        'content' : '好',
        'img' : []
    }
    [submit(url, data) for i in range(2)]
    logger.info('党员视角发布已完成')


# =====================================================
# 学习心得体会
# =====================================================

def study():

    url = API_HOST + '/official/study/comment/add'
    data = {
        'content' : '不忘初心，方得始终。中国共产党人的初心和使命，就是为中国人民谋幸福，\
            为中华民族谋复兴。这个初心和使命是激励中国共产党人不断前进的根本动力。\
            全党同志一定要永远与人民同呼吸、共命运、心连心，永远把人民对美好生活的向往作为奋斗目标，\
            以永不懈怠的精神状态和一往无前的奋斗姿态，继续朝着实现中华民族伟大复兴的宏伟目标奋勇前进。',
        'mid' : 'ad0bdd6d140a3aa05945f3b7d6b3a74b'  # 对应学习材料习近平在首届中国国际进口博览会开幕式上的主旨演讲（2018.11.5），不变
    }
    submit(url, data)
    logger.info('学习心得体会已完成')


# =====================================================
# 答题 
# =====================================================

def exam():

    url = API_HOST + '/official/exam/competition/order'
    data = {'id' : '19'}
    answers = get_id(url, data)
    url = API_HOST + '/official/exam/competition/begin'
    ids = get_id(url, data)
    url = API_HOST + '/official/exam/ques/check'
    for id in ids:
        data = {
            'answer_loc' : '2',
            'bank_id' :	'19',
            'question_id' : id,
            'user_answer' : answers[id]
        }
        submit(url, data)
    logger.info('答题已完成')


# =====================================================
# 签到
# =====================================================

def checkin():

    url = API_HOST+'/official/ucenter/ucuser/checkin'
    data = {
        'client' : '2',
        'version' : '0.0.1'
    }
    submit(url, data)
    logger.info('签到已完成')


# =====================================================
# 在线学习时长 
# =====================================================

def study_time():

    url = API_HOST + '/official/study/Common/startStudy'
    submit(url)
    for i in range(303, -1, -1):
        print('还需要学习', end='')
        print(' {}秒'.format(i), end='\r')
        time.sleep(1)
    url = API_HOST + '/official/study/Common/endStudy'
    data = {
        'mid' : 'ad0bdd6d140a3aa05945f3b7d6b3a74b',
        'type' : '1',
        'web_time' : '305'
    }
    submit(url, data)
    logger.info('在线学习时长已完成')


def get_id(url, data):

    rs = s.post(url, data, headers=headers, cookies=cookies)
    if 'order' in url:    
        answers = {i.get('id'):i.get('answer') for i in rs.json()['data']['list']}
        return answers
    else:
        ids = [i.get('id') for i in rs.json()['data']['list']]
        return ids

def submit(url, data=None):

    s.post(url, data, headers=headers, cookies=cookies)
    time.sleep(2)
def main():

    cms()
    bbs()
    view()
    study()
    [exam() for i in range(2)]
    checkin()
    study_time()

if __name__ == "__main__":
    
    cookies = login()
    main()
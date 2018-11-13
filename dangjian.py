import requests
import time
from PIL import Image
import io

API_HOST = 'https://capi.dangjianwang.com'

s = requests.session()
# 通用headers
headers = {
    'Host': 'capi.dangjianwang.com',
    'Connection': 'keep-alive',
    # 'Content-Length': '1467',
    'Accept': 'application/json, text/plain, */*',
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
    headers = {
        'Host': 'capi.dangjianwang.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://www.dangjianwang.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 \
        Safari/537.36 Core/1.63.6735.400 QQBrowser/10.2.2614.400',
        'Referer': 'https://www.dangjianwang.com/login',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    rs = s.get(url, headers= headers, verify = False)
    # data={
    #     'captcha_token' : 'Ch62d1vosN'
    #     'captcha_url' : 'https://capi.dangjianwang.com/official/ucenter/login/getCaptcha?captcha_token=Ch62d1vosN'
    # }
    data = rs.json()['data']
    headers = {
        'Host': 'capi.dangjianwang.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 \
        Safari/537.36 Core/1.63.6735.400 QQBrowser/10.2.2614.400',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': 'https://www.dangjianwang.com/login',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    rs = s.get(data['captcha_url'], headers= headers, verify = False)
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
    captcha, ctoken = get_captcha()
    url = API_HOST + '/official/ucenter/login/index'
    headers ={
        'Host': 'capi.dangjianwang.com',
        'Connection': 'keep-alive',
        'Content-Length': '85',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://www.dangjianwang.com',
        'Appid': '33beba686fd8333e',  # 无此项无法获取cookies
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 \
        Safari/537.36 Core/1.63.6735.400 QQBrowser/10.2.2614.400',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://www.dangjianwang.com/login',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    data = {
        'username' : name,
        'password' : pwd,
        'captcha_code' : captcha,
        'captcha_token' : ctoken
    }
    rs = s.post(url, data , headers= headers, verify = False)
    
    cookies = rs.cookies.get_dict()
    return cookies

cookies = login()

# =====================================================
# 首页评论
# =====================================================

cms = [
    API_HOST+'/official/cms/article/list',  # 获取article_id的url
    {
        'menu_id' :	'90d0ac07a626a7a6b39c246d6532f7bd',  # 首页时政标签id,不会变化
        'page_index' :	'1',
        'page_size' : '10',
        'system_id' : '5d8e26a0798913e5117584c21a18d76a'  # 党建云系统id（另一个系统为郑州市直机关党建云），不会变化
    },
    API_HOST+'/official/cms/comment/add'  # 评论url
]

# =====================================================
# 党员论坛
# =====================================================

bbs = [
    API_HOST+'/official/bbs/home/listBySys',  # 获取pid的url      
    {
        'page_index' :	'1',
        'page_size' : '2',
        'system_id' : '21888'  # 市直机关工委党建云id,不变
    },
    API_HOST+'/official/bbs/comment/add'  # 回帖url
]

# =====================================================
# 党员视角
# =====================================================

view = [
    API_HOST+'/official/view/View/publish',
    {
        'auth' : '0',
        'content' : '好',
        'img' : []
    }
]

# =====================================================
# 学习
# =====================================================

study = [
    API_HOST + '/official/study/comment/add',
    {
        'content' : '不忘初心，方得始终。中国共产党人的初心和使命，就是为中国人民谋幸福，\
            为中华民族谋复兴。这个初心和使命是激励中国共产党人不断前进的根本动力。\
            全党同志一定要永远与人民同呼吸、共命运、心连心，永远把人民对美好生活的向往作为奋斗目标，\
            以永不懈怠的精神状态和一往无前的奋斗姿态，继续朝着实现中华民族伟大复兴的宏伟目标奋勇前进。',
        'mid' : 'ad0bdd6d140a3aa05945f3b7d6b3a74b'  # 对应学习材料习近平在首届中国国际进口博览会开幕式上的主旨演讲（2018.11.5），不变
    },
    API_HOST + '/official/study/Common/endStudy',
    {
        'mid' : 'ad0bdd6d140a3aa05945f3b7d6b3a74b',
        'type' : '1',
        'web_time' : '303'
    },
    API_HOST + '/official/study/Common/startStudy',
    API_HOST + '/official/ucenter/file/uptoken'
]

# =====================================================
# 答题 
# =====================================================
exam = [
    API_HOST + '/official/exam/competition/begin',
    API_HOST + '/official/exam/competition/order',
    {'id' : '19'},
    API_HOST + '/official/exam/ques/check'
]

# =====================================================
# 签到
# =====================================================

checkin = [
    API_HOST+'/official/ucenter/ucuser/checkin',
    {
        'client' : '2',
        'version' : '0.0.1'
    }
]

# cms,bbs,view,study,exam,checkin模式类似，共用
def get_id(url, data):
    rs = s.post(url, data , headers= headers,cookies = cookies, verify = False)
    if 'order' in url:    
        answers = {i.get('id'):i.get('answer') for i in rs.json()['data']['list']}
        return answers
    else:
        ids = [i.get('id') for i in rs.json()['data']['list']]
        return ids

def comment(url, id=None):

    if 'cms' in url:
        data = {
            'article_id' : id,
            'content' : '关注',
            'img' : []
        }
    elif 'bbs' in url:
        data = {
            'content' : '关注',
            'img' : [],
            'pid' : id,
            'system_id' : '21888' 
        }
    elif 'view' in url:
        data = view[1]

    elif 'uptoken' in url:
        data = None
    elif 'startStudy' in url:
        data = None
    elif 'endStudy' in url:
        data = study[3]
    elif 'study' in url:
        data = study[1]
    elif 'checkin' in url:
        data = checkin[1]
    elif 'exam' in url:
        data={
            'answer_loc' : '2',
            'bank_id' :	'19',
            'question_id' : id,
            'user_answer' : answers[id]
        }

    s.post(url, data , headers= headers,cookies = cookies, verify = False)
    time.sleep(2)

# 根据需要去掉注释即可完成相应模块

# [comment(cms[2], id) for id in get_id(cms[0], cms[1])]  # 评论10条
# print('评论完成')

# [comment(bbs[2], id) for id in get_id(bbs[0], bbs[1])]  # 论坛回复两次
# print('论坛回复完成')

# [comment(view[0]) for i in range(2)]  # 党员视角发布两条
# print('党员视角完成')

# comment(study[0])  # 学习心得体会
# print('学习心得体会完成')

# comment(study[5])
def uptokentest():
    url = 'https://capi.dangjianwang.com/official/ucenter/file/uptoken'
    rs = s.get(url, headers= headers, verify = False)
# uptokentest()
# print('发送uptoken')
comment(study[4])
print('发送start')
time.sleep(65)
for i in range(62):
    print(i,end='\r')
    time.sleep(1)
comment(study[2])  # 在线学习
print('发送end')
# comment(study[4])
# print('发送start')
print('在线学习完成')

answers = get_id(exam[1], exam[2])  # 获取题库答案
# [[comment(exam[3], id) for id in get_id(exam[0], exam[2])] for i in range(2)] # 答题2次
# print('答题完成')

# comment(checkin[0])  # 签到
# print('签到完成')
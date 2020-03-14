import re
import time
import datetime
import math
from dateutil.parser import parse
import jieba
import jieba.analyse
import json
import pynlpir
from weibotest.connect_database import *

# 去除微博里不需要的html标签
def ReHtml(content):
    pat = re.compile('<[^>]+>', re.S)
    # pat = re.compile('@(.*?)\s', re.S)
    return pat.sub('', content)

#去除微博不需要的符号
def ReSymbol(content):
    r = re.compile('//[^>]+:', re.I | re.M | re.S)
    s = r.sub('', content)
    r = re.compile('<[^>]+>', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''@.*?:''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''@.*?\s''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''【.*?】''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''#.*?#''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''&.*?;''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''//''', re.I | re.M | re.S)
    s = r.sub('', s)
    sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a\s])", "", s)
    r = re.compile(r'转发微博', re.I | re.M | re.S)
    sub_str = r.sub('', sub_str)
    r = re.compile(r'全文', re.I | re.M | re.S)
    sub_str = r.sub('', sub_str)
    return sub_str
    pass


# 创建停用词表
def stopWords():
    stopwords = [line.strip() for line in open('stop-words.txt', encoding='UTF-8').readlines()]
    # print(stopwords)
    return stopwords

def splittest():
    stop_words = [line.strip() for line in open('stop-words.txt', encoding='UTF-8').readlines()]
    pynlpir.open()

    id_list, text_list = DatabaseExecute()
    splited_words = []
    for i in text_list:
        split_content = pynlpir.segment(i, pos_tagging=False)
        str = ''
        for j in split_content:
            if (j not in stop_words and j != ' ' and len(j) > 1 and not j.isdigit()):
                str += j + ' '
        splited_words.append(str)
    pynlpir.close()

    return splited_words
def splittest1(content):
    stop_words = [line.strip() for line in open('stop-words.txt', encoding='UTF-8').readlines()]
    pynlpir.open()

    # id_list, text_list = DatabaseExecute()
    splited_words = []

    split_content = pynlpir.segment(content, pos_tagging=False)
    str = ''
    for j in split_content:
        if (j not in stop_words and j != ' ' and len(j) > 1 and not j.isdigit()):
            str += j + ' '
    splited_words.append(str)
    pynlpir.close()

    return splited_words
# 分词并去除停用词
def splitWords(content):
    split_content = jieba.cut(content.strip())
    stop_words = stopWords()
    splited_words = []
    for i in split_content:
        if (i not in stop_words) and i != ' ':
            splited_words.append(i)
    # print(splited_words)
    return splited_words



# 第一种微博热度计算
def Calc_HD(fl, re, cm):
    HD = math.log10(fl + 1) + math.sqrt(re) + cm
    HD=("%.2f"%HD)
    HD=float(HD)
    return HD
    pass


# 对时间进行数据清理
def parse_Date(date):
    # re匹配到刚刚这样的时间就把时间设置为现在的时间
    # time.localtime(time.time())可以将当前时间转为时间戳
    # time.strftime可以格式化时间戳
    if re.match('刚刚', date):
        date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
    # 匹配到几分钟前，用re取得所对应的数字进行处理，group（）用来提出分组截获的字符串
    if re.match('\d+分钟前', date):
        minute = re.match('(\d+)', date).group(1)
        date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(minute) * 60))
    if re.match('\d+小时前', date):
        hour = re.match('(\d+)', date).group(1)
        date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(hour) * 60 * 60))
    # 匹配到昨天，用re取得昨天后面所对应的数字进行处理，strip()去掉空格
    if re.match('昨天.*', date):
        date = re.match('昨天(.*)', date).group(1).strip()
        date = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60)) + ' ' + date
    if re.match('\d{2}-\d{2}', date):
        date = time.strftime('%Y-', time.localtime()) + date + ' 00:00'
    return date


# 计算两个日期之间的天数差
def calc_Days(target_time):
    current_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
    cut_time = ((parse(current_time) - parse(target_time)).days)
    return cut_time


# 提取话题
def getTopidc(content):
    rule = r'#(.*?)#'
    topic = re.findall(rule, content)
    topic = set(topic)
    all_topic = ''
    for i in topic:
        all_topic += '#' + i + "#"
    return all_topic
    pass


# TextRank提取关键词作为话题
def TextRank(content):
    all_topiclist = []
    if (len(content) <= 50):
        topK = 1
    elif (len(content) > 50 and len(content) <= 100):
        topK = 2
    else:
        topK = 3
    keywords = jieba.analyse.textrank(content, topK=topK, withWeight=True)
    stop_words = stopWords()
    all_topic = ''
    for keyword in keywords:
        if (keyword not in stop_words):
            all_topic = '#' + keyword[0] + "#"
            all_topiclist.append('#' + keyword[0] + "#")
    return all_topic, all_topiclist



def Test1():
    # 4371108037367742  # 重生# 19562.75722 2019-05-12 00:00
    item = {'hot': 19562.75722, 'id': '4371108037367742', 'topic': '#重生#'}
    with open("spider.txt", "r", encoding="utf-8") as f1:
        lists = f1.readlines()
        f1.close()
    with open("spider.txt", "w+", encoding="utf-8") as f:
        flag = True
        for i in lists:
            # 防止同一条微博两次记录
            if item['id'] == i[0:16]:
                flag = False
            rule = r'#(.*?)#'
            topic = re.findall(rule, i)
            topic = "#" + topic[0] + "#"
            print(topic)
            if item['topic'] == topic:
                print(11)
                hot = str(float(item['hot']) + float(i.split(' ')[2]))
                a = re.sub(i.split(' ')[2], hot, i)
                print(a)
                f.writelines(a)
            else:
                f.writelines(i)

        # if flag:
        #     f.write(item['id'] + ' ' + topic + ' ' + item['hot'] + ' ' + item['created_at'])
        #     f.write("\n")

        f.close()
    pass


if __name__ == '__main__':
    list = []
    test = '猜胜负赢大奖5月25日晚1935 江苏苏宁易购队对战河北华夏幸福队快来参与竞猜抽奖活动赢JBLCLIP2蓝牙音箱 '
    print(test)
    print(splittest1(test))

    # date = "昨天 11:09"
    # calc_Days(parse_Date(date))
    #
    # # content = '&quot;想做你指间的沙 流过你的虎口悬崖 你微微扬手我便绕指情柔&quot; '
    # content = "#asdf#asdf#asdf#"
    # # print(getTopidc(content))
    # # print(type(getTopidc(content)))
    # # print(Calc_HD(34137085,63872,11007))
    # test = '信你信你，无忧将来！ '
    # print(splitWords(ReHtml(test)))
    # print(TextRank(test))
    # keywords = jieba.analyse.textrank(test, topK=20, withWeight=True)
    # print(keywords)
    # Tse()
    # stopWords()
    # Test1()
    pass

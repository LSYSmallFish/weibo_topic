import jieba
import jieba.posseg as pseg
import os
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from weibotest.connect_database import *
import numpy
import math
import pynlpir

#中科院分词
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

#jieba分词
def splitWords():
    stop_words = [line.strip() for line in open('stop-words.txt', encoding='UTF-8').readlines()]
    id_list, text_list = DatabaseExecute()
    splited_words_list = []
    for i in text_list:
        split_content = jieba.cut(i.strip())
        splited_words = []
        str = ''
        for j in split_content:
            if (j not in stop_words) and j != ' ':
                str += j + ' '
        splited_words_list.append(str)
        # print(splited_words)
        pass

    return splited_words_list


def TFIDF():
    text_list = splittest()
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(text_list))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    # print(word)
    weight = tfidf.toarray()

    # print(weight)
    for i in range(50):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print(u"-------这里输出第", i, u"个文本的词语tf-idf权重------")
        for j in range(len(word)):
            if(weight[i][j]>0):
                print(word[j],weight[i][j])
    # sm = cosine_similarity(weight)
    # for i in range(1):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    #     for j in range(len(sm[i])):
    #         if (sm[i][j] > 0.1):
    #             print(sm[i][j], text_list[j])
    #             print('\n')
    # for i in sm:
    #     for j in i:
    #         if(j>0.1 and j<0.99):
    #             print(j)
    return weight, word, text_list
    pass


# 计算两个文本向量的余弦相似度
def Calc_Cos(w1, w2):

    #     pass
    product = numpy.matmul(w1, w2)
    length_product = numpy.linalg.norm(w1) * numpy.linalg.norm(w2)
    if (length_product == 0):
        return 0.0
    else:
        Cos = product / length_product
        return Cos

#single-pass聚类
def Single_Pass(weight, word, text_llist):
    # a=weight[0].tolist()
    # print(word[a.index(max(a))])

    #获取热度值
    hot_list=getHot()

    #总话题簇列表
    cluster = []
    #新话题簇列表
    new_cluster = []
    #将第一个文本向量作为新话题簇
    new_cluster.append(weight[0])
    #将第一个话题簇加入话题簇列表
    cluster.append(new_cluster)

    #将第一个文本向量用列表表示向量矩阵
    a = weight[0].tolist()
    #总话题关键词列表
    new_keyword = []
    #新话题关键词列表
    key_words = []
    #在词袋中找到文本向量中，权值最大的词加入话题关键词列表，这个词就代表这个文本
    new_keyword.append(word[a.index(max(a))])
    #将话题关键词加入总列表
    key_words.append(new_keyword)

    #话题名
    topicwords_list = []
    new_topicword = []
    topicwords_dict = {}
    #构建话题字典，关键词作为key值，权值作为value值
    topicwords_dict[word[a.index(max(a))]] = max(a)
    new_topicword.append(topicwords_dict)
    topicwords_list.append(new_topicword)

    #将热度之加入列表
    hots = []
    hots.append(hot_list[0])
    # print(a)

    #从第二个文本开始遍历
    for i in range(1, len(weight)):
        #flag作为标识，True代表有大于阈值的簇
        flag = False
        #相似度字典
        similar_dict = {}

        #遍历话题簇
        for j in range(len(cluster)):

            #话题簇列表中的每个话题簇的第一个文本为话题簇中心，和它进行相似度计算
            similar = Calc_Cos(weight[i], cluster[j][0])
            #大于阈值
            if (similar > 0.1 and similar < 0.99):
                #将其加入字典，其实是做标记，等等所有大于阈值的话题簇进行比较
                similar_dict[j] = similar
                flag = True

        if (flag):
            #如果有大于阈值的话题簇，则选取最大的那个簇
            index = max(similar_dict, key=similar_dict.get)
            #将文本加入改话题簇，并更新为簇中心
            cluster[index].insert(0, weight[i])

            #将代表该话题的关键词加入列表
            a = weight[i].tolist()[1:]
            key_words[index].insert(0, word[a.index(max(a))])

            #将该话题的关键词以及权值加入话题名列表，最后进行比较选取值最大的关键词作为话题名
            topicwords_list[index].insert(0, {word[a.index(max(a))]: max(a)})

            #改文本的热度值也计算如改话题的热度值中
            hots[index]+=hot_list[i]

        else:
            #如果所有话题簇没有大于阈值的，将该文本归为新话题簇
            new_cluster = []
            new_cluster.append(weight[i])
            cluster.append(new_cluster)

            #文本关键词作为新的关键词加入
            a = weight[i].tolist()
            new_keyword = []
            new_keyword.append(word[a.index(max(a))])
            key_words.append(new_keyword)

            new_topicword=[]
            new_topicword.append({word[a.index(max(a))]: max(a)})
            topicwords_list.append(new_topicword)

            hots.append(hot_list[i])

    # print(key_words)
    # print(len(cluster[6]))
    # print(len(topicwords_list))
    # print(len(cluster))
    #
    # print(len(hots))
    # print(hots)
    return topicwords_list,hots,key_words


#获得话题名
def getTopic(topicword_list,word,hots,key_words):
    topic_list=[]
    #获得热度值
    hot_list=hots.copy()
    #遍历话题名列表
    for i in range(len(topicword_list)):
        topic = []
        #遍历每个话题簇中的文本向量
        for j in range(len(topicword_list[i])):

            sum=0
            #获得关键词
            #获得关键词权值
            key = list(topicword_list[i][j])[0]
            value = list(topicword_list[i][j].values())[0]
            #遍历词袋，判断关键词在所有文本出现的总次数
            for k in word:
                if(key==k):
                    sum+=1
            #关键词*总次数的值作为判断依据
            topic.append(sum*value)

        #获取到最大的那个值作为话题名
        topic_list.append(list(topicwords_list[i][topic.index(max(topic))])[0])

    temp=[]
    #获取热度值最大的50个话题
    for i in range(50):
        temp.append(hot_list.index(max(hot_list)))
        hot_list[hot_list.index(max(hot_list))]=0
    # print(temp)
    top_list=[]
    #提取话题关键词
    for j in temp:
        top=[]
        top.append(topic_list[j])
        top.append(hots[j])
        str=''
        for k in set(key_words[j]):
            str+=k+' '
        top.append(str)
        top_list.append(top)
    print(top_list)
    return top_list
    # print(topic_list)
    # print(set(topic_list))
#将话题信息插入数据库
def insertDatabase(topic_list):
    insertTopic(topic_list)
    pass
if __name__ == "__main__":
    # print(splitWords()[0])

    weight, word, text_list = TFIDF()

    topicwords_list,hots,key_words=Single_Pass(weight, word, text_list)
    top_list=getTopic(topicwords_list,word,hots,key_words)
    insertDatabase(top_list)



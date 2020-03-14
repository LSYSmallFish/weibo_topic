# coding: utf-8
# 安装驱动 pymysql
import pymysql.cursors


def DatabaseExecute():
    # 1.连接mysql数据库
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='scrapytest1',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.SSCursor)

    # 2.通过cursor创建游标
    cursor = connection.cursor()

    # 创建sql语句
    # sql = "INSERT INTO `users` (`email`, `password`) VALUES ('huzhiheng@itest', '1236')"

    # 执行SQL语句
    # cursor.execute(sql)

    # 提交SQL语句
    # connection.commit()

    # 执行数据查询
    # sql = "SELECT `id`, `password` FROM `users` WHERE `email`='huzhiheng@itest.info'"
    # cursor.execute(sql)

    # 查询数据库单条数据
    # result = cursor.fetchone()
    # print(result)

    # print("-----------华丽分割线------------")

    # 执行数据查询
    sql = "SELECT `id`, `text`, `hot`  FROM `blog`"
    cursor.execute(sql)

    # 查询数据库多条数据
    result = cursor.fetchone()
    # for data in result:
    #     print(type(data))
    id_list = []
    text_list = []
    while result is not None:
        # print(result[0])
        id_list.append(result[0])
        text_list.append(result[1])
        result = cursor.fetchone()

    # 关闭光标
    cursor.close()
    # 关闭数据连接
    connection.close()
    return id_list, text_list
    pass


def getHot():
    # 1.连接mysql数据库
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='scrapytest1',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.SSCursor)

    # 2.通过cursor创建游标
    cursor = connection.cursor()

    # 执行数据查询
    sql = "SELECT `hot` FROM `blog`"
    cursor.execute(sql)

    # 查询数据库多条数据
    result = cursor.fetchone()
    # for data in result:
    #     print(type(data))
    hot_list = []
    while result is not None:
        hot_list.append(result[0])
        result = cursor.fetchone()

    # 关闭光标
    cursor.close()
    # 关闭数据连接
    connection.close()
    return hot_list
    pass


def insertTopic(top_list):
    # 1.连接mysql数据库
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='scrapytest1',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.SSCursor)

    # 2.通过cursor创建游标
    cursor = connection.cursor()
    sql="TRUNCATE table topic"
    cursor.execute(sql)
    connection.commit()
    # 执行数据插入
    for i in range(len(top_list)):
        sql = "INSERT INTO topic(topic_id,topic_name,topic_keywords,hot) VALUES ('%d', '%s', '%s','%f')" % (
        i+1, top_list[i][0], top_list[i][2], top_list[i][1])
        # print(sql)
        cursor.execute(sql)
    connection.commit()
    # 关闭光标
    cursor.close()
    # 关闭数据连接
    connection.close()
    pass


if __name__ == '__main__':

    id_list, textlist = DatabaseExecute()
    # for i in textlist:
    #     print(len(i))
    if (textlist[-2] == ' '):
        print(1)

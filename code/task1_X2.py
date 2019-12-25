# -*- coding:utf-8 -*-
#重新统计消费金额，获取食堂消费数据和18级学生消费数据
import pandas as pd
import datetime as dt
# 未处理非营业值的数据集
info = pd.read_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task1_X1.csv',encoding='gbk')

#按时间间隔将数据切分，时间间隔取20min
timelist = {}
i = 6
for j in range(54):

    if (j)%3==0:
        timelist[j] = dt.time(i,0,0)
    elif j%3==1:
        timelist[j] = dt.time(i,20,0)
    else:
        timelist[j] = dt.time(i,40,0)
        i = i+1
print(timelist)

#对消费记录进行整理
def recount(d2):
    Day = [] #存放时间，代表收集数据所涉及的日期
    Cardno = []  #存放卡号，代表该天进行过消费的同学
    dic1 = {}  #存放一天内同学消费记录所在的行
    now_p = {}  #存放一天内，限定时间30min内，同学所在的消费场所
    timeline = dt.time(0,0,0) #存放时间段

    new_data = pd.DataFrame()
    new_data['Time'] = dt.time(0, 0, 0)
    new_data['Timeline'] = dt.time(0, 0, 0)
    new_data['Day'] = dt.date(2019, 1, 1)
    new_data['CardNo'] = 'a'
    new_data['Money'] = 0
    new_data['Dept'] = 'a'
    # 提取元数据集所在列的编号
    d = list(d2.columns).index('Day')
    t = list(d2.columns).index('Time')
    c = list(d2.columns).index('CardNo')
    p = list(d2.columns).index('Dept')
    m = list(d2.columns).index('Money')

    t2 = list(new_data.columns).index('Time')
    m2 = list(new_data.columns).index('Money')
    print('开始运行：')
    for i in range(len(d2)):
        print(i)
        day = [d2.iloc[i, d]]
        cardno = [d2.iloc[i, c]]
        time = pd.to_datetime(d2.iloc[i, t])  # 可能出现格式错误
        money = d2.iloc[i, m]
        place = [d2.iloc[i, p]]
        for j in range(len(timelist)):
            if j < (len(timelist) - 1):
                if timelist[j] <= time.time() < timelist[(j + 1)]:
                    timeline = timelist[j]
                    break
            else:
                if timelist[j] <= time.time():
                    timeline = timelist[j]
        if set(day) & set(Day):
            if set(cardno) & set(Cardno):
                if set(place) & set([now_p[cardno[0]]]):
                    if (time - pd.to_datetime(new_data.iloc[dic1[cardno[0]], t2])).seconds<=1800:
                        new_data.iloc[dic1[cardno[0]], m2] = money + new_data.iloc[dic1[cardno[0]], m2]
                    else:
                        # update the record
                        new_data = new_data.append([{'Day': d2.iloc[i, d], 'Time': d2.iloc[i, t], 'CardNo': d2.iloc[i, c],
                              'Money': d2.iloc[i, m], 'Dept': d2.iloc[i, p],'Timeline': timeline}])
                        dic1[cardno[0]] = len(new_data) - 1
                # this student moved to another place to buy something
                else:
                    # update the record
                    new_data = new_data.append([{'Day': d2.iloc[i, d], 'Time': d2.iloc[i, t], 'CardNo': d2.iloc[i, c],
                                                 'Money': d2.iloc[i, m], 'Dept': d2.iloc[i, p],'Timeline': timeline}])
                    now_p[cardno[0]] = place[0]
                    dic1[cardno[0]] = len(new_data) - 1  # 重新定点该同学的位置，时间
            # a new student who did not buy anything on this day
            else:
                Cardno = Cardno + cardno # record this student in today's list
                # update the record
                new_data = new_data.append([{'Day': d2.iloc[i, d], 'Time': d2.iloc[i, t], 'CardNo': d2.iloc[i, c],
                                             'Money': d2.iloc[i, m], 'Dept': d2.iloc[i, p],'Timeline': timeline}])
                now_p[cardno[0]] = place[0]
                dic1[cardno[0]] = len(new_data) - 1
        # a new day
        else:
            dic1 = {}  # new turn
            now_p = {}  # new turn
            Day = Day + day  # update the content of the Day list
            Cardno = cardno  # update the content of the Cardno list
            # update the record
            new_data = new_data.append([{'Day': d2.iloc[i, d], 'Time': d2.iloc[i, t], 'CardNo': d2.iloc[i, c],
                                         'Money': d2.iloc[i, m], 'Dept': d2.iloc[i, p],'Timeline': timeline}])
            now_p[cardno[0]] = place[0]
            dic1[cardno[0]] = len(new_data) - 1  # update the content of the dic1
    print('新生成表格。')
    return new_data

new_info=recount(info)
print('去除 Time 列。')
new_info = new_info.drop('Time',axis=1)#去除
new_info.to_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task1_X2.csv',encoding='gbk',index=None)

#食堂数据集（只需消费记录，因此用前一次版本的）
cus = new_info[new_info['Dept'].isin(['第一食堂','第二食堂','第三食堂','第四食堂','第五食堂','教师食堂'])]
cus.to_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task1_X3.csv',encoding='gbk',index=None)
#18级消费数据
info = pd.read_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/project_data/data1.csv',encoding='gbk',index_col=0)
eighteenth = pd.merge(new_info,info,on='CardNo')
eighteenth.to_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task1_X4.csv',encoding='gbk',index=None)

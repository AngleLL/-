# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib
import  matplotlib.pyplot as plt
pd.set_option('display.max_columns', None) #完全显示
stats = pd.read_excel('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task3_X3.xlsx',encoding='gbk',index_col=0)
print(stats)
#画饼
#先计算总和
#再用总和来画饼
def bingtu(data):
    data['sum'] = data['Label_0']+data['Label_2']+data['Label_3']
    string = input('请输入该表格名称：')
    num = len(data) #查看就餐总人次
    str2 = '                            ——18级学生4月参与消费人数为：'+str(num)
    value = data['sum'].value_counts()
    print(value)#看看怎么解决标签的问题
    No = list(value.index)  # 餐厅，做标签
    matplotlib.rcParams['font.sans-serif']=['SimHei'] #解决中文乱码问题
    length = [i/20 for i in range(value.size)]
    plt.pie(value,autopct='%.2f %%',explode=length,labels=No,labeldistance=1.1)
    plt.title(string+'\n'+str2)
    path = 'C:/Users/lenovo/Desktop/学生校园消费行为分析/pic/'+string+'.png'
    plt.savefig(path)
    plt.show()

print('将绘制聚类结果饼图')
bingtu(stats)

#从0到3进行组合切割
L_0_0 = stats[stats['Label_0']==0]
L_0_1 = stats[stats['Label_0']==1]
L_0_2 = stats[stats['Label_0']==2]

L_0_0_0 = L_0_0[L_0_0['Label_2']==0]
L_0_0_1 = L_0_0[L_0_0['Label_2']==1]
L_0_0_2 = L_0_0[L_0_0['Label_2']==2]

L_0_1_0 = L_0_1[L_0_1['Label_2']==0]
L_0_1_1 = L_0_1[L_0_1['Label_2']==1]
L_0_1_2 = L_0_1[L_0_1['Label_2']==2]

L_0_2_0 = L_0_2[L_0_2['Label_2']==0]
L_0_2_1 = L_0_2[L_0_2['Label_2']==1]
L_0_2_2 = L_0_2[L_0_2['Label_2']==2]

L_000 = L_0_0_0[L_0_0_0['Label_3']==0]
L_000['Label']='000'
L_001 = L_0_0_0[L_0_0_0['Label_3']==1]
L_001['Label']='001'
L_002 = L_0_0_0[L_0_0_0['Label_3']==2]
L_002['Label']='002'
L_003 = L_0_0_0[L_0_0_0['Label_3']==3]
L_003['Label']='003'

L_010 = L_0_0_1[L_0_0_1['Label_3']==0]
L_010['Label']='010'
L_011 = L_0_0_1[L_0_0_1['Label_3']==1]
L_011['Label']='011'
L_012 = L_0_0_1[L_0_0_1['Label_3']==2]
L_012['Label']='012'
L_013 = L_0_0_1[L_0_0_1['Label_3']==3]
L_013['Label']='013'

L_020 = L_0_0_2[L_0_0_2['Label_3']==0]
L_020['Label']='020'
L_021 = L_0_0_2[L_0_0_2['Label_3']==1]
L_021['Label']='021'
L_022 = L_0_0_2[L_0_0_2['Label_3']==2]
L_022['Label']='022'
L_023 = L_0_0_2[L_0_0_2['Label_3']==3]
L_023['Label']='023'

L_100 = L_0_1_0[L_0_1_0['Label_3']==0]
L_100['Label']='100'
L_101 = L_0_1_0[L_0_1_0['Label_3']==1]
L_101['Label']='101'
L_102 = L_0_1_0[L_0_1_0['Label_3']==2]
L_102['Label']='102'
L_103 = L_0_1_0[L_0_1_0['Label_3']==3]
L_103['Label']='103'

L_110 = L_0_1_1[L_0_1_1['Label_3']==0]
L_110['Label']='110'
L_111 = L_0_1_1[L_0_1_1['Label_3']==1]
L_111['Label']='111'
L_112 = L_0_1_1[L_0_1_1['Label_3']==2]
L_112['Label']='112'
L_113 = L_0_1_1[L_0_1_1['Label_3']==3]
L_113['Label']='113'

L_120 = L_0_1_2[L_0_1_2['Label_3']==0]
L_120['Label']='120'
L_121 = L_0_1_2[L_0_1_2['Label_3']==1]
L_121['Label']='121'
L_122 = L_0_1_2[L_0_1_2['Label_3']==2]
L_122['Label']='122'
L_123 = L_0_1_2[L_0_1_2['Label_3']==3]
L_123['Label']='123'

#转化为文件
stats = L_000.append([L_001,L_002,L_003,L_010,L_011,L_012,L_013,L_020,L_021,L_022,L_023,
                      L_100,L_101,L_102,L_103,L_110,L_111,L_112, L_113,L_120,L_121,L_122,L_123])

# print(stats.shape)
# print(stats.tail(3))
stats.to_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task3_X4.csv',encoding='gbk')
#统计分析
stats['Count'] = stats['Count'].apply(pd.to_numeric)
lib = stats['Label'].value_counts()
lib = list(lib.index)
lib.sort()
for item in lib:
    print('Label: ',item)
    print(stats[stats['Label']==item].describe())
    print('\n')





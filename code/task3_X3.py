# -*- coding:utf-8 -*-
#进行聚类
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
stats = pd.read_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task3_X2.csv',encoding='gbk',index_col=0)
print(stats.head(3))
print(stats.describe()) #对计算指标进行统计，以辅助后面的聚类分析

#对不同变量的异常值处理模块：
#为了说明
def draw(data,x):
    plt.scatter(data.iloc[:, x], data.iloc[:, x], 50, color='orange', marker='+')
    plt.xlabel(x)
    plt.ylabel(x)
    s = '散点图_' + str(x)
    path = 'C:/Users/lenovo/Desktop/学生校园消费行为分析/pic/' + s + '.png'
    plt.savefig(path)
    plt.show()

# print('聚类前异常值处理判断：')
# draw(stats,0)
# draw(stats,2)
# draw(stats,3)

stats = stats[stats['work_mean']<22] #对均值异常值处理
# stats = stats[stats['holiday_mean']<28] #对周末均值异常值处理

#对进行了异常值处理后的数据进行离差标准化处理
def MinMaxScale(data):
    return (data - data.min())/(data.max() - data.min())
for i in range(4):
    stats.iloc[:,i] = MinMaxScale(stats.iloc[:,i])
print('数据经离差标准化处理。')
print(stats.head(3))

#聚类结果可视化
def result(x,y,k,model,cons):
    #查看聚类结果
    print(model.cluster_centers_)
    #在原始表格中添加聚类结果
    cons['Label'] = model.labels_
    #绘图查看i
    result = []
    col = ['orange','gold','green','blue','red','brown','purple','deeppink','royalblue']
    for j in range(k):
        result.append(cons.loc[cons['Label'] == j])
        plt.scatter(result[j].iloc[:, x], result[j].iloc[:, y], 50, color=col[j], marker='+')
    plt.xlabel(x)
    plt.ylabel(y)
    s = '_' + str(x) + str(y)+str(k)
    path = 'C:/Users/lenovo/Desktop/学生校园消费行为分析/pic/task3/散点图/' + s + '.png'
    plt.savefig(path)
    plt.show()

# #对聚类的试值
# #聚类-外部距离最大化，内部距离最小化
# a_cons = stats.iloc[:,[2]] #用以改变需要聚类的变量
# a_cons = a_cons.values
# for k in range(2,9):
#     model = KMeans(n_clusters=k).fit(a_cons)
#     res = silhouette_score(a_cons,model.labels_)
#     print(k,'\t',res)
#     result(2,2,k,model,stats)

#将聚类结果写入表格
def bulit(x,k,model,cons):
    #查看聚类结果
    print(model.cluster_centers_)
    #在原始表格中添加聚类结果
    lab = 'Label_'+str(x)
    cons[lab] = model.labels_
    z = 'task3_X3_'+str(x)+str(k)
    path = 'C:/Users/lenovo/Desktop/学生校园消费行为分析/result/'+z+'.csv'
    cons.to_csv(path,encoding='gbk')

# #对消费频率进行分类
# a_cons = stats.iloc[:,[0]]
# a_cons = a_cons.values
# model = KMeans(n_clusters=3).fit(a_cons)
# res = silhouette_score(a_cons,model.labels_)
# print(res)
# bulit(0,3,model,stats)

#对工作日消费均值进行分类
a_cons = stats.iloc[:,[2]]
a_cons = a_cons.values
model = KMeans(n_clusters=3).fit(a_cons)
res = silhouette_score(a_cons,model.labels_)
print(res)
bulit(2,3,model,stats)

# #对周末消费均值进行分类
# a_cons = stats.iloc[:,[3]]
# a_cons = a_cons.values
# model = KMeans(n_clusters=6).fit(a_cons)
# res = silhouette_score(a_cons,model.labels_)
# print(res)
# bulit(3,6,model,stats)


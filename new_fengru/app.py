from flask import Flask, render_template, request, jsonify, session
from read import readtxt, parseInt
import os
import mysql.connector
import numpy as np

app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="liubowen0101LBW",
    database="buaa_sch"
)

sch_id = 0


def getBaseInfo(sch_id):
    BaseInfo = []
    list = []
    dict = {}
    mycursor = mydb.cursor()
    sql = "SELECT name, position, subDepartment FROM scholar WHERE id =" + str(sch_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        BaseInfo.append(x)
    sql = "SELECT * FROM people_paper WHERE peopleId=" + str(sch_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    BaseInfo.append(len(myresult))
    for x in myresult:
        list.append(x[0])
    for x in list:
        sql = "SELECT title, publicYear FROM paper WHERE id=" + str(x) + " ORDER BY publicYear DESC"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if str(myresult[0][1]) == "None":
            continue
        if myresult[0][1] not in dict:
            dict.update({myresult[0][1]: [myresult[0][0]]})
        else:
            if len(dict[myresult[0][1]]) < 10:
                dict[myresult[0][1]].append(myresult[0][0])

    dic = sorted(dict.items(), key=lambda d: d[0], reverse=True)
    return BaseInfo, dic



def getPaperList(sch_id):
    id_list = []
    dict = {}
    mycursor = mydb.cursor()
    sql = "SELECT * FROM people_paper WHERE peopleId=" + str(sch_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        id_list.append(x[0])
    for x in id_list:
        sql = "SELECT title, publicYear FROM paper WHERE id=" + str(x) + " ORDER BY publicYear DESC"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if str(myresult[0][1]) == "None":
            continue
        if myresult[0][1] not in dict:
            dict.update({myresult[0][1]: [myresult[0][0]]})
        else:
            if len(dict[myresult[0][1]]) < 5:
                dict[myresult[0][1]].append(myresult[0][0])

    dic = sorted(dict.items(), key=lambda d: d[0], reverse=True)
    return dic


@app.route('/')
def Home():
    return render_template("home.html")

@app.route('/predict')
def toPredict():
    return render_template("predict.html")

@app.route('/re/<int:id>')
def toResult(id):
    global sch_id
    sch_id = id
    infoList, _ = getBaseInfo(id)
    print(infoList)
    name = infoList[0][0]
    position = infoList[0][1]
    department = infoList[0][2]
    public = infoList[1]
    return render_template("re.html",name=name,position=position,department=department,public=public)

@app.route('/paper', methods=['POST','GET'])
def getPaper():
    _, paperList = getBaseInfo(sch_id)
    return jsonify(paper = [x for x in paperList])


@app.route('/data', methods=['POST', 'GET'])
def charts():
    list1 = [40, 50, 55, 62, 42, 84, 88, 92, 102]
    list2 = [50, 60, 62, 68, 70, 89, 104, 123, 151]
    list3 = [2001, 2002, 2010, 2022, 2023, 2033, 2034, 2035, 2036, 2037]
    l1 = list1.copy()
    l2 = list2.copy()
    l1.sort()
    l2.sort()
    Min1 = l1[0] - 5
    Max1 = l1[-1] + 10
    Min2 = l2[0] - 5
    Max2 = l2[-1] + 10

    return jsonify(amount1=[x for x in list1], amount2=[x for x in list2], year=[x for x in list3], Min1=Min1,
                   Max1=Max1, Min2=Min2, Max2=Max2)

@app.route('/data_ra', methods=['POST', 'GET'])
def ret():
    list = [5, 2, 3, 5, 5]
    return jsonify(ability=[x for x in list])

@app.route('/data5', methods=['POST', 'GET'])
def getD():
    amount1 = [5, 6, 7, 8, 9, 10, 11, 12, 13]
    amount2 = [15, 25, 32, 37, 41, 44, 46, 47, 47]
    avg1 = [20, 20, 20, 20, 20, 20, 20, 20, 20]
    avg2 = [60, 60, 60, 60, 60, 60, 60, 60, 60]
    year = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    l1 = amount1.copy()
    l2 = amount2.copy()
    l3 = avg1.copy()
    l4 = avg2.copy()
    l1.sort()
    l2.sort()
    l3.sort()
    l4.sort()
    min1 = min(l1[0],l3[0]) - 5
    min2 = min(l2[0],l4[0]) - 5
    max1 = max(l1[-1],l3[-1]) + 10
    max2 = max(l2[-1],l4[-1]) + 10
    return jsonify(amount1 = [x for x in amount1], amount2 = [x for x in amount2], avg1 = [x for x in avg1], avg2 = [x for x in avg2], year = [x for x in year], min1=min1, min2=min2, max1=max1, max2=max2)








if __name__ == '__main__':
    app.run()

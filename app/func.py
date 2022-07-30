
from ast import Pass
from hashlib import new
import json 
import random
import sqlalchemy
from app import app
from app import db
from app.models import Student, Teacher, Manager, Course, Student_Class_table, Class, Major, Dept,Account
engine = sqlalchemy.create_engine( 'postgresql+psycopg2://gaussdb:123@QWEasd@122.9.68.170:15432/css',pool_pre_ping=True)

import re     
day_map = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,1:'一',2:'二',3:'三',4:'四',5:'五',6:'六',7:'七'}


def classtime_judge(newTime,classes):
    timebox=[[0 for j in range(14)] for i in range(8)]
    newtimebox = [[0 for j in range(14)] for i in range(8)]
    time_transform(newTime,newtimebox)
    for cla in classes:
        print(cla.ClassTime)
        time_transform(cla.ClassTime,timebox)
        if time_overlap_check(newtimebox,timebox):
            return cla
    return None
  
def time_transform(time,timebox):
    times = time.split(' ')
    for time in times :
        import re
        if re.match(r'[一二三四五六七][1-9][0-9]*-[1-9][0-9]*', time):
            day = day_map[time[0]]
            endpoints = re.compile(r'\d+').findall(time)
            if len(endpoints)==2:
                a,b = endpoints[:]
                le = min(int(a),int(b))
                re = max(int(a),int(b))
                for _ in range(le,re+1):
                    timebox[day][_]=1

def time_overlap_check(box1,box2):
    for i in range(8):
        for j in range(14):
            if box1[i][j] and box2[i][j] :
                return True
    return False


# StudentNum = '19000000'
# student = Student.query.filter_by(StudentNum = StudentNum).first()
# classnum = '00814022_1001'
# cla = Class.query.filter_by(ClassNum=classnum)
# test = "一5-6   四7-8 全英语"
# test2 = "二3-6 123 四5-6"
# timebox=[[0 for j in range(14)] for i in range(8)]
# timebox2=[[0 for j in range(14)] for i in range(8)]
# time_transform(test,timebox)
# time_transform(test2,timebox2)
# # print(time_overlap_check(timebox,timebox2))
# print(classtime_judge(test,student.Classes))
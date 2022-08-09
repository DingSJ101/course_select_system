import xlrd # read excel
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
deptnames = ['马克思主义学院','文学院','外国语学院','法学院','社会学院', #1
'新闻传播学院','钱伟长学院','理学院','通信与信息工程学院','计算机工程与科学学院',#6
'机电工程与自动化学院','材料科学与工程学院','环境与化学工程学院','生命科学学院','中欧工程技术学院',#11
'微电子学院力学与工程科学学院','经济学院','管理学院','悉尼工商学院','图书情报档案系',#16
'上海美术学院','上海电影学院','音乐学院','上海温哥华电影学院','社区学院',#21
'体育学院','社会科学学部','国际交流学院','土木工程系']# 26
deptnums = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0011', '0012', '0013', '0014', '0015', '0016', '0017', '0018', '0019', '0020', '0021', '0022', '0023', '0024', '0025', '0026', '0027', '0028', '9999']
major2deptnum=[
    22,17,17,17,4,4,5,5,1,2,
    23,2,3,3,6,6,6,6,2,8,
    8,8,8,8,11,11,11,11,11,11,
    12,12,12,12,12,7,11,9,12,9,
    8,9,8,11,10,22,10,10,22,29,
    13,11,13,9,14,21,21,14,18,18,
    18,18,18,18,18,20,20,18,11,23,
    23,22,22,22,22,22,22,22,21,21,
    21,21,21,21,21,6
]
majornames=['哲学', '经济学', '金融学', '国际经济与贸易', '法学', '知识产权', '社会学', '社会工作', '思想政治教育', '汉语言文学', '汉语言', '汉语国际教育', '英语', '日语', '新闻学', '广播电视学', '广告学', '网络与新媒体', '历史学', '数学与应用数学', '信息与计算科学', '应用物理学', '应用化学', '理论与应用力学', '机械工程', '机械设计制造及其自动化', '机械电子工程', '工业设计', '智能制造工程', '测控技术与仪器', '材料物理', '冶金工程', '金属材料工程', '无机非金属材料工程', '高分子材料与工程', '材料设计科学与工程', '电气工程及其自动化', '电子信息工程', '电子科学与技术', '通信工程', '微电子科学与工程', '光电信息科学与工程', '电子信息科学与技术', '自动化', '计算机科学与技术', '数字媒体技术', '智能科学与技术', '网络空间安全', '电影制作', '土木工程', '化学工程与工艺', '包装工程', '环境工程', '生物医学工程', '食品科学与工程', '建筑学', '城乡规划', '生物工程', '管理科学', '信息管理与信息系统', '工程管理', '工商管理', '会计学', '财务管理', '人力资源管理', '档案学', '信息资源管理', '物流管理', '工业工程', '音乐表演', '音乐学', '表演', '戏剧影视文学', '广播电视编导', '戏剧影视导演', '戏剧影视美术设计', '动画', '影视摄影与制作', '美术学', '绘画', '雕塑', '中国画', '视觉传达设计', '环境设计', '数字媒体艺术', '艺术与科技']
majornums=['010101', '020101', '020301K', '020401', '030101K', '030102T', '030301', '030302', '030503', '050101', '050102', '050103', '050201', '050207', '050301', '050302', '050303', '050306T', '060101', '070101', '070102', '070202', '070302', '080101', '080201', '080202', '080204', '080205', '080213T', '080301', '080402', '080404', '080405', '080406', '080407', '080415T', '080601', '080701', '080702', '080703', '080704', '080705', '080714T', '080801', '080901', '080906', '080907T', '080911TK', '080913T', '081001', '081301', '081702', '082502', '082601', '082701', '082801', '082802', '083001', '120101', '120102', '120103', '120201K', '120203K', '120204', '120206', '120502', '120503', '120601', '120701', '130201', '130202', '130301', '130304', '130305', '130306', '130307', '130310', '130311T', '130401', '130402', '130403', '130406T', '130502', '130503', '130508', '130509T']


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

def deptname2deptnum(deptname):
    if deptname in deptnames :
        return deptnums[deptnames.index(deptname)]
    else :
        return '9999'
def majorname2majornum(majorname):
    if majorname in majornames :
        return majornums[majornames.index(majorname)]
    else :
        return '000000'
def load_student_from_file(filepath):
    new_student_numbers = []
    new_student_names = []
    maxNum = int(Student.query.order_by(-Student.StudentNum).first().StudentNum ) + 1
    # file txt format :
    # Order | StudentName | DeptName | MajorName
    filetype = filepath.split('.')[-1]
    file_extension = filepath.split('.')[-1]
    if(file_extension == 'xlsx' or file_extension == 'xls'):
        filetype = 'excel'
    if(file_extension == 'txt'):
        filetype = 'txt'
    
    if filetype == 'txt':
        f = open(filepath,encoding = "utf-8")
        for i , line in enumerate(f.readlines()):
            order , name , dept , major  =  re.split(r' +|\n|\t',line)[:4]
            deptnum = deptname2deptnum(dept)
            majornum = majorname2majornum(major)
            new_student = Student(str(maxNum+i),name,majornum,deptnum)
            print(new_student)
            print(str(maxNum+i),name,deptnum,majornum)
            try:
                db.session.add(new_student)
                db.session.commit()
                new_student_numbers.append(new_student.StudentNum)
                new_student_names.append(new_student.StudentName)
            except:
                db.session.rollback()
    if filetype == 'excel':
        data = xlrd.open_workbook(filepath)
        table = data.sheets()[0]
        nrows = table.nrows  # 行数
        ncols = table.ncols  # 列数
        for i in range(nrows):
            order , name , dept , major  =  table.row_values(i)[:4]
            deptnum = deptname2deptnum(dept)
            majornum = majorname2majornum(major)
            new_student = Student(str(maxNum+i),name,majornum,deptnum)
            try:
                db.session.add(new_student)
                db.session.commit()
                new_student_numbers.append(new_student.StudentNum)
                new_student_names.append(new_student.StudentName)
            except:
                db.session.rollback()
    return new_student_numbers,new_student_names
    
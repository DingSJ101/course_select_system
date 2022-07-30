from ast import Pass
from hashlib import new
import json 
import random
import sqlalchemy
from app import app
from app import db
from app.models import Student, Teacher, Manager, Course, Student_Class_table, Class, Major, Dept,Account
engine = sqlalchemy.create_engine( 'postgresql+psycopg2://gaussdb:123@QWEasd@122.9.68.170:15432/css',pool_pre_ping=True)
# engine = sqlalchemy.create_engine( 'postgresql+psycopg2://gaussdb:123@QWEasd@175.24.167.6:15432/css',pool_pre_ping=True)
print('create engine')
depts = ['马克思主义学院','文学院','外国语学院','法学院','社会学院', #1
'新闻传播学院','钱伟长学院','理学院','通信与信息工程学院','计算机工程与科学学院',#6
'机电工程与自动化学院','材料科学与工程学院','环境与化学工程学院','生命科学学院','中欧工程技术学院',#11
'微电子学院力学与工程科学学院','经济学院','管理学院','悉尼工商学院','图书情报档案系',#16
'上海美术学院','上海电影学院','音乐学院','上海温哥华电影学院','社区学院',#21
'体育学院','社会科学学部','国际交流学院','土木工程系']# 26

s3=[
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
s2="""
哲学
经济学
金融学
国际经济与贸易
法学
知识产权
社会学
社会工作
思想政治教育
汉语言文学
汉语言
汉语国际教育
英语
日语
新闻学
广播电视学
广告学
网络与新媒体
历史学
数学与应用数学
信息与计算科学
应用物理学
应用化学
理论与应用力学
机械工程
机械设计制造及其自动化
机械电子工程
工业设计
智能制造工程
测控技术与仪器
材料物理
冶金工程
金属材料工程
无机非金属材料工程
高分子材料与工程
材料设计科学与工程
电气工程及其自动化
电子信息工程
电子科学与技术
通信工程
微电子科学与工程
光电信息科学与工程
电子信息科学与技术
自动化
计算机科学与技术
数字媒体技术
智能科学与技术
网络空间安全
电影制作
土木工程
化学工程与工艺
包装工程
环境工程
生物医学工程
食品科学与工程
建筑学
城乡规划
生物工程
管理科学
信息管理与信息系统
工程管理
工商管理
会计学
财务管理
人力资源管理
档案学
信息资源管理
物流管理
工业工程
音乐表演
音乐学
表演
戏剧影视文学
广播电视编导
戏剧影视导演
戏剧影视美术设计
动画
影视摄影与制作
美术学
绘画
雕塑
中国画
视觉传达设计
环境设计
数字媒体艺术
艺术与科技
"""
s1="""
010101
020101
020301K
020401
030101K
030102T
030301
030302
030503
050101
050102
050103
050201
050207
050301
050302
050303
050306T
060101
070101
070102
070202
070302
080101
080201
080202
080204
080205
080213T
080301
080402
080404
080405
080406
080407
080415T
080601
080701
080702
080703
080704
080705
080714T
080801
080901
080906
080907T
080911TK
080913T
081001
081301
081702
082502
082601
082701
082801
082802
083001
120101
120102
120103
120201K
120203K
120204
120206
120502
120503
120601
120701
130201
130202
130301
130304
130305
130306
130307
130310
130311T
130401
130402
130403
130406T
130502
130503
130508
130509T
"""
firstName = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻水云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐费岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅卞齐康伍余元卜顾孟平" \
            "黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计成戴宋茅庞熊纪舒屈项祝董粱杜阮席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田胡凌霍万柯卢莫房缪干解应宗丁宣邓郁单杭洪包诸左石崔吉" \
            "龚程邢滑裴陆荣翁荀羊甄家封芮储靳邴松井富乌焦巴弓牧隗山谷车侯伊宁仇祖武符刘景詹束龙叶幸司韶黎乔苍双闻莘劳逄姬冉宰桂牛寿通边燕冀尚农温庄晏瞿茹习鱼容向古戈终居衡步都耿满弘国文东殴沃曾关红游盖益桓公晋楚闫"
# 女孩名字
girl = '秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣飘育滢馥筠柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝思丽'
# 男孩名字
boy = '伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘'
# 名
midname = '中笑贝凯歌易仁器义礼智信友上都卡被好无九加电金马钰玉忠孝'
types = ['0','1','2']
def createStudent(count):
    majors = Major.query.all()
    for i in range(19000000,19000000+count):
        account=str(i)
        psw = account
        
        type = '0'
        firstName_name =firstName[random.choice(range(len(firstName)))]
        sex = random.choice(range(2))
        
        name_1 =''
        if(sex == 1):
            boy_name = boy[random.choice(range(len(boy)))]
            if random.choice(range(2)) > 0:
                name_1 = midname[random.choice(range(len(midname)))]
            name =  firstName_name + name_1 + boy_name
        else:
            girl_name = girl[random.choice(range(len(girl)))]
            if random.choice(range(2)) > 0:
                name_1 = midname[random.choice(range(len(midname)))]
            name =  firstName_name + name_1 + girl_name 
        # print(account,name)
        major = random.choice(majors)
        new_account = Account(account,'0',account)
        new_student = Student(account,name,major.MajorNum,major.DeptNum)
        try:
            db.session.add(new_account)
            db.session.commit()
        except:
            db.session.rollback()
        try:
            db.session.add(new_student)
            db.session.commit()
        except:
            db.session.rollback()

def createCourse(count):
    sql = """select distinct classinfo.cid,classinfo.ttid,classinfo.capacity,pairs.cname,pairs.credit from classinfo join pairs on classinfo.cid=pairs.cid and classinfo.ttid = pairs.ttid"""
    sql = """
        select t.cid,cname,credit,capacity from (
        select cid,max(capacity) capacity from classinfo group by cid ) t 
        join 
        ( select distinct cid,cname ,credit from pairs  ) s 
        on t.cid=s.cid
    """
    results = engine.execute(sql).fetchall()
    for result in results[:count]:
        cid,cname,credit,capacity = result[:]
        new_course =Course(cid,cname,credit,capacity)
        db.session.add(new_course)
        db.session.commit()

def createTeacher(count=9999):
    result = engine.execute("select distinct pairs.tname from pairs").fetchall()
    names=[]
    for item in result:
        line = item[0]
        if(len(line)>1 and len(line)<10 and line[-1]!='等'):
            names.append(line)
    cnt = 10000000
    for name in set(names):
        result = engine.execute("""select t.title from 
( select distinct tname,teacher_title title from classinfo join pairs on classinfo.cid=pairs.cid and classinfo.ttid=pairs.ttid ) t
where t.tname = '%s'"""%(name)).fetchone()[0]
        sql = """insert into teacher values('%s','%s','tt','9999')"""%(str(cnt),name,)
        new_teacher = Teacher(str(cnt),name,result)
        new_account = Account(str(cnt),'1',str(cnt))
        db.session.add(new_account)
        db.session.add(new_teacher)
        db.session.commit()
        cnt=cnt+1
        if(cnt>10000000+count):break


def createClass(count=9999):
    courses = Course.query.all()
    for course in courses:
        pass
    sql = """ select classinfo.cid,classinfo.ttid,pairs.tname,time,venue from classinfo join pairs on classinfo.cid=pairs.cid and classinfo.ttid=pairs.ttid """
    results = engine.execute(sql).fetchall()
    cnt=0
    for result in results:
        courseNum,classNum,teacherName,time,venue = result[:]
        teacherNum = Teacher.query.filter_by(TeacherName=teacherName).first()
        if teacherNum is None:
            continue
        new_class = Class(str(courseNum)+'_'+str(classNum),courseNum,teacherNum.TeacherNum,time,venue)
        
        try:
            db.session.add(new_class)
            db.session.commit()
            cnt=cnt+1
        except:
            db.session.rollback()
            # print(result)
        if(cnt>=count):break


def createStudent_Class(count_student=-1,count_class=10):
    classes = Class.query.all()
    students = Student.query.all()
    cnt_student=0
    for i,student in enumerate(students):
        course_selected = []
        for cla in random.sample(classes,count_class):
            if cla.ClassNum[:8] in course_selected or cla.MaxCapacity<=cla.ClassCapacity:
                continue
            new_record = Student_Class_table(student.StudentNum,cla.ClassNum)
            course_selected.append(cla.ClassNum[:8])
            try:
                db.session.add(new_record)
                db.session.commit()
                cnt_class=cnt_class+1
            except:
                db.session.rollback()
        if(i>=count_student):break
        

def createDept():
    # insert into dept
    for i,dept in enumerate(depts):
        idx = str(i)
        id = '0'*(4-len(idx))+idx
        sql = """insert into dept values ('%s','%s');"""%(id,dept)
        engine.execute(sql)
    engine.execute("insert into dept values('9999','未知');")

def createMajor():
    #insert into major
    for a,b,c in zip(s1.split('\n')[1:],s2.split('\n')[1:],s3):
        d = '0'*(4-len(str(c-1)))+str(c-1)
        sql = """insert into major values ('%s','%s','%s');"""%(a,b,d)
        engine.execute(sql)

def createManager():
    new_teacher = Manager('1000','1000')
    new_account = Account('1000','2','1000')
    db.session.add(new_account)
    db.session.add(new_teacher)
    db.session.commit()

def add_trigger():
    add_trigger  = """
        create or replace function sync_MaxCapacity() returns trigger as $$
        BEGIN
            update class set class."MaxCapacity" = 
                (select CourseCapacity from course 
                    where CourseNum = left(new.ClassNum,8) limit 1 ) 
                where class."ClassNum"=new."ClassNum";
        return new;
        END 
        $$ LANGUAGE PLPGSQL;
    """
    set_trigger = """
        create trigger sync_class_max_capacity  after insert on class 
        for each row execute PROCEDURE public.sync_MaxCapacity();
    """
    try:
        engine.execute(add_trigger)
    except:
        print("error when add trigger")
    try:
        engine.execute(set_trigger)
    except:
        print("error when set trigger")
# sql  = 'select *  from class' 
# tmp = 'select * distinct cid,distinct cname from '
# result = engine.execute(sql)
# print('execute sql')
# print(result.fetchone())

if __name__ == "__main__":
    # createDept()
    # createMajor()
    # createStudent(100)
    # createCourse(100)
    # createTeacher()
    # createManager()
    # add_trigger()
    createClass(100)
    createStudent_Class(100)
    pass
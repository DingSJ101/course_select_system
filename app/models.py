from lib2to3.pgen2.token import NUMBER
from mimetypes import init
from sqlalchemy import ForeignKey,and_, null
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from app import login


@login.user_loader
def load_user(Num):
    account = Account.query.filter_by(User_id=Num).first()
    user_type = account.User_type
    if user_type == '0' : #学生
        user = Student.query.get(int(Num))
    elif user_type == '1' : #教师
        user = Teacher.query.get(int(Num))
    elif user_type == '2' : #管理员
        user = Manager.query.get(int(Num))
    return user


class Account(db.Model):
    User_id = db.Column(db.String(8), primary_key=True)
    User_type = db.Column(db.String(4))
    Passwd = db.Column(db.Text, nullable=False)

    def set_password(self, password):
        self.Passwd = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Passwd, password)
    
    def __init__(self,account,type,passwd = '123456'):
        self.User_id=account
        self.User_type = type
        self.set_password(passwd)

class Dept(db.Model):
    # 学院
    DeptNum = db.Column(db.String(4), primary_key=True)
    DeptName = db.Column(db.String(20), nullable=False)
    Teachers = db.relationship('Teacher', backref='dept', lazy='dynamic')
    Majors = db.relationship('Major', backref='dept', lazy='dynamic')
    Students = db.relationship('Student',backref = 'dept',lazy='dynamic')

class Major(db.Model):
    # 专业
    MajorNum = db.Column(db.String(10), primary_key=True)
    MajorName = db.Column(db.String(15), nullable=False)
    DeptNum = db.Column(db.String(4), db.ForeignKey('dept.DeptNum'), nullable=False)
    Students = db.relationship('Student', backref='major', lazy='dynamic')

class Student_Class_table(db.Model):
    __tablename__ = "student_class_table"
    StudentNum = db.Column(db.String(8), db.ForeignKey('student.StudentNum'), primary_key=True, nullable=False)
    ClassNum = db.Column(db.String(16), db.ForeignKey('class.ClassNum'), primary_key=True, nullable=False)
    Grade = db.Column(db.Integer)
    # CourseNum = db.Column(db.String(8), db.ForeignKey('course.CourseNum'), nullable=True, primary_key=True)
    def __init__(self, StudentNum,ClassNum):
        self.StudentNum = StudentNum
        self.ClassNum = ClassNum
        self.Grade = null()
    # def __init__(self, StudentNum,CourseNum,ClassNum):
    #     self.StudentNum = StudentNum
    #     self.ClassNum = CourseNum+'-'+ClassNum

    def input_grade(self, grade=None):
        self.Grade = grade

    def get_course(self):
        return self.ClassNum.split('_')[0]
    
    def get_class(self):
        return self.ClassNum.split('_')[-1]

class Teacher(UserMixin, db.Model):
    # 教师
    TeacherNum = db.Column(db.String(8), primary_key=True)
    TeacherName = db.Column(db.String(10), nullable=False)
    TeacherTitle = db.Column(db.String(10))
    DeptNum = db.Column(db.String(4), db.ForeignKey('dept.DeptNum'), nullable=False)
    Classes = db.relationship('Class', backref='teacher', lazy='dynamic')
    
    
    def __init__(self, TeacherNum,TeacherName, TeacherTitle, DeptNum='9999'):
        self.TeacherNum = TeacherNum
        self.DeptNum = DeptNum
        self.TeacherName = TeacherName
        self.TeacherTitle = TeacherTitle
        try:
            new_account = Account(TeacherNum, '1', TeacherNum)
            db.session.add(new_account)
            db.session.commit()
        except:
            db.session.rollback()
            Account.query.filter_by(User_id=TeacherNum).first().set_password(TeacherNum)
    # override
    def get_id(self):
        return self.TeacherNum

class Student(UserMixin, db.Model):
    # 学生
    StudentNum = db.Column(db.String(8), primary_key=True)
    StudentName = db.Column(db.String(10), nullable=False)
    MajorNum = db.Column(db.String(10), db.ForeignKey('major.MajorNum'), nullable=False)
    DeptNum = db.Column(db.String(4), db.ForeignKey('dept.DeptNum'), nullable=False)
    Classes = db.relationship('Class', secondary='student_class_table', backref='students', lazy='dynamic')
    # dept
    # major
    def __init__(self, StudentNum,StudentName, MajorNum='000000', DeptNum='9999'):
        self.StudentNum = StudentNum
        self.StudentName = StudentName
        self.MajorNum = MajorNum
        self.DeptNum = DeptNum
        try:
            new_account = Account(StudentNum, '0', StudentNum)
            db.session.add(new_account)
            db.session.commit()
        except:
            db.session.rollback()
            Account.query.filter_by(User_id=StudentNum).first().set_password(StudentNum)

    # override
    def get_id(self):
        return self.StudentNum

    def drop_course(self, classNum):
        record = Student_Class_table.query.filter(Student_Class_table.StudentNum==self.StudentNum,Student_Class_table.ClassNum==classNum).first()
        # print(record.all())
        # print('-'*20)
        # record.delete()
        db.session.delete(record)


class Course(db.Model):
    # 课程
    CourseNum = db.Column(db.String(8), primary_key=True)
    CourseName = db.Column(db.String(50), nullable=False)
    CourseCredit = db.Column(db.String(10))
    CourseCapacity = db.Column(db.Integer)
    Classes = db.relationship('Class', backref='course', lazy='dynamic')
    
    def __init__(self, CourseNum, CourseName, CourseCredit=0,CourseCapacity=0):
        self.CourseNum = CourseNum
        self.CourseName = CourseName
        self.CourseCredit = CourseCredit
        self.CourseCapacity = CourseCapacity

class Class(db.Model):
    ClassNum = db.Column(db.String(16), primary_key=True) #CourseNum_classnum
    ClassTime = db.Column(db.Text)
    ClassVenue = db.Column(db.Text)
    ClassCapacity = db.Column(db.Integer)
    MaxCapacity = db.Column(db.Integer)
    CourseNum = db.Column(db.String(8), db.ForeignKey('course.CourseNum'), nullable=True)
    TeacherNum = db.Column(db.String(8), db.ForeignKey('teacher.TeacherNum'), nullable=True)
    IsLock = db.Column(db.Boolean)
    # course
    # students
    # teacher
    def __init__(self, ClassNum ,CourseNum,TeacherNum,ClassTime='',ClassVenue='',IsLock=null()):
        self.ClassNum = ClassNum
        self.ClassTime = ClassTime
        self.ClassVenue = ClassVenue
        self.CourseNum = CourseNum
        self.TeacherNum = TeacherNum
        self.IsLock = IsLock
        self.ClassCapacity=0
        self.MaxCapacity = 0 # 使用触发器实现
    def change_max_capacity(self,number=1):
        self.MaxCapacity += int(number)
        db.session.commit()

class Manager(UserMixin, db.Model):
    # 管理员
    ManagerNum = db.Column(db.String(8), primary_key=True)
    ManagerName = db.Column(db.String(10), nullable=False)

    # override
    def get_id(self):
        return self.ManagerNum

    def __init__(self,Num,Name='admin'):
        self.ManagerNum=Num
        self.ManagerName = Name

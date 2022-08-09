from app.func import *
## classtime_judge test --------------
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
## -------------------------------------


## load_student_from_file test --------------
filepath = 'upload/1.xlsx'
# filepath = 'upload/test.txt'
print(majorname2majornum('计算机科学与技术'))
print(deptname2deptnum('计算机工程与科学学院'))
print(load_student_from_file(filepath))
## -------------------------------------



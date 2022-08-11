from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Student, Teacher, Manager, Course, Student_Class_table, Class, Major, Dept, Account
from app.forms import EditProfileForm
from app import db
from flask_sqlalchemy import  SQLAlchemy
from sqlalchemy import and_, or_, null
from app import func



import os

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/major_info', methods=['GET', ])
@login_required
def major_info():
    return render_template('student/major_info.html')


@app.route('/dept_info', methods=['GET', ])
@login_required
def dept_info():
    return render_template('student/dept_info.html')


@app.route('/voluntary_selection')
@login_required
def voluntary_selection():
    return render_template('student/voluntary_selection.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        if isinstance(current_user._get_current_object(), Student):
            return redirect(url_for('student_index'))
        elif isinstance(current_user._get_current_object(), Teacher):
            return redirect(url_for('teacher_index'))
        elif isinstance(current_user._get_current_object(), Manager):
            return redirect(url_for('manager'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')
        remember = [True if remember == 'on' else False][0]
        error = None
        account = Account.query.filter_by(User_id=username).first()
        if not account:
            error = '用户不存在！'
        elif not account.check_password(password):
            error = '密码错误！'
        else:
            user_type = account.User_type
            print(user_type)
            if user_type == '0':  # 学生
                user = Student.query.filter_by(StudentNum=username).first()
            elif user_type == '1':  # 教师
                user = Teacher.query.filter_by(TeacherNum=username).first()
            elif user_type == '2':  # 管理员
                user = Manager.query.filter_by(ManagerNum=username).first()

        if error is None:
            login_user(user, remember=remember)
            if isinstance(user, Student):
                return redirect(url_for('student_index'))
            elif isinstance(user, Teacher):
                return redirect(url_for('teacher_index'))
            else:
                return redirect(url_for('manager'))
        flash(error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# 学生端主页
@app.route('/student_index')
@login_required
def student_index():
    if isinstance(current_user._get_current_object(), Student):
        return render_template('student/student.html')
    else:
        logout_user()

# 教师端主页
@app.route('/teacher_index')
@login_required
def teacher_index():
    if isinstance(current_user._get_current_object(), Teacher):
        return render_template('teacher/teacher.html')
    else:
        logout_user()

# 管理端主页
@app.route('/manager')
@login_required
def manager():
    if isinstance(current_user._get_current_object(), Manager):
        return render_template('admin/manager.html')
    else:
        logout_user()
        return redirect(url_for('login'))

# 学生端-修改密码
# - GET : 返回页面
# - POST : 接受表单，修改密码，重定向返回页面
#     old_password 
#     new_password 
#     new_password2 
# return :  student/student_info.html 
@app.route('/student_info/<int:change>', methods=['GET', 'POST'])
@app.route('/student_info', defaults={'change': 0}, methods=['GET', 'POST'])
@login_required
def student_info(change):
    if request.method == 'POST':
        old_password = request.form['oldpassword']
        new_password = request.form['newpassword']
        new_password2 = request.form['newpassword2']
        user_id = current_user.StudentNum
        account = Account.query.filter_by(User_id=user_id).first()
        if not new_password == new_password2:
            flash('两次密码输入不一致！')
        elif not account.check_password(old_password):
            flash('原密码输入错误！')
        else:
            account.set_password(new_password)
            db.session.commit()
            flash('Your changes have been saved.')
        return redirect(url_for('student_info'))
    return render_template('student/student_info.html', change=change)

# 教师端-修改密码
# - GET : 返回页面
# - POST : 接受表单，修改密码，重定向返回页面
    # old_password 
    # new_password 
    # new_password2 
# return :  teacher/teacher_info.html
@app.route('/teacher_info/<int:change>', methods=['GET', 'POST'])
@app.route('/teacher_info', defaults={'change': 0}, methods=['GET', 'POST'])
@login_required
def teacher_info(change):
    if request.method == 'POST':
        old_password = request.form['oldpassword']
        new_password = request.form['newpassword']
        new_password2 = request.form['newpassword2']
        user_id = current_user.TeacherNum
        account = Account.query.filter_by(User_id=user_id).first()
        if not new_password == new_password2:
            flash('两次密码输入不一致！')
        elif not account.check_password(old_password):
            flash('原密码输入错误！')
        else:
            account.set_password(new_password)
            db.session.commit()
            flash('Your changes have been saved.')
        return redirect(url_for('teacher_info'))
    return render_template('teacher/teacher_info.html', change=change)

# 学生端-查看已选课程
# - GET : 返回页面
# return :  student/course_select_table.html
    # - tables
    #     'CourseNum': _course.CourseNum,
    #     'CourseName': _course.CourseName,
    #     'ClassNum': cla.ClassNum.split('_')[1],
    #     'CourseCredit': _course.CourseCredit,
    #     'ClassTime': cla.ClassTime,
    #     'ClassVenue': cla.ClassVenue,
    #     'TeacherName': cla.teacher.TeacherName
@app.route('/course_select_table', methods=['GET', ])
@login_required
def course_select_table():
    if isinstance(current_user._get_current_object(), Student):
        Classes = current_user.Classes
        tables = []
        for cla in Classes:
            _course = cla.course
            table = {
                'CourseNum': _course.CourseNum,
                'CourseName': _course.CourseName,
                'ClassNum': cla.ClassNum.split('_')[1],
                'CourseCredit': _course.CourseCredit,
                'ClassTime': cla.ClassTime,
                'ClassVenue': cla.ClassVenue,
                'TeacherName': cla.teacher.TeacherName
            }
            tables.append(table)
        return render_template('student/course_select_table.html', tables=tables)


# 学生端-查看具体课程信息
# - GET : 返回页面
# return :  student/course_teachers.html
    # - tables
    #     'classNum': cla.ClassNum.split('_')[1],
    #     'ClassNum': cla.ClassNum,
    #     'CourseNum': cla.CourseNum,
    #     'TeacherNum': cla.TeacherNum,
    #     'CourseName': course.CourseName,
    #     'TeacherName': cla.teacher.TeacherName,
    #     'Time': cla.ClassTime,
    #     'CourseCapacity': cla.MaxCapacity,
    #     'CourseStudents': cla.ClassCapacity,
@app.route('/course_teachers/<CourseNum>', methods=['GET', ])
@login_required
def course_teachers(CourseNum:'00864122_3001'):
    if isinstance(current_user._get_current_object(), Student):
        CourseNum = CourseNum[:8]
        course = Course.query.filter_by(CourseNum=CourseNum).first()
        # course = Course.query.filter_by(CourseNum.like('%' + CourseNum + '%')).first()
        # cla = Class.query.filter(Class.ClassNum.like(CourseNum + '%')).first()
        tables = []
        for cla in course.Classes:
            table = {
                'classNum': cla.ClassNum.split('_')[1],
                'ClassNum': cla.ClassNum,
                'CourseNum': cla.CourseNum,
                'TeacherNum': cla.TeacherNum,
                'CourseName': course.CourseName,
                'TeacherName': cla.teacher.TeacherName,
                'Time': cla.ClassTime,
                'CourseCapacity': cla.MaxCapacity,
                'CourseStudents': cla.ClassCapacity,
            }
            tables.append(table)

        return render_template('student/course_teachers.html', tables=tables)

# 学生端-查看所有课程
# - GET : 重定向 /course
# - POST : 模糊查询，重定向 /course    
    # searchNum: 课程号/课程名
@app.route('/course_query', methods=['GET', 'POST'])
@login_required
def course_query():
    CourseNum = request.form['CourseNum']
    return redirect(url_for('course', searchNum=CourseNum))

# 学生端-查看所有课程
# - GET : 返回页面
# - POST : 模糊查询，返回页面
    # searchNum: 课程号/课程名
# return :  student/course.html
    # - tables
    #     'CourseNum': course.CourseNum,
    #     'CourseName': course.CourseName,
    #     'CourseCredit': course.CourseCredit,
    # - course_selected # 已选课程
    #     List: Class.CourseNum
@app.route('/course/<searchNum>', methods=['GET', ])
@app.route('/course', defaults={'searchNum': 'all'}, methods=['GET', 'POST'])
@login_required
def course(searchNum:'模糊查询字段，课程号/课程名'):
    print(searchNum)
    if isinstance(current_user._get_current_object(), Student):
        if searchNum == 'all':
            all_courses = Course.query.all()
        else:
            all_courses = Course.query.filter(or_(Course.CourseNum.like('%'+searchNum+'%'), Course.CourseName.like('%'+searchNum+'%'))).all()
        Classes = current_user.Classes
        class_selected = [Cla.CourseNum for Cla in Classes]
        tables = []
        for course in all_courses:
            table = {
                'CourseNum': course.CourseNum,
                'CourseName': course.CourseName,
                'CourseCredit': course.CourseCredit,
                # 'CourseTime':course.Classes[course].ClassTime
            }
            tables.append(table)
        return render_template('student/course.html', tables=tables, course_selected=class_selected)


# 学生端-退课
# - GET : 退课，重定向 /course_select_table
@app.route('/course_drop/<CourseNum>', methods=['GET', ])
@login_required
def course_drop(CourseNum:'00864122_3001'):
    if isinstance(current_user._get_current_object(), Student):
        Classes = current_user.Classes
        tmpMap = {}
        for cla in Classes:
            tmpMap[cla.ClassNum.split('_')[0]] = cla.ClassNum
        class_selected = [cla.ClassNum.split('_')[0] for cla in Classes]
        if CourseNum not in class_selected:
            flash('您未选择该门课程！')
        else:
            CourseNum = tmpMap[CourseNum]
            current_user.drop_course(CourseNum)
            db.session.commit()
            flash('您已成功退选该门课程。')
        return redirect(url_for('course_select_table'))

# 学生端-选课
# - GET : 选课，重定向 /course_select_table
@app.route('/course_select/<ClassNum>', methods=['GET', ])
@login_required
def course_select(ClassNum:'00864122_3001'):
    if isinstance(current_user._get_current_object(), Student):
        flag = 0
        classes = current_user.Classes
        for cla in classes:
            if ClassNum.split('_')[0] == cla.ClassNum.split('_')[0]:
                flash('错误：您已选课程中存在该门课程！')
                flag = 1
                break
        cla = Class.query.filter_by(ClassNum = ClassNum).first()
        if flag == 0:
            _ = func.classtime_judge(cla.ClassTime,classes)
            if _ :
                flash('所选课程%s与已选课程%s存在时间冲突'%(cla.ClassNum,_.ClassNum))
            else:
                new_record = Student_Class_table(current_user.StudentNum, ClassNum)
                db.session.add(new_record)
                db.session.commit()
                flash('您已成功选择该门课程。')
        return redirect(url_for('course_select_table'))


# 学生端-重选课程
# - GET : 退选当前课程，重定向 /course_teachers
    # CourseNum : '00864122' # 当前课程的课程号
@app.route('/course_change/<CourseNum>', methods=['GET', ])
@login_required
def course_change(CourseNum:'00864122_3001'):
    if isinstance(current_user._get_current_object(), Student):
        cla = Student_Class_table.query.filter(and_(Student_Class_table.ClassNum.like(CourseNum+'_%'),Student_Class_table.StudentNum==current_user._get_current_object().StudentNum)).first()
        current_user.drop_course(cla.ClassNum)
        db.session.commit()
        return redirect(url_for('course_teachers', CourseNum=cla.ClassNum))


# 学生端-查看成绩
# - GET : 返回页面
# return student/grade_query.html
    # - tables 
    #     - List: table
    #         'CourseNum': course.CourseNum,
    #         'ClassNum': cla.ClassNum.split('_')[1],
    #         'CourseName': course.CourseName,
    #         'CourseCredit': course.CourseCredit,
    #         'CourseTime': cla.ClassTime,
    #         'CourseDept': teacher.dept.DeptName,
    #         'TeacherName': teacher.TeacherName,
    #         'Grade': grade,
@app.route('/grade_query', methods=['GET', ])
@login_required
def grade_query():
    if isinstance(current_user._get_current_object(), Student):
        classes = current_user.Classes
        tables = []
        for cla in classes:
            teacher = cla.teacher
            course = cla.course
            grade = Student_Class_table.query.filter_by(StudentNum=current_user.StudentNum,
                                                        ClassNum=cla.ClassNum).first().Grade
            table = {
                'CourseNum': course.CourseNum,
                'ClassNum': cla.ClassNum.split('_')[1],
                'CourseName': course.CourseName,
                'CourseCredit': course.CourseCredit,
                'CourseTime': cla.ClassTime,
                'CourseDept': teacher.dept.DeptName,
                'TeacherName': teacher.TeacherName,
                'Grade': grade,
            }
            tables.append(table)
        return render_template('student/grade_query.html', tables=tables)


# 教师端-开课详情
# - GET : 返回页面
# return :  teacher/course_select_detail.html
    # - course_tables
    #     List : [course_info , tables ]
    #         - course_info
    #             'ClassNum': cla.ClassNum.split('_')[1],
    #             'CourseNum': course.CourseNum,
    #             'CourseName': course.CourseName,
    #             'CourseStudents': cla.ClassCapacity,
    #             'CourseCapacity': cla.MaxCapacity,
    #             'CourseCredit': course.CourseCredit,
    #             'ClassVenue': cla.ClassVenue,
    #             'ClassTime': cla.ClassTime
    #         - tables
    #             List: table
    #                 'StudentNum': student.StudentNum,
    #                 'StudentName': student.StudentName,
    #                 'DeptName': student.major.dept.DeptName,
    #                 'MajorName': student.major.MajorName,
@app.route('/course_select_detail')
@login_required
def course_select_detail():
    if isinstance(current_user._get_current_object(), Teacher):
        classes = current_user.Classes
        course_tables = []
        for cla in classes:
            course_select_tables = Student_Class_table.query.filter_by(ClassNum=cla.ClassNum).all()
            course = cla.course
            course_info = {
                'ClassNum': cla.ClassNum.split('_')[1],
                'CourseNum': course.CourseNum,
                'CourseName': course.CourseName,
                'CourseStudents': cla.ClassCapacity,
                'CourseCapacity': cla.MaxCapacity,
                'CourseCredit': course.CourseCredit,
                'ClassVenue': cla.ClassVenue,
                'ClassTime': cla.ClassTime
            }
            tables = []
            for student in cla.students:
                table = {
                    'StudentNum': student.StudentNum,
                    'StudentName': student.StudentName,
                    'DeptName': student.major.dept.DeptName,
                    'MajorName': student.major.MajorName,
                }
                tables.append(table)
            course_tables.append([course_info, tables])
        return render_template('teacher/course_select_detail.html', course_tables=course_tables)


## CourseNum like 'CourseNum_ClassNum'('00864122_3001')
# 教师端-更新成绩
# - GET : 返回页面
# - POST : 修改成绩，重定向 /course_grade_input
# return :  teacher/course_grade_input.html
    # - course_tables
    #     List : [course_info , tables , flag]
    #         - course_info
    #             'CourseNum': course.CourseNum,
    #             'CourseName': course.CourseName,
    #             'CourseStudents': cla.ClassCapacity,
    #             'ClassNum': cla.ClassNum,
    #             'ClassNum1': cla.ClassNum.split('_')[1],
    #             'IsLock': cla.IsLock
    #         - tables
    #             List: table
    #                 'StudentNum': student.StudentNum,
    #                 'StudentName': student.StudentName,
    #                 'DeptName': student.dept.DeptName,
    #                 'MajorName': student.major.MajorName,
    #                 'Grade': record.Grade
    #         - flag # 是否全部录入
@app.route('/course_grade_input/<CourseNum>', methods=['GET', 'POST'])
@app.route('/course_grade_input', defaults={'CourseNum': 0})
@login_required
def course_grade_input(CourseNum:'00864122_3001'):
    # CourseNum = CourseNum[:8]
    if isinstance(current_user._get_current_object(), Teacher):
        if request.method == 'POST':
            course_select_tables = Student_Class_table.query.filter_by(ClassNum=CourseNum).all()
            for course_select_table in course_select_tables:
                if not course_select_table.Grade:
                    grade = request.form[course_select_table.StudentNum]
                    course_select_table.input_grade(grade)
            db.session.commit()
            flash('成绩录入成功！')
            return redirect(url_for('course_grade_input'))
        else:
            classes = current_user.Classes
            course_tables = []
            for cla in classes:
                flag = 0
                course = cla.course
                course_select_tables = Student_Class_table.query.filter_by(ClassNum=cla.ClassNum).all()
                course_info = {
                    'CourseNum': course.CourseNum,
                    'CourseName': course.CourseName,
                    'CourseStudents': cla.ClassCapacity,
                    'ClassNum': cla.ClassNum,
                    'ClassNum1': cla.ClassNum.split('_')[1],
                    'IsLock': cla.IsLock
                }
                tables = []
                for record in course_select_tables:
                    student = Student.query.filter_by(StudentNum=record.StudentNum).first()
                    table = {
                        'StudentNum': student.StudentNum,
                        'StudentName': student.StudentName,
                        'DeptName': student.dept.DeptName,
                        'MajorName': student.major.MajorName,
                        'Grade': record.Grade
                    }
                    if not table['Grade']:
                        flag = 1
                    tables.append(table)
                course_tables.append([course_info, tables, flag])
        return render_template('teacher/course_grade_input.html', course_tables=course_tables)


# 教师端-锁定成绩
# - GET : 重定向 /course_grade_input
@app.route('/set_lock/<CourseNum>')
def set_lock(CourseNum:'00864122_3001'):
    if isinstance(current_user._get_current_object(), Teacher):
        currentClass = Class.query.filter_by(ClassNum=CourseNum).first()
        currentClass.IsLock = True # 锁定成绩
        db.session.commit()
        return redirect(url_for('course_grade_input'))


# 管理端-查看所有教师
# - GET : 返回页面
# return admin/teacher_manage.html
    # - info 
    #     List: Dept.DeptName 
    # - teachers
    #     List: Teacher.query.all()
@app.route('/teacher_manage', methods=['GET',])
@login_required
def teacher_manage():
    if isinstance(current_user._get_current_object(), Manager):
        info = {
            'depts': [dept.DeptName for dept in Dept.query.all()]
        }
        teachers = Teacher.query.order_by(Teacher.DeptNum).all()
        return render_template('admin/teacher_manage.html', info=info, teachers=teachers)


# 管理端-查看所有学生
# - POST : 重定向 /student_manage
    # searchNum: 课程号/课程名
@app.route('/student_query', methods=['POST'])
@login_required
def student_query():
    StudentNum = request.form['StudentNum']
    return redirect(url_for('student_manage', searchNum=StudentNum))

# 管理端-查看所有学生
# - GET : 返回页面
# - POST : 模糊查询，返回页面
    # searchNum: 课程号/课程名
# return admin/student_manage.html
#     - students
#         List: table 
#             'DeptName': student.major.dept.DeptName,
#             'MajorName': student.major.MajorName,
#             'StudentNum': student.StudentNum,
#             'StudentName': student.StudentName,
#     - info 
#         - majors
#             List: Major.MajorName
#         - dept 
#             List: Dept.DeptName
@app.route('/student_manage/<searchNum>', methods=['GET', ])
@app.route('/student_manage', defaults={'searchNum': 'all'}, methods=['GET', 'POST'])
@login_required
def student_manage(searchNum):
    if isinstance(current_user._get_current_object(), Manager):
        info = {
            'majors': [major.MajorName for major in Major.query.all()],
            'dept': [dept.DeptName for dept in Dept.query.all()]
        }
        if searchNum == 'all':
            all_students = Student.query.all()
        else:
            all_students = Student.query.filter(or_(Student.StudentNum.like('%'+searchNum+'%'), Student.StudentName.like('%'+searchNum+'%'))).all()
        tables = []
        for student in all_students:
            table = {
                'DeptName': student.major.dept.DeptName,
                'MajorName': student.major.MajorName,
                'StudentNum': student.StudentNum,
                'StudentName': student.StudentName,
            }
            tables.append(table)
        return render_template('admin/student_manage.html', students=tables, info=info)

# 管理端-查看课程开课情况，手动签退课
# - GET : 返回页面
# return admin/course_select_manage.html
    # - tables
    #     'ClassNum': cla.ClassNum.split('_')[1],
    #     'CourseNum': course.CourseNum,
    #     'CourseName': course.CourseName,
    #     'TeacherNum': teacher.TeacherNum,
    #     'TeacherName': teacher.TeacherName,
    #     'CourseCapacity': cla.MaxCapacity,
    #     'CourseStudents': cla.ClassCapacity,
@app.route('/course_select_manage', methods=['GET', ])
@login_required
def course_select_manage():
    if isinstance(current_user._get_current_object(), Manager):
        classes = Class.query.order_by(Class.ClassNum).all()
        tables = []
        for cla in classes:
            course = cla.course
            teacher = cla.teacher
            table = {
                'ClassNum': cla.ClassNum.split('_')[1],
                'CourseNum': course.CourseNum,
                'CourseName': course.CourseName,
                'TeacherNum': teacher.TeacherNum,
                'TeacherName': teacher.TeacherName,
                'CourseCapacity': cla.MaxCapacity,
                'CourseStudents': cla.ClassCapacity,
            }
            tables.append(table)
    return render_template('admin/course_select_manage.html', tables=tables)


# 管理端-查看课程开课情况
# - GET : 返回页面
# - POST : 精准查询，返回页面
    # CourseNum: '00864122'
    # Class: '1000'
# return admin/course_select_search.html
    # - tables
    #     List: table
    #         'ClassNum': cla.ClassNum.split('_')[1],
    #         'CourseNum': _course.CourseNum,
    #         'CourseName': _course.CourseName,
    #         'TeacherNum': cla.TeacherNum,
    #         'TeacherName': cla.teacher.TeacherName,
    #         'CourseCapacity': cla.MaxCapacity,
    #         'CourseStudents': cla.ClassCapacity,
@app.route('/course_select_search', methods=['GET', 'POST'])
@login_required
def course_select_search():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            CourseNum = request.form['CourseNum']
            Class1 = request.form['Class']
            ClassNum = CourseNum + '_' + Class1
            classes = Class.query.filter_by(ClassNum=ClassNum).all()
        else:
            classes = Class.query.order_by(Class.CourseNum).all()
        tables = []
        for cla in classes:
            _course = cla.course
            table = {
                'ClassNum': cla.ClassNum.split('_')[1],
                'CourseNum': _course.CourseNum,
                'CourseName': _course.CourseName,
                'TeacherNum': cla.TeacherNum,
                'TeacherName': cla.teacher.TeacherName,
                'CourseCapacity': cla.MaxCapacity,
                'CourseStudents': cla.ClassCapacity,
            }
            tables.append(table)
    return render_template('admin/course_select_search.html', tables=tables)


# 管理端-课程管理
# - GET : 返回页面
# return admin/course_manage.html
    # - tables
    #     List: table
    #         'CourseNum': course.CourseNum,
    #         'CourseName': course.CourseName,
    #         'ClassNum': cla.ClassNum.split('_')[1],
    #         'TeacherNum': teacher.TeacherNum,
    #         'TeacherName': teacher.TeacherName,
    #         'CourseCapacity': course.CourseCapacity,
    #         'CourseCredit': course.CourseCredit,
    # - courses
    #     List: Course.query.order_by(Course.CourseNum).all()
    # - info 
    #     List: Course.CourseName
    #     List: Teacher.TeacherName
@app.route('/course_manage', methods=['GET', ])
@login_required
def course_manage():
    if isinstance(current_user._get_current_object(), Manager):
        info = {
            'courses': [course.CourseName for course in Course.query.all()],
            'teachers': [teacher.TeacherName for teacher in Teacher.query.order_by(Teacher.TeacherName).all()],
        }
        courses = Course.query.order_by(Course.CourseNum).all()
        classes = Class.query.order_by(Class.ClassNum).all()
        tables = []
        for cla in classes:
            course = cla.course
            teacher = cla.teacher
            table = {
                'CourseNum': course.CourseNum,
                'CourseName': course.CourseName,
                'ClassNum': cla.ClassNum.split('_')[1],
                'TeacherNum': teacher.TeacherNum,
                'TeacherName': teacher.TeacherName,
                'CourseCapacity': course.CourseCapacity,
                'CourseCredit': course.CourseCredit,
            }
            tables.append(table)
    return render_template('admin/course_manage.html', info=info, courses=courses, tables=tables)


# 管理端-录入学生
# - POST: 录入学生，重定向 /student_manage
    # StudentNum 
    # MajorName
    # StudentName
    # DeptName
@app.route('/add_student', methods=['POST', ])
@login_required
def add_student():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            StudentNum = request.form['StudentNum']
            MajorName = request.form['MajorName']
            MajorNum = Major.query.filter_by(MajorName=MajorName).first().MajorNum
            StudentName = request.form['StudentName']
            DeptName = request.form['DeptName']
            DeptNum = Dept.query.filter_by(DeptName=DeptName).first().DeptNum
            if not Student.query.filter_by(StudentNum=StudentNum).first():
                student = Student(StudentNum, StudentName, MajorNum, DeptNum)
                # new_account = Account(StudentNum, '0', StudentNum)
                db.session.add(student)
                # db.session.add(new_account)
                db.session.commit()
                flash('录入学生信息成功！')
            else:
                flash('学号%s已存在！' % (StudentNum))
        return redirect(url_for('student_manage'))


# 管理端-录入教师
# - POST: 录入教师，重定向 /teacher_manage
    # TeacherNum 
    # MajorName
    # TeacherName
    # TeacherTitle
@app.route('/add_teacher', methods=['POST', ])
@login_required
def add_teacher():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            TeacherNum = request.form['TeacherNum']
            DeptName = request.form['DeptName']
            DeptNum = Dept.query.filter_by(DeptName=DeptName).first().DeptNum
            TeacherName = request.form['TeacherName']
            TeacherTitle = request.form['TeacherTitle']
            if not Teacher.query.filter_by(TeacherNum=TeacherNum).first():
                teacher = Teacher(TeacherNum, TeacherName, TeacherTitle, DeptNum)
                db.session.add(teacher)
                db.session.commit()
                flash('录入教师信息成功！')
            else:
                flash('工号%s已存在!' % (TeacherNum))
        return redirect(url_for('teacher_manage'))


# 管理端-删除学生
# - GET: 删除学生,重定向 /student_manage
@app.route('/delete_student/<StudentNum>', methods=['GET', 'POST'])
@login_required
def delete_student(StudentNum:'19000000'):
    if isinstance(current_user._get_current_object(), Manager):
        delete_stu = Student.query.filter_by(StudentNum=StudentNum).first()
        # 先删除选课表中信息
        course_tables = Student_Class_table.query.filter_by(StudentNum=StudentNum).all()
        try:
            for course_table in course_tables:
                db.session.delete(course_table)
            db.session.commit()
        except:
            db.session.rollback()
        try:
            db.session.delete(delete_stu)
            account = Account.query.filter_by(User_id=StudentNum).first()
            db.session.delete(account)
            db.session.commit()
            flash('删除学生成功！')
        except:
            flash('删除学生失败！')
        return redirect(url_for('student_manage'))


# 管理端-添加课程
# - POST : 添加课程，重定向 /course_manage
    # CourseName 
    # CourseNum 
    # CourseCredit 
    # CourseCapacity 
@app.route('/add_course', methods=['POST', ])
@login_required
def add_course():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            CourseName = request.form['CourseName']
            CourseNum = request.form['CourseNum']
            CourseCredit = request.form['CourseCredit']
            CourseCapacity = request.form['CourseCapacity']
            if not Course.query.filter_by(CourseNum=CourseNum).first():
                course = Course(CourseNum, CourseName, CourseCredit, CourseCapacity)
                db.session.add(course)
                db.session.commit()
                flash('创建课程成功！')
            else:
                flash('课程号"%s"重复，请修改课程号！' % (CourseNum))
        return redirect(url_for('course_manage'))


# Todo course_teacher换成了Class，但没有改完  to_test
# 管理端-添加课程班
# - POST : 添加课程班，重定向 /course_manage
    # ClassNum 
    # CourseNum 
    # TeacherNum 
    # ClassTime 
    # ClassVenue 
@app.route('/add_course_teacher', methods=['POST', ])
@login_required
def add_course_teacher():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            ClassNum = request.form['ClassNum']
            CourseNum = request.form['CourseNum']
            new_classnum = CourseNum + '_' + ClassNum
            TeacherNum = request.form['TeacherNum']
            ClassTime = request.form['ClassTime']
            ClassVenue = request.form['ClassVenue']
            if not Class.query.filter_by(ClassNum=new_classnum).first():
                course_teacher = Class(new_classnum, CourseNum, TeacherNum, ClassTime, ClassVenue, null())
                db.session.add(course_teacher)
                db.session.commit()
                flash('开设课程成功！')
            else:
                flash('%s老师已开设"%s"课程，请勿重复添加！' % (TeacherNum, CourseNum))
        return redirect(url_for('course_manage'))


# 管理端-删除课程
# - GET : 删除课程，重定向 /course_manage
@app.route('/course_delete/<CourseNum>')
@login_required
def course_delete(CourseNum:'00864122'):
    if isinstance(current_user._get_current_object(), Manager):
        # 先删除选课信息
        course_select_tables = Student_Class_table.query.filter(
            Student_Class_table.ClassNum.like(CourseNum + '_%')).all()
        for course_select_table in course_select_tables:
            db.session.delete(course_select_table)
        db.session.commit()
        flash('删除学生选课信息成功！')
        # 再删除课程与老师的对应表
        classes = Class.query.filter_by(CourseNum=CourseNum).all()
        for cla in classes:
            db.session.delete(cla)
        db.session.commit()
        flash('删除教师开设课程成功！')
        # 最后删除课程
        course = Course.query.filter_by(CourseNum=CourseNum).first()
        db.session.delete(course)
        db.session.commit()
        flash('删除课程成功！')
    return redirect(url_for('course_manage'))


# 管理端-删除课程班
# - GET : 删除课程班，重定向 /course_select_manage
@app.route('/course_teacher_delete/<CourseNum>/<TeacherNum>')
@login_required
def course_teacher_delete(CourseNum:'00864122', TeacherNum:''):
    if isinstance(current_user._get_current_object(), Manager):
        # 先删除选课信息
        course_select_tables = Student_Class_table.query.filter(
            Student_Class_table.ClassNum.like(CourseNum + '%')).all()
        for course_select_table in course_select_tables:
            db.session.delete(course_select_table)
        db.session.commit()
        flash('删除学生选课信息成功！')
        # 再删除课程与老师的对应表
        classes = Class.query.filter_by(CourseNum=CourseNum).all()
        for cla in classes:
            db.session.delete(cla)
        db.session.commit()
        flash('删除教师开设课程成功！')
    return redirect(url_for('course_select_manage'))


## Post parameters :
## CourseNum : 12345678
## Class : 1234
## StudentNum : 19XX1234

# 管理端-手动选课
# - POST : 手动选课，重定向 /course_select_manage
    # CourseNum 
    # Class 
    # StudentNum
@app.route('/add_course_select', methods=['POST', ])
@login_required
def add_course_select():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            CourseNum = request.form['CourseNum']
            classnum = request.form['Class']
            StudentNum = request.form['StudentNum']
            ClassNum = CourseNum + '_' + classnum
            cla = Class.query.filter_by(ClassNum=ClassNum).first()
            student = Student.query.filter_by(StudentNum = StudentNum).first()
            _ = func.classtime_judge(cla.ClassTime,student.Classes)
            if not cla:
                flash('当前教师未开设该课程')
            elif _:
                flash('所选课程%s与已选课程%s存在时间冲突' % (cla.ClassNum, _.ClassNum))
            elif not Student_Class_table.query.filter_by(StudentNum=StudentNum, ClassNum=cla.ClassNum).first():
                course_select_table = Student_Class_table(StudentNum, cla.ClassNum)
                db.session.add(course_select_table)
                db.session.commit()
                flash('手动选课成功！')
                if cla.ClassCapacity >= cla.MaxCapacity:
                    cla.change_max_capacity(cla.ClassCapacity-cla.MaxCapacity)
            else:
                flash('手动选课失败！该学生已选择该门课程！')
    return redirect(url_for('course_select_manage'))


# 管理端-手动退课
# - POST : 手动退课，重定向 /course_select_manage
    # CourseNum 
    # Class 
    # StudentNum
@app.route('/drop_course_select', methods=['POST', ])
@login_required
def drop_course_select():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            CourseNum = request.form['CourseNum']
            classnum = request.form['Class']
            StudentNum = request.form['StudentNum']
            ClassNum = CourseNum + '_' + classnum
            course_select_table = Student_Class_table.query.filter_by(StudentNum=StudentNum, ClassNum=ClassNum).first()
            if course_select_table:
                cla = Class.query.filter_by(ClassNum=ClassNum).first()
                db.session.delete(course_select_table)
                db.session.commit()
                flash('手动退课成功！')
            else:
                flash('手动退课失败！学生(%s)未选择班级(%s)' % (StudentNum, ClassNum))
    return redirect(url_for('course_select_manage'))



# 管理端-修改课程班容量
# - GET : 修改课程班容量，重定向 /course_select_manage
@app.route('/change_course_capacity/<CourseNum>/<classnum>/<add_or_sub>/<Number>', methods=['GET', ],defaults={'Number': 10})
@login_required
def change_course_capacity(CourseNum:'00864122', classnum:'1000', add_or_sub:'add/sub', Number:int):
    if isinstance(current_user._get_current_object(), Manager):
        ClassNum = CourseNum + '_' + classnum
        cla = Class.query.filter_by(ClassNum=ClassNum).first()
        if add_or_sub == 'add' and cla.MaxCapacity < 500:
            cla.change_max_capacity(Number)
            flash('课程容量扩容10人！')
        elif add_or_sub == 'sub' and cla.MaxCapacity >= cla.ClassCapacity + 10:
            cla.change_max_capacity(-1*Number)
            flash('课程容量缩容10人！')
        else:
            flash('容量扩容/缩容失败！')
        db.session.commit()
        db.session.commit()
    return redirect(url_for('course_select_manage'))

# 管理端-上传文件
# - GET : 返回页面
@app.route('/upload')
def upload_file():
    return render_template('upload.html')


# 管理端-从文件导入学生名单
# - GET : 返回页面
# - POST : 接收文件，导入名单
@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        print(request.files)
        print(f)
        print('-'*3)
        newname = secure_filename(f.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], newname)
        f.save(filepath)
        a,b = func.load_student_from_file(filepath)
        return f'file uploaded successfully <br> student number:<br>{a}<br> student name:<br>{b}'
    else:
        return render_template('upload.html')
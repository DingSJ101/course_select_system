from werkzeug.urls import url_parse

from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Student, Teacher, Manager, Course, Student_Class_table, Class, Major, Dept, Account
from app.forms import EditProfileForm
from app import db
from flask_sqlalchemy import  SQLAlchemy
from sqlalchemy import and_,or_

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


@app.route('/student_index')
@login_required
def student_index():
    if isinstance(current_user._get_current_object(), Student):
        return render_template('student/student.html')
    else:
        logout_user()


@app.route('/teacher_index')
@login_required
def teacher_index():
    if isinstance(current_user._get_current_object(), Teacher):
        return render_template('teacher/teacher.html')
    else:
        logout_user()


@app.route('/manager')
@login_required
def manager():
    if isinstance(current_user._get_current_object(), Manager):
        return render_template('admin/manager.html')
    else:
        logout_user()
        return redirect(url_for('login'))


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


## 查看已选课表
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
                'ClassNum': cla.ClassNum,
                'CourseCredit': _course.CourseCredit,
                'ClassTime': cla.ClassTime,
                'ClassVenue': cla.ClassVenue,
                'TeacherName': cla.teacher.TeacherName
            }
            tables.append(table)
        return render_template('student/course_select_table.html', tables=tables)


## CourseNum like 'CourseNum_ClassNum'('00864122_3001')
@app.route('/course_teachers/<CourseNum>', methods=['GET', ])
@login_required
def course_teachers(CourseNum):
    if isinstance(current_user._get_current_object(), Student):
        CourseNum = CourseNum[:8]
        course = Course.query.filter_by(CourseNum=CourseNum).first()
        tables = []
        for cla in course.Classes:
            table = {
                'ClassNum': cla.ClassNum,
                'CourseNum': cla.CourseNum,
                'TeacherNum': cla.TeacherNum,
                'CourseName': course.CourseName,
                'TeacherName': cla.teacher.TeacherName,
                'Time': cla.ClassTime,
                'CourseCapacity': course.CourseCapacity,
                'CourseStudents': cla.ClassCapacity,

            }
            tables.append(table)

        return render_template('student/course_teachers.html', tables=tables)


## 查看所有课程，展示所有Course，具体classes在/course_teachers
@app.route('/course', methods=['GET', ])
@login_required
def course():
    if isinstance(current_user._get_current_object(), Student):
        # all_classes = Class.query.all()
        # Classes = current_user.Classes
        # class_selected = [Cla.CourseNum for Cla in Classes]
        # tables = []
        # for cla in all_classes:
        #     _course = cla.course
        #     table = {
        #         'CourseNum': _course.CourseNum,
        #         'CourseName': _course.CourseName,
        #         'ClassNum':cla.ClassNum,
        #         'CourseCredit': _course.CourseCredit,
        #         'ClassTime': cla.ClassTime,
        #         'ClassVenue': cla.ClassVenue,
        #         'TeacherName': cla.teacher.TeacherName,
        #         'TeacherNum': cla.TeacherNum

        #     }
        #     tables.append(table)
        all_courses = Course.query.all()
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


## CourseNum like 'CourseNum_ClassNum'('00864122_3001') #question
@app.route('/course_drop/<CourseNum>', methods=['GET', ])
@login_required
def course_drop(CourseNum):
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


# Todo ---查询 404报错 ## to_test
# @app.route('/course_query/<CourseNum>/<ClassNum>', methods=['GET','POST' ])
@app.route('/course_query', methods=['GET', 'POST'])
@login_required
def course_query():
    CourseNum = request.form['CourseNum']
    # ClassNum = request.form['TeacherNum']
    if isinstance(current_user._get_current_object(), Student):
        # classes = Class.query.filter(Class.ClassNum.like(CourseNum+'%'))
        # course = Course.query.filter_by(CourseNum=CourseNum).first()
        # tables = []
        # for cla in classes:
        #     teacher= cla.teacher
        #     student_class = Student_Class_table.query.filter_by(ClassNum=cla.ClassNum).all
        #     table = {
        #         'CourseNum':course.CourseNum,
        #         'CourseName':course.CourseName,
        #         'ClassNum':cla.ClassNum,
        #         'TeacherName':teacher.TeacherName,
        #         'CourseCredit':course.CourseCredit,
        #         'ClassTime':cla.ClassTime
        #     }
        #     tables.append(table)
        # return render_template('student/course_teachers.html', tables=tables)
        course = Course.query.filter_by(CourseNum=CourseNum).first()
        if not course:
            flash('没有开设此课程号的课程')
            return redirect(url_for('course'))
        return redirect(url_for('course_teachers', CourseNum=CourseNum))


# 手动选课
@app.route('/course_select/<CourseNum>', methods=['GET', ])
@login_required
def course_select(CourseNum):
    if isinstance(current_user._get_current_object(), Student):
        flag = 0
        classes = current_user.Classes
        # print(classes[0].ClassNum)
        for cla in classes:
            if CourseNum.split('_')[0] == cla.ClassNum.split('_')[0]:
                flash('错误：您已选课程中存在该门课程！')
                flag = 1
                break
        if flag == 0:
            new_record = Student_Class_table(current_user.StudentNum, CourseNum)
            db.session.add(new_record)
            db.session.commit()
            flash('您已成功选择该门课程。')
        return redirect(url_for('course_select_table'))


# CourseNum like 'CourseNum_ClassNum'('00864122_3001')
@app.route('/course_change/<CourseNum>', methods=['GET', ])
@login_required
def course_change(CourseNum):
    if isinstance(current_user._get_current_object(), Student):
        # cla = Class.query.filter(Class.ClassNum.like(CourseNum+'_%')).first()
        cla = Student_Class_table.query.filter(and_(Student_Class_table.ClassNum.like(CourseNum+'_%'),Student_Class_table.StudentNum==current_user._get_current_object().StudentNum)).first()
        current_user.drop_course(cla.ClassNum)
        db.session.commit()
        return redirect(url_for('course_teachers', CourseNum=cla.ClassNum))


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
                'CourseName': course.CourseName,
                'CourseCredit': course.CourseCredit,
                'CourseTime': cla.ClassTime,
                'CourseDept': teacher.dept.DeptName,
                'TeacherName': teacher.TeacherName,
                'Grade': grade,
            }
            tables.append(table)
        return render_template('student/grade_query.html', tables=tables)


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
                'CourseNum': course.CourseNum,
                'CourseName': course.CourseName,
                'CourseStudents': cla.ClassCapacity,
                'CourseCapacity': course.CourseCapacity
            }
            tables = []
            for student in cla.students:
                # for course_select_table in course_select_tables:
                # student = Student.query.filter_by(StudentNum=course_select_table.StudentNum).first()
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
@app.route('/course_grade_input/<CourseNum>', methods=['GET', 'POST'])
@app.route('/course_grade_input', defaults={'CourseNum': 0})
@login_required
def course_grade_input(CourseNum):
    if isinstance(current_user._get_current_object(), Teacher):
        if request.method == 'POST':
            course_select_tables = Student_Class_table.query.filter_by(ClassNum=CourseNum).all()
            # course_select_tables = Student_Class_table.query.filter(
            #     Student_Class_table.ClassNum.like(CourseNum + '_%')).all()
            for course_select_table in course_select_tables:
                if not course_select_table.Grade:
                    try:
                        grade = request.form[course_select_table.StudentNum]
                        course_select_table.input_grade(grade)
                        db.session.commit()
                        flash('成绩录入成功！')
                    except:
                        continue
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
                    'Class':cla.ClassNum[-4:]
                }
                tables = []
                for record in course_select_tables:
                    student = Student.query.filter_by(StudentNum=record.StudentNum).first()
                    table = {
                        'StudentNum': student.StudentNum,
                        'StudentName': student.StudentName,
                        # 'StudentSex': student.StudentSex,
                        'DeptName': student.dept.DeptName,
                        'MajorName': student.major.MajorName,
                        'Grade': record.Grade
                    }
                    if not table['Grade']:
                        flag = 1
                    tables.append(table)
                course_tables.append([course_info, tables, flag])
        return render_template('teacher/course_grade_input.html', course_tables=course_tables)


## Todo 原因：可能不是很重要，还没有成功显示过 提交了的表单成绩  #to_test
@app.route('/grade_set_zero/<CourseNum>/<StudentNum>')
def grade_set_zero(CourseNum, StudentNum):
    if isinstance(current_user._get_current_object(), Teacher):
        course_select_table = Student_Class_table.query.filter(and_(Student_Class_table.ClassNum.like(CourseNum+'_%'), Student_Class_table.StudentNum == StudentNum)).first()
        course_select_table.input_grade(None)
        db.session.commit()
        return redirect(url_for('course_grade_input'))


@app.route('/student_manage', methods=['GET', 'POST'])
@login_required
def student_manage():
    if isinstance(current_user._get_current_object(), Manager):
        info = {
            'majors': [major.MajorName for major in Major.query.all()],
            'dept': [dept.DeptName for dept in Dept.query.all()]
        }
        # major_dic = {str(major.MajorNum):major.MajorName for major in Major.query.all()}
        students = Student.query.order_by(Student.MajorNum).all()
        return render_template('admin/student_manage.html', info=info, students=students)


@app.route('/teacher_manage', methods=['GET', 'POST'])
@login_required
def teacher_manage():
    if isinstance(current_user._get_current_object(), Manager):
        info = {
            'depts': [dept.DeptName for dept in Dept.query.all()]
        }
        teachers = Teacher.query.order_by(Teacher.DeptNum).all()
        return render_template('admin/teacher_manage.html', info=info, teachers=teachers)


@app.route('/course_select_manage', methods=['GET', 'POST'])
@login_required
def course_select_manage():
    if isinstance(current_user._get_current_object(), Manager):
        classes = Class.query.order_by(Class.ClassNum).all()
        tables = []
        for cla in classes:
            course = cla.course
            teacher = cla.teacher
            table = {
                'ClassNum': cla.ClassNum,
                'CourseNum': course.CourseNum,
                'CourseName': course.CourseName,
                'TeacherNum': teacher.TeacherNum,
                'TeacherName': teacher.TeacherName,
                'CourseCapacity': course.CourseCapacity,
                'CourseStudents': cla.ClassCapacity,
            }
            tables.append(table)
    return render_template('admin/course_select_manage.html', tables=tables)


# Todo --管理端的查找 查找成功，但前端需要加个跳转页面显示（可能来不及做辽）
@app.route('/course_select_search', methods=['GET', 'POST'])
@login_required
def course_select_search():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            CourseNum = request.form['CourseNum']
            TeacherNum = request.form['TeacherNum']
            classes = Class.query.filter_by(TeacherNum=TeacherNum, CourseNum=CourseNum).all()
        else:
            classes = Class.query.order_by(Class.CourseNum).all()
        tables = []
        # for cla in classes:
        # # _course = cla.course
        # #             table = {
        # #                 'CourseNum': _course.CourseNum,
        # #                 'CourseName': _course.CourseName,
        # #                 'ClassNum':cla.ClassNum,
        # #                 'CourseCredit': _course.CourseCredit,
        # #                 'ClassTime': cla.ClassTime,
        # #                 'ClassVenue': cla.ClassVenue,
        # #                 'TeacherName': cla.teacher.TeacherName,
        # #                 'TeacherNum': cla.TeacherNum
        # #
        # #             }
        for cla in classes:
            _course = cla.course
            # teacher=cla.teacher
            table = {
                'CourseNum': _course.CourseNum,
                'CourseName': _course.CourseName,
                'TeacherNum': cla.TeacherNum,
                'TeacherName': cla.teacher.TeacherName,
                'CourseCapacity': _course.CourseCapacity,
                'CourseStudents': cla.ClassCapacity,
                # 'CourseStudents': cla.ClassCapacity,

            }
            tables.append(table)
    return render_template('admin/course_select_search.html', tables=tables)


@app.route('/course_manage', methods=['GET', 'POST'])
@login_required
def course_manage():
    if isinstance(current_user._get_current_object(), Manager):
        info = {
            # 'depts': [dept.DeptName for dept in Dept.query.all()],
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
                'TeacherNum': teacher.TeacherNum,
                'TeacherName': teacher.TeacherName,
                'CourseCapacity': course.CourseCapacity,
                'CourseCredit': course.CourseCredit,
                # 'CourseStudents': cla.ClassCapacity,
            }
            tables.append(table)
    return render_template('admin/course_manage.html', info=info, courses=courses, tables=tables)


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
            # StudentSex = request.form['StudentSex']
            # StudentInyear = request.form['StudentInyear']
            if not Student.query.filter_by(StudentNum=StudentNum).first():
                student = Student(StudentNum, StudentName, MajorNum, DeptNum)
                new_account = Account(StudentNum, '0', StudentNum)
                db.session.add(student)
                db.session.add(new_account)
                db.session.commit()
                flash('录入学生信息成功！')
            else:
                flash('学号%s已存在！' % (StudentNum))
        return redirect(url_for('student_manage'))


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


@app.route('/delete_student/<StudentNum>', methods=['GET', 'POST'])
@login_required
def delete_student(StudentNum):
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
@app.route('/add_course_teacher', methods=['POST', ])
@login_required
def add_course_teacher():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            ClassNum = request.form['ClassNum']
            # ClassNum = Course.query.filter_by(CourseName=ClassName).first().ClassNum
            CourseName = request.form['CourseName']
            CourseNum = Course.query.filter_by(CourseName=CourseName).first().CourseNum
            new_classnum = CourseNum + '_' + ClassNum
            TeacherName = request.form['TeacherName']
            TeacherNum = Teacher.query.filter_by(TeacherName=TeacherName).first().TeacherNum
            # CourseCapacity = request.form['CourseCapacity']
            ClassTime = request.form['ClassTime']
            ClassVenue = request.form['ClassVenue']
            if not Class.query.filter_by(ClassNum=new_classnum).first():
                course_teacher = Class(new_classnum, CourseNum, TeacherNum, ClassTime, ClassVenue)
                db.session.add(course_teacher)
                db.session.commit()
                flash('开设课程成功！')
                # if not Course_Teacher.query.filter_by(CourseNum=CourseNum, TeacherNum=TeacherNum).first():
                #     course_teacher = Course_Teacher(CourseNum, TeacherNum, CourseCapacity)
                #     db.session.add(course_teacher)
                #     db.session.commit()
                #     flash('开设课程成功！')
            else:
                flash('%s老师已开设"%s"课程，请勿重复添加！' % (TeacherName, CourseName))
        return redirect(url_for('course_manage'))


# ClassNum ,CourseNum,TeacherNum,ClassTime='',ClassVenue='' )
@app.route('/course_delete/<CourseNum>')
@login_required
def course_delete(CourseNum):
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


# Todo extra todo--管理端删除开设课程 报错get_course没有self  # to_test
@app.route('/course_teacher_delete/<CourseNum>/<TeacherNum>')
@login_required
def course_teacher_delete(CourseNum, TeacherNum):
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


## todo   to_test
@app.route('/add_course_select', methods=['POST', ])
@login_required
def add_course_select():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            # CourseNum = request.form['CourseNum']
            # TeacherNum = request.form['TeacherNum']
            try:
                ClassNum = request.form['ClassNum']
                StudentNum = request.form['StudentNum']
                if not Student_Class_table.query.filter(and_(Student_Class_table.StudentNum==StudentNum, Student_Class_table.ClassNum.like(ClassNum[:8]+'_%'))).first():
                # if not Student_Class_table.query.filter_by(StudentNum=StudentNum, ClassNum=ClassNum).first():
                    course_select_table = Student_Class_table(StudentNum, ClassNum)
                    db.session.add(course_select_table)
                    db.session.commit()
                    flash('手动选课成功！')
                else:
                    flash('手动选课失败！该学生已选择该门课程！')
            except:
                flash('当前班级不存在')
            
            # cla = Class.query.filter_by(CourseNum=CourseNum, TeacherNum=TeacherNum).first()
            # if not cla:
                
            # elif not Student_Class_table.query.filter_by(StudentNum=StudentNum, ClassNum=cla.ClassNum).first():
            #     course_select_table = Student_Class_table(StudentNum, cla.ClassNum)
            #     db.session.add(course_select_table)
            #     db.session.commit()
            #     flash('手动选课成功！')
            # else:
                
    return redirect(url_for('course_select_manage'))


@app.route('/drop_course_select', methods=['POST', ])
@login_required
def drop_course_select():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            ClassNum = request.form['ClassNum']
            # TeacherNum = request.form['TeacherNum']
            StudentNum = request.form['StudentNum']
            course_select_table = Student_Class_table.query.filter_by(StudentNum=StudentNum, ClassNum=ClassNum).first()
            if course_select_table:
                db.session.delete(course_select_table)
                db.session.commit()
                flash('手动退课成功！')
            else:
                flash('手动退课失败！学生(%s)未选择教师(%s)的课程(%s)' % (StudentNum, ClassNum))
    return redirect(url_for('course_select_manage'))


# Todo --管理端学生选课管理扩课 报错NoneType有course # totest
@app.route('/change_course_capacity/<CourseNum>/<TeacherNum>/<add_or_sub>', methods=['GET', ])
@login_required
def change_course_capacity(CourseNum, TeacherNum, add_or_sub):
    if isinstance(current_user._get_current_object(), Manager):
        course_teacher = Class.query.filter_by(CourseNum=CourseNum, TeacherNum=TeacherNum).first()
        course = course_teacher.course
        if add_or_sub == 'add' and course.CourseCapacity < 500:
            course.CourseCapacity += 10
            flash('课程容量扩容10人！')
        elif add_or_sub == 'sub' and course.CourseCapacity > 10:
            course.CourseCapacity -= 10
            flash('课程容量缩容10人！')
        else:
            flash('容量扩容/缩容失败！')
        db.session.commit()
    return redirect(url_for('course_select_manage'))

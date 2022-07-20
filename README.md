## quick start 

```bash
git clone # this repo

## way one  build new container
docker-compose up -d 
## way two use my container
docker run -idt  --name course_select_system -v ~/workspace/course_select_system:/course_select_system -v /etc/localtime:/etc/localtime -p 8000:8000 dingsj101/course_select_system:1.2 sh /course_select_system/run.sh

## open http://127.0.0.1:8000 in browser
curl http://127.0.0.1:8000  # test deployment
```



## 一、Python_Flask的初始化（Bootstrap框架、SQLalchemy的ORM框架、数据库迁移工具）


## 二、选课系统关系模型的定义

在基础的属性定义外，还定义了各类之间的一对多关系，多对多关系，包括：

- 学院：教师 = 1:n
- 学院：专业 = 1:n
- 学院：课程 = 1:n
- 专业：学生 = 1:n
- 教师：课程 = m:n
- 学生：课程 = m:n

在教师与课程的多对多关系中，额外建立一张表，用于存储老师开设课程的具体属性：上课时间、课程容量等。

在教师、课程、学生这个三方多对多关系中，额外建立一张结联表。 


## 三、登录、登出模块

登录验证时，首先从学生表中查找输入的学号，若无，再从教师表中去查找。管理员采用单独的登录界面，用于区分。

密码验证采用flask的加盐哈希加密算法，无SQL注入风险，保证用户的信息安全。



## 四、学生界面的功能简述

1. 信息查询：学生个人信息（可修改密码）、专业信息、学院信息

2. 查询已选课程信息，更换已选课程授课教师，退课

3. 查询所有开设课程的信息

4. 查询已选课程的成绩


## 五、教师界面功能简述

1. 信息查询：教师个人信息（可修改密码）

2. 查看学生选此教师开设课程的详情，包括各个学生的个人信息，以及已选学生人数等

3. 为此教师开设课程中的学生，录入此门课程的成绩，支持录入后修改成绩的功能

## 六、管理员界面简述

1. 学生管理：
   - 录入学生：先检测学生表中是否存在学号冲突的学生，若无则插入此学生信息。
   - 删除学生：先查询出此学生所有已选课程，系统将其全部退选后，再删除此学生。

2. 教师管理：
   - 录入教师：同"录入学生"。

3. 课程管理：
   - 创建课程
   - 教师开设课程
   - 删除课程

4. 学生选课管理：
   - 手动签课
   - 手动退课
   - 修改课程容量
   - 删除此开设课程


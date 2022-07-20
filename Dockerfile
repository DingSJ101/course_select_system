FROM python:3.7

COPY requirements.txt requirements.txt

RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ numpy scikit-image imutils --trusted-host mirrors.aliyun.com -r requirements.txt 

WORKDIR /course_select_system

# docker pull python:3.7.13-alpine3.15
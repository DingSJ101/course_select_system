import os


class Config(object):
    SECRET_KEY = 'you-will-never-guess!'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/course_select_system?charset=utf8'
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://gaussdb:123@QWEasd@175.24.167.6:15432/css'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://gaussdb:123@QWEasd@122.9.68.170:15432/css'
#    SQLALCHEMY_TRACK_MODIFICATIONS = False
# 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    # 开启代码自动提交功能 [不推荐开启]
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
class DevelopmentConfig(Config):
    # 开发模式
    DEBUG = True
class ProductionConfig(Config):
    # 生产环境
    pass

config_map = {
   "develop": DevelopmentConfig,
    "product": ProductionConfig
}
# 跨域
cors = {
    "Access-Control-Allow-Origin": "*"
}


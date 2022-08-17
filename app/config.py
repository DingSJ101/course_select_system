import os


class Config(object):
    SECRET_KEY = 'you-will-never-guess!'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/course_select_system?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://gaussdb:123@QWEasd@175.24.167.6:15432/css'
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://gaussdb:123@QWEasd@122.9.68.170:15432/css'

    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_ECHO = True
    # ���������Զ��ύ���� [���Ƽ�����]
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
class DevelopmentConfig(Config):
    # ����ģʽ
    DEBUG = False
class ProductionConfig(Config):
    # ��������
    pass

config_map = {
   "develop": DevelopmentConfig,
    "product": ProductionConfig
}
# ����
cors = {
    "Access-Control-Allow-Origin": "*"
}


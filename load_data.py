import json 
import sqlalchemy
# engine = sqlalchemy.create_engine( 'postgresql+psycopg2://gaussdb:123@QWEasd@175.24.167.6:15432/css')
engine = sqlalchemy.create_engine( 'postgresql+psycopg2://gaussdb:123@QWEasd@122.9.68.170:15432/css',pool_pre_ping=True)
# sql  = 'select *  from test'
# result = engine.execute(sql)
# print(result.fetchone())
def create_table_pairs():
    engine.execute("drop table if exists pairs;")
    create_table_pairs = """CREATE TABLE "public"."pairs" ( 
        "id" serial primary key,  
        "campus" varchar(10),  
        "time" varchar(100),
        "cid" varchar(10),  
        "cname" varchar(40),  
        "credit" float4,  
        "ttid" int4,  
        "tname" varchar(40)
        );"""
    engine.execute(create_table_pairs)
    course = json.loads(open('course.txt','r').read())
    for sign in course :
        sql = f"""insert into pairs("campus","time","cid","cname","credit","ttid","tname") values{tuple(sign.values())};"""
        engine.execute(sql)

def create_table_classinfo():
    engine.execute("drop table if exists classinfo;")
    create_table_classinfo = """CREATE TABLE "public"."classinfo" ( 
        "id" serial primary key,  
        "cid" varchar(10),
        "ttid" int4,  
        "capacity" int4,  
        "teacher_title" varchar(20),
        "venue" varchar(40)
        );"""
    engine.execute(create_table_classinfo)
    
    info = json.loads(open('info.txt','r').read())
    for key in info['data'] :
        t = info['data'][key]
        # print(t.keys()) #dict_keys(['capacity', 'date', 'limitations', 'number', 'teacher_title', 'venue'])
        res = key.split('-')
        res.append(t['capacity'])
        res.append(t['teacher_title'])
        res.append(t['venue'])
        # tmp = f"""{tuple(res)}"""
        sql = f"""insert into classinfo("cid","ttid","capacity","teacher_title","venue") values{tuple(res)};"""
        engine.execute(sql)


print("start create table pairs and data...")
create_table_pairs()
print("finished...")
print("start create table classinfo and data...")
create_table_classinfo()
print("finished...")
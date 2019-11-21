def compact_add(list_source, list_target):
    list_add = []
    [list_add.append(i) for i in list_source if i not in list_target]
    return list_add

def compact_del(list_source, list_target):
    list_del = []
    [list_del.append(i) for i in list_target if i not in list_source]
    return list_del

def compact_same(list_source, list_target):
    list_same = []
    [list_same.append(i) for i in list_source if i in list_target]
    return list_same

#传入cursor,获取当前数据库中所有的表
def get_table(cursor):
    table_list=[]
    sql = "show tables"
    try:
        cursor.execute(sql) 	#执行sql语句
        results = cursor.fetchall()	#获取查询的所有记录
        for tb in results:
            table_list.append([tb][0][0])
    except Exception as e:
        raise e
    return table_list

#获取建表sql
def get_table_sql(cursor,tab):
   sql = "show create table %s " %(tab)
   try:
        cursor.execute(sql) 	#执行sql语句
        sql = cursor.fetchone()[1] + ";"
   except Exception as e:
        raise e
   return sql

#传入表名生成删除表的SQL
#传入表名删除表
# def drop_table_sql(cursor,tab):
#     sql = "drop table `" + tab + "`;"
#     try:
#         cursor.execute(sql)
#     except Exception as e:
#         raise e
#     return (sql)

#def drop_table_sql(cursor,tab):
#    for t in tab:
#        sql="drop table %s " %(t)+";"
#        cursor.execute(sql)
#        print(sql)

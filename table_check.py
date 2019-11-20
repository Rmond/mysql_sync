def compact_add(list_source, list_target):
        # 源库中存在，目标库中不存在，则需要添加
    set1 = set(list_source)
    #print(set1)
    set2 = set(list_target)
    #print(set2)
    list_add = set1.difference(set2)
    return list(list_add)

def compact_del(list_source, list_target):
    # 如果目标库中存在，而源库中不存在，则需要删除该
    set1 = set(list_source)
    set2 = set(list_target)
    list_del= set2.difference(set1)
    return list(list_del)

def compact_same(list_source, list_target):
    set1 = set(list_source)
    set2 = set(list_target)
    list_same = set1.intersection(set2)
    return list(list_same)

#传入cursor,获取当前数据库中所有的表
def get_table(cursor):
    table_list=[]
    sql = "show tables"
    try:
        cursor.execute(sql) 	#执行sql语句
        results = cursor.fetchall()	#获取查询的所有记录
        #print(results)
        for tb in range(len(results)):
            table_list.append(results[tb][0])
    except Exception as e:
        raise e
    #print(table_list)
    return (table_list)

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

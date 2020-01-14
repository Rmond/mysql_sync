from table_check import *

#传入游标，表，返回一个包含索引及列的字典
def get_key(cursor,db,tab):
    key_list = []
    sql="SELECT index_name,GROUP_CONCAT(COLUMN_NAME order by SEQ_IN_INDEX) FROM  INFORMATION_SCHEMA.STATISTICS where table_schema='%s' and table_name='%s' group by index_name;"  %(db,tab)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for key in results:
            temp_dict = {}
            temp_col = ''
            for i in key[1].split(','):
                temp_col+="`"+i+"`,"
            temp_dict["name"] = key[0]
            temp_dict["colname"] = temp_col[:-1]
            key_list.append(temp_dict)
    except Exception as e:
        raise e
    return key_list

#比较源表中有，而目标表中没有的索引，并返回索引名字；对这部分索引生成创建索引的sql
#传入源表，目标表中的{keyname,column}
def compare_key(srclist,taglist):
    key_dict = {}
    add_list = []
    del_list = []
    for tag_dict in taglist:
        if tag_dict not in srclist:
            del_list.append(tag_dict)
    key_dict['dellist'] = del_list
    for src_dict in srclist:
        if src_dict not in taglist:
            add_list.append(src_dict)
    key_dict['addlist'] = add_list
    return key_dict

#返回该索引的属性
def getkey_property(curosr,db,tab,keyname):
    property=0
    sql = "SELECT distinct non_unique FROM  INFORMATION_SCHEMA.STATISTICS where table_schema='%s' and table_name='%s' and index_name='%s';" % (db,tab,keyname)
    try:
        curosr.execute(sql) 	#执行sql语句
        for key in curosr.fetchall():	#获取查询的所有记录
            property=key[0]
    except Exception as e:
        raise e
    return property

# #检查索引是否存在
# def checkey(cursor,db,tab,keyname):
#     sql="show index from %s where key_name='%s';"  %(tab,keyname)
#     try:
#         cursor.execute(sql)
#         results = cursor.fetchall()
#     except Exception as e:
#         raise e
#     return results


#生成创建索引的SQL,传入表名，索引属性，索引名字，索引列
def getkey_sql(tab,key_property,key_dict,mode):
    key_name = key_dict['name']
    key_column = key_dict['colname']
    if mode == 'a':
        if(key_property == 0 and key_name.lower() == 'primary'): #主键
            sql = "alter table " + str(tab) + " add primary key (" + str(key_column) +");"
        elif(key_property==0 and key_name.lower()!='primary'):#唯一索引                sql = "alter table " + str(tab) + " add " + str(key_name) + "("+key_column+");"
            sql = "alter table " + str(tab) + " add unique index " + str(key_name) + "("+key_column+");"
        else:#普通索引
            sql = "alter table " + str(tab) + " add index " + str(key_name) + "(" + key_column+");"
    else:#删除索引
        if(key_name.lower() == 'primary'):
            sql = "alter table " + str(tab) + " drop primary key;"
        else:
            sql = "alter table " + str(tab) + " drop index `" + str(key_name) + "`;"
    return sql

#传入表名，获取所有的列
def col_get(cursor,db,tab):
    col_list = []
    sql = "select column_name from information_schema.columns where table_name= '%s'and table_schema='%s'" %(tab,db)
    try:
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchall()
        for col in results:
            col_list.append(col[0])
    except Exception as e:
        raise e
    return col_list

#获取修改字段的前一个字段名
def before_col_get(cursor,db,tab,column_name):
    sql = "select column_name from information_schema.columns,(select ordinal_position - 1 as ordinal  from information_schema.columns where table_name= '%s'and table_schema='%s' AND column_name = '%s') t where ordinal_position = t.ordinal and table_name= '%s'and table_schema='%s'"  %(tab,db,column_name,tab,db)
    try:
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchone()
    except Exception as e:
        raise e
    return results



#传入字段属性名，获取字段属性,注意这里返回的是一个包含字段类型，是否为空，及默认值的list
def col_type_get(cursor,db,tab,column_name):
    sql = "select COLUMN_TYPE,IS_NULLABLE,COLUMN_DEFAULT,COLUMN_COMMENT from information_schema.columns where table_name= '%s' and column_name ='%s' and table_schema = '%s'"  % (tab,column_name,db)
    try:
        cursor.execute(sql)  # 执行sql语句
        col_type_list = cursor.fetchone()
    except Exception as e:
        raise e
    return col_type_list



#传入一个字段，修改类型，生成SQL,传入表名，字段名，字段类型，列表，生成列的模式
def col_sql(tab,column_name,column_type,mode,before_col=None):
    col_type=column_type[0]
    col_isnull=column_type[1]
    col_defaul=column_type[2]
    col_comment=column_type[3]
    if before_col:
        col_front = "' AFTER `" + before_col[0] + "`;"
    else:
        col_front = "' FIRST;"
    if mode == 'c':
       if (col_isnull == 'YES' and col_defaul==None):  # 如果允许为空且无任何默认值
           sql = "alter table " + str(tab) + " modify column `" + str(column_name) + "` " + str(col_type) + " default null COMMENT '"+str(col_comment) + str(col_front)
       elif(col_isnull == 'YES' and col_defaul!=None):#允许为空且有默认值
           sql = "alter table " + str(tab) + " modify column `" + str(column_name) + "` " + str(col_type) + " default '"+ str(col_defaul) +"' COMMENT '" + str(col_comment) + str(col_front)
       elif (col_isnull != 'YES' and col_defaul==None): #不允许为空且无默认值
           sql = "alter table " + str(tab) + " modify column `" + str(column_name) + "` " + str(col_type) + " not null COMMENT '" + str(col_comment) + str(col_front)
       else:  # 如果不允许为空，且设置了默认值 col_defaul != 'None':
           sql = "alter table " + str(tab) + " modify column `" + str(column_name) + "` " + str(col_type) + " not null default '" + str(col_defaul) + "' COMMENT '" + str(col_comment) + str(col_front)
    elif mode == 'a':
        if (col_isnull =='YES' and col_defaul==None):#如果允许为空，且无默认值
            sql = "alter table " + str(tab) + " add  column `" + str(column_name) + "` " + str(col_type)+" COMMENT '"+str(col_comment) + str(col_front)
        elif (col_isnull=='YES' and col_defaul!=None): #如果允许为空,且有默认值
            sql="alter table " + str(tab) + " add  column `" + str(column_name) + "` " + str(col_type)+" NULL default '"+str(col_defaul) +"' COMMENT '" + str(col_comment) + str(col_front)
        elif (col_isnull !='YES' and col_defaul==None): #如果不允许为空，且没有默认值
            sql = "alter table " + str(tab) + " add  column `" + str(column_name) + "` " + str(col_type)+" not null COMMENT '"+str(col_comment) + str(col_front)
        else:  #如果不允许为空，且设置了默认值
            sql = "alter table " + str(tab) + " add  column `" + str(column_name) + "` " + str(col_type)+" not null default  '"+str(col_defaul) +"' COMMENT '" + str(col_comment) + str(col_front)
    elif mode == 'd':
        sql = "alter table " + str(tab) + " drop column `" + str(column_name)+"`;"
    return sql

# -*- coding: UTF-8 -*-
import sys
import os,json
import time
import operator
import pymysql
from column_check import *
from key_check import *

#初始化不同的数据库
def init(user,passwd,ip,port,db):
  dbsource = pymysql.connect(host=ip, db=db, user=user, passwd=passwd,port=int(port),charset='utf8')
  cursorsource = dbsource.cursor()
  return cursorsource

#手动关闭数据库
def close_db(cursorsource):
  cursorsource.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error,The conf is needed!")
        sys.exit(0)
    else:
        conf_file = sys.argv[1]
        if os.path.isfile(conf_file):
            with open(conf_file) as config_file:
                config = json.load(config_file)
        else:
            print('Config file not exist!')
            sys.exit(0)
    cur_path = os.path.abspath(os.curdir)
    cur_time= time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))
    out_put=(cur_path + '/logs/' + conf_file.split('.json')[0] + cur_time + '.sql')
    db_source = config["source"][-1]
    db_dest = config["dest"][-1]
    #print(db_source)
    #print(db_dest)
    src_coursor=init(*config["source"])
    tag_coursor=init(*config["dest"])
    source_table=get_table(src_coursor)
    #print(source_table)
    dest_table=get_table(tag_coursor)
    #print(dest_table)
    add_table=compact_add(source_table,dest_table)
    #print(add_table)
    same_table=compact_same(source_table,dest_table)
    del_table=compact_del(source_table,dest_table)
    with open(out_put,'w',encoding="utf-8") as f:
        for tab in del_table:
            sql = "drop table `" + tab + "`;"
            f.write(sql+'\n')
        for tab in add_table:
            sql = get_table_sql(src_coursor,db_source,tab)
            #print(sql)
            f.write(sql+'\n')
    #需要比较表结构的表
        for tab in same_table:

            src_col = col_get(src_coursor, db_source, tab)
            dest_col = col_get(tag_coursor, db_dest, tab)
            add_col = compact_add(src_col,dest_col)
            same_col = compact_same(src_col, dest_col)
            del_col = compact_del(src_col, dest_col)
            src_keylist = get_key(src_coursor, db_source, tab)
            tag_keylist = get_key(tag_coursor, db_dest, tab)
            key_dict = compare_key(src_keylist, tag_keylist)
            #
            src_format = get_tb_format(src_coursor,db_source,tab)
            dest_format = get_tb_format(tag_coursor,db_dest,tab)
            if src_format != dest_format:
                sql = 'ALTER TABLE '+ tab +' ROW_FORMAT = ' +src_format+ ';'
                f.write(sql+'\n')

            #先删除索引，否则删除列导出重复删除报错
            for key in key_dict["dellist"]:
                sql = getkey_sql(tab,'', key, 'd')
                f.write(sql+ '\n')

            for column in add_col:
                col_type = col_type_get(src_coursor, db_source, tab, column)
                before_col = before_col_get(src_coursor, db_source, tab, column)
                sql = col_sql(tab, column, col_type, 'add', before_col)
                f.write(sql+'\n')
        #source,target中都有，需要对比，并修改
            for column in same_col:
                src_col_type = col_type_get(src_coursor, db_source, tab, column)
                tag_col_type = col_type_get(tag_coursor, db_dest, tab, column)
                before_col = before_col_get(src_coursor, db_source, tab, column)
                #print(front_column)
            # 如果两个列表完全一致，则不需要修改
                if operator.eq(src_col_type, tag_col_type):
                    continue
                else:
                    sql = col_sql(tab, column, src_col_type, 'modify', before_col)
                    f.write(sql+'\n')
        # source中没有，target中有，需要删除
            for column in del_col:
                sql = "alter table " + tab + " drop column `" + column+"`;"
                f.write(sql+'\n')
            for key in key_dict["addlist"]:
                key_property = getkey_property(src_coursor, db_source, tab, key["name"])
                sql = getkey_sql(tab, key_property, key, 'a')
                f.write(sql + '\n')
    f.close()
    if config["sync"]:
        user,passwd,host,port,db = config["dest"]
        shell='mysql -u'+user+' -h'+host+' -p'+passwd+' -P'+port+' '+db+'<'+out_put
        os.popen(shell)
        print("Success Synced")
    close_db(src_coursor)
    close_db(tag_coursor)


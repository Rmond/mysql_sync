# mysql_sync

mysql表结构自动同步工具

用于将 线上 数据库结构变化同步到 本地环境!
支持功能：

同步新表
同步字段 变动：新增、修改
同步索引 变动：新增、修改
支持预览（只对比不同步变动）

不支持数据表的描述同步和列的描述同步

依赖：
pip3 install PyMySQL

配置
参考 默认配置文件 config.json 配置同步源、目的地址。

配置示例(config.json):
{
 "source": ["user","password","ip","port","db"],
 "dest": ["user","password","ip","port","db"],
 "sync": true //是否同步，false只生成sql语句，不执行
}


运行
直接运行
python3 main.py xxx.json

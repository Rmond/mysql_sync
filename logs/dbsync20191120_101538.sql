alter table testzq modify column `123` varchar(20) not null COMMENT '1' FIRST;
alter table testzq drop column `haha`;
alter table testzq drop index teet;
alter table testzq add primary key (`123`);

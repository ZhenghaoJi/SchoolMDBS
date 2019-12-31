drop database test1;
create database test1;
use test1;
create table admin_login
(
	adminid varchar(8) not null,
    adminpw varchar(16) not null,
	primary key(adminid)
);
insert into admin_login value('admin1','admin1');
create table stu_inf
(
	stuid varchar(8) not null,
    stuname varchar(16) not null,
    sex varchar(1) not null,
    native_place varchar(16),   
	primary key(stuid),
    check(sex='F'or sex='M')
);
insert into stu_inf values('10001','Lee','M','Shanghai'),('10002','Ming','F','Beijing'),('10003','Zhang','F','Tianjin');
create table stu_login
(
	stuid char(8) not null,
    stupw varchar(16),
	primary key(stuid),
    foreign key(stuid) references stu_inf(stuid)
);
insert into stu_login values('10001','changeme123'),('10002','changeme123'),('10003','changeme123');
create table tea_inf
(
	teaid varchar(8) not null,
    teaname varchar(16) not null,
    sex varchar(1),
    college varchar(8),    
    primary key(teaid),
    check(sex='F'or sex='M')
);
insert into tea_inf values('20001','Yu','M','Math'),('20002','Jin','F','Math');
create table tea_login
(
	teaid char(8) not null,
    teapw varchar(16),
	primary key(teaid),
    foreign key(teaid) references tea_inf(teaid)
);
create table class_inf
(
    classid varchar(8) not null,
	classname varchar(16),
    examtime varchar(8),
    teaid varchar(8) not null,
	primary key(classid),
	foreign key(teaid) references tea_inf(teaid)
		on delete cascade
);
insert into class_inf values('30001','MathI','1202','20001');
create table sc
(
	classid varchar(8) not null,
    stuid varchar(8) not null,
	grade varchar(3) ,
    primary key(classid,stuid),
    foreign key(classid) references class_inf(classid),
    foreign key(stuid) references stu_inf(stuid)
);
INSERT INTO sc VALUE('30001','10001','99');


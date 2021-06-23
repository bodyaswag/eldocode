

--Scanaction
create table public.scanaction
(
id serial  primary key,
sku int,
price int,
user_id int,
timestamp timestamp default current_timestamp
);


insert into public.scanaction (sku,price,user_id) values(1,49900,1);
insert into public.scanaction (sku,price,user_id) values(2,32900,1);
insert into public.scanaction (sku,price,user_id) values(3,119000,1);
insert into public.scanaction (sku,price,user_id) values(4,4500,1);

insert into public.scanaction (sku,price,user_id) values(2,31000,2);
insert into public.scanaction (sku,price,user_id) values(3,118000,2);

insert into public.scanaction (sku,price,user_id) values(2,31000,3);
insert into public.scanaction (sku,price,user_id) values(3,118000,3);

insert into public.scanaction (sku,price,user_id) values(2,31000,4);
insert into public.scanaction (sku,price,user_id) values(3,118000,4);

insert into public.scanaction (sku,price,user_id) values(2,31000,5);
insert into public.scanaction (sku,price,user_id) values(3,118000,5);





--Tasks
create table public.tasks
(id serial primary key,
sku int,
tasktype text,
task_dt date,
task_due_dt date
);

insert into public.tasks (sku,tasktype,task_dt) values(3,'Обновить ценник',now()::date)


--Sku


create table public.sku
(sku int,
name text,
img_src text,
price int,
group_name text)
truncate table  public.sku

insert into public.sku (sku,name,img_src,price,group_name) values(1, 'Iphone 12', 'static/sku1.png', 99000, 'Смартфоны');
insert into public.sku (sku,name,img_src,price,group_name) values(71346007, 'Телевизор LG', 'static/sku71346007.png', 33000, 'Телевизоры');
insert into public.sku (sku,name,img_src,price,group_name) values(2,'Холодильник Indesit','static/sku2.png',23000,'Холодильники');
insert into public.sku (sku,name,img_src,price,group_name) values(3,'Macbook Pro','static/sku3.png',120000,'Ноутбуки');
insert into public.sku (sku,name,img_src,price,group_name) values(4,'Фен Philips','static/sku4.png',4900,'Товары для красоты');


--Store
create table public.store(
sku int,
cnt int
);

insert into public.store values(1,10);
insert into public.store values(2,20);
insert into public.store values(3,30);
insert into public.store values(4,40);*


--Pricetags
create view public.pricetags
as 
select 
sku,
price,
timestamp 
from (
select t.*,
row_number () over (partition by sku order by timestamp desc) rn
from public.skanaction t) j
where j.rn = 1
;

--Actualtask
create view public.actualtask
as 
select 
row_number() over (partition by 1) as id,
t.*
from(
select 
gg.sku,
tasktype,
jj.img_src,
jj.name,
jj.group_name,
task_dt
from public.tasks gg
left join public.sku jj
	on gg.sku = jj.sku

union all

select 
t1.sku,
'Добавить на полку',
ll.img_src,
ll.name,
ll.group_name,
now()::date
from public.store t1
left join public.sku ll
	on ll.sku = t1.sku
left join public.pricetags t2
	on t1.sku = t2.sku
where t2.sku is null) t;



--Users
create table public.users(
id int,
name text,
img_src text
)

insert into users values(1,'Eldocode Winner','static/user1.png');
insert into users values(2,'Рома','static/user2.png');
insert into users values(3,'Никита','static/user3.png');
insert into users values(4,'Богдан','static/user4.png');
insert into users values(5,'Вадя','static/user5.png');



--Leaderboard

create view leaderboard
as
select 
j.*,
case when user_id = 1 then 1 else 0 end as user_flg,
k.name,
k.img,
ROW_NUMBER() OVER (PARTITION BY 1 ORDER by j.scan_cnt desc) place,
row_number() over (partition by 1) as id
from (
select 
user_id,
count(*) scan_cnt
from public.scanaction
group by user_id) j
left join public.users k
	on j.user_id = k.id
order by user_flg desc,scan_cnt desc
;
-
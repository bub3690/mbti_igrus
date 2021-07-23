show databases;
use miniter;
select * from users;
delete from users where id=1;


create table users(
id int not null auto_increment,
name varchar(255) not null,
email varchar(255) not null,
hashed_password varchar(255) not null,
profile varchar(2000) not null,
created_at timestamp not null default current_timestamp,
updated_at timestamp null default null on update current_timestamp,
primary key (id),
unique key email (email)
);

create table users_follow_list(
user_id int not null,
follow_user_id int not null,
created_at timestamp not null default current_timestamp,
constraint users_follow_list_user_id_fkey foreign key(user_id) 
references users(id),
constraint users_follow_list_follow_user_id_fkey foreign key(follow_user_id) references users(id)
);

create table tweets(
id int not null auto_increment,
user_id int not null,
tweet varchar(300) not null,
created_at timestamp not null default current_timestamp,
primary key(id),
constraint tweets_user_id_fkey foreign key (user_id) references users(id)
);




#이 부분 부터 mbti 서버
create database mbti_user;
show databases;
use mbti_user;

create table users(
id int not null auto_increment,
name varchar(255) not null,
email varchar(255) not null,
hashed_password varchar(255) not null,
profile varchar(2000) null,
created_at timestamp not null default current_timestamp,
updated_at timestamp null default null on update current_timestamp,
primary key (id),
unique key email (email)
);

select * from users;
delete from users where id=1;




create database mbti_user;
show databases;
use mbti_user;

create table star(
	point int not null,
    id int not null auto_increment,
    primary key (id)
    );

select * from star;

insert into star(
	point
    ) values(
    :point
    );
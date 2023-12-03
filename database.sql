create database if not exists ROBOPETY;

use ROBOPETY;


-- this is the table for the user
-- the user will have a username, password, and email
-- the username and email must be unique
-- the id will be auto incremented
create table if not exist users (
    id int not null auto_increment,
    username varchar(255) not null,
    password varchar(255) not null,
    email varchar(255) not null,
    primary key (id)
);


-- this is the table for the robots
-- the robot will have a name and a photo_url
-- the id will be auto incremented
create table if not exist robots (
    id int not null auto_increment,
    name varchar(255) not null,
    photo_url varchar(255) not null,
    primary key (id)
);


-- insert the robots into the database
-- the robots will have a name and a photo_url
-- the photo_url will be a link to the image in the cloud storage
INSERT INTO robots (name, photo_url) VALUES ('donphan', 'gs://robo_images/donphan.png');
INSERT INTO robots (name, photo_url) VALUES ('alcremie', 'gs://robo_images/alcremie.png');
INSERT INTO robots (name, photo_url) VALUES ('armarouge', 'gs://robo_images/armarouge.png');
INSERT INTO robots (name, photo_url) VALUES ('azumarill', 'gs://robo_images/azumarill.png');
INSERT INTO robots (name, photo_url) VALUES ('blaziken', 'gs://robo_images/blaziken.png');
INSERT INTO robots (name, photo_url) VALUES ('blipbug', 'gs://robo_images/blipbug.png');
INSERT INTO robots (name, photo_url) VALUES ('bramblin', 'gs://robo_images/bramblin.png');
INSERT INTO robots (name, photo_url) VALUES ('breloom', 'gs://robo_images/breloom.png');
INSERT INTO robots (name, photo_url) VALUES ('camerupt', 'gs://robo_images/camerupt.png');
INSERT INTO robots (name, photo_url) VALUES ('charmander', 'gs://robo_images/charmander.png');
INSERT INTO robots (name, photo_url) VALUES ('cottonee', 'gs://robo_images/cottonee.png');
INSERT INTO robots (name, photo_url) VALUES ('croconaw', 'gs://robo_images/croconaw.png');
INSERT INTO robots (name, photo_url) VALUES ('dragalge', 'gs://robo_images/dragalge.png');
INSERT INTO robots (name, photo_url) VALUES ('dwebble', 'gs://robo_images/dwebble.png');
INSERT INTO robots (name, photo_url) VALUES ('escavalier', 'gs://robo_images/escavalier.png');
INSERT INTO robots (name, photo_url) VALUES ('finizen', 'gs://robo_images/finizen.png');
INSERT INTO robots (name, photo_url) VALUES ('gardevoir', 'gs://robo_images/gardevoir.png');
INSERT INTO robots (name, photo_url) VALUES ('geodude', 'gs://robo_images/geodude.png');
INSERT INTO robots (name, photo_url) VALUES ('groudon', 'gs://robo_images/groudon.png');
INSERT INTO robots (name, photo_url) VALUES ('gulpin', 'gs://robo_images/gulpin.png');
INSERT INTO robots (name, photo_url) VALUES ('hippowdon', 'gs://robo_images/hippowdon.png');
INSERT INTO robots (name, photo_url) VALUES ('igglybuff', 'gs://robo_images/igglybuff.png');
INSERT INTO robots (name, photo_url) VALUES ('iron_thorns', 'gs://robo_images/iron_thorns.png');
INSERT INTO robots (name, photo_url) VALUES ('kilowattrel', 'gs://robo_images/kilowattrel.png');
INSERT INTO robots (name, photo_url) VALUES ('kricketot', 'gs://robo_images/kricketot.png');
INSERT INTO robots (name, photo_url) VALUES ('lampent', 'gs://robo_images/lampent.png');
INSERT INTO robots (name, photo_url) VALUES ('latias', 'gs://robo_images/latias.png');
INSERT INTO robots (name, photo_url) VALUES ('latios', 'gs://robo_images/latios.png');
INSERT INTO robots (name, photo_url) VALUES ('leavanny', 'gs://robo_images/leavanny.png');
INSERT INTO robots (name, photo_url) VALUES ('linoone', 'gs://robo_images/linoone.png');
INSERT INTO robots (name, photo_url) VALUES ('pichu', 'gs://robo_images/pichu.png');
INSERT INTO robots (name, photo_url) VALUES ('pignite', 'gs://robo_images/pignite.png');
INSERT INTO robots (name, photo_url) VALUES ('primarina', 'gs://robo_images/primarina.png');
INSERT INTO robots (name, photo_url) VALUES ('psyduck', 'gs://robo_images/psyduck.png');
INSERT INTO robots (name, photo_url) VALUES ('revavroom', 'gs://robo_images/revavroom.png');
INSERT INTO robots (name, photo_url) VALUES ('rotom', 'gs://robo_images/rotom.png');
INSERT INTO robots (name, photo_url) VALUES ('salazzle', 'gs://robo_images/salazzle.png');
INSERT INTO robots (name, photo_url) VALUES ('scream_tail', 'gs://robo_images/scream_tail.png');
INSERT INTO robots (name, photo_url) VALUES ('seadra', 'gs://robo_images/seadra.png');
INSERT INTO robots (name, photo_url) VALUES ('sewaddle', 'gs://robo_images/sewaddle.png');
INSERT INTO robots (name, photo_url) VALUES ('shiinotic', 'gs://robo_images/shiinotic.png');
INSERT INTO robots (name, photo_url) VALUES ('slaking', 'gs://robo_images/slaking.png');
INSERT INTO robots (name, photo_url) VALUES ('staravia', 'gs://robo_images/staravia.png');
INSERT INTO robots (name, photo_url) VALUES ('swanna', 'gs://robo_images/swanna.png');
INSERT INTO robots (name, photo_url) VALUES ('totodile', 'gs://robo_images/totodile.png');
INSERT INTO robots (name, photo_url) VALUES ('tynamo', 'gs://robo_images/tynamo.png');
INSERT INTO robots (name, photo_url) VALUES ('urshifu', 'gs://robo_images/urshifu.png');
INSERT INTO robots (name, photo_url) VALUES ('vanilluxe', 'gs://robo_images/vanilluxe.png');
INSERT INTO robots (name, photo_url) VALUES ('vivillon', 'gs://robo_images/vivillon.png');
INSERT INTO robots (name, photo_url) VALUES ('yveltal', 'gs://robo_images/yveltal.png');
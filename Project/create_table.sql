DROP TABLE IF EXISTS songs1;
CREATE TABLE songs1 (
    Song_Id varchar NOT NULL,
    Song_Name varchar NOT NULL,
    Song_Preview_Url varchar,
    Song_Url varchar ,
    Song_Language varchar NOT NULL,
    Song_Duration varchar NOT NULL,
    Song_Popularity int NOT NULL,
    Artist_Name varchar NOT NULL,
    Artist_Id varchar NOT NULL,
    Artist_No_Followers int NOT NULL,
    Album_Id varchar NOT NULL,
    Album_Name varchar NOT NULL,
    Album_No_Songs int NOT NULL,
    Album_Image varchar,
    Album_ReleaseDate varchar NOT NULL
) ;



DROP TABLE IF EXISTS songs cascade;
CREATE TABLE songs (
    Song_Id varchar Primary Key,
    Song_Name varchar NOT NULL,
    Song_Language varchar NOT NULL,
    Song_Duration varchar NOT NULL,
    Song_Popularity int NOT NULL,
    Album_Id varchar NOT NULL,
    Song_Preview_Url varchar,
    Song_Url varchar 
) ;

DROP TABLE IF EXISTS album cascade;
CREATE TABLE album (
    Album_Id varchar primary key,
    Album_Name varchar NOT NULL,
    Album_No_Songs int NOT NULL,
    Album_ReleaseDate varchar NOT NULL,
    Album_Image varchar 
) ;

DROP TABLE IF EXISTS artist cascade;
CREATE TABLE artist (
    Artist_Id varchar primary key,
    Artist_Name varchar NOT NULL,
    Artisi_No_Songs int Not NULL,
    Artist_No_Followers int NOT NULL
) ;

DROP TABLE IF EXISTS albumHasArtist;
CREATE TABLE albumHasArtist (
    Album_Id varchar NOT NULL,
    Album_Name varchar NOT NULL,
    Artist_Id varchar NOT NULL,
    Artist_Name varchar NOT NULL,
    FOREIGN KEY (Album_Id) References album(Album_Id),
    foreign key (Artist_Id) References artist(Artist_Id)
) ;

DROP TABLE IF EXISTS composedBy;
CREATE TABLE composedBy (
    Song_Id varchar NOT NULL,
    Song_Name varchar NOT NULL,
    Artist_Id varchar NOT NULL,
    Artist_Name varchar NOT NULL, 
    FOREIGN KEY (Song_Id) References songs(Song_Id),
    foreign key (Artist_Id) References artist(Artist_Id)
) ;

DROP TABLE IF EXISTS users cascade;
CREATE TABLE users (
    user_Id varchar NOT NULL primary key,
    user_Name varchar NOT NULL,
    gender varchar NOT NULL,
    email varchar NOT NULL,
    password varchar NOT NULL,
    User_Type varchar NOT NULL 
) ;

DROP TABLE IF EXISTS playlist cascade;
CREATE TABLE playlist (
    playlist_Id int NOT NULL primary key,
    num_Songs int,
    playlist_Name varchar NOT NULL,
    User_Id varchar NOT NULL
) ;

DROP TABLE IF EXISTS favourite;
CREATE TABLE favourite (
    user_Id varchar NOT NULL,
    user_Name varchar NOT NULL,
    Song_Id varchar NOT NULL,
    Song_Name varchar NOT NULL,
    FOREIGN KEY (Song_Id) References songs(Song_Id),
    foreign key (User_Id) References users(User_Id)
) ;

DROP TABLE IF EXISTS follows;
CREATE TABLE follows (
    user_Id varchar NOT NULL,
    user_Name varchar NOT NULL,
    Artist_Id varchar NOT NULL,
    Artist_Name varchar NOT NULL, 
    FOREIGN KEY (User_Id) References users(User_Id),
    foreign key (Artist_Id) References artist(Artist_Id)
) ;

DROP TABLE IF EXISTS hasSong;
CREATE TABLE hasSong (
    playlist_Id int,
    Song_Id varchar NOT NULL,
    FOREIGN KEY (Song_Id) References songs(Song_Id),
    foreign key (playlist_Id) References playlist(playlist_Id)
) ;

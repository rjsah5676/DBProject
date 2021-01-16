SET SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS ORDERS;
DROP TABLE IF EXISTS APPEARED_IN;
DROP TABLE IF EXISTS MOVIEQUEUE;
DROP TABLE IF EXISTS CUSTOMERS;
DROP TABLE IF EXISTS MOVIES;
DROP TABLE IF EXISTS ACTORS;

CREATE TABLE CUSTOMERS(
    CustomerId CHAR(11) NOT NULL,
	LName VARCHAR(30) NOT NULL,
    FName VARCHAR(30) NOT NULL,
    Address VARCHAR(30),
    City VARCHAR(30),
    State VARCHAR(30),
    ZipCode VARCHAR(20) NOT NULL,
    Telephone CHAR(12),
    Email VARCHAR(100) UNIQUE,
    CreditCard CHAR(19) NOT NULL,
    AccountId INT UNIQUE NOT NULL,
    AccountType VARCHAR(10) NOT NULL,
    AccCreateDate DATE,
    Rating INT,
    PRIMARY KEY(CustomerId, AccountId),
    CONSTRAINT CHK_CustomerId CHECK(CustomerId LIKE '___-__-____' AND LENGTH(CustomerId)=11),
    CONSTRAINT CHK_Telephone CHECK(Telephone LIKE '___-___-____' AND LENGTH(Telephone)=12),
    CONSTRAINT CHK_AccountType CHECK(AccountType = 'limited' OR AccountType = 'unlimited'),
    CONSTRAINT CHK_CreditCard CHECK(CreditCard LIKE '____-____-____-____' AND LENGTH(CreditCard)=19),
	CONSTRAINT CHK_cst_Rating CHECK(Rating > 0 AND Rating < 6),
    CONSTRAINT CHK_Email CHECK(Email LIKE '%@%.%')
);

CREATE TABLE ACTORS(
	ActorId INT NOT NULL,
    Age INT NOT NULL,
    Sex VARCHAR(6) NOT NULL,
    Rating INT,
    ActorName VARCHAR(50) NOT NULL,
    PRIMARY KEY(ActorId),
    CONSTRAINT CHK_Sex CHECK(Sex='M' OR Sex='F'),
    CONSTRAINT CHK_Age CHECK(Age > 0 AND Age < 121),
    CONSTRAINT CHK_Rating CHECK(Rating > 0 AND RATING < 6)
);

CREATE TABLE MOVIES(
	MovieId INT NOT NULL,
	MovieType VARCHAR(20),
    MovieName VARCHAR(100) NOT NULL,
    NumCopies INT,
    Rating INT,
    PRIMARY KEY(MovieId),
    CONSTRAINT CHK_MOVIE_Rating CHECK(Rating > 0 AND RATING < 6),
    CONSTRAINT CHK_MovieType CHECK(MovieType = 'Comedy' OR MovieType = 'Drama' OR MovieType = 'Action' OR MovieType = 'Foreign')
);

CREATE TABLE ORDERS(
    OmovieId INT NOT NULL,
    OAccountId INT NOT NULL,
    OrderId INT NOT NULL,
    Date_Time DATETIME,
    Return_Date DATE,
    ORating INT,
    PRIMARY KEY(OrderId),
    FOREIGN KEY(OmovieId) REFERENCES MOVIES(MovieId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(OAccountId) REFERENCES CUSTOMERS(AccountId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE MOVIEQUEUE(
	QcustomerId CHAR(11) NOT NULL,
    QAccountId INT NOT NULL,
    QmovieId INT NOT NULL,
    PRIMARY KEY(QcustomerId, QmovieId),
	FOREIGN KEY(QcustomerId) REFERENCES CUSTOMERS(CustomerId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(QmovieId) REFERENCES MOVIES(MovieId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE APPEARED_IN(
	AmovieId INT NOT NULL,
    AactorId INT NOT NULL,
	PRIMARY KEY(AmovieId, AactorId),
	FOREIGN KEY(AmovieId) REFERENCES MOVIES(movieId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(AactorId) REFERENCES ACTORS(ActorId) ON UPDATE CASCADE ON DELETE CASCADE
);

DELIMITER $$
   CREATE TRIGGER UpdateRating
   AFTER UPDATE ON ORDERS
   FOR EACH ROW
   BEGIN
     UPDATE MOVIES SET Rating = ((SELECT SUM(ORating) FROM ORDERS WHERE OmovieId = NEW.OmovieId)/(SELECT COUNT(*) FROM ORDERS WHERE OmovieId = NEW.OmovieId)) WHERE MovieId = NEW.OMovieId;
   END $$
DELIMITER ;

DELIMITER $$
   CREATE TRIGGER InsertRating
   AFTER INSERT ON ORDERS
   FOR EACH ROW
   BEGIN
     UPDATE MOVIES SET Rating = ((SELECT SUM(ORating) FROM ORDERS WHERE OmovieId = NEW.OmovieId)/(SELECT COUNT(*) FROM ORDERS WHERE OmovieId = NEW.OmovieId)) WHERE MovieId = NEW.OMovieId;
   END $$
DELIMITER ;

INSERT INTO CUSTOMERS VALUES
("111-11-1111","Yang","Shang","123 Success Street","New York","NY","11790","516-632-8959","syang@ajou.ac.kr","1234-5678-1234-5678",3,"limited","2010-01-06",1),
("222-22-2222","Du","Victor","456 Fortune Road","West Lafayette","IN","11790","516-632-4360","vicdu@ajou.ac.kr","5678-1234-5678-1234",2,"limited","2010-12-06",1),
("333-33-3333","Smith","John","789 Peace Blvd.","Los Angeles","CA","93536","315-443-4321","jsmith@ajou.ac.kr","2345-6789-2345-6789",4,"unlimited","2010-12-06",1),
("444-44-4444","Philip","Lewis","135 Knowledge Lane","Stony Brook","NY","11794","516-666-8888","pml@ajou.ac.kr","6789-2345-6789-2345",1,"unlimited","2010-01-06",1);

INSERT INTO ACTORS VALUES
(1, 63, 'M', 5, 'Al Pacino'),
(2, 53, 'M', 2, 'Tim Robbins'),
(3, 33, 'F', 4, 'Keira Knightley'),
(4, 40, 'M', 3, 'Mark Ruffalo'),
(5, 57, 'M', 5, 'Keanu Reeves'),
(6, 30, 'F', 4, 'Charlize Theron'),
(7, 59, 'M', 5, 'Jim Carrey'),
(8, 35, 'F', 3, 'Emilia Clarke');

INSERT INTO MOVIES VALUES
(1, 'Drama', 'The Godfather', 3, 5),
(2, 'Drama', 'Shawshank Redemption', 2, 4),
(3, 'Comedy', 'Borat', 1, 3),
(4, 'Action', 'John Wick 3', 2, 4),
(5, 'Foreign', 'Begin Again', 4, 3),
(6, 'Action', 'Old Guard', 1, 5),
(7, 'Comedy', 'Super Sonic', 1, 4),
(8, 'Comedy', 'Last Christmas', 2, 2);

INSERT INTO ORDERS VALUES
(1, 1, 1, '2020-11-09 10:00:00','2020-12-09',5),
(3, 1, 3, '2020-12-01 09:30:00',null,3),
(3, 2, 2, '2020-12-02 18:15:00',null,4),
(2, 2, 4, '2020-12-02 22:22:00',null,4),
(5, 2, 5, '2020-12-03 20:20:00',null,5),
(7, 3, 6, '2020-12-04 19:22:00',null,3),
(8, 3, 7, '2020-12-05 17:12:00',null,4),
(4, 3, 8, '2020-12-06 10:15:00',null,2),
(6, 4, 9, '2020-12-06 12:07:00',null,4),
(5, 4, 10, '2020-12-07 12:07:00',null,5),
(1, 4, 11, '2020-12-07 13:08:00',null,2),
(7, 4, 12, '2020-12-08 10:00:00',null,5);

INSERT INTO MovieQueue VALUES
("444-44-4444",1,1),
("444-44-4444",1,3),
("222-22-2222",2,2),
("222-22-2222",2,3),
("222-22-2222",2,7),
("111-11-1111",3,5),
("111-11-1111",3,8),
("333-33-3333",4,4),
("333-33-3333",4,1),
("333-33-3333",4,8);

INSERT INTO APPEARED_IN VALUES
(1,1),
(3,1),
(1,2),
(4,5),
(5,3),
(5,4),
(6,6),
(7,7),
(8,8);
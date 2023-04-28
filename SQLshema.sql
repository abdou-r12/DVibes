CREATE TABLE IF NOT EXISTS Login(
        IdLog INTEGER PRIMARY KEY AUTOINCREMENT,
        UserName TEXT,
        PassCode TEXT
);
CREATE TABLE IF NOT EXISTS User(
    IdUser INTEGER PRIMARY KEY AUTOINCREMENT,
    IdLog INTEGER,
    FullName TEXT,
    Pfp TEXT,
    Gender TEXT,
    BirthDay TEXT,
    Location TEXT,
    Experience TEXT,
    Phone INTEGER,
    SocialMedia TEXT,
    Balance INTEGER,
    Interests TEXT,
    CONSTRAINT fk_IdLog
        FOREIGN KEY (IdLog)
        REFERENCES  Login(IdLog)
);
CREATE TABLE IF NOT EXISTS Events(
    IdEvent INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT,
    Discription TEXT,
    Text TEXT,
    Image TEXT,
    Date TEXT
);
CREATE TABLE IF NOT EXISTS News(
    IdNew INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT,
    Discription TEXT,
    Text TEXT,
    Img TEXT,
    Date TEXT
);
CREATE TABLE IF NOT EXISTS Request(
    IdReq INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT,
    Gender TEXT,
    BDay TEXT,
    Email TEXT,
    Resume TEXT,
    CV TEXT
);
CREATE TABLE IF NOT EXISTS Coach(
    IdCoach INTEGER PRIMARY KEY AUTOINCREMENT,
    IdLog INTEGER,
    FullName TEXT,
    Pfp TEXT,
    Gender TEXT,
    BirthDay TEXT,
    Balance INTEGER,
    CONSTRAINT fk_IdLog
        FOREIGN KEY (IdLog)
        REFERENCES  LoginCoach(IdLog)
);
CREATE TABLE IF NOT EXISTS CheckUser(
    IdLog INTEGER,
    Code TEXT,
    CONSTRAINT fk_IdLog
        FOREIGN KEY (IdLog)
        REFERENCES  Login(IdLog)
);
CREATE TABLE IF NOT EXISTS LoginCoach(
    IdLog INTEGER PRIMARY KEY AUTOINCREMENT,
    UserName TEXT,
    PassCode TEXT
);
CREATE TABLE IF NOT EXISTS Cours(
    IdCour INTEGER PRIMARY KEY AUTOINCREMENT,
    IdCoach INTEGER,
    Title TEXT,
    Type TEXT,
    Price INTEGER,
    Description TEXT,
    Pwd TEXT,
    CONSTRAINT fk_IdCoach
        FOREIGN KEY (IdCoach)
        REFERENCES  Coach(IdCoach)
);
CREATE TABLE IF NOT EXISTS Attachment(
    IdAtt INTEGER PRIMARY KEY AUTOINCREMENT,
    IdCour INTEGER,
    Title TEXT,
    Type TEXT,
    Pwd TEXT,
    CONSTRAINT fk_IdCour
        FOREIGN KEY (IdCour)
        REFERENCES Cours(IdCour)
);
CREATE TABLE IF NOT EXISTS Purchase(
    IdPur INTEGER PRIMARY KEY AUTOINCREMENT,
    IdUser INTEGER,
    IdCour INTEGER,
    Date TEXT,
    CONSTRAINT fk_IdCour
        FOREIGN KEY (IdCour)
        REFERENCES Cours(IdCour),
    CONSTRAINT fk_IdUser
        FOREIGN KEY (IdUser)
        REFERENCES User(IdUser)
);
CREATE TABLE IF NOT EXISTS Rapports(
    IdRapport INTEGER PRIMARY KEY AUTOINCREMENT,
    IdUser INTEGER,
    Title TEXT,
    RapportText TEXT,
    Date TEXT,
    CONSTRAINT fk_IdUser
        FOREIGN KEY (IdUser)
        REFERENCES  User(IdUser)
);
CREATE TABLE IF NOT EXISTS LoginCashier(
    IdLog INTEGER PRIMARY KEY AUTOINCREMENT,
    UserName TEXT,
    PassCode TEXT,
    FullName TEXT
);
CREATE TABLE IF NOT EXISTS TRHistory(
    IdTrans INTEGER PRIMARY KEY AUTOINCREMENT,
    IdUser TEXT,
    IdLog INTEGER,
    Send_Date TEXT,
    Receive_Date TEXT,
    Note TEXT,
    CONSTRAINT fk_IdUser
        FOREIGN KEY (IdUser)
        REFERENCES  User(IdUser)
);
CREATE TABLE IF NOT EXISTS Bill(
    IdBil INTEGER PRIMARY KEY AUTOINCREMENT,
    IdUser INTEGER,
    Status TEXT,
    Note TEXT,
    Date TEXT,
    Pwd TEXT,
    CONSTRAINT fk_IdUser
        FOREIGN KEY (IdUser)
        REFERENCES  User(IdUser)
);
CREATE TABLE IF NOT EXISTS DBalance(
    Coin INTEGER
);
INSERT INTO DBalance (Coin) VALUES (0);
CREATE TABLE IF NOT EXISTS CoachPayment(
    IdCP INTEGER PRIMARY KEY AUTOINCREMENT,
    IdCoach INTEGER,
    Date TEXT,
    Status TEXT,
    CCP TEXT,
    Note TEXT,
    CONSTRAINT fk_IdCoach
        FOREIGN KEY (IdCoach)
        REFERENCES  Coach(IdCoach)
);
CREATE TABLE IF NOT EXISTS CoachFeed(
    IdFeed INTEGER PRIMARY KEY AUTOINCREMENT,
    IdCoach INTEGER,
    Content TEXT,
    Date TEXT,
    CONSTRAINT fk_IdCoach
        FOREIGN KEY (IdCoach)
        REFERENCES  Coach(IdCoach)
);
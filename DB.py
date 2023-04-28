import sqlite3
from datetime import date

global connection,cursor
connection = sqlite3.connect('DVibes.db', check_same_thread=False)
cursor = connection.cursor()

def Create_tables(cursor):
    Login = '''
    CREATE TABLE IF NOT EXISTS Login(
        IdLog INTEGER PRIMARY KEY AUTOINCREMENT,
        UserName TEXT,
        PassCode TEXT
    )
    '''
    cursor.execute(Login)
    print('login table created successfully')
    User = '''
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
    )
    '''
    cursor.execute(User)
    print('user table created successfully')
    Event = '''
    CREATE TABLE IF NOT EXISTS Events(
        IdEvent INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT,
        Discription TEXT,
        Text TEXT,
        Image TEXT,
        Date TEXT
    )
    '''
    cursor.execute(Event)
    print('Event table created successfully')
    News  = '''
    CREATE TABLE IF NOT EXISTS News(
        IdNew INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT,
        Discription TEXT,
        Text TEXT,
        Img TEXT,
        Date TEXT
    )
    '''
    print('News table created successfully')
    cursor.execute(News)
    Request ='''
    CREATE TABLE IF NOT EXISTS Request(
        IdReq INTEGER PRIMARY KEY AUTOINCREMENT,
        FullName TEXT,
        Gender TEXT,
        BDay TEXT,
        Email TEXT,
        Resume TEXT,
        CV TEXT
    )
    '''
    cursor.execute(Request)
    print('Request table created successfully')
    Coach = '''
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
            REFERENCES  Login(IdLog)
    )
    '''
    cursor.execute(Coach)
    print('Coach table created successfully')
    Check ='''
    CREATE TABLE IF NOT EXISTS CheckUser(
        IdLog INTEGER,
        Code TEXT,
        CONSTRAINT fk_IdLog
            FOREIGN KEY (IdLog)
            REFERENCES  Login(IdLog)
    )
    '''
    cursor.execute(Check)
    print('Check table created successfully')
    Login_coach = '''
    CREATE TABLE IF NOT EXISTS LoginCoach(
        IdLog INTEGER PRIMARY KEY AUTOINCREMENT,
        UserName TEXT,
        PassCode TEXT
    )
    '''
    cursor.execute(Login_coach)
    print('logincoch table created successfully')
    Cours = '''
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
    )
    '''
    cursor.execute(Cours)
    print('Cours table created successfully')
    Attachment = '''
    CREATE TABLE IF NOT EXISTS Attachment(
        IdAtt INTEGER PRIMARY KEY AUTOINCREMENT,
        IdCour INTEGER,
        Title TEXT,
        Type TEXT,
        Pwd TEXT,
        CONSTRAINT fk_IdCour
            FOREIGN KEY (IdCour)
            REFERENCES Cours(IdCour)
    )
    '''
    cursor.execute(Attachment)
    print('Attachment table created successfully')
    Purchase = '''
    CREATE TABLE IF NOT EXISTS Purchase(
        IdPur INTEGER PRIMARY KEY AUTOINCREMENT,
        IdUser INTEGER,
        IdCour INTEGER,
        Date TEXT
    )
    '''
    cursor.execute(Purchase)
    print('Purchase table created successfully')
    rapport = '''
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
    '''
    cursor.execute(rapport)
    print('rapport table created successfully')
    Cashier = '''
    CREATE TABLE IF NOT EXISTS LoginCashier(
        IdLog INTEGER PRIMARY KEY AUTOINCREMENT,
        UserName TEXT,
        PassCode TEXT,
        FullName TEXT
    )
    '''
    cursor.execute(Cashier)
    print('login cashier table created successfully')
    transfer_history = '''
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
    '''
    cursor.execute(transfer_history)
    print('transfer history table created successfully')
    bill = '''
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
    )
    '''
    cursor.execute(bill)
    print('bill table created successfully')
    DBalance = '''
    CREATE TABLE IF NOT EXISTS DBalance(
        Coin INTEGER
    );
    '''
    cursor.execute(DBalance)
    print('DBalance table created successfully')
    cursor.execute("INSERT INTO DBalance (Coin) VALUES (0)")
    Coach_payment = '''
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
    '''
    cursor.execute(Coach_payment)
    print('Coach_payment table created successfully')
    coach_feed = '''
    CREATE TABLE IF NOT EXISTS CoachFeed(
        IdFeed INTEGER PRIMARY KEY AUTOINCREMENT,
        IdCoach INTEGER,
        Content TEXT,
        Date TEXT,
        CONSTRAINT fk_IdCoach
            FOREIGN KEY (IdCoach)
            REFERENCES  Coach(IdCoach)
    );
    '''
    cursor.execute(coach_feed)
    print('coach feed table created successfully')
    coach_map = '''
    CREATE TABLE IF NOT EXISTS CoachMap(
        IdMap INTEGER PRIMARY KEY AUTOINCREMENT,
        IdCoach INTEGER,
        Location TEXT,
        LocationLink TEXT,
        Note TEXT,
        CONSTRAINT fk_IdCoach
            FOREIGN KEY (IdCoach)
            REFERENCES  Coach(IdCoach)
    )
    '''
    cursor.execute(coach_map)
    print('coach map table created successfully')
    connection.commit()

def setVariable():
    balance = cursor.execute("SELECT * FROM DBalance").fetchone()
    if balance == None:
        cursor.execute("UPDATE DBalance SET Coin = ?",[0])
        connection.commit()

def Update_News(id,title,description,text,dir):
    last_date=date.today()
    if dir == "":
        cursor.execute("UPDATE News SET Title=?,Discription=?,Text=?,Date=? WHERE IdNew=?",[title,description,text,last_date,id])
    else:
        cursor.execute("UPDATE News SET Title=?,Discription=?,Text=?,Img=?,Date=? WHERE IdNew=?",[title,description,text,dir,last_date,id])
    connection.commit()

def Remove_News(id):
    cursor.execute("DELETE FROM News WHERE IdNew=?",[id])
    connection.commit()

def Update_Events(id,title,description,text,dir):
    last_date=date.today()
    if dir == "":
        cursor.execute("UPDATE Events SET Title=?,Discription=?,Text=?,Date=? WHERE IdEvent=?",[title,description,text,last_date,id])
    else:
        cursor.execute("UPDATE Events SET Title=?,Discription=?,Text=?,Img=?,Date=? WHERE IdEvent=?",[title,description,text,dir,last_date,id])
    connection.commit()

def Remove_Events(id):
    cursor.execute("DELETE FROM Events WHERE IdEvent=?",[id])
    connection.commit()

def Remove_Coach_Req(id):
    cursor.execute("DELETE FROM Request WHERE IdReq=?",[id])
    connection.commit()

def Remove_Coach(id):
    cursor.execute("DELETE FROM Coach WHERE IdCoach=?",[id])
    cursor.execute("DELETE FROM LoginCoach WHERE IdLog=?",[id])
    connection.commit()

if __name__ == "__main__":
    print('database created')
    Create_tables(cursor)
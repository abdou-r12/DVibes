from flask import(
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)
import sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import date
from Functions import *
from DB import *

app = Flask(__name__)
app.secret_key = "secret key"
connection = sqlite3.connect('DVibes.db', check_same_thread=False)
cursor = connection.cursor()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# home page
@app.route("/")
def index():
    if Get_ID()=="admin":
        user = "admin"
        usertype = "admin"
    elif Get_ID()!=None:
        user = cursor.execute('SELECT FullName FROM User WHERE IdUser = ?',[Get_ID()]).fetchone()[0]
        usertype = "user"
    elif Get_ID_Coach()!=None:
        user = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[Get_ID_Coach()]).fetchone()[0]
        usertype = "coach"
    else:
        user = None
        usertype = None
    return render_template("home/index.html",log=Check_log(),user=user,usertype=usertype)

# Events and news page
@app.route("/evnew")
def evnew():
    events = cursor.execute('SELECT * FROM Events ORDER BY IdEvent DESC').fetchall()[:3]
    news = cursor.execute('SELECT * FROM News ORDER BY IdNew DESC').fetchall()[:3]
    return render_template("home/evnew.html",news=news,events=events)

# show all the events
@app.route("/events")
def events():
    data = cursor.execute('SELECT * FROM Events').fetchall()
    return render_template("home/events.html",data=data,log=Check_log())

# show one detailed event
@app.route("/event<id>")
def show_event(id):
    if Get_ID()=="admin":
        user = "admin"
    elif Get_ID()!=None:
        user = cursor.execute('SELECT FullName FROM User WHERE IdUser = ?',[Get_ID()]).fetchone()[0]
    else:
        user = None
    data = cursor.execute("SELECT * FROM Events WHERE IdEvent=?",[id]).fetchone()
    return render_template("home/show-event.html",id=id,data=data,user=user,log=Check_log())

# show all the news
@app.route("/news")
def news():
    log = Check_log()
    data = cursor.execute('SELECT * FROM News').fetchall()
    return render_template("home/news.html",data=data,log=log)

# show one detailed news
@app.route("/new<id>")
def show_new(id):
    if Get_ID()=="admin":
        user = "admin"
    elif Get_ID()!=None:
        user = cursor.execute('SELECT FullName FROM User WHERE IdUser = ?',[Get_ID()]).fetchone()[0]
    else:
        user = None
    data = cursor.execute("SELECT * FROM News WHERE IdNew=?",[id]).fetchone()
    return render_template("home/show-New.html",id=id,data=data,user=user,log=Check_log())

# sing up page
@app.route("/singup",methods = ['GET' , 'POST'])
def singup():
    if Check_log()==True:
        if Get_ID()=="admin":
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('user'))
    if request.method == 'POST':
        email = request.form['email']
        if(cursor.execute("SELECT EXISTS(SELECT UserName FROM Login WHERE UserName=?)",[email]).fetchone()[0]==1):
            return redirect(url_for('singup'))
        else:
            fullname = request.form['fullname']
            gender = request.form['check']
            bday = request.form['bday']
            password = request.form['password']
            cursor.execute('''INSERT INTO Login(UserName, PassCode)
                            VALUES('{email}','{password}')
                        '''.format(email=email,password=password))
            iD = cursor.execute("SELECT IdLog FROM Login WHERE UserName = '{email}'".format(email=email)).fetchone()[0]
            cursor.execute('''INSERT INTO User(IdLog, FullName, pfp, Gender, BirthDay, Balance)
                            VALUES('{id}','{fullname}','{pfp}','{gender}','{bd}','{bal}')
                        '''.format(id=iD,fullname=fullname,pfp=None,gender=gender,bd=bday,bal='0'))
            cursor.execute('''INSERT INTO CheckUser(IdLog,Code)
                            VALUES('{id}','{tsc}')'''.format(id=iD,tsc=twostepcheck(email)))
            connection.commit()
            id = cursor.execute("SELECT IdUser FROM User WHERE IdLog='{id}'".format(id=iD)).fetchone()[0]
            session['user'] = id
            session['log'] = True
            return redirect(url_for('user_check'))
    return render_template("register/singup.html")

# athautification page for user
@app.route('/user-check',methods = ['GET' , 'POST'])
def user_check():
    id = cursor.execute('SELECT IdLog FROM User WHERE IdUser = ?',[session['user']]).fetchone()[0]
    code = cursor.execute("SELECT Code FROM CheckUser WHERE IdLog = ?",[id]).fetchone()[0]
    if request.method == "POST":
        codeinput = request.form['code']
        if code == codeinput:
            cursor.execute("DELETE FROM CheckUser WHERE IdLog=?",[id])
            connection.commit()
            return redirect(url_for('user'))
        else:
            return redirect(url_for('user_check'))
    return render_template("register/twostepcheck.html")

# ask to be a coach
@app.route('/becoach',methods = ['GET' , 'POST'])
def be_coach():
    if Check_log()==True:
        return redirect(url_for('login'))
    if Get_ID() == 'admin':
        return redirect(url_for('admin'))
    if request.method == "POST":
        email = request.form['email']
        if(cursor.execute("SELECT EXISTS(SELECT UserName FROM LoginCoach WHERE UserName=?)",[email]).fetchone()[0]==1):
            return redirect(url_for('be_coach'))
        else:
            UPLOAD_FOLDER = 'static/uploads/request'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            file = request.files['file']
            fullname = request.form['fullname']
            gender = request.form['check']
            bday = request.form['bday']
            resume = request.form['resume']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filedir = app.config['UPLOAD_FOLDER']+"/"+filename
            cursor.execute('''INSERT INTO Request(FullName, Gender, BDay, Email, Resume, CV)
                                VALUES('{fullname}','{gender}','{bday}','{email}','{resume}','{cv}')
                            '''.format(fullname=fullname,gender=gender,bday=bday,email=email,resume=resume,cv=filedir))
            connection.commit()
    return render_template('register/becoach.html')

# login page for user
@app.route('/login',methods = ['GET' , 'POST'])
def login():
    if Check_log()==True:
        if Get_ID()=="admin":
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('user'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if(username=="admin" and password=="admin"):
            session["user"]="admin"
            session["log"]=True
            return redirect(url_for("admin"))
        elif(cursor.execute("SELECT EXISTS(SELECT * FROM Login WHERE UserName = ?)",[username]).fetchone()[0]==0):
            return redirect(url_for('login'))
        else:
            AccountInfo = cursor.execute("SELECT * FROM Login WHERE UserName = ?",[username]).fetchone()
            if AccountInfo[2]==password:
                session['user']=AccountInfo[0]
                session['log']=True
                return redirect(url_for('user'))
            else:
                return redirect(url_for("login"))
    return render_template("register/login.html")

# login page for coach
@app.route('/login-coach',methods = ['GET' , 'POST'])
def login_coach():
    if Check_log()==True:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if(cursor.execute("SELECT EXISTS(SELECT * FROM LoginCoach WHERE UserName = ?)",[username]).fetchone()[0]==0):
            return redirect(url_for('login-coach'))
        else:
            AccountInfo = cursor.execute("SELECT * FROM LoginCoach WHERE UserName = ?",[username]).fetchone()
            if AccountInfo[2]==password:
                session['coach']=AccountInfo[0]
                session['log']=True
                return redirect(url_for('coach'))
            else:
                return redirect(url_for("login_coach"))
    return render_template("register/login-coach.html")

# user main
@app.route('/user')
def user():
    if Check_log()!=True or Get_ID() == None:
        return redirect(url_for("login"))
    elif session["user"]=="admin":
        return redirect(url_for("admin"))
    elif (cursor.execute("SELECT EXISTS(SELECT * FROM CheckUser WHERE IdLog=?)",[cursor.execute("SELECT IdLog FROM User WHERE IdUser=?",[session["user"]]).fetchone()[0]]).fetchone()[0]==1):
        return redirect(url_for('user_check'))
    return render_template("user/usermain.html")

# user profile
@app.route('/user/profile')
def userprofile():
    if Check_log()!=True or Get_ID() == None:
        return redirect(url_for('login'))
    elif session["user"]=="admin":
        return redirect(url_for('admin'))
    elif (cursor.execute("SELECT EXISTS(SELECT * FROM CheckUser WHERE IdLog=?)",[cursor.execute("SELECT IdLog FROM User WHERE IdUser=?",[session["user"]]).fetchone()[0]]).fetchone()[0]==1):
        return redirect(url_for('user_check'))
    data = cursor.execute("SELECT * FROM User WHERE IdUser=?",[session["user"]]).fetchone()
    email = cursor.execute("SELECT UserName FROM Login WHERE IdLog=?",[data[1]]).fetchone()[0]
    return render_template("user/profile.html",data=data,email=email)

# admin main
@app.route('/admin')
def admin():
    if Check_log()==False:
        return redirect(url_for('login'))
    elif session["user"] != "admin":
        return redirect(url_for("login"))
    return render_template("admin/adminmain.html")

# news manager page
@app.route('/admin/news-manager',methods = ['POST','GET'])
def news_manager():
    if Check_log()!=True or session['user']!="admin":
        return redirect(url_for('login'))
    else:
        data = cursor.execute('select * from News').fetchall()
        heading = ('ID','Title','Description','Content','Date','Picture')
        if request.method == "POST":
            UPLOAD_FOLDER = 'static/uploads/news'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            file = request.files['file']
            title = request.form['title']
            text = request.form['text']
            disc = request.form['discription']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filedir = app.config['UPLOAD_FOLDER']+"/"+filename
            cursor.execute('''INSERT INTO News(Title, Discription,Text, Img, Date)
                            VALUES('{title}','{disc}','{text}','{img}','{date}')
                        '''.format(title=title,disc=disc,text=text,img=filedir,date=date.today()))
            connection.commit()
    return render_template("admin/news-manager.html",heading=heading,data=data)

# remove news function
@app.route('/admin/news-manager/remove:<id>')
def remove_news(id):
    if Check_log()==True and session['user']=="admin":
        Remove_News(id)
    else:
        return redirect(url_for('login'))
    return redirect(url_for('news_manager'))

# edit news function
@app.route('/admin/news-manager/edit:<id>',methods = ['POST','GET'])
def edit_news(id):
    if Check_log()!=True and session['user']!="admin":
        return redirect(url_for('login'))
    else:
        data = cursor.execute("SELECT * FROM News WHERE IdNew=?",[id]).fetchone()
        if request.method == "POST":
            UPLOAD_FOLDER = 'static/uploads/news'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            title = request.form['title']
            disc = request.form['discription']
            text = request.form['text']
            file = request.files['file']
            filename = secure_filename(file.filename)
            if filename == "":
                filedir = ""
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filedir = UPLOAD_FOLDER+"/"+filename
            Update_News(id,title,disc,text,filedir)
            return redirect(url_for("news_manager"))
    return render_template("admin/edit-news.html",data=data)

# events manager page
@app.route('/admin/events-manager',methods = ['POST','GET'])
def events_manager():
    if Check_log()!=True and session['user']!="admin":
        return redirect(url_for('login'))
    else:
        data = cursor.execute('select * from Events').fetchall()
        heading = ('ID','Title','Description','Content','Picture','Date')
        if request.method == "POST":
            UPLOAD_FOLDER = 'static/uploads/events'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            file = request.files['file']
            title = request.form['title']
            text = request.form['text']
            disc = request.form['discription']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filedir = UPLOAD_FOLDER+"/"+filename
            cursor.execute('''INSERT INTO Events(Title, Discription,Text, Image, Date)
                                VALUES('{title}','{disc}','{text}','{img}','{date}')
                        '''.format(title=title,disc=disc,text=text,img=filedir,date=date.today()))
            connection.commit()
    return render_template("admin/events-manager.html",data=data,heading=heading)

# remove event function
@app.route('/admin/event-manager/remove:<id>')
def remove_event(id):
    if Check_log()==True and session['user']=="admin":
        Remove_Events(id)
    else:
        return redirect(url_for('login'))
    return redirect(url_for('events_manager'))

# edit event function
@app.route('/admin/events-manager/edit:<id>',methods = ['POST','GET'])
def edit_events(id):
    if Check_log()!=True and session['user']!="admin":
        return redirect(url_for('login'))
    else:
        data = cursor.execute("SELECT * FROM Events WHERE IdEvent=?",[id]).fetchone()
        if request.method == "POST":
            UPLOAD_FOLDER = 'static/uploads/event'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            title = request.form['title']
            disc = request.form['discription']
            text = request.form['text']
            file = request.files['file']
            filename = secure_filename(file.filename)
            if filename == "":
                filedir = ""
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filedir = UPLOAD_FOLDER+"/"+filename
            Update_Events(id,title,disc,text,filedir)
            return redirect(url_for("events_manager"))
    return render_template("admin/edit-events.html",data=data)

# coach manager page
@app.route('/admin/coach-manager',methods = ['POST','GET'])
def add_coach():
    if Check_log()!=True and session['user']!="admin":
        return redirect(url_for('login'))
    else:
        coach = cursor.execute('SELECT * FROM Coach').fetchall()
        requests = cursor.execute('select * from Request').fetchall()
        heading_coach = ('ID','Title','Description','Content','Picture','Date')
        heading_req = ('id','full name','gender','birthday','email','resume','cv')
    return render_template('admin/coach-manager.html',heading_coach=heading_coach,heading_req=heading_req,coach=coach,requests=requests)

# accept request to be coach page
@app.route("/admin/coach-manager/remove:<id>")
def Remove_coach(id):
    if Check_log()==True and session['user']=="admin":
        Remove_Coach(id)
    else:
        return redirect(url_for('login'))
    return redirect(url_for('add_coach'))

# remove request to be coach page
@app.route("/admin/coach-manager/accept:<id>")
def accept_coach(id):
    if Check_log()!=True and session['user']!="admin":
        return redirect(url_for('login'))
    else:
        info = cursor.execute("SELECT * FROM Request WHERE IdReq=?",[id]).fetchone()
        cursor.execute('''INSERT INTO LoginCoach(UserName, PassCode)
                            VALUES('{email}','{password}')
                    '''.format(email=info[4],password=get_random_string(8)))
        iD = cursor.execute("SELECT IdLog FROM LoginCoach WHERE UserName = '{email}'".format(email=info[4])).fetchone()[0]
        cursor.execute('''INSERT INTO Coach(IdLog, FullName, pfp, Gender, BirthDay)
                            VALUES('{id}','{fullname}','{pfp}','{gender}','{bd}')
                    '''.format(id=iD,fullname=info[1],pfp=None,gender=info[2],bd=info[3]))
        cursor.execute("DELETE FROM Request WHERE IdReq=?",[id])
        connection.commit()
        return redirect(url_for('add_coach'))

# coach page
@app.route("/coach")
def coach():
    if Check_log()!=True or Get_ID_Coach()==None:
        return redirect(url_for('login_coach'))
    return render_template("coach/coachmain.html")

# cours manager page
@app.route("/coach/cours-manager",methods = ['POST','GET'])
def cours_manager():
    if Check_log()!=True or Get_ID_Coach()==None:
        return redirect(url_for('login_coach'))
    data = cursor.execute('SELECT * FROM Cours WHERE IdCoach = ?',[Get_ID_Coach()]).fetchall()
    if request.method == "POST":
        title = request.form['title']
        courstype =request.form['type']
        file = request.files['file']
        UPLOAD_FOLDER = 'static/uploads/cours'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filedir = UPLOAD_FOLDER+"/"+filename
        cursor.execute('''INSERT INTO Cours(IdCoach, Title, Type, Playlist, Pwd)
                            VALUES('{id}','{title}','{courstype}',"None",'{pwd}')
                        '''.format(id=Get_ID_Coach(),title=title,courstype=courstype,pwd=filedir))
        connection.commit()
    return render_template("coach/cours-manager.html",data=data)

# Create playlist
@app.route('/coach/playlist-manager',methods = ['POST','GET'])
def cours_playlist():
    if Check_log()!=True or Get_ID_Coach()==None:
        return redirect(url_for('login_coach'))
    data = cursor.execute('''SELECT * FROM Cours WHERE IdCoach = {id} AND Playlist = "None"'''.format(id=Get_ID_Coach()))
    if request.method == "POST":
        id = request.form['id-cour']
        print(id)
    return render_template("coach/cours-playlist.html",data=data)

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("log",False)
    return redirect('login')

@app.route('/logout-coach')
def logout_coach():
    session.pop("coach",None)
    session.pop("log",False)
    return redirect('login-coach')

def Check_log():
    global log
    log = False
    if "log" in session:
        log = session["log"]
    return log

def Get_ID():
    global user
    user = None
    if "user" in session:
        user = cursor.execute("SELECT IdUser FROM User WHERE IdLog = ?",[session["user"]]).fetchone()[0]
    return user

def Get_ID_Coach():
    global coach
    coach = None
    if "coach" in session:
        coach = cursor.execute("SELECT IdCoach FROM Coach WHERE IdLog = ?",[session["coach"]]).fetchone()[0]
    return coach

if __name__ == '__main__':
    app.run(debug=Flask,host='0.0.0.0')
    connection.close()
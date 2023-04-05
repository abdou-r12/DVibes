from flask import(
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
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

# home page
@app.route("/")
def index():
    global info
    info = ""
    if(session.get("user") != None):
        if(session.get("user") == "admin"):
            pass
        else:
            info = cursor.execute("SELECT FullName FROM User WHERE IdUser=?",[session.get("user")]).fetchone()[0]
    if(session.get("coach") != None):
        info = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach=?",[session.get("coach")]).fetchone()[0]
    return render_template("home/index.html",log=Check_log(),user=Get_Account_Type(),info=info)

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
        elif Get_ID()!=None:
            return redirect(url_for('user'))
        elif Get_ID_Coach()!=None:
            return redirect(url_for("coach"))
    if request.method == 'POST':
        email = request.form['email']
        if(cursor.execute("SELECT EXISTS(SELECT UserName FROM Login WHERE UserName=?)",[email]).fetchone()[0]==1):
            flash("Email already used try to login or use different email")
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

# ask to be a coach
@app.route('/becoach',methods = ['GET' , 'POST'])
def be_coach():
    if Check_log()==True:
        if Get_ID()=="admin":
            return redirect(url_for('admin'))
        elif Get_ID()!=None:
            return redirect(url_for('user'))
        elif Get_ID_Coach()!=None:
            return redirect(url_for("coach"))
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
            ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filedir = app.config['UPLOAD_FOLDER']+"/"+filename
            cursor.execute('''INSERT INTO Request(FullName, Gender, BDay, Email, Resume, CV)
                                VALUES('{fullname}','{gender}','{bday}','{email}','{resume}','{cv}')
                            '''.format(fullname=fullname,gender=gender,bday=bday,email=email,resume=resume,cv=filedir))
            connection.commit()
    return render_template('register/becoach.html')

@app.route('/login',methods = ['GET' , 'POST'])
def login():
    if Check_log()==True:
        if Get_ID()=="admin":
            return redirect(url_for('admin'))
        elif Get_ID()!=None:
            return redirect(url_for('user'))
        elif Get_ID_Coach()!=None:
            return redirect(url_for("coach"))
    if request.method == "POST":
        user_username = request.form['user_username']
        user_password = request.form["user_password"]
        coach_username = request.form['coach_username']
        coach_password = request.form["coach_password"]
        if (coach_username == "" and coach_password == ""):
            if(user_username=="admin" and user_password=="admin"):
                session["user"]="admin"
                session["log"]=True
                return redirect(url_for("admin"))
            elif(cursor.execute("SELECT EXISTS(SELECT * FROM Login WHERE UserName = ?)",[user_username]).fetchone()[0]==0):
                flash("Username doesn't exist please check again")
                return redirect(url_for('login'))
            else:
                AccountInfo = cursor.execute("SELECT * FROM Login WHERE UserName = ?",[user_username]).fetchone()
                if AccountInfo[2]==user_password:
                    session['user']=AccountInfo[0]
                    session['log']=True
                    return redirect(url_for('user'))
                else:
                    flash('Incorrect password please check again')
                    return redirect(url_for("login"))
        elif(user_username == "" and user_password == ""):
            if(coach_username=="admin" and coach_password=="admin"):
                session["user"]="admin"
                session["log"]=True
                return redirect(url_for("admin"))
            elif(cursor.execute("SELECT EXISTS(SELECT * FROM LoginCoach WHERE UserName = ?)",[coach_username]).fetchone()[0]==0):
                flash("Username doesn't exist please check again")
                return redirect(url_for('login'))
            else:
                AccountInfo = cursor.execute("SELECT * FROM LoginCoach WHERE UserName = ?",[coach_username]).fetchone()
                if AccountInfo[2]==coach_password:
                    session['coach']=AccountInfo[0]
                    session['log']=True
                    return redirect(url_for('coach'))
                else:
                    flash('Incorrect password please check again')
                    return redirect(url_for("login"))
    return render_template('register/log.html')

# user main
@app.route('/user')
def user():
    if Check_log()!=True or session.get("user")==None:
        return redirect(url_for("login"))
    elif (Check_authentification()==1):
        return redirect(url_for('user_check'))
    return render_template("user/usermain.html")

# athautification page for user
@app.route('/user-check',methods = ['GET' , 'POST'])
def user_check():
    if Check_log()!=True:
        return redirect(url_for("login"))
    id = cursor.execute('SELECT IdLog FROM User WHERE IdUser = ?',[session['user']]).fetchone()[0]
    email = cursor.execute('SELECT UserName FROM Login WHERE IdLog = ?',[session['user']]).fetchone()[0]
    code = cursor.execute("SELECT Code FROM CheckUser WHERE IdLog = ?",[id]).fetchone()[0]
    if request.method == "POST":
        codeinput = request.form['code']
        if code == codeinput:
            cursor.execute("DELETE FROM CheckUser WHERE IdLog=?",[id])
            connection.commit()
            return redirect(url_for('user'))
        else:
            flash("Incorrect code entered. Please try again")
            return redirect(url_for('user_check'))
    return render_template("register/twostepcheck.html",email=email)

# user profile
@app.route('/user/profile')
def userprofile():
    if Check_log()!=True or Get_ID() == None:
        return redirect(url_for('login'))
    elif session["user"]=="admin":
        return redirect(url_for('admin'))
    elif (Check_authentification()==1):
        return redirect(url_for('user_check'))
    data = cursor.execute("SELECT * FROM User WHERE IdUser=?",[session["user"]]).fetchone()
    email = cursor.execute("SELECT UserName FROM Login WHERE IdLog=?",[data[1]]).fetchone()[0]
    course_id = cursor.execute("SELECT Idcour FROM Purchase WHERE IdUser=?",[session["user"]]).fetchall()
    course_liste = []
    for id in course_id:
        course_liste.append(cursor.execute("SELECT * FROM Cours WHERE IdCour=?",[id[0]]).fetchone())
    return render_template("user/profile.html",data=data,email=email,course_liste=course_liste)

# show all course available for user
@app.route('/user/cours')
def check_courses():
    if Check_log()!=True or Get_ID() == None:
        return redirect(url_for('login'))
    elif session["user"]=="admin":
        return redirect(url_for('admin'))
    elif (Check_authentification()==1):
        return redirect(url_for('user_check'))
    cours = cursor.execute("SELECT * FROM Cours").fetchall()
    return render_template("user/cours.html",cours=cours)

# show detail of one course
@app.route('/user/cours/overview:<id>')
def over_view_course(id):
    if Check_log()!=True or Get_ID() == None:
        return redirect(url_for('login'))
    elif session["user"]=="admin":
        return redirect(url_for('admin'))
    elif (Check_authentification()==1):
        return redirect(url_for('user_check'))
    cour_info = cursor.execute("SELECT * FROM Cours WHERE IdCour=?",[id]).fetchone()
    return render_template("user/over-view.html",cour_info=cour_info,id=Get_ID())

# purchase function
@app.route('/user/cours/<id_user>-purchase:<id_course>')
def purchase(id_user,id_course):
    if Check_log()!=True or Get_ID() == None:
        return redirect(url_for('login'))
    elif session["user"]=="admin":
        return redirect(url_for('admin'))
    elif (Check_authentification()==1):
        return redirect(url_for('user_check'))
    user_balance = cursor.execute("SELECT Balance FROM User WHERE IdUser=?",[id_user]).fetchone()[0]
    course_balance = cursor.execute("SELECT Price FROM Cours WHERE IdCour=?",[id_course]).fetchone()[0]
    if(user_balance >= course_balance):
        cursor.execute("INSERT INTO Purchase(IdUser, IdCour) VALUES('{id_user}','{id_course}')".format(id_user=id_user,id_course=id_course))
        cursor.execute("UPDATE User SET Balance=? WHERE IdUser=?",[user_balance-course_balance,id_user])
        connection.commit()
        return redirect(url_for('user'))
    else:
        # refill
        pass

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
            ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
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
            ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
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
            ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
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
            ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
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
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
        title = request.form['title']
        courstype =request.form['type']
        file = request.files['file']
        price = request.form['price']
        Description = request.form['description']
        UPLOAD_FOLDER = 'static/uploads/cours/cover'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filedir = UPLOAD_FOLDER+"/"+filename
        cursor.execute('''INSERT INTO Cours(IdCoach, Title, Type, Price, Description,Pwd)
                            VALUES('{id}','{title}','{courstype}','{price}','{Description}','{pwd}')
                        '''.format(id=Get_ID_Coach(),title=title,courstype=courstype,price=price,Description=Description,pwd=filedir))
        connection.commit()
    return render_template("coach/cours-manager.html",data=data)

@app.route('/coach/cours-list')
def cours_playlist():
    if Check_log()!=True or Get_ID_Coach()==None:
        return redirect(url_for('login_coach'))
    data = cursor.execute('''SELECT * FROM Cours WHERE IdCoach = {id}'''.format(id=Get_ID_Coach()))
    return render_template("coach/cours-playlist.html",data=data)

@app.route('/coach/cours-list/<id>',methods = ['POST','GET'])
def cours(id):
    if Check_log()!=True or Get_ID_Coach()==None:
        return redirect(url_for('login_coach'))
    info = cursor.execute("SELECT * FROM Cours WHERE IdCour={id_cour} AND IdCoach={id_coach}".format(id_cour=id,id_coach=Get_ID_Coach())).fetchone()
    cour_video = cursor.execute("SELECT * FROM Attachment WHERE IdCour={id} AND Type='video'".format(id=id)).fetchall()
    cour_doc = cursor.execute("SELECT * FROM Attachment WHERE IdCour={id} AND Type='document'".format(id=id)).fetchall()
    if request.method == "POST":
        title = request.form['title']
        file = request.files['file']
        att_type = request.form['type']
        if att_type == 'video':
            ALLOWED_EXTENSIONS = set(['mp4','webm','mkv','avi'])
            UPLOAD_FOLDER = 'static/uploads/cours/video'
        elif att_type == 'document':
            ALLOWED_EXTENSIONS = set(['doc','ppt','pdf','zip','rar'])
            UPLOAD_FOLDER = 'static/uploads/cours/document'
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filedir = UPLOAD_FOLDER+"/"+filename
        cursor.execute('''INSERT INTO Attachment(IdCour, Title, type, Pwd)
                            VALUES('{id}','{title}','{att_type}','{pwd}')
                        '''.format(id=id,title=title,att_type=att_type,pwd=filedir))
        connection.commit()
    return render_template("coach/cours.html",info=info,cour_video=cour_video,cour_doc=cour_doc)

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("log",False)
    return redirect('login')

@app.route('/logout-coach')
def logout_coach():
    session.pop("coach",None)
    session.pop("log",False)
    return redirect('login')

def Check_log():
    global log
    log = False
    if "log" in session:
        log = session["log"]
    return log

def Check_authentification():
    return cursor.execute('''SELECT EXISTS(SELECT * FROM CheckUser WHERE IdLog=?)''',[cursor.execute("SELECT IdLog FROM User WHERE IdUser=?",[session["user"]]).fetchone()[0]]).fetchone()[0]


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

def Get_Account_Type():
    coach = session.get("coach")
    user = session.get("user")
    if(coach == "admin" or user == "admin"):
        return "admin"
    elif coach is not None:
        return "coach"
    elif user is not None:
        return "user"
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
    connection.close()
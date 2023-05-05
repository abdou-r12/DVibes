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
import datetime
from werkzeug.utils import secure_filename
from datetime import date
from Functions import *
from DB import *

app = Flask(__name__)
app.secret_key = get_random_string(64)
print("secret key : ",app.secret_key,"\n")
connection = sqlite3.connect('DVibes.db', check_same_thread=False)
cursor = connection.cursor()
Create_tables(cursor)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# home page
@app.route("/")
def index():
    info = None
    if session.get("user") != None:
        info = cursor.execute("SELECT FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchone()[0]
    elif session.get("coach") != None:
        info = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        info = "admin"
    news = cursor.execute("SELECT * FROM News LIMIT 10").fetchall()
    coaches = cursor.execute("SELECT * FROM Coach LIMIT 3").fetchall()
    return render_template("home/index.html",log=session.get("log"),info=info,data=news,coaches=coaches)

# about us
@app.route('/about-us')
def about_us():
    info = None
    if session.get("user") != None:
        info = cursor.execute("SELECT FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchone()[0]
    elif session.get("coach") != None:
        info = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        info = "admin"
    return render_template("home/about-us.html",log=session.get("log"),info=info)

#view coaches list
@app.route('/coaches')
def coaches_list():
    info = None
    if session.get("user") != None:
        info = cursor.execute("SELECT FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchone()[0]
    elif session.get("coach") != None:
        info = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        info = "admin"
    coaches_list = cursor.execute("SELECT * FROM Coach").fetchall()
    return render_template("home/coaches-list.html",info=info,coaches_list=coaches_list)

# coach search
@app.route('/coaches/search:<name>')
def coach_search(name):
    info = None
    if session.get("user") != None:
        info = cursor.execute("SELECT FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchone()[0]
    elif session.get("coach") != None:
        info = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        info = "admin"
    query = "SELECT * FROM Coach WHERE FullName LIKE '%" + name + "%'"
    if cursor.execute("SELECT EXISTS({query})".format(query=query)).fetchone()[0] == True:
        coaches_list = cursor.execute(query).fetchall()
    else:
        coaches_list = []
    return render_template("home/coaches-list.html",info=info,coaches_list=coaches_list)

# view coach
@app.route('/coaches:<id>')
def coach_view(id):
    info = None
    if session.get("user") != None:
        info = cursor.execute("SELECT FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchone()[0]
    elif session.get("coach") != None:
        info = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        info = "admin"
    coach_info = cursor.execute("SELECT * FROM Coach WHERE IdCoach=?",[id]).fetchall()[0]
    coach_course = cursor.execute("SELECT * FROM Cours WHERE IdCoach=?",[id]).fetchall()
    coach_location = cursor.execute("SELECT * FROM CoachMap WHERE IdCoach=?",[id]).fetchall()
    coach_feed = cursor.execute("SELECT * FROM CoachFeed WHERE IdCoach=? ORDER BY IdFeed DESC",[id]).fetchall()
    return render_template("home/coach-view.html",info=info,coach_info=coach_info
                           ,coach_course=coach_course,coach_location=coach_location,
                           coach_feed=coach_feed,log=session.get("log"))

# show all the events
@app.route("/events")
def events():
    info = None
    if session.get("user") != None:
        info = cursor.execute("SELECT FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchone()[0]
    elif session.get("coach") != None:
        info = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        info = "admin"
    data = cursor.execute('SELECT * FROM Events').fetchall()
    return render_template("home/events.html",data=data,log=session.get("log"),info=info)

# show one detailed event
@app.route("/event:<id>")
def show_event(id):
    info = None
    if session.get("user") != None:
        info = cursor.execute("SELECT FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchone()[0]
    elif session.get("coach") != None:
        info = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        info = "admin"
    data = cursor.execute("SELECT * FROM Events WHERE IdEvent=?",[id]).fetchone()
    return render_template("home/show-event.html",data=data,log=session.get("log"),info=info)

# show all the news
@app.route("/news")
def news():
    info = None
    if session.get("user") != None:
        info = cursor.execute("SELECT FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchone()[0]
    elif session.get("coach") != None:
        info = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        info = "admin"
    data = cursor.execute('SELECT * FROM News').fetchall()
    return render_template("home/news.html",data=data,log=session.get("log"),info=info)

# show one detailed news
@app.route("/news:<id>")
def show_new(id):
    info = None
    if session.get("user") != None:
        info = cursor.execute("SELECT FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchone()[0]
    elif session.get("coach") != None:
        info = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        info = "admin"
    data = cursor.execute("SELECT * FROM News WHERE IdNew=?",[id]).fetchone()
    print(data)
    print(id)
    return render_template("home/show-new.html",data=data,log=session.get("log"),info=info)

# sing up page
@app.route("/singup",methods = ['GET' , 'POST'])
def singup():
    if session.get("log")==True:
        return redirect(url_for("login"))
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
            cursor.execute('''INSERT INTO Login(UserName, PassCode)VALUES('{}','{}')'''.format(email,password))
            iD = cursor.execute("SELECT IdLog FROM Login WHERE UserName = ?",[email]).fetchone()[0]
            cursor.execute('''INSERT INTO User(IdLog, FullName, pfp, Gender, BirthDay, Location, Experience, Interests, Phone, SocialMedia, Balance)
                            VALUES('{id}','{fullname}','{pfp}','{gender}','{bd}','{extra}','{extra}','{extra}','{extra}','{extra}','{bal}')
                        '''.format(id=iD,fullname=fullname,pfp='',gender=gender,bd=bday,extra='',bal='0'))

            cursor.execute('''INSERT INTO CheckUser(IdLog,Code)
                            VALUES('{id}','{tsc}')'''.format(id=iD,tsc=twostepcheck(email)))
            connection.commit()
            id = cursor.execute("SELECT IdUser FROM User WHERE IdLog=?",[iD]).fetchone()[0]
            session['user'] = id
            session['log'] = True
            return redirect(url_for('user_check'))
    return render_template("register/singup.html")

# ask to be a coach
@app.route('/becoach',methods = ['GET' , 'POST'])
def be_coach():
    if session.get("log")==True:
        return redirect(url_for("login"))
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

# user and coach login
@app.route('/login',methods = ['GET' , 'POST'])
def login():
    if session.get("log")==True:
        if session.get("user") != None:
            return redirect(url_for('user'))
        elif session.get("coach") != None:
            return redirect(url_for("coach"))
    if request.method == "POST":
        user_username = request.form['user_username']
        user_password = request.form["user_password"]
        coach_username = request.form['coach_username']
        coach_password = request.form["coach_password"]
        if (coach_username == "" and coach_password == ""):
            if(cursor.execute("SELECT EXISTS(SELECT * FROM Login WHERE UserName = ?)",[user_username]).fetchone()[0]==0):
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
            if(cursor.execute("SELECT EXISTS(SELECT * FROM LoginCoach WHERE UserName = ?)",[coach_username]).fetchone()[0]==0):
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
    return render_template('register/login.html')

# user main
@app.route('/user')
def user():
    if session.get("log")!=True or session.get("user")==None:
        return redirect(url_for("login"))
    elif (Check_authentification()==1):
        return redirect(url_for('user_check'))
    user_name = cursor.execute("SELECT FullName FROM User WHERE IdLog=?",[session.get("user")]).fetchone()[0]
    return render_template("user/usermain.html",user_name=user_name)

# athautification page for user
@app.route('/user-check',methods = ['GET' , 'POST'])
def user_check():
    if session.get("log") != True and Check_authentification() != True:
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
@app.route('/user/profile', methods=['GET', 'POST'])
def userprofile():
    if session.get("log") != True or session.get("user") == None:
        return redirect(url_for('login'))
    elif Check_authentification() == 1:
        return redirect(url_for('user_check'))
    data = cursor.execute("SELECT * FROM User WHERE IdUser=?", [session.get("user")]).fetchone()
    email = cursor.execute("SELECT UserName FROM Login WHERE IdLog=?", [data[1]]).fetchone()[0]
    if request.method == "POST":
        location = request.form.get("location")
        experience = request.form.get("experience")
        interests = request.form.get("interests")
        username = request.form.get("username")
        new_email = request.form.get("email")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        title = request.form.get("title")
        rapport_text = request.form.get("raport_text")
        if username is not None and username.strip():
            cursor.execute("UPDATE User SET FullName=? WHERE IdUser=?", [username.strip(), session.get("user")])
        if location is not None and location.strip():
            cursor.execute("UPDATE User SET Location=? WHERE IdUser=?", [location, session.get("user")])
        if experience is not None and experience.strip():
            cursor.execute("UPDATE User SET Experience=? WHERE IdUser=?", [experience, session.get("user")])
        if interests is not None and interests.strip():
            cursor.execute("UPDATE User SET Interests=? WHERE IdUser=?", [interests, session.get("user")])
        if (title is not None and title.strip() ) and (rapport_text is not None and rapport_text.strip()):
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO Rapports (IdUser, Title, RapportText, Date) VALUES (?, ?, ?, ?)", [session.get("user"), title, rapport_text, current_time])
        if (old_password is not None and old_password.strip() ) and (new_password is not None and new_password.strip()):
            user_data = cursor.execute("SELECT * FROM Login WHERE IdLog=?", [data[1]]).fetchone()
            if user_data[2] == old_password:
                cursor.execute("UPDATE Login SET PassCode=? WHERE IdLog=?", [new_password, data[1]])
                flash("Password updated successfully","success")
            else:
                flash("Invalid old password","error")
        connection.commit()
        return redirect(url_for("userprofile"))
    return render_template("user/profile.html", data=data, email=email)

# user profile picture
@app.route('/user/profile/change-profile-picture',methods=["POST","GET"])
def change_pfp():
    if session.get("log") != True or session.get("user") == None:
        return redirect(url_for('login'))
    elif Check_authentification() == 1:
        return redirect(url_for('user_check'))
    user_info = cursor.execute("SELECT FullName,Pfp FROM User WHERE IdUser=?", [session.get("user")]).fetchall()[0]
    if request.method == "POST":
            UPLOAD_FOLDER = 'static/uploads/user/profile'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            file = request.files['file']
            ALLOWED_EXTENSIONS = set(['bmp','svg','png', 'jpg', 'jpeg'])
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filedir = app.config['UPLOAD_FOLDER']+"/"+filename
            cursor.execute("UPDATE User SET Pfp = ? WHERE IdUser = ?",[filedir,session.get("user")])
            connection.commit()
            flash("Profile picture added successfully","success")
            return redirect(url_for("userprofile"))
    return render_template("user/change-pfp.html",user_info=user_info)

# show all course available for user
@app.route('/user/cours')
def check_courses():
    user = None
    if session.get("user") != None:
        user = cursor.execute("SELECT FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchone()[0]
    elif session.get("coach") != None:
        user = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        user = "admin"
    cours = cursor.execute("SELECT Cours.* , Coach.FullName As CoachName From Cours JOIN Coach ON Cours.IdCoach = Coach.IdCoach").fetchall()
    return render_template("user/cours.html",cours=cours,user=user,log=session.get("log"))

# search course by title
@app.route('/user/cours/search-title:<title>')
def search_course_title(title):
    user = None
    if session.get("user") != None:
        user = cursor.execute("SELECT FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchone()[0]
    elif session.get("coach") != None:
        user = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        user = "admin"
    query = "SELECT Cours.*, Coach.FullName FROM Cours JOIN Coach ON Cours.IdCoach = Coach.IdCoach WHERE Cours.Title LIKE '%" + title + "%'"
    if cursor.execute("SELECT EXISTS({query})".format(query=query)).fetchone()[0] == True:
        courses = cursor.execute(query).fetchall()
    else:
        courses = []
    return  render_template("/user/course-search.html",courses=courses,user=user)

# search course by title
@app.route('/user/cours/search-category:<category>')
def search_course_category(category):
    user = None
    if session.get("user") != None:
        user = cursor.execute("SELECT FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchone()[0]
    elif session.get("coach") != None:
        user = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        user = "admin"
    query = "SELECT Cours.*, Coach.FullName FROM Cours JOIN Coach ON Cours.IdCoach = Coach.IdCoach WHERE Cours.Type LIKE '%" + category + "%'"
    if cursor.execute("SELECT EXISTS({query})".format(query=query)).fetchone()[0] == True:
        courses = cursor.execute(query).fetchall()
    else:
        courses = []
    return  render_template("/user/course-search.html",courses=courses,user=user)

# show detail of one course
@app.route('/user/cours/overview:<id>')
def over_view_course(id):
    user = None
    if session.get("user") != None:
        user = cursor.execute("SELECT IdUser,FullName FROM User WHERE IdUser = ?",[session.get("user")]).fetchall()[0]
    elif session.get("coach") != None:
        user = cursor.execute("SELECT FullName FROM Coach WHERE IdCoach = ?",[session.get("coach")]).fetchone()[0]
    elif session.get("admin") == True:
        user = "admin"
    cour_info = cursor.execute("SELECT * FROM Cours WHERE IdCour=?",[id]).fetchone()
    return render_template("user/over-view.html",cour_info=cour_info,user=user,log=session.get("log"))

# purchase function
@app.route('/user/cours/<id_user>-purchase:<id_course>')
def purchase(id_user,id_course):
    if session.get("log") != True or session.get("user") == None:
        return redirect(url_for('login'))
    elif (Check_authentification()==1):
        return redirect(url_for('user_check'))
    user_balance = cursor.execute("SELECT Balance FROM User WHERE IdUser=?",[id_user]).fetchone()[0]
    course_info = cursor.execute("SELECT IdCoach,Price FROM Cours WHERE IdCour=?",[id_course]).fetchall()[0]
    if(user_balance >= course_info[1]):
        cursor.execute("INSERT INTO Purchase(IdUser, IdCour, Date) VALUES('{id_user}','{id_course}','{date}')".format(id_user=id_user,id_course=id_course,date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
))
        cursor.execute("UPDATE User SET Balance = Balance - ? WHERE IdUser=?",[course_info[1],id_user])
        cursor.execute("UPDATE Coach SET Balance = Balance + ? WHERE IdCoach = ?",[course_info[1]-(course_info[1]*0.25),course_info[0]])
        cursor.execute("UPDATE DBalance SET Coin = {coin}".format(coin=+course_info[1]*0.25))
        connection.commit()
        return redirect(url_for('my_courses'))
    else:
        return redirect(url_for("my_wallet"))

# Show owned courses
@app.route('/user/mycourses')
def my_courses():
    if session.get("log") != True or session.get("user") == None:
        return redirect(url_for('login'))
    elif (Check_authentification()==1):
        return redirect(url_for('user_check'))
    user_info = cursor.execute("SELECT FullName FROM User WHERE IdLog=?",[session.get("user")]).fetchone()[0]
    courses = cursor.execute('''
        SELECT Purchase.*, Cours.*
        FROM Purchase
        JOIN Cours ON Purchase.IdCour = Cours.IdCour
        WHERE Purchase.IdUser = ?
    ''',[session.get("user")]).fetchall()
    return render_template("user/my-courses.html",courses=courses,user_info=user_info)

# show detail about owned course
@app.route('/user/mycourses/<id>')
def course_preview(id):
    if session.get("log") != True or session.get("user") == None:
        return redirect(url_for('login'))
    elif (Check_authentification()==1):
        return redirect(url_for('user_check'))
    user_info = cursor.execute("SELECT FullName FROM User WHERE IdLog=?",[session.get("user")]).fetchone()[0]
    if cursor.execute("SELECT EXISTS(SELECT * FROM Purchase WHERE IdUser=? and IdCour=?)",[session.get("user"),id]).fetchone()[0] == True:
        course = cursor.execute('''
            SELECT Cours.*, Coach.FullName AS CoachName
            FROM Cours
            INNER JOIN Coach ON Cours.IdCoach = Coach.IdCoach
            WHERE IdCour=?
        ''',[id]).fetchall()[0]
        document = cursor.execute("SELECT Title,Pwd FROM Attachment WHERE IdCour=? and Type='document'",[id]).fetchall()
        video = cursor.execute("SELECT * FROM Attachment WHERE IdCour=? and Type='video'",[id]).fetchall()
    else:
        redirect("/user/cours/overview:{id}".format(id=id))
    return render_template("user/course-preview.html",course=course,document=document,video=video,user_info=user_info)

# Video show
@app.route('/user/mycourses/<id_course>/<id_video>')
def video_show(id_course,id_video):
    if session.get("log") != True or session.get("user") == None:
        return redirect(url_for('login'))
    elif (Check_authentification()==1):
        return redirect(url_for('user_check'))
    user_info = cursor.execute("SELECT FullName FROM User WHERE IdLog=?",[session.get("user")]).fetchone()[0]
    if cursor.execute("SELECT EXISTS(SELECT * FROM Purchase WHERE IdUser=? and IdCour=?)",[session.get("user"),id_course]).fetchone()[0] == True:
        video = cursor.execute("SELECT IdCour,Title,Pwd FROM Attachment WHERE IdAtt = ?",[id_video]).fetchone()
        video_list = cursor.execute("SELECT IdAtt,Title FROM Attachment WHERE IdCour = ? AND Type='video'",[id_course]).fetchall()
    return render_template("user/course-video.html",user_info=user_info,video=video,video_list=video_list)

# Balance manager
@app.route('/user/mywallet',methods=['POST','GET'])
def my_wallet():
    if session.get("log") != True or session.get("user") == None:
        return redirect(url_for('login'))
    elif (Check_authentification()==1):
        return redirect(url_for('user_check'))
    user_info = cursor.execute("SELECT IdUser,FullName,Balance FROM User WHERE IdUser=?",[session.get('user')]).fetchall()[0]
    purchases = cursor.execute('''
        SELECT Purchase.IdPur, Purchase.Date, Cours.Title, Cours.Price
        FROM Purchase
        INNER JOIN Cours ON Purchase.IdCour = Cours.IdCour
        WHERE Purchase.IdUser = ?;
    ''',[session.get("user")]).fetchall()
    requests = cursor.execute("SELECT * FROM Bill WHERE IdUser = ? ORDER BY IdBil DESC",[session.get("user")]).fetchall()
    if request.method == "POST":
            UPLOAD_FOLDER = 'static/uploads/user/bill'
            ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filedir = app.config['UPLOAD_FOLDER']+"/"+filename
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''INSERT INTO Bill (IdUser, Status, Note, Date,Pwd)
                VALUES (?,?,?,?,?)''',[session.get("user"),"Pending","-",date,filedir])
            connection.commit()
            flash("Submit successfully")
    return render_template("user/my-wallet.html",user_info=user_info,purchases=purchases,requests=requests)

# admin login
@app.route('/login-admin', methods=['GET', 'POST'])
def login_admin():
    if session.get("log") is True or session.get("admin") is True or session.get("coach") is not None or session.get("user") is not None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "admin":
            session["admin"] = True
            session["log"] = True
            return redirect(url_for("admin"))
        else:
            flash("Wrong username or password")
    return render_template("admin/login.html")

# admin main
@app.route('/admin')
def admin():
    if session.get("log") == True and session.get("admin") == True:
        return render_template("admin/adminmain.html")
    else:
        return redirect(url_for('login'))

# news manager page
@app.route('/admin/news-manager',methods = ['POST','GET'])
def news_manager():
    if session.get("log") == True and session.get("admin") == True:
        data = cursor.execute('SELECT * FROM News ORDER BY IdNew DESC').fetchall()
        heading = ('ID','Title','Description','Content','Picture','Date')
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
                            VALUES(?,?,?,?,?)
                        ''',[title,disc,text,filedir,date.today()])
            connection.commit()
    else:
        return redirect(url_for('login'))
    return render_template("admin/news-manager.html",heading=heading,data=data)

# edit news function
@app.route('/admin/news-manager/edit:<id>',methods = ['POST','GET'])
def edit_news(id):
    if session.get("log") == True and session.get("admin") == True:
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
            flash("News updated successfully")
            return redirect(url_for("news_manager"))
    else:
        return redirect(url_for('login'))
    return render_template("admin/edit-news.html",data=data)

# remove news function
@app.route('/admin/news-manager/remove:<id>')
def remove_news(id):
    if session.get("log") == True and session.get("admin") == True:
        Remove_News(id)
    else:
        return redirect(url_for('login'))
    return redirect(url_for('news_manager'))

# events manager page
@app.route('/admin/events-manager',methods = ['POST','GET'])
def events_manager():
    if session.get("log") == True and session.get("admin") == True:
        data = cursor.execute('SELECT * FROM Events ORDER BY IdEvent DESC').fetchall()
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
                                VALUES(?,?,?,?,?)
                        ''',[title,disc,text,filedir,date.today()])
            connection.commit()
    else:
        return redirect(url_for('login'))
    return render_template("admin/events-manager.html",data=data,heading=heading)

# edit event function
@app.route('/admin/events-manager/edit:<id>',methods = ['POST','GET'])
def edit_events(id):
    if session.get("log") == True and session.get("admin") == True:
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
            flash("Event updated successfully")
            return redirect(url_for("events_manager"))
    else:
        return redirect(url_for('login'))
    return render_template("admin/edit-events.html",data=data)

# remove event function
@app.route('/admin/events-manager/remove:<id>')
def remove_event(id):
    if session.get("log") == True and session.get("admin") == True:
        Remove_Events(id)
    else:
        flash("Event removed successfully")
        return redirect(url_for('events_manager'))
    return redirect(url_for('events_manager'))

# coach manager page
@app.route('/admin/coach-requests',methods = ['POST','GET'])
def add_coach():
    if session.get("log") == True and session.get("admin") == True:
        coach = cursor.execute('SELECT * FROM Coach').fetchall()
        requests = cursor.execute('select * from Request').fetchall()
        heading_coach = ('ID','Title','Description','Content','Picture','Date')
        heading_req = ('id','full name','gender','birthday','email','resume','cv')
    else:
        return redirect(url_for('login'))
    return render_template('admin/coach-requests.html',heading_coach=heading_coach,heading_req=heading_req,coach=coach,requests=requests)

# accept request to be coach page
@app.route("/admin/coach-requests/remove:<id>")
def Remove_coach(id):
    if session.get("log") == True and session.get("admin") == True:
        Remove_Coach_Req(id)
    else:
        return redirect(url_for('login'))
    return redirect(url_for('add_coach'))

# remove request to be coach page
@app.route("/admin/coach-requests/accept:<id>")
def accept_coach(id):
    if session.get("log") == True and session.get("admin") == True:
        info = cursor.execute("SELECT * FROM Request WHERE IdReq=?",[id]).fetchone()
        cursor.execute('''INSERT INTO LoginCoach(UserName, PassCode)
                            VALUES('{email}','{password}')
                    '''.format(email=info[4],password=get_random_string(8)))
        iD = cursor.execute("SELECT IdLog FROM LoginCoach WHERE UserName = '{email}'".format(email=info[4])).fetchone()[0]
        cursor.execute('''INSERT INTO Coach(IdLog, FullName, pfp, Gender, BirthDay,Balance)
                            VALUES('{id}','{fullname}','{pfp}','{gender}','{bd}','{bal}')
                    '''.format(id=iD,fullname=info[1],pfp=None,gender=info[2],bd=info[3],bal=0))
        cursor.execute("DELETE FROM Request WHERE IdReq=?",[id])
        connection.commit()
        return redirect(url_for('add_coach'))
    else:
        return redirect(url_for('login'))

# coach list
@app.route('/admin/coach-manager')
def coachs():
    if session.get("log") == True and session.get("admin") == True:
        data = cursor.execute("SELECT * FROM Coach").fetchall()
        heading_coach = ("ID","Full Name","Gender","BirthDay","Profile picture")
    else:
        return redirect(url_for('login'))
    return render_template("admin/coach-manager.html",data=data,heading_coach=heading_coach)

# remove coach
@app.route('/admin/coach-manager/remove:<id>')
def remove_coach(id):
    if session.get("log") == True and session.get("admin") == False:
        Remove_coach(id)
    else:
        return redirect(url_for('login'))
    return redirect(url_for('coach-manager'))

# courses reports
@app.route('/admin/course-manager')
def course_manager():
    if session.get("log") == True and session.get("admin") == True:
        heading = ("ID","Coach ID","Title","Type","Description","Price","Cover")
        course = cursor.execute("SELECT * FROM Cours").fetchall()
    else:
        return redirect(url_for('login'))
    return render_template("admin/course-manager.html",course=course,heading=heading)

# balances and statics
@app.route('/admin/payment-manager',methods = ['POST','GET'])
def payment_manager():
    if session.get("log") == True and session.get("admin") == True:
        balance = cursor.execute("SELECT * FROM DBalance").fetchone()[0]
        purchase_number = cursor.execute("SELECT COUNT(*) FROM Purchase").fetchone()[0]
        total_budget = (cursor.execute("SELECT SUM(Balance) FROM User").fetchone()[0])+(cursor.execute("SELECT SUM(Balance) FROM Coach").fetchone()[0])
        cashier = cursor.execute("SELECT * FROM LoginCashier").fetchall()
        user_info = cursor.execute('''
        SELECT User.FullName, User.Balance, Login.UserName
        FROM User
        JOIN Login ON User.IdLog = Login.IdLog
        ''').fetchall()
        if request.method == "POST":
            name = request.form["name"]
            username = request.form["username"]
            password = request.form["password"]
            cursor.execute("INSERT INTO LoginCashier (UserName, PassCode, FullName) VALUES (?, ?, ?)", (username, password, name))
            connection.commit()
    else:
        return redirect(url_for('login'))
    return render_template("admin/payment-manager.html",balance=balance,purchase_number=purchase_number,total_budget=total_budget,cashier=cashier,user_info=user_info)

# cashier login
@app.route('/login-cashier', methods=['GET', 'POST'])
def login_cashier():
    if session.get("log") == True and session.get("cashier") != None:
        return redirect(url_for("cashier"))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_info = cursor.execute("SELECT * FROM LoginCashier WHERE UserName = ? AND PassCode = ?",[username,password]).fetchone()
        if user_info is not None:
            if (user_info[1]==username and user_info[2]==password):
                session["cashier"] = user_info[0]
                session["log"] = True
                return redirect(url_for("cashier"))
            else:
                flash("Wrong username or password")
        else:
            flash("Invalid username or password")

    return render_template('cashier/login.html')

# cashier page
@app.route('/cashier',methods=["GET", "POST"])
def cashier():
    if session.get("log") == False or session.get("cashier") == None:
        return redirect(url_for("login_cashier"))
    bill_pending = cursor.execute('''
        SELECT Bill.*, User.FullName, User.Balance, Login.UserName
        FROM Bill
        JOIN User ON Bill.IdUser = User.IdUser
        JOIN Login ON User.IdLog = Login.IdLog
        WHERE Bill.Status = 'Pending'
    ''').fetchall()
    bill_done = cursor.execute('''
        SELECT Bill.*, User.FullName, User.Phone, User.Balance, Login.UserName
        FROM Bill
        JOIN User ON Bill.IdUser = User.IdUser
        JOIN Login ON User.IdLog = Login.IdLog
        WHERE Bill.Status != 'Pending'
    ''').fetchall()
    coach_pending = cursor.execute('''
        SELECT CoachPayment.*, Coach.FullName, Coach.Balance, LoginCoach.UserName
        FROM CoachPayment
        JOIN Coach ON CoachPayment.IdCoach = Coach.IdCoach
        JOIN LoginCoach ON Coach.IdLog = LoginCoach.IdLog
        WHERE CoachPayment.Status = 'Pending'
    ''').fetchall()
    coach_done = cursor.execute('''
        SELECT CoachPayment.*, Coach.FullName, Coach.Balance, LoginCoach.UserName
        FROM CoachPayment
        JOIN Coach ON CoachPayment.IdCoach = Coach.IdCoach
        JOIN LoginCoach ON Coach.IdLog = LoginCoach.IdLog
        WHERE CoachPayment.Status != 'Pending'
    ''').fetchall()
    return render_template("cashier/cashier.html",bill_pending=bill_pending,
                           bill_done=bill_done,cashier=session.get("cashier"),
                           coach_pending=coach_pending,coach_done=coach_done)

# process coach request
@app.route('/cashier/coach-payment:<id>',methods=["POST","GET"])
def coach_payment(id):
    if session.get("log") == False or session.get("cashier") == None:
        return redirect(url_for("login_cashier"))
    coach_req = cursor.execute('''
        SELECT CoachPayment.*, Coach.FullName, Coach.Balance, LoginCoach.UserName
        FROM CoachPayment
        JOIN Coach ON CoachPayment.IdCoach = Coach.IdCoach
        JOIN LoginCoach ON Coach.IdLog = LoginCoach.IdLog
        WHERE CoachPayment.IdCP = ?
    ''',[id]).fetchone()
    if request.method == "POST":
        note = request.form['note']
        cursor.execute("UPDATE CoachPayment SET Status=?,Note=?,Date=? WHERE IdCP=?",['Rejected',note,datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),id])
        connection.commit()
        return redirect(url_for("cashier"))
    return render_template("cashier/coach-payment.html",coach_req=coach_req)

# accept coach request payment
@app.route('/cashier/coach-payment/accept:<IdCP><IdCoach>')
def coach_payment_accept(IdCP,IdCoach):
    if session.get("log") == False or session.get("cashier") == None:
        return redirect(url_for("login_cashier"))
    cursor.execute("UPDATE CoachPayment SET Status=?,Date=? WHERE IdCP=?",["Accepted",datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),IdCP])
    cursor.execute("UPDATE Coach SET Balance = 0 WHERE IdCoach=?",[IdCoach])
    connection.commit()
    return redirect(url_for("cashier"))

# process user request
@app.route('/cashier/add-credit:<id>',methods=["POST","GET"])
def add_credit(id):
    if session.get("log") == False or session.get("cashier") == None:
        return redirect(url_for("login_cashier"))
    bill = cursor.execute("""
        SELECT Bill.*, User.FullName, User.Phone, User.Balance, Login.UserName
        FROM Bill
        JOIN User ON Bill.IdUser = User.IdUser
        JOIN Login ON User.IdLog = Login.IdLog
        WHERE Bill.IdBil = ?
    """,[id]).fetchone()
    if request.method == "POST":
        value = request.form["add"]
        note = request.form["note"]
        if value == "" and note == "":
            flash("Invalid operation")
        elif value == "":
            cursor.execute("UPDATE Bill SET Status=?, Note=? WHERE IdBil=? ",['Rejected',note,id])
            cursor.execute("INSERT INTO TRHistory(IdUser,IdLog,Send_Date,Receive_Date,Note) VALUES(?,?,?,?,?)",[bill[1],session.get("cashier"),bill[4],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'Rejected'])
            connection.commit()
            return redirect(url_for("cashier"))
        elif note == "":
            cursor.execute("UPDATE User SET Balance= Balance + ? WHERE IdUser = ?",[value,bill[1]])
            cursor.execute("UPDATE Bill SET Status = 'Accepted' WHERE IdBil = ?",[bill[0]])
            cursor.execute("INSERT INTO TRHistory(IdUser,IdLog,Send_Date,Receive_Date,Note) VALUES(?,?,?,?,?)",[bill[1],session.get("cashier"),bill[4],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'Accepted'])
            connection.commit()
            return redirect(url_for("cashier"))
    return render_template("cashier/add-credit.html",bill=bill,cashier=session.get("cashier"))

# coach page
@app.route("/coach")
def coach():
    if session.get("log") == False or session.get("coach") == None:
        return redirect(url_for('login'))
    name = cursor.execute("SELECT FullName FROM Coach WHERE IdLog = ?",[session.get("coach")]).fetchone()[0]
    return render_template("coach/coachmain.html",name=name)

# coach profile
@app.route('/coach/profile', methods=['GET', 'POST'])
def coach_profile():
    if session.get("log") != True or session.get("coach") == None:
        return redirect(url_for('login'))
    data = cursor.execute("SELECT * FROM Coach WHERE IdCoach=?", [session.get("coach")]).fetchone()
    email = cursor.execute("SELECT UserName FROM LoginCoach WHERE IdLog=?", [data[1]]).fetchone()[0]
    if request.method == "POST":
        username = request.form.get("username")
        new_email = request.form.get("email")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        title = request.form.get("title")
        rapport_text = request.form.get("raport_text")
        if username is not None and username.strip():
            cursor.execute("UPDATE Coach SET FullName=? WHERE IdCoach=?", [username.strip(), session.get("coach")])
        if (title is not None and title.strip() ) and (rapport_text is not None and rapport_text.strip()):
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO Rapports (IdUser, Title, RapportText, Date) VALUES (?, ?, ?, ?)", [session.get("coach"), title, rapport_text, current_time])
        if (old_password is not None and old_password.strip() ) and (new_password is not None and new_password.strip()):
            user_data = cursor.execute("SELECT * FROM LoginCoach WHERE IdLog=?", [data[1]]).fetchone()
            if user_data[2] == old_password:
                cursor.execute("UPDATE LoginCoach SET PassCode=? WHERE IdLog=?", [new_password, data[1]])
                flash("Password updated successfully","success")
            else:
                flash("Invalid old password","error")
        connection.commit()
    return render_template("coach/profile.html", data=data, email=email)

# coach profile picture
@app.route('/coach/profile/change-profile-picture',methods=["POST","GET"])
def change_pfp_coach():
    if session.get("log") != True or session.get("coach") == None:
        return redirect(url_for('login'))
    user_info = cursor.execute("SELECT FullName,Pfp FROM Coach WHERE IdCoach=?", [session.get("coach")]).fetchall()[0]
    if request.method == "POST":
            UPLOAD_FOLDER = 'static/uploads/coach/profile'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            file = request.files['file']
            ALLOWED_EXTENSIONS = set(['bmp','svg','png', 'jpg', 'jpeg'])
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filedir = app.config['UPLOAD_FOLDER']+"/"+filename
            cursor.execute("UPDATE Coach SET Pfp = ? WHERE IdCoach = ?",[filedir,session.get("coach")])
            connection.commit()
            flash("Profile picture added successfully","success")
            return redirect(url_for("coach_profile"))
    return render_template("user/change-pfp.html",user_info=user_info)

# cours manager page
@app.route("/coach/cours-manager",methods = ['POST','GET'])
def cours_manager():
    if session.get("log") == False or session.get("coach") == None:
        return redirect(url_for('login'))
    data = cursor.execute('SELECT * FROM Cours WHERE IdCoach = ?',[session.get("coach")]).fetchall()
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
        filedir = UPLOAD_FOLDER+"/"+filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cursor.execute('''INSERT INTO Cours(IdCoach, Title, Type, Price, Description,Pwd)
                            VALUES('{id}','{title}','{courstype}','{price}','{Description}','{pwd}')
                        '''.format(id=session.get("coach"),title=title,courstype=courstype,price=price,Description=Description,pwd=filedir))
        connection.commit()
        flash(title," added successfully")
        return redirect(url_for("cours_manager"))
    return render_template("coach/cours-manager-c.html",data=data)

# edit course attachment
@app.route('/coach/cours-manager/<id>',methods = ['POST','GET'])
def cours(id):
    if session.get("log") == False or session.get("coach") == None:
        return redirect(url_for('login'))
    info = cursor.execute("SELECT * FROM Cours WHERE IdCour={id_cour} AND IdCoach={id_coach}".format(id_cour=id,id_coach=session.get("coach"))).fetchone()
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
            ALLOWED_EXTENSIONS = set(['doc','ppt','pdf','zip','rar','png','jpeg','svg'])
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
        flash("Attachment added successfully")
        return redirect("/coach/cours-manager/{}".format(id))
    return render_template("coach/cours.html",info=info,cour_video=cour_video,cour_doc=cour_doc)

# delete video
@app.route('/couch/cours-manager/delete:<idcour>-<idatt>')
def delete_attachment(idcour,idatt):
    if session.get("log") == False or session.get("coach") == None:
        return redirect(url_for('login'))
    cursor.execute("DELETE FROM Attachment WHERE IdAtt = ?",[idatt])
    connection.commit()
    return redirect("/coach/cours-manager/{}".format(idcour))

# coach wallet
@app.route('/coach/mywallet',methods=["POST","GET"])
def c_my_wallet():
    if session.get("log") is False or session.get("coach") is None:
        return redirect(url_for("login"))
    balance = cursor.execute("SELECT Balance FROM Coach WHERE IdCOach = ?",[session.get("coach")]).fetchone()[0]
    total = cursor.execute('''
        SELECT COUNT(*) AS NumPurchases
        FROM Purchase p
        INNER JOIN Cours c ON p.IdCour = c.IdCour
        INNER JOIN Coach co ON c.IdCoach = co.IdCoach
        WHERE co.IdCoach = ?
    ''',[session.get("coach")]).fetchone()[0]
    payment_req = cursor.execute("SELECT * FROM CoachPayment WHERE IdCoach=? ORDER BY IdCP DESC",[session.get("coach")]).fetchall()
    if request.method == "POST":
        ccp = request.form["ccp"]
        cursor.execute('''INSERT INTO CoachPayment(IdCoach,Date,Status,CCP,Note)
        values(?,?,?,?,?)''',[session.get("coach"),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Pending",ccp,"-"])
        connection.commit()
        flash("Request submitted successfully")
    return render_template("coach/mywallet.html",balance=balance,total=total,payment_req=payment_req)

# Mentor Map
@app.route('/coach/mentor-map',methods=["POST","GET"])
def mentor_map():
    if session.get("log") == False or session.get("coach") == None:
        return redirect(url_for('login'))
    locations = cursor.execute("SELECT * FROM CoachMap WHERE IdCoach = ?",[session.get("coach")]).fetchall()
    if request.method == "POST":
        location = request.form["location"]
        locationlink = request.form["locationlink"]
        note = request.form["note"]
        cursor.execute('''INSERT INTO CoachMap(IdCoach,Location,LocationLink,Note)
        values(?,?,?,?)''',[session.get("coach"),location,locationlink,note])
        connection.commit()
        flash("Location added successfully")
        return redirect(url_for("mentor_map"))
    return render_template("coach/mentor-map.html",locations=locations)

# Delete location
@app.route('/coach/mentor-map/delete:<id>')
def delete_map(id):
    if session.get("log") == False or session.get("coach") == None:
        return redirect(url_for('login'))
    if cursor.execute("SELECT EXISTS(SELECT * FROM CoachMap WHERE IdCoach = ?)",[session.get("coach")]) == False:
        return redirect(url_for("login"))
    cursor.execute("DELETE FROM CoachMap WHERE IdMap=?",[id])
    connection.commit()
    flash("Location Deleted successfully")
    return redirect(url_for("mentor_map"))

# Coach feed
@app.route('/coach/feed',methods=["POST","GET"])
def coach_feed():
    if session.get("log") == False or session.get("coach") == None:
        return redirect(url_for('login'))
    feed = cursor.execute("SELECT * FROM CoachFeed WHERE IdCoach=?",[session.get("coach")]).fetchall()
    if request.method == "POST":
        content = request.form["content"]
        cursor.execute('''INSERT INTO CoachFeed(IdCoach,Content,Date)
        values(?,?,?)''',[session.get("coach"),content,datetime.datetime.now().strftime("%B %d, %Y at %I:%M%p")])
        connection.commit()
        flash("Post submitted successfully")
        return redirect(url_for("coach_feed"))
    return render_template("coach/coach-feed.html",feed=feed)

# Delete post from feed
@app.route('/coach/feed/delete:<id>')
def delete_feed(id):
    if session.get("log") == False or session.get("coach") == None:
        return redirect(url_for('login'))
    if cursor.execute("SELECT EXISTS(SELECT * FROM CoachFeed WHERE IdCoach = ?)",[session.get("coach")]) == False:
        return redirect(url_for("login"))
    cursor.execute("DELETE FROM CoachFeed WHERE IdFeed = ?",[id])
    connection.commit()
    flash("Request deleted successfully")
    return redirect(url_for("coach_feed"))

# check type of account and logout
@app.route('/logout-check')
def logout_check():
    if session.get("user") != None:
        return redirect(url_for("logout"))
    elif session.get("coach") != None:
        return redirect(url_for("logout_coach"))
    elif session.get("admin") != False:
        return redirect(url_for("logout_admin"))

# return to different type of profile
@app.route('/profile-check')
def profile_check():
    if session.get("admin") == True:
        return redirect(url_for("admin"))
    elif session.get("user") != None:
        return redirect("user")
    elif session.get("coach"):
        return redirect("coach")

#logout user
@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("log",False)
    return redirect('login')

# logout admin
@app.route('/logout-admin')
def logout_admin():
    session.pop("admin",None)
    session.pop("log",False)
    return redirect('login-admin')

# logout coach
@app.route('/logout-coach')
def logout_coach():
    session.pop("coach",None)
    session.pop("log",False)
    return redirect('login')

# logout cashier
@app.route('/logout-cashier')
def logout_cashier():
    session.pop("cashier",None)
    session.pop("log",False)
    return redirect('login-cashier')

# check email validation
def Check_authentification():
    return cursor.execute('''SELECT EXISTS(SELECT * FROM CheckUser WHERE IdLog=?)
    ''',[cursor.execute("SELECT IdLog FROM User WHERE IdUser=?",[session.get("user")]).fetchone()[0]]).fetchone()[0]

# check account type
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
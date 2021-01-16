from flask import session, Blueprint, request, render_template, flash, redirect, url_for
#from flask import current_app as current_app
import datetime

from app.module import dbModule

gmmovie = Blueprint('', __name__, url_prefix='/')

@gmmovie.route('/', methods=['GET'])
def index():
    return render_template('/index.html')

@gmmovie.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('/SignupForm.html')
    CustomerId = request.form.get('CustomerId')
    LName = request.form.get('LName')
    FName = request.form.get('FName')
    Address = request.form.get('Address')
    City = request.form.get('City')
    State = request.form.get('State')
    ZipCode = request.form.get('ZipCode')
    Telephone = request.form.get('Telephone')
    Email = request.form.get('Email')
    AccountId = request.form.get('AccountId')
    AccountType = request.form.get('AccountType')
    CreditCard = request.form.get('CreditCard')
    credate = datetime.datetime.now().strftime("%Y-%m-%d")
    if not (CustomerId and LName and FName and Address and City and State and
            ZipCode and Telephone and Email and AccountId and AccountType and CreditCard):
        return redirect('/signup')
    db_class = dbModule.Database()
    sql = "INSERT INTO gmmovie.customers(CustomerId, LName, FName, Address, City, State, ZipCode, Telephone, Email, \
        CreditCard, AccountId, AccountType, AccCreateDate, Rating) \
                    VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '%d','%s', '%s', %d)" % \
          (CustomerId, LName, FName, Address, City, State, ZipCode, Telephone, Email,
           CreditCard, int(AccountId), AccountType, credate, 1)
    db_class.execute(sql)
    db_class.commit()
    return redirect('/')

@gmmovie.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/LoginForm.html')
    db_class = dbModule.Database()
    login_info = request.form
    loginId = login_info['LoginId']
    sql = "SELECT * FROM Customers WHERE Email=%s"
    user = db_class.cursor.execute(sql, loginId)
    if user > 0:
        session['logged_in'] = db_class.cursor.fetchone()
    else:
        print("can't login")
    return redirect('/')

@gmmovie.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    return redirect('/')

@gmmovie.route('/showMovieList', methods=['GET'])
def showMovieList():
    sql = "SELECT * FROM MOVIES"
    db_class = dbModule.Database()
    cnt = db_class.cursor.execute(sql)
    if cnt > 0:
        movie = db_class.cursor.fetchall()
        return render_template('/MovieForm.html',
                               result=movie)
    return render_template('/MovieForm.html',
                           result='')

@gmmovie.route('/showOrder', methods=['GET'])
def showOrder():
    db_class = dbModule.Database()
    sql = "select AccountId from customers where CustomerId=%s;"
    db_class.cursor.execute(sql, session['logged_in']['CustomerId'])
    account_id = db_class.cursor.fetchone()
    sql2 = "select OrderId, MovieName, Date_Time, Return_Date, ORating from movies, " \
        "orders where MovieId=OmovieId and OAccountId ="+str(account_id['AccountId'])+" ORDER BY OrderId;"
    cnt = db_class.cursor.execute(sql2)
    if cnt > 0:
        order = db_class.cursor.fetchall()
        return render_template('/RateForm.html',
                               result=order)
    return render_template('/RateForm.html',
                           result='noorder')

@gmmovie.route('/customerHeldMovies', methods=['GET'])
def customerHeldMovies():
    sql = "SELECT MovieName FROM ORDERS, CUSTOMERS, " \
          "MOVIES WHERE OmovieId = MovieId AND CustomerId = %s" \
          " AND OAccountId=AccountId AND Return_Date IS null ORDER BY MovieName ASC;"
    db_class = dbModule.Database()
    customerId = session['logged_in']['CustomerId']
    cnt = db_class.cursor.execute(sql, customerId)
    if cnt > 0:
        movie = db_class.cursor.fetchall()
        movieList = ''
        for i in range(0, cnt):
            if i == (cnt-1): movieList += movie[i]['MovieName']
            else: movieList += movie[i]['MovieName'] + ', '
        return render_template('/Result.html',
                               result=movieList, method='current')
    return render_template('/Result.html',
                           result='nomovie')

@gmmovie.route('/customerQueue', methods=['GET'])
def customerQueue():
    sql = "SELECT MovieName FROM CUSTOMERS, MOVIEQUEUE, " \
          "MOVIES WHERE CustomerId = %s AND CustomerId = QcustomerId " \
          "AND AccountId = QaccountId AND QmovieId=MovieId ORDER BY MovieName ASC;"
    db_class = dbModule.Database()
    customerId = session['logged_in']['CustomerId']
    cnt = db_class.cursor.execute(sql, customerId)
    if cnt > 0:
        movie = db_class.cursor.fetchall()
        movieList = ''
        for i in range(0, cnt):
            if i == (cnt-1): movieList += movie[i]['MovieName']
            else: movieList += movie[i]['MovieName'] + ', '
        return render_template('/Result.html',
                               result=movieList, method='queue')
    return render_template('/Result.html',
                           result='nomovie')

@gmmovie.route('/customerAccount', methods=['GET'])
def customerAccount():
    sql = "SELECT AccountId, AccountType, AccCreateDate FROM CUSTOMERS " \
          "WHERE CustomerId = %s ORDER BY AccountId ASC;"
    db_class = dbModule.Database()
    customerId = session['logged_in']['CustomerId']
    cnt = db_class.cursor.execute(sql, customerId)
    if cnt > 0:
        account = db_class.cursor.fetchone()
        accountList = '[Account ID' \
                      ': ' + str(account['AccountId']) + '], [Account Type:' \
            ' ' + account['AccountType'] + '], [Account Create Date: ' + str(account['AccCreateDate']) + ']'
    return render_template('/Result.html',
                           result=accountList, method='account')

@gmmovie.route('/availableType', methods=['POST'])
def availableType():
    sql = "SELECT MovieName FROM MOVIES WHERE MovieType=%s;"
    db_class = dbModule.Database()
    type = request.form['type']
    cnt = db_class.cursor.execute(sql, type)
    if cnt > 0:
        movie = db_class.cursor.fetchall()
        movieList = ''
        for i in range(0, cnt):
            if i == (cnt - 1):
                movieList += movie[i]['MovieName']
            else:
                movieList += movie[i]['MovieName'] + ', '
        return render_template('/Result.html',
                               result=movieList, method='type', type=type)
    return render_template('/Result.html',
                           result='nomovie')

@gmmovie.route('/searchMovie', methods=['POST'])
def searchMovie():
    name = request.form['name'].split(',')
    sql = "SELECT MovieName FROM MOVIES WHERE MovieName LIKE '%%"
    lens = len(name)
    for i in range(0, lens):
        if i == lens-1:
            sql += name[i] + "%%';"
        else:
            sql += name[i] + "%%' AND MovieName LIKE '%%"
    db_class = dbModule.Database()
    cnt = db_class.cursor.execute(sql)
    if cnt > 0:
        movie = db_class.cursor.fetchall()
        movieList = ''
        for i in range(0, cnt):
            if i == (cnt - 1):
                movieList += movie[i]['MovieName']
            else:
                movieList += movie[i]['MovieName'] + ', '
        return render_template('/Result.html',
                               result=movieList, name=name, method='search')
    return render_template('/Result.html',
                           result='nomovie')

@gmmovie.route('/actorAppearedIn', methods=['POST'])
def actorAppearedIn():
    name = request.form['actor'].split(',')
    db_class = dbModule.Database()
    sql = 'SELECT DISTINCT MovieName from MOVIES, APPEARED_IN, ACTORS WHERE MovieId=AmovieId'
    lens = len(name)
    for i in range(0, lens):
        sql += " AND MovieId IN(SELECT AmovieId FROM APPEARED_IN, " \
                "ACTORS WHERE ActorId = AactorId AND ActorName=%s)"
    sql += ";"
    cnt = db_class.cursor.execute(sql, name)
    if cnt > 0:
        movie = db_class.cursor.fetchall()
        movieList = ''
        for i in range(0, cnt):
            if i == (cnt - 1):
                movieList += movie[i]['MovieName']
            else:
                movieList += movie[i]['MovieName'] + ', '
        return render_template('/Result.html',
                               result=movieList, method='actor', actor=name)
    return render_template('/Result.html',
                           result='nomovie')

@gmmovie.route('/showBestSeller', methods=['GET'])
def showBestSeller():
    sql = "SELECT MovieName FROM MOVIES WHERE NumCopies > 2;"
    db_class = dbModule.Database()
    cnt = db_class.cursor.execute(sql)
    if cnt > 0:
        movie = db_class.cursor.fetchall()
        movieList = ''
        for i in range(0, cnt):
            if i == (cnt-1): movieList += movie[i]['MovieName']
            else: movieList += movie[i]['MovieName'] + ', '
        return render_template('/Result.html',
                               result=movieList, method='best')
    return render_template('/Result.html',
                           result='nomovie')

@gmmovie.route('/suggestMovie', methods=['GET'])
def suggestMovie():
    sql1 = "DROP VIEW IF EXISTS mostType;"
    sql2 = "CREATE VIEW mostType AS SELECT COUNT(*), MovieType FROM" \
           " ORDERS, MOVIES, CUSTOMERS WHERE CustomerId = %s " \
           "AND AccountId = OaccountId AND OmovieId = MovieId GROUP BY MovieType " \
           "ORDER BY COUNT(*) DESC, MovieType DESC;"
    sql3 = "SELECT MovieName FROM MOVIES WHERE MovieType = (SELECT MovieType FROM" \
           " mostType limit 1) AND MovieId NOT IN(SELECT OMovieId FROM ORDERS, CUSTOMERS" \
           " WHERE CustomerId = %s AND AccountId = OaccountId);"
    db_class = dbModule.Database()
    customerId = session['logged_in']['CustomerId']
    db_class.cursor.execute(sql1)
    db_class.cursor.execute(sql2, customerId)
    cnt = db_class.cursor.execute(sql3, customerId)
    if cnt > 0:
        movie = db_class.cursor.fetchall()
        movieList = ''
        for i in range(0, cnt):
            if i == (cnt-1): movieList += movie[i]['MovieName']
            else: movieList += movie[i]['MovieName'] + ', '
        return render_template('/Result.html',
                               result=movieList, method='suggest')
    return render_template('/Result.html',
                           result='nomovie')

@gmmovie.route('/rateMovie', methods=['POST'])
def rateMovie():
    order_id = request.form.get('OrderId')
    rating = request.form.get('Rating')
    db_class = dbModule.Database()
    sql = "UPDATE ORDERS SET ORating = "+rating+" WHERE OrderId="+order_id+";"
    db_class.cursor.execute(sql)
    db_class.commit()
    return redirect('/')

from flask import Flask , request , render_template , flash , redirect , url_for , session, logging,make_response
from flask_mysqldb import MySQL
from wtforms import Form , StringField , TextAreaField , PasswordField , validators ,SelectField
from passlib.hash import sha256_crypt
from functools import wraps
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
import os
import pdfkit
app = Flask(__name__)
#


#line remove
UPLOAD_FOLDER = 'static/img/upload_files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mohammad'
app.config['MYSQL_PASSWORD'] = '1375'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args , **kwargs):
        if 'logged_in' in session:
            return f(*args , **kwargs)
        else:
            flash('Unauthorized , Please login' , 'danger')
            return redirect(url_for('login'))
    return wrap



@app.route('/', defaults={'page':1})
@app.route('/<int:page>')
def index(page):
    cur = mysql.connection.cursor()

    perpage=5
    if page==1:
        startat=0
    else :
        startat=(page-1)*perpage
    result = cur.execute("select articles.id,articles.summery,articles.image_url,articles.body,articles.title,articles.author,articles.create_date,subjects.id,subjects.title as sub from articles join subjects on articles.subject = subjects.id  limit %s,%s" ,[startat,perpage])
    #result = cur.execute("CALL home_articles (%s,%s)" ,[startat,perpage])
    articles=cur.fetchall()
    result = cur.execute("SELECT * FROM subjects")
    subjects=cur.fetchall()
    if result>0:
        return render_template('home.html' , articles=articles,page=page,subjects=subjects)
    else:
        msg = "No Articles Found"
        return render_template('home.html' , msg=msg)
    cur.close()


@app.route('/pdf/<string:id>')
def pdf(id):
    cur = mysql.connection.cursor()
#
# #    result = cur.execute("SELECT * FROM articles WHERE id= %s " , [id])
#     result = cur.execute("select articles.id,articles.image_url,articles.body,articles.title,articles.author,articles.create_date,subjects.id,subjects.title as sub from articles join subjects on articles.subject = subjects.id where articles.id = %s " , [id])
    result = cur.execute("CALL select_article (%s)",[id])
    article=cur.fetchone()
    rendered = render_template('article.html' , article=article)
    #
    pdf=pdfkit.from_string(rendered,False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment ; filename=output.pdf'
    return response
    cur.close()


class SearchForm(Form):
    word = StringField('Name', [validators.Length(min=1, max=200)])
# @app.route('/search/<string:word>', methods=['POST'])
# def search(word):
#     cur = mysql.connection.cursor()
#
#     result = cur.execute("SELECT * FROM articles WHERE title=%s ", [str(word)])
#     articles=cur.fetchall()
#     if result>0:
#         return render_template('search.html' , articles=articles,word=word)
#     else:
#         msg = "No Articles Found"
#         return render_template('search.html' , msg=msg)
#     cur.close()
#
#
@app.route('/search')
def search():
    search='%'+request.args.get("word")+'%'
    cur = mysql.connection.cursor()
    # perpage=5
    # if page==1:
    #     startat=0
    # else :
    #     startat=(page-1)*perpage
    # result = cur.execute("select articles.id,articles.body,articles.title,articles.author,articles.create_date,subjects.id,subjects.title as sub from articles join subjects on articles.subject = subjects.id  limit %s,%s" ,[startat,perpage])
    result = cur.execute("SELECT * FROM articles WHERE title LIKE   %s UNION SELECT * FROM articles WHERE body LIKE %s" , [str(search),str(search)])

    articles=cur.fetchall()
    result = cur.execute("SELECT * FROM subjects")
    subjects=cur.fetchall()
    if result>0:
        return render_template('search.html' , articles=articles,subjects=subjects)
    else:
        msg = "No Articles Found"
        return render_template('search.html' , msg=msg)
    cur.close()

@app.route('/cat/<int:id>')
def searchh(id):

    cur = mysql.connection.cursor()
    # perpage=5
    # if page==1:
    #     startat=0
    # else :
    #     startat=(page-1)*perpage
    # result = cur.execute("select articles.id,articles.body,articles.title,articles.author,articles.create_date,subjects.id,subjects.title as sub from articles join subjects on articles.subject = subjects.id  limit %s,%s" ,[startat,perpage])
    result = cur.execute("SELECT * FROM articles WHERE subject=%s " , [id])
    articles=cur.fetchall()

    result = cur.execute("SELECT * FROM subjects")
    subjects=cur.fetchall()
    if result>0:
        return render_template('search.html' , articles=articles,subjects=subjects)
    else:
        msg = "No Articles Found"
        return render_template('search.html' , msg=msg)
    cur.close()



@app.route('/about')
def about():
    return render_template('about.html')
# @app.route('/articles')

@app.route('/articles', defaults={'page':1})
@app.route('/articles/<int:page>')
def articles(page):

    cur = mysql.connection.cursor()

    perpage=3
    if page==1:
        startat=1
    else :
        startat=(page-1)*perpage
    # result = cur.execute("SELECT * FROM articles limit %s,%s" ,[startat,perpage])
    result = cur.execute("CALL sp_articles")
    articles=cur.fetchall()
    result = cur.execute("SELECT * from subjects")
    subjects=cur.fetchall()
    if result>0:
        return render_template('articles.html' , articles=articles,subjects=subjects)
    else:
        msg = "No Articles Found"
        return render_template('articles.html' , msg=msg)
    cur.close()


@app.route('/article/<string:id>/')
def article(id):
    cur = mysql.connection.cursor()

#    result = cur.execute("SELECT * FROM articles WHERE id= %s " , [id])
    result = cur.execute("select articles.id,articles.summery,articles.image_url,articles.body,articles.title,articles.author,articles.create_date,subjects.id,subjects.title as sub from articles join subjects on articles.subject = subjects.id where articles.id = %s " , [id])
    #result = cur.execute("CALL select_article (%s)",[id])
    article=cur.fetchone()
    #

    return render_template('article.html' , article=article)
    cur.close()


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    level = SelectField('Level',choices=[])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')    ])
    confirm = PasswordField('Confirm Password')

# User Register
@app.route('/regs', methods=['GET', 'POST'])
def regs():

    form = RegisterForm(request.form)
    cur = mysql.connection.cursor()


    result = cur.execute("select * from level")
    levels=cur.fetchall()
    form.level.choices=[(level['id'],level['title']) for level in levels]
    cur.close()
    if request.method == 'POST' :#and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        level = form.level.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password , level_id) VALUES(%s, %s, %s, %s,%s)", (name, email, username, password ,level))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))
    return render_template('regs.html', form=form)

class CommentForm(Form):

    body = TextAreaField('Body', [validators.Length(min=30)])


@app.route('/add_comment/<int:post_id>' , methods = ['GET' ,'POST'])
@is_logged_in
def add_comment(post_id):
    if session['level'] not in [1,2]:
        flash ('You Not A admin' )
        return render_template('home.html' ,page=0)
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        body = form.body.data


        cur = mysql.connection.cursor()

        cur.execute("INSERT into comments(body  , writer_id,post_id) VALUES (%s , %s,%s)" , (body , session['username'],post_id) )

        mysql.connection.commit()

        cur.close()
        flash('Subject Created' , 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_subject.html' , form=form)


class ArticleForm(Form):
    title = StringField('Name', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])
    url=StringField('Image URL')
    subject = SelectField('Subject',choices=[])
    summery = TextAreaField('Summery', [validators.Length(min=30)])




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/add_article' , methods = ['GET' ,'POST'])
@is_logged_in
def add_article():
    if session['level'] not in [1,2]:
        flash ('You Not A admin' )
        return render_template('home.html' ,page=0)
    # colours = ['Red', 'Blue', 'Black', 'Orange']
    form = ArticleForm(request.form)
    cur = mysql.connection.cursor()
    # result = cur.execute("SELECT id,title FROM subjects")
    result = cur.execute("CALL select_subject")
    subjects=cur.fetchall()
    form.subject.choices=[(subject['id'],subject['title']) for subject in subjects]


    cur.close()
    filename=""
    if request.method == 'POST' :#and form.validate():
        file = request.files['file']
        if file and allowed_file(file.filename):
#            filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cur = mysql.connection.cursor()
        title = form.title.data
        body = form.body.data
        subject=form.subject.data
        summery=form.summery.data

        # cur = mysql.connection.cursor()

        cur.execute("INSERT into articles(title , body , author,subject,image_url,summery) VALUES (%s , %s , %s,%s,%s,%s)" , (title , body , session['username'] ,subject ,filename,summery))
        print("INSERT into articles(title , body , author,subject,image_url,summery) VALUES (%s , %s , %s,%s,%s,%s)" , (title , body , session['username'] ,subject ,filename,summery))
        mysql.connection.commit()

        cur.close()
        flash('Aricle Created' , 'success')
        return redirect(url_for('dashboard'))
    app.logger.info(form.subject.data)
    return render_template('add_article.html' , form=form)



@app.route('/login' , methods =['GET' , 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        # result = cur.execute("select * from users where username = %s" , [username])
        result = cur.execute("call select_user (%s)" , [username])

        if result >0 :
            data = cur.fetchone()
            password = data['password']
            level = data['level_id']
            if sha256_crypt.verify(password_candidate , password):
                #app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['username'] = username
                session['level'] = level

                flash('You Are logged in' , 'success')
                return redirect(url_for('dashboard'))
            else :
                error = 'Invalid Login'
                return render_template('login.html' , error=error)
            cur.close()
        else:
            error = 'UserName Not Found'
            return render_template('login.html' , error=error)
    return render_template('login.html')




@app.route('/logout' )
@is_logged_in
def logout():
    session.clear()
    flash ('You are now logged out' ,'success' )
    return redirect(url_for('login'))




@app.route('/dashboard')
@is_logged_in
def dashboard():
    if session['level'] not in [1,2]:
        flash ('You Not A admin' )
        return render_template('home.html' ,page=0)

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM articles")
    articles=cur.fetchall()

    if result>0:
        return render_template('dashboard.html' , articles=articles)
    else:
        msg = "No Articles Found"
        return render_template('dashboard.html' , msg=msg)
    cur.close()


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    if session['level'] not in [1,2]:
        flash ('You Not A admin' )
        return render_template('home.html' ,page=0)
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM articles Where id=%s",[id])
    article=cur.fetchone()

    result = cur.execute("SELECT id,title FROM subjects")
    subjects=cur.fetchall()
    app.logger.info(article['body'])

    cur.close()

    form = ArticleForm(request.form)
    form.subject.choices=[(subject['id'],subject['title']) for subject in subjects]
    form.subject.default=article['subject']
    form.process()
    form.title.data = article['title']
    form.body.data = article['body']
    form.summery.data = article['summery']

    # app.logger.info(form.title.data)
    if request.method == 'POST':# and form.validate():
        cur = mysql.connection.cursor()
        title = request.form['title']
        body = request.form['body']
        subject = request.form['subject']
        summery = request.form['summery']
        cur.execute("UPDATE articles SET title=%s , body=%s ,subject=%s,summery=%s Where id=%s",(title , body ,subject,summery,id) )
        print("UPDATE articles SET title=%s , body=%s ,subject=%s,summery=%s Where id=%s",(title , body ,subject,summery,id))
        mysql.connection.commit()
        cur.close()

        flash('Aricle Updated' , 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_article.html' , form=form )



@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):

    if session['level'] not in [1,2]:
        flash ('You Not A admin' )
        return render_template('articles.html' )
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM articles WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()

    flash('Aricle Deleted' , 'success')
    return redirect(url_for('dashboard'))







######Subject



class SubjectForm(Form):
    title = StringField('Name', [validators.Length(min=1, max=200)])



@app.route('/subjects')
def subjects():

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM subjects")
    subjects=cur.fetchall()

    if result>0:
        return render_template('subjects.html' , subjects=subjects)
    else:
        msg = "No Subjects Found"
        return render_template('subjects.html' , msg=msg)
    cur.close()


@app.route('/add_subject' , methods = ['GET' ,'POST'])
@is_logged_in
def add_subject():
    if session['level'] not in [1,2]:
        flash ('You Not A admin' )
        return render_template('home.html' ,page=0)
    form = SubjectForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data


        cur = mysql.connection.cursor()

        cur.execute("INSERT into subjects(title  , author) VALUES (%s , %s)" , (title , session['username']) )

        mysql.connection.commit()

        cur.close()
        flash('Subject Created' , 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_subject.html' , form=form)

@app.route('/edit_subject/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_subject(id):
    if session['level'] not in [1,2]:
        flash ('You Not A admin' )
        return render_template('home.html' ,page=0)
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM subjects Where id=%s",[id])
    article=cur.fetchone()
    cur.close()

    form = SubjectForm(request.form)

    form.title.data = article['title']



    if request.method == 'POST' and form.validate():

        title = request.form['title']

        cur = mysql.connection.cursor()
        app.logger.info(title)
        cur.execute("UPDATE subjects SET title =%s  Where id=%s",(title ,id) )

        mysql.connection.commit()
        cur.close()

        flash('Subject Updated' , 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_subject.html' , form=form)


@app.route('/delete_subject/<string:id>', methods=['POST'])
@is_logged_in
def delete_subject(id):
    if session['level'] not in [1,2]:
        flash ('You Not A admin' )
        return render_template('home.html' ,page=0)
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM subjects WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()

    flash('Subject Deleted' , 'success')
    return redirect(url_for('subjects'))


@app.route('/test')
def test():
    render_template('test.html')

if __name__ == "__main__":
    app.secret_key = 'secret123'
    #app.run(debug=True ,host = '0.0.0.0',port=80)
    app.run(debug=True)

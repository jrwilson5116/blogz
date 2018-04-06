from flask import Flask, request, redirect, render_template, url_for,session
from flask_sqlalchemy import SQLAlchemy 
from input_checks import valid_length, match

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'shhh123'
db = SQLAlchemy(app)



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.Text)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.title = name
        self.body =body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner_id')

    def __init__(self,username,password):
        self.username = username
        self.password = password
     


@app.route('/')
def index():
    #TODO add home page
    return render_template('index.html')


@app.route('/blog', methods=['GET'])
def blog():
    blog_post = request.args.get('id')

    if blog_post is None:
        tasks = Blog.query.all()
    else:
        tasks = Blog.query.filter_by(id = blog_post)
    return render_template('blog.html',title="Blog", tasks=tasks)


@app.route('/newpost',methods=['POST','GET'])
def add_post():
    if request.method == 'POST':
        blog_name = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_name,blog_body,owner)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('blog'))
    return render_template('newpost.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    name_error = ''
    password_error = ''
    match_error = ''

    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify']

        valid = True 

        if not valid_length(user_name):
            name_error = 'Invalid username'
            valid = False
        elif not User.query.filter_by(username=user_name).first() == None:
            name_error = 'Username is already taken'
            valid = False
        if not valid_length(password):
            password_error = 'Invalid password'
            valid = False 
        if not match(password,verify_password):
            match_error = 'Passwords do not match'
            valid = False 
        
        if valid == True:
            new_user = User(user_name,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = user_name
            return redirect(url_for('add_post'))

    return render_template('signup.html').format(name_error,password_error,match_error)

@app.route('/login', methods=['POST','GET'])
def login():
    name_err=''
    pass_err=''

    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=user_name).first() == None:
            name_err='Invalid username'
        else:
            current_user = User.query.filter_by(username=user_name).first()
            
        if current_user and current_user.password == password:
            session['username'] = user_name
            return redirect(url_for('add_post'))
        elif current_user and current_user.password != password:
            pass_err = 'Invalid password'

    return render_template('login.html').format(name_err,pass_err)

@app.route('/logout')
def logout():
    #TODO remove username from 
    return redirect(url_for('blog'))



if __name__=='__main__':
    app.run()
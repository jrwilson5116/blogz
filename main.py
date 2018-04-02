from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy 
from input_checks import valid_length, match

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.title = name
        self.body =body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self,username,password):
        self.username = username
        self.password = password
     


@app.route('/')
def index():
    #TODO add home page
    return redirect(url_for('blog'))


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
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify']

        if not valid_length(username):
            name_error = 'Invalid username'
        if not valid_length(password):
            password_error = 'Invalid password'
        if not match(password,verify_password):
            match_error = 'Passwords do not match'
        
        if valid_length(username) and valid_length(password) and match:
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('add_post'))

    return render_template('signup.html').format(name_error,password_error,match_error)

@app.route('/login', methods=['POST','GET'])
def login():
    #TODO process login attempt
    # if username is real and password matches store username in session and redirect to newpost page
    # if username does not exist, redirect to login with bad username message
    # if username exists but password does not match

    return render_template('login.html')

@app.route('/logout')
def logout():
    #TODO remove username from session
    return redirect(url_for('blog'))



if __name__=='__main__':
    app.run()
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

    def __init__(self, name, body,owner):
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
    users = User.query.order_by(User.id.desc()).all()
    return render_template('index.html', users = users)


@app.before_request
def require_login():
    allowed_routes = ['login','signup','blog','index','logout']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect(url_for('login'))


@app.route('/blog', methods=['GET'])
def blog():
    blog_ID = request.args.get('id')
    username_get = request.args.get('username')
    
    if blog_ID is not None: 
        blog = Blog.query.filter_by(id = blog_ID).first()
        return render_template('singlePost.html',title='Blog',blog=blog)
    elif username_get is not None:
        author = User.query.filter_by(username = username_get).first()
        blogs = Blog.query.filter_by(owner=author.id)
        return render_template('singleUser.html',title = 'blog', blogs=blogs)
    elif 'username' in session:
        author = User.query.filter_by(username = session['username']).first()
        blogs = Blog.query.filter_by(owner=author.id)
        return render_template('singleUser.html',title ='blog',blogs=blogs)

    blogs = Blog.query.all()

    return render_template('blog.html',title="Blog", blogs=blogs)


@app.route('/newpost',methods=['POST','GET'])
def add_post():
    if request.method == 'POST':
        blog_name = request.form['title']
        blog_body = request.form['body']

        currentUser = User.query.filter_by(username = session['username']).first()

        new_blog = Blog(blog_name,blog_body,currentUser.id)

        db.session.add(new_blog)
        db.session.commit()

        return redirect(url_for('blog',id=new_blog.id))

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

        name_error = valid_length(user_name)
        password_error = valid_length(password)
        match_error = match(password,verify_password)
        
        if not name_error and not password_error and not match_error:
            new_user = User(user_name,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = user_name
            return redirect(url_for('add_post'))

    return render_template('signup.html').format(name_error,password_error,match_error)

@app.route('/login', methods=['POST','GET'])
def login():
    #TODO add error messages tailored to error 
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
    if 'username' in session:
        del session['username']
    return redirect('/')
    

if __name__=='__main__':
    app.run()
from flask import Flask, request, redirect, render_template, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:buildtheblogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(120))
        body = db.Column(db.Text(900))
        owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        def __init__(self, title, owner, body):
            self.title = title
            self.body = body
            self.owner = owner

class User(db.Model):

       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(35))
       password = db.Column(db.String(45))
       blogs = db.relationship('Blog', backref='owner')




@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods=['Post', 'GET']) #original route
def index():

    blogs = Blog.query.all()
    return render_template('blog.html', page_title ="Blogz", blogs=blogs)

@app.route('/newpost', methods=['GET']) #original route
def newpost():

    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    return render_template('newpost.html', page_title=blog.title, entry=blog.body)

#worked on this, need redirect signup if no accnt
@app.route('/login', methods=['POST, GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        user = User.query.filter_by('username=username').first()
        if user and user.name == name:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash ('User name incorrect, or user does not exist' )

        return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        def is_input_not_valid(input): #original code
            if input == "" or len(input) < 3 or len(input) > 20 or " " in input:
                return True
        return False

def not_matching_passwords(password1, password2):
    if not password1 == password2:
        return True
    return False

def email_not_valid(email):
    if not email == '':
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email) or len(email) < 3 or len(email) > 20:
            return True 
        return False #end original code

    existing_user = User.query.filter_by(username=username.first())
    if not existing_user:
        new_user = User(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect('/')
    else:
        return "<h1> Duplicate User </h1>"

    return render_template('register.html')


@app.route('/entry', methods=['POST', 'GET'])
def blog_entry():
    return render_template('entry.html', page_title="Blogz")




@app.route('/all_posts', methods=['GET'])
def all_posts():

    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    return render_template('all_posts.html', page_title=blog.title, entry=blog.body)

@app.route('/enter-data', methods=['GET', 'POST']) #original route
def data_entry():

    if request.method == 'POST': 
        title = request.form['title']
        entry = request.form['entry']

        if title == '' or entry == '':
            return render_template('entry.html', title=title, entry=entry)


        fresh_blog = Blog(title, entry)
        db.session.add(fresh_blog)
        db.session.commit()
        
    blogs = Blog.query.all() #end of original route
    return render_template('all_posts.html', entry=entry, page_title=title)    

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__':
    app.run()
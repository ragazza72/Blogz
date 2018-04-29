from flask import Flask, request, redirect, render_template, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:buildtheblogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'shhhhitsasecret'

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
    allowed_routes = ['login', 'signup', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods=['Post', 'GET']) #original route
def index():

    users = User.query.all()
    return render_template('index.html', page_title ="Blogz", users=users)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('username') is not None:
        flash("You are already logged in. Please sign out.")
        return redirect('/blog')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash ('User name incorrect, or user does not exist' )
               
    return render_template('login.html')



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Existing User")
            print(session)
            return redirect('/signup')
       
        if not username or not password or not verify:
            flash("All fields need filled in.")
            print(session)
            return redirect('/signup')
        
        if password != verify:
            flash("Your passwords do not match")
            print(session)
            return redirect('/signup')      
        
        if len(password)<3 or len(username)<3:
            flash("Your username and password does not match.")
            print(session)
            return redirect('/signup')   
        
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            print(session)
            return redirect('/newpost')


    return render_template('signup.html')




@app.route('/blog', methods=['GET'])
def blog():
    def blog():
        if request.args.get('id'):
            blog_id = int(request.args.get('id'))
            single_id = Blog.query.get(blog_id)
        return render_template('entry.html', blog=single_id)

    blogs = Blog.query.all()
    return render_template('blog.html',blogs=blogs)


@app.route('/singleuser')
def singleuser():
    if request.method == 'GET':
        user_id = int(request.args.get('id'))
        user = User.query.filter_by(id=user_id).first()
        blogs = Blog.query.filter_by(owner_id=user_id)

    return render_template('singleUser.html', blogs=blogs, user=user)   

@app.route('/newpost', methods=['GET', 'POST']) #original route
def newpost():

    if request.method == 'POST': 
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()

    if body and title:
            new_post = Blog(title,body,owner)
            db.session.add(new_post)
            db.session.commit()
            return redirect ('/blog?id='+str(new_post.id))

    if not body or not title:
            flash("Text Required In All Fields")
    return render_template('newpost.html')
        
        
   

@app.route('/logout')
def logout():
    if 'user' in session:
        del session['username']
    return redirect('/login')

if __name__ == '__main__':
    app.run()
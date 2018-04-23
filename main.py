from flask import Flask, request, redirect, render_template, session, url_for
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

        def __init__(self, title, body):
            self.title = title
            self.body = body

#class User(db.Model):

       # id = db.Column(db.Integer, primary_key=True)




@app.route('/', methods=['Post', 'GET'])
def index():

    blogs = Blog.query.all()
    return render_template('blog.html', page_title ="Build a Blog", blogs=blogs)




@app.route('/entry', methods=['POST', 'GET'])
def blog_entry():
    return render_template('entry.html', page_title="Build a Blog")




@app.route('/newpost', methods=['GET'])
def newpost():

    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    return render_template('newpost.html', page_title=blog.title, entry=blog.body)

@app.route('/enter-data', methods=['GET', 'POST'])
def data_entry():

    if request.method == 'POST': 
        title = request.form['title']
        entry = request.form['entry']

        if title == '' or entry == '':
            return render_template('entry.html', title=title, entry=entry)


        fresh_blog = Blog(title, entry)
        db.session.add(fresh_blog)
        db.session.commit()
        
    blogs = Blog.query.all()
    return render_template('newpost.html', entry=entry, page_title=title)    

if __name__ == '__main__':
    app.run()
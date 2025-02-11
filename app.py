from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

pcl = [ 
    { 
        'model':'Dell', 'cpu': 'AMD', 'ram': '8GB'  
    },

    {
        'model1':'Acer', 'cpu1': 'intel1', 'ram1': '4GB'
    }
]
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/posts', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')
        
@app.route('/laps')
def lap():
    return render_template('l.html', specs = pcl)

@app.route('/PCs')
def pc():
    return render_template('komputri.html')


def test():
    return render_template('test.html', specs=pcl)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=('2095'), debug=True)
    

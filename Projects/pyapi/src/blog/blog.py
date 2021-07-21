from pathlib import Path
from quart import Quart
from sqlite3 import dbapi2 as sqlite3


app = Quart(__name__)

app.config.update({
    'SECRET_KEY':'development key',
    'DATABASE':app.root_path / 'blog.db',
    'USERNAME': 'admin',
    'PASSWORD': 'default'
})

def connect_db():
    engine = sqlite3.connect(app.config['DATABASE'])
    engine.row_factory = sqlite3.Row
    return engine

#allow initialize empty db from terminal
@app.cli.command('init_db')
def init_db():
    #creating empty db
    db = connect_db()
    with open(Path(__file__).parent / 'shema.sql', mode='r') as file_:
        db.cursor().executescript(file_.read())
    db.commit()
    
    
from quart import render_template, g 

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.route('/',methods=['GET'])
async def posts():
    db = get_db()
    cur = db.execute(
        """SELECT title, text
        FROM post
        ORDER BY id DESC"""
    )
    posts = cur.fetchall()
    return await render_template('post.html', posts=posts)

#create a new post
from quart import redirect, request, url_for,abort
@app.route('/',methods=['POST'])
async def creator():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    form  = await request.form
    db.execute(
        "INSERT INTO post (title,text) VALUES (?,?)",
        [form['title'],form['text']],
    )
    db.commit()
    return redirect(url_for('posts'))

#configuring authentication

from quart import session 

@app.route('/login/',methods=['POST','GET'])
async def login():
    error = None 
    if request.method == 'POST':
        form = await request.form
        if form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif form['password'] != app.config['PASSWORD']:
            error = 'Invalid Password'
        else:
            session['logged_in'] = True
            return redirect(url_for('posts'))
    return await render_template('login.html',error=error)

@app.route('/logout/')
async def logout():
    session.pop('logged_in',None)
    #await flash('You were logged out')
    return redirect(url_for('posts'))
    



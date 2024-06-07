from flask import Flask, request, render_template, url_for, redirect
import sqlite3

app = Flask(__name__)


db_locale = ('posts.db')
# table name posts_table

def conn_w_db():
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    return conn, c

def commit_close(conn):
    conn.commit()
    conn.close()


def post_table():
    conn, c = conn_w_db()
    c.execute("""CREATE TABLE IF NOT EXISTS posts_table(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              post TEXT NOT NULL,
              timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP              
              )""")



posts =  [
    {
        "title": "something1",
        "post": "some long text that is a blablablbalbalba"
    },
    {
        "title": "something2",
        "post": "some long text that is a blablablbalbalba"
    }
]




#  insert into db
@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    conn, c = conn_w_db()
    if request.method == "GET":
        commit_close(conn)   
        return render_template(url_for('home'))
           
    

    elif request.method == "POST":
        try:            
            post_title = request.form['post_title']
            post_content = request.form['post_content']
            c.execute("INSERT INTO posts_table (title, post) VALUES (?,?)", (post_title, post_content))
            commit_close(conn)
            return redirect(url_for('home'))
        except sqlite3.error as e:
            return f"Database error {e}"
        
    else:
        commit_close(conn)
        return redirect(url_for('home'))
    



@app.route("/read_del/<int:id>", methods=['GET', 'POST'])
def read_del(id):
    return ""
    


    









@app.route('/')
def home():
    conn, c = conn_w_db()
    c.execute("SELECT * FROM posts_table ORDER BY id DESC")
    posts = c.fetchall()
    return render_template("home.html", posts=posts)














if (__name__) == "__main__":
    app.run(debug=True)
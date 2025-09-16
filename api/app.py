from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Ensure templates/static are resolved from project root, not this api/ folder
app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Configure SQLite path differently for Vercel vs local
if os.environ.get("VERCEL") or os.environ.get("VERCEL_URL"):
    # Vercel's writable filesystem is under /tmp
    _db_path = "/tmp/Todo.db"
else:
    _instance_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance'))
    os.makedirs(_instance_dir, exist_ok=True)
    _db_path = os.path.join(_instance_dir, 'Todo.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{_db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable= False)
    desc = db.Column(db.String(500), nullable= False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)
   

@app.route('/about')
def about():
   return render_template('about.html')

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
  if request.method == 'POST':
    title = request.form['title']
    desc = request.form['desc']
    # updatetime =  db.Column(db.DateTime, default = datetime.utcnow)
    todo = Todo.query.filter_by(sno=sno).first()
    todo.title = title
    todo.desc = desc
    # todo.date_creates =  updatetime
    db.session.add(todo)
    db.session.commit()
    return redirect('/')
  todo = Todo.query.filter_by(sno=sno).first()
  return render_template('update.html',todo=todo)
    

if __name__ == '__main__':
    app.run(debug = True,port=8000)
 
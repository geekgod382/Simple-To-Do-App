from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='temp')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default = datetime.now)

    def _repr_ (self):
        return f"{self.sno} - {self.title}, {self.description}, {self.date_created}"
    
@app.route('/')
def todo():
    allTodo = Todo.query.all()
    return render_template('todo.html', allTodo = allTodo)

@app.route('/add', methods = ['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    todo = Todo(title = title, description = description)
    db.session.add(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = todo)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)

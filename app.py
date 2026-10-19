
from flask import Flask,render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///try.db'
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(70),nullable=False)
    date_time = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/' , methods=['POST','GET'])
def index():
    if request.method == 'POST':
        # return "Hello POST"
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_time).all()
        return render_template('index.html',tasks=tasks)
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.filter_by(id = id).first()
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "OOPs! Something went wrong"
@app.route('/update/<int:id>',methods=["POST","GET"])
def update(id):
    task = Todo.query.filter_by(id = id).first()
    if request.method == 'POST':
            # return "Hello POST"
            task.content = request.form['content']
            try:
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue updating your task'
    
    else:
        return render_template('update.html',task =task)
if __name__ == "__main__":
    app.run(debug=True)
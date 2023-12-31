from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#setup application
application = Flask(__name__) 

# {///} is a relative path; {////} is a absolute path
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
#initialise database
db=SQLAlchemy(application)
application.app_context().push() #after this db got created
#create a model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

#return a string everytime we create new item / one of the way to create object
    def __repr__(self):
        return '<Task %r>' % self.id

#routing part
@application.route('/', methods = ['POST', 'GET']) 
#define function for the route
def index(): 
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Issue with the database"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@application.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/')
    except:
            return "Problem with deleting"
    
@application.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
     task = Todo.query.get_or_404(id)
     if request.method == 'POST':
        task.content=request.form['content']
        try:
          db.session.commit()
          return redirect('/')
        except:
          return "issue"
     else:
        return render_template('update.html', task=task)

    

if __name__ == "__main__":
    application.run(debug=True)
     

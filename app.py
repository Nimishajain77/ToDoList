from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///todo.db"
db = SQLAlchemy(app)


class ToDo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(500),nullable=False)
    deadline = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} : {self.description}"


@app.route('/',methods=['POST','GET'])
def home():
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        
        todo = ToDo(title=title,description=description)
        db.session.add(todo)
        db.session.commit()
    
    
    allTodos = ToDo.query.all()
    return render_template("index.html",allTodos=allTodos)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>',methods=['POST','GET'])
def update_todos(sno):
    if request.method == 'POST':
        title=request.form['title']
        description = request.form['description']
        todo =  ToDo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)


    
    return "this is todo page!"



if __name__ == "__main__":
    app.run(debug=True)
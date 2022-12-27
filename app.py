from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/tasks.db'
db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    status = db.Column(db.Boolean)


with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template("index.html", tasksList=tasks)


@app.route('/create-task', methods=['POST'])
def create():
    task = Task(content=request.form['input_task'], status=False)
    if request.form['input_task'] == "":
        print(task)
        return redirect(url_for('home'))
    db.session.add(task)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/delete-task/<id>')
def delete(id):
    Task.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/done/<id>')
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.status = not(task.status)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy

# creates a flask app
app = Flask(__name__)

# tells sqlalchemy where the database is
# for sqlite use firefox sqlite manager
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'

# instance of the db connection
db = SQLAlchemy(app)

# tells the web server to associate url with this method
# GET is for links/urls and POST is for forms
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method=='POST': 
        name = request.form['name']
        email = request.form['email']
        user = User(name, email)
        db.session.add(user)
        db.session.commit()
    users = User.query.all()
    users = sorted(users, key = lambda x:x.name)
    return render_template('form.html', users=users)

@app.route('/delete_user', methods=['GET'])
def delete_user():
    user = User.query.get(request.args.get('id'))
    if user != None: 
        db.session.delete(user)
        db.session.commit()
    return users()

# interface to the user table in sql database, needs to be there
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

# when you convert object to a string, this method is called 
    def __repr__(self):
        return '<User %r>' % self.name

# asks if it was a script created from the command line
# if included as a library, will not run 
if __name__ == '__main__':
    app.run(debug=True)

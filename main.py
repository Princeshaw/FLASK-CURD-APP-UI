from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
file_path = os.path.abspath(os.getcwd())+"/test.db"

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

#create the model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default = datetime.utcnow)
    def __repr__(self):
        return '<Name %r>' % self.id

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        # Handle POST Request here
        name = request.form['name']
        new_friend = Friends(name=name)
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/')
        except:
            return "There is problem with adding in db"  
    else: 
        friends = Friends.query.order_by(Friends.date_created)         
        return render_template('index.html', friends=friends)

@app.route('/subscribe',methods=['GET','POST'])
def subscribe():
    if request.method=='POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        print('hello')
        if(first_name=="" or last_name=="" or email==""):
            return render_template('subscribe.html',error_msg = True,first_name=first_name,last_name=last_name,email=email)
        # Handle POST Request here
        return render_template('subscribe.html')
    return render_template('subscribe.html')


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)
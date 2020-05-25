from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/foursouls'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_ECHO'] = True



#def repr(self):
#    return '<User %r>' % self.username


# Character

class Characters(db.Model):
    character_id = db.Column(db.Integer, primary_key=True)
#    trinket_id = db.Column(db.Integer, db.ForeignKey('trinket.id'))
    character_name = db.Column(db.String(50), unique=True, nullable=False)
    character_health = db.Column(db.Integer, nullable=False)
    character_atk = db.Column(db.Integer, nullable=False)
    character_trinket = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name, health, atk, trinket):
        self.character_name = name
        self.character_health = health
        self.character_atk = atk
        self.character_trinket = trinket


@app.route('/')
def Index():
   all_data = Characters.query.all()

   return render_template("index.html", isaac=all_data)

#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        character_name = request.form['name']
        character_health = request.form['health']
        character_atk = request.form['atk']
        character_trinket = request.form['trinket']
    
        my_data = Characters(character_name, character_health, character_atk, character_trinket)
        db.session.add(my_data)
        db.session.commit()

        flash("Character complete")

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Characters.query.get(request.form.get('id'))

        my_data.character_name = request.form['name']
        my_data.character_health = request.form['health']
        my_data.character_atk = request.form['atk']
        my_data.character_trinket = request.form['trinket']

        db.session.commit()
        flash("Character complete")

        return redirect(url_for('Index'))


#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(character_id):
    my_data = Characters.query.get(character_id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Character complete")

    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)

"""
    def repr(self, name, health, atk):
        return '<Characters %r>' % self.name
"""
"""
# Trinket

class Trinkets(db.Model):
    trinket_id = db.Column(db.Integer, primary_key=True)
    #character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    trinket_name = db.Column(db.String(50), unique=True, nullable=False)
    trinket_effect = db.Column(db.String(50), unique=True, nullable=False)
    #character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)

    def __init__(self, name, effect):
        self.trinket_name = name
        self.trinket_effect = effect


    def repr(self, name, health, atk):
        return '<Trinkets %r>' % self.name
"""

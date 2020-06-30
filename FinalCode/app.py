from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test5.db'
db = SQLAlchemy(app)

visitEvents = db.Table('visitevents',
db.Column('visitorID', db.Integer, db.ForeignKey('user_table.id')),
db.Column('eventID', db.Integer, db.ForeignKey('event.id'))
)

class UserTable(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    FirstName = db.Column(db.String(200) )
    LastName = db.Column(db.String(200) )
    BirthDate = db.Column(db.String(200) )
    Country = db.Column(db.String(20) )
    City = db.Column(db.String(50) )
    PostalCode = db.Column(db.String(20) )
    Street = db.Column(db.String(200) )
    Email = db.Column(db.String(50) )

    events = db.relationship('Event', secondary = visitEvents, backref=db.backref('visitors', lazy = 'dynamic'))

    def __repr__(self):
        return '<Your ID is %r>' % self.UserID

class Artist(db.Model):
    name = db.Column(db.String, primary_key = True)
    genre = db.Column(db.String)
    description = db.Column(db.String)
    origin = db.Column(db.String)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return '<Artist %r>' % self.name

class Location(db.Model):
    adress = db.Column(db.String, primary_key = True)
    name = db.Column(db.String)
    capacitytotal = db.Column(db.Integer)
    capacityseats = db.Column(db.Integer)
    indoor = db.Column(db.Boolean)
    disabledaccess = db.Column(db.Boolean)
    cardpayment =  db.Column(db.Boolean)
    visitorrating = db.Column(db.String)

    def __repr__(self):
        return '<Location %r>' % self.adress

class Event(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    artistName = db.Column(db.String)
    eventName = db.Column(db.String)
    date = db.Column(db.String)
    location = db.Column(db.String)
    price = db.Column(db.String)
    ticketsLeft = db.Column(db.Integer)
    preshowArtist = db.Column(db.String)

    

    def __repr__(self):
        return '<Event %r>' % self.id

class BillingInfo(db.Model):
    creditcardNumber = db.Column(db.Integer, primary_key= True)
    cvc = db.Column(db.Integer)
    expirationDate = db.Column(db.String)

    def __repr__(self):
        return '<ArtBillingInfoist %r>' % self.creditcardNumber

class paymentOptions(db.Model):
    ownerID = db.Column(db.Integer, primary_key = True)
    creditcardNumber = db.Column(db.Integer, primary_key = True)

    def __repr__(self):
        return '<paymentOptions %r>' % self.ownerID



@app.route('/', methods=['POST', 'GET'])
def index():        
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        new_user = UserTable(FirstName = first_name, LastName = last_name)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/userprofile')
        except:
           return 'There was an issue adding the user'
    else:
        return render_template('index.html')


@app.route('/userprofile', methods=['POST', 'GET'])

def userprofile():

    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        birth_date = request.form['birthdate']
        country = request.form['country']
        city = request.form['city']
        postal_code = request.form['postalcode']
        street_nr = request.form['streetnr']
        e_mail = request.form['email']

        new_user = UserTable(FirstName = first_name, LastName = last_name, BirthDate = birth_date, Country = country, City = city, PostalCode = postal_code, Street = street_nr, Email = e_mail)

        try:
            db.session.add(new_user)
            db.session.commit()
            # return redirect('/userprofile')
            return render_template('UserProfile.html', user = new_user)
        except:
            return 'Issue'
    else:
        return render_template('UserProfile.html')

@app.route('/AllArtists', methods=['POST', 'GET'])
def AllArtists():
    artists = Artist.query.all()
    return render_template("AllArtists.html", artists = artists)

@app.route('/AllEventsFiltered/<string:name>', methods=['POST', 'GET'])
def AllEventsFiltered(name):
    events = Event.query.filter_by(artistName = name)
    return render_template("AllEvents.html", events = events)

@app.route('/AllEvents', methods=['POST', 'GET'])
def AllEvents():
    events = Event.query.all()
    return render_template("AllEvents.html", events = events)

@app.route('/findUser', methods=['POST', 'GET'])
def findUser():
    if request.method == "POST":
        userID = request.form['userid']
        user = UserTable.query.get_or_404(userID)
        
        # Session Storage tryout
        # window.sessionStorage.setItem = ('user', user)
        
        events = Event.query.all()
        myconcerts = []
        for event in events:
            for visitor in event.visitors:
                if visitor.id == int(userID):
                    myconcerts.append(event)

        return render_template('UserProfile.html', user = user, concerts = myconcerts)
    else:
        return render_template("UserProfile.html")

@app.route('/myevents', methods=['POST', 'GET'])
def myevents():
    events = Event.query.all()
    myconcerts = []
    for event in events:
        for visitor in event.visitors:
            if visitor.id == 3:
                myconcerts.append(event)
    return render_template("UserProfileMyEvents.html", concerts = myconcerts)

@app.route('/buyticket/<int:eventid>', methods=['POST', 'GET'])
def buyticket(eventid):
    if request.method == 'POST':
        userid = int(request.form['userid'])
        event = Event.query.get_or_404(eventid)
        user = UserTable.query.get_or_404(userid)
        event.visitors.append(user)
        db.session.commit()
        return render_template('UserProfile.html')
    else:
        return render_template('UserProfile.html')

if __name__ == "__main__":
    app.run(debug=True)

from flaskApp.config.mysqlconnection import connectToMySQL
from flask import Flask, render_template, redirect, session, request, flash
from flaskApp import app
from flaskApp.models.booking_mod import Booking_cls
from flaskApp.models.user_mod import User_cls
from flaskApp.models.flight_mod import Flight_cls

# load form to book flight
@app.route('/flights/<int:flight_id>/book/')
def bookFlight(flight_id): 
    data = {
        'id': session['user_id']
    }
    flightData = {
        'id': flight_id
    }
    return render_template(
        'bookFlight.html'
        , display_get_oneUser = User_cls.get_oneUser(data)
        , display_get_oneFlight = Flight_cls.get_oneFlight(flightData))

@app.route("/saveBooking/", methods =['POST'])
def saveBooking():
    data = {
        'tripLeaderFirstName': request.form['tripLeaderFirstName']
        , 'tripLeaderLastName': request.form['tripLeaderLastName']
        , 'passengerCount': request.form['passengerCount']
        , 'passengerCountAdult': request.form['passengerCountAdult']
        , 'flightDate': request.form['flightDate']
        , 'checkedBagsCount': request.form['checkedBagsCount']
        , 'user_id': request.form['user_id']
        , 'flight_id': request.form['flight_id']
    }
    Booking_cls.saveBooking(data)
    return redirect('/dashboard/')


# let's discuss below? 
@app.route('/booking/<int:booking_id>/edit')
def editBooking(booking_id): 
    pass

@app.route('/booking/<int:booking_id>/update')
def updateBooking(booking_id): 
    pass

@app.route('/booking/<int:booking_id>/delete')
def deleteBooking(booking_id): 
    pass
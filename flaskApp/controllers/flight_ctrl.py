from flaskApp import app
from flask import Flask, render_template, redirect, session, request, flash
from flaskApp.models.flight_mod import Flight_cls
from flaskApp.models.airline_mod import Airline_cls
from flaskApp.models import user_mod
from flaskApp.config.mysqlconnection import connectToMySQL # i don't see this in the cohort/melissa file.  but don't we need this?? 

# above is all good, now rock out below. 

@app.route('/flights/')
def flightHome():
    if 'user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
        flash("You must be logged in to view this page.")
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template(
        'flights.html', 
        display_get_allFlight = Flight_cls.get_allFlight(), 
        display_get_allAirline = Airline_cls.get_allAirline(), # let's confirm this line??
        display_user = user_mod.User_cls.getOneUser(data) 
    )

@app.route('/flights/add/')
def addFlight():
    if 'user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
        flash("You must be logged in to view this page.")
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template(
        'addFlight.html' , 
        display_get_allAirline = Airline_cls.get_allAirline(), # let's confirm this line??
        display_user = user_mod.User_cls.getOneUser(data) # don't we need a use data here? 
    )

@app.route('/flights/create/', methods = ['POST'])
def createFlight():
    data = {
        'flightNumber': request.form['flightNumber'], 
        'departureAirport': request.form['departureAirport'], 
        'arrivalAirport': request.form['arrivalAirport'], 
        'airline_id': request.form['airline_id']
    }
    # right here: I want to make an adjustment to the design: upon creating the airline, EU should be redirected to that airline profile/view, not to the airlines directory.  
    # to do above, I think we need to preference the line below with "airline_id = ", then have the return line redirect to the airline view page, i.e. redirect('/airlines/<int:airline_id>/view')
    Flight_cls.saveFlight(data)
    return redirect('flights/')

@app.route('/flights/<int:flight_id>/view')
def viewFlight(flight_id): 
    if 'user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
        flash("You must be logged in to view this page.")
        return redirect('/')
    # why are we sometimes on this ctrl file inserting the userData, but not all? 
    userData = {
        "id": session['user_id']
    }
    data = {
        'id': flight_id
    }
    return render_template(
        'viewFlight.html', 
        display_get_oneFlight = Flight_cls.get_oneFlight(data), 
        display_get_allAirline = Airline_cls.get_allAirline(), 
        display_user = user_mod.User_cls.getOneUser(userData) 
    )

@app.route('/flights/<int:flight_id>/edit')
def editFlight(flight_id): 
    if 'user_id' not in session: 
        flash("You must be logged in to view this page.")
        return redirect('/')
    userData = {
        "id": session['user_id']
    }
    data = {
        'id': flight_id
    }
    return render_template(
        'editFlight.html', 
        display_get_oneFlight = Flight_cls.get_oneFlight(data), 
        display_get_allAirline = Airline_cls.get_allAirline(), 
        display_user = user_mod.User_cls.getOneUser(userData) 
    )

@app.route('/flights/<int:flight_id>/update', methods=['POST'])
def updateFlight(flight_id): 
    data = {
        'id': flight_id, 
        'flightNumber': request.form['flightNumber'], 
        'departureAirport': request.form['departureAirport'], 
        'arrivalAirport': request.form['arrivalAirport']
    }
    Flight_cls.updateFlight(data)
    return redirect(f'flights/{flight_id}/view')

@app.route('/airlines/<int:flight_id>/delete')
def deleteFlight(flight_id): 
    data = {
        'id': flight_id
    }
    Flight_cls.deleteFlight(data)
    # I want to add a flash here that indicates airline was deleted.  Help? 
    return redirect ('/flights/')


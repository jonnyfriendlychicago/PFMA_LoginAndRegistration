from flaskApp import app
from flask import Flask, render_template, redirect, session, request, flash
from flaskApp.models.airline_mod import Airline_cls
from flaskApp.models import user_mod # let's talk about why line above we can import the class directly, but here we need to import the whole model file (that's what we're doing right? )

# below existed originally, but we whacked it b/c now index is gonna be the register/login screen (right?)
# @app.route('/')
# def index():
#     return redirect ('/airlines')

@app.route('/airlines/')
def airlineHome():
    if 'user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
        flash("You must be logged in to view this page.")
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template(
        'airlines.html'
        , display_get_allAirline = Airline_cls.get_allAirline()
        , display_get_oneUser = user_mod.User_cls.get_oneUser(data) 
    )

@app.route('/airlines/add/')
def addAirline():
    if 'user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
        flash("You must be logged in to view this page.")
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template(
        'addAirline.html' , 
        display_user = user_mod.User_cls.get_oneUser(data) 
    )

@app.route('/airlines/create/', methods = ['POST'])
def createAirline():
    data = {
        'airlineName': request.form['airlineName'], 
        'hqCity': request.form['hqCity'], 
        'locationCount': request.form['locationCount'], 
        'workerCount': request.form['workerCount'], 
        'planeCount': request.form['planeCount']
    }
    # right here: I want to make an adjustment to the design: upon creating the airline, EU should be redirected to that airline profile/view, not to the airlines directory.  
    # to do above, I think we need to preference the line below with "airline_id = ", then have the return line redirect to the airline view page, i.e. redirect('/airlines/<int:airline_id>/view')
    Airline_cls.saveAirline(data)
    return redirect('/airlines/')

@app.route('/airlines/<int:airline_id>/view')
def viewAirline(airline_id): 
    if 'user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
        flash("You must be logged in to view this page.")
        return redirect('/')
    # why are we sometimes on this ctrl file inserting the userData, but not all? 
    userData = {
        "id": session['user_id']
    }
    data = {
        'id': airline_id
    }
    get_oneAirlineAllFlight = Airline_cls.get_oneAirlineAllFlight(data)
    print("allFlight: ", get_oneAirlineAllFlight) # let's discuss what we expect to learn/prove in this print statment
    return render_template(
        'viewAirline.html', 
        display_get_oneAirline = Airline_cls.get_oneAirline(data), 
        display_get_oneAirlineAllFlight = get_oneAirlineAllFlight, 
        display_user = user_mod.User_cls.get_OneUser(data) 
    )

@app.route('/airlines/<int:airline_id>/edit')
def editAirline(airline_id): 
    if 'user_id' not in session: 
        flash("You must be logged in to view this page.")
        return redirect('/')
    userData = {
        "id": session['user_id']
    }
    data = {
        'id': airline_id
    }
    return render_template(
        'editAirline.html', 
        display_get_oneAirline = Airline_cls.get_oneAirline(data), 
        display_user = user_mod.User_cls.getOneUser(userData) 
    )

@app.route('/airlines/<int:airline_id>/update', methods=['POST'])
def updateAirline(airline_id): 
    data = {
        'id': airline_id, 
        'airlineName': request.form['airlineName'], 
        'hqCity': request.form['hqCity'], 
        'locationCount': request.form['locationCount'], 
        'workerCount': request.form['workerCount'], 
        'planeCount': request.form['planeCount']
    }
    updateAirline = Airline_cls.updateAirline(data)
    print(updateAirline) # this print statement just shows what's up.  without this line, 'updateAirline' variable should be removed, just state the class.method(x)
    return redirect(f'airlines/{airline_id}/view')

@app.route('/airlines/<int:airline_id>/delete')
def deleteAirline(airline_id): 
    data = {
        'id': airline_id
    }
    Airline_cls.deleteAirline(data)
    # I want to add a flash here that indicates airline was deleted.  Help? 
    return redirect ('/airlines/')


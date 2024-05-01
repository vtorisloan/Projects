from flask_app import app, bcrypt
from flask_app.models.user import User
from flask import flash, render_template, redirect, request, session


@app.get("/")
def index():
    """This route displays the login form"""
    return render_template("index.html")

@app.post("/users/register")
def register():
    """This route processess the registration"""

    # if form not valid redirect
    if not User.registration_is_valid(request.form):
        return redirect("/")
    
    # check if user already exists
    potential_user = User.find_by_email(request.form["email"])

    # if user already exists redirect
    if potential_user is not None:
        flash("Email already exists", "register")
        return redirect("/")
    
    # user does not exist, safe to creat and hash password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    user_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
    }
    user_id = User.register(user_data)

    # save user id in session (log them in)
    session["user_id"] = user_id
    return redirect("/animes/all")

@app.post("/users/login")
def login():
    """This route processes the login"""

    # if form not valid redirect
    if not User.login_is_valid(request.form):
        print("a")
        return redirect("/")

    # check if user exists
    potential_user = User.find_by_email(request.form["email"])

    # if user does not exist redirect
    if potential_user == None:
        flash("invalid credentials", "login")
        print("b")
        return redirect("/")
    
    # user exists
    user = potential_user

    # check if password is correct
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Password is incorrect", "login")
        print("c")
        return redirect("/")
    
    # save user id in session (log them in)
    session["user_id"] = user.id
    return redirect("/animes/all")

@app.post("/animes/all")
def dashboard():
    """This route displayes the user dashboard"""
    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect("/")
    
    user = User.find_by_id(session["user_id"])
    return render_template("all_animes.html", user=user)

@app.get("/users/logout")
def logout():
    """This route logs the user out"""
    session.clear()
    return redirect("/")



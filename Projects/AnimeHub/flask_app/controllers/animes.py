from flask_app import app
from flask_app.models.anime import Anime
from flask_app.models.user import User
from flask_app.models.hub import Hub
from flask import flash, render_template, redirect, request, session


@app.route('/animes/all')
def animes():
    """This route displays all animes"""

    if "user_id" not in session: 
        flash("please log in. ", "login")
        return redirect('/')
    
    animes = Anime.find_all_with_users()
    user_watchlist = Hub.get_all_by_id(session["user_id"])
    print("\n\n\n\nline18 user_watchlist", user_watchlist   )
    user = User.find_by_id(session["user_id"])
    # context = {"animes": animes, "user": user}
    return render_template("all_animes.html", user=user, animes=animes, user_watchlist=user_watchlist)

@app.get("/anime/new")
def new_anime():
    """This route displays the new anime form"""

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    user = User.find_by_id(session["user_id"])
    # context = {"user": user}
    return render_template("new_anime.html", user=user)
    

@app.post('/anime/create')
def create_anime():
    """This route  processes the anime form"""

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    if not Anime.form_is_valid(request.form):
        return redirect("/anime/new")
    
    if Anime.count_by_title(request.form["title"]) >= 1:
        # session["comment"] = request.form["comment"]
        flash("Anime already exists", "error")    
        return redirect("/anime/new")
    
    anime_id = Anime.create(request.form)

    data = {
        "anime_id": anime_id,
        "user_id": session["user_id"],
        "watch_status": "Watching"
    }

    Anime.add_to_watchlist(data)

    
    return redirect("/animes/all")


@app.get('/anime/<int:anime_id>')
def anime_details(anime_id):
    """This route displays the one anime's details"""

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    anime = Anime.find_by_id_with_users(anime_id)
    user = User.find_by_id(session["user_id"])

    return render_template("anime_details.html", user=user, anime=anime)

@app.get('/animes/<int:anime_id>/edit')
def edit_anime(anime_id):
    """This route displays the edit anime form"""

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    anime = Anime.find_by_id(anime_id)
    user = User.find_by_id(session["user_id"])
    return render_template("edit_anime.html", user=user, anime=anime)

@app.post('/animes/update')
def update_anime():
    """this route processes the anime edit"""
   

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    anime_id = request.form["anime_id"]
    if not Anime.form_is_valid(request.form):
        return redirect(f'/animes/{anime_id}/edit')
    
    Anime.update_by_id(request.form)
    return redirect(f'/anime/{anime_id}')

@app.post('/anime/<int:anime_id>/delete')
def delete_anime(anime_id):
    """This route deletes an anime form"""

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect('/')
    
    Anime.delete_by_id(anime_id)
    return redirect('/animes/all')
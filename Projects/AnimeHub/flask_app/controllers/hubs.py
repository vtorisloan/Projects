from flask_app import app
from flask import flash, redirect, request, session
from flask_app.models.hub import Hub


@app.post("/hub/watch")
def watch_hub():
    """This route processes an anime to our watch list"""

    Hub.watch_hub()

    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect("/")

    form_data = {
        "user_id": session["user_id"],
        "anime_id": request.form["anime_id"]
    }
    Hub.watch(form_data)
    return redirect("/hub")



@app.get("/watchlist/remove/<int:anime_id>/<int:user_id>")
def remove(anime_id, user_id):
    """This route removes an anime from our watch list"""
    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect("/")

    form_data = {
        "user_id": user_id,
        "anime_id": anime_id
    }
    Hub.remove(form_data)
    return redirect("/animes/all")

@app.get("/watchlist/add/<int:anime_id>/<int:user_id>")
def add(anime_id, user_id):
    """This route adds an anime to our watch list"""
    if "user_id" not in session:
        flash("please log in. ", "login")
        return redirect("/")

    form_data = {
        "user_id": user_id,
        "anime_id": anime_id,
        "watch_status": "watching"
    }
    Hub.add(form_data)
    return redirect("/animes/all")


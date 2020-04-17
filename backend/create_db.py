import flaskblog

app = flaskblog.create_app()

with app.app_context():
    flaskblog.db.create_all()


from flask import render_template, request, Blueprint, current_app
from flaskblog.models import Post
from flaskblog.config import Config


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    data = {
        "language": "pl-PL",
        "API_URL": current_app.config['API_URL']
    }
    return render_template('main/home.html', data=data)


@main.route("/about")
def about():
    return render_template('main/about.html', title='About')

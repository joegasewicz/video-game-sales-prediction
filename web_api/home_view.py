from flask import render_template, Blueprint

home_view = Blueprint("home_view", __name__)


@home_view.route("/", methods=["GET", "POST"])
def home():
    single_dict = {
        "Year_of_Release": 2025,
        "Critic_Score": 78.0,
        "Critic_Count": 96,
        "User_Score": 81.0,
        "User_Count": 325,
    }
    data = {}
    return render_template("home.jinja2", data=data)


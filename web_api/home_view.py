import os

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from flask import render_template, Blueprint, request
from marshmallow import ValidationError

from web_api.schemas import PredictionSchema

home_view = Blueprint("home_view", __name__)


@home_view.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.jinja2", data=None, errors=None)
    elif request.method == "POST":
        try:
            prediction_inputs = {
                "year_of_release": request.form.get("year_of_release"),
                "critic_score": request.form.get("critic_score"),
                "critic_count": request.form.get("critic_count"),
                "user_score": request.form.get("user_score"),
                "user_count": request.form.get("user_count"),
            }
            schema = PredictionSchema()
            schema.dump(prediction_inputs)
            prediction_loaded = schema.load(prediction_inputs)
            # If we reach here then the form data is validated
            csv_path = "datasets/Video_Games_Sales_as_at_22_Dec_2016.csv"
            df = pd.read_csv(f"{csv_path}")
            X = df[[
                "Year_of_Release",
                "Critic_Score",
                "Critic_Count",
                "User_Score",
                "User_Count",
            ]]
            y = df["EU_Sales"]
            X = X.apply(pd.to_numeric, errors="coerce")
            y = y.apply(pd.to_numeric, errors="coerce")
            X.fillna(0, inplace=True)
            y.fillna(0, inplace=True)
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.4,
            )
            lm = LinearRegression()
            lm.fit(X_train, y_train)
            prediction_inputs = {
                "Year_of_Release": prediction_loaded["year_of_release"],
                "Critic_Score": prediction_loaded["critic_score"],
                "Critic_Count": prediction_loaded["critic_count"],
                "User_Score": prediction_loaded["user_score"],
                "User_Count": prediction_loaded["user_count"],
            }
            single_input_df = pd.DataFrame([prediction_inputs])

            prediction = lm.predict(single_input_df)
            # metric = np.sqrt(metrics.mean_squared_error(y_test, prediction))
            data = {
                "prediction": round(prediction[0], 2),
                # "metric": metric,
            }
            return render_template("home.jinja2", data=data)
        except ValidationError as err:
            err = {
                "message": err.messages,
            }
            data = None
        except ValueError as err:
            err = {
                "message": err,
            }
            data = None
            return render_template("home.jinja2", data=data, errors=err)

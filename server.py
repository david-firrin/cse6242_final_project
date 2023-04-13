from flask import Flask, render_template, request, jsonify
from wtforms import Form, StringField, TextAreaField, validators
from Server_Analyze import Server_Analyze
import pandas as pd
import pdb
import time

app = Flask(__name__)


class AnalyzeForm(Form):
    car_manufacturer = StringField('Select Car Manufacturer', [
                                   validators.DataRequired()])
    car_model = StringField('Select Car Model', [validators.DataRequired()])
    car_type = StringField('Select Car Type', [
        validators.DataRequired()])
    car_condition = StringField('Select Car Condition', [
                                validators.DataRequired()])
    car_cylinder = StringField('Select Number of Cylinders', [
        validators.DataRequired()])
    car_fuel = StringField('Select Car Fuel Type', [
        validators.DataRequired()])
    car_value = StringField('Enter Car Value', [validators.DataRequired()])
    car_year = StringField('Enter Car Year', [validators.DataRequired()])
    car_miles = StringField('Enter Number of Miles', [
                            validators.DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = AnalyzeForm(request.form)
    if request.method == "POST":
        car_value_prediction = Server_Analyze().PredictCarPrice(request.form)
        plot_mileage_age_curves = Server_Analyze().PlotMileageAgeCurve(request.form)
        plot_residuals = Server_Analyze().PlotResiduals(request.form)
        important_parameters = Server_Analyze().GetCarParameters(request.form)
        return jsonify(car_value_prediction=car_value_prediction,
                       plot_mileage_age_curves=plot_mileage_age_curves,
                       plot_residuals=plot_residuals,
                       important_parameters = important_parameters)

    if request.method == 'GET':
        # <!-- miles_10kx  car_age_yearsx  conditionx  title_status  fuelx  typex  modelx  manufacturerx  cylindersx  drive  transmission  paint_color        long        lat -->
        # pdb.set_trace()
        df = pd.read_pickle(
            "data/transform/step_2_preprocessed_data/01_df_no_encoding.pkl")
        car_manufacturers = sorted(df['manufacturer'].unique())
        car_models = sorted(df['model'].unique())
        car_types = sorted(df['type'].unique())
        car_condition = sorted(df['model'].unique())
        car_cylinders = sorted(df['cylinders'].unique())
        car_fuel = sorted(df['fuel'].unique())

        return render_template("index.html",
                               form=form,
                               car_manufacturers=car_manufacturers,
                               car_models=car_models,
                               car_types=car_types,
                               car_cylinders=car_cylinders,
                               car_fuel=car_fuel)


if __name__ == "__main__":
    app.run(host="localhost", port=4500, debug=True)

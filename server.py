from flask import Flask, render_template, request, jsonify, session
import uuid
from wtforms import Form, StringField, TextAreaField, validators
from Server_Analyze import Server_Analyze
import pandas as pd
import pdb
import time

app = Flask(__name__)
app.secret_key = 'some_secret_key'


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
    df = pd.read_pickle(
        "data/transform/step_2_preprocessed_data/01_df_no_encoding.pkl")

    if request.method == "POST":
        page_name = request.form['page']
        if page_name == 'car_manufacturer':
            form_data = {
                'last_page': None,
                'current_page':  page_name,
                'next_page': 'car_model',
                'inputs': [
                    {
                        'label':  'Please select a car manufacturer',
                        'data':  sorted(df['manufacturer'].unique())
                    }
                ]
            }
        elif page_name == 'car_model':
            # Get the car manufacturer depending on whether next/back button pushed
            if request.form['direction'] == 'next':
                selected_car_manufacturer = request.form['my-form']
                session['car_manufacturer'] = selected_car_manufacturer
            elif request.form['direction'] == 'last':
                selected_car_manufacturer = session['car_manufacturer']
            print(session)
            # Filter Data
            car_models = df[df['manufacturer'] == selected_car_manufacturer]
            car_models = sorted(car_models['model'].unique())

            form_data = {
                'last_page': 'car_manufacturer',
                'current_page':  page_name,
                'next_page': 'car_fuel',
                'inputs': [
                    {
                        'label':  'Please select a car model',
                        'data':  car_models
                    }
                ]
            }

        elif page_name == 'car_fuel':
            # Get the car model depending on whether next/back button pushed
            if request.form['direction'] == 'next':
                selected_car_model = request.form['my-form']
                session['car_model'] = request.form['my-form']
            elif request.form['direction'] == 'last':
                selected_car_model = session['car_model']
            print(session)
            # Filter Data
            car_fuel_types = df[df['model'] == selected_car_model]
            car_fuel_types = sorted(car_fuel_types['fuel'].unique())
            form_data = {
                'last_page': 'car_model',
                'current_page':  page_name,
                'next_page': 'car_cylinders',
                'inputs': [
                    {
                        'label': "Please select your car's energy source",
                        'data':  car_fuel_types
                    }
                ]
            }

        elif page_name == 'car_cylinders':
            # Get the car model depending on whether next/back button pushed
            if request.form['direction'] == 'next':
                selected_car_model = session['car_model']
                selected_fuel_type = request.form['my-form']
                session['car_fuel'] = selected_fuel_type
            elif request.form['direction'] == 'last':
                selected_car_model = session['car_model']
                selected_fuel_type = session['car_fuel']
            print(session)
            # Filter Data
            filter_1 = df['model'] == selected_car_model
            filter_2 = df['fuel'] == selected_fuel_type
            car_cylinder_numbers = df[filter_1 & filter_2]
            car_cylinder_numbers = sorted(
                car_cylinder_numbers['cylinders'].unique())
            form_data = {
                'last_page': 'car_fuel',
                'current_page':  page_name,
                'next_page': 'car_transmission',
                'inputs': [
                    {
                        'label': "Please select your car's number of cylinders",
                        'data':  car_cylinder_numbers
                    }
                ]
            }
        elif page_name == 'car_transmission':
            # Get the car model depending on whether next/back button pushed
            if request.form['direction'] == 'next':
                selected_car_model = session['car_model']
                selected_car_cylinders = request.form['my-form']
                session['car_cylinders'] = selected_car_cylinders
            elif request.form['direction'] == 'last':
                selected_car_model = session['car_model']
                selected_car_cylinders = session['car_cylinders']
            print(session)
            # Filter Data
            # pdb.set_trace()
            filter_1 = df['model'] == selected_car_model
            filter_2 = df['cylinders'] == selected_car_cylinders
            car_transmission = df[filter_1 & filter_2]
            car_transmission = sorted(
                car_transmission['transmission'].unique())

            form_data = {
                'last_page': 'car_cylinders',
                'current_page':  page_name,
                'next_page': 'car_drive',
                'inputs': [
                    {
                        'label': "Please select your car's transmission type",
                        'data':  car_transmission
                    }
                ]
            }
        elif page_name == 'car_drive':
            # Get the car model depending on whether next/back button pushed
            if request.form['direction'] == 'next':
                selected_car_model = session['car_model']
                selected_car_transmission = request.form['my-form']
                session['car_transmission'] = selected_car_transmission
            elif request.form['direction'] == 'last':
                selected_car_model = session['car_model']
                selected_car_transmission = session['car_transmission']

            print(session)
            # Filter Data
            filter_1 = df['model'] == selected_car_model
            filter_2 = df['transmission'] == selected_car_transmission
            car_drive = df[filter_1 & filter_2]
            car_drive = sorted(car_drive['drive'].unique())

            form_data = {
                'last_page': 'car_transmission',
                'current_page':  page_name,
                'next_page': 'car_miles',
                'inputs': [
                    {
                        'label': "Please select your car's drive type",
                        'data':  car_drive
                    }
                ]
            }
        elif page_name == 'car_miles':
            # Get the car model depending on whether next/back button pushed
            if request.form['direction'] == 'next':
                selected_car_drive = request.form['my-form']
                session['car_drive'] = selected_car_drive
            elif request.form['direction'] == 'last':
                selected_car_drive = session['car_drive']
            print(session)
            form_data = {
                'last_page': 'car_drive',
                'current_page':  page_name,
                'next_page': 'car_years',
                'inputs': [
                    {
                        'label': "Please input your car's miles",
                        'data':  None
                    }
                ]
            }
        elif page_name == 'car_years':
            # Get the car model depending on whether next/back button pushed
            if request.form['direction'] == 'next':
                selected_car_miles = request.form['my-form']
                session['car_miles'] = float(selected_car_miles)
            elif request.form['direction'] == 'last':
                selected_car_miles = session['car_miles']
            print(session)
            form_data = {
                'last_page': 'car_miles',
                'current_page':  page_name,
                'next_page': 'car_condition',
                'inputs': [
                    {
                        'label': "Please input your car's year",
                        'data':  None
                    }
                ]
            }
        elif page_name == 'car_condition':
            # Get the car model depending on whether next/back button pushed
            if request.form['direction'] == 'next':
                selected_car_years = request.form['my-form']
                session['car_years'] = float(selected_car_years)
            elif request.form['direction'] == 'last':
                selected_car_years = session['car_years']
            car_condition = sorted(df['condition'].unique())
            form_data = {
                'last_page': 'car_years',
                'current_page':  page_name,
                'next_page': 'car_color',
                'inputs': [
                    {
                        'label': "Please input your car's condition",
                        'data':  car_condition
                    }
                ]
            }
        elif page_name == 'car_color':
            # Get the car model depending on whether next/back button pushed
            if request.form['direction'] == 'next':
                selected_car_condition = request.form['my-form']
                session['car_condition'] = selected_car_condition
            elif request.form['direction'] == 'last':
                selected_car_condition = session['car_condition']
            car_color = sorted(df['paint_color'].unique())
            form_data = {
                'last_page': 'car_condition',
                'current_page':  page_name,
                'next_page': 'car_value',
                'inputs': [
                    {
                        'label': "Please input your car's condition",
                        'data':  car_color
                    }
                ]
            }
        elif page_name == 'car_value':
            # Get the car model depending on whether next/back button pushed
            if request.form['direction'] == 'next':
                selected_car_color = request.form['my-form']
                session['car_color'] = request.form['my-form']
            elif request.form['direction'] == 'last':
                selected_car_color = session['car_color']
            form_data = {
                'last_page': 'car_color',
                'current_page':  page_name,
                'next_page': 'check_inputs',
                'inputs': [
                    {
                        'label': "Please input your car's value",
                        'data':  None
                    }
                ]
            }

        elif page_name == 'check_inputs':
            # Get the car model depending on whether next/back button pushed
            if request.form['direction'] == 'next':
                selected_car_value = request.form['my-form']
                session['car_value'] = float(selected_car_value)
            elif request.form['direction'] == 'last':
                selected_car_value = session['car_value']
            inputted_data = Server_Analyze().encode_data(session)
            form_data = {
                'last_page': 'car_value',
                'current_page': page_name,
                'next_page': 'analyze',
                'inputs': inputted_data
            }
            return render_template('check_inputs.html',
                                   form_data=form_data)

        elif page_name == 'analyze':
            car_value_prediction = Server_Analyze().PredictCarPrice(session)
            plot_mileage_age_curves = Server_Analyze().PlotMileageAgeCurve(session)
            important_parameters = Server_Analyze().GetCarParameters(session)
            form_data = {
                'current_page': page_name,
                'car_value_predicticion': car_value_prediction,
                'plot_mileage_age_curves': plot_mileage_age_curves,
                'important_parameters': important_parameters
            }
            return render_template('analyze.html',
                                   form_data=form_data)

        return render_template('form_template.html',
                               form_data=form_data)

    if request.method == 'GET':
        session_id = request.cookies.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
        # <!-- miles_10kx  car_age_yearsx  conditionx  title_status  fuelx  typex  modelx  manufacturerx  cylindersx  drive  transmission  paint_color        long        lat -->
        # pdb.set_trace()
        # df = pd.read_pickle(
        #     "data/transform/step_2_preprocessed_data/01_df_no_encoding.pkl")
        # car_manufacturers = sorted(df['manufacturer'].unique())
        # car_models = sorted(df['model'].unique())
        # car_types = sorted(df['type'].unique())
        # car_condition = sorted(df['model'].unique())
        # car_cylinders = sorted(df['cylinders'].unique())
        # car_fuel = sorted(df['fuel'].unique())

        return render_template("index.html")

        #    form=form,
        #    car_manufacturers=car_manufacturers,
        #    car_models=car_models,
        #    car_types=car_types,
        #    car_cylinders=car_cylinders,
        #    car_fuel=car_fuel


if __name__ == "__main__":
    app.run(host="localhost", port=2500, debug=True)

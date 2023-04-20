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
    '''
    car manufacturer - 1
    car model - 1
    car type - 1

    car fuel
    car cylinders
    car transmission
    car drive


    '''
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
                'prompt': "What brand is your car?",
                'prompt_instructions': "Please select your car's manufacturer from the dropdown below.",
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
                'prompt': "What's your car's model?",
                'prompt_instructions': "Please select your car's model from the dropdown below.",
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
                car_type = df[df['model'] ==
                              selected_car_model]['type'].unique()
                # pdb.set_trace()
                if len(car_type) == 1:
                    session['car_type'] = car_type[0]
                else:
                    print('make car type separate')

                session['car_model'] = request.form['my-form']

            elif request.form['direction'] == 'last':
                selected_car_model = session['car_model']
            print(session)
            # Filter Data
            car_fuel_types = df[df['model'] == selected_car_model]
            car_fuel_types = sorted(car_fuel_types['fuel'].unique())
            # Remove 'nan' values
            car_fuel_types = [x for x in car_fuel_types if 'nan' not in x]
            form_data = {
                'last_page': 'car_model',
                'current_page':  page_name,
                'next_page': 'car_cylinders',
                'prompt': 'What kind of fuel does your car take?',
                'prompt_instructions': 'Please select a fuel type from the dropdown below.',
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
            # Remove 'nan' value
            car_cylinder_numbers = [
                x for x in car_cylinder_numbers if 'nan' not in x]
            form_data = {
                'last_page': 'car_fuel',
                'current_page':  page_name,
                'next_page': 'car_transmission',
                'prompt': 'How many cylinders does your car have?',
                'prompt_instructions': "Please select your car's number of cylinders from the dropdown below.",
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
                'prompt': "Is your car an automatic, or manual?",
                'prompt_instructions': "Please select whether your car is an automatic, stick shift, or other from the dropdown below.",
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
            # Remove 'nan' values from output
            car_drive = [x for x in car_drive if 'nan' not in x]
            form_data = {
                'last_page': 'car_transmission',
                'current_page':  page_name,
                'next_page': 'car_miles',
                'prompt': "What's your car's drive type?",
                'prompt_instructions': "Please select whether your car is Front Wheel Drive(FWD), Rear-Wheel Drive(RWD) \
                                        or Four Drive(4WD) from the dropdown below.",
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
                'prompt': "How many miles has your car racked up?",
                'prompt_instructions': "Please enter the total number of miles on your car below.",
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
                'prompt': "What year is your car?",
                'prompt_instructions': "Please enter the year your car was made below.",
                'inputs': [
                    {
                        'label': "Please input your car's year",
                        'data':  [year for year in range(1950, 2023)]
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
            print(car_condition)
            form_data = {
                'last_page': 'car_years',
                'current_page':  page_name,
                'next_page': 'car_color',
                'prompt': "How would you describe the condition of your car?",
                'prompt_instructions': "Please choose the option that best describes your vehicle's condition using the dropdown below.",
                'inputs': [
                    {
                        'label': "Please input your car's condition",
                        'data':  ['new', 'like new', 'excellent', 'good', 'fair', 'salvage']
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
            car_color = [x for x in car_color if 'nan' not in x]
            form_data = {
                'last_page': 'car_condition',
                'current_page':  page_name,
                'next_page': 'car_value',
                'prompt': "What color is your car?",
                'prompt_instructions': "Please choose the option that is closest to the color of your car.",
                'inputs': [
                    {
                        'label': "Please input your car's color",
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
                'prompt': "What is the value of the car you're looking to buy or sell?",
                'prompt_instructions': "Please input a valid number for the value of the car you're looking to buy or sell",
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

            inputted_data = Server_Analyze().encode_data(session, as_list=False)
            inputted_data['car_value'] = session['car_value']
            form_data = {
                'last_page': 'car_value',
                'current_page': page_name,
                'next_page': 'analyze',
                'inputs': inputted_data
            }
            return render_template('check_inputs.html',
                                   form_data=form_data)

        # elif page_name == 'analyze':
        #     inputted_data = Server_Analyze().encode_data(session, as_list=False)
        #     car_value_prediction = Server_Analyze().PredictCarPrice(session)
        #     plot_mileage_age_curves = Server_Analyze().PlotMileageAgeCurve(session)
        #     important_parameters = Server_Analyze().GetCarParameters(session)
        #     anomoly_detection = Server_Analyze().Anomaly_Detection(session)
        #     # pdb.set_trace()
        #     form_data = {
        #         'current_page': None,
        #         'car_value_prediction': car_value_prediction,
        #         'plot_mileage_age_curves': plot_mileage_age_curves,
        #         'important_parameters': important_parameters,
        #         'inputs': inputted_data,
        #         'anomoly_detection': str(anomoly_detection)
        #     }
        #     return render_template('analyze.html',
        #                            form_data=form_data)

        return render_template('form_template.html',
                               form_data=form_data)

    if request.method == 'GET':
        session_id = request.cookies.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())

        form_data = {
            'last_page': None,
            'current_page': 'opening',
            'next_page': None,
            'inputs': None
        }

        return render_template("index.html", form_data=form_data)


@app.route('/analyze', methods=['POST'])
def analyze():
    # pdb.set_trace()
    inputted_data = Server_Analyze().encode_data(session, as_list=False)
    car_value_prediction = Server_Analyze().PredictCarPrice(session)
    plot_mileage_age_curves = Server_Analyze().PlotMileageAgeCurve(session)
    important_parameters = Server_Analyze().GetCarParameters(session)
    anomoly_detection = Server_Analyze().Anomaly_Detection(session)
    # pdb.set_trace()
    form_data = {
        'current_page': None,
        'car_value_prediction': car_value_prediction,
        'plot_mileage_age_curves': plot_mileage_age_curves,
        'important_parameters': important_parameters,
        'inputs': inputted_data,
        'anomoly_detection': str(anomoly_detection)
    }
    return render_template('analyze.html',
                            form_data=form_data)

if __name__ == "__main__":
    app.run(host="localhost", port=2500, debug=True)

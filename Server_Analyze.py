from sklearn.preprocessing import LabelEncoder
import pickle
import pandas as pd
import numpy as np
from pygam import GAM, GammaGAM
import pdb
from sklearn.model_selection import train_test_split
import random
from user_interface_model_utils import UserInterfaceModelUtils


class Server_Analyze(UserInterfaceModelUtils):
    def __init__(self):
        with open('data/transform/step_3_GAM_model/gam_1.pkl', 'rb') as f_gam:
            self.gam_model = pickle.load(f_gam)

        with open('data/transform/step_2_preprocessed_data/01_df.pkl', 'rb') as f_gam:
            self.encoded_data = pickle.load(f_gam)
        self.get_training_data(self.encoded_data)

    def get_training_data(self, df):
        train, test = train_test_split(df, test_size=0.20, random_state=0)

        self.X_train = train.drop('price', axis=1)
        self.X_test = test.drop('price', axis=1)
        self.y_train = train['price']
        self.y_test = test['price']
        # return X_train, X_test, y_train, y_test

    def encode_data(self, session, as_list=True, alter=False):
        form_data = {
            'car_miles': session['car_miles'],  # car miles
            'car_years': session['car_years'],  # car year
            'car_condition': session['car_condition'],  # car condition
            'car_title': 'clean',  # title status
            'car_fuel': session['car_fuel'],  # fuel
            'car_type': session['car_type'],  # type
            'car_model': session['car_model'],  # car model
            'car_manufacturer': session['car_manufacturer'],
            'car_cylinders': session['car_cylinders'],  # cylinders
            'car_drive': session['car_drive'],  # drive
            'car_transmission': session['car_transmission'],  # transmission
            'car_color': session['car_color'],  # paint color
            'longitude': -85.4800,  # longitude
            'latitude': 32.590  # latitude
        }
        if alter == True:
            form_data['car_miles'] = form_data['car_miles'] / 10_000
            form_data['car_years'] = 2023 - form_data['car_years']
        if as_list == True:
            form_data = list(form_data.values())
        return form_data

    def GetCarParameters(self, session):
        encoded_data = self.encode_data(session)
        important_parameters = UserInterfaceModelUtils(
            assets_path='user_interface_utils_assets').get_n_most_important_variables(encoded_data)
        return important_parameters

    def PredictCarPrice(self, session):
        '''
        miles_10k  car_age_years  condition  title_status  fuel  type  model  manufacturer  cylinders  drive  transmission  paint_color        long        lat
        '''
        encoded_data = self.encode_data(session, alter=True)
        # y_test_pred = self.gam_model.predict(encoded_data)
        # predicted_car_price = round(float(y_test_pred[0]))

        predicted_car_price = UserInterfaceModelUtils(
            assets_path='user_interface_utils_assets').predict(encoded_data)

        # Calculate whether car is a good or bad deal:
        user_inputted_car_price = float(session['car_value'])

        # if predicted_car_price > user_inputted_car_price:
        #     deal_assessment = 'good'
        # elif predicted_car_price < user_inputted_car_price:
        #     deal_assessment = 'bad'
        car_value_prediction = {
            'predicted_car_price': predicted_car_price['prediction'],
            'user_inputted_car_price': user_inputted_car_price,
            'deal_assessment': 'good'
        }
        return car_value_prediction

    def Percentiles(self, session):
        '''
        Get the percentiles of the car's price per make and model
        'Your car is 35% more expensive than other car's of the same make and model'
        'Your car is 55% more expensive than other car's that are in the same condition'
        '''

    def PlotMileageAgeCurve(self, form_request):
        miles_pd_X = self.gam_model.generate_X_grid(term=0)[:, 0]
        age_pd_X = self.gam_model.generate_X_grid(term=1)[:, 1]

        miles_pd_log = self.gam_model.partial_dependence(term=0)
        age_pd_log = self.gam_model.partial_dependence(term=1)

        miles_pd_exp = np.exp(miles_pd_log)
        age_pd_exp = np.exp(age_pd_log)

        plot_mileage_age_curves = {
            'miles_pd_X': miles_pd_X.tolist(),
            'age_pd_X': age_pd_X.tolist(),
            'miles_pd_exp': miles_pd_exp.tolist(),
            'age_pd_exp': age_pd_exp.tolist(),
            'miles_pd_log': miles_pd_log.tolist(),
            'age_pd_log': age_pd_log.tolist()
        }
        return plot_mileage_age_curves

    def Anomaly_Detection(self, session):
        with open('data/anomoly_files/ad_model.pkl', 'rb') as model:
            ad_model = pickle.load(model)

        with open('data/anomoly_files/ad_label_encoders.pkl', 'rb') as model:
            ad_label_encoders = pickle.load(model)

        def is_anomaly(x_input, encoders, ad_model):
            # x_input needs to be a dataframe and
            # have columns miles, car_age_years, model, manufacturer, cylinders
            actual = x_input['miles']
            x_input = x_input.iloc[:, 1:]

            factor_vars = [
                'model',
                'manufacturer',
                'cylinders']

            for var in factor_vars:
                x_input[var] = encoders[var].transform(x_input[var])

            transformed_input = x_input

            pred_mileage = ad_model.predict(transformed_input)
            # print(pred_mileage)

            return pred_mileage > actual * 1.4

        # example invocation
        # Create a dictionary with your input data
        # data = {'miles': [32485.0], 'car_age_years': [2.459],
        #         'model': ['Tundra'], 'manufacturer': ['Toyota'],
        #         'cylinders': ['4 cylinders']}

        data = self.encode_data(session, as_list=False)
        # Create a dataframe from the dictionary
        x_input = pd.DataFrame([data])
        
        x_input = x_input[['car_miles', 'car_years',
                           'car_model', 'car_manufacturer', 'car_cylinders']]
        x_input.columns = ['miles', 'car_age_years',
                           'model', 'manufacturer', 'cylinders']
        anomoly = is_anomaly(x_input, ad_label_encoders, ad_model)
        anomoly = anomoly[0]
        # pdb.set_trace()
        return anomoly

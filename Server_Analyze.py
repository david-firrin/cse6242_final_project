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

    def encode_data(self, session, as_list=True):
        form_data = {
            'car_miles': session['car_miles'],  # car miles
            'car_years': session['car_years'],  # car year
            'car_condition': session['car_condition'],  # car condition
            'car_title': 'clean',  # title status
            'car_fuel': session['car_fuel'],  # fuel
            'car_type': session['car_type'],  # type
            'car_model': session['car_model'],  # car model
            'car_manufacturer': session['car_manufacturer'], # car manufacturer
            'car_cylinders': session['car_cylinders'],  # cylinders
            'car_drive': session['car_drive'],  # drive
            'car_transmission': session['car_transmission'],  # transmission
            'car_color': session['car_color'],  # paint color
            'longitude': -85.4800,  # longitude
            'latitude': 32.590  # latitude
        }
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
        encoded_data = self.encode_data(session)
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
            'predicted_car_price': predicted_car_price,
            'user_inputted_car_price': user_inputted_car_price,
            'deal_assessment': 'good'
        }
        return car_value_prediction

    def PlotMileageAgeCurve(self, form_request):
        miles_pd_X = self.gam_model.generate_X_grid(term=0)[:, 0]
        age_pd_X = self.gam_model.generate_X_grid(term=1)[:, 1]

        miles_pd_log = self.gam_model.partial_dependence(term=0)
        age_pd_log = self.gam_model.partial_dependence(term=1)

        # encoded_data = self.encode_data(form_request)
        # user_miles = encoded_data.iloc[0]['miles_10k']
        # user_car_age = encoded_data.iloc[0]['car_age_years']

        # def get_user_miles_PD(user_miles):
        #     X_grid = self.gam_model.generate_X_grid(term=0)
        #     X_grid[:, 0] = user_miles
        #     pd_value = self.gam_model.partial_dependence(term=0, X=X_grid)
        #     return np.exp(pd_value[0])

        # def get_user_car_age_PD(user_car_age):
        #     X_grid = self.gam_model.generate_X_grid(term=1)
        #     X_grid[:, 1] = user_car_age
        #     pd_value = self.gam_model.partial_dependence(term=1, X=X_grid)
        #     return np.exp(pd_value[0])

        # user_car_age_PD = get_user_car_age_PD(user_car_age)
        # user_miles_PD = get_user_miles_PD(user_miles)

        miles_pd_exp = np.exp(miles_pd_log)
        age_pd_exp = np.exp(age_pd_log)

        plot_mileage_age_curves = {
            'miles_pd_X': miles_pd_X.tolist(),
            'age_pd_X': age_pd_X.tolist(),
            'miles_pd_exp': miles_pd_exp.tolist(),
            'age_pd_exp': age_pd_exp.tolist(),
            'miles_pd_log': miles_pd_log.tolist(),
            'age_pd_log': age_pd_log.tolist(),
            # 'user_car_age_PD': {'user_input': user_miles, 'PD': user_car_age_PD},
            # 'user_miles_PD': {'user_input': user_car_age, 'PD': user_miles_PD}
        }
        return plot_mileage_age_curves

    # def PlotResiduals(self, form_request):
    #     y_train_hat = self.gam_model.predict_mu(self.X_train)
    #     residuals = self.gam_model.deviance_residuals(
    #         self.X_train, self.y_train)

    #     # random_resid_idxs = random.sample(range(len(residuals)), 10)
    #     # residuals_subset = [residuals[i] for i in random_resid_idxs]

    #     # pdb.set_trace()
    #     plot_residuals = {
    #         # 'X_train': self.X_train,
    #         # 'X_test': self.X_test,
    #         # 'Y_train': self.y_train,
    #         # 'Y_test': self.y_test,
    #         'y_train_hat': y_train_hat.tolist(),
    #         'residuals': residuals.tolist()
    #     }
    #     return plot_residuals

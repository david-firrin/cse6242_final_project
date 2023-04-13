from os import PathLike as os_PathLike
from os.path import join as os_path_join
from pickle import load as pickle_load
from numpy import abs as np_abs
from numpy import array, ndarray
from pandas import DataFrame
from typing import List
import pdb

class UserInterfaceModelUtils:

    '''
    This class provides functionality for getting the most important predictors
    given some user input. Once loaded, getting the most important 
    predictors should be as simple as calling 
    Object.get_n_most_important_variables.

    This object needs to load some assets (GAM object, 
    label encoders, and sklearn.k_means object to convert coordinates to
    cluster). These objects should be stored in pickle format and within
    a shared directory. Alternatively, feel free to modify this.
    '''

    def __init__(
        self, 
        assets_path: os_PathLike,
        model_n_most: int = 25,
        manufacturer_n_most: int = 7
    ):
        
        '''
        params:
        assets_path -- path to directory containing the files gam.pkl, 
        df_label_encoders.pkl, and k_means_coords.pkl

        model_n_most -- number of models to include as important factor; see

        manufacturer_n_most -- analagous to model_n_most
        '''

        gam_path = os_path_join(assets_path, 'gam.pkl')
        label_encoders_path = os_path_join(assets_path, 'df_label_encoders.pkl')
        k_means_coords_path = os_path_join(assets_path, 'k_means_coords.pkl')

        with open(gam_path, 'rb') as f:
            self.gam = pickle_load(f)

        with open(label_encoders_path, 'rb') as f:
            self.label_encoders = pickle_load(f)

        with open(k_means_coords_path, 'rb') as f:
            self.k_means_coords = pickle_load(f)  

        self.gam_coef = {}
        self.gam_coef['condition'] = self.gam.coef_[20:26]
        self.gam_coef['title_status'] = self.gam.coef_[26:30]
        self.gam_coef['fuel'] = self.gam.coef_[30:35]
        self.gam_coef['type'] = self.gam.coef_[35:46]
        self.gam_coef['model'] = self.gam.coef_[46:246]
        self.gam_coef['manufacturer'] = self.gam.coef_[246:280]
        self.gam_coef['cylinders'] = self.gam.coef_[280:288]
        self.gam_coef['drive'] = self.gam.coef_[288:292]
        self.gam_coef['transmission'] = self.gam.coef_[292:295]
        self.gam_coef['paint_color'] = self.gam.coef_[295:308]
        self.gam_coef['cluster'] = self.gam.coef_[308:408]

        self.models_top = self.__get_superlative_factors__(
            self.gam_coef['model'], model_n_most
        )     

        self.manufacturers_top = self.__get_superlative_factors__(
            self.gam_coef['manufacturer'], manufacturer_n_most
        )    

    def __get_superlative_factors__(
        self,
        factor_coef: ndarray, 
        n_factor: int, 
        is_abs: bool = False,
    ):
                    
        # is_abs ---> largest and smallest magnitude coefficients
        # not is_abs ---> most negative / positive coefficients
            
        factor_coef = np_abs(factor_coef) if is_abs else factor_coef
        argsort = factor_coef.argsort()
        smallest_factor_idx = argsort[:n_factor]
        largest_factor_idx = argsort[-n_factor:]

        return {'smallest': smallest_factor_idx, 'largest': largest_factor_idx}
        
    def __convert_user_input_to_data_vector__(self, X: List):

        '''
        Converts user input data vector into form suitable for model
        '''

        # Assume X is provided from user-input

        coords = DataFrame({
            'long': float(X[12]), 
            'lat': float(X[13])
        }, index=[0])

        cluster = int(self.k_means_coords.predict(coords))
        
        return array([
            float(X[0]), 
            float(X[1]), 
            int(self.label_encoders['condition'].transform([X[2]])),
            int(self.label_encoders['title_status'].transform([X[3]])),
            int(self.label_encoders['fuel'].transform([X[4]])),
            int(self.label_encoders['type'].transform([X[5]])),
            int(self.label_encoders['model'].transform([X[6]])),
            int(self.label_encoders['manufacturer'].transform([X[7]])),
            int(self.label_encoders['cylinders'].transform([X[8]])),
            int(self.label_encoders['drive'].transform([X[9]])),
            int(self.label_encoders['transmission'].transform([X[10]])),
            int(self.label_encoders['paint_color'].transform([X[11]])),
            float(X[12]),
            float(X[13]),
            int(cluster),
        ])
    
    def get_n_most_important_variables(self, X: List, n_vars: int = 3):

        '''
        Get n most variables with largest contribution to car's predicted price

        params:
        X -- list; should have user-inputted style (e.g., model is str not int)
        n_vars -- number of variables to output

        returns:
        List with n_vars elements; each element is a (string, string) tuple 
        where the 1st value gives the variable name and the 2nd value denotes
        whether the variable has a positive or negative effect on price;
        Variables are sorted in decreasing order of magnitude of 
        effect on price
        '''
        
        # Assume X is provided from user-input
        X = self.__convert_user_input_to_data_vector__(X)

        importance = []

        factor_var_idx_name = [
            (2, 'condition'), (3, 'title_status'), (5, 'type'),
            (8, 'cylinders'), (9, 'drive'), (10, 'transmission'), 
            (14, 'cluster')
        ]
            
        importance = [
            (var_name, self.gam_coef[var_name][int(X[var_idx])])
            for var_idx, var_name in factor_var_idx_name
        ]

        importance = sorted(importance, key=lambda x: abs(x[1]), reverse=True)
        importance = [(v[0], '+' if v[1] >= 0 else '-') for v in importance]

        if X[0] <= 5:
            importance = [('miles_10k', '+')] + importance
        elif X[0] >= 35:
            importance = [('miles_10k', '-')] + importance  

        if X[1] <= 2:
            importance = [('car_age_years', '+')] + importance
        elif X[1] >= 35:
            importance = [('car_age_years', '-')] + importance

        if X[7] in self.manufacturers_top['largest']:
            importance = [('manufacturer', '+')] + importance
        elif X[7] in self.manufacturers_top['smallest']:
            importance = [('manufacturer', '-')] + importance

        if X[6] in self.models_top['largest']:
            importance = [('model', '+')] + importance
        elif X[6] in self.models_top['smallest']:
            importance = [('model', '-')] + importance

        importance = importance[:n_vars]
        return {
            i: {'variable': v[0], 'effect': v[1]} 
            for i, v in enumerate(importance)
        }
    
    def predict(self, X: List):

        X = self.__convert_user_input_to_data_vector__(X)
        prediction = self.gam.predict(X.reshape(1, -1))[0]
        return {'prediction': prediction}


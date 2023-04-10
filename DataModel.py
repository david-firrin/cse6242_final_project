import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from pygam import GAM, GammaGAM
from pygam import f, s, te
import pdb


class DataModel:

    def __init__(self):
        self.prepocess_path = 'data/transform/step_2_preprocessed_data/'
        self.model_path = 'data/transform/step_3_GAM_model/'

        self.factor_vars = [
            'condition',
            'title_status',
            'fuel',
            'type',
            'model',
            'manufacturer',
            'cylinders',
            'drive',
            'transmission',
            'paint_color'
        ]

    def model(self):
        df, label_encoders = self.load_data()
        X_train, X_test, y_train, y_test = self.train_test_split_data(df)
        # self.train_GAM_Model(X_train, y_train)
        gam_model = self.load_gam_model()
        pdb.set_trace()
        y_test_pred = gam_model.predict(X_test)
        print('yo')
        self.PredictCarPrice(gam_model, X_test)



    def load_data(self):
        # Load Label Encoders
        with open(self.prepocess_path + 'df_label_encoders.pkl', 'rb') as f_label_encoders:
            label_encoders = pickle.load(f_label_encoders)
        # Load Data
        df = pd.read_pickle(self.prepocess_path + '01_df.pkl')
        return df, label_encoders

    def train_test_split_data(self, df):
        train, test = train_test_split(df, test_size=0.20, random_state=0)

        # Remove price since it's the target variable
        X_train = train.drop('price', axis=1)
        # Remove price since it's the target variable
        X_test = test.drop('price', axis=1)

        y_train = train['price']
        y_test = test['price']
        return X_train, X_test, y_train, y_test

    def train_GAM_Model(self, X_train, y_train):
        # Splines
        gam_2_model = s(0, n_splines=10, lam=0.6)
        gam_2_model += s(1, n_splines=10, lam=0.6)

        # Factors
        for var in self.factor_vars:
            idx = X_train.columns.get_loc(var)
            gam_2_model += f(idx)

        # Interactions
        gam_2_model += te(s(0, n_splines=10, lam=0.6), f(7)) # miles*manufacturer
        gam_2_model += te(s(1, n_splines=10, lam=0.6), f(7)) # age*manufacturer
        gam_2_model += te(f(2), f(7))                        # condition*manufacturer

        gam_2 = GammaGAM(gam_2_model).fit(X_train, y_train)
        with open(self.model_path + 'gam_2.pkl', 'wb') as f_gam:
            pickle.dump(gam_2, f_gam)
    
    def load_gam_model(self):
        with open(self.model_path + 'gam_1.pkl', 'rb') as f_gam:
            gam_2 = pickle.load(f_gam)
        return gam_2

    def PredictCarPrice(self, gam_model, X_test):
        pdb.set_trace()
        y_test_pred = gam_model.predict(X_test)
        print('yo')


if __name__ == "__main__":
    DataModel().model()

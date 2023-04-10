import time
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pdb


class DataPreprocess:

    def clean_data(self):
        df = pd.read_pickle('data/transform/step_1_cleaned_data/01_df.pkl')
        df = df.drop(['region', 'state'], axis=1)
        df = df.replace({'missing': pd.NA})

        # Drop NA in modelled columns
        df = df.dropna(subset=['condition', 'title_status'])

        # Remove cars less than $1k
        df = df[df['price'] >= 1000]

        # Convert mileage to 10k miles (more interpretable coeff)
        df = df.rename(columns={'odometer': 'miles_10k'})
        df['miles_10k'] /= 10000
        df = df[df['miles_10k'] <= 40]  # Removes about 80 observations

        # Get approximate age of car in years
        df['year'] = pd.to_datetime(df['year'], format='%Y')
        df['car_age_years'] = (df['posting_date'] - df['year'])
        df['car_age_years'] = df['car_age_years'].clip(pd.Timedelta('0 days'))
        df['car_age_years'] /= pd.Timedelta('365 days')
        df = df.drop(['posting_date', 'year'], axis=1)

        def get_manufacturer(s: str) -> str:

            if 'Mazda' in s:
                return 'Mazda'
            elif 'Alfa Romeo' in s:
                return 'Alfa-Romeo'
            elif 'Range Rover' in s:
                return 'Land Rover'
            else:
                r = s.split()[0]
                return r if r != 'Mercur' else 'Mercury'

        df['manufacturer'] = df['model'].map(get_manufacturer)

        def get_model(s: str) -> str:
            if 'Mazda' in s:
                return s
            elif 'Alfa Romeo' in s:
                return 'Stevio'
            elif 'Range Rover' in s:
                return 'Range Rover Sport'
            else:
                return ' '.join(s.split()[1:])

        # Note no model name exists with 2 manufacturers
        df['model'] = df['model'].map(get_model)

        # For each model, get most common type
        # and change all other types to that type
        for model in df['model'].unique():
            most_common_type = df[df['model'] ==
                                  model]['type'].value_counts().index[0]
            df.loc[df['model'] == model, 'type'] = most_common_type

        # Drop single observation with 12 cylinders
        df = df[df['cylinders'] != '12 cylinders']

        # Drop <50 observations with 'parts only' title
        df = df[df['title_status'] != 'parts only']

        # Change na to 'nan'
        df = df.fillna('nan')

        factor_vars = [
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

        # Change column order
        df = df[['price', 'miles_10k', 'car_age_years'] +
                factor_vars+['long', 'lat']]

        # Encode categorical variables
        label_encoders = {}
        for var in factor_vars:
            le = LabelEncoder().fit(df[var])
            df[var] = le.transform(df[var])
            label_encoders[var] = le

        with open('data/transform/step_2_preprocessed_data/df_label_encoders.pkl', 'wb') as f_label_encoders:
            pickle.dump(label_encoders, f_label_encoders)

        df.to_pickle('data/transform/step_2_preprocessed_data/01_df.pkl')


if __name__ == "__main__":
    DataPreprocess().clean_data()

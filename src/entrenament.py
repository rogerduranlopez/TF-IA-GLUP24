# Entrenament model offline En format python per facilitar la execució del codi.
# S'ha seguit el codi de offline_glucosa.ipynb que s'ha fet previament per fer les proves i diverses configuracions.
# No s'ha afegit comentaris ja que es el mateix codi utilitzat al notebook.
# L'unic que hem de fer es modificar les rutes, ja que s'executa des de l'arrel del projecte

#####################################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error


import warnings

warnings.simplefilter("ignore", FutureWarning)

pd.set_option('display.max_columns', None)

################################################################################
cols = [
    'year', 'month', 'day', 'hour', 'minute', 'second', # A–F
    'glucose_level', # G
    'finger_stick', # H
    'basal', # I
    'bolus', # J
    'sleep', # K
    'work', # L
    'stressors', # M
    'hypo_event', # N
    'illness', # O
    'exercise', # P
    'basis_heart_rate', # Q
    'basis_gsr', # R
    'basis_skin_temperature', # S
    'basis_air_temperature',  # T
    'basis_step', # U
    'basis_sleep', # V
    'meal', # W
    'meal_type' # X
]
######################################################################
PACIENTS = [559, 563, 570, 575, 588, 591]
HORITZO = {30: 6, 60: 12}

################################################################################


################################################################################
# CARREGUEM LES DADES
def load_data(pacient, train_or_test):
    df=pd.read_csv(f'data/{pacient}/{pacient}_{train_or_test}.csv', sep=';', header = None, names = cols) 
    return df

################################################################################
# PREPROCESSAMENT
def preprocess(df):
    prep = df.copy()
    prep['time'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])
    prep = prep.drop(columns=['second']) 
    prep.sort_values('time', inplace=True)

    convert = ["basal","bolus","basis_gsr","basis_skin_temperature","basis_air_temperature"]
    
    for c in convert:
        prep[c] = (prep[c].astype(str)
                   .str.replace(",",".", regex=False)
                   .str.strip()
                   .astype(float))

    cat_meal = {
        1:"Desayuno",
        2:"Almuerzo",
        3:"Cena",
        4:"Snack",
        5:"Correccion_hipo"
    }

    prep["meal_type"] = prep["meal_type"].map(cat_meal).astype("category")

    prep = pd.get_dummies(prep, columns=['meal_type'], dummy_na=False, prefix='meal')

    invalid_zero = [
        "glucose_level",
        "basis_heart_rate",
        "basis_gsr",
        "basis_skin_temperature",
        "basis_air_temperature"
    ]

    prep[invalid_zero] = prep[invalid_zero].replace(0, np.nan)

    imputacio = [
        "basis_heart_rate",
        "basis_gsr",
        "basis_skin_temperature",
        "basis_air_temperature"
    ]
    
    prep[imputacio] = prep[imputacio].fillna(method='ffill')

    prep = prep.dropna(subset=['glucose_level'])
    
    prep = prep.drop(columns=['time'])

    return prep



#################################################################################
def make_xy(df, files):
    y = df['glucose_level'].shift(-files)
    X = df.iloc[:-files].copy()
    y = y.iloc[:-files]

    return X, y

def evaluate(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae  = mean_absolute_error(y_true, y_pred)
    return rmse, mae

#################################################
# EXECUCIÓ DEL CODI .py
if __name__ == "__main__":
    resultats = []
    
    for pacient in PACIENTS:
        print(f'Entrenant model per pacient {pacient}')
        train_raw = load_data(pacient, 'train')
        test_raw  = load_data(pacient, 'test')

        train = preprocess(train_raw)
        test  = preprocess(test_raw)

        train, test = train.align(test, join='outer', axis=1, fill_value=0)

        test = test.iloc[12:].reset_index(drop=True)

        for minuts, files in HORITZO.items():
            X_train, y_train = make_xy(train, files)
        
            model = RandomForestRegressor(
                n_estimators=1000,
                max_depth=10,
                min_samples_leaf=5,
                random_state=42,
                n_jobs=-1
            )
            model.fit(X_train, y_train)

            X_test = test.iloc[:-files].copy()

            y_true = test['glucose_level'].shift(-files)

            y_true = y_true.iloc[:-files].reset_index(drop=True)

            y_pred = model.predict(X_test)

            directori_pred = f'data/predicted/pred{pacient}_{minuts}min.csv'

            df_pred = pd.DataFrame({'Index': X_test.index + 12, f'pred_glucosa_t+{minuts}': y_pred}) # Comença als 30 mins
            df_pred.to_csv(directori_pred, index=False)

            rmse, mae = evaluate(y_true, y_pred)

            resultats.append({
                'Pacient': pacient,
                'Horitzo': minuts,
                'RMSE': rmse,
                'MAE' : mae
            })

    ################ MOSTREM ELS RESUTATS ##############################
    resultats_df = pd.DataFrame(resultats)

    taula = (resultats_df.pivot(index='Pacient', columns='Horitzo', values=['RMSE','MAE']))

    taula.columns = ['RMSE 30','RMSE 60','MAE 30', 'MAE 60']
    taula = taula[['RMSE 30','MAE 30','RMSE 60','MAE 60']]

    promig = taula.mean().to_frame().T
    promig.index = ['PROMIG'] 
    taula_final = pd.concat([taula, promig], axis=0)

    print("\nRESULTATS FINALS:")
    print(taula_final)
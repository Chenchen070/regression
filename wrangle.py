import pandas as pd
import env
import os

def get_connection(db, username=env.username, host=env.host, password=env.password):

    return f'mysql+pymysql://{username}:{password}@{host}/{db}'


def get_zillow_data():
    """Seeks to read the cached zillow.csv first """
    filename = "zillow.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        return get_new_zillow_data()


def get_new_zillow_data():

    return pd.read_sql('select bedroomcnt,bathroomcnt, calculatedfinishedsquarefeet,\
                        taxvaluedollarcnt, yearbuilt, taxamount, fips FROM zillow.properties_2017\
                        where propertylandusetypeid = 261',\
                       get_connection('zillow'))

def handle_nulls(df):    
    # We keep 99.41% of the data after dropping nulls
    # round(df.dropna().shape[0] / df.shape[0], 4) returned .9941
    df = df.dropna()
    return df


def optimize_types(df):
    # Convert some columns to integers
    # fips, yearbuilt, and bedrooms can be integers
    df[['bedroomcnt', 'calculatedfinishedsquarefeet','taxvaluedollarcnt',\
        'yearbuilt', 'fips']] = df[['bedroomcnt', 'calculatedfinishedsquarefeet','taxvaluedollarcnt',\
        'yearbuilt', 'fips']].astype('int')
    return df

def handle_outliers(df):
    """Manually handle outliers that do not represent properties likely for 99% of buyers and zillow visitors"""
    df = df[df.bathroomcnt <= 6]
    
    df = df[df.bedroomcnt <= 6]

    df = df[df.taxvaluedollarcnt < 2_000_000]

    return df

def wrangle_zillow():
    """
    Acquires Zillow data
    Handles nulls
    optimizes or fixes data types
    handles outliers w/ manual logic
    returns a clean dataframe
    """
    df = get_zillow_data()

    df = handle_nulls(df)

    df = optimize_types(df)

    df = handle_outliers(df)

    df.to_csv("zillow.csv", index=False)

    return df.reset_index(drop=True)


from sklearn.model_selection import train_test_split

def split_zillow(df):
    
    train_and_validate, test = train_test_split(df, random_state=123)
    train, validate = train_test_split(train_and_validate, random_state=123)
    
    return train, validate, test

from sklearn.preprocessing import MinMaxScaler
import sklearn.preprocessing
import numpy as np
import pandas as pd

def scale_zillow(df):
    train, validate, test = split_zillow(df)
    
    scaler = sklearn.preprocessing.MinMaxScaler()
    cols_to_scale = ['calculatedfinishedsquarefeet', 'taxvaluedollarcnt']
    scaler.fit(train[cols_to_scale])

    train_scaled = scaler.transform(train[cols_to_scale])
    validate_scaled = scaler.transform(validate[cols_to_scale])
    test_scaled = scaler.transform(test[cols_to_scale])
    
    train_scaled = pd.DataFrame(train_scaled)
    train_scaled = train_scaled.rename(columns = {0 :'squarefeet_scaled',1 :'taxvalue_scaled'})
    train_scaled = train_scaled.set_index([train.index.values])
    train['squarefeet_scaled'] = train_scaled['squarefeet_scaled']
    train['taxvalue_scaled'] = train_scaled['taxvalue_scaled']
    
    validate_scaled = pd.DataFrame(validate_scaled)
    validate_scaled = validate_scaled.rename(columns = {0 :'squarefeet_scaled',1 :'taxvalue_scaled'})
    validate_scaled = validate_scaled.set_index([validate.index.values])
    validate['squarefeet_scaled'] = validate_scaled['squarefeet_scaled']
    validate['taxvalue_scaled'] = validate_scaled['taxvalue_scaled']
    
    test_scaled = pd.DataFrame(test_scaled)
    test_scaled = test_scaled.rename(columns = {0 :'squarefeet_scaled',1 :'taxvalue_scaled'})
    test_scaled = test_scaled.set_index([test.index.values])
    test['squarefeet_scaled'] = test_scaled['squarefeet_scaled']
    test['taxvalue_scaled'] = test_scaled['taxvalue_scaled']
    
    return train, validate, test
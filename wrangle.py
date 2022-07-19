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


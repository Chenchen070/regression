import pandas as pd
import env

def get_connection(db, username=env.username, host=env.host, password=env.password):

    return f'mysql+pymysql://{username}:{password}@{host}/{db}'


def new_zillow_data():

    return pd.read_sql('select bedroomcnt,bathroomcnt, calculatedfinishedsquarefeet,\
                        taxvaluedollarcnt, yearbuilt, taxamount, fips FROM zillow.properties_2017\
                        where propertylandusetypeid = 261',\
                       get_connection('zillow'))

def wrangle_zillow():
    df = new_zillow_data()
    df = df.dropna()
    df[['bedroomcnt','bathroomcnt', 'calculatedfinishedsquarefeet','taxvaluedollarcnt',\
        'yearbuilt', 'fips']] = df[['bedroomcnt','bathroomcnt', 'calculatedfinishedsquarefeet','taxvaluedollarcnt',\
        'yearbuilt', 'fips']].astype('int')
    
    return df
'''
This code has been adapted from the SIBOS Hackathon Project FINclude: https://github.com/cimotadev/finclude by Data Scientist Kareem Zedan
'''
from flask import render_template, request, jsonify, Flask
import traceback
import os
import pickle
import pandas as pd
import sys
import argparse
import json
import glob
import joblib

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# App definition
app = Flask(__name__)

# Random Forest Classifier
filename = os.path.join(BASE_PATH, 'FusionCreditSenseCLF.pkl')
CLF = joblib.load(filename)

# Random Forest Regressor
rfr = os.path.join(BASE_PATH, 'model_rfr.pkl')
with open(rfr, 'rb') as f2:
    REGR = pickle.load(f2)


def load_from_request(data):   
    df = pd.DataFrame(data)
    d = {"amount": "float64", 
           "currency": "category",
           "transaction_type": "category",
           "status": "category",
           "description": "category",
           "bank_transaction_code": "category",
           "bank_transaction_issuer": "category",
           "booking_datetime": "category"
          }
    df = df.astype(d)
    df_obj = df.to_dict(orient='list')
    return {"df": df_obj}

def select_features(dfl, features=["reference", "amount", "bank_transaction_code", "description"]):
    df = dfl[features]
    return df

def return_selected_features(df):
    '''Returns dataframe of selected features.'''
    features = ['reference', 'amount', 'booking_datetime', 'bank_transaction_code', 'description']
    df = df[features]
    new = df['booking_datetime'].str.split("T", n = 1, expand = True)
    df['booking_date'] = new[0]
    df = df.drop(columns = ['booking_datetime'])
    df['booking_date'] = pd.to_datetime(df['booking_date'])
    return df

def aggregate(df):
    '''Aggregates the dataframe by account reference. For credit score model'''
    df_agg1 = df.groupby('reference').agg({'amount': ["sum", 'describe']})
    df_agg1.columns = df_agg1.columns.get_level_values(0) + "_" + df_agg1.columns.get_level_values(2)
    df_agg1.rename(columns={'amount_amount':'amount_sum'}, inplace=True)
    df_agg2 = df.groupby('reference').agg({"bank_transaction_code": lambda tdf: tdf.unique().tolist()})
    df_agg = df_agg1.join(df_agg2)
    return df_agg

def aggregate_2(df):
    '''Separate aggregation of data for credit line model'''
    pd.MultiIndex.from_frame(df)
    aggs = {
    'reference':['count'],
    'amount': ['sum', 'min', 'max', 'mean', 'std'],
    'booking_date': ['max']}
    df_agg = df.groupby(['reference',pd.Grouper(key='booking_date', freq='1Y')]).agg(aggs)
    df_agg.columns = df_agg.columns.get_level_values(0) + "_" + df_agg.columns.get_level_values(1)
    df_agg2 = df.groupby('reference').agg({"bank_transaction_code": lambda tdf: tdf.unique().tolist()})
    agg_df = df_agg.join(df_agg2)
    agg_df = agg_df.reset_index()
    return agg_df

def transform(df):
    '''Transform to numbers. Self made one hot encoding.'''
    # print(df)
    # btc = {'SO', 'BGC', 'PAY', '1', 'CR', 'DEP', 'DD', '30'}
    btc = {'SO', 'DD', 'CR', 'YE', 'HL', 'PN', 'NJ', 'OW', 'DS', 'WB', 'VI', 'MT',
       'IV', 'FR', 'EO', 'QL', 'EK', 'UB', 'OL', 'DF', 'MG', 'XL', 'WK', 'DP',
       'ZF', 'PQ', 'YK', 'OC', 'FH', 'DJ', 'YT', 'HH'}
    btcs = df["bank_transaction_code"].to_list()
    # print(btcs)
    d = dict()
    for c in btc:
        l = list()
        for l2 in btcs:
            l.append(1 if c in l2 else 0)
        d[c] = l
    dfr = pd.DataFrame.from_records(d, index=df.index)
    dfr = dfr.join(df)
    dfr.drop(columns=['bank_transaction_code'], inplace=True)
    return dfr




@app.route('/')
def welcome():
    return "Flask model backend"

@app.route('/prepare_dataset', methods=['POST'])
def prepare_dataset():
    """
    Transform the incoming JSON transactions into a dataframe
    """
    try:
        data = request.get_json()
        return load_from_request(data['transactions'])
    except:
        return jsonify({
                "trace": traceback.format_exc()
            })
 
@app.route('/pipe_predict', methods=['POST', 'GET'])
def pipe_predict():
    '''Backend transform method for the incoming message variables.'''
    if request.method == 'GET':
        return "Select features: GET"

    if request.method == 'POST':
        try:
            # form_data = request.form["df"]
            data = request.get_json()
            if not data: return "No data received."
            dfl = pd.DataFrame.from_dict(data['df'], orient='columns')       
            # aggregate data & predict using credit score model     
            dff = select_features(dfl)
            dfa = aggregate(dff)
            dft = transform(dfa)
            preds = REGR.predict(dft)
            # aggregate and append credit score prediction as feature & predict using credit line model
            df_h = return_selected_features(dfl)
            df_h_agg = aggregate_2(df_h)
            df_h_agg['credit_score'] = preds
            df_h_t = transform(df_h_agg)
            df_h_t = df_h_t.drop(columns = ['reference','booking_date', 'booking_date_max'])
            cred_line_pred = CLF.predict(df_h_t)
            ret = {"cred_line_pred": cred_line_pred.tolist(), "y_pred": preds.tolist()}
            return ret
            # return json.dumps(ret)
            # return dft.to_dict()
        except:
            return jsonify({
                "trace": traceback.format_exc()
            })

    return "Neither POST nor GET"

@app.route('/transform', methods=['POST', 'GET'])
def transform_im():
    '''Backend transform method for the transactions for one account.'''
    if request.method == 'GET':
        return "Transformation page Incoming Message: GET"

    if request.method == 'POST':
        try:
            # form_data = request.form["df"]
            data = request.get_json()
            if not data: return "No data received."
            dfl = pd.DataFrame.from_dict(data['df'], orient='columns')            
            dft = transform(dfl)
            return dft.to_dict()
        except:
            return jsonify({
                "trace": traceback.format_exc()
            })

    return "Neither POST nor GET"


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    '''Backend predict method'''
    if request.method == 'GET':
        return "Prediction page: GET"

    if request.method == 'POST':
        try:
            # form_data = request.form["df"]
            data = request.get_json()
            if not data: return "No data received."
            dfl = pd.DataFrame.from_dict(data['df'], orient='columns')
            #return dfl.to_dict()
            label = CLF.predict(dfl)
            d = {"cred_line_pred": label}
            return d
        except:
            return jsonify({
                "trace": traceback.format_exc()
            })

    return "Neither POST nor GET"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default='8000')
    args = parser.parse_args()
    print("args.port", args.port)
    print("args.host", args.host)
    app.run(debug=True, port=args.port, host=args.host)
    #app.run(debug=True)

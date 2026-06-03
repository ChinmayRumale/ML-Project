# This file loads saved model and makes predictions on new input data

import pickle  # load saved model, scaler, selector
import numpy as np  # numerical operations
import pandas as pd  # data manipulation
from dotenv import load_dotenv  # load env variables
import os  # access env variables

load_dotenv()  # load .env file

def load_artifacts():
    # load saved model from disk
    with open(os.getenv('MODEL_PATH'), 'rb') as f:
        model = pickle.load(f)  # deserialize model

    # load saved scaler from disk
    with open('./ml/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)  # deserialize scaler

    # load saved selector from disk
    with open('./ml/selector.pkl', 'rb') as f:
        selector = pickle.load(f)  # deserialize selector

    # load selected feature names
    with open('./ml/selected_features.pkl', 'rb') as f:
        selected_features = pickle.load(f)  # deserialize feature names

    return model, scaler, selector, selected_features  # return all artifacts


def _build_input_dataframe(input_data: dict, scaler):
    feature_names = getattr(scaler, 'feature_names_in_', None)
    if feature_names is None:
        raise ValueError('Scaler has no feature_names_in_, cannot build input vector.')

    data = {name: 0 for name in feature_names}

    # copy direct numeric fields
    for field in [
        'Administrative', 'Administrative_Duration', 'Informational', 'Informational_Duration',
        'ProductRelated', 'ProductRelated_Duration', 'BounceRates', 'ExitRates',
        'PageValues', 'SpecialDay', 'OperatingSystems', 'Browser', 'Region',
        'TrafficType', 'Weekend'
    ]:
        if field in input_data:
            data[field] = float(input_data[field])

    # map Month to one-hot fields if necessary
    month_map = {
        0: 'Month_Jan', 1: 'Month_Feb', 2: 'Month_Mar', 3: 'Month_Apr',
        4: 'Month_May', 5: 'Month_Jun', 6: 'Month_Jul', 7: 'Month_Aug',
        8: 'Month_Sep', 9: 'Month_Oct', 10: 'Month_Nov', 11: 'Month_Dec'
    }
    month_value = int(input_data.get('Month', 0))
    month_feature = month_map.get(month_value)
    if month_feature and month_feature in data:
        data[month_feature] = 1

    # map VisitorType to one-hot fields if necessary
    visitor_map = {
        0: 'VisitorType_New_Visitor',
        1: None,
        2: 'VisitorType_Returning_Visitor'
    }
    visitor_value = int(input_data.get('VisitorType', 0))
    visitor_feature = visitor_map.get(visitor_value)
    if visitor_feature and visitor_feature in data:
        data[visitor_feature] = 1

    return pd.DataFrame([data], columns=feature_names)


def predict(input_data: dict):
    model, scaler, selector, selected_features = load_artifacts()  # load all artifacts

    # convert input dict to the exact feature vector used in training
    df = _build_input_dataframe(input_data, scaler)

    # scale all features first (same as training)
    df_scaled = scaler.transform(df)

    # then select top features using saved selector
    df_selected = selector.transform(df_scaled)

    # make prediction
    prediction = model.predict(df_selected)[0]  # 0 or 1
    probability = model.predict_proba(df_selected)[0][1]  # probability of Revenue=1

    result = {
        "prediction": int(prediction),
        "probability": round(float(probability), 4),
        "message": "Will Purchase" if prediction == 1 else "Will Not Purchase"
    }

    return result





if __name__ == "__main__":
    # sample input — all 17 features (Revenue excluded as it is target)
    sample_input = {
        "Administrative": 0,
        "Administrative_Duration": 0.0,
        "Informational": 0,
        "Informational_Duration": 0.0,
        "ProductRelated": 1,
        "ProductRelated_Duration": 0.0,
        "BounceRates": 0.2,
        "ExitRates": 0.2,
        "PageValues": 0.0,
        "SpecialDay": 0.0,
        "Month": 2,
        "OperatingSystems": 1,
        "Browser": 1,
        "Region": 1,
        "TrafficType": 1,
        "VisitorType": 2,
        "Weekend": 0
    }

    result = predict(sample_input)  # run prediction
    print(result)  # print result

# This file cleans and preprocesses raw data for ML model

import pandas as pd  # data manipulation library


def transform_data(df):
    # drop duplicate rows if any
    df = df.drop_duplicates()

    # drop rows where any value is null
    df = df.dropna()

    # normalize Revenue values to integer target
    revenue_map = {
        True: 1, False: 0,
        'TRUE': 1, 'FALSE': 0,
        'True': 1, 'False': 0,
        'true': 1, 'false': 0,
        '1': 1, '0': 0
    }
    if 'Revenue' in df.columns:
        df['Revenue'] = df['Revenue'].replace(revenue_map).astype(int)

    # normalize Weekend values to integer
    bool_map = {
        True: 1, False: 0,
        'TRUE': 1, 'FALSE': 0,
        'True': 1, 'False': 0,
        'true': 1, 'false': 0,
        'YES': 1, 'NO': 0,
        'Yes': 1, 'No': 0,
        'yes': 1, 'no': 0,
        '1': 1, '0': 0
    }
    if 'Weekend' in df.columns:
        df['Weekend'] = df['Weekend'].replace(bool_map).astype(int)

    # handle month encoding; prefer one-hot month_* columns if present
    month_onehot_cols = [col for col in df.columns if col.startswith('Month_')]
    if month_onehot_cols:
        df[month_onehot_cols] = df[month_onehot_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
        if 'Month' in df.columns:
            df = df.drop(columns=['Month'])
    elif 'Month' in df.columns:
        month_map = {
            'jan': 0, 'feb': 1, 'mar': 2, 'apr': 3,
            'may': 4, 'jun': 5, 'jul': 6, 'aug': 7,
            'sep': 8, 'oct': 9, 'nov': 10, 'dec': 11
        }
        df['Month'] = (
            df['Month']
            .astype(str)
            .str.strip()
            .str[:3]
            .str.lower()
            .map(month_map)
        )
        if df['Month'].isna().any():
            raise ValueError('Unsupported Month values found in raw data.')
    else:
        raise ValueError('Dataset does not contain Month or Month_* features.')

    # handle visitor type encoding; prefer one-hot VisitorType_* columns if present
    visitor_onehot_cols = [col for col in df.columns if col.startswith('VisitorType_')]
    if visitor_onehot_cols:
        df[visitor_onehot_cols] = df[visitor_onehot_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
        if 'VisitorType' in df.columns:
            df = df.drop(columns=['VisitorType'])
    elif 'VisitorType' in df.columns:
        visitor_map = {
            'new_visitor': 0,
            'other': 1,
            'returning_visitor': 2,
            'new visitor': 0,
            'other visitor': 1,
            'returning visitor': 2
        }
        df['VisitorType'] = (
            df['VisitorType']
            .astype(str)
            .str.strip()
            .str.lower()
            .replace(visitor_map)
        )
        if df['VisitorType'].isna().any():
            raise ValueError('Unsupported VisitorType values found in raw data.')
    else:
        raise ValueError('Dataset does not contain VisitorType or VisitorType_* features.')

    print(f"Transformed data shape: {df.shape}")  # log final shape
    return df  # return cleaned dataframe

if __name__ == "__main__":
    from extract import extract_data  # import extract function
    df = extract_data()  # fetch raw data
    df = transform_data(df)  # apply transformations
    print(df.head())  # print first 5 rows to verify
    print(df.dtypes)  # print column data types to verify encoding
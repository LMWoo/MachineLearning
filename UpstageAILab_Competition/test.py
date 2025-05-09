import pandas as pd
import numpy as np
from tqdm import tqdm
import pickle
import warnings;warnings.filterwarnings('ignore')

# Model
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

import eli5
from eli5.sklearn import PermutationImportance

import joblib

from data.load import load_data

import argparse

parser = argparse.ArgumentParser(description="Train parser")

parser.add_argument("--is_feature_reduction", type=bool, default=False, help='50 features -> top 8 features')
parser.add_argument("--is_feature_engineering", type=bool, default=False, help='gu -> High, Mid, Low')
parser.add_argument("--is_logScale", type=bool, default=False, help='target -> logScale')
parser.add_argument("--is_lightGBM", type=bool, default=False, help='model train LightGBM')
parser.add_argument("--is_subway", type=bool, default=False, help='Add grade based on distance to subway station')
parser.add_argument("--train_data_path", type=str, default="../../data/train.csv", help="train data path") 
parser.add_argument("--test_data_path", type=str, default="../../data/test.csv", help="test data path") 
parser.add_argument("--model_name", type=str, default="save_model")
parser.add_argument("--save_file", type=str, default="output")

if __name__ == "__main__":

    args = parser.parse_args()

    X_train, y_train, X_val, y_val, categorical_columns_v2, label_encoders, dt_test = load_data(args.train_data_path, args.test_data_path, args.is_feature_reduction, args.is_feature_engineering, args.is_subway)


    dt_test.head(2)      # test dataset에 대한 inference를 진행해보겠습니다.

    if args.is_lightGBM == True:
        model = joblib.load('./weights/'+ args.model_name + '.pkl')

        X_test = dt_test.drop(['target'], axis=1)

        real_test_pred = model.predict(X_test)

        preds_df = pd.DataFrame(real_test_pred.astype(int), columns=["target"])
        preds_df.to_csv('./results/' + args.save_file + '.csv', index=False)
    else:
        # 저장된 모델을 불러옵니다.
        with open('./weights/'+ args.model_name + '.pkl', 'rb') as f:
            print('./weights/'+ args.model_name + '.pkl')
            model = pickle.load(f)

        # %%time
        X_test = dt_test.drop(['target'], axis=1)

        # Test dataset에 대한 inference를 진행합니다.
        real_test_pred = model.predict(X_test)
        if args.is_logScale == True:
            real_test_pred = np.expm1(real_test_pred)
        # 앞서 예측한 예측값들을 저장합니다.
        preds_df = pd.DataFrame(real_test_pred.astype(int), columns=["target"])
        preds_df.to_csv('./results/' + args.save_file + '.csv', index=False)
        
    print('finish test')

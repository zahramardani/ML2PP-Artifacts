import sys
import time, datetime
import pandas as pd
import numpy as np
import pickle

timestamps = sys.argv[1]
features = sys.argv[2].split(',')
feature_types = sys.argv[3].split(',')
feature_values_for_prediction = sys.argv[4].split(',')
timestamp_for_prediction = sys.argv[5]

# Load full, un-scaled training frame
with open(r'/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/pickles/preprocess_original_df.pickle','rb') as f:
    original_df = pickle.load(f)

# Load pre-processed design matrices
with open(r'/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/pickles/preprocess_X_train.pickle','rb') as f:
    X_train = pickle.load(f)
with open(r'/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/pickles/preprocess_y_train.pickle','rb') as f:
    y_train = pickle.load(f)

array_features_indexes = list(filter(lambda x: '[' in feature_types[x], range(len(feature_types))))
new_feature_values_for_prediction = []
for index in array_features_indexes:
    for item in feature_values_for_prediction[index][2:-2].split(' '):
        new_feature_values_for_prediction.append(item)
    feature_values_for_prediction.pop(index)
    feature_values_for_prediction.append(new_feature_values_for_prediction)
    feature_name = features[index]
    features.pop(index)
    i=index
    for item in range(len(new_feature_values_for_prediction)):
        features.insert(i,feature_name+'_'+str(item))
        i=i+1
if(len(array_features_indexes)!=0):
    feature_values_for_prediction = feature_values_for_prediction[0]

col_names = []
num_col_names = []
cat_col_names = []
if(timestamps.lower() == 'on'):
    col_names.append('timestamp')
for i in range(len(features)):
    feature=features[i]
    feature_type=feature_types[i]
    if(("String" in feature_type) or ("Char" in feature_type)):
        cat_col_names.append(feature)
    if(("Int" in feature_type) or ("Long" in feature_type) or ("Double" in feature_type)):
        num_col_names.append(feature)
    col_names.append(feature)

if(len(cat_col_names)!=0):
    from sklearn.preprocessing import LabelEncoder
    with open('/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/pickles/preprocess_label_encoder.pickle', 'rb') as pickle_file:
        le = pickle.load(pickle_file)

flag = False
for i in range(len(features)):
    if features[i] in cat_col_names:
        if not np.isin([feature_values_for_prediction[i]],original_df[features[i]]).item(0):
            flag = True
            break

if(flag):
    print (False)
else:
    import os, pickle
    import pandas as pd

    n_out = 3

    output_txt_path = r'/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/outputs/prediction.txt'
    output_csv_path = r'/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/outputs/prediction.csv'
    os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    model = xgb.Booster()
    model.load_model(r'/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/pickles/xgboost_model_fit.pickle')
    dmatrix = xgb.DMatrix([feature_values_for_prediction])
    prediction = model.predict(dmatrix)

    formatted = str(prediction[0])
    with open(output_txt_path, 'a') as f:
        f.write(f"🔹 Prediction: {formatted}\n")

    df = pd.DataFrame([prediction], columns = ['XGBoost_pred'])
    df.to_csv(output_csv_path,
              mode   = 'a',
              header = not os.path.exists(output_csv_path),
              index  = False)

import pickle

with open('/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/pickles/preprocess_X_train.pickle', 'rb') as pf:
    X_train = pickle.load(pf)
with open('/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/pickles/preprocess_X_test.pickle',  'rb') as pf:
    X_test = pickle.load(pf)
with open('/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/pickles/preprocess_y_train.pickle', 'rb') as pf:
    y_train = pickle.load(pf)
with open('/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/pickles/preprocess_y_test.pickle',  'rb') as pf:
    y_test = pickle.load(pf)
import pandas as pd
import xgboost as xgb
import pickle
import matplotlib.pyplot as plt
import numpy as np

# ✅ Ensure X_train and y_train are valid numpy arrays
if isinstance(X_train, list):
    X_train = np.array(X_train)
if isinstance(y_train, list):
    y_train = np.array(y_train)
if X_train.ndim == 1:
    X_train = X_train.reshape(-1, 1)
if y_train.ndim == 2 and y_train.shape[1] == 1:
    y_train = y_train.ravel()

# ⛑️ Data shape check before training
print("🔍 X_train shape:", getattr(X_train, "shape", None))
print("🔍 y_train shape:", getattr(y_train, "shape", None))
if X_train is None or y_train is None or len(X_train) == 0 or len(y_train) == 0:
    raise ValueError("❌ X_train or y_train is empty. Cannot proceed with training.")

# Manual XGBoost Training
model = xgb.XGBRegressor(max_depth=6, learning_rate=0.1, n_estimators=100, objective='reg:squarederror', booster='gbtree', gamma=0, min_child_weight=1.0, subsample=0.8, colsample_bytree=0.8, colsample_bylevel=1.0, colsample_bynode=1.0, reg_alpha=0.0, reg_lambda=1.0, scale_pos_weight=1.0, base_score=0.5, random_state=42, missing=None, importance_type='gain')
model_fit = model.fit(X_train, y_train)

with open('/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/pickles/xgboost_model_fit.pickle', 'wb') as f:
    pickle.dump(model_fit, f)


# ---------------- Forecasting Plots ----------------
import os
import numpy as np
y_pred = np.array(y_pred)
y_test = np.array(y_test)
# reshape to 2D if single-step forecast
if y_test.ndim == 1:
    y_test = np.tile(y_test.reshape(-1, 1), (1, y_pred.shape[1]))
if y_pred.ndim == 1:
    y_pred = y_pred.reshape(-1, 1)
nSteps = min(y_test.shape[1], y_pred.shape[1])
# plot exactly nSteps forecast steps
steps = nSteps
titles = [f'Prediction {i+1} (t+{i})' for i in range(steps)]
filenames = [f'forecast_vs_actual_t{i}.png' for i in range(steps)]
for i in range(steps):
    plt.figure(figsize=(10,5))
    plt.plot(y_test[:, i], label='Actual')
    plt.plot(y_pred[:, i], label='Forecast', linestyle='--')
    plt.title(titles[i])
    plt.xlabel('Time Steps')
    plt.ylabel('Value')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join('/home/mlpluspy/appservers/apache-tomcat-10.1.26/webapps/ROOT/GeneratedCode/user1/python_java/src/python-scripts/plots/', filenames[i]))
    plt.close()

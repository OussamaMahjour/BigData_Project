import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import numpy as np
# Example data
95788.00000000
data = pd.read_csv("lag_dataset.csv")

X = data[[
    'open_price_t0',
    'open_price_t1',
    'open_price_t2',
    'open_price_t3',
    'open_price_t4',
    # 'open_price_t5',
    # 'open_price_t6',
    # 'open_price_t7',
    # 'open_price_t8',
    ]]
y = data['open_price_t5']

scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))
# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, shuffle=False)

# Convert to DMatrix
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

params = {
    'objective': 'reg:squarederror',
    'eval_metric': 'rmse',
    'max_depth': 6,
    'eta': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8
}

num_round = 100
model = xgb.train(params, dtrain, num_round, evals=[(dtest, 'test')], early_stopping_rounds=10)


# Make predictions
y_pred = model.predict(dtest)

# Evaluate performance
rmse =np.sqrt(mean_squared_error(y_test, y_pred))
print(f"RMSE: {rmse}") 



latest_data = data.iloc[-1]
    # Prepare it in the same format used for predictions
latest_features = pd.DataFrame({
        'open_price_t0': [latest_data['open_price_t0']],
        'open_price_t1': [latest_data['open_price_t1']],
        'open_price_t2': [latest_data['open_price_t2']],
        'open_price_t3': [latest_data['open_price_t3']],
        'open_price_t4': [latest_data['open_price_t4']]
    })

output = []
for x in range(0,20):
     
    latest_data_scaled = scaler_X.transform(latest_features)
    latest_dmatrix = xgb.DMatrix(latest_data_scaled)
    scaled_future_prediction = model.predict(latest_dmatrix)
    future_prediction = scaler_y.inverse_transform([[scaled_future_prediction[0]]])[0, 0]
    #print(f"Predicted Value: {future_prediction}")
    tmp = {
        
        'open_price_t0': latest_features['open_price_t0'][0],
        'open_price_t1': latest_features['open_price_t1'][0],
        'open_price_t2': latest_features['open_price_t2'][0],
        'open_price_t3': latest_features['open_price_t3'][0],
        'open_price_t4': latest_features['open_price_t4'][0],
        'open_price_t5': future_prediction
    }
    output.append(tmp)
    for d in range(len(latest_features.keys())-1):
        latest_features[f"open_price_t{d}"]=latest_features[f"open_price_t{d+1}"]
    latest_features["open_price_t4"]=future_prediction
    print(latest_features)

   
output = pd.DataFrame(output)
output.to_csv("predicted_dataset.csv",index=False)
    



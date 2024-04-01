import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV

# Load data from the CSV file
dfile = r'C:\Users\chris_pedretti\Downloads\hw1_data.csv'
hdata = pd.read_csv(dfile)

# Select categorical and continuous data columns
categorical_data = hdata.select_dtypes(include=['object'])
continuous_data = hdata.select_dtypes(exclude=['object'])

# Create and fit the OneHotEncoder
encoder = OneHotEncoder()
encoder.fit(categorical_data)

# Transform categorical data into one-hot encoded vectors
encoded_categorical_data = encoder.transform(categorical_data)

# Convert the matrix to an array
encoded_categorical_data = encoded_categorical_data.toarray()

# Create a DataFrame from the one-hot encoded categorical data
encoded_categorical_df = pd.DataFrame(encoded_categorical_data, columns=encoder.get_feature_names_out(categorical_data.columns))

# Concatenate the one-hot encoded data with the continuous data
result_data = pd.concat([encoded_categorical_df, continuous_data], axis=1)

X = result_data.drop(columns=['SalePrice'])
y = result_data['SalePrice']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a SimpleImputer instance to fill missing values with the mean
imputer = SimpleImputer(strategy='mean')

# Fit the imputer on the training data and transform both X_train and X_test
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# Standardize continuous features using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)

# Create models with different regularization
models = {
    'Linear Regression': LinearRegression(),
    'Polynomial Regression': make_pipeline(PolynomialFeatures(degree=2), LinearRegression()),
    'Ridge Regression': Ridge(alpha=0.01),
    'Lasso Regression': Lasso(alpha=0.01),
    'Elastic Net': ElasticNet(alpha=0.01, l1_ratio=0.5)
}

# Fit and evaluate each model
for model_name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    mse = mean_squared_error(y_test, y_pred, squared=True)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"{model_name}:")
    print(f"MSE: {mse}")
    print(f"RMSE: {rmse}")
    print(f"MAE: {mae}")
    print(f"R-squared: {r2}")
    print('\n')
    
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred)
    plt.title(f'{model_name} - Actual vs. Predicted')
    plt.xlabel('Actual Sale Price')
    plt.ylabel('Predicted Sale Price')
    plt.show()

    #Analysis
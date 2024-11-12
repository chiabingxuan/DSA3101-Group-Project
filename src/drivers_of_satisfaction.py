import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report
import os
import shap
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

####################################################################################################
### Objective: To determine main drivers of overall satisfaction                                 ###
### Analysis conducted: Key Driver Analysis                                                      ###
### End Product: Performance-Importance Matrix                                                   ###
####################################################################################################

# Load the File
df = pd.DataFrame(pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/combined_trip_data.csv"), keep_default_na=False))

# Identify features that contributes to Overall Satisfaction, based on Domain Knowledge
selected_columns = ['waiting_time_satisfaction', 'crowdedness_satisfaction', 'comfort', 'safety', 'overall_satisfaction']

# Investigate each feature to determine the range, skewness and identify any outliers
plt.figure(figsize=(12,8))

# Plot Boxplot for each feature
for i, selected_column in enumerate(selected_columns, 1):
    plt.subplot(len(selected_columns), 2, 2*i-1)
    sns.boxplot(x=df[selected_column])
    plt.title(f'Box Plot of {selected_column}')

# Plot Histogram for each feature
for i, selected_column in enumerate(selected_columns, 1):
    plt.subplot(len(selected_columns), 2, 2 * i)
    sns.histplot(df[selected_column], kde=True)
    plt.title(f'Histogram of {selected_column}')

plt.tight_layout()
plt.show()

# Investigate the Performance of each factor by obtaining the Median score of each factor
## Calculate the median score for each column
median_scores = df[selected_columns].median()

## Print Median Score for each column
print("Median Scores for each column:")
print(median_scores)

# Investigate the Relationship between Crowdedness and Crowdedness Satisfaction
## Box Plot of Crowdedness against Crowdedness Satisfaction
sns.boxplot(x='crowdedness', y='crowdedness_satisfaction', data=df)
plt.title('Crowdedness vs. Crowdedness Satisfaction')
plt.xlabel('Crowdedness')
plt.ylabel('Crowdedness Satisfaction')
plt.show()

## Conduct a Linear Regression of Crowdedness against Crowdedness Satisfaction
### Define predictor (independent) variable X and response (dependent) variable y
X_c = df['crowdedness']
y_c = df['crowdedness_satisfaction']

### Add a constant to the predictor variable to include an intercept in the model
X_c = sm.add_constant(X_c)

### Fit the linear regression model
model_LR_C = sm.OLS(y_c, X_c).fit()

### Print the model summary to see the regression results
print(model_LR_C.summary())

# Investigate the Relationship between Waiting Time and Waiting Time Satisfaction
## Box Plot of Waiting Time against Waiting Time Satisfaction
sns.boxplot(x='waiting_time', y='waiting_time_satisfaction', data=df)
plt.title('Waiting Time vs Waiting Time Satisfaction')
plt.xlabel('Waiting Time')
plt.ylabel('Waiting Time Satisfaction')
plt.show()

## Linear Regression of Waiting Time against Waiting Time Satisfaction
### Define predictor (independent) variable X and response (dependent) variable y
X_c = df['waiting_time']
y_c = df['waiting_time_satisfaction']

### Add a constant to the predictor variable to include an intercept in the model
X_c = sm.add_constant(X_c)

### Fit the linear regression model
model_LR_WT = sm.OLS(y_c, X_c).fit()

### Print the model summary to see the regression results
print(model_LR_WT.summary())

# Correlation Analysis
## Conduct a Correlation Analysis between the different factors and overall satisfaction scores to determine a suitable model to determine Key Drivers of Satisfaction and Dissatisfaction\
selected_columns = ['waiting_time_satisfaction', 'crowdedness_satisfaction', 'comfort', 'safety', 'overall_satisfaction']
selected_df = df[selected_columns]
print(selected_df.head())

corr_matrix = selected_df.corr()

## Visualise the Correlation Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot = True, cmap='coolwarm', vmin=-1, vmax = 1, fmt = '.2f', square = True)
plt.title('Correlation Heatmap for Selected Features')
plt.show()

## Based on our results, there seems to be moderate correlation between each factor and overall satisfaction. We will use other methods to determine the relationship between each factor and overall satisfaction.
## Based on our results, there is moderate correlation between factors. This could imply low multicollinearity. We conduct Variance Inflation Factor (VIF) to determine if the correlations are high enough to be considered as multicollinearity.

# Calculate Variance Inflation Factor (VIF)
X = df[['waiting_time_satisfaction', 'crowdedness_satisfaction', 'comfort', 'safety']]
X = sm.add_constant(X)

vif_data = pd.DataFrame()
vif_data["selected_column"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

vif_data = vif_data[vif_data["selected_column"] != "const"]
print(vif_data)
## Given that VIF for all factors are less than 2, multicollinearity is not an issue and Multiple Linear Regression can be conducted to determine weight of each factor when for Overall Satisfaction

# Conduct Multiple Linear Regression
## Define the Variables
y = df['overall_satisfaction']

## Run the Linear Regression Model
model_MLR = LinearRegression()
results_MLR = model_MLR.fit(X,y)

## Print the Coefficients of the Linear Regression Model
print(f'Intercept: {model_MLR.intercept_}')
print('Coefficients:')
for feature, coef in zip(X.columns, model_MLR.coef_):
    print(f'{feature}: {coef}')

## Based on Multiple Regression Analysis, we see that the Beta Coefficients for the factprs affecting overall satisfaction is as follows (from largest to smallest): Comfort, Safety, Crowdedness Satisfaction, Waiting Time Satisfaction

# Conduct Dominance Analysis to compare the importance of each factor when it comes to overall satisfaction. Measures relative importance of factors.
# Function to calculate R-squared
def calculate_r_squared(X,y):
    model = sm.OLS(y, X).fit()
    return model.rsquared

## Fit Full Model
full_r_squared = calculate_r_squared(X,y)
print(f"Full Model R-squared: {full_r_squared:.4f}")

## Calculate R-squared for models excluding each predictor
r_squared_values = {}
for predictor in X.columns:
    reduced_X = X.drop(columns=[predictor])
    r_squared_values[predictor] = calculate_r_squared(reduced_X, y)

## Display the R-squared values for each reduced model
print("\nR-squared Values for Reduced Models:")
for predictor, r2 in r_squared_values.items():
    print(f"Excluding {predictor}: R-squared = {r2:.4f}")

## Calculate the change in R-squared
print("\nChange in R-squared when excluding each predictor:")
for predictor, r2 in r_squared_values.items():
    change = full_r_squared - r2
    print(f"Change when excluding {predictor}: {change:.4f}")   

## Based on the Dominance Analysis, the removal of each factor leads to small decrease in explained variance. Comparing them (from largest to smallest impact) is as follows: Comfort, Safety, Crowdedness Satisfaction, Waiting Time Satisfaction
## Based on the R-Squared of the Model 0.3216, the explanatory power of the 4 factors identified gives a low contribution to the overall satisfaction. Thus, we will explore other Relative Importance Analysis Methods.

# Conduct SHAP Regression to determine Feature Importance using a Random Forest Model to determine overall satisfaction scores
shap.initjs()

# Import Train and Test Datasets
train = pd.DataFrame(pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/train_trip_data_after_sdv.csv"), keep_default_na=False))
test = pd.DataFrame(pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test_trip_data_after_sdv.csv"), keep_default_na=False))

selected_features = ['waiting_time_satisfaction', 'crowdedness_satisfaction', 'comfort', 'safety']
X_train = train[selected_features]
X_test = test[selected_features]
y_train = train['overall_satisfaction']
y_test = test['overall_satisfaction']

print(X_train, X_train.shape)
print(X_test, X_test.shape)
print(y_train, y_train.shape)
print(y_test, y_test.shape)

# Train a random forest model
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Make prediction on test data
# y_pred = clf.predict(X_test)

# Classification Report 
# print(classification_report(y_pred, y_test))

explainer = shap.Explainer(clf, X_train, feature_names=X_train.columns)
shap_values = explainer(X_test)
## shap_values_mean = np.mean(shap_values, axis=2)

print(shap_values.shape)
print(X_test.shape)

shap.summary_plot(shap_values, X_test)

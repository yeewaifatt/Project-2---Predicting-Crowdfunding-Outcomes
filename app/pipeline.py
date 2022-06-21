import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score

from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline

# Find the dataset @ (CSV files 2022-04-21, https://webrobots.io/kickstarter-datasets/)
# download link: https://s3.amazonaws.com/weruns/forfun/Kickstarter/Kickstarter_2022-04-21T03_20_08_060Z.zip

# get db connection
load_dotenv()
db_connection = os.getenv("KICKSTARTER_DB_URL")

# init database engine
engine = create_engine(db_connection)

# Query the database for data to build models.
query = """
        SELECT  kickstarters.state, 
                country, 
                fx_rate, 
                goal, 
                created_at, 
                launched_at, 
                kickstarters.state_changed_at, 
                deadline, 
                parent_name,
                category.name
        FROM kickstarters
        INNER JOIN category
        ON kickstarters.id=category.kickstarter_id
        WHERE state='failed' OR state='successful';
        """
        #  	
model_data = pd.read_sql(query, engine)


# create goal_usd column so that all goal amounts are in the same units, drop fx_rate and goals afterward
model_data['goal_usd'] = model_data['fx_rate']*model_data['goal']
model_data = model_data.drop(columns=['fx_rate', 'goal'])

# create total days active column as another metric
model_data['total_days_active'] = (model_data.deadline-model_data.launched_at)*0.00001157
model_data['launch_time'] = (model_data.launched_at-model_data.created_at)*0.00001157
model_data = model_data.drop(columns=['state_changed_at', 'deadline', 'launched_at', 'created_at'])

# Drop NA's (before pipeline, maybe later version could impute missing values)
model_data = model_data.dropna()


# split into X and y variables
X = model_data.drop(columns=['state'])
y = model_data.state

# generate 70% train/test split 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state = 1)


# encoding transformer
encoding_columns = list((X.select_dtypes(include=['bool', 'object'])).columns)
scaling_columns = list((X.select_dtypes(include=['int', 'float'])).columns)

column_transformer = make_column_transformer(
    (OneHotEncoder(handle_unknown='ignore'), encoding_columns),
    (StandardScaler(), scaling_columns),
    remainder='drop'
    )

# init and fit RF classifier
rf_classifier = RandomForestClassifier()
rf_pipe = make_pipeline(column_transformer, rf_classifier)
rf_pipe.fit(X_train, y_train)

# perform predictions on testing and validation data
rf_predictions  = rf_pipe.predict(X_test)

# classification reports for the test and validation set
rf_report = classification_report(y_test, rf_predictions)
print (rf_report)

# pickle the model
pickle.dump(rf_pipe, open('rf_pipe.sav', 'wb'))

# init and fit RF classifier
svm_classifier = SVC(kernel='linear', max_iter=500)
svm_pipe = make_pipeline(column_transformer, svm_classifier)
svm_pipe.fit(X_train, y_train)

# perform predictions on testing and validation data
svm_predictions  = svm_pipe.predict(X_test)

# classification reports for the test and validation set
svm_report = classification_report(y_test, svm_predictions)
print (svm_report)

# pickle the model
pickle.dump(svm_pipe, open('svm_pipe.sav', 'wb'))

# init and fit RF classifier
nn_classifier = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(4, 2), random_state=1)
nn_pipe = make_pipeline(column_transformer, nn_classifier)
nn_pipe.fit(X_train, y_train)

# perform predictions on testing and validation data
nn_predictions  = nn_pipe.predict(X_test)

# classification reports for the test and validation set
nn_report = classification_report(y_test, nn_predictions)
print (nn_report)


# pickle the model
pickle.dump(nn_pipe, open('nn_pipe.sav', 'wb'))


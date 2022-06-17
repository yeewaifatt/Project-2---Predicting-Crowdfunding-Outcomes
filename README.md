# Project-2---Predicting-Crowdfunding-Outcomes
This project was inspired by a research paper by S.Khosla et al. The paper discussed the application of various machine learning models to predict the outcome of Kickstarter projects. The results obtained in the paper were quite reproducable, as many of the models tested in this project see similar accuracy scores to that of the Standford paper, albeit with slightly different methodology/data. [Read the paper here](https://cs229.stanford.edu/proj2021spr/report2/81995033.pdf)

This repository includes the data collection, processing and model building as well as a small streamlit application for anyone wanting to test out the model with their own input data.

## Raw data
All of the data used in this porject was sourced from a pre-existing amazon s3 bucket, which was compiled by a [web scraping service](https://webrobots.io/kickstarter-datasets/), The download link for the exact dataset used can be found [here](https://s3.amazonaws.com/weruns/forfun/Kickstarter/Kickstarter_2022-04-21T03_20_08_060Z.zip).

## SQL Database 
The raw data is a zip file which contains a set of csv files, of which some columns contain JSON objects. The make_database.py script will populate an SQL database with the extracted CSV files. 

If you wish to run this code on your local machine, ensure that you have set up an SQL DB and have the exctracted CSV files in a folder named 'raw_data' in the SQLDatabase directory. Also  ensure you have a .env file with 'KICKSTARTER_DB_URL' as a variable to ensure that the python script can connect with your DB.

![DB_schema](images/Database%20Schema.png)


## Model exploration

## Pipeline
 these files were concatenated along rows to build one large data frame. This gave us approximately 30000 data points each with more than 30 individual features. Some of the features were expressed as a JSON, these features required some extra data wrangling to unpack so that we could use them.
After the initial data processing, we began trimming the features to build a dataset that would be suitable as an input into various classification models. We also conducted some basic feature engineering, such as calculation of total active days and time to launch.
Following this, the non numerical data was encoded using sklearn's LabelEncoder, giving us a numerical dataset to feed into the models.
The now encoded data was split into a validation set and a testing set, with the validation set being from the recent market volatility of 2020. Following this, values were scaled using sklearn's StandardScaler, and train/test split was done to feed into various models.
Some things that were tested but didn't make it into the final data model included Random Over sampling to address the imbalanced dataset, removal of 'live' and 'cancelled' states from the final predictions and the testing of regressive models as a predictor of funding amount.


## Support Vector Machine (SVM) Classification Model

### Parameters
* Target Vector : State (Successful, Live, Failed, Cancelled)
* Data-points : 30,992 rows x 13 columns (fairly imbalanced dataset - State is heavily skewed to 
'Successful' 19,712 rows vs 'Failed' 9,538 rows vs 'Canceled' 953 and 'Live' 789 rows)
* Validation dataset : 2,295 rows
* Train-test dataset : 28,697 rows
* SVM type: Linear

### Key Findings
* In fitting the model, we note that the number of iteration has a bearing on the prediction accuracy.
* Generally, as the number of iteration increases so does the prediction accuracy.
* However, the setback is that the model will tend to overfit i.e. it can predict accurately based on
the training data but will likely perform poorly on unseen data.
* The challenge then becomes finding the optimal training parameters that yields the best fit through trial and error.

### Comparing The Two Versions

#### Version 1
![Version 1 Validation Data](images/SVM_P_v1.jpg) ![Version 1 Validation Classification Report](images/SVM_R_v1.jpg)

![Version 1 Train Test Data](images/SVM_TT_P_v1.jpg) ![Version 1 Train Test Classification Report](images/SVM_TT_R_v1.jpg)

#### Version 2

![Version 2 Validation Data](images/SVM_P_v2.jpg) ![Version 2 Validation Classification Report](images/SVM_R_v2.jpg)

![Version 2 Train Test Data](images/SVM_TT_P_v2.jpg) ![Version 2 Train Test Classification Report](images/SVM_TT_R_v2.jpg)

---
## Random Forest Classifier

### Features

Most important features appear to be relativly evenly split, the results are not heavily skewed by the value of any one feature.

![feature_importances](images/Feature_importances.png)

### Classification report

The smaller validation set appeared to have a higher accuracy than the training/testing set. This is possibly due to the skewness of the data and a tendency for the model to overfit when using a smaller data set. Implementing an over/undersampling step may alleviate these problems.

![classification_reports](images/Classification_reports_random_forest.png)

### Confusion Matrix
It is also evident that the model is incapable of accuratly predicting the lesser known states, the poor precision/recal of the 'cancelled' state is due to the model often confusing this state with a failed state.

![confusion_matrix](images/Testing_cm.png)
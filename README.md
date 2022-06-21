# Project-2---Predicting-Crowdfunding-Outcomes
This project was inspired by a research paper by S.Khosla et al. The paper discussed the application of various machine learning models to predict the outcome of Kickstarter projects. The results obtained in the paper were quite reproducable, as many of the models tested in this project see similar accuracy scores to that of the Standford paper, albeit with slightly different methodology/data. [Read the paper here](https://cs229.stanford.edu/proj2021spr/report2/81995033.pdf)

This repository includes the data collection, processing and model building as well as a small streamlit application for anyone wanting to test out the model with their own input data.

## Raw data
All of the data used in this project was sourced from a pre-existing amazon s3 bucket, which was compiled by a [web scraping service](https://webrobots.io/kickstarter-datasets/), The download link for the exact dataset used can be found [here](https://s3.amazonaws.com/weruns/forfun/Kickstarter/Kickstarter_2022-04-21T03_20_08_060Z.zip).

## SQL Database 
The raw data is a zip file which contains a set of csv files, of which some columns contain JSON objects. The files were concatenated along rows to build one large data frame. This gave approximately 30000 data points each with more than 30 individual features. Some of the features were expressed as a JSON, these features required some extra data wrangling to unpack so that we could use them. The make_database.py script will populate an SQL database with the extracted original dataframe and JSON objects. 

If you wish to run this code on your local machine, ensure that you have set up an SQL DB and have the extracted CSV files in a folder named 'raw_data' in the SQLDatabase directory. Also  ensure you have a .env file with 'KICKSTARTER_DB_URL' as a variable to ensure that the python script can connect with your DB.

![DB_schema](images/Database%20Schema.png)

---
## Preprocessing and Feature engineering
Features were selected form the databe using an SQL engine and pandas. The query was written to select data that would only have been available prior to the the kickstarter project ending. Data preprocessing consisted of dropping of duplicates, NaN values and some low level feature engineering. Non-neumerical features were encoded using a OneHotEncoding and all other values were scaled using a standard scaler.

---
## Model exploration
Four different classification models have been have been tested on the training data.

### Random Forest
SKlearn's RandomForest was used with no changes to the hyperparameters and returns an accuracy of 80% for the testing data, this aligns very closely to the results obained in the Stanford paper. 

### Support Vector Machine (SVM)
The Support vector machine was run using a linear kernel, and the gradient was iterated 500 times. This model yeilded a testing accuracy of 67%, with results heavily skewed toward the 'successful' project state, likely because of the imbalanced nature of the dataset. This result falls short of the Stanford paper of 79% accuracy, and is probably attirbuted to the lack of under/over sampling of the data. 

### SKlearn's Neural Network
SKlearn's implementation of a multi-layer perceptron classifier was used with the lbfgs solver and an architecture of (input,4,2,1). The model achieved an accuracy of 80%, equivalent to the 80% achieved in the Stanford paper. Given more data processing and feature engineering, this model could see significant improvements in performance as it faces similar problems to the SVM with the imbalanced dataset.

### XGBoost
The implementation of the XGBoosting algorithm was used as a comparison to the random forest classifier, the parameters for XGBoost were chosen after a small amount of manual trial and error however, a gridSearch would be nessecary for optimal model performance. The XGBoosted model achieved an accuracy score of 83% making it almost identical to the Random forest model and the Stanford paper's result (although the paper used only gradient boosting, not XGBoost).

---
## App
a small applcation was built using streamlit to allow users to play around with the pretrained random forest, SVM and neural network models. [The app is hosted using streamlit's free service here.](https://share.streamlit.io/epicosp/predicting-crowdfunding-outcomes/main/app/app.py)

### Pipeline
The data processing steps used in the model selection section were compressed into an sklearn pipeline, the Random forest, SVM and neural network models were pickled into .sav files to be used as predictors in the app.




---
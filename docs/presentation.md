### Presentation guidelines
---
 - Core message/hyptothesis

 how accuraly can we predict the success/failure of a kickstarter project based on data available at th early stages of a project lifecycle?

---

- Elaborate on predictive model/reasons it was chosen

models chosen were models typically used for classication tasks, this task in particular is a binary classification task hence the reason for comparing SVM/Naive Bayes/RandomForest

---

- Describe data Clean/model training

The Data was obtained from pre-existing s3 bucket built from a webscraping tool, the original dataset contained a variety of columns with different data types, including json objects. The columns containing JSON's were unpacked and stored as seperate files. 

A model appropriate data frame was built using features that are obtainable at the beginning or near the beginning of a kickstarter project.

We came across issues with some data perfectly describing the success of a project as this data is only available after a projects completion. these features had to be trimmed from the data set as the models were giving 100% accuracy scores.

---

- Discuss the techniques for model evaluation

models were primarilty evaluated using a combination of precision/recall/f1 score and accuracy. Other metrics explored were the ROC curve and AUC.

---

- Were the models sufficient for a predictive task?

---

- Discuss dificulties/challenges  and how they were dealt with

---

- Discuss additional questions/problems to solve given more time



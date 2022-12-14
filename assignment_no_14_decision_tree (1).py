# -*- coding: utf-8 -*-
"""Assignment No-14-Decision Tree.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11H13XfA-zMWqh9skP2C3pHVhGcoxDucf

# Question.1- Fraud Data

Q. Use Decision Trees to prepare a model on fraud data treating those who have taxable_income <= 30000 as "Risky" and others are "Good".

Data Description :

Undergrad : person is under graduated or not

Marital.Status : marital status of a person

Taxable.Income : Taxable income is the amount of how much tax an individual owes to the government

Work Experience : Work experience of an individual person

Urban : Whether that person belongs to urban area or not

# Import Libraries / Load dataset
"""

#importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets  
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import  DecisionTreeClassifier
from sklearn import tree
from sklearn.metrics import classification_report
from sklearn import preprocessing
import warnings
warnings.filterwarnings('ignore')
from sklearn.metrics import classification_report, confusion_matrix 
from sklearn.tree import plot_tree
from sklearn.metrics import accuracy_score#importing metrics for accuracy calculation (confusion matrix)
from sklearn.ensemble import BaggingClassifier#bagging combines the results of multipls models to get a generalized result. 
from sklearn.ensemble import AdaBoostClassifier #boosting method attempts to correct the errors of previous models.

df = pd.read_csv("Fraud_check.csv")
#Viewing top 5 rows of dataframe
df.head()

#Creating dummy vairables for ['Undergrad','Marital.Status','Urban'] dropping first dummy variable

df=pd.get_dummies(df,columns=['Undergrad','Marital.Status','Urban'], drop_first=True)

#Creating new cols TaxInc and dividing 'Taxable.Income' cols on the basis of [10002,30000,99620] for Risky and Good
df["TaxInc"] = pd.cut(df["Taxable.Income"], bins = [10002,30000,99620], labels = ["Risky", "Good"])

"""# **Lets assume: taxable_income <= 30000 as ???Risky=0??? and others are ???Good=1???**"""

#After creation of new col. TaxInc also made its dummies var concating right side of df
df = pd.get_dummies(df,columns = ["TaxInc"],drop_first=True)

#Viewing top 10 observations
df.head(10)

# let's plot pair plot to visualise the attributes all at once
import seaborn as sns
sns.pairplot(data=df, hue = 'TaxInc_Good')

# Normalization function 
def norm_func(i):
    x = (i-i.min())/(i.max()-i.min())
    return (x)

# Normalized data frame (considering the numerical part of data)
df_norm = norm_func(df.iloc[:,1:])
df_norm.head(10)

# Declaring features & target
X = df_norm.drop(['TaxInc_Good'], axis=1)
y = df_norm['TaxInc_Good']

from sklearn.model_selection import train_test_split

# Splitting data into train & test
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=0)

##Converting the Taxable income variable to bucketing. 
df_norm["income"]="<=30000"
df_norm.loc[df["Taxable.Income"]>=30000,"income"]="Good"
df_norm.loc[df["Taxable.Income"]<=30000,"income"]="Risky"

##Droping the Taxable income variable
df.drop(["Taxable.Income"],axis=1,inplace=True)

df.rename(columns={"Undergrad":"undergrad","Marital.Status":"marital","City.Population":"population","Work.Experience":"experience","Urban":"urban"},inplace=True)
## As we are getting error as "ValueError: could not convert string to float: 'YES'".
## Model.fit doesnt not consider String. So, we encode

from sklearn import preprocessing
le=preprocessing.LabelEncoder()
for column_name in df.columns:
    if df[column_name].dtype == object:
        df[column_name] = le.fit_transform(df[column_name])
    else:
        pass

##Splitting the data into featuers and labels
features = df.iloc[:,0:5]
labels = df.iloc[:,5]

## Collecting the column names
colnames = list(df.columns)
predictors = colnames[0:5]
target = colnames[5]
##Splitting the data into train and test

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(features,labels,test_size = 0.2,stratify = labels)

"""# **Building Decision Tree Classifier using Entropy Criteria**"""

model = DecisionTreeClassifier(criterion = 'entropy',max_depth=3)
model.fit(x_train,y_train)

from sklearn import tree

#PLot the decision tree
tree.plot_tree(model);

colnames = list(df.columns)
colnames

fn=['population','experience','Undergrad_YES','Marital.Status_Married','Marital.Status_Single','Urban_YES']
cn=['1', '0']
fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=300)
tree.plot_tree(model,
               feature_names = fn, 
               class_names=cn,
               filled = True);

#Predicting on test data
preds = model.predict(x_test) # predicting on test data set 
pd.Series(preds).value_counts() # getting the count of each category

preds

pd.crosstab(y_test,preds) # getting the 2 way table to understand the correct and wrong predictions

# Accuracy 
np.mean(preds==y_test)

"""# **Building Decision Tree Classifier (CART) using Gini Criteria**"""

from sklearn.tree import DecisionTreeClassifier
model_gini = DecisionTreeClassifier(criterion='gini', max_depth=3)

model_gini.fit(x_train, y_train)

#Prediction and computing the accuracy
pred=model.predict(x_test)
np.mean(preds==y_test)

"""# **Decision Tree Regression**"""

# Decision Tree Regression
from sklearn.tree import DecisionTreeRegressor

array = df.values
X = array[:,0:3]
y = array[:,3]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)

model = DecisionTreeRegressor()
model.fit(X_train, y_train)

#Find the accuracy
model.score(X_test,y_test)



"""# **Question.2- Company Data**

Problem Statement:
A cloth manufacturing company is interested to know about the segment or attributes causes high sale. 

Approach - A decision tree can be built with target variable Sale (we will first convert it in categorical variable) & all other variable will be independent in the analysis.  

About the data: 
Let???s consider a Company dataset with around 10 variables and 400 records. 
The attributes are as follows: 
*  Sales -- Unit sales (in thousands) at each location
* Competitor Price -- Price charged by competitor at each location
* Income -- Community income level (in thousands of dollars)
* Advertising -- Local advertising budget for company at each location (in thousands of dollars)
* Population -- Population size in region (in thousands)
* Price -- Price company charges for car seats at each site
* Shelf Location at stores -- A factor with levels Bad, Good and Medium indicating the quality of the shelving location for the car seats at each site
* Age -- Average age of the local population
* Education -- Education level at each location
* Urban -- A factor with levels No and Yes to indicate whether the store is in an urban or rural location
* US -- A factor with levels No and Yes to indicate whether the store is in the US or not
The company dataset looks like this:

# **Load dataset / EDA**
"""

#reading the data
company = pd.read_csv('/content/Company_Data.csv')
company.head()

company.dtypes

#getting information of dataset
company.info()

company.shape

company.isnull().sum()

from sklearn import preprocessing
le=preprocessing.LabelEncoder()

df['ShelveLoc']=df['ShelveLoc'].map({'Good':1,'Medium':2,'Bad':3})
company["Urban"]=le.fit_transform(company["Urban"])
company["US"]=le.fit_transform(company["US"])

from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

company.head()

company=company.assign(Sale=pd.cut(company['Sales'], 
                               bins=[ 0, 4, 9,15], 
                               labels=['Low', 'Medium', 'High']))

company.head()

# let's plot pair plot to visualise the attributes all at once
sns.pairplot(data=company, hue = "Sale")

# correlation matrix
sns.heatmap(company.corr())

target = pd.DataFrame.astype(company['Sale'], dtype="object")
df1 = company.copy()
df1 = df1.drop('Sale', axis =1)

# Defining the attributes
X = df1

target = target.fillna('').apply(str)
target

#label encoding
target = le.fit_transform(target)
target

y = target

# Splitting the data - 80:20 ratio
X_train, X_test, y_train, y_test = train_test_split(X , y, test_size = 0.2, random_state =25)
print("Training split input- ", X_train.shape)
print("Testing split input- ", X_test.shape)

# Defining the decision tree algorithm
dtree=DecisionTreeClassifier()
dtree.fit(X_train,y_train)
print('Decision Tree Classifier Created')

# Predicting the values of test data
y_pred = dtree.predict(X_test)
#print("Classification report - \n", classification_report(y_test,y_pred))

#2 Way table to understand the correct and wrong  predictions

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5,5))
sns.heatmap(data=cm,linewidths=.5, annot=True,square = True,  cmap = 'Blues')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
all_sample_title = 'Accuracy Score: {0}'.format(dtree.score(X_test, y_test))
plt.title(all_sample_title, size = 14)

#PLot the decision tree
from sklearn import tree
tree.plot_tree(dtree);

"""# **Building Decision Tree Classifier using Entropy Criteria**

"""

#Building Decision Tree Classifier using Entropy Criteria

model = DecisionTreeClassifier(criterion = 'entropy',max_depth=3)
model.fit(X_train,y_train)

# Predicting the values of test data
y_pred1 = model.predict(X_test)

#2 Way table to understand the correct and wrong  predictions

cm = confusion_matrix(y_test, y_pred1)
plt.figure(figsize=(5,5))
sns.heatmap(data=cm,linewidths=.5, annot=True,square = True,  cmap = 'Blues')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
all_sample_title = 'Accuracy Score: {0}'.format(model.score(X_test, y_test))
plt.title(all_sample_title, size = 14)

#PLot the decision tree
from sklearn import tree
tree.plot_tree(model);

"""# **Building Decision Tree Classifier (CART) using Gini Criteria**"""

#Building Decision Tree Classifier (CART) using Gini Criteria
model_gini = DecisionTreeClassifier(criterion='gini', max_depth=3)

model_gini.fit(X_train, y_train)

#Prediction and computing the accuracy
pred=model.predict(X_test)
np.mean(pred==y_test)

"""#**Decision Tree Regression**"""

#Decision Tree Regression Example
from sklearn.tree import  DecisionTreeRegressor
model1 = DecisionTreeRegressor()
model1.fit(X_train, y_train)

#Find the accuracy
model1.score(X_test,y_test)
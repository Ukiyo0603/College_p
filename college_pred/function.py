import pandas as pd
import numpy as np
import seaborn as sns
from sqlalchemy import false
from college_pred.forms import InputDataForm


data = pd.read_csv('/Users/shivanimakde/PBLproject/College-Predictor/A_PBL_DATA_CLG.csv')

data.head()

print(data.columns)

print(data.shape)

form = InputDataForm()
user_percent = {{ form.percentile.data }}
user_category = {{ form.category.data }}
user_branch = {{ form.branch.data }}


#CONCERT TO LIST
marks = data['MeritScore'].tolist()
Cllg = data['CollegeName'].tolist()
Branch = data['CourseName'].tolist()
Category = data['SeatTypeCode'].tolist()

output = []
output1 = []
finaloutput = []
finalCllg = []
finalMarks = []

def selected(percent, category, branch):
    # To filter the College in which the user can get admission according to his percent
    for i in range(18630):
        if marks[i] <= percent:
            output.append(i)
    
    #To filter the College in which the user can get admission according to his percent, Category
    for i in range(len(output)):
        if Category[output[i]] == category:
            output1.append(output[i])
    
    #To filter the College in which the user can get admission according to his percent, category and Branch

    for i in range(len(output1)):
        if Branch[output1[i]] == branch:
            finaloutput.append(output1[i])

selected(user_percent, user_category, user_branch)

for j in finaloutput:
    finalCllg.append(Cllg[j])
    finalMarks.append(marks[j])

df = pd.DataFrame({"College Name": finalCllg, "CutOff":finalMarks })

df.to_excel('predicted.xlsx', sheet_name='Sheet1', index=false)



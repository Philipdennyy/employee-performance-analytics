import pandas as pd
import numpy as np
df= pd.read_csv("raw.csv")
print("Shape =", df.shape)
df["CurrentSalaryBand"] = df["CurrentSalaryBand"].fillna(df["CurrentSalaryBand"].median())
df["CurrentSalaryBand"] = df["CurrentSalaryBand"].astype(int)
df["TasksCompleted"] = np.minimum(df["TasksCompleted"], df["TasksAssigned"])
df["BugsFixed"] = np.minimum(df["BugsFixed"], df["BugsReported"])
df["TaskCompletionRate"] = df["TasksCompleted"]/ df["TasksAssigned"]
df["BugsResolutionRate"] = np.where(df["BugsReported"] ==0, 1, df["BugsFixed"]/df["BugsReported"])
df["ResponseEfficiency"] = 1 - (df["AvgResponseTimeHours"]/24)
df["DeliveryScore"] = (df["TaskCompletionRate"]*40 + df["DeadlineMeetRate"]*0.3 + df["SprintCompletionRate"]*0.3)
df["QualityScore"] = (df["BugsResolutionRate"]*40 + df["CodeReviewPassRate"]*0.4 + (1 - df["ReworkCount"]/(df["ReworkCount"].max() +1))*20) 
df["ReliabilityScore"] =(df["AttendanceRate"]*0.5 + df["ResponseEfficiency"]*50)
df["LearningScore"] = (
    (df["TrainingsCompleted"] / 6) * 100 * 0.4 +
    (df["NewSkillsLearned"] / 5) * 100 * 0.3 +
    (df["Certifications"] / 3) * 100 * 0.3
)

df["FinalPerfomanceScore"] = (df["DeliveryScore"]*0.3 + df["QualityScore"]*0.3 + df["ReliabilityScore"]*0.2 + df["LearningScore"]*0.2)
df["EmpID"] = "Dev_"+ df["EmpID"].astype(str)
df.to_csv("processed_dataset.csv", index=False)

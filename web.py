import pandas as pd
import streamlit as st
import plotly.express as px
df= pd.read_csv("processed_dataset.csv")
st.title("Developer Performance Analytics Dashboard")
st.sidebar.header("Filter")
team_list = sorted(df["Team"].unique())
Selected_Team = st.sidebar.selectbox("Select Team", team_list)
team_df = df[df["Team"]== Selected_Team]
Dev_list = sorted(team_df["EmpID"].unique(),key=lambda x: int(x.split("_")[1]))
Selected_Dev = st.sidebar.selectbox("Select Dev", Dev_list)
Dev_data = team_df[team_df["EmpID"]== Selected_Dev]
st.subheader("Developer Details")
st.dataframe(Dev_data)
Dev= Dev_data.iloc[0]
st.header("Perfomance Summary")
st.metric(label= "Final Perfomance Score", value = round(Dev["FinalPerfomanceScore"],2 ))
col1, col2,col3,col4 = st.columns(4)
col1.metric("Delivery Score", round(Dev["DeliveryScore"]))
col2.metric("Quality Score", round(Dev["QualityScore"]))
col3.metric("ReliabilityScore",round(Dev["ReliabilityScore"]))
col4.metric("Learning Score", round(Dev["LearningScore"]))
st.subheader("Team Comparison")
team_avg_score = team_df["FinalPerfomanceScore"].mean()
st.metric("Team Average Score",round(team_avg_score,2)) 
difference = Dev["FinalPerfomanceScore"] - team_avg_score
if difference > 5:
    st.success("This developer is performing ABOVE team average")
elif difference < -5:
    st.error("This developer is performing BELOW team average")
else:
    st.info("This developer is performing CLOSE to team average")
    st.subheader("Salary Fairness Analysis")
score = Dev["FinalPerfomanceScore"]
salary = Dev["CurrentSalaryBand"]
if score>=85:
    expected  = 5
elif score>=75:
    expected = 4
elif score>=65:
    expected = 3
elif score>=55:
    expected = 2
else:
    expected  = 1
band_meaning = {
    1: "Fresher (3–6 LPA)",
    2: "Junior Developer (6–10 LPA)",
    3: "Mid-Level Developer (10–15 LPA)",
    4: "Senior Developer (15–20 LPA)",
    5: "Lead / Expert (20+ LPA)"
}
st.write("Expected Salary Level:", band_meaning[expected])
st.write("Current Salary Level:", band_meaning[salary])
if expected > salary:
    st.warning("Employee may be UNDERPAID")
elif expected < salary:
    st.warning("Employee may be OVERPAID")
else:
    st.success("Salary matches performance level")
fig = px.histogram(team_df,x= "FinalPerfomanceScore",nbins= 20, title="How performance scores are spread in the team")
fig.add_vline(x= Dev["FinalPerfomanceScore"], line_width= 3, line_dash= "dash",line_color = "red")
st.plotly_chart(fig, use_container_width= True)
st.subheader("Team Leaderboard")
leaderboard = team_df.sort_values(by = "FinalPerfomanceScore", ascending= False)[["EmpID","FinalPerfomanceScore","CurrentSalaryBand"]]
leaderboard = leaderboard.reset_index(drop=True)
leaderboard.index = leaderboard.index+1
st.dataframe(leaderboard, use_container_width= True)
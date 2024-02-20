import streamlit as st
import csv 
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns



def load_data():
    df = pd.read_csv('Expanded_data_with_more_features.csv', encoding='unicode_escape')
    df.dropna(inplace=True)
    df.drop('Unnamed: 0', inplace=True, axis=1)
    df.reset_index(drop=True, inplace=True)
    df.index += 1

    return df


def main():
    
    st.markdown("""
    <style>
        /* Metric */
        div[data-testid="stMetric"] {
            border: 2px solid #007bff; /* Add a blue border */
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 20px;
        }

        /* Table */
        div[data-testid="stDataTable"] {
            border: 2px solid #007bff; /* Add a blue border */
            border-radius: 5px;
            padding: 10px;
        }
    </style>
    """, unsafe_allow_html=True) 
   
    with st.spinner("Loading..."):
        time.sleep(5)
    st.success('WELCOME')
    st.sidebar.header("**Student Score Analysis 📊**")
    df = load_data()

    st.sidebar.image("student_img.webp", use_column_width=True) 
    
    with st.sidebar:
        add_radio = st.radio(
        "Choose options 👇 ",
        (":rainbow[View Dataset]", ":rainbow[Statistics Analysis]",":rainbow[Outlier Detection]"))




    if add_radio==":rainbow[View Dataset]":
        col1, col2, col3 ,col4= st.columns(4)
        col1.metric("Total Students", "19243")#, "1.2 °F")
        col2.metric("Avg Math Score" ,"66.63")
        col3.metric("Avg Writing Score", "69.53")
        col4.metric("Avg Reading Score", "68.60")
        st.header("**Students Score Analysis**")
        st.table(df.head(10).style.set_table_attributes({"width": "100%"}))
        


    if add_radio == ":rainbow[Statistics Analysis]":
       st.header('Genderwise count')
       fig, ax = plt.subplots(figsize=(10, 5)) 
       ax = sns.countplot(x='Gender', data=df)
       for p in ax.patches:
          ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', fontsize=10, color='black', xytext=(0, 8), textcoords='offset points')
       st.set_option('deprecation.showPyplotGlobalUse', False)
       st.pyplot()
       
       g1=df.groupby('ParentEduc').agg({'MathScore':'mean','ReadingScore':'mean','WritingScore':'mean'})
       st.header('Parent educ and children Scores')
       g1_reset=g1.reset_index().sort_values('MathScore', ascending=False)
       g1_reset.reset_index(drop=True, inplace=True)
       g1_reset.index+=1
    
       rename = ["Master's Degree","Bachelor's Degree","Associate's Degree","Some College","High School","Some High School"]
       g1_reset['ParentEduc']=rename
       st.table(g1_reset)
       


       st.header("Ethnicwise Data")
       GroupA= df.loc[(df['EthnicGroup'] =="group A")].count()
       GroupB= df.loc[(df['EthnicGroup'] =="group B")].count()
       GroupC= df.loc[(df['EthnicGroup'] =="group C")].count()
       GroupD= df.loc[(df['EthnicGroup'] =="group D")].count()
       GroupE= df.loc[(df['EthnicGroup'] =="group E")].count()

       mlist=[GroupA['EthnicGroup'],GroupB['EthnicGroup'],GroupC['EthnicGroup'],GroupD['EthnicGroup'],GroupE['EthnicGroup']]
       l=['Group A','Group B','Group C','Group D','Group E']

       mlist = pd.Series([GroupA['EthnicGroup'], GroupB['EthnicGroup'], GroupC['EthnicGroup'], GroupD['EthnicGroup'], GroupE['EthnicGroup']])
       new_list = mlist.reset_index().rename(columns={"index": "Group", 0: "Count"})
       new_group_names = ['Group A', 'Group B', 'Group C', 'Group D', 'Group E']
       new_list.index+=1

       new_list['Group'] = new_group_names
       
       st.table(new_list)

       st.header("Ethnic Group Distribution")
       fig, ax = plt.subplots(figsize=(10, 5))  
       ax.pie(mlist, labels=l, autopct='%1.2f%%')
       ax.axis('equal')  
       st.pyplot(fig)


       st.header('Weekly study hrs and score')
       study_hrs=df.groupby('WklyStudyHours').agg({'MathScore':'mean','ReadingScore':'mean','WritingScore':'mean'})
       study_hrs=study_hrs.sort_values('MathScore', ascending=False)
       st.table(study_hrs)
      
       fig, ax = plt.subplots(figsize=(10, 5)) 
       ax= sns.heatmap(study_hrs, annot=True)
       st.pyplot(fig)

       st.header(' LunchType and Score')
       g4=df.groupby('LunchType').agg({'MathScore':'mean','ReadingScore':'mean','WritingScore':'mean'})
       g4.reset_index()
       g5=g4.sort_values('MathScore', ascending=False)
       st.table(g5)
       fig, ax = plt.subplots(figsize=(10, 5)) 
       ax=sns.heatmap(g5, annot=True)
       st.pyplot(fig)



    if add_radio == ":rainbow[Outlier Detection]":
       
       selected_col = ["ReadingScore", "WritingScore", "MathScore"]
       selected_boxplot=st.sidebar.selectbox("Select Score 👇 ", selected_col)

       fig , ax = plt.subplots(figsize=(10,5))
       st.header('Boxplot of '+selected_boxplot)
       ax =sns.boxplot(data=df, x = selected_boxplot,ax= ax)
       st.pyplot(fig)




    # st.sidebar.write("Made by Vishal Verma")
    st.sidebar.markdown("[Create by Vishal Verma Linkedin](https://www.linkedin.com/in/vishal-verma-4632a1244/)")
         
if __name__ == "__main__":
    main()
   

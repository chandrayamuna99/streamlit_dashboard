# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

company_list = ['C:\\S&P_resources\\individual_stocks_5yr\\AME_data.csv',
                'C:\\S&P_resources\\individual_stocks_5yr\\AAPL_data.csv',
                'C:\\S&P_resources\\individual_stocks_5yr\\GOOGL_data.csv',
                'C:\\S&P_resources\\individual_stocks_5yr\\MSFT_data.csv']

all_data=pd.DataFrame()

for file in company_list:
    current_file=pd.read_csv(file)
    all_data=pd.concat([all_data,current_file],ignore_index=True)

all_data['date']=pd.to_datetime(all_data['date'])


st.set_page_config(page_title="stock analysis dashboard",layout="wide")
st.title("Tech stocks analysis dashboard")

tech_list=all_data['Name'].unique()
st.sidebar.title("choose a company")
selected_company=st.sidebar.selectbox("Select a box",tech_list)

company_df=all_data[all_data["Name"]==selected_company]
company_df.sort_values("date",inplace=True)

#plot 1
st.subheader(f"1. {selected_company} Time series analysis by close")
fig1=px.line(company_df,x="date",y="close",title="closing prices over time")
st.plotly_chart(fig1,use_container_width=True)

#plot 2
st.subheader(f"2. {selected_company} mean average (10,20,50)")

list=[10,20,50]
new_data=all_data.copy()
for ma in list:
    company_df["close_"+str(ma)]=company_df["close"].rolling(ma).mean()
    
fig2=px.line(company_df,x="date",y=["close","close_10","close_20","close_50"],title="closing prices mean average")
st.plotly_chart(fig2,use_container_width=True)

#plot 3   
st.subheader(f"3. Daily return for {selected_company}")

company_df['daily return (in%)']=company_df['close'].pct_change()*100


fig3=px.line(company_df,x="date",y='daily return (in%)',title="Daily return percentage")
st.plotly_chart(fig3,use_container_width=True)


#plot 4
st.subheader(f"4. Resampled closing price {selected_company}")

company_df.set_index("date",inplace=True)
resample_option=st.radio("select resample frequency",["monthly","quarterly","yearly"])

if resample_option=="monthly":
    resampled=company_df['close'].resample('ME').mean().reset_index()

elif resample_option=="quarterly":
    resampled=company_df['close'].resample('QE').mean().reset_index()
    
else:
    resampled=company_df['close'].resample('YE').mean().reset_index()


fig4 = px.line(resampled,x='date',y='close',title="Average Closing Price")
st.plotly_chart(fig4,use_container_width=True)

#plot 5

st.subheader(f"5. correlation in close price")
amez=pd.read_csv(company_list[0])
app=pd.read_csv(company_list[1])
googl=pd.read_csv(company_list[2])
msft=pd.read_csv(company_list[3])

closing_price=pd.DataFrame()
closing_price["amez_close"]=amez["close"]
closing_price["app_close"]=app["close"]
closing_price["googl_close"]=googl["close"]
closing_price["msft_close"]=msft["close"]

fig5 = px.imshow(closing_price.corr(),color_continuous_scale="RdBu_r",title="Correlation Heatmap")
st.plotly_chart(fig5, use_container_width=True)



st.markdown("...")
st.markdown("**Note:**This dashboard provides basic technical analysis of major tech stocks using python and streamlit")









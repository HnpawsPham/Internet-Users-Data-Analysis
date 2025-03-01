import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from additional import *
from millify import millify

# SET LAYOUT
header_icon = get_base64_image("Final_Project/assets/internet.png")
st.markdown(f"""
    <div style="display: flex; justify-content: center;">
        <img src=data:image/png;base64,{header_icon} width="150">
    </div>
            
    <div style="text-align: center;">
        <h1>INTERNET USERS DATA ANALYSIS</h1><br>
        <h3>Data board</h3><br>
    </div>
    """, unsafe_allow_html=1)

df = pd.read_csv(".\\Final_Project\\internet_users.csv")

# CLEAN DATA
df["Year"] = df["Year"].fillna(0).astype(int)
df["Year.1"] = df["Year.1"].fillna(0).astype(int)
df["Year.2"] = df["Year.2"].fillna(0).astype(int)

df.loc[0, "Users (CIA)"] = df["Users (CIA)"].sum()

df["Rate (WB)"] = df["Rate (WB)"].fillna(0)
df["Rate (ITU)"] = df["Rate (ITU)"].fillna(0)
df["Users (CIA)"] = df["Users (CIA)"].fillna(0)

# DATA BOARD LAYOUT
col1, col2 = st.columns([0.8, 0.2]) 

with col1:
    st.dataframe(df, use_container_width=1)
with col2:
    st.table(pd.DataFrame(df.dtypes, columns=["Type"]))
    st.markdown(f"""
        <div style="background-color: white; padding: 10px; border-radius: 10px; line-height: 32px; color: {BLACK}; text-align: center;">
            Data Status<br>
            <p style="font-size: 28px; margin: 0 0 2px 20px; font-weight: bold;">Cleaned
                <svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="30px" fill="#2D2727"><path d="M382-240 154-468l57-57 171 171 367-367 57 57-424 424Z"/></svg>
            </p>
        </div>
    """,unsafe_allow_html=True)

add_endline(2)

# BASIC INFO
col3, col4, col5 = st.columns(3)
country_icon = get_base64_image("Final_Project/assets/country.png")
time_range_icon = get_base64_image("Final_Project/assets/time_range.png")
organization_icon = get_base64_image("Final_Project/assets/organization.png")

# Get all different years
years = [year for year in sorted(df["Year"].unique()) if year > 0]

with col3:
    createBasicInfoCol("Countries/ Regions", len(df["Location"]), country_icon)
with col4:
    createBasicInfoCol("Time range", f"{len(years)} years", time_range_icon)
with col5:
    createBasicInfoCol("Organization", "WB & ITU", organization_icon)

add_endline(2)

# GRAPHS

# Top users
df_users_sorted = df.sort_values(by="Users (CIA)", ascending=1)
df_users_sorted = df_users_sorted[df_users_sorted["Location"] != "World"]

st.subheader("Top 20 Countries/ Region with the MOST Internet users")

fig = px.bar(df_users_sorted.tail(20), x="Location", y="Users (CIA)", 
            color="Users (CIA)",
            color_continuous_scale="Viridis")
st.plotly_chart(fig)

col11, col12 = st.columns(2)

with col11:
    data = df_users_sorted.iloc[-1]
    num =  millify(data["Users (CIA)"], precision=3)
    createHotspotCol("Highest Internet usage", data["Location"], num, data["Rate (WB)"], data["Rate (ITU)"])
with col12:
    data = df_users_sorted.iloc[0]
    num =  millify(data["Users (CIA)"], precision=3)
    createHotspotCol("Lowest Internet usage", data["Location"], num, data["Rate (WB)"], data["Rate (ITU)"])

add_endline(3)

# Data from each organization
st.subheader("Comparing 2 Organization Internet users Rate")

st.markdown("""
    <h4 style="margin-bottom: -50px;">Choose a year</h4>
""", unsafe_allow_html=1)

years.insert(0, "All the time")
selected_year = st.selectbox("", years)

space, col6, col7 = st.columns([0.1, 1, 1])

with col6:
    fig1 = px.choropleth(df[df["Year"] == selected_year] if selected_year != "All the time" else df, 
                    locations="Location",   
                    locationmode="country names",
                    color = "Rate (WB)",
                    hover_name="Location", 
                    color_continuous_scale="Turbo")
    fig1.update_layout(title="By World Bank", title_x=0.32, title_y=0.25, margin={"b": 140})
    st.plotly_chart(fig1)
with col7:
    fig2 = px.choropleth(df[df["Year.1"] == selected_year] if selected_year != "All the time" else df, 
                    locations="Location",   
                    locationmode="country names",
                    color = "Rate (ITU)",
                    hover_name="Location", 
                    color_continuous_scale="Turbo")
    fig2.update_layout(title="By ITU", title_x=0.38, title_y=0.25, margin={"b": 140})
    st.plotly_chart(fig2)

col13, col14 = st.columns(2)
total_internet_users = df["Users (CIA)"].iloc[0]
df["Continent"] = df["Location"].apply(get_continent)

with col13:
    createContinentUsageCol("Internet usage", "Europe", 10, 10, total_internet_users)
with col14:
    df_asia = df[df["Continent"] == "Asia"]
    asia_users = df_asia.sum()

    createContinentUsageCol("Internet usage", "Asia", 10, asia_users, total_internet_users)

# Difference between to datas
df["Diff (ITU & WB)"] = (df["Rate (WB)"] - df["Rate (ITU)"]).abs()
diff_avg = df.groupby(["Year", "Location"],as_index=0)["Diff (ITU & WB)"].mean()
diff_avg = diff_avg[diff_avg["Year"] >= 2019]
diff_avg = diff_avg[diff_avg["Diff (ITU & WB)"] >= 0.1]

st.subheader("Median Internet users Rate Difference (ITU & WB) - All the time")

fig3 = px.bar(diff_avg, x="Year", y = "Diff (ITU & WB)",
            color="Location",
            barmode = "group")
fig3.update_layout(yaxis_type="log")
st.plotly_chart(fig3)

df["Median Difference"] = ((df["Rate (WB)"] - df["Rate (ITU)"]).abs() / df[["Rate (WB)", "Rate (ITU)"]].median(axis=1)) * 100
diff_percent_avg = df.groupby("Year", as_index=False)["Median Difference"].median()
diff_percent_avg = diff_percent_avg[diff_percent_avg["Year"] >= 2019]

min_diff = diff_percent_avg["Median Difference"].min()
max_diff = diff_percent_avg["Median Difference"].max()

most_accurate_year = diff_percent_avg.loc[diff_percent_avg["Median Difference"] == min_diff, "Year"].tolist()
least_accurate_year = diff_percent_avg.loc[diff_percent_avg["Median Difference"] == max_diff, "Year"].tolist()

diff_percent_avg["Median Difference"] = diff_percent_avg["Median Difference"].apply(lambda x: f"{x:.4f}%")

col8, col9, col10 = st.columns([1, 2, 2])

with col8:
    st.write(diff_percent_avg)
with col9:
    data = ', '.join(map(str, most_accurate_year))
    percent = f"{min_diff:.2f}%"
    createConclusionCol("Most Accurate Year", data, percent)
with col10:
    data = ', '.join(map(str, least_accurate_year))
    percent = f"{max_diff:.2f}%"
    createConclusionCol("Least Accurate Year", data, percent)
         
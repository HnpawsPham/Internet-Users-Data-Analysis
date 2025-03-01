import streamlit as st
import base64
import plotly.graph_objects as go
import pycountry_convert as pc

# COLORS
BLACK = "#2D2727"
GREEN = "#4E9F3D"
BLUE = "#4d8aeb"

# ADDITIONA FUNCS
def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()
    
def get_continent(location):
    try:
        country_code = pc.country_name_to_country_alpha2(location)
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_mapping = {
            "NA": "North America",
            "SA": "South America",
            "EU": "Europe",
            "AF": "Africa",
            "AS": "Asia",
            "OC": "Oceania"
        }
        return continent_mapping.get(continent_code, "Unknown")
    except:
        return "Unknown"

def create_half_gauge(val, max_val):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = val,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, max_val], 'tickvals': [0, max_val / 2, max_val]},
            'bar': {'color': "white", "thickness": 0.4},
            'bgcolor': "white",
            'borderwidth': 0,
            'bordercolor': "white",
            'axis': {'tickfont': {'size': 14}},
            'steps' : [
                 {'range': [0, max_val], 'color': f"{BLUE}"},
                 {'range': [max_val/2, max_val], 'color': f"{BLUE}"}],
            'threshold' : {'line': {'color': "black", 'width': 0}, 'thickness': 0.5, 'value': val}
        }))

    fig.update_layout(margin=dict(l=20, r=20, b=0, t=60), height=350)
    return fig


def createBasicInfoCol(title, data, icon):
    return st.markdown(f"""
        <div style="border-radius: 10px; background-color: white; color: black; padding: 15px 40px;">
            <p style="font-size: 20px; margin-bottom: 0px;">{title}</p>
            <div style="display: flex; align-items: center;">
                <img src="data:image/png;base64,{icon}" width="42px" height="42px">
                <b style="font-size: 42px; margin-left: 30px;">{data}</b>
            </div>
        </div>
    """, unsafe_allow_html=True)

def createHotspotCol(title, name, data, rate_wb, rate_itu):
    st.markdown(f"""
        <div style="background-color:#FFFFFF;padding:15px;border-radius:10px">
            <p style="color: {BLACK}; font-size:20px; position: relative;  padding-left: 5%;">
                <span style="position: absolute; background: {GREEN}; border-radius: 30px; color: white; padding: 3px 15px; right: 5px;">
                {data}</span><br><br>
                {title} <br>
                <b style="font-size: 42px">{name}</b> 
                <span style="position: absolute; left: 75%;"> 
                Rate:&ensp;{rate_wb} (WB) <br> {"&ensp;" * 5} {rate_itu} (ITU)</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

def createContinentUsageCol(title, name, data, usage, max_usage):
    fig = create_half_gauge(usage, max_usage)
    st.plotly_chart(fig)

def createConclusionCol(title, name, data):
    st.markdown(f"""
        <div style="background-color:#FFFFFF;padding:15px;border-radius:10px">
            <p style="color: {BLACK}; font-size:20px; position: relative;  padding-left: 5%;">
                <span style="position: absolute; background: {GREEN}; border-radius: 30px; color: white; padding: 3px 15px; right: 5px;">
                {data}</span><br><br>
                {title} <br>
                <b style="font-size: 42px">{name}</b> 
            </p>
        </div>
    """, unsafe_allow_html=True)

def add_endline(num):
    st.markdown("<br>" * num, unsafe_allow_html=1)

# COMMON STYLE CUSTOMING
st.set_page_config(layout='wide') #prevent bug 

st.markdown("""
    <style>
        h3 {
            padding-top: 50px !important;
            border-top: 1px solid white;
            text-align: center !important;
        }
    </style>
""", unsafe_allow_html=1)
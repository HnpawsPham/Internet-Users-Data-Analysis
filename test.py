import streamlit as st
import plotly.graph_objects as go

def create_half_gauge(value, min_value=0, max_value=500000, title_text=""):
    """Creates a half-gauge chart with a needle."""

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title_text, 'align': 'center'},
        gauge = {
            'axis': {'range': [min_value, max_value], 'tickvals': [min_value, max_value / 2, max_value], 'ticktext': ["$0", "$250k", "$500k"]},
            'bar': {'color': "lightcoral"}, #No line setting anymore
            'bgcolor': "white",
            'borderwidth': 0,  # Remove gauge border
            'bordercolor': "white",   #Ensure bg color and boder color match to hide any sign of a line
            'axis': {'tickfont': {'size': 14}}, # Set font size of tick labels
            'steps' : [
                 {'range': [min_value, max_value/2], 'color': "lightcoral"}, # set the gauge's color range
                 {'range': [max_value/2, max_value], 'color': "lightgray"}],
            'threshold' : {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': value}  # The needle
        }))

    fig.update_layout(margin=dict(l=20, r=20, b=0, t=60),  # Reduced bottom margin, increased top
                      height=350)   #Reduced height

    return fig

# Streamlit app
st.title("Half Gauge Chart")

# Example value (you can replace this with user input or data)
current_value = 200000

# Create the chart
fig = create_half_gauge(current_value)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio
import requests
import json

app = Flask(__name__)

def get_diabetes_data():
    api_url = 'https://api.glooko.com/v1/diabetes_data'  # Replace with actual endpoint
    headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  # Replace with your access token
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def create_charts(df, top_n):
    # Example: Bar chart for average glucose levels per state
    bar_fig = px.bar(
        df,
        x='state',
        y='average_glucose',
        title=f'Top {top_n} States: Average Glucose Levels',
        labels={'average_glucose': 'Average Glucose'},
        color='average_glucose',
        color_continuous_scale='Rainbow'
    )
    bar_fig.update_layout(
        xaxis_title='State',
        yaxis_title='Average Glucose',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    bar_fig_html = pio.to_html(bar_fig, full_html=False)

    # Create Pie Chart for Distribution of Average Glucose Levels
    pie_fig = px.pie(
        df,
        names='state',
        values='average_glucose',
        title=f'Distribution of Average Glucose Levels in Top {top_n} States'
    )
    pie_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest'
    )
    pie_fig_html = pio.to_html(pie_fig, full_html=False)

    # Create Enhanced Scatter Plot
    scatter_fig = px.scatter(
        df,
        x='average_glucose',
        y='number_of_patients',
        size='number_of_patients',
        color='state',
        title=f'Distribution of Glucose Levels and Number of Patients in Top {top_n} States',
        labels={'average_glucose': 'Average Glucose', 'number_of_patients': 'Number of Patients'},
        color_continuous_scale='Viridis',
        size_max=60
    )
    scatter_fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color='DarkSlateGrey')))
    scatter_fig.update_layout(
        xaxis_title='Average Glucose',
        yaxis_title='Number of Patients',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest'
    )
    scatter_fig_html = pio.to_html(scatter_fig, full_html=False)

    return bar_fig_html, pie_fig_html, scatter_fig_html

@app.route('/')
def index():
    diabetes_data = get_diabetes_data()
    
    # Assume the data is in a format that can be directly converted into a DataFrame
    df = pd.DataFrame(diabetes_data)
    
    top_n = int(request.args.get('top_n', 10))

    # Assuming we want to filter and sort by some metrics
    top_states = df.sort_values(by='average_glucose', ascending=False).head(top_n)

    bar_fig_html, pie_fig_html, scatter_fig_html = create_charts(top_states, top_n)

    # Prepare data for the Apex chart if needed
    apex_chart_data = {
        "categories": top_states['state'].tolist(),
        "average_glucose": top_states['average_glucose'].tolist(),
    }

    return render_template('diabetes.html', 
                           bar_fig_html=bar_fig_html,
                           pie_fig_html=pie_fig_html,
                           scatter_fig_html=scatter_fig_html,
                           top_n=top_n,
                           apex_chart_data=json.dumps(apex_chart_data))

if __name__ == '__main__':
    app.run(debug=True)

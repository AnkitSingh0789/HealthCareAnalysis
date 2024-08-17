from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json

app = Flask(__name__)

# Dummy data for all 36 states and union territories for diabetes analysis
data = {
    'State': ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
              'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
              'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
              'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands', 'Chandigarh',
              'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Lakshadweep', 'Puducherry', 'Ladakh', 'Jammu and Kashmir'],
    'Cases': [1500000, 200000, 1200000, 1400000, 800000, 300000, 2500000, 1100000, 500000, 900000, 2000000, 
              1800000, 1600000, 3000000, 400000, 600000, 250000, 350000, 1300000, 1100000, 1700000, 150000, 
              2200000, 1300000, 450000, 1600000, 500000, 2000000, 80000, 150000, 120000, 1500000, 50000, 200000, 
              70000, 500000],
    'Deaths': [30000, 10000, 25000, 28000, 15000, 5000, 50000, 22000, 10000, 18000, 45000, 
               40000, 35000, 65000, 8000, 12000, 6000, 9000, 26000, 22000, 34000, 3000, 
               44000, 26000, 9000, 32000, 10000, 40000, 2000, 3000, 2500, 30000, 1000, 4000, 
               1500, 10000],
    'Recovered': [900000, 150000, 800000, 850000, 500000, 200000, 1500000, 700000, 300000, 500000, 1300000, 
                  1100000, 1000000, 2000000, 250000, 350000, 150000, 250000, 800000, 700000, 1000000, 90000, 
                  1400000, 800000, 300000, 1000000, 300000, 1200000, 60000, 90000, 75000, 900000, 40000, 150000, 
                  50000, 300000],
    'Active': [570000, 35000, 320000, 525000, 285000, 95000, 950000, 380000, 190000, 380000, 700000, 
               650000, 570000, 1000000, 142000, 238000, 94000, 90000, 510000, 380000, 670000, 57000, 
               760000, 470000, 141000, 580000, 190000, 760000, 18000, 57000, 42500, 600000, 9000, 46000, 
               19000, 190000]
}

df = pd.DataFrame(data)

df['Cure Rate (%)'] = (df['Recovered'] / df['Cases']) * 100
df['Death Rate (%)'] = (df['Deaths'] / df['Cases']) * 100

def create_charts(top_states, top_n):
    # Create Colorful Bar Chart for Cases per State
    bar_fig = px.bar(
        top_states,
        x='State',
        y='Cases',
        title=f'Top {top_n} States in India: Diabetes Cases',
        labels={'Cases': 'Number of Cases'},
        color='Cases',
        color_continuous_scale='Rainbow'
    )
    bar_fig.update_layout(
        xaxis_title='State',
        yaxis_title='Number of Cases',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    bar_fig_html = pio.to_html(bar_fig, full_html=False)

    # Create Pie Chart for Distribution of Cases
    pie_fig = px.pie(
        top_states,
        names='State',
        values='Cases',
        title=f'Distribution of Diabetes Cases in Top {top_n} States'
    )
    pie_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest'
    )
    pie_fig_html = pio.to_html(pie_fig, full_html=False)

    # Create Enhanced Scatter Plot
    scatter_fig = px.scatter(
        top_states,
        x='Cure Rate (%)',
        y='Death Rate (%)',
        size='Cases',
        color='State',
        title=f'Distribution of Cure and Death Rates in Top {top_n} States',
        labels={'Cure Rate (%)': 'Cure Rate (%)', 'Death Rate (%)': 'Death Rate (%)'},
        hover_data=['Active'],
        color_continuous_scale='Viridis',
        size_max=60
    )
    scatter_fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color='DarkSlateGrey')))
    scatter_fig.update_layout(
        xaxis_title='Cure Rate (%)',
        yaxis_title='Death Rate (%)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest'
    )
    scatter_fig_html = pio.to_html(scatter_fig, full_html=False)

    return bar_fig_html, pie_fig_html, scatter_fig_html

@app.route('/')
def index():
    top_n = int(request.args.get('top_n', 10))
    top_states = df.sort_values(by='Cases', ascending=False).head(top_n)

    bar_fig_html, pie_fig_html, scatter_fig_html = create_charts(top_states, top_n)

    # Prepare data for the Apex chart
    apex_chart_data = {
        "categories": top_states['State'].tolist(),
        "cases": top_states['Cases'].tolist(),
    }

    return render_template('diabetes.html', 
                           bar_fig_html=bar_fig_html,
                           pie_fig_html=pie_fig_html,
                           scatter_fig_html=scatter_fig_html,
                           top_n=top_n,
                           apex_chart_data=json.dumps(apex_chart_data))

if __name__ == '__main__':
    app.run(debug=True)

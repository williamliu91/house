import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data
df = pd.read_csv('SydneyHousePrices.csv')

# Convert 'Date' to datetime format and extract 'Year'
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

# Create lists of unique suburbs and property types for dropdown menus
suburbs = df['suburb'].unique()
prop_types = df['propType'].unique()

# Streamlit app layout
st.title('Sydney House Prices Dashboard')

# Dropdown for selecting a suburb
selected_suburb = st.selectbox(
    'Select a suburb:',
    options=suburbs
)

# Dropdown for selecting a property type
selected_prop_type = st.selectbox(
    'Select a property type:',
    options=prop_types
)

# Filter the data based on the selected suburb and property type
filtered_df = df[(df['suburb'] == selected_suburb) & (df['propType'] == selected_prop_type)]

# Dropdown for selecting chart type
chart_type = st.selectbox(
    'Select chart type:',
    options=[
        'Median Sell Price by Year',
        'Average Bed Count by Year',
        'Average Bath Count by Year',
        'Average Car Count by Year',
        'Total Number of Properties by Year',
        'Box Plot of Sell Prices by Year',
        'Histogram of Sell Prices',
        'Scatter Plot: Sell Price vs. Bed Count',
        'Heatmap of Correlations'
    ]
)

# Create charts based on the selected chart type
if chart_type == 'Median Sell Price by Year':
    # Aggregate data: calculate median price by year
    agg_df = filtered_df.groupby(['Year'])['sellPrice'].median().reset_index()

    # Create Plotly Line Chart
    fig = px.line(agg_df, x='Year', y='sellPrice', markers=True,
                  title=f'Median House Prices in {selected_suburb} ({selected_prop_type}) by Year',
                  labels={'Year': 'Year', 'sellPrice': 'Median Sell Price'})

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Median Sell Price',
        template='plotly_white'
    )

elif chart_type == 'Average Bed Count by Year':
    # Aggregate data: calculate average bed count by year
    agg_df = filtered_df.groupby(['Year'])['bed'].mean().reset_index()

    # Create Plotly Line Chart
    fig = px.line(agg_df, x='Year', y='bed', markers=True,
                  title=f'Average Bed Count in {selected_suburb} ({selected_prop_type}) by Year',
                  labels={'Year': 'Year', 'bed': 'Average Bed Count'})

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Average Bed Count',
        template='plotly_white'
    )

elif chart_type == 'Average Bath Count by Year':
    # Aggregate data: calculate average bath count by year
    agg_df = filtered_df.groupby(['Year'])['bath'].mean().reset_index()

    # Create Plotly Line Chart
    fig = px.line(agg_df, x='Year', y='bath', markers=True,
                  title=f'Average Bath Count in {selected_suburb} ({selected_prop_type}) by Year',
                  labels={'Year': 'Year', 'bath': 'Average Bath Count'})

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Average Bath Count',
        template='plotly_white'
    )

elif chart_type == 'Average Car Count by Year':
    # Aggregate data: calculate average car count by year
    agg_df = filtered_df.groupby(['Year'])['car'].mean().reset_index()

    # Create Plotly Line Chart
    fig = px.line(agg_df, x='Year', y='car', markers=True,
                  title=f'Average Car Count in {selected_suburb} ({selected_prop_type}) by Year',
                  labels={'Year': 'Year', 'car': 'Average Car Count'})

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Average Car Count',
        template='plotly_white'
    )

elif chart_type == 'Total Number of Properties by Year':
    # Aggregate data: count total number of properties by year
    agg_df = filtered_df.groupby(['Year'])['Id'].count().reset_index()

    # Create Plotly Bar Chart
    fig = px.bar(agg_df, x='Year', y='Id',
                 title=f'Total Number of Properties in {selected_suburb} ({selected_prop_type}) by Year',
                 labels={'Year': 'Year', 'Id': 'Total Number of Properties'})

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Total Number of Properties',
        template='plotly_white'
    )

elif chart_type == 'Box Plot of Sell Prices by Year':
    # Create a Box Plot for sell prices by year
    fig = px.box(filtered_df, x='Year', y='sellPrice',
                 title=f'Box Plot of Sell Prices in {selected_suburb} ({selected_prop_type}) by Year',
                 labels={'Year': 'Year', 'sellPrice': 'Sell Price'})

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Sell Price',
        template='plotly_white'
    )

elif chart_type == 'Histogram of Sell Prices':
    # Create a Histogram of sell prices
    fig = px.histogram(filtered_df, x='sellPrice',
                       title=f'Histogram of Sell Prices in {selected_suburb} ({selected_prop_type})',
                       labels={'sellPrice': 'Sell Price'})

    fig.update_layout(
        xaxis_title='Sell Price',
        yaxis_title='Count',
        template='plotly_white'
    )

elif chart_type == 'Scatter Plot: Sell Price vs. Bed Count':
    # Create a Scatter Plot of sell price vs. bed count
    fig = px.scatter(filtered_df, x='bed', y='sellPrice',
                     title=f'Scatter Plot of Sell Price vs. Bed Count in {selected_suburb} ({selected_prop_type})',
                     labels={'bed': 'Bed Count', 'sellPrice': 'Sell Price'})

    fig.update_layout(
        xaxis_title='Bed Count',
        yaxis_title='Sell Price',
        template='plotly_white'
    )

elif chart_type == 'Heatmap of Correlations':
    # Compute correlations
    corr = filtered_df[['sellPrice', 'bed', 'bath', 'car']].corr()

    # Create a Heatmap of correlations
    fig = px.imshow(corr, text_auto=True,
                    title=f'Heatmap of Correlations in {selected_suburb} ({selected_prop_type})',
                    labels={'color': 'Correlation'})

    fig.update_layout(
        xaxis_title='Features',
        yaxis_title='Features',
        template='plotly_white'
    )

# Display the chart
st.plotly_chart(fig)

# Display detailed data table
st.subheader('Detailed Property Data')
detailed_df = filtered_df[['postalCode', 'sellPrice', 'bed', 'bath', 'car', 'propType']]
st.dataframe(detailed_df)

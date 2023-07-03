import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyaxis import pyaxis
import base64
import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

# Set the page width
st.set_page_config(layout="wide")

custom_color_sequence = [
    '#80bbad', '#435254', '#17e88f', '#dbd99a', '#5ab689', '#368c7a', '#93b886', '#779778', '#1ad3aa', '#c4c085',
    '#a6b481', '#15634d', '#00aa85', '#007754', '#abd4c8', '#d4c997', '#bebf7a', '#e2c48e', '#9db784', '#82a793',
    '#6c9b89', '#4392a3', '#0d808e', '#2b9f83', '#17e8b2', '#c4d6a5', '#a3b082', '#7b8765', '#5ab689', '#368c7a',
    '#1ad3aa', '#c4c085', '#a6b481', '#779778', '#15634d', '#00aa85', '#007754', '#abd4c8', '#d4c997', '#bebf7a',
    '#e2c48e', '#9db784', '#82a793', '#6c9b89', '#4392a3', '#0d808e', '#2b9f83', '#17e8b2', '#c4d6a5', '#a3b082',
    '#7b8765', '#5ab689', '#368c7a', '#1ad3aa', '#c4c085', '#a6b481', '#779778', '#15634d', '#00aa85', '#007754',
    '#abd4c8', '#d4c997', '#bebf7a', '#e2c48e', '#80bbad', '#435254', '#17e88f', '#dbd99a', '#5ab689', '#368c7a',
    '#93b886', '#779778', '#1ad3aa', '#c4c085', '#a6b481', '#15634d', '#00aa85', '#007754', '#abd4c8', '#d4c997',
    '#bebf7a', '#e2c48e', '#9db784', '#82a793', '#6c9b89', '#4392a3', '#0d808e', '#2b9f83', '#17e8b2', '#c4d6a5',
    '#a3b082', '#7b8765', '#5ab689', '#368c7a', '#1ad3aa', '#c4c085', '#a6b481', '#779778', '#15634d', '#00aa85',
    '#007754', '#abd4c8', '#d4c997', '#bebf7a', '#e2c48e', '#9db784', '#82a793', '#6c9b89', '#4392a3', '#0d808e',
    '#2b9f83', '#17e8b2', '#c4d6a5', '#a3b082', '#7b8765', '#5ab689', '#368c7a', '#1ad3aa', '#c4c085', '#a6b481',
    '#779778', '#15634d', '#00aa85', '#007754', '#abd4c8', '#d4c997', '#bebf7a', '#e2c48e', '#9db784', '#82a793',
    '#6c9b89', '#4392a3', '#0d808e', '#2b9f83', '#17e8b2', '#c4d6a5', '#a3b082', '#7b8765', '#5ab689', '#368c7a',
    '#1ad3aa'
]

# Store data as a pandas dataframe
@st.cache_data
def load_data():
    # Current date
    current_date = datetime.date.today()
    # Calculate the cutoff date (last day of the month before the previous month)
    cutoff_date = datetime.date(current_date.year, current_date.month, 1) - relativedelta(months=2) - datetime.timedelta(days=1)

    # Herkunftsland
    url = "https://dam-api.bfs.admin.ch/hub/api/dam/assets/25805370/master"
    px_data = pyaxis.parse(uri=url, encoding='ISO-8859-2')
    df_country = px_data['DATA']

    # Filter rows
    df_country = df_country[(df_country["Monat"] != "Jahrestotal") & (df_country["Herkunftsland"] != "Herkunftsland - Total")]

    # Pivot the dataframe
    df_country = df_country.pivot(index=["Jahr", "Monat", "Gemeinde", "Herkunftsland"], columns="Indikator", values="DATA").reset_index()

    # Angebot und Nachfrage
    url = "https://dam-api.bfs.admin.ch/hub/api/dam/assets/25805379/master"
    px_data = pyaxis.parse(uri=url, encoding='ISO-8859-2')
    df_supply = px_data['DATA']

    # Filter rows
    df_supply = df_supply[df_supply["Monat"] != "Jahrestotal"]

    # Pivot the dataframe
    df_supply = df_supply.pivot(index=["Jahr", "Monat", "Gemeinde"], columns="Indikator", values="DATA").reset_index()

    # Dictionary mapping German month names to numeric month numbers
    month_mapping = {
        'Januar': 1, 'Februar': 2, 'März': 3, 'April': 4, 'Mai': 5, 'Juni': 6,
        'Juli': 7, 'August': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Dezember': 12
    }

    # Function to convert 'Jahr' and 'Monat' columns to a datetime object
    def convert_to_datetime(df):
        df['Date'] = pd.to_datetime(df['Jahr'].astype(str) + '-' + df['Monat'].map(month_mapping).astype(str))
        df['Date'] = df['Date'].dt.date  # Extract only the date part
        df = df[['Date'] + df.columns[:-1].tolist()]  # Set 'Date' column as the first column
        df = df.sort_values('Date').reset_index(drop=True)
        return df

    # Convert columns to the correct formats and calculate new columns
    df_country = convert_to_datetime(df_country)
    df_country["Logiernächte"] = pd.to_numeric(df_country["Logiernächte"], errors='coerce')
    df_country["Ankünfte"] = pd.to_numeric(df_country["Ankünfte"], errors='coerce')
    df_country["Aufenthaltsdauer"] = df_country["Logiernächte"] / df_country["Ankünfte"]

    df_supply = convert_to_datetime(df_supply)
    df_supply["Ankünfte"] = pd.to_numeric(df_supply["Ankünfte"], errors='coerce')
    df_supply["Betriebe"] = pd.to_numeric(df_supply["Betriebe"], errors='coerce')
    df_supply["Betten"] = pd.to_numeric(df_supply["Betten"], errors='coerce')
    df_supply["Bettenauslastung in %"] = pd.to_numeric(df_supply["Bettenauslastung in %"], errors='coerce')
    df_supply["Logiernächte"] = pd.to_numeric(df_supply["Logiernächte"], errors='coerce')
    df_supply["Zimmer"] = pd.to_numeric(df_supply["Zimmer"], errors='coerce')
    df_supply["Zimmerauslastung in %"] = pd.to_numeric(df_supply["Zimmerauslastung in %"], errors='coerce')
    df_supply["Zimmernächte"] = pd.to_numeric(df_supply["Zimmernächte"], errors='coerce')

    # Filter based on current date
    df_supply = df_supply[df_supply['Date'] <= cutoff_date]
    # Filter based on current date
    df_country = df_country[df_country['Date'] <= cutoff_date ]

    return df_country, df_supply

df_country,df_supply = load_data()



def create_main_page(df,df_2):
    # Sidebar for selecting specific Gemeinde
    selected_Gemeinde = st.sidebar.selectbox('Gemeinde', df['Gemeinde'].unique(), index=0)

    # Filter dataframe based on selected Gemeinde
    filtered_df = df[df['Gemeinde'] == selected_Gemeinde]
    filtered_df_2 = df_2[df_2['Gemeinde'] == selected_Gemeinde]

    current_date = datetime.date.today()
    # Calculate the cutoff date (last day of the month before the previous month)
    cutoff_date = datetime.date(current_date.year, current_date.month, 1) - relativedelta(months=2) - datetime.timedelta(days=1)


    # Define the date range for the slider
    start_date = datetime.date(2013, 1, 1)
    end_date = cutoff_date
    first_day_actual_month = cutoff_date.replace(day=1) 

    # Move the code to the Streamlit sidebar
    st.sidebar.subheader("Date Range")

    # Create the date slider widget
    selected_dates = st.sidebar.date_input("Select Dates", [start_date, end_date])
    # Convert the selected dates to datetime.date objects
    start_date = selected_dates[0]
    end_date = selected_dates[1]
    # Filter df2 based on selection
    filtered_df_2 = filtered_df_2 [(filtered_df_2['Date'] >= start_date) & (df['Date'] <= end_date)]



    # Metrics Avererges whole time
    # Format the metrics with thousand separators and no decimal places
    average_zimmerauslastung_per_month_formatted = "{:,.0f}%".format(filtered_df_2['Zimmerauslastung in %'].mean())
    average_bettenauslastung_per_month_formatted = "{:,.0f}%".format(filtered_df_2['Bettenauslastung in %'].mean())
    average_logiernächte_per_month_formatted_2 = "{:,.0f}".format(filtered_df_2['Logiernächte'].mean())
    average_betten_per_month_formatted = "{:,.0f}".format(filtered_df_2['Betten'].mean())
    average_betriebe_per_month_formatted = "{:,.0f}".format(filtered_df_2['Betriebe'].mean())
    average_ankünfte_per_month_formatted = "{:,.0f}".format(filtered_df_2['Ankünfte'].mean())

    st.subheader(f"Monatliche Durchschnittswerte für {selected_Gemeinde}")

    earliest_year = filtered_df_2["Jahr"].min()
    most_recent_year = filtered_df_2["Jahr"].max()
    
    st.caption(f"Betrachtungszeitraum {earliest_year} - {most_recent_year}")
    # Create two columns for metrics and line chart
    col1, col2, col3 = st.columns(3)

    # Display the metrics dynamically based on the selected plot type
    col2.metric(f"Betriebe",average_betriebe_per_month_formatted)
    col1.metric(f"Logiernächte",average_logiernächte_per_month_formatted_2)
    col3.metric(f"Bettenauslastung", average_bettenauslastung_per_month_formatted)

    # Create two columns for metrics and line chart
    col1, col2, col3 = st.columns(3)

    col3.metric(f"Zimmerauslastung", average_zimmerauslastung_per_month_formatted)
    col2.metric(f"Betten",average_betten_per_month_formatted)
    col1.metric(f"Ankünfte",average_ankünfte_per_month_formatted)

    # Create two columns
    col1, col2 = st.columns([4, 1])

    # Select box in the second column
    # Add CSS styling to vertically center the select box
    selected_indicator_1 = col2.selectbox('Indikator', ["Logiernächte", "Ankünfte", "Betten","Zimmer","Betriebe",'Zimmerauslastung in %','Bettenauslastung in %',"Zimmernächte"], index=0)

    # Line chart using Plotly in the first column
    fig_line = px.line(filtered_df_2,
                    x='Date',
                    y=selected_indicator_1,
                    title=f"{selected_Gemeinde} pro Monat",
                    color_discrete_sequence=['#0e4130'])
    # calculate indikator mean
    avg = filtered_df_2[selected_indicator_1].mean()


    # Add trace for the average line
    fig_line.add_hline(y=avg, line_dash="dot", line_color='#0e4130', annotation_text=f"Average: {avg:,.0f}")
    
    fig_line.update_layout(
        xaxis_title=''  # Hide the title of the x-axis
    )

    col1.plotly_chart(fig_line, use_container_width=True, auto_open=False)

    # Metrics Avererges last Month
    filtered_df_2_current_month = filtered_df_2[filtered_df_2["Date"] == first_day_actual_month]

    # Format the metrics with thousand separators and no decimal places
    average_zimmerauslastung_current_month_formatted = "{:,.0f}%".format(filtered_df_2_current_month['Zimmerauslastung in %'].mean())
    average_bettenauslastung_current_month_formatted = "{:,.0f}%".format(filtered_df_2_current_month['Bettenauslastung in %'].mean())
    average_logiernächte_current_month_formatted_2 = "{:,.0f}".format(filtered_df_2_current_month['Logiernächte'].mean())
    average_betten_current_month_formatted = "{:,.0f}".format(filtered_df_2_current_month['Betten'].mean())
    average_betriebe_current_month_formatted = "{:,.0f}".format(filtered_df_2_current_month['Betriebe'].mean())
    average_ankünfte_current_month_formatted = "{:,.0f}".format(filtered_df_2_current_month['Ankünfte'].mean())

    st.subheader(f"Aktuelle Durchschnittswerte für {selected_Gemeinde} im {str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}")
    # Create two columns for metrics and line chart
    col1, col2, col3 = st.columns(3)

    # Display the metrics dynamically based on the selected plot type
    col2.metric(f"Betriebe",average_betriebe_current_month_formatted)
    col1.metric(f"Logiernächte",average_logiernächte_current_month_formatted_2)
    col3.metric(f"Bettenauslastung", average_bettenauslastung_current_month_formatted)

    # Create two columns for metrics and line chart
    col1, col2, col3 = st.columns(3)

    col3.metric(f"Zimmerauslastung", average_zimmerauslastung_current_month_formatted)
    col2.metric(f"Betten",average_betten_current_month_formatted)
    col1.metric(f"Ankünfte",average_ankünfte_current_month_formatted)


    # Create two columns
    col1, col3 = st.columns([4, 1])
     # Add CSS styling to vertically center the select box
    selected_indicator_2 = col3.selectbox('Indikator', ["Logiernächte", "Ankünfte", "Betten","Zimmer","Betriebe",'Zimmerauslastung in %','Bettenauslastung in %',"Zimmernächte"], index=0,key="selected_indicator_2")

    # Line chart using Plotly in the first column
    fig_line = px.line(filtered_df_2,
                    x='Monat',
                    color='Jahr',
                    y=selected_indicator_2,
                    title=f"{selected_Gemeinde} pro Monat",
                    color_discrete_sequence=custom_color_sequence)
    # calculate indikator mean
    avg = filtered_df_2[selected_indicator_2].mean()


    # Add trace for the average line
    fig_line.add_hline(y=avg, line_dash="dot", line_color='#0e4130', annotation_text=f"Average: {avg:,.0f}")
    
    fig_line.update_layout(
        xaxis_title='',  # Hide the title of the x-axis
        legend_traceorder="reversed"  # Sort the legend in descending order
    )

    col1.plotly_chart(fig_line, use_container_width=True, auto_open=False)






    # Add a multi-select sidebar for selecting Herkunftsländer
    all_herkunftsländer = df['Herkunftsland'].unique()
    herkunftsländer_options = ['Alle Herkunftsländer'] + all_herkunftsländer.tolist()
    selected_herkunftsländer = st.sidebar.multiselect('Herkunftsländer', herkunftsländer_options,
                                                    default=['Alle Herkunftsländer'])

    # Check if "Alle Herkunftsländer" option is chosen
    if 'Alle Herkunftsländer' in selected_herkunftsländer:
        selected_herkunftsländer = all_herkunftsländer


    # Filter dataframe based on selected Herkunftsländer and date range
    filtered_df = filtered_df[(filtered_df['Herkunftsland'].isin(selected_herkunftsländer))]
    # Filter DataFrame based on selected date range
    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Add a radio button to switch between Logiernächte and Ankünfte
    plot_type = st.sidebar.radio("Kennzahl", ("Logiernächte", "Ankünfte"))

    # Determine the column for the y-axis based on the selected plot type
    if plot_type == 'Logiernächte':
        y_column = 'Logiernächte'
    elif plot_type == 'Ankünfte':
        y_column = 'Ankünfte'
    
    
    
    # Calculate totals
    totals = filtered_df.groupby('Date')[y_column].sum().reset_index()


     # Create two columns for metrics and line chart
    col1, col2,col3 = st.columns([2,0.2,1])
    # Perform grouping and aggregation
    grouped_df = filtered_df.groupby('Herkunftsland').mean().reset_index()

    # Sort the unique values based on aggregated values in descending order
    sorted_values = grouped_df.sort_values(y_column, ascending=False)['Herkunftsland'].tolist()

    # Create a new column to group Herkunftsländer
    grouped_df['Herkunftsland_grouped'] = grouped_df['Herkunftsland'].apply(lambda x: x if x in sorted_values[:15] else 'Others')

    # Group by the new column and mean the values
    grouped_df = grouped_df.groupby('Herkunftsland_grouped').mean().reset_index()

    fig_bar = px.bar(
        grouped_df,
        x='Herkunftsland_grouped',
        y=y_column,
        color='Herkunftsland_grouped',
        title="Durchschnittliche " + plot_type + " pro Monat nach Herkunftsland",
        color_discrete_sequence=custom_color_sequence,
        category_orders={'Herkunftsland_grouped': sorted_values[:15] + ['Others']}  # Set custom category order
    )

    fig_bar.update_traces(hovertemplate='%{y}')
    fig_bar.update_layout(
        legend_title='Herkunftsland',
        xaxis_title='',  # Hide the title of the x-axis
        showlegend=False  # Remove the legend
    )

    # Donut Chart
    fig_donut = px.pie(
        grouped_df,
        names='Herkunftsland_grouped',
        values=y_column,
        hole=0.5,
        color_discrete_sequence=custom_color_sequence,
        category_orders={'Herkunftsland_grouped': sorted_values[:15] + ['Others']}  # Set custom category order
    )

    fig_donut.update_traces(textposition='inside', textinfo='percent')
    fig_donut.update_layout(
        legend_title='Herkunftsland'
    )

    col1.plotly_chart(fig_bar, use_container_width=True, auto_open=False)
    col3.plotly_chart(fig_donut, use_container_width=True, auto_open=False)

    # Display selected data as a table
    st.write("")
    st.dataframe(filtered_df.reset_index(drop=True))

    # Download CSV
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv'
    )



create_main_page(df_country,df_supply)

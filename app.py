import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyaxis import pyaxis
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

def create_main_page(df):
    # Sidebar for selecting specific Gemeinde
    selected_Gemeinde = st.sidebar.selectbox('Auswahl Gemeinde', df['Gemeinde'].unique(), index=0)

    # Filter dataframe based on selected Gemeinde
    filtered_df_2 = df[df['Gemeinde'] == selected_Gemeinde]

    current_date = datetime.date.today()
    # Calculate the cutoff date (last day of the month before the previous month)
    cutoff_date = datetime.date(current_date.year, current_date.month, 1) - relativedelta(months=2) - datetime.timedelta(days=1)


    # Define the date range for the slider
    start_date = datetime.date(2018, 1, 1)
    end_date = cutoff_date
    first_day_actual_month = cutoff_date.replace(day=1)


    # Create the date slider widget
    selected_dates = st.sidebar.date_input("Auswahl Zeithorizont", [start_date, end_date])
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
    st.title(":flag-ch: Hotellerie Explorer")
    st.header(f"Kennzahlen nach Gemeinde: {selected_Gemeinde}")
    #st.subheader(f"Markt und Gesamtentwicklung")

    earliest_year = filtered_df_2["Jahr"].min()
    most_recent_year = filtered_df_2["Jahr"].max()

    #################### Aktuelle KPIS #######################

    # Metrics Avererges last Month
    filtered_df_2_current_month = filtered_df_2[filtered_df_2["Date"] == first_day_actual_month]
    filtered_df_2_current_month_last_year = filtered_df_2[filtered_df_2["Date"] == first_day_actual_month - datetime.timedelta(days=365)]

    def calculate_percentage_change(current_value, previous_value):
        percentage_change = ((current_value - previous_value) / previous_value) * 100
        return round(percentage_change, 1)
    
    # Format the metrics with thousand separators and no decimal places
    average_zimmerauslastung_current_month = filtered_df_2_current_month['Zimmerauslastung in %'].mean()
    average_zimmerauslastung_current_month_formatted = "{:,.0f}%".format(average_zimmerauslastung_current_month)
    average_zimmerauslastung_current_month_last_year = filtered_df_2_current_month_last_year['Zimmerauslastung in %'].mean()
    average_zimmerauslastung_current_month_change = "{:,.0f}".format(average_zimmerauslastung_current_month - average_zimmerauslastung_current_month_last_year)

    average_bettenauslastung_current_month = filtered_df_2_current_month['Bettenauslastung in %'].mean()
    average_bettenauslastung_current_month_formatted = "{:,.0f}%".format(average_bettenauslastung_current_month)
    average_bettenauslastung_current_month_last_year = filtered_df_2_current_month_last_year['Bettenauslastung in %'].mean()
    average_bettenauslastung_current_month_change = "{:,.0f}".format(average_bettenauslastung_current_month - average_bettenauslastung_current_month_last_year)


    average_logiernächte_current_month = filtered_df_2_current_month['Logiernächte'].mean()
    average_logiernächte_current_month_formatted = "{:,.0f}".format(average_logiernächte_current_month)
    average_logiernächte_current_month_last_year = filtered_df_2_current_month_last_year['Logiernächte'].mean()
    average_logiernächte_current_month_change = "{:,.1f}".format(calculate_percentage_change(average_logiernächte_current_month, average_logiernächte_current_month_last_year ))

    average_ankünfte_current_month = filtered_df_2_current_month['Ankünfte'].mean()
    average_ankünfte_current_month_formatted = "{:,.0f}".format(average_ankünfte_current_month)
    average_ankünfte_current_month_last_year = filtered_df_2_current_month_last_year['Ankünfte'].mean()
    average_ankünfte_current_month_change = "{:,.1f}".format(calculate_percentage_change(average_ankünfte_current_month, average_ankünfte_current_month_last_year ))

    average_betten_current_month = filtered_df_2_current_month['Betten'].mean()
    average_betten_current_month_formatted = "{:,.0f}".format(average_betten_current_month)
    average_betten_current_month_last_year = filtered_df_2_current_month_last_year['Betten'].mean()
    average_betten_current_month_change = "{:,.0f}".format(average_betten_current_month - average_betten_current_month_last_year)

    average_betriebe_current_month = filtered_df_2_current_month['Betriebe'].mean()
    average_betriebe_current_month_formatted = "{:,.0f}".format(average_betriebe_current_month)
    average_betriebe_current_month_last_year = filtered_df_2_current_month_last_year['Betriebe'].mean()
    average_betriebe_current_month_change = "{:,.0f}".format(average_betriebe_current_month - average_betriebe_current_month_last_year)
    
    #css_example = '''
    #I'm importing the font-awesome icons as a stylesheet!                                                                                                                                                       
    #<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
                                                                                                                                                                                                                
    #<i class="fa-solid fa-bed"></i>'''

    #st.write(css_example, unsafe_allow_html=True)

    # Create two columns for metrics and line chart
    col1, col2, col3, col4, col5, col6 ,col7, col8 = st.columns(8)

    # Display the metrics dynamically based on the selected plot type
    col1.metric(f"Logiernächte ⌀ ",average_logiernächte_per_month_formatted_2)
    col2.metric(f"{str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}",
                average_logiernächte_current_month_formatted,
                delta=f"{average_logiernächte_current_month_change}%")
    col4.metric(f"Betriebe ⌀ ",average_betriebe_per_month_formatted)
    col5.metric(f" {str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}",
                average_betriebe_current_month_formatted,
                delta=f"{average_betriebe_current_month_change}")
    col7.metric(f"Bettenauslastung ⌀ ", average_bettenauslastung_per_month_formatted)
    col8.metric(f"{str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}",
                average_bettenauslastung_current_month_formatted,
                delta = f"{average_bettenauslastung_current_month_change}"
                )

    # Create two columns for metrics and line chart
    col1, col2, col3, col4, col5, col6 ,col7, col8 = st.columns(8)

    col7.metric(f"Zimmerauslastung ⌀ ", average_zimmerauslastung_per_month_formatted)
    col8.metric(
        f"{str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}",
        average_zimmerauslastung_current_month_formatted,
        delta=f"{average_zimmerauslastung_current_month_change}"
        )
    col4.metric(f"Betten ⌀ ",average_betten_per_month_formatted)
    col5.metric(f"{str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}",
                average_betten_current_month_formatted,
                delta=f"{average_betten_current_month_change}")
    col1.metric(f"Ankünfte ⌀ ",average_ankünfte_per_month_formatted)
    col2.metric(f"{str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}",
                average_ankünfte_current_month_formatted,
                delta=f"{average_ankünfte_current_month_change}%"
                )

    st.info(f"Die oben aufgezeigten Kennzahlen zeigen die monatliche Durchschnittswerte im ausgewählten Zeithorizont ({earliest_year} - {most_recent_year}) sowie die aktuellesten Monatswerte ({str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}) verglichen mit dem Vorjahresmonat ({str(filtered_df_2_current_month_last_year['Monat'].iloc[0])} {str(filtered_df_2_current_month_last_year['Jahr'].iloc[0])})")

    selected_indicator = st.sidebar.selectbox('Auswahl Kennzahl', ["Logiernächte", "Ankünfte", "Betten","Zimmer","Betriebe",'Zimmerauslastung in %','Bettenauslastung in %',"Zimmernächte"], index=0)


    # Line chart using Plotly in the first column
    fig_line = px.line(filtered_df_2,
                    x='Date',
                    y=selected_indicator,
                    title=f"",
                    color_discrete_sequence=['#000000'])
    # calculate indikator mean
    avg = filtered_df_2[selected_indicator].mean()


    # Add trace for the average line
    fig_line.add_hline(y=avg,
                       line_dash="dot",
                       #annotation_text=f"⌀ {selected_indicator}",
                       #annotation_position="bottom right",
                       #annotation_text_color='#0e4130'
                       )
    
    fig_line.update_layout(
        xaxis_title=''  # Hide the title of the x-axis
    )
    st.plotly_chart(fig_line, use_container_width=True, auto_open=False)
    st.caption(f"Abbildung 1: {selected_indicator} pro Monat in der Gemeinde {selected_Gemeinde} von  {earliest_year} - {most_recent_year}")


    # Line chart using Plotly in the first column
    fig_line = px.line(filtered_df_2,
                    x='Monat',
                    color='Jahr',
                    y=selected_indicator,
                    title=f"",
                    color_discrete_sequence=custom_color_sequence)
    # calculate indikator mean
    avg = filtered_df_2[selected_indicator].mean()

    
    fig_line.update_layout(
        xaxis_title='',  # Hide the title of the x-axis
        legend_traceorder="reversed"  # Sort the legend in descending order
    )

    st.plotly_chart(fig_line, use_container_width=True, auto_open=False)
    st.caption(f"Abbildung 2: {selected_indicator} pro Monat in der Gemeinde {selected_Gemeinde} im Jahresvergleich")

    # Create two columns for metrics and line chart
    col1, col2, col3, col4, col5, col6 ,col7, col8 = st.columns(8)
    col1.text("")

def create_other_page(df):
    selected_Gemeinde = st.sidebar.selectbox('Auswahl Gemeinde', df['Gemeinde'].unique(), index=0)
    # Filter dataframe based on selected Gemeinde
    filtered_df = df[df['Gemeinde'] == selected_Gemeinde]
    st.title(":flag-ch: Hotellerie Explorer")
    st.header(f"Kennzahlen nach Gemeinde und Herkunftsland: {selected_Gemeinde}")


    current_date = datetime.date.today()
    # Calculate the cutoff date (last day of the month before the previous month)
    cutoff_date = datetime.date(current_date.year, current_date.month, 1) - relativedelta(months=2) - datetime.timedelta(days=1)


    # Define the date range for the slider
    start_date = datetime.date(2018, 1, 1)
    end_date = cutoff_date


    # Create the date slider widget
    selected_dates = st.sidebar.date_input("Auswahl Zeithorizont", [start_date, end_date])
    # Convert the selected dates to datetime.date objects
    start_date = selected_dates[0]
    end_date = selected_dates[1]
    # Filter df2 based on selection
    filtered_df = filtered_df [(filtered_df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Filter DataFrame based on selected date range
    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (df['Date'] <= end_date)]

    earliest_year = filtered_df["Jahr"].min()
    most_recent_year = filtered_df["Jahr"].max()

    # Add a radio button to switch between Logiernächte and Ankünfte
    selected_indicator = st.sidebar.selectbox('Auswahl Kennzahl', ["Logiernächte", "Ankünfte"], index=0)


    # Determine the column for the y-axis based on the selected plot type
    if selected_indicator == 'Logiernächte':
        y_column = 'Logiernächte'
    elif selected_indicator == 'Ankünfte':
        y_column = 'Ankünfte'


     # Create two columns for metrics and line chart
    col1, col2,col3 = st.columns([2,0.2,1])
    # Perform grouping and aggregation
    grouped_df = filtered_df.groupby('Herkunftsland').mean().reset_index()

    # Sort the unique values based on aggregated values in descending order
    sorted_values = grouped_df.sort_values(y_column, ascending=False)['Herkunftsland'].tolist()

    # Create a new column to group Herkunftsländer
    grouped_df['Herkunftsland_grouped'] = grouped_df['Herkunftsland'].apply(lambda x: x if x in sorted_values[:15] else 'Others')

    # Group by the new column and mean the values
    #grouped_df = grouped_df.groupby('Herkunftsland_grouped').mean().reset_index()

    fig_bar = px.bar(
        grouped_df,
        x='Herkunftsland_grouped',
        y=y_column,
        color='Herkunftsland_grouped',
        title="",
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

    st.caption(f"Abbildung 3: Durchschnittliche {selected_indicator} pro Monat in der Gemeinde {selected_Gemeinde} von {earliest_year} - {most_recent_year} nach Herkunftsland")

    # Display selected data as a table
    #st.write("")
    #st.dataframe(filtered_df.reset_index(drop=True))

    # Download CSV
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv'
    )

def create_markt_page(df_country):
    st.write("Coming soon")
    st.image("")

# Sidebar navigation
page = st.sidebar.selectbox("Seitenauswahl", ("Nach Gemeinde", "Nach Gemeinde und Herkunftsland","Gesamtmarkt"))
    
if page == "Nach Gemeinde":
    create_main_page(df_supply)
elif page == "Nach Gemeinde und Herkunftsland":
    create_other_page(df_country)
elif page == "Gesamtmarkt":
    create_markt_page(df_country)
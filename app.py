import streamlit as st
import pandas as pd
import plotly.express as px
from pyaxis import pyaxis
import datetime
import numpy as np
from PIL import Image
import calendar

# Set the page width
st.set_page_config(layout="wide",page_title='Hotellerie Explorer (Beta)',page_icon= "🇨🇭")


# Store data as a pandas dataframe
@st.cache_data
def load_data():
    # Calculate the cutoff date (last day of the month before the previous month
    current_date = datetime.date.today()

    if current_date.day < 8:
        cutoff_date = datetime.date(current_date.year, current_date.month - 3, calendar.monthrange(current_date.year, current_date.month - 3)[1])
    else:
        cutoff_date = datetime.date(current_date.year, current_date.month - 2, calendar.monthrange(current_date.year, current_date.month - 2)[1])

    # Herkunftsland
    url = "https://www.pxweb.bfs.admin.ch/DownloadFile.aspx?file=px-x-1003020000_101"
    px_data = pyaxis.parse(uri=url, encoding='ISO-8859-2')
    df_country = px_data['DATA']

    # Filter rows
    df_country = df_country[(df_country["Monat"] != "Jahrestotal") & (df_country["Herkunftsland"] != "Herkunftsland - Total")]

    # Pivot the dataframe
    df_country = df_country.pivot(index=["Jahr", "Monat", "Gemeinde", "Herkunftsland"], columns="Indikator", values="DATA").reset_index()

    # Angebot und Nachfrage
    url = "https://www.pxweb.bfs.admin.ch/DownloadFile.aspx?file=px-x-1003020000_201"
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
    df_country["Herkunftsland_grob"] = df_country["Herkunftsland"].apply(lambda x: "Domestic" if x == "Schweiz" else "International")

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

    df_country['Jahr'] = df_country['Jahr'].astype(int)
    df_supply ['Jahr'] = df_supply ['Jahr'].astype(int)

    return df_country, df_supply

df_country,df_supply = load_data()


def create_main_page(df,selected_Gemeinde):

    # Sidebar for selecting specific Gemeinde
    #selected_Gemeinde = st.sidebar.selectbox('Auswahl Gemeinde', df['Gemeinde'].unique(), index=0)

    st.title(f":flag-ch: Kennzahlen nach Gemeinde")
    st.divider()
    #st.caption(f"Gemeinde: {selected_Gemeinde}")

    # Filter dataframe based on selected Gemeinde
    filtered_df_2 = df[df['Gemeinde'] == selected_Gemeinde]

    ##########
    ##########
    ##########

    # Metrics Avererges whole time
    # Format the metrics with thousand separators and no decimal places
    average_zimmerauslastung_per_month_formatted = "{:,.0f}%".format(filtered_df_2['Zimmerauslastung in %'].mean())
    average_zimmer_per_month_formatted = "{:,.0f}".format(filtered_df_2['Zimmer'].mean())
    sum_logiernächte_per_month_formatted_2 = "{:,.0f}".format(filtered_df_2['Logiernächte'].sum())
    average_zimmernaechte_per_month_formatted = "{:,.0f}".format(filtered_df_2['Zimmernächte'].mean())
    average_betriebe_per_month_formatted = "{:,.0f}".format(filtered_df_2['Betriebe'].mean())
    sum_ankünfte_per_month_formatted = "{:,.0f}".format(filtered_df_2['Ankünfte'].sum())

    earliest_year = filtered_df_2["Jahr"].min()
    most_recent_year = filtered_df_2["Jahr"].max()

    #################### Aktuelle KPIS #######################

    # Dataframes last avaiable Month and same month last year
    filtered_df_2_current_month = filtered_df_2[filtered_df_2["Date"] == first_day_actual_month]
    filtered_df_2_current_month_last_year = filtered_df_2[filtered_df_2["Date"] == first_day_actual_month - datetime.timedelta(days=365)]


    ### Ytd current year and Last year ####
    # Calculate the start and end dates for the YTD period
    current_year = first_day_actual_month.year
    current_month = first_day_actual_month.month
    start_date_ytd = datetime.date(current_year, 1, 1)

    # Format the start and end dates as strings
    start_date_str = start_date_ytd.strftime("%B")
    end_date_str = end_date.strftime("%B %Y")
    # Create the YTD period string
    ytd_period_str = f"{start_date_str} - {end_date_str}" # needed for KPIs


    # Filter the DataFrame for the YTD period of the current year
    filtered_df_2_ytd_current_year = filtered_df_2[
        (filtered_df_2["Date"] >= start_date_ytd) & (filtered_df_2["Date"] <= end_date)
    ]

    # Calculate the start and end dates for the YTD period of the previous year
    previous_year = current_year - 1
    start_date_last_year = datetime.date(previous_year, 1, 1)
    end_date_last_year = datetime.date(previous_year, current_month, 1)

    # Filter the DataFrame for the YTD period of the previous year
    filtered_df_2_ytd_last_year = filtered_df_2[
        (filtered_df_2["Date"] >= start_date_last_year) & (filtered_df_2["Date"] <= end_date_last_year)
    ]

    ########

    def calculate_percentage_change(current_value, previous_value):
        percentage_change = ((current_value - previous_value) / previous_value) * 100
        return round(percentage_change, 1)
    
    # Format the metrics with thousand separators and no decimal places
    average_zimmerauslastung_current_month = filtered_df_2_current_month['Zimmerauslastung in %'].mean()
    average_zimmerauslastung_current_month_formatted = "{:,.0f}%".format(average_zimmerauslastung_current_month)
    average_zimmerauslastung_current_month_last_year = filtered_df_2_current_month_last_year['Zimmerauslastung in %'].mean()
    average_zimmerauslastung_current_month_change = "{:,.0f}".format(average_zimmerauslastung_current_month - average_zimmerauslastung_current_month_last_year)

    average_zimmer_current_month = filtered_df_2_current_month['Zimmer'].mean()
    average_zimmer_current_month_formatted = "{:,.0f}".format(average_zimmer_current_month)
    average_zimmer_current_month_last_year = filtered_df_2_current_month_last_year['Zimmer'].mean()
    average_zimmer_current_month_change = "{:,.0f}".format(average_zimmer_current_month - average_zimmer_current_month_last_year)


    average_logiernächte_current_month = filtered_df_2_current_month['Logiernächte'].mean()
    average_logiernächte_current_month_formatted = "{:,.0f}".format(average_logiernächte_current_month)
    average_logiernächte_current_month_last_year = filtered_df_2_current_month_last_year['Logiernächte'].mean()
    average_logiernächte_current_month_change = "{:,.1f}".format(calculate_percentage_change(average_logiernächte_current_month, average_logiernächte_current_month_last_year ))

    total_logiernächte_ytd = filtered_df_2_ytd_current_year['Logiernächte'].sum()
    total_logiernächte_ytd_formatted = "{:,.0f}".format(total_logiernächte_ytd)
    total_logiernächte_currenächte_ytd_last_year = filtered_df_2_ytd_last_year['Logiernächte'].sum()
    total_logiernächte_ytd_change = "{:,.1f}".format(calculate_percentage_change(total_logiernächte_ytd,total_logiernächte_currenächte_ytd_last_year))

    average_ankünfte_current_month = filtered_df_2_current_month['Ankünfte'].mean()
    average_ankünfte_current_month_formatted = "{:,.0f}".format(average_ankünfte_current_month)
    average_ankünfte_current_month_last_year = filtered_df_2_current_month_last_year['Ankünfte'].mean()
    average_ankünfte_current_month_change = "{:,.1f}".format(calculate_percentage_change(average_ankünfte_current_month, average_ankünfte_current_month_last_year ))

    total_ankünfte_ytd = filtered_df_2_ytd_current_year['Ankünfte'].sum()
    total_ankünfte_ytd_formatted = "{:,.0f}".format(total_ankünfte_ytd)
    total_ankünfte_currenächte_ytd_last_year = filtered_df_2_ytd_last_year['Ankünfte'].sum()
    total_ankünfte_ytd_change = "{:,.1f}".format(calculate_percentage_change(total_ankünfte_ytd,total_ankünfte_currenächte_ytd_last_year))

    average_zimmernaechte_current_month = filtered_df_2_current_month['Zimmernächte'].mean()
    average_zimmernaechte_current_month_formatted = "{:,.0f}".format(average_zimmernaechte_current_month)
    average_zimmernaechte_current_month_last_year = filtered_df_2_current_month_last_year['Zimmernächte'].mean()
    average_zimmernaechte_current_month_change = "{:,.0f}".format(average_zimmernaechte_current_month - average_zimmernaechte_current_month_last_year)

    average_betriebe_current_month = filtered_df_2_current_month['Betriebe'].mean()
    average_betriebe_current_month_formatted = "{:,.0f}".format(average_betriebe_current_month)
    average_betriebe_current_month_last_year = filtered_df_2_current_month_last_year['Betriebe'].mean()
    average_betriebe_current_month_change = "{:,.0f}".format(average_betriebe_current_month - average_betriebe_current_month_last_year)
    
    st.markdown('#')

    # Create two columns for metrics and line chart
    st.header("Logiernächte & Ankünfte",
              help="Logiernächte: Die Gesamtanzahl der Übernachtungen.\n\nAnkünfte: Die Gesamtanzahl der Gäste, die angekommen sind.",
              )
    
    col1, col2, col3 = st.columns(3)

    col1.metric(f"Logiernächte (Total)",
                sum_logiernächte_per_month_formatted_2,
                help=f"Summierte Logiernächte im gesamten Zeitraum ({start_year} - {end_year})"
                )
    
    col2.metric(f"{str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}",
                average_logiernächte_current_month_formatted,
                help=f"Monatliche Logiernächte für {str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}. Delta zeigt den Prozentualen Unterschied verglichen zur gleichen Monat im Vorjahr.",
                delta=f"{average_logiernächte_current_month_change}%")
    
    col3.metric(ytd_period_str,
                total_logiernächte_ytd_formatted,
                help=f"Summierte Logiernächte im Zeitraum {ytd_period_str}. Delta zeigt den Prozentualen Unterschied verglichen zur gleichen Periode im Vorjahr.",
                delta=f"{ total_logiernächte_ytd_change}%"
                )
    
    col1, col2, col3 = st.columns(3)

    col1.metric(f"Ankünfte (Total)",
                sum_ankünfte_per_month_formatted,
                help=f"Summierte Ankünfte im gesamten Zeitraum ({start_year} - {end_year})")
    col2.metric(f"{str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}",
                average_ankünfte_current_month_formatted,
                help=f"Monatliche Ankünfte für {str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}. Delta zeigt den Prozentualen Unterschied verglichen zur gleichen Monat im Vorjahr.",
                delta=f"{average_ankünfte_current_month_change}%"
                )
    col3.metric(ytd_period_str,
                total_ankünfte_ytd_formatted,
                help=f"Summierte Ankünfte im Zeitraum {ytd_period_str}. Delta zeigt den Prozentualen Unterschied verglichen zur gleichen Periode im Vorjahr.",
                delta=f"{ total_ankünfte_ytd_change}%")
    
    st.subheader("Gesamtentwicklung")
    

    # Remove the selection and show both "Logiernächte" and "Ankünfte" in the chart
    selected_indicator_1 = "Logiernächte"  # Set the selected indicator to "Logiernächte"
    selected_indicator_2 = "Ankünfte"  # Set the second indicator to "Ankünfte"

    # Line chart using Plotly in the first column
    fig_line = px.line(filtered_df_2,
                    x='Date',
                    y=[selected_indicator_1, selected_indicator_2],  # Pass both indicators as a list
                    title="",
                    color_discrete_sequence=custom_color_sequence)  # Add colors for each indicator

    fig_line.update_layout(
        xaxis_title='',  # Hide the title of the x-axis
        yaxis_title='',
        legend_title_text=''  # Hide the title of the x-axis

    )
    st.plotly_chart(fig_line, use_container_width=True, auto_open=False)
    st.caption(f"Abbildung 1: {selected_indicator_1} und {selected_indicator_2} pro Monat in der Gemeinde {selected_Gemeinde} von {earliest_year} - {most_recent_year}")


    #### Jahresvergleich

    st.subheader("Jahresvergleich")

    selected_indicator_Ankünfte_Logiernächte = st.selectbox('Auswahl Kennzahl', ["Logiernächte", "Ankünfte"], index=0)
    # Line chart using Plotly in the first column
    fig_line = px.line(filtered_df_2,
                    x='Monat',
                    color='Jahr',
                    y=selected_indicator_Ankünfte_Logiernächte,
                    title=f"",
                    color_discrete_sequence=custom_color_sequence)
    
    # calculate indikator mean
    avg = filtered_df_2[selected_indicator_Ankünfte_Logiernächte].mean()

    fig_line.update_layout(
        xaxis_title='',  # Hide the title of the x-axis
        #legend_traceorder="reversed",  # Sort the legend in descending order
        legend_title_text=''  # Hide the title of the x-axis
    )
    st.plotly_chart(fig_line, use_container_width=True, auto_open=True)
    st.caption(f"Abbildung 2: {selected_indicator_Ankünfte_Logiernächte} pro Monat in der Gemeinde {selected_Gemeinde} im Jahresvergleich")

    st.markdown('#')
    st.markdown('#')

    st.header("Betriebe, Zimmer und Auslastung")


    col1, col2, col3 = st.columns(3)

    col1.metric(f"Geöffnete Betriebe ⌀",
                average_betriebe_per_month_formatted,
                help=f"⌀ Anzahl der geöffneten Betriebe im ausgewählten Zeitraum ({start_year} - {end_year})"
                )
    col2.metric(f"{str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}",
                average_betriebe_current_month_formatted,
                help=f"Anzahl der geöffneten Betriebe im {str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}. Delta zeigt die Absolute Differenz zum gleichen Monat im Vorjahr",
                delta=f"{average_betriebe_current_month_change}")

    col1, col2, col3 = st.columns(3)

    col1.metric(f"Verfügbare Zimmer ⌀",
                average_zimmer_per_month_formatted,
                help=f"⌀ Anzahl der verfügbaren Zimmer im ausgewählten Zeitraum ({start_year} - {end_year})")
    col2.metric(f"{str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}",
                average_zimmer_current_month_formatted,
                help=f"Anzahl der verfügbaren Zimmer im {str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}. Delta zeigt die Absolute Differenz zum gleichen Monat im Vorjahr",
                delta = f"{average_zimmer_current_month_change}"
                )



    col1, col2, col3 = st.columns(3)

    
    col1.metric(f"Monatliche Zimmernächte ⌀ ",
                average_zimmernaechte_per_month_formatted,
                help=f"⌀ Monatliche Zimmernächte im ausgewählten Zeitraum ({start_year} - {end_year})")
    col2.metric(f"{str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}",
                average_zimmernaechte_current_month_formatted,
                help=f"Monatliche Zimmernächte im {str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}. Delta zeigt die Absolute Differenz der % Punkte zum gleichen Monat im Vorjahr",
                delta=f"{average_zimmernaechte_current_month_change}")
    

    # Create two columns for metrics and line chart
    col1, col2, col3 = st.columns(3)

    col1.metric(f"Monatliche Zimmerauslastung ⌀",
                average_zimmerauslastung_per_month_formatted,
                help=f"⌀ Monatliche Zimmerauslastung im ausgewählten Zeitraum ({start_year} - {end_year})"
                )
    
    col2.metric(f"{str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}",
                average_zimmerauslastung_current_month_formatted,
                help=f"Monatliche Zimmerauslastung im {str(filtered_df_2_current_month['Monat'].iloc[0])} {str(filtered_df_2_current_month['Jahr'].iloc[0])}. Delta zeigt die % Differenz zum gleichen Monat im Vorjahr",
                delta=f"{average_zimmerauslastung_current_month_change}"
                )

    

    selected_indicator = st.selectbox('Auswahl Kennzahl', ["Betriebe","Zimmer","Zimmernächte",'Zimmerauslastung in %'], index=0)

    # Line chart using Plotly in the first column
    st.subheader("Gesamtentwicklung")
    fig_line = px.line(filtered_df_2,
                    x='Date',
                    y=selected_indicator,
                    title="",
                    color_discrete_sequence=custom_color_sequence)  # Add colors for each indicator

    fig_line.update_layout(
        xaxis_title='',  # Hide the title of the x-axis
        yaxis_title='',
        legend_title_text=''  # Hide the title of the x-axis

    )
    st.plotly_chart(fig_line, use_container_width=True, auto_open=False)
    st.caption(f"Abbildung 3: {selected_indicator} pro Monat in der Gemeinde {selected_Gemeinde} von {earliest_year} - {most_recent_year}")


    st.subheader("Jahresvergleich")
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
        #legend_traceorder="reversed",  # Sort the legend in descending order
        legend_title_text=''  # Hide the title of the x-axis
    )

    st.plotly_chart(fig_line, use_container_width=True, auto_open=False)
    st.caption(f"Abbildung 4: {selected_indicator} pro Monat in der Gemeinde {selected_Gemeinde} im Jahresvergleich")

    # Create two columns for metrics and line chart
    col1, col2, col3, col4, col5, col6 ,col7, col8 = st.columns(8)
    col1.text("")

def create_other_page(df,selected_Gemeinde):
    #selected_Gemeinde = st.sidebar.selectbox('Auswahl Gemeinde', df['Gemeinde'].unique(), index=0)
    
    # Filter dataframe based on selected Gemeinde
    filtered_df = df[df['Gemeinde'] == selected_Gemeinde]
    #st.title(":flag-ch: Hotellerie Explorer")
    st.title(f":flag-ch: Kennzahlen nach Gemeinde und Herkunftsland")
    st.divider()
    #st.caption(f"Gemeinde: {selected_Gemeinde}")
    # Add a radio button to switch between Logiernächte and Ankünfte
    selected_indicator = st.selectbox('Auswahl Kennzahl', ["Logiernächte", "Ankünfte"], index=0)

    #######
    #######

    # Determine the column for the y-axis based on the selected plot type
    if selected_indicator == 'Logiernächte':
        y_column = 'Logiernächte'
    elif selected_indicator == 'Ankünfte':
        y_column = 'Ankünfte'

    # Perform grouping and aggregation
    grouped_df = filtered_df.groupby(['Herkunftsland', 'Date']).sum().reset_index()
    # Sort the unique values based on aggregated values in descending order
    sorted_values = grouped_df.groupby('Herkunftsland').sum().sort_values(y_column, ascending=False).index.tolist()
    # Create a new column to group Herkunftsländer
    grouped_df['Herkunftsland_grouped'] = grouped_df['Herkunftsland'].apply(lambda x: x if x in sorted_values[:15] else 'Others')
    grouped_df_no_date = grouped_df.groupby('Herkunftsland_grouped').agg({'Ankünfte': 'sum', 'Logiernächte': 'sum','Aufenthaltsdauer': 'mean'}).reset_index()
    grouped_df_date = grouped_df.groupby(['Herkunftsland_grouped','Date']).agg({'Ankünfte': 'sum', 'Logiernächte': 'sum','Aufenthaltsdauer': 'mean'}).reset_index()

    # Create two columns for metrics and line chart
    col1, col2, col3 = st.columns([2, 0.2, 1])


    #### Detailed top 15 Countries ########
    fig_bar = px.bar(
        grouped_df_no_date,
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
        grouped_df_no_date,
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


    # Time Areas Detailed
    fig_area = px.area(
        grouped_df_date,
        x='Date',
        y=y_column,
        color='Herkunftsland_grouped',
        color_discrete_sequence=custom_color_sequence
    )
    fig_area.update_xaxes(categoryorder='array',
                          categoryarray=sorted_values + ['Others'])
    fig_area.update_layout(
        legend_title='Herkunftsland'
    )

    ### Grobe granularität (International und Domestic ###

    grouped_df_grob = filtered_df.groupby(['Herkunftsland_grob', 'Date']).sum().reset_index()
    grouped_df_no_date_grob = grouped_df_grob.groupby('Herkunftsland_grob').agg({'Ankünfte': 'sum', 'Logiernächte': 'sum','Aufenthaltsdauer': 'mean'}).reset_index()
    grouped_df_date_grob = grouped_df_grob.groupby(['Herkunftsland_grob','Date']).agg({'Ankünfte': 'sum', 'Logiernächte': 'sum','Aufenthaltsdauer': 'mean'}).reset_index()

    fig_bar_grob = px.bar(
        grouped_df_no_date_grob,
        x='Herkunftsland_grob',
        y=y_column,
        color='Herkunftsland_grob',
        title="",
        color_discrete_sequence=custom_color_sequence,
    )

    fig_bar_grob.update_traces(
        hovertemplate='%{y}',
        texttemplate='%{y:,.0f}',  # Format the label to display the value with two decimal places
        textposition='auto'  # Position the labels outside the bars
        )
    fig_bar_grob.update_layout(
        legend_title='Herkunftsland',
        xaxis_title='',  # Hide the title of the x-axis
        showlegend=False  # Remove the legend
    )

    # Donut Chart
    fig_donut_grob = px.pie(
        grouped_df_no_date_grob,
        names='Herkunftsland_grob',
        values=y_column,
        hole=0.5,
        color_discrete_sequence=custom_color_sequence,
    )

    fig_donut_grob.update_traces(textposition='inside', textinfo='percent')
    fig_donut_grob.update_layout(
        legend_title='Herkunftsland'
    )

    # Time Areas grob
    fig_area_grob = px.area(
        grouped_df_date_grob ,
        x='Date',
        y=y_column,
        color='Herkunftsland_grob',
        color_discrete_sequence=custom_color_sequence
    )
    fig_area_grob.update_layout(
    legend_title='Herkunftsland',
    legend_traceorder='reversed'  # Reverse the order of the legend
    )
    
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_bar_grob, use_container_width=True, auto_open=False)
    col2.plotly_chart(fig_donut_grob, use_container_width=True, auto_open=False)
    st.caption(f"Abbildung 2: {selected_indicator} für die Gemeinde {selected_Gemeinde} (Zeitraum {start_year} - {end_year})")
    st.plotly_chart(fig_area_grob, use_container_width=True, auto_open=False)
    st.caption(f"Abbildung 3: {selected_indicator} pro Monat in der Gemeinde {selected_Gemeinde} von {start_year} - {end_year} nach Herkunftsland")

    st.plotly_chart(fig_bar, use_container_width=True, auto_open=False)
    st.caption(f"Abbildung 1: {selected_indicator} für die Gemeinde {selected_Gemeinde} nach Herkunftsland Absolut (Zeitraum {start_year} - {end_year})")
    st.plotly_chart(fig_donut, use_container_width=True, auto_open=False)
    st.caption(f"Abbildung 2: {selected_indicator} für die Gemeinde {selected_Gemeinde} nach Herkunftsland in % (Zeitraum {start_year} - {end_year})")
    st.plotly_chart(fig_area, use_container_width=True, auto_open=False)
    st.caption(f"Abbildung 3: {selected_indicator} pro Monat in der Gemeinde {selected_Gemeinde} von {start_year} - {end_year} nach Herkunftsland")

    # Download CSV
    #csv = filtered_df.to_csv(index=False)
    #st.download_button(
    #    label="Download data as CSV",
    #   data=csv,
    #   file_name='large_df.csv',
    #    mime='text/csv'
    #)


def create_markt_page():
    #st.title(":flag-ch: Hotellerie Explorer")
    st.title(f":flag-ch: Kennzahlen Gesamtmarkt")
    image = Image.open('under-construction.gif')
    st.image(image, caption='Coming Chritmas 2002')



#### Globale Datumsvariablen und Update BFS Logik 8 tag im Monat ###########
# Calculate the cutoff date (last day of the month before the previous month
current_date = datetime.date.today()

if current_date.day < 8:
    cutoff_date = datetime.date(current_date.year, current_date.month - 3, calendar.monthrange(current_date.year, current_date.month - 3)[1])
else:
    cutoff_date = datetime.date(current_date.year, current_date.month - 2, calendar.monthrange(current_date.year, current_date.month - 2)[1])

# Define the date range for the slider
start_date = datetime.date(2018, 1, 1)
end_date = cutoff_date
first_day_actual_month = cutoff_date.replace(day=1)

start_year = start_date.year
end_year = end_date.year

###############################################


######################
# Sidebar navigation #
######################

st.sidebar.title("🇨🇭 Hotellerie Explorer")
page = st.sidebar.selectbox("", ("Nach Gemeinde", "Nach Gemeinde und Herkunftsland"))
st.sidebar.divider() 

#### Auswahl Gemeinde Global
selected_Gemeinde = st.sidebar.selectbox('Auswahl Gemeinde', df_supply['Gemeinde'].unique(), index=0)


##### Auswahl Zeithorizont und filterung DFs
selected_years = st.sidebar.slider(
    "Zeitraum:",
    value=(start_year, end_year),
    min_value=2013,  # Set the minimum value of the slider
    max_value=end_year  # Set the maximum value of the slider
)

start_year = selected_years[0]
end_year = selected_years[1]

# Get the start_date and end_date based on the selection
start_date = datetime.date(start_year, 1, 1)
end_date = datetime.date(end_year, 12, 31)

# Apply date filter to df Country
df_country = df_country[(df_country['Jahr'] >= start_year) & (df_country['Jahr'] <= end_year)]
first_day_actual_month = df_country['Date'].max()
if end_date > first_day_actual_month:
    end_date = first_day_actual_month

# Apply date filter to df Supply 
df_supply = df_supply[(df_supply['Jahr'] >= start_year) & (df_supply['Jahr'] <= end_year)]
first_day_actual_month = df_supply['Date'].max()
if end_date > first_day_actual_month:
    end_date = first_day_actual_month


#### Einstellungen
st.sidebar.divider() 
st.sidebar.write("")
expander = st.sidebar.expander("Custom Colors")
with expander:
    col1, col2, col3, col4, col5 = st.columns(5)
    color1 = col1.color_picker('1st', '#80bbad')
    color2 = col2.color_picker('2nd', '#435254')
    color3 = col3.color_picker('3rd', '#17e88f')
    color4 = col4.color_picker('4th', '#dbd99a')
    color5 = col5.color_picker('5th', '#5ab689')
    color6 = col1.color_picker('6th', '#368c7a')
    color7 = col2.color_picker('7th', '#93b886')
    color8 = col3.color_picker('8th', '#779778')
    color9 = col4.color_picker('9th', '#1ad3aa')
    color10 = col5.color_picker('10th', '#c4c085')
    color11 = col1.color_picker('11th', '#a6b481')
    color12 = col2.color_picker('12th', '#15634d')
    color13 = col3.color_picker('13th', '#00aa85')
    color14 = col4.color_picker('14th', '#007754')
    color15 = col5.color_picker('15th', '#abd4c8')
    color16 = col1.color_picker('16th', '#d4c997')
    color17 = col2.color_picker('17th', '#bebf7a')
    color18 = col3.color_picker('18th', '#e2c48e')
    color19 = col4.color_picker('19th', '#9db784')
    color20 = col5.color_picker('20th', '#82a793')

    custom_color_sequence = [
        color1, color2, color3, color4, color5, color6, color7, color8, color9, color10,
        color11, color12, color13, color14, color15, color16, color17, color18, color19, color20
    ]


#### Page Selection

if page == "Nach Gemeinde":
    create_main_page(df_supply,selected_Gemeinde)
elif page == "Nach Gemeinde und Herkunftsland":
    create_other_page(df_country,selected_Gemeinde)
elif page == "Gesamtmarkt":
    create_markt_page()

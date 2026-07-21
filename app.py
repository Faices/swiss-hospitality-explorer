import streamlit as st
import pandas as pd
import plotly.express as px
from pyaxis import pyaxis
import datetime
import numpy as np
from PIL import Image
import calendar
from streamlit import config
import requests
from io import BytesIO
import datetime
import calendar
import pandas as pd
import plotly.graph_objs as go
import base64
import os
import gc

APP_DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_resource
def local_icon_data_uri(relative_path: str) -> str:
    mime = "image/png" if relative_path.lower().endswith(".png") else "image/svg+xml"
    with open(os.path.join(APP_DIR, relative_path), "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


# Set the page width m #
st.set_page_config(page_title='Swiss Hospitality Explorer (Beta)',page_icon= "🇨🇭",initial_sidebar_state="auto")

# Plot styling
line_shape = 'spline'

##########
## Data ##
##########

## Kantonswappen Links ##
kantonswappen = {
        "Aargau":"images/kantonicons/Aargau.svg",
        "Appenzell Ausserrhoden":"images/kantonicons/AppenzellAusserrhoden.svg",
        "Appenzell Innerrhoden":"images/kantonicons/AppenzellInnerrhoden.svg",
        "Basel-Landschaft":"images/kantonicons/Basel-Landschaft.svg",
        "Basel-Stadt":"images/kantonicons/Basel-Stadt.svg",
        "Bern / Berne":"images/kantonicons/Bern.svg",
        "Fribourg / Freiburg":"images/kantonicons/Fribourg.svg",
        "Genčve":"images/kantonicons/Geneve.svg",
        "Glarus":"images/kantonicons/Glarus.svg",
        "Graubünden / Grigioni / Grischun":"images/kantonicons/Graubuenden.svg",
        "Jura":"images/kantonicons/Jura.svg",
        "Luzern":"images/kantonicons/Luzern.svg",
        "Neuchâtel":"images/kantonicons/Neuchatel.svg",
        "Nidwalden":"images/kantonicons/Nidwalden.svg",
        "Obwalden":"images/kantonicons/Obwalden.svg",
        "Schaffhausen":"images/kantonicons/Schaffhausen.svg",
        "Schwyz":"images/kantonicons/Schwyz.svg",
        "Solothurn":"images/kantonicons/Solothurn.svg",
        "St. Gallen":"images/kantonicons/StGallen.svg",
        "Thurgau":"images/kantonicons/Thurgau.svg",
        "Ticino":"images/kantonicons/Ticino.svg",
        "Uri":"images/kantonicons/Uri.svg",
        "Valais / Wallis":"images/kantonicons/Valais.svg",
        "Vaud":"images/kantonicons/Vaud.svg",
        "Zug":"images/kantonicons/Zug.svg",
        "Zürich":"images/kantonicons/Zuerich.svg"
    }
kantonswappen = {k: local_icon_data_uri(v) for k, v in kantonswappen.items()}


## Gemeindewappen Links
gemeindewappen = {
    'Adelboden': 'images/gemeindeicons/Adelboden.svg',
    'Andermatt': 'images/gemeindeicons/Andermatt.svg',
    'Anniviers': 'images/gemeindeicons/Anniviers.svg',
    'Arosa': 'images/gemeindeicons/Arosa.svg',
    'Ascona': 'images/gemeindeicons/Ascona.svg',
    'Bad Ragaz': 'images/gemeindeicons/BadRagaz.svg',
    'Baden': 'images/gemeindeicons/Baden.svg',
    'Basel': 'images/gemeindeicons/Basel.svg',
    'Beatenberg': 'images/gemeindeicons/Beatenberg.svg',
    'Bellinzona': 'images/gemeindeicons/Bellinzona.svg',
    'Bern': 'images/gemeindeicons/Bern.svg',
    'Biel/Bienne': 'images/gemeindeicons/BielBienne.svg',
    'Brienz (BE)': 'images/gemeindeicons/Brienz.svg',
    'Brig-Glis': 'images/gemeindeicons/BrigGlis.svg',
    'Bulle': 'images/gemeindeicons/Bulle.svg',
    'Celerina/Schlarigna': 'images/gemeindeicons/CelerinaSchlarigna.svg',
    'Chur': 'images/gemeindeicons/Chur.svg',
    'Crans-Montana': 'images/gemeindeicons/CransMontana.svg',
    'Davos': 'images/gemeindeicons/Davos.svg',
    'Disentis/Mustér': 'images/gemeindeicons/DisentisMuster.svg',
    'Einsiedeln': 'images/gemeindeicons/Einsiedeln.svg',
    'Engelberg': 'images/gemeindeicons/Engelberg.svg',
    'Feusisberg': 'images/gemeindeicons/Feusisberg.svg',
    'Flims': 'images/gemeindeicons/Flims.svg',
    'Freienbach': 'images/gemeindeicons/Freienbach.svg',
    'Fribourg': 'images/gemeindeicons/Fribourg.svg',
    'Gambarogno': 'images/gemeindeicons/Gambarogno.svg',
    'Genčve': 'images/gemeindeicons/Geneve.svg',
    'Glarus Nord': 'images/gemeindeicons/GlarusNord.svg',
    'Glarus Süd': 'images/gemeindeicons/GlarusSud.svg',
    'Grindelwald': 'images/gemeindeicons/Grindelwald.svg',
    'Hasliberg': 'images/gemeindeicons/Hasliberg.svg',
    'Ingenbohl': 'images/gemeindeicons/Ingenbohl.svg',
    'Interlaken': 'images/gemeindeicons/Interlaken.svg',
    'Kandersteg': 'images/gemeindeicons/Kandersteg.svg',
    'Kerns': 'images/gemeindeicons/Kerns.svg',
    'Klosters-Serneus': 'images/gemeindeicons/KlostersSerneus.svg',
    'Kloten': 'images/gemeindeicons/Kloten.svg',
    'Kriens': 'images/gemeindeicons/Kriens.svg',
    'Küssnacht (SZ)': 'images/gemeindeicons/Küssnacht.svg',
    'Laax': 'images/gemeindeicons/Laax.svg',
    'Lausanne': 'images/gemeindeicons/Lausanne.svg',
    'Lauterbrunnen': 'images/gemeindeicons/Lauterbrunnen.svg',
    'Lenk': 'images/gemeindeicons/Lenk.svg',
    'Leukerbad': 'images/gemeindeicons/Leukerbad.png',
    'Leysin': 'images/gemeindeicons/Leysin.svg',
    'Leytron': 'images/gemeindeicons/Leytron.svg',
    'Locarno': 'images/gemeindeicons/Locarno.svg',
    'Lugano': 'images/gemeindeicons/Lugano.svg',
    'Luzern': 'images/gemeindeicons/Luzern.svg',
    'Martigny': 'images/gemeindeicons/Martigny.svg',
    'Matten bei Interlaken': 'images/gemeindeicons/MattenBeiInterlaken.svg',
    'Meiringen': 'images/gemeindeicons/Meiringen.svg',
    'Meyrin': 'images/gemeindeicons/Meyrin.svg',
    'Minusio': 'images/gemeindeicons/Minusio.svg',
    'Montreux': 'images/gemeindeicons/Montreux.svg',
    'Morges': 'images/gemeindeicons/Morges.svg',
    'Morschach': 'images/gemeindeicons/Morschach.svg',
    'Muralto': 'images/gemeindeicons/Muralto.svg',
    'Neuchâtel': 'images/gemeindeicons/Neuchatel.svg',
    'Ollon': 'images/gemeindeicons/Ollon.svg',
    'Olten': 'images/gemeindeicons/Olten.svg',
    'Opfikon': 'images/gemeindeicons/Opfikon.svg',
    'Ormont-Dessus': 'images/gemeindeicons/OrmontDessus.svg',
    'Paradiso': 'images/gemeindeicons/Paradiso.svg',
    'Pontresina': 'images/gemeindeicons/Pontresina.svg',
    'Pratteln': 'images/gemeindeicons/Pratteln.svg',
    'Quarten': 'images/gemeindeicons/Quarten.svg',
    'Saanen': 'images/gemeindeicons/Saanen.svg',
    'Saas-Fee': 'images/gemeindeicons/SaasFee.svg',
    'Sachseln': 'images/gemeindeicons/Sachseln.svg',
    'Samedan': 'images/gemeindeicons/Samedan.svg',
    'Samnaun': 'images/gemeindeicons/Samnaun.svg',
    'Schaffhausen': 'images/gemeindeicons/Schaffhausen.svg',
    'Schwende-Rüte': 'images/gemeindeicons/SchwendeRute.png',
    'Scuol': 'images/gemeindeicons/Scuol.svg',
    'Sigriswil': 'images/gemeindeicons/Sigriswil.svg',
    'Sils im Engadin/Segl': 'images/gemeindeicons/SilsImEngadinSegl.svg',
    'Silvaplana': 'images/gemeindeicons/Silvaplana.svg',
    'Sion': 'images/gemeindeicons/Sion.svg',
    'Solothurn': 'images/gemeindeicons/Solothurn.svg',
    'Spiez': 'images/gemeindeicons/Spiez.svg',
    'St. Gallen': 'images/gemeindeicons/StGallen.svg',
    'St. Moritz': 'images/gemeindeicons/StMoritz.svg',
    'Thun': 'images/gemeindeicons/Thun.svg',
    'Täsch': 'images/gemeindeicons/Tasch.svg',
    'Unterseen': 'images/gemeindeicons/Unterseen.svg',
    'Val de Bagnes': 'images/gemeindeicons/ValDeBagnes.svg',
    'Vals': 'images/gemeindeicons/Vals.svg',
    'Vaz/Obervaz': 'images/gemeindeicons/VazObervaz.svg',
    'Vevey': 'images/gemeindeicons/Vevey.svg',
    'Weggis': 'images/gemeindeicons/Weggis.svg',
    'Wilderswil': 'images/gemeindeicons/Wilderswil.svg',
    'Wildhaus-Alt St. Johann': 'images/gemeindeicons/WildhausAltStJohann.svg',
    'Winterthur': 'images/gemeindeicons/Winterthur.svg',
    'Zermatt': 'images/gemeindeicons/Zermatt.svg',
    'Zernez': 'images/gemeindeicons/Zernez.svg',
    'Zug': 'images/gemeindeicons/Zug.svg',
    'Zurzach': 'images/gemeindeicons/Zurzach.svg',
    'Zürich': 'images/gemeindeicons/Zürich.svg'
}
gemeindewappen = {k: local_icon_data_uri(v) for k, v in gemeindewappen.items()}





## Flaggen Herkunfstländer Links imgur hashhiker ##
countryflags = {
        'Argentinien':'images/countryicons/argentina.svg',
        'Australien':'images/countryicons/australia.svg',
        'Bahrain':'images/countryicons/bahrain.svg',
        'Belarus':'images/countryicons/belarus.svg',
        'Belgien':'images/countryicons/belgium.svg',
        'Brasilien':'images/countryicons/brazil.svg',
        'Bulgarien':'images/countryicons/bulgaria.svg',
        'Chile':'images/countryicons/chile.svg',
        'China':'images/countryicons/china.svg',
       'Deutschland':'images/countryicons/germany.svg',
       'Dänemark':'images/countryicons/denmark.svg',
       'Estland':'images/countryicons/estonia.svg',
       'Finnland':'images/countryicons/finland.svg',
       'Frankreich':'images/countryicons/france.svg',
       'Griechenland':'images/countryicons/greece.svg',
       'Hongkong':'images/countryicons/hong-kong.svg',
       'Indien':'images/countryicons/india.svg',
       'Indonesien':'images/countryicons/indonesia.svg',
       'Irland':'images/countryicons/ireland.svg',
       'Island':'images/countryicons/iceland.svg',
       'Israel':'images/countryicons/israel.svg',
       'Italien':'images/countryicons/italy.svg',
       'Japan':'images/countryicons/japan.svg',
       'Kanada':'images/countryicons/canada.svg',
       'Katar':'images/countryicons/qatar.svg',
       'Korea (Süd-)':'images/countryicons/south-korea.svg',
       'Kroatien':'images/countryicons/croatia.svg',
       'Kuwait':'https://i.imgur.com/FZ75488.png',
       'Lettland':'images/countryicons/latvia.svg',
       'Liechtenstein':'images/countryicons/liechtenstein.svg',
       'Litauen':'images/countryicons/lithuania.svg',
       'Luxemburg':'images/countryicons/luxembourg.svg',
       'Malaysia':'images/countryicons/malasya.svg',
       'Malta':'images/countryicons/malta.svg',
       'Mexiko':'images/countryicons/mexico.svg',
       'Neuseeland, Ozeanien':'images/countryicons/new-zealand.svg',
       'Niederlande':'images/countryicons/netherlands.svg',
       'Norwegen':'images/countryicons/norway.svg',
       'Oman':'images/countryicons/oman.svg',
       'Philippinen':'images/countryicons/philippines.svg',
       'Polen':'images/countryicons/poland.svg',
       'Portugal':'images/countryicons/portugal.svg',
       'Rumänien':'images/countryicons/romania.svg',
       'Russland':'images/countryicons/russia.svg',
       'Saudi-Arabien':'images/countryicons/saudi-arabia.svg',
       'Schweden':'images/countryicons/sweden.svg',
       'Schweiz':'images/countryicons/switzerland.svg',
       'Serbien':'images/countryicons/serbia.svg',
       'Singapur':'images/countryicons/singapore.svg',
       'Slowakei':'images/countryicons/slovakia.svg',
       'Slowenien':'images/countryicons/slovenia.svg',
       'Spanien':'images/countryicons/spain.svg',
       'Südafrika':'images/countryicons/south-africa.svg',
       'Taiwan (Chinesisches Taipei)':'images/countryicons/taiwan.svg',
       'Thailand':'images/countryicons/thailand.svg',
       'Tschechien':'images/countryicons/czech-republic.svg',
       'Türkei':'images/countryicons/turkey.svg',
       'Ukraine':'images/countryicons/ukraine.svg',
       'Ungarn':'images/countryicons/hungary.svg',
       'Vereinigte Arabische Emirate':'images/countryicons/united-arab-emirates.svg',
       'Vereinigte Staaten':'images/countryicons/united-states.svg',
       'Vereinigtes Königreich':'images/countryicons/united-kingdom.svg',
       'Zypern':'https://upload.wikimedia.org/wikipedia/commons/d/d4/Flag_of_Cyprus.svg',
       'Ägypten':'images/countryicons/egypt.svg',
       'Österreich':'images/countryicons/austria.svg',
       'Übriges Afrika':'',
       'Übriges Europa':'https://i.imgur.com/sMKYRfd.png',
       'Übriges Nordafrika':'',
       'Übriges Süd- und Ostasien':'',
       'Übriges Südamerika':'',
       'Übriges Westasien':'',
       'Übriges Zentralamerika, Karibik':''
    }
countryflags = {k: (local_icon_data_uri(v) if v.startswith("images/") else v) for k, v in countryflags.items()}


gemeinde_kanton_mapping = {
    'Zürich': 'Zürich',
    'Samedan': 'Graubünden / Grigioni / Grischun',
    'Sachseln': 'Obwalden',
    'Saas-Fee': 'Valais / Wallis',
    'Saanen': 'Bern / Berne',
    'Quarten': 'St. Gallen',
    'Pratteln': 'Basel-Landschaft',
    'Pontresina': 'Graubünden / Grigioni / Grischun',
    'Paradiso': 'Ticino',
    'Ormont-Dessus': 'Vaud',
    'Opfikon': 'Zürich',
    'Olten': 'Solothurn',
    'Ollon': 'Vaud',
    'Neuchâtel': 'Neuchâtel',
    'Muralto': 'Ticino',
    'Morschach': 'Schwyz',
    'Morges': 'Vaud',
    'Montreux': 'Vaud',
    'Minusio': 'Ticino',
    'Meyrin': 'Genčve',
    'Meiringen': 'Bern',
    'Matten bei Interlaken': 'Bern',
    'Samnaun': 'Graubünden / Grigioni / Grischun',
    'Luzern': 'Luzern',
    'Schaffhausen': 'Schaffhausen',
    'Scuol': 'Graubünden / Grigioni / Grischun',
    'Zernez': 'Graubünden / Grigioni / Grischun',
    'Zermatt': 'Valais / Wallis',
    'Winterthur': 'Zürich',
    'Wildhaus-Alt St. Johann': 'St. Gallen',
    'Wilderswil': 'Bern',
    'Weggis': 'Luzern',
    'Vevey': 'Vaud',
    'Vaz/Obervaz': 'Graubünden / Grigioni / Grischun',
    'Vals': 'Graubünden / Grigioni / Grischun',
    'Val de Bagnes': 'Valais / Wallis',
    'Unterseen': 'Bern',
    'Täsch': 'Valais / Wallis',
    'Thun': 'Bern',
    'St. Moritz': 'Graubünden / Grigioni / Grischun',
    'St. Gallen': 'St. Gallen',
    'Spiez': 'Bern',
    'Solothurn': 'Solothurn',
    'Sion': 'Valais / Wallis',
    'Silvaplana': 'Graubünden / Grigioni / Grischun',
    'Sils im Engadin/Segl': 'Graubünden / Grigioni / Grischun',
    'Sigriswil': 'Bern',
    'Schwende-Rüte': 'Appenzell Ausserrhoden',
    'Zug': 'Zug',
    'Lugano': 'Ticino',
    'Leytron': 'Valais / Wallis',
    'Einsiedeln': 'Schwyz',
    'Disentis/Mustér': 'Grisons',
    'Davos': 'Graubünden / Grigioni / Grischun',
    'Crans-Montana': 'Valais / Wallis',
    'Chur': 'Graubünden / Grigioni / Grischun',
    'Celerina/Schlarigna': 'Graubünden / Grigioni / Grischun',
    'Bulle': 'Fribourg / Freiburg',
    'Brig-Glis': 'Valais / Wallis',
    'Brienz (BE)': 'Bern',
    'Biel/Bienne': 'Bern',
    'Bern': 'Bern / Berne',
    'Bellinzona': 'Ticino',
    'Beatenberg': 'Bern',
    'Basel': 'Basel-Stadt',
    'Baden': 'Aargau',
    'Bad Ragaz': 'St. Gallen',
    'Ascona': 'Ticino',
    'Arosa': 'Graubünden / Grigioni / Grischun',
    'Anniviers': 'Valais / Wallis',
    'Andermatt': 'Uri',
    'Adelboden': 'Bern',
    'Engelberg': 'Obwalden',
    'Locarno': 'Ticino',
    'Feusisberg': 'Schwyz',
    'Freienbach': 'Schwyz',
    'Leysin': 'Vaud',
    'Leukerbad': 'Valais / Wallis',
    'Lenk': 'Bern',
    'Lauterbrunnen': 'Bern',
    'Lausanne': 'Vaud',
    'Laax': 'Graubünden / Grigioni / Grischun',
    'Küssnacht (SZ)': 'Schwyz',
    'Kriens': 'Luzern',
    'Kloten': 'Zürich',
    'Klosters-Serneus': 'Graubünden / Grigioni / Grischun',
    'Kerns': 'Obwalden',
    'Kandersteg': 'Bern',
    'Interlaken': 'Bern',
    'Ingenbohl': 'Schwyz',
    'Hasliberg': 'Bern',
    'Grindelwald': 'Bern',
    'Glarus Süd': 'Glarus',
    'Glarus Nord': 'Glarus',
    'Genčve': 'Genčve',
    'Gambarogno': 'Ticino',
    'Fribourg': 'Fribourg / Freiburg',
    'Flims': 'Graubünden / Grigioni / Grischun',
    'Zurzach': 'Aargau',
    'Martigny': 'Valais / Wallis'
}


country_mapping = {
    'Argentinien': 'ARG',
    'Australien': 'AUS',
    'Bahrain': 'BHR',
    'Belarus': 'BLR',
    'Belgien': 'BEL',
    'Brasilien': 'BRA',
    'Bulgarien': 'BGR',
    'Chile': 'CHL',
    'China': 'CHN',
    'Deutschland': 'DEU',
    'Dänemark': 'DNK',
    'Estland': 'EST',
    'Finnland': 'FIN',
    'Frankreich': 'FRA',
    'Griechenland': 'GRC',
    'Hongkong': 'HKG',
    'Indien': 'IND',
    'Indonesien': 'IDN',
    'Irland': 'IRL',
    'Island': 'ISL',
    'Israel': 'ISR',
    'Italien': 'ITA',
    'Japan': 'JPN',
    'Kanada': 'CAN',
    'Katar': 'QAT',
    'Korea (Süd-)': 'KOR',
    'Kroatien': 'HRV',
    'Kuwait': 'KWT',
    'Lettland': 'LVA',
    'Liechtenstein': 'LIE',
    'Litauen': 'LTU',
    'Luxemburg': 'LUX',
    'Malaysia': 'MYS',
    'Malta': 'MLT',
    'Mexiko': 'MEX',
    'Neuseeland, Ozeanien': 'NZL',
    'Niederlande': 'NLD',
    'Norwegen': 'NOR',
    'Oman': 'OMN',
    'Philippinen': 'PHL',
    'Polen': 'POL',
    'Portugal': 'PRT',
    'Rumänien': 'ROU',
    'Russland': 'RUS',
    'Saudi-Arabien': 'SAU',
    'Schweden': 'SWE',
    'Schweiz': 'CHE',
    'Serbien': 'SRB',
    'Singapur': 'SGP',
    'Slowakei': 'SVK',
    'Slowenien': 'SVN',
    'Spanien': 'ESP',
    'Südafrika': 'ZAF',
    'Taiwan (Chinesisches Taipei)': 'TWN',
    'Thailand': 'THA',
    'Tschechien': 'CZE',
    'Türkei': 'TUR',
    'Ukraine': 'UKR',
    'Ungarn': 'HUN',
    'Vereinigte Arabische Emirate': 'ARE',
    'Vereinigte Staaten': 'USA',
    'Vereinigtes Königreich': 'GBR',
    'Zypern': 'CYP',
    'Ägypten': 'EGY',
    'Österreich': 'AUT',
    'Übriges Afrika': 'AFR',
    'Übriges Europa': 'EUR',
    'Übriges Nordafrika': 'NAF',
    'Übriges Süd- und Ostasien': 'SOA',
    'Übriges Südamerika': 'SAM',
    'Übriges Westasien': 'WAS',
    'Übriges Zentralamerika, Karibik': 'ZAK'
}

# Constants
COUNTRY_URL = "https://www.pxweb.bfs.admin.ch/DownloadFile.aspx?file=px-x-1003020000_101"
SUPPLY_URL = "https://www.pxweb.bfs.admin.ch/DownloadFile.aspx?file=px-x-1003020000_201"
KANTON_URL = "https://www.pxweb.bfs.admin.ch/DownloadFile.aspx?file=px-x-1003020000_102"
MONTH_MAPPING = {
    'Januar': '1', 'Februar': '2', 'März': '3', 'April': '4', 'Mai': '5', 'Juni': '6',
    'Juli': '7', 'August': '8', 'September': '9', 'Oktober': '10', 'November': '11', 'Dezember': '12'
}


# Helper functions

def _categorize_low_cardinality_columns(df: pd.DataFrame) -> pd.DataFrame:
    # The raw PX data repeats a handful of Jahr/Monat/Gemeinde/Herkunftsland/Indikator
    # strings across millions of rows; category dtype cuts that memory dramatically
    # during download/pivot, where the peak footprint otherwise blows past the
    # ~1GB memory budget on Streamlit Community Cloud.
    for column in df.columns:
        if column != "DATA":
            df[column] = df[column].astype("category")
    return df

def download_data(url: str) -> pd.DataFrame:
    px_data = pyaxis.parse(uri=url, encoding='ISO-8859-2')
    return _categorize_low_cardinality_columns(px_data['DATA'])

def download_data_utf8(url: str) -> pd.DataFrame:
    px_data = pyaxis.parse(uri=url, encoding='utf-8')
    return _categorize_low_cardinality_columns(px_data['DATA'])


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[(df["Monat"] != "Jahrestotal")]
    return df

def pivot_data(df: pd.DataFrame, index_columns: list[str], columns: str, values: str) -> pd.DataFrame:
    df = df.pivot(index=index_columns, columns=columns, values=values).reset_index()
    # Cast back to plain string dtype so downstream groupby/merge behavior stays
    # exactly as before category dtype was introduced (category groupby includes
    # unused categories by default, which would otherwise add phantom rows).
    for column in index_columns:
        df[column] = df[column].astype(str)
    return df

def convert_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    
    # Ensure 'Jahr' is in integer format and then convert to string
    df['Year'] = df['Jahr'].astype(int).astype(str)
    
    # Map 'Monat' to its corresponding integer value
    df['Month'] = df['Monat'].map(MONTH_MAPPING).astype(int).astype(str)
    
    # Create a combined 'Date' string
    df['Date_str'] = df['Year'] + '-' + df['Month']
    
    # Check if there are any problematic date strings before conversion
    problematic_dates = df[~df['Date_str'].str.match(r'^\d{4}-\d{1,2}$')]
    if not problematic_dates.empty:
        raise ValueError(f"Problematic date strings found: {problematic_dates['Date_str'].values}")
    
    # Convert 'Date_str' to datetime
    df['Date'] = pd.to_datetime(df['Date_str'])
    df['Date'] = df['Date'].dt.date
    
    # Rearrange columns and sort by date
    df = df[['Date'] + df.columns[:-3].tolist()]
    df = df.sort_values('Date').reset_index(drop=True)
    
    return df

def convert_columns(df: pd.DataFrame, numeric_columns: list[str]) -> pd.DataFrame:
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce', downcast='float')
    return df

def calculate_additional_columns(df: pd.DataFrame, numerator: str, denominator: str, result_column: str) -> pd.DataFrame:
    df[result_column] = df[numerator] / df[denominator]
    return df

def map_herkunftsland(df: pd.DataFrame, herkunftsland_column: str, result_column: str) -> pd.DataFrame:
    df[result_column] = df[herkunftsland_column].apply(lambda x: "Domestic" if x == "Schweiz" else "International")
    return df

# Check if a value is numeric
def is_numeric(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# Load data
@st.cache_data
def load_data():
    df_country = download_data(COUNTRY_URL)
    df_country = filter_data(df_country)
    df_country = pivot_data(df_country, ["Jahr", "Monat", "Gemeinde", "Herkunftsland"], "Indikator", "DATA")
    df_country = convert_to_datetime(df_country)
    df_country = convert_columns(df_country, ["Logiernächte", "Ankünfte"])
    df_country = df_country[df_country['Ankünfte'].apply(is_numeric) & df_country['Logiernächte'].apply(is_numeric)] #filter out not avaiable data
    df_country = calculate_additional_columns(df_country, "Logiernächte", "Ankünfte", "Aufenthaltsdauer")
    df_country = map_herkunftsland(df_country, "Herkunftsland", "Herkunftsland_grob")
    df_country = df_country[(df_country["Monat"] != "Jahrestotal") & (df_country["Herkunftsland"] != "Herkunftsland - Total")]
    gc.collect()

    df_supply = download_data(SUPPLY_URL)
    df_supply = filter_data(df_supply)
    df_supply = pivot_data(df_supply, ["Jahr", "Monat", "Gemeinde"], "Indikator", "DATA")
    df_supply = convert_to_datetime(df_supply)
    df_supply = convert_columns(df_supply, ["Ankünfte", "Betriebe", "Betten", "Bettenauslastung in %", "Logiernächte", "Zimmer", "Zimmerauslastung in %", "Zimmernächte"])
    df_supply = df_supply[df_supply['Ankünfte'].apply(is_numeric) & df_supply['Logiernächte'].apply(is_numeric)] #filter out not avaiable data
    gc.collect()

    df_kanton = download_data(KANTON_URL)
    df_kanton = filter_data(df_kanton)
    df_kanton = df_kanton[(df_kanton["Kanton"] != "Schweiz")]
    df_kanton = df_kanton[~df_kanton["Herkunftsland"].isin(['Baltische Staaten', 'Australien, Neuseeland, Ozeanien', 'Golf-Staaten', 'Serbien und Montenegro', 'Zentralamerika, Karibik'])]
    df_kanton = pivot_data(df_kanton, ["Jahr", "Monat", "Kanton", "Herkunftsland"], "Indikator", "DATA")
    df_kanton = convert_to_datetime(df_kanton)
    df_kanton = convert_columns(df_kanton, ["Logiernächte", "Ankünfte"])
    df_kanton = calculate_additional_columns(df_kanton, "Logiernächte", "Ankünfte", "Aufenthaltsdauer")
    df_kanton = df_kanton[df_kanton['Ankünfte'].apply(is_numeric) & df_kanton['Logiernächte'].apply(is_numeric)] #filter out not avaiable data
    df_kanton = map_herkunftsland(df_kanton, "Herkunftsland", "Herkunftsland_grob")
    df_kanton = df_kanton[(df_kanton["Monat"] != "Jahrestotal") & (df_kanton["Herkunftsland"] != "Herkunftsland - Total")]

    df_country['Jahr'] = df_country['Jahr'].astype(int)
    df_supply['Jahr'] = df_supply['Jahr'].astype(int)
    df_kanton['Jahr'] = df_kanton['Jahr'].astype(int)

    #df_hotels = pd.read_feather(f"data/20230721_Hotels.feather")


    return df_country, df_kanton, df_supply #df_hotels

df_country, df_kanton, df_supply = load_data()



def create_main_page(df,selected_Gemeinde):


    # Add a placeholder at the beginning of the page to not jump to a section
    top_placeholder = st.empty()
    st.write(
        f'<script>document.getElementById("{top_placeholder._id}").scrollIntoView();</script>',
        unsafe_allow_html=True
    )

     # Filter dataframe based on selected Gemeinde
    filtered_df_2 = df[df['Gemeinde'] == selected_Gemeinde]

    # map kantonicons to df
    filtered_df_2.insert(0, "Kanton", filtered_df_2['Gemeinde'].map(gemeinde_kanton_mapping))
    filtered_df_2.insert(0, "Kantonswappen", filtered_df_2['Kanton'].map(kantonswappen))
    kantonswappen_url = filtered_df_2['Kantonswappen'].iloc[0]
    filtered_df_2.insert(0, "Gemeindewappen", filtered_df_2['Gemeinde'].map(gemeindewappen))
    gemeindewappen_url = filtered_df_2['Gemeindewappen'].iloc[0]


    # Display the title with image at the end
    st.markdown(
        f'<h1 style="display: flex; align-items: center;">Kennzahlen für die Gemeinde {selected_Gemeinde}<img src="{gemeindewappen_url}" style="max-height: 40px; margin-left: 10px;"></h1>',
        unsafe_allow_html=True
    )
    st.divider()


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
    
    # Create two columns for metrics and line chart
    st.header("Logiernächte & Ankünfte",
              help="Logiernächte: Die Gesamtanzahl der Übernachtungen.\n\nAnkünfte: Die Gesamtanzahl der Gäste, die angekommen sind.",
              )
    st.divider()
    
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
                    line_shape=line_shape,
                    color_discrete_sequence=custom_color_sequence)  # Add colors for each indicator

    fig_line.update_layout(
        xaxis_title='',  # Hide the title of the x-axis
        yaxis_title='',
        legend_title_text=''  # Hide the title of the x-axis

    )
    st.plotly_chart(fig_line,
                    width='stretch')
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
                    line_shape=line_shape,
                    color_discrete_sequence=custom_color_sequence)
    
    # calculate indikator mean
    avg = filtered_df_2[selected_indicator_Ankünfte_Logiernächte].mean()

    fig_line.update_layout(
        xaxis_title='',  # Hide the title of the x-axis
        #legend_traceorder="reversed",  # Sort the legend in descending order
        legend_title_text=''  # Hide the title of the x-axis
    )
    st.plotly_chart(fig_line,
                    width='stretch')
    st.caption(f"Abbildung 2: {selected_indicator_Ankünfte_Logiernächte} pro Monat in der Gemeinde {selected_Gemeinde} im Jahresvergleich")


    st.divider()
    st.header("Betriebe, Zimmer & Auslastung")
    st.divider()


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
                    line_shape=line_shape,
                    color_discrete_sequence=custom_color_sequence)  # Add colors for each indicator

    fig_line.update_layout(
        xaxis_title='',  # Hide the title of the x-axis
        yaxis_title='',
        legend_title_text=''  # Hide the title of the x-axis

    )
    st.plotly_chart(fig_line, width='stretch')
    st.caption(f"Abbildung 3: {selected_indicator} pro Monat in der Gemeinde {selected_Gemeinde} von {earliest_year} - {most_recent_year}")


    st.subheader("Jahresvergleich")
    # Line chart using Plotly in the first column
    fig_line = px.line(filtered_df_2,
                    x='Monat',
                    color='Jahr',
                    y=selected_indicator,
                    title=f"",
                    line_shape=line_shape,
                    color_discrete_sequence=custom_color_sequence)
    # calculate indikator mean
    avg = filtered_df_2[selected_indicator].mean()

    
    fig_line.update_layout(
        xaxis_title='',  # Hide the title of the x-axis
        #legend_traceorder="reversed",  # Sort the legend in descending order
        legend_title_text=''  # Hide the title of the x-axis
    )

    st.plotly_chart(fig_line, width='stretch')
    st.caption(f"Abbildung 4: {selected_indicator} pro Monat in der Gemeinde {selected_Gemeinde} im Jahresvergleich")
    st.divider()
    st.caption("with :heart: by Hashhiker")

def create_other_page(df,selected_Gemeinde):
    # Filter dataframe based on selected Gemeinde
    filtered_df = df[df['Gemeinde'] == selected_Gemeinde]

    # map kantonicons to df
    filtered_df.insert(0, "Kanton", filtered_df['Gemeinde'].map(gemeinde_kanton_mapping))
    filtered_df.insert(0, "Kantonswappen", filtered_df['Kanton'].map(kantonswappen))
    kantonswappen_url = filtered_df['Kantonswappen'].iloc[0]
    filtered_df.insert(0, "Gemeindewappen", filtered_df['Gemeinde'].map(gemeindewappen))
    gemeindewappen_url = filtered_df['Gemeindewappen'].iloc[0]


    # Display the title with image at the end
    st.markdown(
        f'<h1 style="display: flex; align-items: center;">Kennzahlen nach Herkunftsland für die Gemeinde {selected_Gemeinde}<img src="{gemeindewappen_url}" style="max-height: 40px; margin-left: 10px;"></h1>',
        unsafe_allow_html=True
    )


    
    # Add a radio button to switch between Logiernächte and Ankünfte
    st.divider()
    selected_indicator = st.selectbox('Auswahl Kennzahl', ["Logiernächte", "Ankünfte"], index=0)
    st.divider()
    st.header("Domestic vs. International")
    st.divider()

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
    sorted_values = grouped_df.groupby('Herkunftsland')[y_column].sum().sort_values(ascending=False).index.tolist()
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
        line_shape=line_shape,
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

    # Create a dictionary mapping values to specific colors
    fig_bar_grob = px.bar(
        grouped_df_no_date_grob,
        x='Herkunftsland_grob',
        y=y_column,
        color='Herkunftsland_grob',
        title="",
        color_discrete_sequence=[color1,color2]
        )

    fig_bar_grob.update_traces(
        hovertemplate='%{y}',
        texttemplate='%{y:,.0f}',  # Format the label to display the value with two decimal places
        textposition='auto'
    )

    fig_bar_grob.update_layout(
        legend_title='Herkunftsland',
        xaxis_title='',  # Hide the title of the x-axis
        showlegend=False  # Remove the legend
    )

    # Donut Chart
    color_map = {'International': color2, 'Domestic': color1}

    fig_donut_grob = px.pie(
        grouped_df_no_date_grob,
        names='Herkunftsland_grob',
        values=y_column,
        hole=0.5,
        color_discrete_sequence=[color_map[value] for value in grouped_df_no_date_grob['Herkunftsland_grob']]
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
        line_shape=line_shape,
        color='Herkunftsland_grob',
        color_discrete_sequence=[color1,color2]
    )
    fig_area_grob.update_layout(
    legend_title='Herkunftsland',
    legend_traceorder='reversed'  # Reverse the order of the legend
    )
    
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_bar_grob, width='stretch')
    col2.plotly_chart(fig_donut_grob, width='stretch')
    st.caption(f"Abbildung 1: {selected_indicator} für die Gemeinde {selected_Gemeinde} (Zeitraum {start_year} - {end_year})")
    st.plotly_chart(fig_area_grob, width='stretch')
    st.caption(f"Abbildung 2: {selected_indicator} pro Monat in der Gemeinde {selected_Gemeinde} von {start_year} - {end_year} nach Herkunftsland")

    st.divider()
    st.header("Top 15 Herkunftsländer")
    st.divider()
    st.plotly_chart(fig_bar, width='stretch')
    st.caption(f"Abbildung 3: {selected_indicator} für die Gemeinde {selected_Gemeinde} nach Herkunftsland Absolut (Zeitraum {start_year} - {end_year})")
    st.plotly_chart(fig_donut, width='stretch')
    st.caption(f"Abbildung 4: {selected_indicator} für die Gemeinde {selected_Gemeinde} nach Herkunftsland in % (Zeitraum {start_year} - {end_year})")
    st.plotly_chart(fig_area, width='stretch')
    st.caption(f"Abbildung 5: {selected_indicator} pro Monat in der Gemeinde {selected_Gemeinde} von {start_year} - {end_year} nach Herkunftsland")


    # Herkunftsland Dataframe
    grouped_df_Herkunftsland = filtered_df.groupby(['Date','Monat','Jahr','Herkunftsland']).agg({selected_indicator: 'sum'}).reset_index()
    grouped_df_Herkunftsland = grouped_df_Herkunftsland.groupby('Herkunftsland').agg({selected_indicator: list}).reset_index()
    grouped_df_Herkunftsland[f"{selected_indicator} Total"] = grouped_df_Herkunftsland[selected_indicator].apply(lambda x: sum(x))
    grouped_df_Herkunftsland[f"{selected_indicator} Anteil"] = ((100 / sum(grouped_df_Herkunftsland[f"{selected_indicator} Total"])) * grouped_df_Herkunftsland[f"{selected_indicator} Total"]).apply(lambda x: f"{x:.2f}%")
    grouped_df_Herkunftsland.insert(0, "Flagge", grouped_df_Herkunftsland['Herkunftsland'].map(countryflags))
    grouped_df_Herkunftsland = grouped_df_Herkunftsland.sort_values(f"{selected_indicator} Total",ascending=False)


    st.dataframe(
        grouped_df_Herkunftsland,
        column_config={
            "Flagge": st.column_config.ImageColumn("Flagge"),
            "Herkunftsland": "Herkunftsland",
            selected_indicator: st.column_config.LineChartColumn(
                selected_indicator),
            f"{selected_indicator} Anteil":st.column_config.ProgressColumn(
        f"{selected_indicator} Anteil",
            help="% zum Gesamtmarkt",
            min_value=0,
            max_value=1,
        ),

        },
        hide_index=True,
        width='stretch'
    )
    st.caption(f"Abbildung 6: {selected_indicator} für die Gemeinde {selected_Gemeinde} von {start_year} - {end_year} nach Herkunftsland")


    # Download CSV
    #csv = filtered_df.to_csv(index=False)
    #st.download_button(
    #    label="Download data as CSV",
    #   data=csv,
    #   file_name='large_df.csv',
    #    mime='text/csv'
    #)
    st.divider()
    st.caption("with :heart: by Hashhiker")


def create_markt_page(df,df_gemeinde):
    
    swissflag_url = local_icon_data_uri("images/countryicons/switzerland.svg")

    # Display the title with image at the end
    st.markdown(
        f'<h1 style="display: flex; align-items: center;">Kennzahlen Schweiz<img src="{swissflag_url }" style="max-height: 40px; margin-left: 10px;"></h1>',
        unsafe_allow_html=True
    )

    df = df.sort_values('Date')
    df_gemeinde = df_gemeinde.sort_values('Date')

    # Metrics Avererges whole time
    # Format the metrics with thousand separators and no decimal places
    sum_logiernächte_per_month_formatted_2 = "{:,.0f}".format(df['Logiernächte'].sum())
    sum_ankünfte_per_month_formatted = "{:,.0f}".format(df['Ankünfte'].sum())

    earliest_year = df["Jahr"].min()
    most_recent_year = df["Jahr"].max()

    #################### Aktuelle KPIS #######################

    # Dataframes last avaiable Month and same month last year
    filtered_df_2_current_month = df[df["Date"] == first_day_actual_month]
    filtered_df_2_current_month_last_year = df[df["Date"] == first_day_actual_month - datetime.timedelta(days=365)]

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
    filtered_df_2_ytd_current_year = df[
        (df["Date"] >= start_date_ytd) & (df["Date"] <= end_date)
    ]

    # Calculate the start and end dates for the YTD period of the previous year
    previous_year = current_year - 1
    start_date_last_year = datetime.date(previous_year, 1, 1)
    end_date_last_year = datetime.date(previous_year, current_month, 1)

    # Filter the DataFrame for the YTD period of the previous year
    filtered_df_2_ytd_last_year = df[
        (df["Date"] >= start_date_last_year) & (df["Date"] <= end_date_last_year)
    ]

    ########

    def calculate_percentage_change(current_value, previous_value):
        percentage_change = ((current_value - previous_value) / previous_value) * 100
        return round(percentage_change, 1)
    
    # Format the metrics with thousand separators and no decimal places
    average_logiernächte_current_month = filtered_df_2_current_month['Logiernächte'].sum()
    average_logiernächte_current_month_formatted = "{:,.0f}".format(average_logiernächte_current_month)
    average_logiernächte_current_month_last_year = filtered_df_2_current_month_last_year['Logiernächte'].sum()
    average_logiernächte_current_month_change = "{:,.1f}".format(calculate_percentage_change(average_logiernächte_current_month, average_logiernächte_current_month_last_year ))

    total_logiernächte_ytd = filtered_df_2_ytd_current_year['Logiernächte'].sum()
    total_logiernächte_ytd_formatted = "{:,.0f}".format(total_logiernächte_ytd)
    total_logiernächte_currenächte_ytd_last_year = filtered_df_2_ytd_last_year['Logiernächte'].sum()
    total_logiernächte_ytd_change = "{:,.1f}".format(calculate_percentage_change(total_logiernächte_ytd,total_logiernächte_currenächte_ytd_last_year))

    average_ankünfte_current_month = filtered_df_2_current_month['Ankünfte'].sum()
    average_ankünfte_current_month_formatted = "{:,.0f}".format(average_ankünfte_current_month)
    average_ankünfte_current_month_last_year = filtered_df_2_current_month_last_year['Ankünfte'].sum()
    average_ankünfte_current_month_change = "{:,.1f}".format(calculate_percentage_change(average_ankünfte_current_month, average_ankünfte_current_month_last_year))

    total_ankünfte_ytd = filtered_df_2_ytd_current_year['Ankünfte'].sum()
    total_ankünfte_ytd_formatted = "{:,.0f}".format(total_ankünfte_ytd)
    total_ankünfte_currenächte_ytd_last_year = filtered_df_2_ytd_last_year['Ankünfte'].sum()
    total_ankünfte_ytd_change = "{:,.1f}".format(calculate_percentage_change(total_ankünfte_ytd,total_ankünfte_currenächte_ytd_last_year))

    # Create two columns for metrics and line chart
    st.divider()
    st.header("Logiernächte & Ankünfte",
              help="Logiernächte: Die Gesamtanzahl der Übernachtungen.\n\nAnkünfte: Die Gesamtanzahl der Gäste, die angekommen sind.",
              )
    st.divider()
    
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

    grouped_df = df.groupby('Date').agg({'Ankünfte': 'sum', 'Logiernächte': 'sum','Aufenthaltsdauer': 'mean'}).reset_index()

    # Line chart using Plotly in the first column
    fig_line = px.line(grouped_df,
                    x='Date',
                    y=[selected_indicator_1, selected_indicator_2],  # Pass both indicators as a list
                    title="",
                    line_shape=line_shape,
                    color_discrete_sequence=custom_color_sequence)  # Add colors for each indicator

    fig_line.update_layout(
        xaxis_title='',  # Hide the title of the x-axis
        yaxis_title='',
        legend_title_text=''  # Hide the title of the x-axis

    )
    st.plotly_chart(fig_line, width='stretch')
    st.caption(f"Abbildung 1: {selected_indicator_1} und {selected_indicator_2} pro Monat von {earliest_year} - {most_recent_year}")


    #### Jahresvergleich

    st.subheader("Jahresvergleich")

    selected_indicator_Ankünfte_Logiernächte = st.selectbox('Auswahl Kennzahl', ["Logiernächte", "Ankünfte"], index=0, key='selected_indicator_Ankünfte_Logiernächte')
    grouped_df_2 = df.groupby(['Date','Monat','Jahr']).agg({'Ankünfte': 'sum', 'Logiernächte': 'sum','Aufenthaltsdauer': 'mean'}).reset_index()
    grouped_df_2 = grouped_df_2.sort_values('Date')


    # Line chart using Plotly in the first column
    fig_line = px.line(grouped_df_2,
                    x='Monat',
                    color='Jahr',
                    y=selected_indicator_Ankünfte_Logiernächte,
                    title=f"",
                    line_shape=line_shape,
                    color_discrete_sequence=custom_color_sequence)
    
    # calculate indikator mean
    avg = df[selected_indicator_Ankünfte_Logiernächte].mean()

    fig_line.update_layout(
        xaxis_title='',  # Hide the title of the x-axis
        #legend_traceorder="reversed",  # Sort the legend in descending order
        legend_title_text=''  # Hide the title of the x-axis
    )
    st.plotly_chart(fig_line, width='stretch')
    st.caption(f"Abbildung 2: {selected_indicator_Ankünfte_Logiernächte} pro Monat im Jahresvergleich von {earliest_year} - {most_recent_year}")



    # Kantons Dataframe
    st.subheader("Entwicklung Kantone")
    selected_indicator_Ankünfte_Logiernächte_2 = st.selectbox('Auswahl Kennzahl', ["Logiernächte", "Ankünfte"], index=0,key='selected_indicator_Ankünfte_Logiernächte_2')
    grouped_df_kanton = df.groupby(['Date','Monat','Jahr','Kanton']).agg({selected_indicator_Ankünfte_Logiernächte_2: 'sum'}).reset_index()
    grouped_df_kanton = grouped_df_kanton.groupby('Kanton').agg({selected_indicator_Ankünfte_Logiernächte_2: list}).reset_index()
    grouped_df_kanton[f"{selected_indicator_Ankünfte_Logiernächte_2} Total"] = grouped_df_kanton[selected_indicator_Ankünfte_Logiernächte_2].apply(lambda x: sum(x))
    grouped_df_kanton[f"{selected_indicator_Ankünfte_Logiernächte_2} Anteil"] = ((100 / sum(grouped_df_kanton[f"{selected_indicator_Ankünfte_Logiernächte_2} Total"])) * grouped_df_kanton[f"{selected_indicator_Ankünfte_Logiernächte_2} Total"]).apply(lambda x: f"{x:.2f}%")
    grouped_df_kanton.insert(0, "Wappen", grouped_df_kanton['Kanton'].map(kantonswappen))
    grouped_df_kanton = grouped_df_kanton.sort_values(f"{selected_indicator_Ankünfte_Logiernächte_2} Total",ascending=False)

    st.dataframe(
        grouped_df_kanton,
        column_config={
            "Wappen": st.column_config.ImageColumn("Wappen"),
            "Kanton": "Kanton",
            selected_indicator_Ankünfte_Logiernächte_2: st.column_config.LineChartColumn(
                selected_indicator_Ankünfte_Logiernächte_2),
            f"{selected_indicator_Ankünfte_Logiernächte_2} Anteil":st.column_config.ProgressColumn(
        f"{selected_indicator_Ankünfte_Logiernächte_2} Anteil",
            help="% zum Gesamtmarkt",
            min_value=0,
            max_value=1,
        ),
                },
        hide_index=True,
        width='stretch'
    )
    st.caption(f"Abbildung 3: {selected_indicator_Ankünfte_Logiernächte} nach Kanton von {earliest_year} - {most_recent_year}")

    #Gemeinde Dataframe
    st.subheader("Entwicklung Gemeinden")
    grouped_df_gemeinde = df_gemeinde.groupby(['Date','Monat','Jahr','Gemeinde']).agg({selected_indicator_Ankünfte_Logiernächte_2: 'sum'}).reset_index()
    grouped_df_gemeinde = grouped_df_gemeinde.groupby('Gemeinde').agg({selected_indicator_Ankünfte_Logiernächte_2: list}).reset_index()
    grouped_df_gemeinde[f"{selected_indicator_Ankünfte_Logiernächte_2} Total"] = grouped_df_gemeinde[selected_indicator_Ankünfte_Logiernächte_2].apply(lambda x: sum(x))
    grouped_df_kanton[f"{selected_indicator_Ankünfte_Logiernächte_2} Anteil"] = ((100 / sum(grouped_df_gemeinde[f"{selected_indicator_Ankünfte_Logiernächte_2} Total"])) * grouped_df_gemeinde[f"{selected_indicator_Ankünfte_Logiernächte_2} Total"]).apply(lambda x: f"{x:.2f}%")
    grouped_df_gemeinde.insert(0, "Wappen", grouped_df_gemeinde['Gemeinde'].map(gemeindewappen))
    grouped_df_gemeinde = grouped_df_gemeinde.sort_values(f"{selected_indicator_Ankünfte_Logiernächte_2} Total",ascending=False)


    st.dataframe(
        grouped_df_gemeinde,
        column_config={
            "Wappen": st.column_config.ImageColumn("Wappen"),
            "Gemeinde": "Gemeinde",
            selected_indicator_Ankünfte_Logiernächte_2: st.column_config.LineChartColumn(
                selected_indicator_Ankünfte_Logiernächte_2),
            f"{selected_indicator_Ankünfte_Logiernächte_2} Anteil":st.column_config.ProgressColumn(
        f"{selected_indicator_Ankünfte_Logiernächte_2} Anteil",
            help="% zum Gesamtmarkt",
            min_value=0,
            max_value=1,
        ),
                },
        hide_index=True,
        width='stretch'
    )

    st.caption(f"Abbildung 4: {selected_indicator_Ankünfte_Logiernächte} nach Gemeinde von {earliest_year} - {most_recent_year}")






    ##### Herkunftsland Map ####
    st.subheader("Entwicklung nach Herkunftsland")
    selected_indicator_Ankünfte_Logiernächte_3 = st.selectbox('Auswahl Kennzahl', ["Logiernächte", "Ankünfte"], index=0,key='selected_indicator_Ankünfte_Logiernächte_3')


    # Add ISO codes to the country data
    country_totals = df.groupby('Herkunftsland')[selected_indicator_Ankünfte_Logiernächte_3].sum().reset_index()


    iso_codes = []
    for country in country_totals['Herkunftsland']:
        iso_code = country_mapping.get(country)
        iso_codes.append(iso_code)

    country_totals['ISO_Code'] = iso_codes
    # Drop Switzerland from the dataframe
    country_totals = country_totals[country_totals['ISO_Code'] != 'CHE']



    # Generate a custom continuous color scale by interpolating between the base color and white
    color_scale = ['#FAFAFA',primaryColor]

    fig = go.Figure(data=go.Choropleth(
        locations=country_totals['ISO_Code'],
        z=country_totals[selected_indicator_Ankünfte_Logiernächte_3].astype(float),
        colorscale=color_scale ,
        text=country_totals['Herkunftsland'], # hover text
        marker_line_color='white'# line markers between states
    ))


    # Update the map layout
    fig.update_geos(
        showcountries=False,
        showcoastlines=False,
        showland=True,
        showframe=False,
        scope='world',
        landcolor='#FAFAFA'  # Set the land color to light gray
        )
    # Display the map
    #st.plotly_chart(fig,use_container_width = True)

    #st.caption(f"Abbildung 5: {selected_indicator_Ankünfte_Logiernächte} nach Herkunftsland von {earliest_year} - {most_recent_year} (International)")




    # Herkunftsland Dataframee
    grouped_df_Herkunftsland = df.groupby(['Date','Monat','Jahr','Herkunftsland']).agg({selected_indicator_Ankünfte_Logiernächte_3: 'sum'}).reset_index()
    grouped_df_Herkunftsland = grouped_df_Herkunftsland.groupby('Herkunftsland').agg({selected_indicator_Ankünfte_Logiernächte_3: list}).reset_index()
    grouped_df_Herkunftsland[f"{selected_indicator_Ankünfte_Logiernächte_3} Total"] = grouped_df_Herkunftsland[selected_indicator_Ankünfte_Logiernächte_3].apply(lambda x: sum(x))
    grouped_df_Herkunftsland[f"{selected_indicator_Ankünfte_Logiernächte_3} Anteil"] = ((100 / sum(grouped_df_Herkunftsland[f"{selected_indicator_Ankünfte_Logiernächte_3} Total"])) * grouped_df_Herkunftsland[f"{selected_indicator_Ankünfte_Logiernächte_3} Total"]).apply(lambda x: f"{x:.2f}%")
    grouped_df_Herkunftsland.insert(0, "Flagge", grouped_df_Herkunftsland['Herkunftsland'].map(countryflags))
    grouped_df_Herkunftsland = grouped_df_Herkunftsland.sort_values(f"{selected_indicator_Ankünfte_Logiernächte_3} Total",ascending=False)

    
    st.dataframe(
        grouped_df_Herkunftsland,
        column_config={
            "Flagge": st.column_config.ImageColumn("Flagge"),
            "Herkunftsland": "Herkunftsland",
            selected_indicator_Ankünfte_Logiernächte_3: st.column_config.LineChartColumn(
                selected_indicator_Ankünfte_Logiernächte_3),
            f"{selected_indicator_Ankünfte_Logiernächte_3} Anteil":st.column_config.ProgressColumn(
        f"{selected_indicator_Ankünfte_Logiernächte_3} Anteil",
            help="% zum Gesamtmarkt",
            min_value=0,
            max_value=1,
        ),

        },
        hide_index=True,
        width='stretch'
    )
    st.caption(f"Abbildung 5: {selected_indicator_Ankünfte_Logiernächte} nach Herkunftsland von {earliest_year} - {most_recent_year}")

    st.divider()
    st.caption("with :heart: by Hashhiker")




def create_hotels_page(df,selected_Gemeinde):
    #st.title(":flag-ch: Hotellerie Explorer")
    st.title(f"About")
    # Create two columns for metrics and line chart
    # Filter dataframe based on selected Gemeinde
    df = df[df['Ort'] == selected_Gemeinde]
    st.divider()
    st.dataframe(df)
    st.divider()
    fig = px.bar(
        df,
        x='Hotel',
        y='Anzahl_Zimmer_Apartments',
        color='Stars',
        color_discrete_sequence=custom_color_sequence
    )
    # Sort the bars based on the 'Anzahl_Zimmer_Apartments' column in descending order
    fig.update_xaxes(categoryorder='total descending')
    # Sort the legend alphabetically (assuming 'Stars' column contains categorical values)
    fig.update_layout(
        legend=dict(
            traceorder='reversed',
        )
    )
    st.plotly_chart(fig, width='stretch')


    # Drop rows where either latitude or longitude is missing
    df_map = df.dropna(subset=['lat', 'lon'])
    st.dataframe(df)

    st.map(
        df_map,
        latitude='lat',
        longitude='lon',
        color='Stars',
        #size='Anzahl_Zimmer_Apartments'
        )


    # df_map['Hover_Text'] = df_map['Hotel'] + df_map['Ort']



    # fig = px.scatter_mapbox(df_map,
    #                         lat="lat",
    #                         lon="lon",
    #                         color='Stars',  # Use the fixed color for all points
    #                         color_continuous_scale=px.colors.cyclical.IceFire,
    #                         size_max=15,
    #                         text=df_map['Hover_Text'],
    #                         hover_data={'Hover_Text':True,  
    #                                 "lat":False, 
    #                                 "lon":False,
    #                                 },
    #                         zoom=6
    # )
    
    # fig.update_layout(clickmode='event+select',
    #                   mapbox_style="open-street-map",
    #                   mapbox_center={"lat": df_map['lat'].mean(), "lon": df_map['lon'].mean()}
    #                   )

    # # Display the map
    # st.plotly_chart(fig, use_container_width=True)
    st.caption("with :heart: by Hashhiker")


def create_about_page():
    #st.title(":flag-ch: Hotellerie Explorer")
    st.title(f"About")
    # Create two columns for metrics and line chart
    st.divider()
    st.subheader("Kontakt")
    column1, column2 = st.columns(2)
    column1.markdown('<a href="https://github.com/datachalet"><img src="https://i.imgur.com/EbsWGAk.png" alt="Title" width="80px"></a>', unsafe_allow_html=True)
    st.divider()
    st.subheader("Datenquellen")
    st.write('Hotellerie: Ankünfte und Logiernächte der geöffneten Betriebe in 100 Gemeinden nach Jahr, Monat, Gemeinde und Gästeherkunftsland (BFS):')
    st.write('https://www.bfs.admin.ch/asset/de/26465895')
    st.write('Hotellerie: Ankünfte und Logiernächte der geöffneten Betriebe nach Jahr, Monat, Kanton und Gästeherkunftsland (BFS):')
    st.write('https://www.bfs.admin.ch/asset/de/26465893')
    st.write('Hotellerie: Angebot und Nachfrage der geöffneten Betriebe in 100 Gemeinden nach Jahr, Monat und Gemeinde:')
    st.write('https://www.bfs.admin.ch/asset/de/26465894')
    st.divider()
    st.caption("with :heart: by Hashhiker")









#### Globale Datumsvariablen und Update BFS Logik 8 tag im Monat ###########
# Calculate the cutoff date (last day of the month before the previous month
current_date = datetime.date.today()


## if current_date.day < 8:
##cutoff_date = datetime.date(current_date.year, current_date.month - 3, calendar.monthrange(current_date.year, current_date.month - 3)[1])
##else:
##cutoff_date = datetime.date(current_date.year, current_date.month - 2, calendar.monthrange(current_date.year, current_date.month - 2)[1])

if current_date.month > 3:
    cutoff_date = datetime.date(current_date.year, current_date.month - 3, calendar.monthrange(current_date.year, current_date.month - 3)[1])
else:
    cutoff_date = datetime.date(current_date.year - 1, 12 - (3 - current_date.month), calendar.monthrange(current_date.year - 1, 12 - (3 - current_date.month))[1])


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


st.sidebar.title("Swiss Hospitality Explorer")
page = st.sidebar.selectbox("Seitenauswahl:", (
    "Gesamtmarkt Schweiz",
    "Nach Gemeinde", 
    "Nach Gemeinde und Herkunftsland",
    #"Hotels",
    "About"
    ))
st.sidebar.divider() 

#### Auswahl Gemeinde Global
if page == "Nach Gemeinde" or page == "Nach Gemeinde und Herkunftsland" or page == "Hotels":
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

# Apply date filter to df Supply 
df_kanton = df_kanton[(df_kanton['Jahr'] >= start_year) & (df_kanton['Jahr'] <= end_year)]
first_day_actual_month = df_kanton['Date'].max()
if end_date > first_day_actual_month:
    end_date = first_day_actual_month


#### Einstellungen
st.sidebar.divider() 
st.sidebar.write("")
expander = st.sidebar.expander("Custom Colors")
with expander:
    col1, col2, col3, col4, col5 = st.columns(5)
    color1 = col1.color_picker('Main', '#037F8C')
    color2 = col2.color_picker('2nd', '#7ED0D9')
    color3 = col3.color_picker('3rd', '#01A5BD')
    color4 = col4.color_picker('4th', '#F27244')
    color5 = col5.color_picker('5th', '#F28F79')
    color6 = col1.color_picker('6th', '#368c7a')
    color7 = col2.color_picker('7th', '#7CB342')
    color8 = col3.color_picker('8th', '#0C8040')
    color9 = col4.color_picker('9th', '#1ad3aa')
    color10 = col5.color_picker('10th', '#F2B710')
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

primaryColor=color1 #for the map

st.sidebar.divider() 
st.sidebar.caption("with :heart: by Hashhiker")


#### Page Selection

if page == "Nach Gemeinde":
    create_main_page(df_supply,selected_Gemeinde)
elif page == "Nach Gemeinde und Herkunftsland":
    create_other_page(df_country,selected_Gemeinde)
elif page == "Gesamtmarkt Schweiz":
    create_markt_page(df_kanton,df_supply)
# elif page == "Hotels":
#     create_hotels_page(df_hotels,selected_Gemeinde)
elif page == "About":
    create_about_page()

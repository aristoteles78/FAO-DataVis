import pandas as pd
import pycountry

# funktion zum laden und verarbeiten der daten
def load_and_process_data(file_path):
    # laden der daten aus der CSV-Datei
    data_full = pd.read_csv(file_path, encoding='latin1')
    # löschen der spalten 'latitude' und 'longitude'
    data = data_full.drop(columns=['latitude', 'longitude'])

    # manuelle zuordnung von ländernamen zu ISO-Alpha-3-Codes
    manual_country_mapping = {
        'Bolivia (Plurinational State of)': 'BOL',
        'China, Hong Kong SAR': 'HKG',
        'China, Macao SAR': 'MAC',
        'China, mainland': 'CHN',
        'China, Taiwan Province of': 'TWN',
        'Iran (Islamic Republic of)': 'IRN',
        'Republic of Korea': 'KOR',
        'Swaziland': 'SWZ',
        'The former Yugoslav Republic of Macedonia': 'MKD',
        'Turkey': 'TUR',
        'Venezuela (Bolivarian Republic of)': 'VEN',
        'Croatia': 'HRV',
        'Libya': 'LBY',
        'Congo': 'COG',
        'Democratic Republic of the Congo': 'COD',
        'Republic of the Congo': 'COG',
        'Côte d\'Ivoire': 'CIV',
        'Syria': 'SYR',
        'Tanzania': 'TZA'
    }

    # funktion zur abfrage des ländercodes
    def get_country_code(name):
        if name in manual_country_mapping:
            return manual_country_mapping[name]
        try:
            return pycountry.countries.lookup(name).alpha_3
        except LookupError:
            return None

    # anwenden der funktion auf die spalte 'Area' zur erstellung der 'iso_alpha'-spalte
    data['iso_alpha'] = data['Area'].apply(get_country_code)
    # entfernen von zeilen ohne gültigen 'iso_alpha'-wert
    data = data.dropna(subset=['iso_alpha'])

    # umwandeln der daten in ein langes format
    data_melted = data.melt(id_vars=["Area", "iso_alpha", "Item", "Element", "Unit"], 
                            value_vars=[col for col in data.columns if col.startswith('Y')],
                            var_name="Year", value_name="Value")

    # entfernen des führenden 'Y' aus der 'Year'-spalte und umwandeln in integer
    data_melted['Year'] = data_melted['Year'].str[1:].astype(int)

    # berechnung des gesamtwerts und der änderungsrate
    data_melted['TotalValue'] = data_melted.groupby(['Area', 'Year', 'Element'])['Value'].transform('sum')
    data_melted['ChangeRate'] = data_melted.groupby(['Area', 'Element'])['TotalValue'].pct_change()

    # ersatz von unendlichen werten durch nan und entfernen von zeilen mit nan-ändernungsraten
    data_melted['ChangeRate'].replace([float('inf'), -float('inf')], float('nan'), inplace=True)
    data_melted = data_melted.dropna(subset=['ChangeRate'])

    # erstellung eines datenrahmens mit allen jahren von 1962 bis zum maximalen jahr in den daten
    all_years = pd.DataFrame({'Year': range(1962, data_melted['Year'].max() + 1)})

    return data_melted, all_years

# aufruf der funktion zum laden und verarbeiten der daten
data_melted, all_years = load_and_process_data('data/FAO.csv')

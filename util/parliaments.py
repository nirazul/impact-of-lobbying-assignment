# Imports
import pandas as pd


def load_parliaments_data(source_file):
    # Load and insert parliament size meta data
    result = pd.read_excel(
        source_file,
        header=0,
        names=['body_name_raw', 'parliament_size'],
        nrows=26,
        skiprows=[0, 1],
        usecols=[0, 22],
    )

    result["body_name_clean"] = (
        result["body_name_raw"]
        .str.replace("\u00a0", " ", regex=False)  # normalize non-breaking spaces
        .str.replace(r"\s+\d+\)$", "", regex=True)  # remove trailing footnotes like
        .str.strip()  # optional: trim
    )

    result["body_key"] = result["body_name_clean"].map(map_canton_to_short)

    unmapped_bodies = result.loc[
        result["body_key"].isna(),
        "body_name_clean",
    ].unique()

    if len(unmapped_bodies) > 0:
        raise Exception(f'Incomplete body mapping! {unmapped_bodies} could not be mapped')

    result.loc[len(result)] = {
        'body_name_raw': 'Schweiz',
        'body_name_clean': 'Schweiz',
        'body_key': 'CHE',
        'parliament_size': 246,
    }  # adding a row

    return result


def map_canton_to_short(name: str) -> str | None:
    """
    Maps Swiss canton names (German / French / Italian long forms)
    to their official two-letter abbreviations.

    Returns None if no mapping is found.
    """

    canton_map = {
        "Zürich": "ZH",
        "Bern": "BE",
        "Luzern": "LU",
        "Uri": "UR",
        "Schwyz": "SZ",
        "Obwalden": "OW",
        "Nidwalden": "NW",
        "Glarus": "GL",
        "Zug": "ZG",
        "Freiburg": "FR",
        "Solothurn": "SO",
        "Basel-Stadt": "BS",
        "Basel-Landschaft": "BL",
        "Schaffhausen": "SH",
        "Appenzell A. Rh.": "AR",
        "Appenzell I. Rh.": "AI",
        "St. Gallen": "SG",
        "Graubünden": "GR",
        "Aargau": "AG",
        "Thurgau": "TG",
        "Tessin": "TI",
        "Waadt": "VD",
        "Wallis": "VS",
        "Neuenburg": "NE",
        "Genf": "GE",
        "Jura": "JU",
    }

    return canton_map.get(name)

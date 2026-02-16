import pandas as pd

REFERENCE_DATE = pd.Timestamp("2026-01-01")


def order_categories(df: pd.DataFrame) -> pd.DataFrame:
    df["gender"] = (
        df["gender"]
        .astype("category")
        .cat.reorder_categories(["m", "f"], ordered=True)
        .map({"m": 0, "f": 1})
    )
    party_sizes = df["party"].dropna().value_counts()
    ordered_parties = ["Parteilos"] + party_sizes.drop(
        "Parteilos", errors="ignore"
    ).index.tolist()
    df["party"] = (
        df["party"]
        .astype("category")
        .cat.reorder_categories(ordered_parties, ordered=True)
    )

    return df


def get_party_mask(df: pd.DataFrame):
    party_others_threshold = 25
    party_sizes = df["party"].dropna().value_counts()
    big_parties = party_sizes[party_sizes >= party_others_threshold].index
    exceptions = ["Parteilos"]

    return (
        ~df["party"].isin(big_parties)
        & ~df["party"].isin(exceptions)
        & df["party"].notna()
    )


def prepare_regression_analysis(
    df_analysis_by_member: pd.DataFrame,
    df_analysis_by_body: pd.DataFrame,
) -> pd.DataFrame:
    cols_to_drop = [
        "active",
        "lastname",
        "firstname",
        "membership_begin_date",
        "membership_id",
        "party_harmonized",
    ]

    non_disclosing_bodies = df_analysis_by_body.loc[
        df_analysis_by_body["interest_sum"] == 0, "body_key"
    ]

    result = df_analysis_by_member.copy()
    result = result[~result["body_key"].isin(non_disclosing_bodies)]
    result = result[result["gender"].notna()]
    result = result[result["party_harmonized"].notna()]

    result["party"] = result["party_harmonized"]
    result.loc[get_party_mask(result), "party"] = "Other"
    result["admin_level"] = (
        result["body_key"].eq("CHE").astype("int64").replace({1: 1, 0: 2})
    )
    result["tenure_years"] = (
        REFERENCE_DATE - result["membership_begin_date"]
    ) / pd.Timedelta(days=365.25)
    result = result[result["tenure_years"] >= 0]

    result = result.drop(columns=cols_to_drop)
    result = result.reset_index(drop=True)
    result = order_categories(result)

    return result

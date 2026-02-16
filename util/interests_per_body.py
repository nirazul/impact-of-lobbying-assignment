import pandas as pd


def analyze_declarations_by_body(
    df_analysis: pd.DataFrame, df_parliaments: pd.DataFrame
):
    interest_sum_by_body = df_analysis.groupby("body_key")["num_interests"].sum()

    result = df_analysis["body_key"].value_counts()

    result = df_parliaments[["body_key", "parliament_size"]].merge(
        result.to_frame().reset_index(),
        on="body_key",
        how="left",
    )
    result["person_diff"] = result["count"] - result["parliament_size"]
    result["interest_sum"] = result["body_key"].map(interest_sum_by_body)

    return result

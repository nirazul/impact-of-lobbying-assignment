import pandas as pd


def get_filter_mask(df: pd.DataFrame):
    return (
        (df["body_key"] != "LIE")
        & (df["membership_end_date"].isna())
        & (
            (
                ~(df["body_key"].isin(["GE", "NE", "LU", "VS", "ZG", "ZH"]))
                & (df["membership_type_harmonized_oparl_id"] == 10)
            )
            | (
                (df["body_key"] == "GE")
                & (df["membership_type_harmonized_oparl_id"] == 10)
                & (df["function_latest"].isin(["Député", "Députée"]))
            )
            | ((df["body_key"] == "NE") & (df["function_latest"] == "Député-e"))
            | (
                (df["body_key"] == "VS")
                & (df["function_latest"].isin(["Abgeordnete", "Abgeordneter"]))
            )
            | ((df["body_key"].isin(["LU", "ZG", "ZH"])) & (df["active"] == True))
        )
    )


def prepare_interests(df_members: pd.DataFrame):
    cols_as_int64 = ["interest_id"]
    cols_to_drop = [f"interest_name.{l}" for l in ["de", "fr", "it"]] + [
        "active",
        "gender",
        "interests_list",
        "interest_person_id",
        "party_harmonized",
        "memberships_list",
        "website_parliament_url",
    ]

    result = df_members.explode("interests_list")

    data = pd.json_normalize(result["interests_list"].to_list()).add_prefix("interest_")
    result = result.reset_index(drop=True).join(data)

    result[cols_as_int64] = result[cols_as_int64].astype("Int64")

    result["interest_name"] = (
        result[[f"interest_name.{l}" for l in ["de", "fr", "it"]]]
        .bfill(axis=1)
        .iloc[:, 0]
    )

    result = result.drop(columns=cols_to_drop)

    return result


def analyze_declarations_by_member(
    df_memberships: pd.DataFrame,
    df_interests: pd.DataFrame,
    df_parliaments: pd.DataFrame,
):
    cols_to_drop = [
        "function_latest",
        "membership_active",
        "membership_end_date",
        "membership_group_id",
        "membership_type_harmonized_oparl_id",
    ]

    interest_counts = (
        df_interests.dropna(subset=["interest_id"])  # real interests only
        .loc[df_interests["body_key"] != "VD"]  # VD has declaration docs
        .groupby("id", as_index=False)
        .agg(num_interests=("interest_id", "nunique"))
    )

    result = df_memberships.copy()
    result = result[get_filter_mask(result)]
    result = result.drop_duplicates(
        subset=["firstname", "lastname", "membership_begin_date"],
        keep="last",
    )
    result = result.drop_duplicates(
        subset=["id"],
        keep="last",
    )
    result = result.merge(
        interest_counts,
        on="id",
        how="left",
        validate="many_to_one",
    )
    result = result.merge(
        df_parliaments[["body_key", "parliament_size"]],
        on="body_key",
        how="left",
        validate="many_to_one",
    )

    result["num_interests"] = result["num_interests"].fillna(0).astype("int64")

    result = result.drop(columns=cols_to_drop)
    result = result.reset_index(drop=True)

    return result

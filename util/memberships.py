import pandas as pd


def prepare_memberships(df_members: pd.DataFrame):
    cols_to_drop = ["interests_list", "memberships_list", 'website_parliament_url']
    cols_as_int64 = ["membership_id", "membership_group_id", "membership_type_harmonized_oparl_id"]
    cols_as_timestamp = ["membership_begin_date", "membership_end_date"]

    result = df_members.explode("memberships_list")
    data = pd.json_normalize(result["memberships_list"].to_list()).add_prefix("membership_")

    result = result.reset_index(drop=True).join(data)

    result[cols_as_int64] = result[cols_as_int64].astype("Int64")
    result[cols_as_timestamp] = result[cols_as_timestamp].apply(
        pd.to_datetime,
        format="%Y-%m-%d",
        errors="coerce",
    )

    result = result.drop(columns=cols_to_drop)

    return result

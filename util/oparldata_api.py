import requests


def get_bodies():
    parameters = {
        "indexed": "true",
        "type": ",".join(["canton", "country", "city"]),
        "fields": ",".join(["body_key"]),
    }

    response = requests.get("https://api.openparldata.ch/v1/bodies/", params=parameters)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_persons(body_key: str):
    parameters = {
        "limit": "1000",
        "body_key": body_key,
        "active": "true",
        "expand": ",".join(["interests", "memberships"]),
        "sort_by": "lastname",
        "fields": ",".join(
            [
                "active",
                "body_key",
                "gender",
                "id",
                "firstname",
                "lastname",
                "party_harmonized",
                "website_parliament_url",
                "function_latest",
                "interests.body_key",
                "interests.declaration_doc_url",
                "interests.id",
                "interests.person_id",
                "interests.name",
                "memberships.id",
                "memberships.group_id",
                "memberships.active",
                "memberships.begin_date",
                "memberships.end_date",
                "memberships.name",
                "memberships.type_harmonized_oparl_id",
            ],
        ),
    }

    response = requests.get(
        "https://api.openparldata.ch/v1/persons/", params=parameters
    )

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_groups():
    parameters = {
        "type_harmonized_id": "10",  # Legislative Council
        "expand": ",".join([]),
    }

    response = requests.get("https://api.openparldata.ch/v1/groups/", params=parameters)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def check_parliament_membership_group_type_id(person_data: dict, membership_type_id: int) -> bool | None:
    memberships_obj = person_data.get('memberships')

    if not isinstance(memberships_obj, dict) or not memberships_obj:
        return None

    memberships_list = memberships_obj.get('data')

    if not isinstance(memberships_list, list) or not memberships_list:
        return None

    for membership in memberships_list:
        if not isinstance(membership, dict):
            continue

        if membership.get('type_harmonized_oparl_id') == membership_type_id:
            return True

    return False


def check_parliament_membership_group_id(person_data: dict, membership_id: int) -> bool | None:
    memberships_obj = person_data.get('memberships')

    if not isinstance(memberships_obj, dict) or not memberships_obj:
        return None

    memberships_list = memberships_obj.get('data')

    if not isinstance(memberships_list, list) or not memberships_list:
        return None

    for membership in memberships_list:
        if not isinstance(membership, dict):
            continue

        if membership.get('group_id') == membership_id:
            return True

    return False

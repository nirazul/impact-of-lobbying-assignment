from typing import Mapping, Optional

LANG_ORDER = ("de", "fr", "it", "en")


def get_lang(obj: Mapping[str, str]) -> Optional[str]:
    for lang in LANG_ORDER:
        value = obj.get(lang)

        if value:
            return value

    return None

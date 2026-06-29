def is_tax_legal_event(title: str) -> bool:

    title = title.lower()

    # ❌ explicit rejects (education / admin / systems)
    reject_keywords = [
        "mam dochody",
        "jak rozliczyć",
        "co to jest",
        "e-toll",
        "krajowy plan odbudowy",
        "polski ład",
        "audyt",
        "kontrola zarządcza",
        "formularz",
        "wniosek",
        "rejestracja",
        "program",
        "system",
        "instrukcja"
    ]

    if any(k in title for k in reject_keywords):
        return False

    # ✔ legal triggers
    legal_keywords = [
        "ustawa",
        "nowelizacja",
        "zmiana ustawy",
        "dz. u",
        "ordynacja podatkowa",
        "vat",
        "cit",
        "pit",
        "interpretacja",
        "wyrok",
        "tsue",
        "projekt ustawy",
        "minister finansów",
        "mf",
        "rcl"
    ]

    return any(k in title for k in legal_keywords)

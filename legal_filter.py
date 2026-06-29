def relevance_score(title: str) -> int:

    t = title.lower()
    score = 0

    # CORE TAX LAW SIGNALS
    if any(x in t for x in ["vat", "cit", "pit", "akcyza"]):
        score += 3

    if any(x in t for x in ["ustawa", "nowelizacja", "projekt", "zmiana ustawy"]):
        score += 3

    if any(x in t for x in ["interpretacja", "mf", "dyrektor", "krajowa informacja skarbowa"]):
        score += 2

    if any(x in t for x in ["wyrok", "tsue", "nsa", "wsa"]):
        score += 2

    if any(x in t for x in ["prawo.pl", "rp.pl", "isap", "rcl"]):
        score += 1

    # NEGATIVE FILTER (EDUCATION / ADMIN)
    if any(x in t for x in [
        "jak rozliczyć",
        "mam dochód",
        "co to jest",
        "instrukcja",
        "formularz",
        "e-toll",
        "polski ład",
        "kpo",
        "program"
    ]):
        score -= 10

    return score


def is_valid_tax_event(title: str) -> bool:
    return relevance_score(title) >= 3

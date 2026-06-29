def format_newsletter(items):

    blocks = []

    for n in items:

        title = n.get("title", "")

        what = n.get("what_changed", "")
        impact = n.get("impact", "")
        basis = n.get("legal_basis", "")
        source = n.get("source", "")
        url = n.get("url", "")

        text = f"""
🟢 {title}

Co się zmienia:
{what}

Znaczenie podatkowe:
{impact}

Podstawa prawna:
{basis}

Źródło: {source}
{url}
"""

        blocks.append(text)

    return "\n\n" + ("\n\n" + "-"*60 + "\n\n").join(blocks)

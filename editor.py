def format_newsletter(items):

    blocks = []

    for n in items:

        block = f"""
🟢 {n.title}

📌 Co się zmienia:
{n.what_changed}

📊 Znaczenie podatkowe:
{n.impact}

⚖️ Podstawa prawna:
{n.legal_basis}

🔗 Źródło: {n.source}
{n.url}
"""

        blocks.append(block)

    return "\n\n" + ("\n\n" + "-"*60 + "\n\n").join(blocks)

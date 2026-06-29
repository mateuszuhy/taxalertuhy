def format_newsletter(items):

    output = []

    for n in items:

        block = f"""
🟢 {n.get('title','')}

📌 Co się zmienia:
{n.get('what_changed','')}

📊 Znaczenie podatkowe:
{n.get('impact','')}

⚖️ Podstawa prawna:
{n.get('legal_basis','')}

🔗 Źródło: {n.get('source','')}  
{n.get('url','')}
"""

        output.append(block)

    return "\n\n" + ("\n\n" + "-"*60 + "\n\n").join(output)

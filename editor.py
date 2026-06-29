def write_newsletter(items):

    output = []

    for n in items:

        text = f"""
🟢 {n['title']}

Zmiana:
{n['summary']['what_changed']}

Znaczenie podatkowe:
{n['summary']['impact']}

Podstawa prawna:
{n['summary']['legal_basis']}

Źródło: {n.get('url', 'N/A')}
"""

        output.append(text)

    return "\n\n---\n\n".join(output)

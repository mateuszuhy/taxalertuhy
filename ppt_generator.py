from pptx import Presentation


def create_ppt(items):

    prs = Presentation()

    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "UHY TAX ALERT V5.2"

    for n in items:

        slide = prs.slides.add_slide(prs.slide_layouts[1])

        slide.shapes.title.text = n.title

        content = f"""
{n.what_changed}

{n.impact}

{n.legal_basis}

Źródło: {n.source}
{n.url}
"""

        slide.placeholders[1].text = content

    path = "output/tax_alert.pptx"
    prs.save(path)

    return path

import os
from pptx import Presentation


def create_ppt(data):

    os.makedirs("output", exist_ok=True)

    prs = Presentation()

    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "UHY TAX ALERT – V3.6"

    for n in data.get("lead", []):

        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = n.get("title", "")
        slide.placeholders[1].text = "\n\n".join(n.get("summary", []))

    for n in data.get("standard", []):

        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = n.get("title", "")
        slide.placeholders[1].text = "\n\n".join(n.get("summary", []))

    path = "output/tax_alert.pptx"
    prs.save(path)

    return path

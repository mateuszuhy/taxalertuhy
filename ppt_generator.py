import os
from pptx import Presentation


def create_ppt(data):

    os.makedirs("output", exist_ok=True)

    prs = Presentation()

    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "UHY TAX ALERT – POLAND"

    for n in data.get("lead", []):

        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = n.get("title", "Tax news")

        text = "\n\n".join(n.get("summary", []))
        slide.placeholders[1].text = text

    for n in data.get("standard", []):

        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = n.get("title", "Tax update")

        text = "\n\n".join(n.get("summary", []))
        slide.placeholders[1].text = text

    path = "output/tax_alert.pptx"
    prs.save(path)

    return path

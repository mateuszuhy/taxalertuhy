import os
from pptx import Presentation


def create_ppt(data):

    os.makedirs("output", exist_ok=True)

    prs = Presentation()

    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "UHY TAX ALERT – V4 (LEGAL INTELLIGENCE)"

    def add(slide_data):

        for n in slide_data:

            slide = prs.slides.add_slide(prs.slide_layouts[1])
            slide.shapes.title.text = n.get("title", "")

            text = "\n\n".join(n.get("summary", []))

            if n.get("url"):
                text += f"\n\nŹRÓDŁO: {n['url']}"

            slide.placeholders[1].text = text

    add(data.get("lead", []))
    add(data.get("standard", []))

    path = "output/tax_alert.pptx"
    prs.save(path)

    return path

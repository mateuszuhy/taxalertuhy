from pptx import Presentation


def create_ppt(data):

    prs = Presentation()

    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "UHY Tax Alert V3.3"

    for n in data["lead"]:

        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = n["title"]
        slide.placeholders[1].text = "\n".join(n["summary"])

    for n in data["standard"]:

        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = n["title"]
        slide.placeholders[1].text = "\n".join(n["summary"])

    prs.save("output/tax_alert.pptx")

from pptx import Presentation

def create_ppt(data):

    prs = Presentation()

    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "UHY Tax Alert V3.2"

    for n in data["lead"]:

        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = "LEAD NEWS"
        slide.placeholders[1].text = n["title"]

    for n in data["standard"]:

        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = "STANDARD NEWS"
        slide.placeholders[1].text = n["title"]

    prs.save("output/tax_alert.pptx")

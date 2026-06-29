from pptx import Presentation

def create_ppt(data):

    prs = Presentation()

    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "UHY Tax Alert – AI Engine"

    for item in data["lead"]:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = "LEAD NEWS"
        slide.placeholders[1].text = str(item)

    prs.save("output/tax_alert.pptx")

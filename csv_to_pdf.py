"""
downloaded from http://code.activestate.com/recipes/123612-basedoctemplate-with-2-pagetemplate/
"""
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, NextPageTemplate, PageBreak, PageTemplate
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

styles = getSampleStyleSheet()
Elements = []

doc = BaseDocTemplate('animeworld.pdf', showBoundary=1)


def foot1(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 19)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()


def foot2(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()


def create_pdf(texts):
    # Two Columns
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width / 2 - 6, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin + doc.width / 2 + 6, doc.bottomMargin, doc.width / 2 - 6,
                   doc.height, id='col2')

    Elements.append(NextPageTemplate('TwoCol'))
    Elements.append(Paragraph(texts, styles['Normal']))
    doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame1, frame2], onPage=foot2),
                          ])
    # start the construction of the pdf
    doc.build(Elements)


if __name__ == '__main__':
    df = pd.read_csv('Anime world _2018_09_23 20_18.csv')
    texts = ''
    print('loaded data')
    for index, row in df.iterrows():
        texts += '{}, {}: \n{}\n'.format(row['Date'], row['UserName'], row['MessageBody'])
    print('data prepared to text')
    create_pdf(texts)
    print('created pdf')

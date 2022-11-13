import aspose.words as aw
#pip install aspose-words
doc = aw.Document('ViewPDF.aspx')
          
for page in range(0, doc.page_count):
    extractedPage = doc.extract_pages(page, 1)
    extractedPage.save(f"output/Output_{page + 1}.png")
"""
Parse the database and transform the pdf to txt. 
Dependency: PDFMiner
- Needs a path to the dataset
- Assume .pdf files

TODO: need to add a button to not duplicate the work if the txt exists
"""

import os
import os.path
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator
from utils import Config, get_pdf_filepaths


def extract_txt(pdf_file):
    """
  This function uses PDFMiner library to parse the pdf and get the text.
  We are making sure that the line read has more letters than other junky characters. This avoids all sorts of tables abd arxive markings that are not needed.  
  """

    txt_file = pdf_file + '.txt'
    password = ""
    extracted_text = ""

    fp = open(pdf_file, "rb")
    parser = PDFParser(fp)
    document = PDFDocument(parser, password)

    # Check if document is extractable, if not abort
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    rsrcmgr = PDFResourceManager()

    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                tmp = lt_obj.get_text()  # get the text line in the box

                # see if we have mostly characters and not some junk characters and only then add the line
                nr_char = 0.0
                total_char = 0.0
                for ch in tmp:
                    total_char += 1.0
                    if ch.isalpha():
                        nr_char += 1.0
                # add the line with a lot of characters not some junky staff from the pdf
                if nr_char / total_char > 0.7:
                    # print(nr_char/total_char, tmp)
                    extracted_text += tmp

    fp.close()

    if Config.overwrite_txt == 1:
        if not os.path.isfile(txt_file):
            with open(txt_file, "w") as my_log:
                my_log.write(extracted_text.encode("utf-8"))
    else:
        with open(txt_file, "w") as my_log:
            my_log.write(extracted_text.encode("utf-8"))


def pdf2txt(path):
    files = get_pdf_filepaths(path)
    for f in files:
        print(f)
        extract_txt(f)


### MAIN

pdf2txt(Config.dataset_dir)
print("Done all files!")

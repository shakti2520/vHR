import PyPDF2 as pdf
import nltk
import re
def main():
    obj = open('D:\\Resume.pdf','rb')
    opdf = pdf.PdfFileReader(obj)
    print(opdf)
    page0 = opdf.getPage(0)
    text = page0.extractText()
    #print(text)
    lines = [el.strip() for el in text.split("\n") if len(el)>0]
    #print(lines)
    lines = [nltk.word_tokenize(el) for el in lines]
    
    lines = [nltk.pos_tag(el) for el in lines]
    print(lines)
    instiregex = r'INSTI: {<DT.>?<NNP.*>+<IN.*>?<NNP.*>?}'
    #print(instiregex)
main()
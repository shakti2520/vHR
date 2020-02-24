from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import spacy
from spacy.matcher import Matcher
import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import datefinder

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as fh:
        # iterate over all pages of PDF document
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            # creating a resoure manager
            resource_manager = PDFResourceManager()
            
            # create a file handle
            fake_file_handle = io.StringIO()
            
            # creating a text converter object
            converter = TextConverter(
                                resource_manager, 
                                fake_file_handle, 
                                codec='utf-8', 
                                laparams=LAParams()
                        )

            # creating a page interpreter
            page_interpreter = PDFPageInterpreter(
                                resource_manager, 
                                converter
                            )

            # process current page
            page_interpreter.process_page(page)
            
            # extract text
            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()

# calling above function and extracting text\

nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    #print(nlp_text)
    # First name and Last name are always Proper Nouns
    pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]
    
    matcher.add('NAME', None, pattern)
    
    matches = matcher(nlp_text)
    #print(matches)
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        #print(start,"    ",end)
        return span.text


def extract_mobile_number(resume_text):
    nlp_text = nlp(resume_text)
    pattern = [{"POS":"NUM"}]
    matcher.add('NUM', None, pattern)
    matches = matcher(nlp_text)
    for match_id, start, end in matches:
        if str(nlp_text[start:end]).isnumeric():
            span = nlp_text[start:end]
            return span.text

def extract_email(email):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

# load pre-trained model
nlp = spacy.load('en_core_web_sm')
def extract_skills(resume_text):
    nlp_text = nlp(resume_text)
#     for char in nlp_text:
#         print(char, "   ",char.pos_)
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    
    # reading the csv file
    data = pd.read_csv("D:\\vHR\\skills.csv") 
#     print(data)
    # extract values
    skills = list(data.columns.values)
    
    skillset = []
    nlp_text = nlp(resume_text)
    pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]
    pattern2 = [{"POS": "PROPN"}]
    matcher = Matcher(nlp.vocab)
    matcher.add('SKILL1', None, pattern)
    matcher.add('SKILL2', None, pattern2)
    span = []
    matches = matcher(nlp_text)
    #print(matches)
    for match_id, start, end in matches:
        span.append(nlp_text[start:end]) 
    
    
    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    
    # check for bi-grams and tri-grams (example: machine learning)
    for token in span:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

def extract_experience(resume):
    buf = io.StringIO(resume)
    year2 = []
    year = []
    line = buf.readline()
    while line != "":
        years = re.findall("([A-Z][a-z]+\s[0-9][0-9][0-9][0-9]|[a-z]+\s[0-9][0-9][0-9][0-9])", line)
        if len(years)==2:
            year2.append(years)
        line = buf.readline()
    exp = 0
    for x in year2:
        y = []
        for i in x:
            match = datefinder.find_dates(i)
            for m in match:
                y.append(m.date())
        year.append(y)
#     print(year)
    diff_year = []
    for y in year:
        diff = y[0]-y[1]
        exp = exp + diff.days
        diff_year.append(round((abs(diff.days)/28)/12,1))
    print(diff_year)
    total_exp = round((abs(exp)/28)/12,1)
    experience = { "list_exp": diff_year,
                   "total_exp":total_exp
                 }
    return experience

STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII',
            'BCA', 'MCA', 'B.COM', 'M.COM', 'B.SC', 'M.SC',
            'B.OPTO', 'M.OPTO', 'BBA', 'MBA'
        ]

def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]

    education = []
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                education.append(tex)
    return education

def fetch_all_details(path):
    # calling above function and extracting text\
    text = ''
    #for page in extract_text_from_pdf('D:\\python\\resume parser\\samples\\OmkarResume.pdf'):
    for page in extract_text_from_pdf(path):
        text += ' ' + page
    skills = extract_skills(text)
    
    return skills
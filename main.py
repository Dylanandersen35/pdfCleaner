import os
import pdfplumber
import re
import nltk
from nltk.corpus import words


directory = "./data"


def is_bold(fontname):
    return 'Bold' in fontname


def removable_fonts(word):
    """
    Helper function for removing words in all caps. Only useful for specific documents
    :param word: Each word from the pdf
    :return: A boolean value for if the word matches the font name
    """
    return 'Arial-BoldMT' in word['fontname'] or 'Symbol' in word['fontname']


def remove_caps(words):
    """
    Removes words in all caps if removable_fonts returns true
    :param words: The text extracted from the pdf
    :return: A new list of words with the words in all caps removed
    """
    remove_pattern = r'\b[A-Z0-9]+\b'
    updated_words = []

    for word in words:
        if removable_fonts(word):
            new_text = re.sub(remove_pattern, '', word['text'])
            word['text'] = new_text
        updated_words.append(word)

    return updated_words


def remove_bullet_points(page_text):
    """
    Removes bullet points from the text and makes them a part of the preceding paragraph
    :param page_text: The text from the pdf
    :return: A new text with the bullet points removed
    """
    patterns = [
        r'•\s+',  # Standard bullet points
        # r'[\-\–\—]\s+',  # Dash used as bullets
        r'\b\d+\.\s+',  # Single level numbers like "1.", "2.", etc.
        r'\b(\d+\.)+\s+',  # Multi-level numbers like "1.1.", "2.1.1", etc.
        r'\b[A-Za-z]\.\s+',  # Alphabetical bullets like "A.", "b.", etc.
        r'\(\d+\)\s+',  # Numbers in parentheses like "(1)", "(22)", etc
        r'\b\([a-zA-Z]\)\b'  # Letters in parentheses like "(a)", "(B)", etc
    ]

    for pattern in patterns:
        page_text = re.sub(pattern, '', page_text)

    return page_text


def remove_chapters(page_text):
    """
    Removes the chapter headings
    :param page_text: The text from the pdf
    :return: A new text with the chapter headings removed
    """
    pattern = r'\b(CHAPTER\s\d+.*)(\n)\b'

    page_text = re.sub(pattern, r'\2', page_text)

    return page_text


def remove_sections(page_text):
    """
    Removes the section headings
    :param page_text: The text from the pdf
    :return: A new text with the section headings removed
    """
    pattern = r'\b(SECTION\s\d+.*)(\n)\b'

    page_text = re.sub(pattern, r'\2', page_text)

    return page_text


def remove_decimal_pattern(page_text):
    """
    Removes the decimal patterns that each paragraph begins with. Creates a newline when
    it is the start of the paragraph or removes entirely if it is within a paragraph.
    :param page_text: The text from the pdf
    :return: A new text with the decimal patterns removed or a newline character added
    """
    patterns = [
        r'\b\d+(\.\d+)+\b\s([A-Z][a-z]+)',  # For "1.2.3.4 Apple"
        r'\[([A-Z]+)\]\s\b\d+(\.\d+)+\b\s([A-Z][a-z]+)',  # For "[XYZ] 1.2.3.4 Apple"
        r'\[([A-Z])\]\s\b\d+(\.\d+)+\b\s([A-Z][a-z]+)',  # For "[X] 1.2.3.4 Apple"
        r'\[\]\s\b\d+(\.\d+)+\b\s([A-Z][a-z]+)',
        r'[A-Z]\b\d+(\.\d+)+\b\s([A-Z][a-z]+)'  # For "A1.2.3.4 Apple"
    ]

    for pattern in patterns:
        page_text = re.sub(pattern, r'\n\2', page_text)

    page_text = re.sub(r'\[]\s\.', '\n', page_text)  # In case the capital letter in the bracket gets removed first
    page_text = re.sub(r'\[]\s', '\n', page_text)

    remove_patterns = [
        r'\bSection\s\d+(\.\d+)+\b',
        r'\bSection\s[A-Z]\d+\b',
        r'\bSections\s\d+(\.\d+)+\b',
        r'\bSections\s[A-Z]\d+\b',
        r'\bSection\s\d+\b',
        r'\bSections\s\d+\b',
        r'\bTable\s\d+\b',
        r'\bTable\s[A-Z]\d+\b',
        r'\bTable\s\d+(\.\d+)+\b',
        r'\bTables\s\d+(\.\d+)+\b',
        r'\bTable\s\d+(\.\d+)+\([a-zA-Z]\)\b',
        r'\bTables\s[A-Z]\d+(\.\d+)+\b',
        r'\bTable\s\d+(\.\d+)+\([\d+]\)\b',
        r'\bTable\s\d+(\.\d+)+\([\d+]\)\.\b',
        r'\bTable\s\d+\.\d+\([\d+]\)\.\b',
        r'\bTable\s[A-Z]\d+(\.\d+)+\([a-zA-Z]\)\b',
        r'\bTables\s[A-Z]\d+(\.\d+)+\([a-zA-Z]\)\b',
        r'\bTables\s\d+(\.\d+)\([a-zA-Z0-9]\)\b',
        r'\bTables\s\d+(\.\d+)\(\d\)\b',
        r'\bFigure\s\d+(\.\d+)+\([a-zA-Z]\)\b',
        r'\bFigures\s\d+(\.\d+)+\([a-zA-Z]\)\b',
        r'\bFigures\s\d+(\.\d+)+\(\d+\)\b',
        r'\bFigures\s\d+(\.\d+)+\b',
        r'\[([A-Z]+)]\s\b\d+(\.\d+)+\b',
        r'[A-Z]\s\b\d+(\.\d+)+\b',
        r'\b\d+(\.\d+)+\([a-zA-Z]\)\b',
        r'\d+\.\d+\(\d+\)',
        r'\.\d+\(\d+\)',
        r'\d+\.',
        r'\d+(\.\d+)+\.',
        r'\(\d+\)\,',
        r'\(\)',
        r'\-\d+',
        r'\d+(\-\d+)+',
        r'\[[A-Z]\]',
        r'\[BF\]',
        r'\[BS\]',
        r'\[BG\]',
        r'\[FG\]'
    ]

    for pattern in remove_patterns:
        page_text = re.sub(pattern, '', page_text)

    return page_text


# Loads in a large set of English words
nltk.download('words')
word_list = set(words.words())  # Load the set of English words

# Can continue to add to this list for words we find are not in the nltk set of English words
word_list.update(['connections', 'approved', 'conveys', 'including', 'applications', 'feasibility', 'provisions',
                  'enlargements', 'specified', 'performed', 'sections', 'nationally', 'discharges', 'terminating',
                  'rainwater', 'controlled', 'consisting', 'containing', 'standards', 'materials', 'systems', 'located',
                  'compartments', 'inspectors', 'individuals', 'witnessed', 'assemblies', 'discharged', 'neutralized',
                  'polypropylene', 'prohibited', 'persons', 'facilities', 'products', 'fraternities', 'applying',
                  'customers', 'occupancies', 'employees', 'conforming', 'substances', 'applied', 'hydraulic', 'labeled',
                  'temperatures', 'requirements', 'instructions', 'conditioning', 'connected', 'exchangers', 'urinals',
                  'submeters', 'mixing', 'conveying', 'installed', 'devices', 'additives', 'occupants', 'elements',
                  'functioning', 'located', 'semicontinuous', 'maintained', 'conditions', 'machines', 'processes',
                  'methods', 'fixtures', 'lavatories', 'installations', 'computed', 'projected', 'surfaces', 'nonpotable',
                  'cesspools', 'chapters', 'components', 'constructed', 'recommendations', 'required', 'producing',
                  'demands', 'imparts', 'operations', 'nationally', 'cross-connected', 'trowel-applied'])


def process_hyphenated_words(page_text):
    """
    Uses the updated version of the nltk word_list to verify if words need to be hyphenated
    or not
    :param page_text: The text from the pdf
    :return: A new text with the correct hyphenated words
    """
    # page_text = re.sub(r'-\s*\n\s*', '-', page_text)
    page_text = re.sub(r'\b-\s\b', '-', page_text)

    # Function to process each word
    def process_word(match):
        word_with_hyphen = match.group(0)
        word_without_hyphen = word_with_hyphen.replace('-', '')
        # Check if the word without hyphen exists in the English word list
        if word_without_hyphen.lower() in word_list:
            return word_without_hyphen
        else:
            return word_with_hyphen
    # Regex to find words with hyphens
    return re.sub(r'\b\w+(-\w+)+\b', process_word, page_text)


def normalize_text(page_text):
    """
    Normalizes words from the text so that the AI will not establish different interpretations
    for the same words.
    :param page_text: The text from the pdf
    :return: A new text with the normalized words
    """
    # Can continue to add to this dictionary as we find more words that we want to keep constant
    word_map = {
        r'\bbuilt\s+up\b': 'built-up',
        r'\bbuiltup\b': 'built-up',
    }

    for pattern, replacement in word_map.items():
        page_text = re.sub(pattern, replacement, page_text, flags=re.IGNORECASE)

    return page_text


# Add to keep_words if another method of removing capital words is needed
# Ensures words/acronyms in the text do not get removed
keep_words = ["HVAC", "NFPA", "PVC", "CPVC", "PVDF", "PE-RT", "ANSI", "ASSP", "UL", "CSST", "AWG", "CSA", "LC", "ASTM",
              "ASME", "ABS", "MSS", "MP", "CGA", "LP", "NGV", "RFA", "CNG", "VFA", "I", "II", "III", "IV", "VI", "NA", "NAT",
              "FAN", "MAX", "MIN", "FEMA", "NOAA", "NM", "NMC", "NMS", "SECTION"]


def process_text(file_path):
    """
    Processes the pdf file and performs the necessary actions on the text
    :param file_path: The path to the pdf file
    :return: A new, cleaned version of the text
    """
    all_text = ''
    # Use keep_pattern if keep_words is needed, as mentioned above
    # keep_pattern = r'\b(?:' + '|'.join(keep_words) + r')\b'
    with (pdfplumber.open(file_path) as pdf):
        for page in pdf.pages:
            words = page.extract_words(extra_attrs=['fontname'])
            # words = remove_caps(words)
            page_text = ' '.join(word['text'] for word in words)
            page_text = process_hyphenated_words(page_text)
            page_text = remove_decimal_pattern(page_text)
            page_text = remove_chapters(page_text)
            page_text = remove_sections(page_text)
            page_text = remove_bullet_points(page_text)
            page_text = normalize_text(page_text)
            all_text += page_text + ' '
    return all_text


def load_pdf(dir):
    documents =[]
    for filename in os.listdir(dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            text = process_text(file_path)
            documents.append(text)
    return documents


def list_fonts(path):
    """
    Lists the fonts used in the pdf file. Only needs to be used if new changes are made
    for the program
    :param path: Path to the pdf file
    :return: A list of the font names used in the pdf
    """
    with pdfplumber.open(path) as pdf:
        font_sets = set()
        for page in pdf.pages:
            for char in page.chars:
                font_sets.add(char['fontname'])
    return font_sets

# path = 'data/2015_IMC.pdf'
# fonts = list_fonts(path)
# print(fonts)


documents = load_pdf(directory)
print(documents)

# PDF Text Processing
This project is focused on extracting and cleaning text from PDF files using the pdfplumber library in Python. The code performs various text processing tasks such as removing unwanted characters, normalizing text, and handling hyphenated words.

## Features
- Bold Font Detection: Identifies bold fonts in the text.
- Caps Removal: Removes words in all caps based on specific fonts.
- Bullet Point Removal: Removes bullet points and integrates them with the preceding paragraph.
- Chapter and Section Removal: Removes chapter and section headings.
- Decimal Pattern Removal: Removes decimal patterns and adjusts text formatting.
- Hyphenated Word Processing: Handles hyphenated words and verifies them against a word list.
- Text Normalization: Normalizes specific words to maintain consistency.
- Font Listing: Lists fonts used in the PDF file.

## Setup
#### 1. Clone the repository:

`git clone <repository-url>`

`cd <repository-directory>`

#### 2. Install the required libraries:

`pip install -r requirements.txt`

## Usage
#### 1. Prepare the Data Directory:
Place your PDF file in the data directory.

#### 2. Run the Text Processing:

`from main.py import load_pdf`

`directory = "./data"`

`documents = load_pdf(directory)`

`print(documents)`

#### 3. List Fonts (Optional):
To list all fonts used in a PDF file:

`from main.py import list_fonts`

`path = 'data/your_pdf_file.pdf'`

`fonts = list_fonts(path)`

`print(fonts)`

## Additional Information
- For our purposes, copy and paste the text into Word and use find and replace on '\n' to replace all occurences with a paragraph mark (^p)
- The script uses an extended word list to ensure proper processing of hyphenated words; add to this list as needed.
- Specific words/acronyms can be maintained to avoid unintended removals.
- The project can be extended by adding more patterns and words to the existing lists and dictionaries.

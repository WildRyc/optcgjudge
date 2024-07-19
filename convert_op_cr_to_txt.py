import PyPDF2
import re
import os
import sys

# This script attempts to convert the One Piece Rule Comprehensive PDF to a text file
# Based on https://www.geeksforgeeks.org/convert-pdf-to-txt-file-using-python/

version_number = ''
last_updated = ''

def pdf_to_text(pdf_path, output_text):
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string
        text = ''
        # Iterate over all the pages
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pageText = page.extract_text()
            # find the version number on the first page
            if page_num == 0:
                global version_number 
                version_number = find_document_version(pageText)
                global last_updated
                last_updated = find_document_last_updated(pageText)

            # Remmove the page numbers. They should be a number followed by a new line
            pageText = re.sub(r'\n\d\n', '', pageText)
            # Go over the text, and remove new line characters unless the next line begins with a number
            # This should clean up the "pdf paragraph" problem
            pageText = re.sub(r'\n(?!\d)', ' ', pageText)
            # On the first page, find the version number and date last updated
            if page_num == 0:
                # Find the second line with "1. Game Overview"
                gameOverviewIndex = pageText.find('1. Game Overview', 1)
                # If the line is found, remove everything before it
                pageText = pageText[gameOverviewIndex:]
                
                
            text += pageText

        
    # Write the text to a file
    with open(output_text, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

def quality_check(output_text):
    # Check if the first line of the text file is correct
    with open(output_text, 'r', encoding='utf-8') as text_file:
        first_line = text_file.readline()
        print('First line of the text file', first_line);

    # Check if the page numbers have been removed by finding 1-2-3 at the start of a line
        # for line in text_file:
        #     if re.match('^1-2-3', line):
        #         print('Page numbers have not been removed')
        #         break
        #     else:
        #         print('Page numbers have been removed')

    # Check if the version number has been found
    if version_number == '':
        print('No version number found')
    else:    
        print('Version number:', version_number)
    
    # Check when last updated
    if last_updated == '':
        print('No date last updated found')
    else:
        print('Date last updated:', last_updated)

def find_document_version(text):
    # catch the version number in the format Version x.x.x
    match = re.search(r'Version\s(\d.+\b)\s+Last', text)
    version = match.group(1) if match else 'VERSION_NOT_FOUND'
    version = re.sub(r'\s', '', version)
    return version

def find_document_last_updated(text):
    # catch the date in the format dd/mm/yyyy, but it might be missing a digit and may have extra spaces in the year
    match = re.search(r'Last\supdated:\s(\d{1,2}\/\d\d\/\d.*?\d.*?\d.*?\d.*?)', text)
    updated = match.group(1) if match else 'UPDATED_NOT_FOUND'
    # ditch the spaces
    updated = re.sub(r'\s', '', updated)
    return updated

if __name__ == '__main__':
    print('Converting One Piece Rule Comprehensive PDF to text')
    file_name = sys.argv[1]
    output_text = 'one_piece_rule_comprehensive.txt'
    pdf_to_text(file_name, output_text)
    file_rename = 'One_Piece_Rule_Comprehensive_v_' + version_number + '.txt'
    # check if a file with file_rename already exists
    if os.path.exists(file_rename):
        print('File already exists. Deleting', file_rename)
        os.remove(file_rename)
    os.rename(output_text, file_rename)
    print('Text extracted from PDF file and saved to', file_rename)
    quality_check(file_rename)



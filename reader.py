import os
import io
import requests
from PyPDF2 import PdfReader

keywords = 'medicine'
File = 'journals.uokerbala.edu.iq-PDFs.txt'
file = open(f'C:\\Users\\mhmda\\Desktop\\Scraper029\\Pdf list per site\\{File}')
PDF_links = []
Detected_PDF_link= []
links = file.readlines()
rps = []

for link in links:
    PDF_links.append(link)
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}


while len(PDF_links)>0:
    try:
        url = PDF_links.pop()
        req = requests.get(url.replace('\n',''),headers=headers)
        # req = requests.get('https://phcfm.org/index.php/phcfm/article/download/2047/3573',headers=headers)
        file = io.BytesIO(req.content)
        print(url)
        reader = PdfReader(file)
        Pages = reader.getNumPages()
        Detected = False
        for x in range(0,Pages):
            contents = reader.getPage(x).extract_text()
            if keywords in contents.lower():
                Detected = True

        if Detected == True:
        
            Detected_PDF_link.append(url)
            print(f'\n{len(Detected_PDF_link)} PDFs detected.')
            # Detected_title.append(Title_name[count])
        print(f'{len(PDF_links)} PDFs not scanned yet')
    except Exception as e:
        if 'SSL' in str(e):
            print('need SSL certificate for this website!')
        else:
            print(e)
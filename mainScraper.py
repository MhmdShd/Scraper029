
from time import sleep
import io
import requests
from PyPDF2 import PdfReader
import datetime
from bs4 import BeautifulSoup

articles = []
keywords = 'test'
websites = open(f'C:\\Users\\mhmda\\Desktop\\Scraper029\\sitestoscan.txt')
sites = websites.readlines()

# for site in sites:
#     articles.append(site)


def scrapeStructure_A(page, main): # requests
    soup = parse(page)
    for volume in soup.find_all('a'):
        if 'Volume ' in  volume.text:
            Volume_links.append(main + volume['href'].replace('./',''))
            print(main + volume['href'].replace('./',''))
    print(f'\n\nGathered {len(Volume_links)} Volumes')
    while len(Volume_links) > 0:
        soup = parse(Volume_links.pop())
        links = soup.find_all('a')
        for link in links:
            if 'issue_' in link['href']:
                Issues_links.append(main + link['href'].replace('./',''))
                print(main + link['href'].replace('./',''))
        print(f'\n{len(Volume_links)} Volumes left')
    print(f'\n\nGathered {len(Issues_links)} Issues')
    while len(Issues_links) > 0:
        soup = parse(Issues_links.pop())
        links = soup.find_all('a')
        for link in links:
            if '.pdf' in link['href']:
                PDF_links.append(main + link['href'].replace('./',''))
                print(main + link['href'].replace('./',''))
        print(f'\n{len(Issues_links)} Issues left')
    print(f'\n\nGathered {len(PDF_links)} PDFs')
    print('bruuuuuuuuuuuuuuh')

def scrapeStructure_B(page,main): # requests
    PDF_Page = []
    global Issues_links, PDF_links
    res = requests.get(page)
    soup = BeautifulSoup(res.text,'html.parser')
    Issues = soup.find_all('a',{'title':'Table of Contents'})
    for x in Issues:
        Issues_links.append(main + x['href'])
        print(main + x['href'])
    print(f'Gathered {len(Issues_links)} Issues')

    while len(Issues_links) > 0:
        issue = Issues_links.pop()
        res = requests.get(issue)
        soup = BeautifulSoup(res.text,'html.parser')
        links = soup.find_all('a',text = '[PDF]')
        for link in links:
            PDF_Page.append(main + link['href'])
            print(main + link['href'])
        print(f'{len(Issues_links)} Issues left\n\n')
        
    print(f'\n\nGathered {len(PDF_Page)} PDF pages\n')


    while len(PDF_Page) > 0:
        page = PDF_Page.pop()
        res = requests.get(page)
        soup = BeautifulSoup(res.text,'html.parser')
        links = soup.find_all('a')
        for link in links:
            if '.pdf' in link['href']:
                PDF_links.append(main + link['href'])
                print(main + link['href'])
        print(f'{len(PDF_Page)} Pages left\n\n')
        
    print(f'\n\nGathered {len(PDF_Page)} PDF links\n')

def scrapeStructure_C(page,main): # requests
    stat= True
    try:
        soup = parse(page,stat)
    except Exception as e:
        if 'SSL' in str(e):
            ans = input('Error while parsing website, do you want to disable SSL verification? (y/n): ')
            if ans.lower() == 'y':
                soup = parse(page,False)
                stat = False
            else:
                print("Program terminated manually!")
                raise SystemExit
    Prev_driver = main + soup.find('a',{'class':'previous'})['href']
    Next_driver = main + soup.find('a',{'class':'next'})['href']
    while Prev_driver != None:        
        soup = parse(Prev_driver)
        C_getPDFs(soup)
        try:
            Prev_driver = main +soup.find('a',{'class':'previous'})['href']
        except:
            Prev_driver = None
    print('\nno more previous version')
    while Next_driver != None:
        soup = parse(Next_driver)
        C_getPDFs(soup)
        try:
            Next_driver = main + soup.find('a',{'class':'next'})['href']
        except:
            Next_driver = None
    print('\nno more next versions')
def C_getPDFs(soup):
    links = soup.find_all('a')
    for link in links:
        try:
            href = link['href']
            if 'article/abstract' in href.lower() or 'article/fulltext' in href.lower() and link['class'].lower() != 'blocklink':
                PDF = href.replace('FullText','PDF')
                PDF = href.replace('Abstract','PDF')
                if 'Abstract' not in PDF:
                    PDF_links.append(main+PDF)
                    print(f'{len(PDF_links)} PDFs Gathered')
        except:
            pass

def scrapeStructure_D(page,main): # requests
    global Issues_links
    soup = parse(page)
    temp = []
    temp = findAttrintarget(Issues_links,'a','/pdf/','href','href',main)
    for link in temp:
        PDF_links.append(link+'.pdf')
    Issues_links.append(main + soup.find('a',{'data-test':'next-page'})['href'][1:])
    while len(Issues_links) > 0:
        soup = parse(Issues_links[0])
        temp = findAttrintarget(Issues_links,'a','/pdf/','href','href',main)
        for link in temp:
            PDF_links.append(link+'.pdf')
        try:
            Issues_links.append(main + soup.find('a',{'data-test':'next-page'})['href'][1:])
        except:
            pass
        print(f'gathered {len(PDF_links)} PDFs in this volume.')

def scrapeStructure_E(page,main): # requests
    global PDF_links
    Volume_links = E_getVolumes(page,main)
    PDF_links = findAttrintarget(Volume_links,'a','.pdf','href','href',main)
def E_getVolumes(page,main,stat=True):
    try:
        soup = parse(page,stat)
    except Exception as e:
        if 'SSL' in str(e):
            ans = input('Error while parsing website, do you want to disable SSL verification? (y/n): ')
            if ans.lower() == 'y':
                soup = parse(page,False)
                stat = False
            else:
                print("Program terminated manually!")
                raise SystemExit
    volumes = []
    links = soup.find_all('a')
    for link in links:
        if 'Vol. ' in link.text:
            volumes.append(main+link['onclick'].split("','")[0].replace("window.open('",''))
            print(f'{len(volumes)} Volumes gathered')
    return volumes

def scrapeStructure_F(page,main=''): # requests
    global res
    soup = parse(page)
    container = soup.find('div',{'class':'entry-content'})
    for link in container.find_all('a'):
        print(link['href'])
        if 'http://' in link['href'] and 'https://' in link['href']:
            Issues_links.append(link['href'].replace('http://',''))
        else:
            Issues_links.append(link['href'])
    print(len(Issues_links))

    for issue in Issues_links:
        print('\n'+issue)
        soup = ''
        while soup == '':
            try:
                soup = parse(issue)
            except :
                print('Error parsing page, retrying in 10 second:\n')
                sleep(10)
        container = soup.find('div',{'class':'entry-content'})
        print('\nGetting real PDF link')
        for link in container.find_all('a'):
            try:
                print(link['href'])
                PDF_links.append(link['href'])
            except:
                pass

    links = PDF_links.copy()
    PDF_links.clear()
    for link in links:
        try:
            res = requests.get(link).url
            if '.pdf' in res:
                    print(res)
                    PDF_links.append(res)
        except:
            print(f'Error in URL: {link}')

def scrapeStructure_G(page,main=''): # requests
    global Volume_links,Issues_links,PDF_links
    pages = []
    pages.append(page)
    Volume_links = findAttrintarget(pages,'a','/volume','href','href',main)
    print(f'{len(Volume_links)} Volumes')
    Issues_links_temp = findAttrintarget(Volume_links,'a','issue_','href','href',main)
    for link in Issues_links_temp:
        if len(link) < 70:
            Issues_links.append(link)
    print(f'{len(Issues_links)} Issues')
    PDF_links = findAttrintarget(Issues_links,'a','.pdf','href','href', main)
    print(f'{len(PDF_links)} PDFs')

def scrapeStructure_H(page,main=''): # requests
    global PDF_links
    soup = parse(page)
    issues_section = soup.find('div',{'class':'kcite-section'})
    for link in issues_section.find_all('a',{'title':''}):
        Issues_links.append(link['href'])
        print(f'{len(Issues_links)} issues gathered')
    PDF_links = findAttrintarget(Issues_links,'a','.pdf','href','href',main)
    
def scrapeStructure_I(page,main): # requests
    soup = parse(page)
    div = soup.find('div',{'class':'cat-children'})
    for link in div.find_all('a'):
        Issues_links.append(main + link['href'])
    print(f'{len(Issues_links)} Issues gathered')
    I_getPDFs(main)
def I_getPDFs(main):
    global PDF_links
    PDF_pages = []
    PDFs = []
    while len(Issues_links) > 0:
        soup = parse(Issues_links.pop())
        for link in soup.find_all('td',{'class':'list-title'}):
            PDF_pages.append(main + link.find('a')['href'])
            print(main + link.find('a')['href'])
    PDF_links = findAttrintarget(PDF_pages,'a','.pdf','href','href',main)

def scrapeStructure_J(page, main): # requests
    global Issues_links
    Issues_links = findAttrintarget(findElemintargetByPartialText([page],'a','Volume ','href',main),'a','','href','href',main)
    J_getPDFs(main)
def J_getPDFs(main):
    temp_PDF_pages,temp_PDF_links,PDF_Pages = [],[],[]
    global PDF_links
    while len(Issues_links) > 0:
        issue = Issues_links.pop()
        if 'Size' not in issue:
            issue += '?pageSize=100&page=1'
        soup = parse(issue)
        main_div = soup.find('div',{'class':'issue-listing'})
        # links = main_div.find_all('a')
        for link in main_div.find_all('a'):
            if '/jemtac.' in link['href'] and 'doi.org' not in link['href']:
                try:
                    temp_PDF_pages.append(main + link['href'])
                    print(main + link['href'])
                except:
                    pass
    PDF_Pages = list(dict.fromkeys(temp_PDF_pages))
    print(f'Gathered a total of {len(PDF_Pages)} PDFs pages')

    while len(PDF_Pages) > 0:
        sleep(1)
        soup = parse(PDF_Pages.pop())
        form = soup.find('form',{'class':'ft-download-content__form--pdf'})
        try:
            temp_PDF_links.append(main + form['action'])
            print(main + form['action'])
        except:
            pass
    PDF_links = list(dict.fromkeys(temp_PDF_links))
    print(f'Gathered a total of {len(PDF_links)} PDFs')

def scrapeStructure_K(page,main =''): # requests
    Volume_links_temp =[]
    global Volume_links
    soup = parse(page)
    for link in soup.find('div',{'class':'_3R-H1'}).find_all('a'):
        try:
            Volume_links_temp.append(link['href'])
            print(link['href'])
        except:
            pass
    Volume_links = list(dict.fromkeys(Volume_links_temp))
    print(f'Gathered a total of {len(Volume_links)} Volumes')
    K_getPDFs()
def K_getPDFs():
    PDF_Pages_temp =[]
    PDF_Pages =[]
    global PDF_links
    while len(Volume_links)>0:
        soup = parse(Volume_links.pop())
        for link in soup.find('div',{'class':'_3K7uv'}).find_all('a'):
            try:
                PDF_Pages_temp.append(link['href'])
                print(link['href'])
            except:
                pass
        print(f'{len(Volume_links)} not scanned yet')
    PDF_Pages = list(dict.fromkeys(PDF_Pages_temp))
    print(f'Gathered {len(PDF_Pages)} PDF Pages')
    # get pdf links form pages
    PDF_links = findAttrintarget(PDF_Pages,'a','_files','href','href')
    print(f'Gathered a total of {len(PDF_links)} PDFs')

def scrapeStructure_L(page,main): # requests
    global Issues_links,PDF_links
    Issues_links = findAttrintarget([page],'a','--vol','href','href',main)
    PDF_links = findElemintargetByPartialText(Issues_links,'a','Download','href',main)

def scrapeStructure_M(page,main = ''): # requests
    soup = parse(page)
    volumes = soup.find_all('a')
    Abstract_links =[]
    for volume in volumes:
        if 'ajpp/archive/' in volume['href'].lower():
            Volume_links.append(main + volume['href'])
            print(volume['href'])
    print(f'Gathered a total of {len(Volume_links)} Volumes')
    Issues_links = findAttrintarget(Volume_links,'a','AJPP/edition','href','href',main)
    Abstract_links = findAttrintarget(Issues_links,'a','article-abstract','href','href',main)
    for abstract in Abstract_links:
        PDF_links.append(main + abstract.replace('abstract','full-text-pdf'))
        print(abstract.replace('abstract','full-text-pdf'))

def scrapeStructure_N(page,main=''): # requests
    global Abstracts, Abstracts_link, Issues_links, PDF_links
    Issues_links = findAttrintarget([page],'a','issue/view','href','href',main)
    temp = Issues_links.copy()
    Abstracts_link = findAttrintarget(Issues_links,'a','article/view','href','href',main)
    PDF_links = findAttrintarget(temp,'a','obj_galley_link','class','href',main)
    Abstract_links_temp = Abstracts_link.copy()
    print(len(PDF_links))
    print(len(Abstracts_link))
    while len(Abstract_links_temp)>0:
        soup = parse(Abstract_links_temp.pop())
        try:
            Abstracts.append(soup.find('section',{'class','item abstract'}).text.lower())
            print(f'Gathered {len(Abstracts)} Abstracts!')
        except:
            pass

def scrapeStructure_O(page,main =''): # requests
    Issues_links_temp = []
    Volume_links = findElemintargetByPartialText([page],'a','Volume ','href',main)
    while len(Volume_links)>0:
        soup = parse(Volume_links.pop())
        Issues_links_temp = findAttrintarget(Volume_links,'a','abstract','hef','href',main)
        Issues_links.extend(Issues_links_temp)
        print(f'{len(Issues_links)} Issues gathered in total.')
    while len(Issues_links)>0:
        link = Issues_links.pop()
        soup = parse(link)
        Abstracts_link.append(link)
        Abstracts.append(soup.find('div',{'id':'abstracts'}).text)

def scrapeStructure_P(main): # requests

    global PDF_links
    #  Old Archives Pages 
    #  Only full issue pdf is available
    #  Should add page in which the API was detected
    
    Issues_links.extend(['http://www.mejfm.com/Archives%202014%20-%202016.htm','http://www.mejfm.com/Archives%20June%202003-December%202013.htm','http://www.mejfm.com/archive.htm'])
    PDF_links = findAttrintarget(Issues_links,'a','.pdf','href','href',main)

def scrapeStructure_Q(page): # requests
    global Issues_links, PDF_links
    PDF_Pages = []
    print('ez')
    soup = parse(page)
    Issues_links_temp=soup.find_all('a',{'class':'theme-button'})
    for issue in Issues_links_temp:
        Issues_links.append(issue['href'].replace('https','http'))

    print(f'\n\ngathered a total of {len(Issues_links)} Issues')

    while len(Issues_links) > 0:
        issue = Issues_links.pop()
        soup = parse(issue)
        main_div = soup.find('div',{'class':'single-blog-content entry clr'})
        links = main_div.find_all('a')
        for link in links:
            if 'anafrimed.net' in link['href']:
                PDF_Pages.append(link['href'].replace('https','http'))
                print(link['href'].replace('https','http'))
        print(f'\n\n{len(Issues_links)} issues left')
    Issues_links = list(dict.fromkeys(PDF_Pages))


    print(f'\n\ngathered a total of {len(Issues_links)} PDF Pages')


    print('\n\nNow getting PDF links')
    while len(Issues_links) > 0:
        issue = Issues_links.pop()
        print(issue)
        soup = parse(issue)
        try:
            link = soup.find('a',{'class':'download-link'})
            print(link['href'].replace('https','http'))
            PDF_links.append(link['href'].replace('https','http'))
        except:
            pass

# joker functions
def keywordScan():
    if len(PDF_links) != 0:
        print('started API scan on PDFs')
        while len(PDF_links)>0:
            url = PDF_links.pop()
            req = requests.get(url)
            file = io.BytesIO(req.content)
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

            print(f'\n\n{len(PDF_links)} PDFs not scanned yet')
            
    if len(Abstracts) != 0:
        while len(Abstracts)>0:
            text = Abstracts.pop()
            link_abstract = Abstracts_link.pop()
            if keywords.lower() in text:
                Detected_Abstract_link.append(link_abstract)
                print(f'\n{len(Detected_Abstract_link)} Abstracts detected.')
                # Detected_title.append(Title_name[count])
            print(f'\n\n{len(Abstracts)} Abstracts not scanned yet')
def scrapeRequests(page,main,issueTag,issueTxtSearch,issueattrSearch,IssueTargetAttr,PDfTag,PDFTxtSearch,PDFattrSearch,PDFTargetAttr,stat=True):
            global Volume_links, Issues_links,PDF_links
            Volume_links.append(page)
            Issues_links = findAttrintarget(Volume_links,issueTag,issueTxtSearch,issueattrSearch,IssueTargetAttr,main)
            PDF_links = findAttrintarget(Issues_links,PDfTag,PDFTxtSearch,PDFattrSearch,PDFTargetAttr,main)   
def parse(url,stat=True):
    payload = {}
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://www.iasj.net/iasj/journal/180/issues',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
        }

    print('\nparsing')
    res = requests.get(url, verify=stat ,headers=headers, data=payload)
    return BeautifulSoup(res.text,'html.parser')
def findAttrintarget(pages,tag,text,attr,target,main='',stat=True):
    result = []
    print(f'\nscanning through {len(pages)} targets')
    while len(pages) > 0:
        url = pages.pop()
        try:
            soup = parse(url,stat)
        except Exception as e:
            if 'SSL' in str(e):
                ans = input('Error while parsing website, do you want to disable SSL verification? (y/n): ')
                if ans.lower() == 'y':
                    soup = parse(url,False)
                    stat = False
                else:
                    print("Program terminated manually!")
                    raise SystemExit
            else:
                print('unexpected error occured')
                raise SystemExit
        print(url)
        for link in soup.find_all(tag):
            try:
                if link[attr] != None and link[target] != None:
                    if text in link[attr]:
                        if link[target].startswith('.') or link[target].startswith('/') :
                            print(main + link[target][1:])
                            result.append(main + link[target][1:])
                        else:
                            print(main + link[target])
                            result.append(main + link[target])
            except:
                pass
        print(f'{len(pages)} Targets left.')
    return list(dict.fromkeys(result))
def findElemintargetByPartialText(pages, tag,text, target,main =''):
    result = []
    for page in pages:
        soup = parse(page)
        for link in soup.find_all(tag):
            if text in link.text:
                try:
                    print(main + link[target])
                    result.append(main + link[target])
                except:
                    pass
    return list(dict.fromkeys(result))


errors = open('ErrorLogs.txt','w')
article = input('Journal to be scanned (URL): ')
year = input('Year span (xxxx-xxxx) - not available yet: ')

# for article in articles:

Issues_links = []
Volume_links = []
PDF_links = []
Title_name = []
Detected_title = []
Detected_PDF_link = []
Detected_Abstract_link = []
Abstracts_link = []
Abstracts = []
article = article.replace(' ','')
print(article)
file = ''

if 'journals.ekb.eg' in article:
    if 'bfpc' in  article:
        archives_page = 'https://bfpc.journals.ekb.eg/'
        scrapeStructure_G(archives_page,'https://bfpc.journals.ekb.eg/')
        file = open("bfpc.journals.ekb.eg.txt",'w')
    else:
        if 'ajps' in article:
            archives_page = 'https://ajps.journals.ekb.eg/'
            file = open("ajps.journals.ekb.eg.txt",'w')
            main = 'https://ajps.journals.ekb.eg/'
        if 'ebwhj' in article:
            archives_page = 'https://ebwhj.journals.ekb.eg/'
            file = open("ebwhj.journals.ekb.eg.txt",'w')
            main = 'https://ebwhj.journals.ekb.eg/'
        if 'aeji' in article:
            archives_page = 'https://aeji.journals.ekb.eg'
            file = open("aeji.journals.ekb.eg.txt",'w')
            main = 'https://aeji.journals.ekb.eg/'
        scrapeStructure_A(archives_page, main)
if '.asp' in article: # PDF links needs to be updated every x hours - links always changing.
    if 'ljmsonline' in article:
        archives_page = 'https://www.ljmsonline.com/backissues.asp'
        main= 'https://www.ljmsonline.com/'
        file = open('www.ljmsonline.com.txt','w')
    if 'epj.eg.net' in article:
        archives_page = 'https://www.epj.eg.net/backissues.asp'
        main= 'https://www.epj.eg.net/'
        file = open('www.epj.eg.net.txt','w')
    if 'egyptretinaj' in article:
        archives_page = 'https://www.egyptretinaj.com/backissues.asp'
        main = 'https://www.egyptretinaj.com/'
        file = open('www.egyptretinaj.com.txt','w')
    if 'jeos.eg.net' in article:
        archives_page = 'https://www.jeos.eg.net/backissues.asp'
        main = 'https://www.jeos.eg.net/'
        file = open('www.jeos.eg.net.txt','w')
    if 'ejdv.eg.net' in article:
        archives_page = 'https://www.ejdv.eg.net/backissues.asp'
        main = 'https://www.ejdv.eg.net/'
        file = open('www.ejdv.eg.net.txt','w')
    if 'hamdanjournal' in article:
        archives_page = 'https://www.hamdanjournal.org/backissues.asp'
        main = 'https://www.hamdanjournal.org/'
        file = open('www.hamdanjournal.org.txt','w')
    if 'medjbabylon' in article:
        archives_page = 'https://www.medjbabylon.org/backissues.asp'
        main = 'https://www.medjbabylon.org/'
        file = open('www.medjbabylon.org.txt','w')
    if 'mmjonweb' in article:
        archives_page = 'https://www.mmjonweb.org/backissues.asp'
        main = 'https://www.mmjonweb.org/'
        file = open('www.mmjonweb.org.txt','w')
    scrapeStructure_B(archives_page,main)
if 'www.easpublisher.com/journal' in article:
    if 'easjms' in article: # done
        archives_page ='https://www.easpublisher.com/journal/easjms/archives'
        file = open('www.easpublisher.com-easjms.txt','w')
    if 'easjacc' in article:
        archives_page ='https://www.easpublisher.com/journal/easjacc/archives'
        file = open('www.easpublisher.com-easjacc.txt','w')
    if 'easjop' in article:
        archives_page ='https://www.easpublisher.com/journal/easjop/archives'
        file = open('www.easpublisher.com-easjop.txt','w')
    if 'easjpp' in article:
        archives_page ='https://www.easpublisher.com/journal/easjpp/archives'
        file = open('www.easpublisher.com-easjpp.txt','w')
    if 'easms' in article:
        archives_page ='https://www.easpublisher.com/journal/easms/archives'
        file = open('www.easpublisher.com-easms.txt','w')
    main = 'https://www.easpublisher.com/'
    scrapeRequests(archives_page,main,'a','issue-box','class','href','a','.pdf','href','href')
if 'saudijournals.com' in article:
    if 'sjmps/' in article:
        archives_page = 'https://saudijournals.com/journal/sjmps/archives'
        file = open('www.saudijournals.com-sjmps.txt','w')
    if 'sjbr/' in article:
        archives_page = 'https://saudijournals.com/journal/sjbr/archives'
        file = open('www.saudijournals.com-sjbr.txt','w')
    if 'sjm/' in article:
        archives_page ='https://saudijournals.com/journal/sjm/archives'
        file = open('www.saudijournals.com-sjm.txt','w')
    if 'sjls/' in article:
        archives_page ='https://saudijournals.com/journal/sjls/archives'
        file = open('www.saudijournals.com-sjls.txt','w')
    scrapeRequests(archives_page,main,'a','issue-box','class','href','a','.pdf','href','href')
if 'amj' in article or 'iphr' in article or 'bjsrg' in article:
    if 'amj' in article:
        archives_page = 'https://amj.uoanbar.edu.iq/'
        file = open('amj.uoanbar.edu.iq.txt','w')
        main = 'https://amj.uoanbar.edu.iq/'
    if 'iphr' in article:
        archives_page = 'https://iphr.mosuljournals.com/'
        file = open('iphr.mosuljournals.com.txt','w')
        main = 'https://iphr.mosuljournals.com/'
    if 'bjsrg' in article:
        archives_page = 'https://bjsrg.uobasrah.edu.iq/'
        file = open('bjsrg.uobasrah.edu.iq.txt','w') 
        main = 'https://bjsrg.uobasrah.edu.iq/'
    scrapeRequests(archives_page,main,'a','/issue_','href','href','a','.pdf','href','href')
if 'www.iasj.net' in article: # Not switched to requests - first page is dynamic
    if '14135' in article or '180' in article:
        archives_page = 'https://www.iasj.net/iasj/journal/180/issues'
        file = open('www.iasj.net-14135.txt','w')
    if '13883' in article or '260' in article:
        archives_page = 'https://www.iasj.net/iasj/journal/260/issues'
        file = open('www.iasj.net-13883.txt','w')
    main = 'https://www.iasj.net/'
    # scrapeStructure('href','iasj/issue','target','_blank',1,driver)
    payload = {}
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://www.iasj.net/iasj/journal/180/issues',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
        }
    res = requests.request("POST", 'https://www.iasj.net/iasj/issuesList/c202463a220f3ea2', headers=headers, data=payload)
    soup = BeautifulSoup(res.text,'html.parser')
    scrapeRequests(archives_page,main,'a','iasj/issue','href','href','a','pdf','href','href')
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        PDF_links.append(link.replace('pdf','download'))
if 'batnajms' in article:
    archives_page = 'https://batnajms.net/2019/11/archives-de-la-revue/'
    file = open('batnajms.net.txt','w')
    main = 'https://batnajms.net/'
    scrapeStructure_F(archives_page,main)
if 'journals.ju' in article:
    if 'JJPS' in article:
        archives_page = 'http://journals.ju.edu.jo/JJPS/issue/archive'
        file = open('journals.ju.edu.jo-JJPS.txt','w')
    if 'JMJ' in article:
        archives_page = 'http://journals.ju.edu.jo/JMJ/issue/archive'
        file = open('journals.ju.edu.jo-JMJ.txt','w')
    scrapeRequests(archives_page,'','a','issue/view','href','href','a','target=_blank','href','href')
if 'www.karger.com/' in article:
    archives_page = 'https://www.karger.com/Journal/Issue/281490'
    main = 'https://www.karger.com/'
    file = open('www.karger.com.txt','w')
    scrapeStructure_C(archives_page,main)
if 'springeropen' in article:
    if 'ejb' in article:
        archives_page='https://ejb.springeropen.com/articles'
        Issues_links.append('https://ejb.springeropen.com/articles')
        file = open('ejb.springeropen.com.txt','w')
        main='https://ejb.springeropen.com/'
    if 'ejim' in article:
        archives_page='https://ejim.springeropen.com/articles'
        Issues_links.append('https://ejim.springeropen.com/articles')
        file = open('ejim.springeropen.com.txt','w')
        main = 'https://ejim.springeropen.com/'
    scrapeStructure_D(archives_page,main) 
if 'www.journal-jmsr.net/' in article:
    archives_page = 'https://www.journal-jmsr.net/archives.php'
    file = open('www.journal-jmsr.net.txt','w')
    main = 'https://www.journal-jmsr.net/'
    scrapeStructure_E(archives_page,main)   
if 'lsj.cnrs.edu.lb' in article:
    archives_page = 'https://lsj.cnrs.edu.lb/archives/'
    file = open('lsj.cnrs.edu.lb.txt','w')
    main = 'https://lsj.cnrs.edu.lb/'
    scrapeStructure_H(archives_page,main)  
if 'bahrainmedicalbulletin' in article:
    archives_page = 'https://www.bahrainmedicalbulletin.com/previousisues.html'
    main = 'https://www.bahrainmedicalbulletin.com/'
    file = open('www.bahrainmedicalbulletin.com.txt','w')
    scrapeRequests(archives_page,main,'a','issue_','href','href','a','.pdf','href','href')
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        PDF_links.append(link.replace(' ','%'))
if 'mchandaids' in article:
    archives_page = 'http://mchandaids.org/index.php/IJMA/issue/archive'
    file = open('mchandaids.org.com-IJMA.txt','w')
    main = ''
    scrapeRequests(archives_page,main,'a','cover','class','href','a','obj_galley_link','class','href')
    print(f'{len(PDF_links)}')
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        soup = parse(link)
        PDF_links.append(soup.find('a',{'class','download'})['href'])
        print(f'gathered {len(PDF_links)} PDFs')
if 'journalskuwait.org' in article:
    archives_page = 'https://journalskuwait.org/kjs/index.php/KJS/issue/archive'
    file = open('journalskuwait.org-KJS.txt','w')
    main = ''
    scrapeRequests(archives_page,main,'a','issue/view','href','href','a','obj_galley_link','class','href')
    print(f'{len(PDF_links)}')
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        soup = parse(link)
        PDF_links.append(soup.find('a',{'class','download'})['href'])
        print(f'gathered {len(PDF_links)} PDFs')
if 'mjemonline.com' in article:
    archives_page = 'https://www.mjemonline.com/index.php/mjem/issue/archive'
    file = open('www.mjemonline.com.txt','w')
    main = ''
    scrapeRequests(archives_page,main,'a','issue/view','href','href','a','btn-primary','class','href')
    print(f'{len(PDF_links)}')
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        soup = parse(link)
        for link in soup.find_all('a'):
            if 'download' in link['href']:
                PDF_links.append(link['href'])
                print(f'gathered {len(PDF_links)} PDFs')
if 'ljmr.com' in article:
    archives_page = 'http://www.ljmr.com.ly/index.php?option=com_content&view=category&id=27&Itemid=167'
    file = open('www.ljmr.com.ly.txt','w', encoding="utf-8")
    main = 'http://www.ljmr.com.ly/'
    scrapeStructure_I(archives_page,main)
if 'uomustansiriyah' in article:
    archives_page = 'https://ajps.uomustansiriyah.edu.iq/index.php/AJPS/issue/archive'
    file = open('ajps.uomustansiriyah.edu.iq.txt','w')
    main = ''
    scrapeRequests(archives_page,main,'a','issue/view','href','href','a','obj_galley_link','class','href')
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        soup = parse(link)
        PDF_links.append(soup.find('a',{'class','download'})['href'])
        print(f'gathered {len(PDF_links)} PDFs')
if 'uobaghdad' in article:
    if 'jkmc' in article:
        archives_page = 'https://jkmc.uobaghdad.edu.iq/index.php/MEDICAL/issue/archive'
        file = open('jkmc.uobaghdad.edu.iq.txt','w')
    if 'bijps' in article:
        archives_page = 'https://bijps.uobaghdad.edu.iq/index.php/bijps/issue/archive'
        file = open('bijps.uobaghdad.edu.iq.txt','w')
    main = ''
    scrapeRequests(archives_page,main,'a','issue/view','href','href','a','obj_galley_link','class','href')
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        soup = parse(link)
        try:
            PDF_links.append(soup.find('a',{'class','download'})['href'])
            print(f'gathered {len(PDF_links)} PDFs')
        except:
            pass   
if 'mbmj.org' in article:
    archives_page = 'https://www.mbmj.org/index.php/ijms/issue/archive'
    file = open('www.mbmj.org.txt','w')
    main = ''
    scrapeRequests(archives_page,main,'a','issue/view','href','href','a','btn-primary','class','href')
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        soup = parse(link)
        for link in soup.find_all('a'):
            try:
                if 'download' in link['href']:
                    PDF_links.append(link['href'])
                    print(f'gathered {len(PDF_links)} PDFs')
            except:
                pass
if 'qscience.com' in article:
    archives_page = 'https://www.qscience.com/content/journals/jemtac/2022/4'
    file = open('www.qscience.com.txt','w')
    main = 'https://www.qscience.com/'
    scrapeStructure_J(archives_page,main)
if 'rmsjournal.org/' in article:# Not switched to requests - missing: going to multi pages inside the issue
    archives_page = 'http://rmsjournal.org/Archive.aspx'
    file = open('rmsjournal.org.txt','w')
    # scrapeStructure('href','articles.aspx','href','.pdf',0,driver)
if 'www.annalsofafricansurgery' in article:
    archives_page ='https://www.annalsofafricansurgery.com/past-publications'
    file = open('www.annalsofafricansurgery.com.txt','w')
    Volume_links.append('https://www.annalsofafricansurgery.com/current-issue') # current issue is not present in past issues page
    scrapeStructure_K(archives_page)
if 'jomenas.org' in article:
    archives_page = 'https://www.jomenas.org/home.html'
    file = open('www.jomenas.org.com.txt','w')
    main = 'https://www.jomenas.org/'
    scrapeStructure_L(archives_page,main)
if 'gssrr.org' in article:
    archives_page = 'https://gssrr.org/index.php/JournalOfBasicAndApplied/issue/archive'
    file = open('gssrr.org.txt','w')
    main = ''
    scrapeRequests(archives_page,main,'a','issue/view','href','href','a','obj_galley_link','class','href')
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        soup = parse(link)
        try:
            PDF_links.append(soup.find('a',{'class','download'})['href'])
            print(f'gathered {len(PDF_links)} PDFs')
        except:
            pass 
if 'asjp.cerist.dz' in article:
    archives_page = 'https://www.asjp.cerist.dz/en/Articles/506'
    file = open('www.asjp.cerist.dz.txt','w')
    main = ''
    scrapeRequests(archives_page,main,'a','en/article/','href','href','a','downArticle','href','href')
if 'academicjournals' in article:
    archives_page = 'https://academicjournals.org/journal/AJPP/archive'
    file = open('academicjournals.org.txt','w')
    scrapeStructure_M(archives_page,'https://academicjournals.org/')
if 'bhmedsoc.com' in article:
    current_year = datetime.date.today().year
    issue_year = 2018
    issue_nb = 1
    PDF_links_temp = []
    file = open('www.bhmedsoc.com.txt','w')
    PDF_nbs = len(PDF_links_temp)
    main = 'https://www.bhmedsoc.com/jbms/'
    while issue_year <= current_year:
        Issues_links.append(f'https://www.bhmedsoc.com/jbms/archives.php?Article_Published_Year={issue_year}&Issues={issue_nb}')
        PDF_links = findAttrintarget(Issues_links,'a','.pdf','href','href',main)
        PDF_links_temp.extend(PDF_links)
        if PDF_nbs == len(PDF_links_temp):
            issue_year += 1
            issue_nb = 1
        else:
            issue_nb+=1
        PDF_nbs = len(PDF_links_temp)
        print(f'{PDF_nbs} added till now')
    PDF_links = PDF_links_temp.copy()
if 'ajol.info' in article:
    if 'jmbs' in article:
        archives_page ='https://www.ajol.info/index.php/jmbs/issue/archive'
        file = open('www.ajol.info-jmbs.txt','w')
    if 'eaoj' in article:
        archives_page ='https://www.ajol.info/index.php/eaoj/issue/archive'
        file = open('www.ajol.info-eaoj.txt','w')
    if 'ecajps' in article:
        archives_page ='https://www.ajol.info/index.php/ecajps/issue/archive'
        file = open('www.ajol.info-ecajps.txt','w')
    if 'ajhs' in article:
        archives_page ='https://www.ajol.info/index.php/ajhs/issue/archive'
        file = open('www.ajol.info-ajhs.txt','w')
    if 'ajr' in article:
        archives_page ='https://www.ajol.info/index.php/ajr/issue/archive'
        file = open('www.ajol.info-ajr.txt','w')
    if 'ajst' in article:
        archives_page ='https://www.ajol.info/index.php/ajst/issue/archive'
        file = open('www.ajol.info-ajst.txt','w')
    main = ''
    scrapeRequests(archives_page,main,'a','issue/view','href','href','a','obj_galley_link','class','href')
if 'ejmsonline.org' in article: # SITE IS DOWN
    archives_page = 'https://www.ejmsonline.org/volumes/35'
    file = open('www.ejmsonline.org-Abstracts.txt','w')
    scrapeStructure_O(archives_page)
    print(len(Abstracts_link))
    for link in Abstracts_link:
        file.write(link+'\n')
    file.close()
if 'me-jaa.com' in article:
    archives_page = 'http://www.me-jaa.com/me-jaapastissues.htm'
    file = open('www.me-jaa.com.txt','w')
    main = 'http://www.me-jaa.com/'
    Issues_links.append(archives_page)
    PDF_links = findAttrintarget(Issues_links,'a','.pdf','href','href',main)
if 'mejfm.com' in article:
    archives_page = 'http://www.mejfm.com/journal.htm'
    file = open('www.mejfm.com.txt','w')
    main = 'http://www.mejfm.com/'
    scrapeStructure_P(main)
if 'journals.uokerbala.edu.iq' in article:
    archives_page = 'https://journals.uokerbala.edu.iq/index.php/kj/issue/archive'
    file = open('journals.uokerbala.edu.iq-PDFs.txt','w')
    abstract = open('journals.uokerbala.edu.iq-abstracts.txt','w')
    scrapeStructure_N(archives_page)
    for link in Abstracts_link:
        abstract.write(link+'\n')
    abstract.close()
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        soup = parse(link)
        try:
            PDF_links.append(soup.find('a',{'class','download'})['href'])
            print(f'gathered {len(PDF_links)} PDFs')
        except:
            pass 
if 'www.iraqijms.net' in article:
    archives_page = 'https://www.iraqijms.net/archive.html#parentVerticalTab10'
    file = open('www.iraqijms.net.txt','w')
    main = 'https://www.iraqijms.net/'
    scrapeRequests(archives_page,main,'a','issue&id=','href','href','a','.pdf','href','href')
    temp = PDF_links.copy()
    PDF_links = list(dict.fromkeys(temp))
if 'iraqmedj.org' in article:
    archives_page = 'https://iraqmedj.org/index.php/imj/issue/archive'
    file = open('iraqmedj.org-PDFs.txt','w')
    abstract = open('iraqmedj.org-abstracts.txt','w')
    scrapeStructure_N(archives_page)
    for link in Abstracts_link:
        abstract.write(link+'\n')
    abstract.close()
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        soup = parse(link)
        try:
            PDF_links.append(soup.find('a',{'class','download'})['href'])
            print(f'gathered {len(PDF_links)} PDFs')
        except:
            pass 
if 'rmr.smr.ma/' in article:
    archives_page = 'http://rmr.smr.ma/archives'
    file = open('rmr.smr.ma.txt','w')
    main = 'http://rmr.smr.ma/'
    Issues_links.append(main+'/dernier-numero')
    scrapeRequests(archives_page,main,'a','/archives/','href','href','a','/archives/','href','href')
    Issues_links = PDF_links.copy()
    PDF_links.clear()
    PDF_links = findAttrintarget(Issues_links,'a','task=download','href','href',main)
if 'hsd-fmsb.org' in article:
    archives_page = 'https://www.hsd-fmsb.org/index.php/hsd/issue/archive'
    file = open('www.hsd-fmsb.org.txt','w')
    main = ''
    scrapeRequests(archives_page,main,'a','issue/view','href','href','a','galley-link','class','href')
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        soup = parse(link)
        try:
            PDF_links.append(soup.find('a',{'class','download'})['href'])
            print(f'gathered {len(PDF_links)} PDFs')
        except:
            pass
if 'phcfm.org' in article:
    archives_page = 'https://phcfm.org/index.php/phcfm/issue/archive'
    file = open('phcfm.org.txt','w')
    PDF_links = findAttrintarget(findElemintargetByPartialText(findAttrintarget([archives_page],'a','issue/view','href','href'), 'a', 'PDF','href'),'iframe','pdf.js','src','src')
if 'anafrimed.net' in article:
    archives_page = 'http://anafrimed.net/rubrique/archives/'
    file = open('anafrimed.net.txt','w')
    scrapeStructure_Q(archives_page)
if 'jaccrafrica.com' in article:
    archives_page = 'https://www.jaccrafrica.com/Publications/'
    file = open('www.jaccrafrica.com.txt','w')
    main = 'https://www.jaccrafrica.com/'
    PDF_links = findAttrintarget([archives_page],'a','.pdf','href','href',main)
if 'medtech.ichsmt.org' in article:
    archives_page = 'https://jkmc.uobaghdad.edu.iq/index.php/MEDICAL/issue/archive'
    file = open('medtech.ichsmt.org.txt','w')
    main = ''
    scrapeRequests(archives_page,main,'a','issue/view','href','href','a','obj_galley_link','class','href')
    temp = PDF_links.copy()
    PDF_links.clear()
    for link in temp:
        soup = parse(link)
        try:
            PDF_links.append(soup.find('a',{'class','download'})['href'])
            print(soup.find('a',{'class','download'})['href'])
            print(f'gathered {len(PDF_links)} PDFs')
        except:
            print(link)
            pass
if 'revues.imist.ma' in article:
    archives_page = 'https://revues.imist.ma/index.php/A2S/issue/archive'
    file = open('revues.imist.ma.txt','w')
    PDF_links = findAttrintarget(findAttrintarget(findAttrintarget([archives_page],'a','issue/view','href','href'), 'a', 'file','class','href',),'iframe','pdf.js','src','src')

if file == '':
    print('Journal not supported yet')
else:
    print(f'Gathered a total of {len(PDF_links)} PDFs')
    for link in PDF_links:
        file.write(link+'\n')
    file.close()
errors.close()


# keywordScan()   
# print('Scan done successfully')
# for i in range(0,len(Detected_PDF_link)):
#     print(f'\nLink {i+1}: {Detected_PDF_link[i]} \n\n')
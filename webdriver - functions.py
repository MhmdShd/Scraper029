from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# archive file for webdriver functions
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# headless options
options = Options()
options.add_argument('--headless')
options.add_argument("--disable-gpu")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)


def scrapeStructure_B2():
    getIssuesBY('title','table of contents',driver)
    driver.close()
    B_getPDFslinks()
    print('gathered all PDFs on provided site')
def B_getPDFslinks():#PDF_Pages
    PDF_page_link = []
    while (len(Issues_links)>0):
        url = Issues_links.pop()
        driver1 = webdriver.Chrome(options=options)
        driver1.get(url)
        pages = driver1.find_elements(By.PARTIAL_LINK_TEXT,'[PDF]')
        for link in pages:
            PDF_page_link.append(link.get_attribute('href'))
        print(f'\nGathered {len(PDF_page_link)} PDF Page')
        print(f'{len(Issues_links)} Issues not scanned yet')

    while len(PDF_page_link)>0:
        pdf_page = PDF_page_link.pop()
        driver2 = webdriver.Chrome(options=options)
        driver2.get(pdf_page)
        links = driver2.find_elements(By.TAG_NAME,'a')
        for link in links:
            href = link.get_attribute('href')
            if href != None:
                if '.pdf' in href:
                    PDF_links.append(href)
                    print(href)
        driver2.close()
        print(f'\nGathered {len(PDF_links)} PDFs')
        print(f'{len(PDF_page_link)} PDF Page not scanned yet')

def scrapeStructure_A2():
    while(len(Volume_links) > 0):
        volume = Volume_links.pop()
        driver = webdriver.Chrome(options=options)
        driver.get(volume)
        getIssuesBY('href','issue_',driver)
        print('\n\ngot all issues in this volume')
        driver.close()
    getPDFsInIssuesBY('href','.pdf',0)

def scrapeStructure_G2():
    G_getIssues()
    getPDFsInIssuesBY('href','.pdf')
def G_getVolumes():
    links = driver.find_elements(By.TAG_NAME,'a')
    for link in links:
        href = link.get_attribute('href')
        if href != None:
            if '/volume' in href:
                Volume_links.append(href)
                print(f'{len(Volume_links)} Volumes gathered')
def G_getIssues():
    while len(Volume_links)>0:
        volume = Volume_links.pop()
        driver = webdriver.Chrome(options=options)
        driver.get(volume)
        divs = driver.find_elements(By.TAG_NAME,'div')
        for div in divs:
            try:
                issue_parent_class = div.get_attribute('class')
                if issue_parent_class == 'issue_dv':
                    link = div.find_element(By.XPATH,'.//*')
                    href = link.get_attribute('href')
                    Issues_links.append(href)
                    print(f'{len(Issues_links)} Issues Gathered')
            except:
                pass
        print(f'{len(Volume_links)} volumes unscanned yet.')

def scrapeStructure_F2():
    F_getIssues()
    driver.close()
    F_getPDFs()
def F_getIssues():
    Issues = driver.find_elements(By.PARTIAL_LINK_TEXT,'BJMS Vol ')
    for link in Issues:
        href = link.get_attribute('href')
        Issues_links.append(href)
        print(f'{len(Issues_links)} Issues Gathered')
def F_getPDFs():
    while len(Issues_links)>0:
        issue = Issues_links.pop()
        driver = webdriver.Chrome(options=options)
        driver.get(issue)
        marks = driver.find_elements(By.TAG_NAME,'mark')
        for link in marks:
            href = link.find_element(By.XPATH,'..').get_attribute('href')
            if href != None:
                data = requests.request("GET", href)
                print('\n'+data.url)
                PDF_links.append(data.url)
                print(f'{len(PDF_links)} PDFs gathered\n')
        print(f'\nIssue {len(Issues_links)} left')
        driver.close()

def scrapeStructure_C2():
    Prev_driver = driver.find_element(By.CLASS_NAME,'previous').get_attribute('href')
    Next_driver = driver.find_element(By.CLASS_NAME,'next').get_attribute('href')
    C_getPDFs(driver)
    driver.close()

    while Prev_driver != None:        
        driver2= webdriver.Chrome(options=options)
        driver2.get(Prev_driver)
        C_getPDFs(driver2)
        try:
            Prev_driver = driver2.find_element(By.CLASS_NAME,'previous').get_attribute('href')
        except:
            Prev_driver = None
        driver2.close()    
    print('\nno more previous version')

    while Next_driver != None:
        driver3= webdriver.Chrome(options=options)
        driver3.get(Next_driver)
        C_getPDFs(driver3)
        try:
            Next_driver = driver3.find_element(By.CLASS_NAME,'next').get_attribute('href')
        except:
            Next_driver = None    
        driver3.close()
    print('\nno more next versions')
def C_getPDFs(Driver):
    Links  = Driver.find_elements(By.TAG_NAME, 'a')
    for PDF_page in Links:
        href = PDF_page.get_attribute('href')
        if href != None:
            if 'article/abstract' in href.lower() or 'article/fulltext' in href.lower() and PDF_page.get_attribute('class') != 'blocklink':
                PDF = href.replace('FullText','PDF')
                PDF = href.replace('Abstract','PDF')
                if 'Abstract' not in PDF:
                    PDF_links.append(PDF)
                    print(f'{len(PDF_links)} PDFs Gathered')
        
def scrapeStructure_E2():
    E_getVolumes()
    driver.close()
    getPDFsInIssuesBY('href','.pdf',0)
def E_getVolumes2():
    Volumes = driver.find_elements(By.PARTIAL_LINK_TEXT,'Vol. ')
    print(Volumes)
    for volume in Volumes:
        link = article.replace('archives.php',str(volume.get_attribute('onclick')).split("','")[0].replace("window.open('",''))
        Issues_links.append(link)
        print(f'{len(Issues_links)} Issues gathered')

def scrapeStructure_D2():
    global PDF_links
    Links = driver.find_elements(By.TAG_NAME,'a')
    for link in Links:
        if link.get_attribute('data-test') == 'next-page':
            Issues_links.append(link.get_attribute('href'))
    temp = []
    while len(Issues_links)>0 :
        issue = Issues_links[-0]
        driver1 = webdriver.Chrome(options=options)
        driver1.get(issue)
        getPDFsInIssuesBY('data-test','pdf-link',0)
        for link in PDF_links:
            print(link)
            temp.append(link)
        PDF_links.clear()
        Links = driver1.find_elements(By.TAG_NAME,'a')
        for link in Links:
            if link.get_attribute('data-test') == 'next-page':
                Issues_links.append(link.get_attribute('href'))
        driver1.close()
        print(f'gathered {len(temp)} PDFs in this volume.')
    PDF_links = temp

def scrapeStructure_I2():
    divs = driver.find_elements(By.TAG_NAME,'div')
    for div in divs:
        if div.get_attribute('class') == 'cat-children':
            links = div.find_elements(By.TAG_NAME,'a')
            for link in links:
                Issues_links.append(link.get_attribute('href'))
    print(f'{len(Issues_links)} Issues gathered')
    I_getPDFs2()
def I_getPDFs2():#PDF_Pages
    PDF_pages = []
    while len(Issues_links)>0:
        issue = Issues_links.pop()
        driver1 = webdriver.Chrome(options=options)
        driver1.get(issue)
        parent_elements = driver1.find_elements(By.TAG_NAME,'td')
        for parent in parent_elements:
            if parent.get_attribute('class') == 'list-title':
                PDF_pages.append(parent.find_element(By.TAG_NAME,'a').get_attribute('href'))
        driver1.close()

        for pdf_page in PDF_pages:
            driver2 = webdriver.Chrome(options=options)
            driver2.get(pdf_page)
            links = driver2.find_elements(By.TAG_NAME,'a')
            for link in links:
                if'.pdf' in link.get_attribute('href'):
                    PDF_links.append(link.get_attribute('href'))
                    print(f'{len(PDF_links)} PDFs gathered')
            driver2.close()

def scrapeStructure_J2():
    getVolumesByPartialText('Volume ')
    J_getIssues()
    J_getPDFs()
def J_getIssues():
    global Issues_links
    temp_Issues_links =[]
    while len(Volume_links)>0: 
        volume = Volume_links.pop()
        Vol_driver = webdriver.Chrome(options=options)
        Vol_driver.get(volume)
        for link in Vol_driver.find_elements(By.TAG_NAME,'a'):
            temp_Issues_links.append(link.get_attribute('href'))
            print(f'{len(temp_Issues_links)} Issues Gathered')  
        print(f'{len(Volume_links)} Volumes not scanned YET')
    Vol_driver.close()
    Issues_links = list(dict.fromkeys(temp_Issues_links))
    print(f'Gathered a total of {len(Issues_links)} Issues')   
def J_getPDFs2(): #PDF_Pages
    global PDF_links
    PDF_pages =[]
    temp_PDF_pages =[]
    temp_PDF_links=[]
    while len(Issues_links)>0:
        volume = Issues_links.pop()
        driver1 = webdriver.Chrome(options=options)
        if 'Size' not in 'volume':
            volume+='?pageSize=100&page=1'
        driver1.get(volume)
        Divs = driver1.find_elements(By.TAG_NAME,'div')
        for div in Divs:
            if div.get_attribute('class') == 'col-xs-12 col-sm-9 issue-listing':
                Links = div.find_elements(By.TAG_NAME,'a')
                for link in Links:
                    if '/jemtac.' in link.get_attribute('href') and 'doi.org' not in link.get_attribute('href'):
                        temp_PDF_pages.append(link.get_attribute('href'))
        PDF_pages = list(dict.fromkeys(temp_PDF_pages))
        print(f'Gathered a total of {len(PDF_pages)} PDFs pages')
        driver1.close()
    while len(PDF_pages)>0:
        driver2 = webdriver.Chrome(options=options)
        driver2.get(PDF_pages.pop())
        forms = driver2.find_elements(By.TAG_NAME,'form')
        for form in forms:
            if form.get_attribute('class') == 'ft-download-content__form ft-download-content__form--pdf js-ft-download-form ':
                url = form.get_attribute('action')
                temp_PDF_links.append(url)
                print(url)
        driver2.close()
    PDF_links = list(dict.fromkeys(temp_PDF_links))
    print(f'Gathered a total of {len(PDF_links)} PDFs')

def scrapeStructure_N():
    global Abstracts_link,Abstracts
    Abstract_links_temp = []
    getIssuesBY('href','issue/view',driver)
    driver.close()
    getPDFsInIssuesBY('id','article-')
    Abstracts_link = PDF_links.copy()
    Abstract_links_temp = PDF_links.copy()
    PDF_links.clear()
    getPDFsInIssuesBY('class','obj_galley_link pdf')
    print(len(PDF_links))
    print()
    print(len(Abstracts_link))
    while len(Abstract_links_temp)>0:
        driver1 = webdriver.Chrome(options=options)
        driver1.get(Abstract_links_temp.pop())
        Abstracts.append(driver1.find_element(By.CSS_SELECTOR,'.item.abstract').text.lower())
        print(f'Gathered {len(Abstracts)} Abstracts!')
        driver1.close()

def scrapeStructure_H2():
    Sections = driver.find_elements(By.TAG_NAME,'div')
    for Section in Sections:
        if Section.get_attribute('class') == 'kcite-section':
            issues_section = Section
    links_in_section = issues_section.find_elements(By.TAG_NAME,'a')
    for link in links_in_section:
        if link.get_attribute('title') == '':
            Issues_links.append(link.get_attribute('href'))
            print(f'{len(Issues_links)} issues gathered')
    getPDFsInIssuesBY('href','.pdf')

def scrapeStructure_P2():

    #  Old Archives Pages 
    #  Only full issue pdf is available
    #  Should add page in which the API was detected
    
    Issues_links.extend(['http://www.mejfm.com/Archives%202014%20-%202016.htm','http://www.mejfm.com/Archives%20June%202003-December%202013.htm','http://www.mejfm.com/archive.htm'])
    getPDFsInIssuesBY('href','.pdf')

def scrapeStructure_L2():
    getIssuesBY('href','--vol',driver)
    L_getPDFs2()
def L_getPDFs2():
    while len(Issues_links)>0:
        issue = Issues_links.pop()
        driver1 = webdriver.Chrome(options=options)
        driver1.get(issue)
        links = driver1.find_elements(By.PARTIAL_LINK_TEXT,'Download')
        for link in links:
            PDF_links.append(link.get_attribute('href'))
            print(link.get_attribute('href'))
        driver1.close()

def scrapeStructure_K2():
    Volume_links_temp =[]
    global Volume_links
    divs = driver.find_elements(By.TAG_NAME,'div')
    for div in divs:
        if div.get_attribute('class') == '_3R-H1':
            links = div.find_elements(By.TAG_NAME,'a')
            for link in links:
                if link.get_attribute('href') != None:
                    Volume_links_temp.append(link.get_attribute('href'))
    Volume_links = list(dict.fromkeys(Volume_links_temp))
    print(f'Gathered a total of {len(Volume_links)} Volumes')
    K_getPDFs()
def K_getPDFs2():#PDF_Pages
    PDF_Pages_temp =[]
    PDF_Pages =[]
    global PDF_links
    while len(Volume_links)>0:
        volume = Volume_links.pop()
        print(volume)
        driver1 = webdriver.Chrome(options=options)
        driver1.get(volume)
        divs = driver1.find_elements(By.TAG_NAME,'div')
        for div in divs:
            if div.get_attribute('class') == '_3K7uv':
                links = div.find_elements(By.TAG_NAME,'a')
                for link in links:
                    if '_files' in link:
                        PDF_Pages_temp.append(link.get_attribute('href'))
                        print(link.get_attribute('href'))
        driver1.close()
        print(f'\ngrathered {len(PDF_Pages_temp)} PDF Pages in this volume')
        print(f'{len(Volume_links)} not scanned yet')

    PDF_Pages = list(dict.fromkeys(PDF_Pages_temp))

    # get pdf links form pages

    PDF_links = getAttribute_By_TagName_TextInType(PDF_Pages,'a','href','.pdf','href')
    print(f'Gathered a total of {len(PDF_links)} PDFs')

def scrapeStructure_O2():
    Issues_links_temp = []
    getVolumesByPartialText2('Volume ')
    while len(Volume_links)>0:
        driver1 = webdriver.Chrome(options=options)
        driver1.get(Volume_links.pop())
        getIssuesBY('href','abstract',driver1)
        Issues_links_temp.extend(Issues_links)
        print(f'{len(Issues_links_temp)} Issues gathered in total.')
        driver1.close()
    while len(Issues_links)>0:
        issue = Issues_links.pop()
        driver1 = webdriver.Chrome(options=options)
        driver1.get(issue)
        Abstracts_link.append(issue)
        Abstracts.append(driver1.find_element(By.ID,'abstracts').text)

def scrapeStructure_M2():
    volumes = driver.find_elements(By.TAG_NAME,'a')
    Abstract_links =[]
    for volume in volumes:
        if 'ajpp/archive/' in volume.get_attribute('href').lower():
            Volume_links.append(volume.get_attribute('href'))
            print(volume.get_attribute('href'))
    print(f'Gathered a total of {len(Volume_links)} Volumes')

    Issues_links = getAttribute_By_TagName_TextInType(Volume_links,'a','href','ajpp/edition','href')
    Abstract_links = getAttribute_By_TagName_TextInType(Issues_links,'a','href','article-abstract','href')

        # scrapeStructure('href','ajpp/edition','href','article-abstract',0,driver1)
    for abstract in Abstract_links:
        PDF_links.append(abstract.replace('abstract','full-text-pdf'))
        print(abstract.replace('abstract','full-text-pdf'))

# need more editing to suit all structures, works fine now
def getAttribute_By_TagName_TextInType(link_list, tag_name, Search_attr, Search_attr_txt, Target_attr):
    print('getAttribute_By_TagName_TextInType')
    result_temp = []
    result = []
    while len(link_list)>0:
        link = link_list.pop()
        driver1 = webdriver.Chrome(options=options)
        driver1.get(link)
        print('\n'+link)
        tags = driver1.find_elements(By.TAG_NAME,tag_name)
        for tag in tags:
            try:
                if tag.get_attribute(Search_attr) != None and tag.get_attribute(Target_attr) != None:
                    if Search_attr_txt.lower() in tag.get_attribute(Search_attr).lower():
                        result_temp.append(tag.get_attribute(Target_attr))
                        print(f'Gathered {len(result_temp)} Target')
            except:
                pass
        result = list(dict.fromkeys(result_temp))
        print(len(result))
        driver1.close()
        print(f'{len(link_list)} link remaining in provided list')
    return result
def getAttribute_By_TagName_TextEqualType(link_list, tag_name, Search_attr, Search_attr_txt, Target_attr):
    print('getAttribute_By_TagName_TextEqualType')
    result_temp = []
    result = []
    for link in link_list:
        driver1 = webdriver.Chrome(options=options)
        driver1.get(link)
        tags = driver1.find_elements(By.TAG_NAME,tag_name)
        for tag in tags:
            if tag.get_attribute(Search_attr) != None and tag.get_attribute(Target_attr) != None:
                if tag.get_attribute(Search_attr) == Search_attr_txt:
                    result_temp.append(tag.get_attribute(Target_attr))
            print(f'Gathered {len(result_temp)} Target')
        print(len(result_temp))
        result = list(dict.fromkeys(result_temp))
        driver1.close()
    return result
def getAttribute_By_PartialText_TextEqualType(link_list, Partial_text, Search_attr, Search_attr_txt, Target_attr):
    print('getAttribute_By_PartialText_TextEqualType')
    result_temp = []
    result = []
    for link in link_list:
        driver1 = webdriver.Chrome(options=options)
        driver1.get(link)
        tags = driver1.find_elements(By.PARTIAL_LINK_TEXT,Partial_text)
        for tag in tags:
            if tag.get_attribute(Search_attr) != None and tag.get_attribute(Target_attr) != None:
                if tag.get_attribute(Search_attr) == Search_attr_txt:
                    result_temp.append(tag.get_attribute(Target_attr))
            print(f'Gathered {len(result_temp)} Target')
        print(len(result_temp))
        result = list(dict.fromkeys(result_temp))
        driver1.close()
    return result
def getAttribute_By_PartialText_TextinType(link_list, Partial_text, Search_attr, Search_attr_txt, Target_attr):
    print('getAttribute_By_PartialText_TextinType')
    result_temp = []
    result = []
    while len(link_list)>0:
        link = link_list.pop()
        driver1 = webdriver.Chrome(options=options)
        driver1.get(link)
        tags = driver1.find_elements(By.PARTIAL_LINK_TEXT,Partial_text)
        for tag in tags:
            if tag.get_attribute(Search_attr) != None and tag.get_attribute(Target_attr) != None:
                if Search_attr_txt in tag.get_attribute(Search_attr):
                    result_temp.append(tag.get_attribute(Target_attr))
            print(f'Gathered {len(result_temp)} Target')
        driver1.close()
    result = list(dict.fromkeys(result_temp))
    print(len(result))
    return result

# jokers
def getVolumesByPartialText2(text):
    global Volume_links
    Links = driver.find_elements(By.PARTIAL_LINK_TEXT, text)
    i = 1
    for link in Links:
        Href = link.get_attribute('href')
        if Href != None:
            Volume_links.append(Href)   
            print(f'{len(Volume_links)} Volumes gathered\n')
def scrapeStructureComplex(issue_attr, issue_text, type1, Article_Page_Tag, Article_Page_attr, Partial_text, Article_Page_attr_text, Retreived_attr_Article, type2, PDF_file_Tag, PDF_file_attr, PDF_file_text, Retreived_attr_PDF, Driver=driver):
    global PDF_links
    getIssuesBY(issue_attr,issue_text,Driver)
    print(f'\nGathered a total of {len(Issues_links)} Issues')
    if type1 == 'PT':
        PDF_Pages = getAttribute_By_PartialText_TextinType(Issues_links, Partial_text, Article_Page_attr, Article_Page_attr_text, Retreived_attr_Article)
    else:
        PDF_Pages = getAttribute_By_TagName_TextInType(Issues_links,Article_Page_Tag,Article_Page_attr,Article_Page_attr_text,Retreived_attr_Article)
    print(f'Gathered {len(PDF_Pages)} PDF Pages')
    PDF_links = getAttribute_By_TagName_TextInType(PDF_Pages,PDF_file_Tag,PDF_file_attr,PDF_file_text,Retreived_attr_PDF)
    print(f'Gathered {len(PDF_links)} PDF Links')
def scrapeStructure(issueType,issueTxt,PDFType,PDFText,Sleep=0,Driver=driver):
    getIssuesBY(issueType,issueTxt,Driver)
    print(f'\nGathered a total of {len(Issues_links)} Issues')
    Driver.close()
    getPDFsInIssuesBY(PDFType,PDFText,Sleep)
    print(f'Gathered a total of {len(PDF_links)} PDFs at this point')
def getIssuesBY(type,txt,Driver=driver):
    global Issues_links
    temp_Issues_links =[]
    Issues = Driver.find_elements(By.TAG_NAME,'a')
    for link in Issues:
        try:
            href = link.get_attribute('href')
            if link.get_attribute(type) != None:
                if txt.lower() in link.get_attribute(str(type).lower()):
                    if '#' not in link.get_attribute(str(type).lower()):
                        temp_Issues_links.append(href)
                        print(href)
        except:
            pass 
    for x in list(dict.fromkeys(temp_Issues_links)):
        Issues_links.append(x)
    print(f'\nGathered a total of {len(Issues_links)} Issues')
def getPDFsInIssuesBY(type,txt,Sleep=0):
    global PDF_links
    Temp_PDF_links=[]
    while (len(Issues_links)>0):
        issue = Issues_links.pop()
        if issue == 'https://journals.ju.edu.jo/JMJ/issue/view/357':
            issue = 'https://journals.ju.edu.jo/JMJ/issue/view/357/showToc'
        driver = webdriver.Chrome(options=options)
        driver.get(issue)
        sleep(Sleep)
        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:
            try:
                href = link.get_attribute('href')
                if link.get_attribute(type) != None:
                    if txt in link.get_attribute(str(type)).lower():
                        Temp_PDF_links.append(href)
                        print(f'\n{len(Temp_PDF_links)} PDFs gathered')
                        print(href)
            except:
                pass
        print(f'\nIssue {len(Issues_links)} left')
        for x in list(dict.fromkeys(Temp_PDF_links)):
            PDF_links.append(x)
        print(f'Gathered a total of {len(PDF_links)} PDFs at this point')
        driver.close()


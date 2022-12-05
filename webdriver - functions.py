# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# archive file for webdriver functions
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------



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
def C_getPDFs2(Driver):
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



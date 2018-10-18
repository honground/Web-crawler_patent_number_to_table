"""

install required python package
pip install requests html5lib bs4 progressbar2

"""

import requests, csv, time
#import progressbar
from bs4 import BeautifulSoup

OUTPUT_FILENAME = 'patent_output.csv'
patent_numbers = ['US6025334', 'US8767010', 'US7558853']

# ====================================================================================== #

header = [
    'patent number', 'Patent title', 'Abstract', 'Number of inventor', 
    'Current Assignee', 'Original Assignee', 'Priority date', 'Number of image', 
    'Classification', 'Family', 'Patent citation(backward)', 'Non-patent citation', 
    'cited by', 'Legal events', 'Parent applications', 'Child applications', 
    'Priority applications', 'Application claiming priority', 'Number of claim', 'Claim'
]

def make_row(patent_number):
    url = 'https://patents.google.com/patent/{}'.format(patent_number)
    
    r = requests.get(url, timeout=7)
    b = BeautifulSoup(r.text, 'html5lib')
    row = []
    
    # patent number
    _ = b.find('dd', attrs={'itemprop': 'publicationNumber'}).text
    row.append(_)
    
    # title
    _ = b.find('meta', attrs={'name': 'DC.title'}).attrs['content'].strip()
    row.append(_)
    
    # abstract
    _ = b.find('div', class_='abstract').text.strip()
    row.append(_)
    
    # Number of inventor
    _ = len(b.find_all('meta', attrs={'scheme': 'inventor'}))
    row.append(_)
    
    # Current Assignee
    _ = ', '.join([el.text.strip() for el in b.find_all('dd', attrs={'itemprop': 'assigneeCurrent'})])
    row.append(_)
    
    # Original Assignee
    _ = ', '.join([el.text.strip() for el in b.find_all('dd', attrs={'itemprop': 'assigneeOriginal'})])
    row.append(_)
    
    # Priority date
    _ = b.find('time', attrs={'itemprop': 'priorityDate'}).text
    row.append(_)
    
    # Number of image
    _ = len(b.find_all('li', attrs={'itemprop': 'images'}))
    row.append(_)
    
    # Classification
    _ = ', '.join([li.find('span', attrs={'itemprop': 'Code'}).text for li in [ul.find_all('li')[-1] for ul in b.find_all('ul', attrs={'itemprop': 'cpcs'})]])
    row.append(_)
    
    # Family
    _ = ', '.join(['{} ({})'.format(tr.find('span', attrs={'itemprop': 'countryCode'}).text, tr.find('span', attrs={'itemprop': 'num'}).text) for tr in b.find_all('tr', attrs={'itemprop': 'countryStatus'})])
    row.append(_)
    
    # Patent citation(backward)
    _ = len(b.find_all('tr', attrs={'itemprop': 'backwardReferencesOrig'})) + len(b.find_all('tr', attrs={'itemprop': 'backwardReferencesFamily'}))
    row.append(_)
    
    # Non-patent citation
    _ = len(b.find_all('tr', attrs={'itemprop': 'detailedNonPatentLiterature'}))
    row.append(_)
    
    # cited by
    _ = len(b.find_all('tr', attrs={'itemprop': 'forwardReferencesOrig'})) + len(b.find_all('tr', attrs={'itemprop': 'forwardReferencesFamily'}))
    row.append(_)
    
    # Legal events
    _ = len(b.find_all('tr', attrs={'itemprop': 'legalEvents'}))
    row.append(_)
    
    # Parent applications
    _ = len(b.find_all('tr', attrs={'itemprop': 'parentApps'}))
    row.append(_)
    
    # Child applications
    _ = len(b.find_all('tr', attrs={'itemprop': 'childApps'}))
    row.append(_)
    
    # Priority applications
    _ = len(b.find_all('tr', attrs={'itemprop': 'priorityApps'}))
    row.append(_)
    
    # Application claiming priority
    _ = len(b.find_all('tr', attrs={'itemprop': 'appsClaimingPriority'}))
    row.append(_)
    
    # Number of claim
    _ = int(b.find('section', attrs={'itemprop': 'claims'}).find('span', attrs={'itemprop': 'count'}).text)
    row.append(_)
    
    # Claim
    _ = b.find('section', attrs={'itemprop': 'claims'}).find('div', attrs={'itemprop': 'content'}).text.strip()
    row.append(_)
    
    return row


with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    writer.writerow(header)
    
    #bar = progressbar.ProgressBar(max_len=len(patent_numbers))
    #for pn in bar(patent_numbers):
    for pn in patent_numbers:
        print(patent_numbers)
        try:
            writer.writerow(make_row(pn))
        except:
            writer.writerow([pn, 'error'])
        
        time.sleep(1)

import re
import subprocess
import sys

from datetime import datetime, timedelta

from bs4 import BeautifulSoup

try:
    search = str(sys.argv[1]).lower()
except IndexError:
    search = None

yesterday = (datetime.today() - timedelta(days=1)).strftime('%m/%d/%Y')


def get_page(page):
    page_command = command.format(page , yesterday, yesterday)
    p = subprocess.Popen(page_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out


def parse_page(page):
    page_content = get_page(page)

    for result in BeautifulSoup(page_content, 'html.parser').find_all('div', class_='resultsDiv'):
        parcel = result.div.table.table.find_all('tr')[1].find_all('td')[0].text
        owner = result.div.table.table.find_all('tr')[1].find_all('td')[1].text
        address = result.div.table.table.find_all('tr')[2].table.table.tr.find_all('td')[1].text

        if search in owner.lower():
            # Got an owner match, add address to final list
            if parcel not in addresses.keys():
                addresses[parcel.strip()] = re.sub('\s+', ' ', address).strip()


command  = "curl 'http://oh-mahoning-auditor.publicaccessnow.com/SalesSearch.aspx?page479={}&SearchType=1'"
command += " -H 'Cookie: C_F1L=11/30/2018; C_F1H=11/30/2018; C_F2L=-1; C_F3L=-1; C_F4L=-1; C_F5L=-1; C_F6L=-1; C_F7L=-1; C_F8L=-1; C_F9L=-1; C_F10L=-1; C_F11L=-1; C_s1=1; C_s2=1; C_s3=1; C_s4=1; C_s5=1; C_s6=1; C_s7=1; C_s8=1;'"
command += " --data-binary $'"
command += """------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="StylesheetManager_TSSM"

------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="ScriptManager_TSM"

;;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en:eb198dbd-2212-44f6-bb15-882bde414f00:ea597d4b:b25378d2
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="__EVENTTARGET"

------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="__EVENTARGUMENT"

------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="__VIEWSTATEGENERATOR"

CA0B0334
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="__VIEWSTATEENCRYPTED"

------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="__EVENTVALIDATION"

tFKco0GaAfnknmEgO80y7FTrEkELkvyEgrpqGUdaDsrqVjTws32sQPI+dgxF1jHtQp5wK9ctXg8CcuzWklrnq8LvXNMHn/eqBzvCcA==
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="Field3Low"

-1
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="s3"

1
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="Field3High"

------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="Field1Low"

{}
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="s1"

1
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="Field1High"

{}
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="Field4Low"

------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="s4"

1
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="Field4High"

------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="Field5Low"

------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="s5"

1
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="Field5High"

------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="Field6Low"


------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="s6"

1
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="Field6High"

------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="SearchType"

1
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="dispSearch"

1
------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="btnSearch"


------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="ScrollTop"

------WebKitFormBoundaryt68N7yP3UO6b5nv7
Content-Disposition: form-data; name="__dnnVariable"

------WebKitFormBoundaryt68N7yP3UO6b5nv7--'"""
command += " --compressed"

# Grab first page to see page count
first_page = get_page(1)

first_page_parsed = BeautifulSoup(first_page, 'html.parser')
page_count = int(first_page_parsed.find_all('div', class_='search-results-bar')[0].find_all('a')[-2].text)

addresses = {}

# Try each iteration multiple times because the site doesn't do an ORDER BY
for retry in range(3):
    for page in range(1, page_count+1):
        parse_page(page)

if addresses:
    print 'Found transfers:'
    for parcel, address in addresses.items():
        if re.search(r'\d', address):
            print parcel, address, 'https://www.google.com/maps/place/{}+mahoning+county+oh/'.format(address.replace(' ', '+'))
        else:
            print parcel, address
else:
    print 'No transfers found'

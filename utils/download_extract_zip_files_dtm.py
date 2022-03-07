from fileinput import filename
from bs4 import BeautifulSoup
import os, requests, zipfile
from io import BytesIO

html_page = requests.get(
    'https://www.geopunt.be/download?container=dhm-vlaanderen-ii-dtm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DTM,%20raster,%201m'
)

soup = BeautifulSoup(html_page.content, 'html.parser')

# Download all links
all_links = []
for elem in soup.find_all('a'):
    all_links.append(elem.get('href'))

#print(all_links)

# Remove all unwanted links
all_links = [x for x in all_links if x.startswith('https://downloadagiv')]

all_links_rem = all_links[32:]
print(all_links_rem)

# Download all zip files and extract them in data directory
for i in range(len(all_links_rem)):
    req = requests.get(all_links[i])
    filename = all_links[i].split('/')[-1]
    zip = zipfile.ZipFile(BytesIO(req.content))
    zip.extractall(f'./data/DTM/{filename}')

#Unzip zipped files within each folder
dir_name = '/home/nemish/BeCode/BeCode_Projects/3d-houses/data/DTM'
extension = '.zip'
os.chdir(dir_name)

for folder in os.listdir(dir_name):
    for item in os.listdir(folder):
        if item.endswith(extension):
            file = os.path.abspath(folder + '/' + item)
            zip_ref = zipfile.ZipFile(file)
            zip_ref.extractall(folder)
            zip_ref.close()
import os, zipfile

dir_name = '/home/nemish/BeCode/BeCode_Projects/3d-houses/data'
extension = 'Shapefile.zip'
os.chdir(dir_name)

for folder in os.listdir(dir_name):
    if folder.endswith(extension):
        file = os.path.abspath(folder)
        zip_ref = zipfile.ZipFile(file)
        zip_ref.extractall()
        zip_ref.close()

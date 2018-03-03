import xml.etree.ElementTree as ET
import json

tree = ET.parse('soc.xml')
root = tree.getroot()

data = {}
i = 0

terms = root.find('Terms').findall('Term')

for term in terms:
    classes = term.find('Classes').findall('Class')
    for child in classes:
        data[str(i)] = {}
        data[str(i)]['dept'] = child.find('Subject').text
        data[str(i)]['num'] = child.find('CatalogNbr').text
        data[str(i)]['name'] = child.find('CourseTitleLong').text
        try:
            data[str(i)]['desc'] = child.find('Description').text
        except:
            data[str(i)]['desc'] = ''

        i += 1

# print(data)

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)

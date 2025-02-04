import xml.etree.ElementTree as ET
import json

tree = ET.parse('soc.xml')
root = tree.getroot()

data = []
i = 0

terms = root.find('Terms').findall('Term')

for term in terms:
    classes = term.find('Classes').findall('Class')
    for child in classes:
        data.append({})
        data[i]['dept'] = child.find('Subject').text.replace("'", "''" )
        data[i]['num'] = child.find('CatalogNbr').text.replace("'", "''" )
        data[i]['name'] = child.find('CourseTitleLong').text.replace("'", "''" )
        try:
            data[i]['desc'] = child.find('Description').text.replace("'", "''" )
        except:
            data[i]['desc'] = ''

        i += 1

# print(data)

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)

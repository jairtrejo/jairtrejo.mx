from bs4 import BeautifulSoup

with open('deploy/blog/listing.html') as f:
    soup = BeautifulSoup(f.read())

archive = soup.find('table')

root = {'value': None, 'row': None, 'children': []}
lineage = [root]

for tag in filter(lambda t: t.name, archive.children):
    level = {'year': 1, 'month': 2, 'day': 3}[tag.td.get('class')[0]]

    while len(lineage) > level:
        lineage.pop()

    node = {
        'value': tag.td.string.strip(),
        'row': tag,
        'children': [],
    }

    lineage[-1]['children'].append(node)
    lineage.append(node)


def traverse(node):
    for n in sorted(node['children'], key=lambda n: n['value'], reverse=True):
        archive.append(n['row'])
        traverse(n)

archive.clear()
traverse(root)

with open('deploy/blog/listing.html', 'w') as f:
    f.write(soup.prettify('utf-8'))

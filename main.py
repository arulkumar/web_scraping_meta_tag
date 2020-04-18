import requests, csv, time
from bs4 import BeautifulSoup

start_time = time.time()

def get_meta_title(url):
  content = ""
  try:
    URL = url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find_all("meta")
    for t in title:
      if t.get('name', None) == 'description':
        content = t.get('content')
        break
    return content
  except:
    print(">>" + url)
    return ""
  

dict_title = []

with open('ac.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            meta_title = get_meta_title(row[0])
            dict_title.append({ 'url': row[0], 'description': meta_title })
            line_count += 1
    print(f'Processed {line_count} lines.')

csv_columns = ['url','description']
csv_file = "ac_description.csv"
try:
  with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in dict_title:
      writer.writerow(data)
except IOError:
  print("I/O error")

#Time taken
print("--- %s seconds ---" % (time.time() - start_time))
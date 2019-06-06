import requests

writtenlinks = []
counter = 1
"""
Use Inurl to get in the links content.
"""
while True:
    src = requests.get("inurl:cdn-08.anonfile.com", timeout=10).text
    links = src.split('<h2><a href="')[1:]
    for link in links:
        link = link.split('"')[0]
        if link in writtenlinks:
            continue
        else:
            handle = open('AnonFilelinks.txt', 'a')
            handle.write(link + '\n')
            print(link)
            writtenlinks.append(link)
    counter += 10

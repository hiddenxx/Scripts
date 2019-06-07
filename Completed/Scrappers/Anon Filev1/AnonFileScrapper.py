import requests

requestIndex = 1
writtenlinks = []
keyword = "tutorial"
url = "https://www.bing.com/search?q=site%3aanonfile.com+" + keyword + "&qs=n&sp=-1&pq=site%3aanonfile.com+list&first=" + str(
    requestIndex) + "&FORM=PERE2"
print(url)
"""
Use Inurl to get in the links content.
"""
while True:
    with open('AnonFilelinks.txt', 'a') as handle:
        src = requests.get(url, timeout=10).text
        links = src.split('<h2><a href="')[1:]
        for link in links:
            link = link.split('"')[0]
            if link in writtenlinks:
                continue
            else:
                handle.write(link + '\n')
                print(link)
                writtenlinks.append(link)
        requestIndex += 10

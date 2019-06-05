# import requests , argparse
#
# def main() :
#     ####################################################################################
#     parser = argparse.ArgumentParser(description="Pasting Text to create a pastr.io file to view")
#     parser.add_argument("-f", help=("Input the filename / Drop the file after to paste in Pastr.io"), dest="input", type=str,
#                         required=True)
#     args = parser.parse_args()
#     ####################################################################################
#     def parsePaste():
#         with open(args.input, 'r') as content_file:
#             content = content_file.read()
#             return content
#     content = parsePaste()
#     title = input("Please enter a title for the Pasted text\n")
#
#     headers = {
#         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#         "Accept-Language": "en-US,en;q=0.9",
#         "cache-control": "max-age=0",
#         "Content-Type": "application/x-www-form-urlencoded",
#         "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
#     }
#     login_payload = {
#     }
#     with requests.Session() as s:
#         p = s.post("https://pastr.io/", data=login_payload,headers=headers,timeout=10)
#     print(p.status_code)
#
#     payload = {
#         'api_title': title,
#         'api_paste': content,
#         'api_syntax': ["No Syntax", "nohighlight"],
#         'api_destruct': None
#     }
#
#     api_url = "https://pastr.io/api/create/"
#
#     r = requests.post(api_url,api_url)
#
#     print(r)
# if __name__ == '__main__':
#     main()

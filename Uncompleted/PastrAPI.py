"""
Need to fix Bad Request issue.

"""
import argparse

import requests


def initialLogin(s):
    p1 = s.get("https://pastr.io/login", timeout=5)  # get cookie
    login_payload = {
        "email": "demonmanoj@gmail.com",
        "password": "Dem0n123@",
        "remember": False
    }
    # p = requests.post("https://pastr.io/login", json=login_payload,headers=p1.headers,timeout=10)
    p = s.post("https://pastr.io/login", json=login_payload, headers=p1.headers, timeout=10)
    return p


def parsePaste(args):
    with open(args.input, 'r') as content_file:
        content = content_file.read()
        return content


def parseRespone(r):
    print(r)


def main():
    ####################################################################################
    parser = argparse.ArgumentParser(description="Pasting Text to create a pastr.io file to view")
    parser.add_argument("-f", help=("Input the filename / Drop the file after to paste in Pastr.io"), dest="input",
                        type=str,
                        required=True)
    parser.add_argument("-t", help=("Input the title for the Paste"), dest="title", type=str, required=True)
    args = parser.parse_args()
    ####################################################################################
    content = parsePaste(args)  # this has the Text to be pasted.

    with requests.Session() as s:
        loginStatus = initialLogin(s)
        headers = s.cookies

        if loginStatus == 200:
            print("Login Successful : {}", loginStatus.status_code)
            payload = {
                "OnReadDestroy": 0,
                "destroy_at": "none",
                "paste": args.input,
                "syntax": "nohighlight",
                "title": args.title
            }

            api_url = "https://pastr.io/api/create"

            r = s.post(api_url, cookies=headers, params=payload)
            parsed_response = parseRespone(r)
            print("Adding the link into PasteLinks...")
            with open("Resources/PasteLinks", "w") as file:
                file.writelines(r)
            if r.status_code == 200:
                pass
        else:
            print("Login Unsuccessful :", loginStatus.text)


if __name__ == '__main__':
    main()

import re
import requests

# func to query in baidu's translation web, but single-phrase input is supported only
def query_online(keyword) -> None:
    first_attempt = requests.post(
        url="https://fanyi.baidu.com/sug",
        data={
            "kw": keyword
        },
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.100 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    # transform utf-8 to gbk
    pre_load = first_attempt.text
    for uniChar in re.compile("\\\\\\w+").findall(pre_load):
        pre_load = pre_load.replace(uniChar, str(uniChar).encode("utf-8").decode("unicode_escape"))

    # format output
    for sigData in str(re.compile("\"data\":.*[^}]").findall(pre_load)[0]).split("},{"):
        print(sigData
              .translate({ord(c): None for c in str("{}[]\"")})
              .replace("k:", "")
              .replace("v:", "")
              .replace("data:", "")
              .replace(",", " : "))


# Main
print("Welcome to Azusaings's Dictionary, remember to keep your machine online!(-q to quit)")
while True:
    cmd = input(">>> ")
    if cmd == "-q":
        break
    else:
        query_online(cmd)

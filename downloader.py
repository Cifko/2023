from urllib.request import Request, urlopen
from urllib import parse
import re
import ssl
from html import unescape
from bs4 import BeautifulSoup
from os.path import exists, getsize
from time import sleep
from datetime import datetime

YEAR = 2023

ssl._create_default_https_context = ssl._create_unverified_context

cookie = open("cookie").readline().rstrip()


def wait_for_start(day: int):
    while datetime(YEAR, 12, day, 6, 0, 3, 0) > datetime.now():
        print(" ", datetime(YEAR, 12, day, 6, 0, 3, 0) - datetime.now(), end="\r")
        sleep(0.1)
    print("                           ", end="\r")


def get_input_filename(day: int):
    return f"{day:02}-input.txt"


def get_sample_input_filename(day: int):
    return f"{day:02}-input-sample.txt"


def get_sample_output_filename(day: int):
    return f"{day:02}-output-sample.txt"


def download(day: int):
    wait_for_start(day)
    if exists(get_input_filename(day)):
        if getsize(get_input_filename(day)) != 0:
            return
    try:
        download_sample(day)
    except:
        print("Sample download failed")
    url = f"https://adventofcode.com/{YEAR}/day/{day}/input"

    r = Request(url)
    r.add_header("Cookie", cookie)
    q = urlopen(r)
    f = open(get_input_filename(day), "wb")
    f.write(q.read())
    f.close()


def download_sample(day: int):
    url = f"https://adventofcode.com/{YEAR}/day/{day}"
    r = Request(url)
    r.add_header("Cookie", cookie)
    q = urlopen(r)
    res = q.read()
    res = res.decode("utf-8")
    if not exists(get_sample_input_filename(day)) or getsize(get_sample_input_filename(day)) == 0:
        pattern = r"For example.*<pre><code>(.*?)</code></pre>"
        str_res = re.findall(pattern, res, flags=re.MULTILINE | re.DOTALL)
        if len(str_res) == 0:
            pattern = r"example.*<pre><code>(.*?)</code></pre>"
            str_res = re.findall(pattern, res, flags=re.MULTILINE | re.DOTALL)
            if len(str_res) == 0:
                pattern = r"<pre><code>(.*?)</code></pre>"
                str_res = re.findall(pattern, res, flags=re.MULTILINE | re.DOTALL)
        str_res = str_res[0]
        f = open(get_sample_input_filename(day), "wt")
        f.write(BeautifulSoup(unescape(str_res), "html.parser").text)
        f.close()
    pattern2 = "<code>(?!.*?</code>.*?<em>).*?<em>(.*?)</em>(?!.*<em>).*?</code>"
    str_res = re.findall(pattern2, res, flags=re.MULTILINE)
    f = open(get_sample_output_filename(day), "wt")
    f.write(unescape(str_res[-1]))
    f.close()


def post_answer(day: int, level: int, answer: str):
    if level not in [1, 2]:
        print("Not submitting")
        return
    url = f"https://adventofcode.com/{YEAR}/day/{day}/answer"
    r = Request(url, data=parse.urlencode({"level": level, "answer": answer}).encode())
    r.add_header("Cookie", cookie)
    x = str(urlopen(r).read())
    x = x.replace("\\n", "\n")
    x = x.replace("\\'", "'")
    r = re.search(r"That's.*?[\.!]", str(x))
    if r:
        print(r.group())
        return r.group() == "That's the right answer!"
    else:
        print(x)
        print("Something went wrong !")
        return False

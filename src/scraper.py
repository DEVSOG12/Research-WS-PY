import csv
import os
import sys
import threading
import time
from os import listdir
from os.path import isfile, join
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import pdfkit
import PyPDF2
import signal
import sys

import requests as requests
from bs4 import BeautifulSoup

from src.tests.tests import Test

bad = {}

sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 27)


# Return Map as a table as a string
def map_to_table(map_of_items):
    table = ""
    for i in list(map_of_items.keys()):
        table += "<tr>"
        table += "<td>" + str(i) + "</td>"
        for j in list(map_of_items[str(i)].keys()):
            table += "<td>" + str(map_of_items[str(i)][j]) + "</td>"
        table += "</tr>"
    return table


def send_simple_message(data):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxc90a44973a78431e8faa47bd2b632cb2.mailgun.org/messages",
        auth=("api", "key-ded180a76d4b1efa5e19a1f50730b74b"),
        data={"from": "Research Bot <postmaster@sandboxc90a44973a78431e8faa47bd2b632cb2.mailgun.org>",
              "to": "Oreofe Solarin <khakis_forearm.0u@icloud.com>",
              "subject": "Run Complete",
              "html": str(data)})


# You can see a record of this email in your logs: https://app.mailgun.com/app/logs.

# You can send up to 300 emails/day from this sandbox server.
# Next, you should add your own domain so you can send 10000 emails/month for free.

# new thread will get stack of such size
def signal_handler(sig, frame):
    print("Bad URLS", bad)
    send_simple_message(map_to_table(bad))
    sys.exit(0)


# Parse HTML and return visible text
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = ''.join(chunk for chunk in chunks if chunk)
    return text


def text_from_html(body):
    try:
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll('p')
    # #     Remove the script, style, footer, header, etc.
    #     visible_texts = filter(tag_visible, texts)
    #     texts = u" ".join(t.text for t in visible_texts)

    except Exception as ex:
        texts = ""
        print("Error", ex)
    # visible_texts = filter(tag_visible, texts)
    return texts


signal.signal(signal.SIGINT, signal_handler)


def main(self, dev, test):
    DEV = dev
    TEST = test
    data = []
    paa = {}

    only_files = [f for f in listdir("./data") if isfile(join("./data", f))]

    for i in only_files:
        if not i.__contains__(".csv"):
            only_files.remove(i)

    for mrm in only_files:
        # if mrm in ['IndigenousPeoplesRights.csv', 'TortureCombatantsPrisonersTerror.csv']:
        #     continue
        name = "./data/" + mrm
        print(mrm)
        with open(name, 'r') as file:
            reader_time_s = time.time()
            csvreader = csv.reader(file)
            for row in csvreader:
                data.append(row)
            for i in range(len(data)):
                # print(data[i])
                if i != 0:
                    paa[str(i)] = {
                        data[0][0]: data[i][0],
                        data[0][1]: data[i][1],
                        data[0][2]: data[i][2],
                        "type": data[0][3] if data[i][3] == "1" else data[0][4] if data[i][4] == "1" else data[0][5] if
                        data[i][
                            5] == "1" else
                        data[0][6] if data[i][6] == "1" else data[0][7] if data[i][7] == "1" else data[0][8]
                        if data[i][8] == "1" else
                        data[0][9] if data[i][9] == "1" else data[0][10],

                    }
            # csv.clo
            if not TEST:
                print("Done Reading: ", "Time Taken: ", "--- %s seconds ---" % (time.time() - reader_time_s))
            # print(paa)
            # break
            # print()
            if DEV:
                paa = dict(list(paa.items())[:5])

            # paa = dict(list(paa.items())[::-1])

            for k in list(paa.keys()):

                name_of_file = "{0}_{1}_{2}_{3}.pdf".format(paa[str(k)]["Organization Name"],
                                                            paa[str(k)]["Topic area"], paa[str(k)][
                                                                "type"], str(k))

                namer = "./outputs/" + mrm
                # Filter based on files that are already written
                if os.path.exists(namer + "/" +
                                  paa[str(k)]["Organization Name"].replace(" ", "_") + "/" + paa[str(k)][
                                      "type"].replace(" ", "_") + "/" + name_of_file):
                    continue

                openfolder(namer, paa, k)

                if not (str(paa[str(k)]["URL"]).__contains__('.pdf') or not str(paa[str(k)]["URL"]).startswith("http")):
                    start_re_t = time.time()
                    req = Request(
                        url=paa[str(k)]["URL"],
                        headers={
                            'User-Agent': 'Mozilla/5.0'},
                    )
                    try:
                        header = "<h1>" + paa[str(k)]["Organization Name"] + "</h1>"
                        header2 = "<h1>" + paa[str(k)]["Topic area"] + "</h1>"
                        header3 = "<h1>" + paa[str(k)]["URL"] + "</h1>"
                        header4 = "<h1>" + paa[str(k)]["type"] + "</h1>"
                        total = ""
                        html = urlopen(req, timeout=100000).read()
                        with open(namer + "/" +
                                  paa[str(k)]["Organization Name"].replace(" ", "_") + "/" + paa[str(k)][
                                      "type"].replace(" ", "_") + "/" + name_of_file.replace('.pdf', '.txt'),
                                  "w") as text_file:
                            text_file.write(parse_html(html))
                        for i in text_from_html(html):
                            ksi = ""
                            try:
                                ksi = str(i)
                            except Exception as ex:
                                print("Can't parse string", ex, "<-- the error")
                            total = total + " " + ksi
                        total = header + header2 + header3 + header4 + total
                        total = str(total.encode('ascii', errors='ignore').decode("utf-8"))

                        try:
                            pdfkit.from_string(total, namer + "/" +
                                               paa[str(k)]["Organization Name"].replace(" ", "_") + "/" + paa[str(k)][
                                                   "type"].replace(" ", "_") + "/" + name_of_file)
                            if not TEST:
                                print("Done Request and Writing: ", k, "Time Taken: ",
                                      "--- %s seconds ---" % (time.time() - start_re_t))

                        except Exception as e:
                            print(e, "Done Request and Writing but Failed to Save: ", k, "Time Taken: ",
                                  "--- %s seconds ---" % (time.time() - start_re_t))
                            bad[str(k)] = paa[str(k)]
                        # print(html)
                    except HTTPError:
                        print("HTTP Error in ", k, "th", "\n", "link: ", paa[str(k)]["URL"])
                        bad[str(k)] = paa[str(k)]
                        print("Done Request and Writing but Failed: ", k, "Time Taken: ",
                              "--- %s seconds ---" % (time.time() - start_re_t))
                    except URLError:
                        print("URL Error in ", k, "th", "\n", "link: ", paa[str(k)]["URL"])
                        bad[str(k)] = paa[str(k)]
                        print("Done Request and Writing but Failed: ", k, "Time Taken: ",
                              "--- %s seconds ---" % (time.time() - start_re_t))
                    except Exception as e:
                        print(e, "Done Request and Writing but Failed to Save: ", k, "Time Taken: ",
                              "--- %s seconds ---" % (time.time() - start_re_t))
                        bad[str(k)] = paa[str(k)]

                if str(paa[str(k)]["URL"]).__contains__('.pdf'):
                    final_file_name = namer + "/" + paa[str(k)]["Organization Name"].replace(" ", "_") + "/" + \
                                      paa[str(k)]["type"].replace(" ", "_") + "/" + name_of_file
                    if os.path.exists(final_file_name):
                        continue
                    start_req_t = time.time()
                    req = Request(
                        url=paa[str(k)]["URL"],
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                          'like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
                    )

                    try:
                        response = urlopen(req, timeout=100000)
                        with open(final_file_name, 'wb') as f:
                            f.write(response.read())
                        if not TEST:
                            print("Done Request and Writing: ", k, "Time Taken: ",
                                  "--- %s seconds ---" % (time.time() - start_req_t))
                        pdffileobj = open(final_file_name, 'rb')
                        pdfreader = PyPDF2.PdfFileReader(pdffileobj)
                        for i in range(pdfreader.numPages):
                            pageobj = pdfreader.getPage(i)
                            text = pageobj.extractText()
                            with open(final_file_name.replace('.pdf', '.txt'),
                                      "a") as text_file:
                                text_file.write(text)
                    except HTTPError:
                        print("HTTP Error in ", k, "th", "\n", "link: ", paa[str(k)]["URL"])
                        bad[str(k)] = paa[str(k)]
                        print("Done Request and Writing but Failed: ", k, "Time Taken: ",
                              "--- %s seconds ---" % (time.time() - start_req_t))
                    except URLError:
                        print("URL Error in ", k, "th", "\n", "link: ", paa[str(k)]["URL"])
                        bad[str(k)] = paa[str(k)]
                        print("Done Request and Writing but Failed: ", k, "Time Taken: ",
                              "--- %s seconds ---" % (time.time() - start_req_t))
                    except Exception as e:
                        print(e, "Done Request and Writing but Failed to Save: ", k, "Time Taken: ",
                              "--- %s seconds ---" % (time.time() - start_req_t))
                        bad[str(k)] = paa[str(k)]

            if TEST:
                Test(namer, paa).test1()
                print(bad)


def tests():
    Exception("To Write Test")


def openfolder(namer, paa, k):
    if not os.path.exists(namer):
        os.makedirs(namer)
    if not os.path.exists(namer + "/" + paa[str(k)]["Organization Name"].replace(" ", "_")):
        try:
            os.makedirs(namer + "/" + paa[str(k)]["Topic area"].replace(" ", "_"))
        except Exception as e:
            print(e)
    if not os.path.exists(
            namer + "/" + paa[str(k)]["Organization Name"].replace(" ", "_") + "/" + paa[str(k)][
                "type"].replace(" ", "_")):
        try:
            os.makedirs(
                namer + "/" + paa[str(k)]["Organization Name"].replace(" ", "_") + "/" + paa[str(k)][
                    "type"].replace(" ", "_"))
        except Exception as e:
            print(e)

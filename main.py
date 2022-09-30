import csv
import logging
import os
import sys
import threading
import time
from os import listdir
from os.path import isfile, join
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import socket
import pdfkit
from bs4 import BeautifulSoup

sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size

DEV = True


def text_from_html(body):
    try:
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll('p')
        for x in texts:
            if x.name == 'img':
                x.decompose()

    except Exception as ex:
        texts = ""
        print("Error", ex)
    # visible_texts = filter(tag_visible, texts)
    return texts


datt = []
paa = {}
bad = {}

onlyFiles = [f for f in listdir("./data") if isfile(join("./data", f))]

for i in onlyFiles:
    if not i.__contains__(".csv"):
        onlyFiles.remove(i)

for mrm in onlyFiles:
    name = "./data/" + mrm
    with open(name, 'r') as file:
        readerTimeS = time.time()
        csvreader = csv.reader(file)
        for row in csvreader:
            datt.append(row)
        for i in range(len(datt)):
            if i != 0:
                paa[str(i)] = {
                    datt[0][0]: datt[i][0],
                    datt[0][1]: datt[i][1],
                    datt[0][2]: datt[i][2],
                    "type": datt[0][3] if datt[i][3] == "1" else datt[0][4] if datt[i][4] == "1" else datt[0][5] if
                    datt[i][
                        5] == "1" else
                    datt[0][6] if datt[i][6] == "1" else datt[0][7] if datt[i][7] == "1" else datt[0][8] if datt[i][
                                                                                                                8] == "1" else
                    datt[0][9] if datt[i][9] == "1" else datt[0][10],

                }
        # csv.clo
        print("Done Reading: ", "Time Taken: ", "--- %s seconds ---" % (time.time() - readerTimeS))
        # print(paa)
        # break
        # print()
        for k in list(paa.keys()):
            nameoffile = "{0}_{1}_{2}_{3}.pdf".format(paa[str(k)]["Organization Name"],
                                                      paa[str(k)]["Topic area"], paa[str(k)][
                                                          "type"], str(k))
            namer = "./outputs/" + mrm
            if not os.path.exists(namer):
                os.makedirs(namer)

            if not (str(paa[str(k)]["URL"]).__contains__('.pdf') or not str(paa[str(k)]["URL"])):
                startReqT = time.time()
                req = Request(
                    url=paa[str(k)]["URL"],
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
                )
                try:
                    html = urlopen(req, timeout=10).read()
                except HTTPError:
                    print("HTTP Error in ", k, "th", "\n", "link: ", paa[str(k)]["URL"])
                    bad[str(k)] = paa[str(k)]
                    print("Done Request and Writing but Failed: ", k, "Time Taken: ",
                          "--- %s seconds ---" % (time.time() - startReqT))
                except Exception as e:
                    print(e, "Done Request and Writing but Failed to Save: ", k, "Time Taken: ",
                          "--- %s seconds ---" % (time.time() - startReqT))
                header = "<h1>" + paa[str(k)]["Organization Name"] + "</h1>"
                header2 = "<h1>" + paa[str(k)]["Topic area"] + "</h1>"
                header3 = "<h1>" + paa[str(k)]["URL"] + "</h1>"
                header4 = "<h1>" + paa[str(k)]["type"] + "</h1>"
                total = ""

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
                    pdfkit.from_string(total, namer + "/" + nameoffile)
                    print("Done Request and Writing: ", k, "Time Taken: ",
                          "--- %s seconds ---" % (time.time() - startReqT))

                except Exception as e:
                    print(e, "Done Request and Writing but Failed to Save: ", k, "Time Taken: ",
                          "--- %s seconds ---" % (time.time() - startReqT))
                    bad[str(k)] = paa[str(k)]

            if str(paa[str(k)]["URL"]).__contains__('.pdf'):
                startReqT = time.time()

                req = Request(
                    url=paa[str(k)]["URL"],
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
                )

                try:
                    response = urlopen(req, timeout=10)
                except HTTPError as error:
                    logging.error('Data not retrieved because %s\nURL: %s', error, paa[str(k)]["URL"])
                except URLError as error:
                    if isinstance(error.reason, socket.timeout):
                        logging.error('socket timed out - URL %s', paa[str(k)]["URL"])
                    else:
                        logging.error('some other error happened', paa[str(k)]["URL"])

                file = open(namer + "/" + nameoffile, 'wb')

                file.write(response.read())

                file.close()

                print("Done Request and Writing: ", k, "Time Taken: ", "--- %s seconds ---" % (time.time() - startReqT))
                # print('The k val', k)

            if int(k) == 50 and DEV:
                break
        print(bad)


def tests():
    Exception("To Write Test")

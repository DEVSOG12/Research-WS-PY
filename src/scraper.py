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

from src.tests.tests import Test

sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size


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


def main(self, dev, test):
    DEV = dev
    TEST = test
    data = []
    paa = {}
    bad = {}

    only_files = [f for f in listdir("./data") if isfile(join("./data", f))]

    for i in only_files:
        if not i.__contains__(".csv"):
            only_files.remove(i)

    for mrm in only_files:
        name = "./data/" + mrm
        with open(name, 'r') as file:
            reader_time_s = time.time()
            csvreader = csv.reader(file)
            for row in csvreader:
                data.append(row)
            for i in range(len(data)):
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

            for k in list(paa.keys()):
                name_of_file = "{0}_{1}_{2}_{3}.pdf".format(paa[str(k)]["Organization Name"],
                                                            paa[str(k)]["Topic area"], paa[str(k)][
                                                                "type"], str(k))

                namer = "./outputs/" + mrm

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

                if not (str(paa[str(k)]["URL"]).__contains__('.pdf') or not str(paa[str(k)]["URL"])):
                    start_re_t = time.time()
                    req = Request(
                        url=paa[str(k)]["URL"],
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                          'like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
                    )
                    try:
                        html = urlopen(req, timeout=10).read()
                    except HTTPError:
                        print("HTTP Error in ", k, "th", "\n", "link: ", paa[str(k)]["URL"])
                        bad[str(k)] = paa[str(k)]
                        print("Done Request and Writing but Failed: ", k, "Time Taken: ",
                              "--- %s seconds ---" % (time.time() - start_re_t))
                    except Exception as e:
                        print(e, "Done Request and Writing but Failed to Save: ", k, "Time Taken: ",
                              "--- %s seconds ---" % (time.time() - start_re_t))
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

                if str(paa[str(k)]["URL"]).__contains__('.pdf'):
                    start_req_t = time.time()

                    req = Request(
                        url=paa[str(k)]["URL"],
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                          'like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
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
                    file = open(namer + "/" + paa[str(k)]["Organization Name"].replace(" ", "_") + "/" + paa[str(k)][
                        "type"].replace(" ", "_") + "/" + name_of_file, 'wb')

                    file.write(response.read())

                    file.close()

                    if not TEST:
                        print("Done Request and Writing: ", k, "Time Taken: ",
                              "--- %s seconds ---" % (time.time() - start_req_t))
                    # print('The k val', k)

            if TEST:
                Test(namer, paa).test1()
                print(bad)


def tests():
    Exception("To Write Test")

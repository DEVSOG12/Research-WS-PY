from urllib.error import HTTPError
import time
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
import pdfkit


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll('p')
    # visible_texts = filter(tag_visible, texts)
    return texts


datt = []
paa = {}
bad = {}
with open("./data/ChildrensRights.csv", 'r') as file:
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
                "type": datt[0][3] if datt[i][3] == "1" else datt[0][4] if datt[i][4] == "1" else datt[0][5] if datt[i][
                                                                                                                    5] == "1" else
                datt[0][6] if datt[i][6] == "1" else datt[0][7] if datt[i][7] == "1" else datt[0][8] if datt[i][
                                                                                                            8] == "1" else
                datt[0][9] if datt[i][9] == "1" else datt[0][10],

            }
    # csv.clo
    print("Done Reading: ", "Time Taken: ", "--- %s seconds ---" % (time.time() - readerTimeS))

    for k in range(len(paa)):
        if not (str(paa[str(k + 1)]["URL"]).__contains__('.pdf') or not str(paa[str(k + 1)]["URL"])):
            startReqT = time.time()
            req = Request(
                url=paa[str(k + 1)]["URL"],
                headers={'User-Agent': 'Mozilla/5.0'},
            )
            try:
                html = urlopen(req).read()
            except HTTPError:
                print("HTTP Error in ", k, "th", "\n", "link: ", paa[str(k+1)]["URL"])
                bad[str(k+1)] = paa[str(k+1)]
                print("Done Request and Writing but Failed: ", k, "Time Taken: ", "--- %s seconds ---" % (time.time() - startReqT))
            except Exception as e:
                print(e, "Done Request and Writing but Failed to Save: ", k, "Time Taken: ", "--- %s seconds ---" % (time.time() - startReqT))
            header = "<h1>" + paa[str(k+1)]["Organization Name"] + "</h1>"
            header2 = "<h1>" + paa[str(k+1)]["Topic area"] + "</h1>"
            header3 = "<h1>" + paa[str(k+1)]["URL"] + "</h1>"
            header4 = "<h1>" + paa[str(k+1)]["type"] + "</h1>"
            total = ""

            for i in text_from_html(html):
                total = total + " " + str(i)
            total = header + header2 + header3 + header4 + total
            total = str(total.encode('ascii', errors='ignore').decode("utf-8"))
            nameoffile = paa[str(k+1)]["Organization Name"] + "_" + paa[str(k+1)]["Topic area"] + "_" + paa[str(k+1)][
                "type"] + "_" + str(k + 1) + ".pdf"

            try:
                pdfkit.from_string(total, "./Children/" + nameoffile)
                print("Done Request and Writing: ", k, "Time Taken: ", "--- %s seconds ---" % (time.time() - startReqT))

            except Exception as e:
                print(e, "Done Request and Writing but Failed to Save: ", k, "Time Taken: ", "--- %s seconds ---" % (time.time() - startReqT))
                bad[str(k+1)] = paa[str(k+1)]

        if str(paa[str(k + 1)]["URL"]).__contains__('.pdf'):
            startReqT = time.time()

            req = Request(
                url=paa[str(k + 1)]["URL"],
                headers={'User-Agent': 'Mozilla/5.0'},
            )

            nameoffile = paa[str(k + 1)]["Organization Name"] + "_" + paa[str(k + 1)]["Topic area"] + "_" + \
                         paa[str(k + 1)][
                             "type"] + "_" + str(k + 1) + ".pdf"

            try:
                response = urlopen(req)

            except HTTPError:
                print("HTTP Error in ", k, "th", "\n", "link: ", paa[str(k+1)]["URL"])
                print("Done Request and Writing but Failed: ", k, "Time Taken: ",
                      "--- %s seconds ---" % (time.time() - startReqT))

            file = open("./Children/" + nameoffile, 'wb')

            file.write(response.read())

            file.close()

            print("Done Request and Writing: ", k,  "Time Taken: ", "--- %s seconds ---" % (time.time() - startReqT))

    print(bad)


def tests():
    Exception("To Write Test")
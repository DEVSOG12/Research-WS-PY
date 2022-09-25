# def doubleList(nums):
#     for x in range(nums):
#         print(2 * x)
#
#
# doubleList(100)
from urllib.request import Request, urlopen
req = Request(
    url='https://humanrightsforkids.org/wp-content/uploads/Human-Rights-for-Kids-ACEs-Facts-Sheet.pdf',
headers={'User-Agent': 'Mozilla/5.0'},
            )
response = urlopen(req)
file = open("document.pdf", 'wb')
file.write(response.read())
file.close()
print("Completed")
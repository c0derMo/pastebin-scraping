import requests
import PastebinHTMLParser
import DataManager
from time import sleep

delayMS = 1000

if DataManager.dbExists():
    print("Connecting to metadata-database...")
    conn = DataManager.create_connection("data/metadata.db")
else:
    print("Setting up database...")
    conn = DataManager.create_connection("data/metadata.db")
    DataManager.setupDB(conn)
print("One-time-querying recent pastebins...")
recentRequests = requests.get('https://pastebin.com/archive')
parser = PastebinHTMLParser.ArchiveParser()
parser.feed(recentRequests.text)

for paste in parser.allElements:
    print("{0}".format(paste))

for paste in parser.allElements:
    sleep(delayMS/1000)
    if DataManager.isPasteDownloaded(conn, paste[1:]):
        print(paste + " already downloaded...")
    else:
        print("Quering " + paste + "...")
        pasteRequest = requests.get('https://pastebin.com' + paste)
        pr = PastebinHTMLParser.PasteParser()
        pr.setup()
        pr.feed(pasteRequest.text)
        DataManager.savePasteMetadata(conn, paste[1:], pr.title, pr.language, pr.creationdate, pr.user, pr.expiresat)
        DataManager.savePasteContent(paste[1:], pr.content)

print("Saving DB...")
conn.commit()
print("Closing DB...")
conn.close()
print("Done!")
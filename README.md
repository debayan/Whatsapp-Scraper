
# Whatsapp Web Scraper

* Runtime: Python 3.5
## How to install:
###
```
git clone https://github.com/debayan/Whatsapp-Scraper.git
cd Whatsapp-Scraper
virtualenv -p python3 .
source bin/activate
pip3 install geckodriver-autoinstaller selenium
```

### Run:
```
python whatsapp_web.py
(Scan the QR code using the Whatsapp app)
```
If you want the chat histories of certain users only, then archive all the other user conversations on your phone first (archive, not delete). You can unarchive them later. This way, once the web interface opens up, only the chats required to be saved will show up for the script.

Script selects each user one by one, scrolls up the active chat window to the top (so chats from the past are also visible), then prints the messages on screen and saves to chats.json.

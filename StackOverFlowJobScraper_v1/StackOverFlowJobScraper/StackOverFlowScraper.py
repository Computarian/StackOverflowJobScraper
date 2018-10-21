# Michael Sousa Comp 490-002

import requests
from bs4 import BeautifulSoup
import textwrap
from nltk.tokenize import sent_tokenize
from requests.exceptions import ConnectionError
from tkinter import *
import time


# stores the url in a variable and checks that requests has retrieved it from the server
def get_url():
    # specifies the url
    url = "https://stackoverflow.com/jobs/feed?location=bridgewater&range=50&distanceUnits=Miles"

    # error handling for internet connection and bad url's here
    try:
        requests.get(url)
        if requests.get(url).status_code is 200:
            return url
        else:
            print("Error: Can't connect to ", url)
    except ConnectionError:
        print("Failed to open url.")
        sys.exit()


# parses html retrieved through requests via beautiful soup and organizes it into a list
def jobs_parser(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    items = soup.find_all('item')

    job_posts = []

    for item in items:
        job_post = {}
        job_post['title'] = item.title.text
        job_post['link'] = "https://stackoverflow.com/jobs/" + item.guid.text

        #strips 'most' html markup out of job descriptions
        clean_description = strip_html(item.description.text)
        sentences = sent_tokenize(clean_description)

        #grabs first sentence of description
        job_post['description'] = sentences[0]
        job_posts.append(job_post)

    for item in job_posts:
        print(item['title'])
        print(item['link'])
        value = item['description']
        wrapper = textwrap.TextWrapper(width=70)
        word_list = wrapper.wrap(text=value)
        #prints each line.
        for element in word_list:
            print(element)
        print("\n")


# strips html markup from passed in html data
def strip_html(data):
    cleaned_data = re.compile(r'<.*?>')
    return cleaned_data.sub(' ', data)


# two primary functions, collects the html data and checks for errors, then parses that data
def web_scraper():
    url = get_url()
    jobs_parser(url)


# displays a GUI
class Display(Frame):


    # initializes GUI with two buttons and a frame for output of web_scraper function
    def __init__(self, parent=0):
        Frame.__init__(self, parent)

        # title of window
        self.winfo_toplevel().title("Stack Overflow Jobs Feed Scraper for jobs located within 50 miles of Bridgewater, MA")

        # refresh button to fetch job listings
        self.refresh_button = Button(self, text="Refresh Job Listings", command=self.on_refresh)
        self.refresh_button.pack()

        # text output box for listing job posts
        self.output = Text(self)
        self.output.pack()

        #scroll bar functionality to make it easier to scroll through job posts
        scrollbar = Scrollbar()
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=self.output.yview)

        # quit buttton in case you want a button in the gui and don't want to close the window directly
        self.quit_button = Button(self, text="Quit",command=self.on_quit)
        self.quit_button.pack()
        sys.stdout = self
        self.pack()


    # refreshes job listings
    def on_refresh(self):
        # clears text box
        self.output.delete(1.0, END)
        # sleep time of 1 second to avoid accidental DDOSing from spamming refresh
        time.sleep(1)
        web_scraper()


    # quits the application
    def on_quit(self):
        Tk().quit()


    # inserts web_scraper code into text box
    def write(self, txt):
        self.output.insert(END, str(txt))


    # handles exit code 120 caused by flush from sys.stdout
    def flush(self):
        pass


if __name__ == '__main__':
    Display().mainloop()
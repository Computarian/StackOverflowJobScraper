# Michael Sousa Comp 490-002

import requests
from bs4 import BeautifulSoup
import textwrap
from nltk.tokenize import sent_tokenize
from requests.exceptions import ConnectionError
from tkinter import *
import time
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from collections import Counter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


def basemap(cities):
    fig_map = plt.Figure(figsize=(5, 5), dpi=100)
    axes = fig_map.add_subplot(111)

    # creating map
    map = Basemap(projection='merc', lat_0=57, lon_0=-135,
                  resolution='h', area_thresh=0.1,
                  llcrnrlon=-72, llcrnrlat=41,
                  urcrnrlon=-69, urcrnrlat=43,
                  ax=axes)

    map.drawcoastlines()
    map.drawstates()
    map.fillcontinents()
    map.drawmapboundary()

    #prints number of jobs per city for debugging
    #print(Counter(cities))
    counterCities = Counter(cities)

    # Get the location of each city and plot it
    geolocator = Nominatim()
    for city, num_jobs in counterCities.items():
        loc = geolocator.geocode(city)
        x, y = map(loc.longitude, loc.latitude)
        map.plot(x, y, marker='o', color='Blue')
        axes.text(x, y, (city, num_jobs))

    return fig_map

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
def jobs_parser(url, job_find):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    items = soup.find_all('item')

    job_posts = []

    for item in items:
        job_post = {}
        job_post['title'] = item.title.text
        job_post['citystate'] = re.search("(\(([A-Z][a-z]+\s?)+,\s[A-Z]{2}\))", item.title.text).group(0)
        job_post['link'] = "https://stackoverflow.com/jobs/" + item.guid.text

        #strips 'most' html markup out of job descriptions
        clean_description = strip_html(item.description.text)
        sentences = sent_tokenize(clean_description)

        #grabs first sentence of description
        job_post['description'] = sentences[0]
        if job_find is not "" and ((item.description.text).find(job_find) > 0 or (item.title.text.find(job_find)) > 0):
            job_posts.append(job_post)
        elif job_find is "":
            job_posts.append(job_post)

    cities = []

    for item in job_posts:
        print(item['title'])
        print(item['link'])
        description = item['description']
        wrapper = textwrap.TextWrapper(width=70)
        word_list = wrapper.wrap(text=description)
        #prints each line.
        for element in word_list:
            print(element)
        print("\n")
        #formats city, state to make ready for basemap
        strip_parens = re.compile(r'(\(|\))')
        cities.append(strip_parens.sub('', item['citystate']))

    return cities

# strips html markup from passed in html data
def strip_html(data):
    cleaned_data = re.compile(r'<.*?>')
    return cleaned_data.sub(' ', data)


# two primary functions, collects the html data and checks for errors, then parses that data
def web_scraper(job_find):
    url = get_url()
    cities = jobs_parser(url, job_find)
    jobs_map = basemap(cities)
    return jobs_map

# displays a GUI
class Display(Frame):


    # initializes GUI with two buttons and a frame for output of web_scraper function
    def __init__(self, parent=0):
        Frame.__init__(self, parent)

        # title of window
        self.winfo_toplevel().title("Stack Overflow Jobs Feed Scraper for jobs located within 50 miles of Bridgewater, MA")

        # search button to find jobs with titles, descriptions that contain keyword
        self.search_label = Label(text="Enter a Job keyword to search for")
        self.search_label.pack(side=TOP)

        entry_content = StringVar()
        self.search_entry = Entry(textvariable = entry_content)
        self.search_entry.pack(side=TOP)

        self.search_button = Button(self, text="Search Jobs!", command = self.job_search)
        self.search_button.pack(side=TOP)

        # quit buttton in case you want a button in the gui and don't want to close the window directly
        self.quit_button = Button(self, text="Quit",command=self.on_quit)
        self.quit_button.pack(side=TOP)

        # text output box for listing job posts
        self.output = Text(self)
        self.output.pack(side=RIGHT)

        #scroll bar functionality to make it easier to scroll through job posts
        self.scrollbar = Scrollbar()
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.scrollbar.config(command=self.output.yview)

        sys.stdout = self
        self.pack()


    # searches for job based on job search criteria
    def job_search(self):
        # clears text box
        self.output.delete(1.0, END)
        # collects entry data
        jobs_to_find = self.search_entry.get()
        self.search_entry.delete('0', 'end')
        # sleep time of 1 second to avoid accidental DDOSing from spamming refresh
        time.sleep(1)
        jobs_map = web_scraper(jobs_to_find)

        # drawing the map in the GUI
        self.canvas = FigureCanvasTkAgg(jobs_map, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=LEFT)
        toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=BOTTOM)


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
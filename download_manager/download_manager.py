from selenium import webdriver
import requests
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from torrent_manager.torrent_add import run_torrents_add
import schedule
import pickle
import time

class Torrent:
    def __init__(self, magnetic, seeders, leechers):
        self.magnetic = magnetic
        self.seeders = seeders
        self.leechers = leechers

def run(login_driver: webdriver.Chrome):
    print("Service initialized")
    
    save_cookies(login_driver, "cookies.pkl")

    login_driver.quit()

    chrome_options = Options()
    chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Optional
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "C:\BJ",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False
    })
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    load_cookies(driver, "cookies.pkl")

    runner(driver)
    schedule.every(10).minutes.do(lambda: runner(driver))
    print("scheduler setup")

    while True:
        schedule.run_pending()
        time.sleep(1)

url = "https://bj-share.info/index.php"

def runner(driver: webdriver.Chrome):
    print("Task ran")

    driver.get(url)
    for x in [501, 503, 504, 505]:
        driver.execute_script(f"catLancamentos({x},0)")
        time.sleep(1)

        # Get the page HTML content
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, "html.parser")
        #print(soup)

        torrent_rows = soup.find_all("tr", class_="torrent row")
        torrents = []
        # Extract the text inside the last <td> element of each <tr> element
        for row in torrent_rows:
            #print(row)
            allTd = row.find_all("td")[-3:]
            magnetic = allTd[0].find("a")["href"]
            seeders = allTd[1].get_text(strip=True)
            leechers = allTd[2].get_text(strip=True)
            torrent = Torrent(magnetic, seeders, leechers)
            torrents.append(torrent)


        for torrent in torrents:
            print("Link:" + torrent.magnetic)
            print("Seed:" + torrent.seeders)
            print("Leech:" + torrent.leechers)
            if int(torrent.leechers) >= 10:
                driver.get("https://bj-share.info/" + torrent.magnetic)
            print("")

    run_torrents_add()


def save_cookies(driver, filename):
    # Get the current cookies from the driver
    cookies = driver.get_cookies()

    # Save the cookies to a file using pickle
    with open(filename, 'wb') as file:
        pickle.dump(cookies, file)

def load_cookies(driver, filename):
    # Load the cookies from the file using pickle
    with open(filename, 'rb') as file:
        cookies = pickle.load(file)

    # Add each cookie to the driver
    for cookie in cookies:
        driver.add_cookie(cookie)




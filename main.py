import os
import threading
import time
from urllib.request import Request, urlopen
from lxml import etree
from selenium import webdriver
from collections import deque

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Anime")
os.makedirs(desktop_path, exist_ok=True)  # Create the folder if it doesn't exist

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    link = input("Link: ")
    # link = "https://anime3rb.com/titles/ao-ashi"
    # start_ep = int(input("Start episode: "))
    start_ep = 1
    # end_ep = int(input("End episode: "))
    end_ep = -1

    anime_page = urlopen(Request(link, headers=headers))
    htmlparser = etree.HTMLParser()
    tree = etree.parse(anime_page, htmlparser)
    episodes = int(tree.xpath("/html/body/div[2]/div[4]/main/div[2]/section[1]/div/div/div/div[2]/div[3]/div[2]/div[2]/p[2]")[0].text)

    if end_ep != -1: episodes = end_ep

    anime_name = link[link.rindex("/") + 1:]
    state = True

    service = webdriver.ChromeService("chromedriver.exe")

    # Configure Chrome options
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": desktop_path,  # Set download directory
        "download.prompt_for_download": False,       # Disable download confirmation
        "directory_upgrade": True,                  # Automatically overwrite existing files
        "safebrowsing.enabled": True                # Enable safe browsing
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--disable-throttling')
    options.add_argument('--no-proxy-server')
    # options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(
        # service = service,
        options = options
    )
    driver.get("chrome://downloads/")
    global queue
    queue = deque()

    for i in range(start_ep, episodes + 1):
        ep_link = f"https://anime3rb.com/episode/{anime_name}/{i}"
        print(ep_link)
        ep_page = urlopen(Request(ep_link, headers=headers))
        tree = etree.parse(ep_page, htmlparser)
        download_link = tree.xpath("/html/body/div[2]/div[4]/main/div[2]/section[1]/div/div/div[1]/div[2]/div[4]/div[2]/div[1]/div/div[3]/a")[0].get("href")
        queue.append(download_link)
        if state:
            download_thread = threading.Thread(target=download, args=[driver])
            download_thread.start()
            state = False
        
    download_thread.join()
    driver.quit()

def download(driver: webdriver.Chrome):
    while queue:
        driver.execute_script(f"window.open(\"{queue.popleft()}\")")
        while not is_done() or len(driver.window_handles) > 1:
            time.sleep(1)

def is_done():
    return not any(file.endswith(".crdownload") for file in os.listdir(desktop_path))

if __name__ == "__main__":
    main()
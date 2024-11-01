from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import threading
from pathlib import Path

def is_completed(dir):
    allFiles: list[str] = os.listdir(dir)
    for file_name in allFiles:
        if file_name.endswith(".crdownload"):
            return False  # Download is still in progress
    return True  # No incomplete downloads, meaning the file download is complete

def download():
    i = 1
    while downloadLinks:
        driver.execute_script(f"window.open('{downloadLinks[0]}')")
        print(f"Downloading episode {i}")
        time.sleep(5)
        while not is_completed(dir):
            time.sleep(1)
        downloadLinks.pop(0)
        i += 1
        
def get_download_links():
    global downloadLinks, downloadthread
    downloadthread = None
    downloadLinks = []
    for link in links:
        driver.get(link)
        time.sleep(1)
        downloadBtns = driver.find_elements(
            By.XPATH,
            "/html/body/div[2]/div[4]/main/div/section[1]/div/div/div[1]/div[2]/div[4]/div[2]/div[1]/div/div",
        )
        for button in downloadBtns:
            label = button.find_element(By.TAG_NAME, "label")
            if "480" in label.text:
                downloadLink = button.find_element(By.TAG_NAME, "a")
                otherLink = downloadLink.get_attribute("href")
                downloadLinks.append(otherLink)
                break
        else:
            downloadLink = download[0].find_element(By.TAG_NAME, 'a')
            otherLink = downloadLink.get_attribute("href")
            downloadLinks.append(otherLink)
        if downloadthread is None:
            downloadthread = threading.Thread(target=download)
            downloadthread.start()
    while downloadthread.is_alive():
        time.sleep(1)
    

downloadpath = str(Path.home()) + "\\Desktop\\Anime"
# print(downloadpath)
# print(downloadpath)

# dir = input("Directory: ")

prefs = {
    "download.default_directory": downloadpath,
    "profile.default_content_settings.popups": 0,
    "directory_upgrade": True,
    "safebrowsing.enabled": True,
}

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", prefs)
# options.add_argument("headless")

driver = webdriver.Chrome(options = options)
driver.minimize_window()


link = input("Link: ")
lowerLimit = int(input("Starting from episode: "))
upperLimit = int(input("To episode: "))


driver.get(link)

time.sleep(3)

all_links = driver.find_elements(
    By.XPATH,
    "/html/body/div[2]/div[4]/main/div/section[1]/div/div/div/div[3]/div[2]/div/div/a",
)

links = []
if upperLimit == -1: upperLimit = len(all_links)
for link in all_links[lowerLimit - 1 : upperLimit]:
    url = link.get_attribute("href")
    links.append(url)

get_download_links()


driver.quit()
exit()

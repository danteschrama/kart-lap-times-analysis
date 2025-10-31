import locale
import os
import time
from datetime import datetime

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set the locale to Dutch
locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")

# Selinium options
options = Options()
options.add_argument("--disable-search-engine-choice-screen")
options.headless = True


def get_heat_urls(BASE_URL):
    heats = []

    rows = (
        driver.find_element(By.TAG_NAME, "main")
        .find_element(By.TAG_NAME, "tbody")
        .find_elements(By.TAG_NAME, "tr")
    )
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        for col in columns:
            val = col.find_element(By.TAG_NAME, "span")
            date = val.get_attribute("title")
            if "januari" in date:
                print(date)
                col.click()

                time.sleep(2)

                link_paths = driver.find_element(By.TAG_NAME, "main").find_elements(
                    By.TAG_NAME, "li"
                )
                for link in link_paths:
                    links.append(
                        link.find_element(By.TAG_NAME, "a").get_attribute("href")
                    )

                time.sleep(2)
    return heats


def get_data(loc):
    """
    Function to get the data for a location
    """

    BASE_URL = f"https://reserveren-{loc}.raceplanet.nl"

    # Define Chromium browser
    driver = Chrome(options=options)
    driver.implicitly_wait(30)
    driver.get(BASE_URL + "/heat-results")

    cookies = driver.find_element(
        By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"
    )
    cookies.click()

    heats = get_heat_urls(BASE_URL)

    for heat_link in heats:
        print(heat_link)

    return None


def main() -> None:
    """
    Page is entirely generated using JavaScript so we need a driver to get the actual data.
    """

    location = ["delft", "amsterdam"]

    heats = get_data(location[0])


if __name__ == "__main__":
    main()

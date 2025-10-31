import locale
import os
import time
from datetime import datetime

from playwright.sync_api import sync_playwright

# Set the locale to Dutch
locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")


def get_heat_ids(page, base_url) -> list:
    page.goto(base_url + "/heat-results")
    try:
        page.wait_for_selector("li")
        heats = page.query_selector_all("li")

        heat_ids = []
        for heat in heats:
            heat_id = heat.query_selector("a").get_attribute("href").split("/")[-1]
            heat_ids.append(heat_id)

        return heat_ids
    except:
        return None


def get_all_heats_for_month(page, base_url):
    page.goto(base_url + "/heat-results")

    page.wait_for_selector("li")
    heats = page.query_selector_all("li")

    heat_ids = []
    for heat in heats:
        heat_id = heat.query_selector("a").get_attribute("href").split("/")[-1]
        heat_ids.append(heat_id)

    return


def main() -> None:
    """
    Page is entirely generated using JavaScript so we need a driver to get the actual data.
    """

    location = ["delft", "amsterdam"]

    loc = "delft"
    base_url = f"https://reserveren-{loc}.raceplanet.nl"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False

        page = browser.new_page()
        ids = get_heat_ids(page, base_url)

        print(ids)


if __name__ == "__main__":
    main()

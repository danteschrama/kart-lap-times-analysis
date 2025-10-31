import locale
import time
from datetime import datetime

# Set the locale to Dutch
locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")

import numpy as np
import pandas as pd
import pyodbc as pyodbc
from playwright.sync_api import sync_playwright
from sqlalchemy import create_engine


def main():
    for loc in ["delft", "amsterdam"]:
        print(loc)

        latest_heat = get_latest_heat(loc)
        with sync_playwright() as p:
            browser = p.chromium.launch()  # headless=False

            base_url = f"https://reserveren-{loc}.raceplanet.nl"
            page = browser.new_page()
            page.goto(base_url + "/heat-results")

            # heats
            heat_id = []
            heat_name = []
            date = []
            time = []
            location = []
            try:
                page.wait_for_selector("h2")
                date_str = get_date(page.query_selector("h2").inner_text())

                page.wait_for_selector("li")
                heats = page.query_selector_all("li")  # li

                latest_heat_id = latest_heat.iloc[0]["heat_id"]
                for heat in heats:
                    if (
                        latest_heat_id
                        == heat.query_selector("a").get_attribute("href").split("/")[-1]
                    ):
                        print("breaking")
                        break

                    heat_id.append(
                        heat.query_selector("a").get_attribute("href").split("/")[-1]
                    )
                    heat_name.append(
                        heat.query_selector("a")
                        .query_selector_all("span")[-1]
                        .inner_text()
                    )
                    date.append(date_str)
                    time.append(
                        heat.query_selector("a")
                        .query_selector_all("span")[0]
                        .inner_text()
                        + ":00"
                    )
                    location.append(loc)
            except:
                pass

            heats_df = pd.DataFrame(
                {
                    "heat_id": heat_id,
                    "heat_name": heat_name,
                    "date": date,
                    "time": time,
                    "location": location,
                }
            )

            c = int(latest_heat.iloc[0]["sorting"])
            heats_df["sorting"] = list(reversed(range(c, c + heats_df.shape[0])))

            print(heats_df)

            # lap_times
            heats = []
            driver = []
            lap = []
            seconds = []
            try:
                if len(heat_id) > 0:
                    for heat in heat_id:
                        page.goto(base_url + "/heat-results/" + heat)

                        page.wait_for_selector("table")
                        columns = page.query_selector("thead").query_selector_all("th")
                        rows = page.query_selector("tbody").query_selector_all("tr")

                        for row in rows:
                            driver_str = row.query_selector_all("th")[2].inner_text()

                            laps = row.query_selector_all("td")
                            for i in range(len(laps)):
                                heats.append(heat)
                                driver.append(driver_str[0:50])
                                lap.append(columns[i + 4].inner_text())
                                seconds.append(laps[i].inner_text().replace(",", "."))

            except:
                pass

            browser.close()

            lap_times_df = pd.DataFrame(
                {
                    "heat_id": heats,
                    "driver": driver,
                    "lap": lap,
                    "seconds": seconds,
                }
            ).replace("", np.nan)
            print(lap_times_df)

            # https://reserveren-delft.raceplanet.nl/heat-results/4360F0071F9D4455B0746B8C5DF6F895

            lap_times_df["lap"] = lap_times_df["lap"].astype("int")
            lap_times_df["seconds"] = lap_times_df["seconds"].astype("float")
            lap_times_df["position"] = lap_times_df.groupby(["heat_id", "lap"])[
                "seconds"
            ].rank(method="min")


if __name__ == "__main__":
    main()

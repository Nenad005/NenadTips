from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument('headless')
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("useAutomationExtension", False)
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
driver = webdriver.Chrome(service= Service(executable_path="""C:/dev/Enterprise/NenadTips/scraper/chromedriver.exe"""), options=options)
driver.get("https://www.soccerbet.rs/sr/sportsko-kladjenje/fudbal/S")
time.sleep(8)
driver.execute_script('document.querySelector("body > app-root > ng-component > ion-app > div > ds-main-layout > ds-main-layout-desktop > ion-row > ion-row > div.DESK-content--center > ion-router-outlet > ds-offer > ion-content > ds-offer-landing > ds-offer-landing-desk > ds-offer-type-filter > ion-row > ion-button.offer-type-filter--btn.offer-type-filter--btn-calendar.ion-color.ion-color-clear.ios.button.button-solid.ion-activatable.ion-focusable.hydrated").shadowRoot.querySelector("button").click()')
time.sleep(1)
driver.execute_script('document.querySelector("body > app-root > ng-component > ion-app > div > ds-main-layout > ds-main-layout-desktop > div > ion-row > ds-time-offer-filter > ion-row > ion-button:nth-child(4)").shadowRoot.querySelector("button").click()')
time.sleep(1)
def scroll_to_bottom(driver):
    prev_children_count = -1
    same_count_times = 0
    while same_count_times < 8:
        children_count = driver.execute_script('return document.querySelector("body > app-root > ng-component > ion-app > div > ds-main-layout > ds-main-layout-desktop > ion-row > ion-row > div.DESK-content--center > ion-router-outlet > ds-offer > ion-content > ds-offer-landing > ds-offer-landing-desk > div:nth-child(4) > ds-matches-by-time-container").children.length')
        print(children_count)
        if children_count == prev_children_count:
            same_count_times += 1
        else:
            same_count_times = 0
        prev_children_count = children_count
        driver.execute_script('document.querySelector("body > app-root > ng-component > ion-app > div > ds-main-layout > ds-main-layout-desktop > ion-row > ion-row > div.DESK-content--center > ion-router-outlet > ds-offer > ion-content").scrollByPoint(1000, 1000)')
        time.sleep(1)

scroll_to_bottom(driver)
# input()
driver.close()

# document.querySelector("body > app-root > ng-component > ion-app > div > ds-main-layout > ds-main-layout-desktop > ion-row > ion-row > div.DESK-content--center > ion-router-outlet > ds-offer > ion-content > ds-offer-landing > ds-offer-landing-desk > div:nth-child(4) > ds-matches-by-time-container").children.length

# document.querySelector("body > app-root > ng-component > ion-app > div > ds-main-layout > ds-main-layout-desktop > ion-row > ion-row > div.DESK-content--center > ion-router-outlet > ds-offer > ion-content").scrollByPoint(1000, 1000)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class GoogleFormScrapper:
    def __init__(self, driver_type="chrome"):
        if driver_type == "chrome":
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=chrome_options)
        elif driver_type == "firefox":
            firefox_options = FirefoxOptions()
            firefox_options.add_argument("--headless")
            self.driver = webdriver.Firefox(options=firefox_options)
        else:
            raise ValueError("Invalid driver type. Choose either 'chrome' or 'firefox'")

    def scrape(self, url):
        try:
            self.driver.get(url)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@role='list']/div[@role='listitem']")
                )
            )

            questions = self.driver.find_elements(
                By.XPATH, "//div[@role='listitem' and not(@jsaction)]"
            )
            question_data = []
            for question in questions:
                question_data.append(question.get_attribute("outerHTML"))

            return question_data

        finally:
            self.driver.quit()


if __name__ == "__main__":
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSd9gli7KqnYFNkrc_PWNxvmhi7ZJz2jPp0qTsceqT7lkIBo2Q/viewform"
    scrapper = GoogleFormScrapper()
    questions = scrapper.scrape(form_url)
    print(f"Number of Questions scrapped: {len(questions)}")

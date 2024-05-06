from time import sleep

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import Chrome

LABORMED_RESULTS_URL = "https://shift.labormed.net.br/shift/lis/labormed/elis/s01.iu.web.Login.cls?config=UNICO"
WEBDRIVER_RENDER_TIMEOUT_SECONDS = 10
PRODUCT_PURCHASE_INTERVAL_SECONDS = 5
GAME_TIMEOUT_MINUTES = 5


def buy_products(driver):
    best_product = driver.find_elements(By.XPATH,
                                        "/html/body/div/div[2]/div[19]/div[3]/div[6]"
                                        "/div[@class='product unlocked enabled'][last()]")

    if len(best_product) > 0:
        product_info = best_product[0].text.split("\n")
        name = product_info[0]
        cost = product_info[1]
        print(f"Bought {name} for {cost} cookies")
        best_product[0].click()


def find_element_if_visible(locator, driver):
    wait = WebDriverWait(driver, WEBDRIVER_RENDER_TIMEOUT_SECONDS)
    return wait.until(ec.visibility_of_element_located(locator))


def get_cookie_rate(driver):
    while True:
        try:
            cookies_per_second = driver.find_element(By.ID, "cookiesPerSecond").text
            return cookies_per_second.replace("per second: ", "")
        except StaleElementReferenceException:
            pass


def main():
    driver = Chrome()
    driver.get(LABORMED_RESULTS_URL)

    user_text_input = find_element_if_visible((By.XPATH, "//*[@id='control_40']"), driver)
    user_text_input.send_keys("")

    password_input = find_element_if_visible((By.XPATH, "//*[@id='control_42']"), driver)
    password_input.send_keys("")

    login_button = find_element_if_visible((By.XPATH, "//*[@id='control_51']"), driver)
    login_button.click()

    find_element_if_visible((By.CLASS_NAME, "tpOdd"), driver)
    results_status_table = driver.find_elements(By.XPATH,
                                                "/html/body/div[4]/table/tbody/tr[1]/td/div/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/div[6]/div[7]/div/div/div[8]/table/tbody/tr[1]/td/div/table/tbody/tr/td[4]")

    results_ready_list = [result_status for result_status in results_status_table if result_status.text == "Pronto"]

    if len(results_ready_list) > 0:
        driver.get("https://instantsfun.es/wp-content/uploads/2017/09/chan.mp3")
        sleep(4)
        driver.close()

    print(f"{len(results_ready_list)} prontos!")
    pass

    # language_selector = find_element_if_visible((By.XPATH, "//*[@id='langSelect-EN']"), driver)
    # language_selector.click()

    # cookie_button = find_element_if_visible((By.ID, "bigCookie"), driver)
    # product_purchase_interval = time.time() + PRODUCT_PURCHASE_INTERVAL_SECONDS
    # game_timeout = time.time() + 60 * GAME_TIMEOUT_MINUTES
    #
    # while time.time() <= game_timeout:
    #     cookie_button.click()
    #
    #     if time.time() >= product_purchase_interval:
    #         buy_products(driver)
    #         product_purchase_interval = time.time() + PRODUCT_PURCHASE_INTERVAL_SECONDS
    #
    # print(f"\nFinal rate: {get_cookie_rate(driver)} cookies/second")


if __name__ == "__main__":
    main()

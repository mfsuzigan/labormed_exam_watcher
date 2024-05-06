from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import Chrome

LABORMED_RESULTS_URL = "https://shift.labormed.net.br/shift/lis/labormed/elis/s01.iu.web.Login.cls?config=UNICO"
FOUND_SOUND_URL = "https://instantsfun.es/wp-content/uploads/2017/09/chan.mp3"
NOT_FOUND_SOUND_URL = "https://instantsfun.es/wp-content/uploads/2020/05/roblox-oof.mp3"
WEBDRIVER_RENDER_TIMEOUT_SECONDS = 10
PRODUCT_PURCHASE_INTERVAL_SECONDS = 5
GAME_TIMEOUT_MINUTES = 5


def find_element_if_visible(locator, driver):
    wait = WebDriverWait(driver, WEBDRIVER_RENDER_TIMEOUT_SECONDS)
    return wait.until(ec.visibility_of_element_located(locator))


def main():
    driver = Chrome()
    login(driver)

    while True:

        if not ready_results_exist(driver):
            print("No results ready for now")
            play_sound(driver, NOT_FOUND_SOUND_URL)
            driver.get(LABORMED_RESULTS_URL)

    # print("Finished")


def ready_results_exist(driver):
    find_element_if_visible((By.CLASS_NAME, "tpOdd"), driver)
    results_status_table = driver.find_elements(By.XPATH,
                                                "/html/body/div[4]/table/tbody/tr[1]/td/div/table/tbody/tr["
                                                "2]/td/div/table/tbody/tr/td/div/div[6]/div[7]/div/div/div["
                                                "8]/table/tbody/tr[1]/td/div/table/tbody/tr/td[4]")
    results_ready_list = [result_status for result_status in results_status_table if result_status.text == "Pronto"]
    read_results_exist = len(results_ready_list) > 0

    while read_results_exist:
        print("New results are in!")
        play_sound(driver, FOUND_SOUND_URL)

    print(f"{len(results_ready_list)} ready!")
    return read_results_exist


def play_sound(driver, sound_url):
    driver.get(sound_url)
    sleep(4)


def login(driver):
    driver.get(LABORMED_RESULTS_URL)
    user_text_input = find_element_if_visible((By.XPATH, "//*[@id='control_40']"), driver)
    user_text_input.send_keys("")
    password_input = find_element_if_visible((By.XPATH, "//*[@id='control_42']"), driver)
    password_input.send_keys("")
    login_button = find_element_if_visible((By.XPATH, "//*[@id='control_51']"), driver)
    login_button.click()


if __name__ == "__main__":
    main()

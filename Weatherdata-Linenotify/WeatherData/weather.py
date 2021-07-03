import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tqdm import tqdm


options = Options()
# headlessモードを使用する
options.add_argument('--headless')
# headlessモードで暫定的に必要なフラグ(そのうち不要になる)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--start-maximized')          # 起動時にウィンドウを最大化する


driver_path = 'Weatherdata_Linenotify/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path, options=options)
driver.execute_cdp_cmd(
    "Browser.grantPermissions",
    {
        "origin": "https://tenki.jp/",
        "permissions": ["geolocation"]
    },
)
driver.execute_cdp_cmd(
    "Emulation.setGeolocationOverride",
    {
        "latitude": 35.74817193409818,      # 東京電機大学千住キャンパス
        "longitude": 139.80610202266766,
        "accuracy": 100,
    },
)
# 要素が見つかるまで最大10秒待機
driver.implicitly_wait(10)

driver.get('https://tenki.jp/')


class Weather:

    # cssセレクターから要素を取得する
    def getElement(self, css_selector, wait_second, retries_count):

        error_message = ''
        for _ in range(retries_count):
            try:
                selector = css_selector
                element = WebDriverWait(driver, wait_second).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, selector))
                )
            except TimeoutException as e:
                # エラーメッセージを格納
                error_message = e
            else:
                # 失敗しなかったらループから抜ける
                break
        else:
            # リトライが全て失敗した場合の処理

            #  プログラムの強制終了
            sys.exit()

        return element

    # 雨雲レーダーの画像を取得し保存
    def get_rainCloud_img(self):

        print('雨雲レーダーの画像を取得中...')
        bar = tqdm(total=100)

        self.getElement(
            '#menu-basis > li:nth-child(1) > a > span', 30, 3).click()

        bar.update(14)

        self.getElement('#pc_map_bottom_link', 30, 3).click()

        bar.update(14)

        self.getElement('#ymap_gps_search > a', 30, 3).click()

        bar.update(14)

        self.getElement(
            '#ymap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div > a.leaflet-control-zoom-in', 30, 3).click()

        bar.update(14)

        self.getElement(
            '#ymap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div > a.leaflet-control-zoom-in', 30, 3).click()

        bar.update(14)

        self.getElement(
            '#ymap > div.leaflet-control-container > div.leaflet-top.leaflet-left > div > a.leaflet-control-zoom-in', 30, 3).click()

        bar.update(14)

        w = driver.execute_script("return document.body.scrollWidth;")
        h = driver.execute_script("return document.body.scrollHeight;")

        # set window size
        driver.set_window_size(w, h)

        time.sleep(3)

        # Get Screen Shot
        png = driver.find_element_by_css_selector('#ymap')
        png.screenshot("screen.png")

        bar.update(16)

        print("雨雲レーダーの画像、取得完了！")

        driver.get('https://tenki.jp/')  # トップページに戻る

    # 現在値周辺の降水確率を取得

    def get_rainfall(self):

        print("降水確率を取得中...")
        bar = tqdm(total=100)

        self.getElement('#body-search-gps > a', 30, 3).click()

        bar.update(33)

        self.getElement(
            '#main-column > section > ul > li.forecast-select-1h > a', 30, 3).click()

        bar.update(33)

        rainfall = self.getElement(
            '#forecast-point-1h-today > tbody > tr.prob-precip', 30, 3).text

        bar.update(34)

        rainfall_list = rainfall.split(' ')  # rainfall_list[0] = '降水確率'
        rainfall_list.pop(0)

        print("降水確率、取得完了！")

        driver.get('https://tenki.jp/')  # トップページに戻る

        return rainfall_list  # 24時までの降水確率

    # 現在値周辺の気温を取得
    def get_tempareture(self):

        print("気温を取得中...")
        bar = tqdm(total=100)

        self.getElement('#body-search-gps > a', 30, 3).click()

        bar.update(33)

        self.getElement(
            '#main-column > section > ul > li.forecast-select-1h > a', 30, 3).click()

        bar.update(33)

        temp = self.getElement(
            '#forecast-point-1h-today > tbody > tr.temperature', 30, 3).text

        bar.update(34)

        temp_list = temp.split(' ')

        print("気温、取得完了！")

        driver.get('https://tenki.jp/')  # トップページに戻る

        return temp_list  # 24時までの気温

    # 現在値周辺の天気の様子を取得
    def get_weather(self):

        print("天気の様子を取得中...")
        bar = tqdm(total=100)

        self.getElement('#body-search-gps > a', 30, 3).click()

        bar.update(33)

        self.getElement(
            '#main-column > section > ul > li.forecast-select-1h > a', 30, 3).click()

        bar.update(33)

        weather = self.getElement(
            '#forecast-point-1h-today > tbody > tr.weather', 30, 3).text

        bar.update(34)

        weather_list = weather.split('\n')  # weather_list[0] = '天気'
        weather_list.pop(0)

        print("天気の様子、取得完了！")

        driver.get('https://tenki.jp/')  # トップページに戻る

        return weather_list  # 24時までの天気

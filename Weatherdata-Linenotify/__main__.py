import datetime

from WeatherData import weather as wd
from Line import LineNotify as l
from Line import sendtext as st


def main():

    w = wd.Weather()

    w.get_rainCloud_img()  # 雨雲レーダーの画像を取得

    weather_list = w.get_weather()  # 天気のリスト
    temp_list = w.get_tempareture()  # 気温のリスト
    rainfall_list = w.get_rainfall()  # 降水確率のリスト
    time, item, border = st.get_message_comp()  # 文字列など

    text = []
    dt_now = datetime.datetime.now()
    nowHour = int(dt_now.strftime('%H'))

    for i in range(nowHour-1, 24):
        text.append(time[i] + "時:" + "  " + weather_list[i] +
                    "   " + temp_list[i]+"℃" + "   " + rainfall_list[i]+"%")

    message = "\n" + item + "\n" + border + "\n" + '\n'.join(text)

    l.send_line_notify(message)


if __name__ == '__main__':
    main()

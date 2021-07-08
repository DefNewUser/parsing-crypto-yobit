import requests


def get_info():
    """
    весь список торгующих пар и их информация.
    :return:
    """
    response = requests.get(url="http://yobit.net/api/3/info")

    with open("info.txt", 'w') as file:
        file.write(response.text)

    return response.text


def get_ticker(coin_one="btc", coin_two="usdt"):
    """
    Парсим конкретные пары
    :return:
    """
    # response = requests.get(url="http://yobit.net/api/3/ticker/btc_usdt-eth_usdt-xrp_usdt?ignore_invalid=1")
    response = requests.get(url=f"http://yobit.net/api/3/ticker/{coin_one}_{coin_two}?ignore_invalid=1")

    with open("ticker.txt", "w") as file:
        file.write(response.text)

    return response.text


def get_depth(coin1="btc", coin2="usdt", limit=200):
    """
    Парсим глубину стакана с ордерами
    :param coin1:
    :param coin2:
    :param limit: глубина стакана
    :return:
    """
    response = requests.get(url=f"http://yobit.net/api/3/depth/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")

    with open("depth.txt", "w") as file:
        file.write(response.text)

    # получаю доступ к к ключу bids, где значения списки с ордерами а покупку
    bids = response.json()[f"{coin1}_usdt"]["bids"]

    total_bits_amount = 0
    for item in bids:
        price = item[0]
        coin_amount = item[1]

        total_bits_amount += price * coin_amount

    return f"Total bids: {total_bits_amount} $"


def get_trades(coin1="btc", coin2="usdt", limit=2000):
    """
    Парсим совершённые трейды и сумируем объём покупки и продажи
    :param coin1:
    :param coin2:
    :param limit:
    :return:
    """
    response = requests.get(url=f"http://yobit.net/api/3/trades/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")

    with open("trades.txt", "w") as file:
        file.write(response.text)

    total_trade_ask = 0
    total_trade_bid = 0
    for item in response.json()[f"{coin1}_{coin2}"]:
        if item["type"] == "ask":
            # Перемножаем прайс на кол-во проданных монет = сумма сделки
            total_trade_ask += item["price"] * item["amount"]
        else:
            total_trade_bid += item["price"] * item["amount"]

    # информативные принты
    info = f"[-] TOTAL {coin1} SELL: {round(total_trade_ask, 2)} $\n[+] TOTAL {coin2} BUY: {round(total_trade_bid, 2)} $"

    return info


def main():
    # print(get_info())
    # print(get_ticker())
    # print(get_ticker(coin_one="eth"))
    # print(get_depth())
    print(get_trades())


if __name__ == '__main__':
    main()

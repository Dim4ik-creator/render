import aiohttp
import asyncio
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}


# Асинхронные функции для парсинга сайтов
async def pars_obi_async():
    base_url = "https://obi.ru/instrument"
    max_pages = 2
    catalog = []

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [fetch_page(session, f"{base_url}?PAGEN_1={page}") for page in range(1, max_pages + 1)]
        pages_content = await asyncio.gather(*tasks)

        for html in pages_content:
            soup = BeautifulSoup(html, "html.parser")
            products = soup.select("div.FuS7R")
            for product in products:
                name = product.select_one("._1UlGi").get_text(strip=True) if product.select_one(
                    "._1UlGi") else "Название не найдено"
                price = product.select_one("._3IeOW").get_text(strip=True)[:-1] if product.select_one(
                    "._3IeOW") else "Цена не указана"
                image = product.find("source").get("srcset").split(',')[0].split(' ')[0] if product.find(
                    "source") else "Изображение отсутствует"
                url = 'https://obi.ru' + product.select_one("a")['href'] if product.select_one(
                    "a") else "URL отсутствует"
                catalog.append({"name": name, "price": price, "image": image, "url": url})
            # print(catalog)
    return catalog


async def pars_rostovinstrument_async():
    url = "https://rostovinstrument.ru/catalog/elektroinstrument/"
    catalog = []

    async with aiohttp.ClientSession(headers=headers) as session:
        html = await fetch_page(session, url)
        soup = BeautifulSoup(html, "html.parser")
        products = soup.find_all("div", class_="list_item_wrapp item_wrap item")

        for product in products:
            name = product.find("span").text.strip() if product.find("span") else "Название не найдено"
            price = product.find("span", class_="price_value").text.strip() if product.find("span",
                                                                                            class_="price_value") else "Цена не указана"
            image = "https://rostovinstrument.ru" + product.find("img").get("data-src") if product.find(
                "img") else "Изображение отсутствует"
            url = "https://rostovinstrument.ru" + product.find("a").get("href") if product.find(
                "a") else "URL отсутствует"
            catalog.append({"name": name, "price": price, "image": image, "url": url})
    return catalog


async def pars_instrumentdon_async():
    base_url = "https://instrumentdon.ru/catalog/"
    max_pages = 2
    catalog = []

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [fetch_page(session, f"{base_url}?PAGEN_1={page}") for page in range(1, max_pages + 1)]
        pages_content = await asyncio.gather(*tasks)

        for html in pages_content:
            soup = BeautifulSoup(html, "html.parser")
            products = soup.find_all(class_="item_block col-4 col-md-3 col-sm-6 col-xs-6")

            for product in products:
                name = product.find(class_='item-title').text.strip() if product.find(
                    class_='item-title') else "Название не найдено"
                price = product.find(class_='price_value').text.strip() if product.find(
                    class_='price_value') else "Цена не указана"
                image = "https://instrumentdon.ru" + product.find("img").get("data-src") if product.find(
                    "img") else "Изображение отсутствует"
                url = "https://instrumentdon.ru" + product.find("a").get("href") if product.find(
                    "a") else "URL отсутствует"
                catalog.append({"name": name, "price": price, "image": image, "url": url})
    # print(catalog)
    return catalog


async def fetch_page(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


# Запуск всех функций
async def run_all_parsers():
    obi_data = await pars_obi_async()
    rostovinstrument_data = await pars_rostovinstrument_async()
    instrumentdon_data = await pars_instrumentdon_async()

    # print(f"OBI: {len(obi_data)} товаров.")
    # print(f"RostovInstrument: {len(rostovinstrument_data)} товаров.")
    # print(f"InstrumentDon: {len(instrumentdon_data)} товаров.")
    catalog = obi_data + rostovinstrument_data + instrumentdon_data
    return catalog
# print(*asyncio.run(run_all_parsers()))

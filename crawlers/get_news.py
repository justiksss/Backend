import asyncio
import pprint

from PIL import Image
import httpx
from io import BytesIO
from bs4 import BeautifulSoup
from typing import Union


async def get_response(url: str) -> Union[httpx.Response,str]:
    try:
        response: httpx.Response = httpx.get(url, timeout=15)

        return response
    except:
        if response.status_code != 200:

            return "status code is not 200"


async def download_image(link: str) -> str:
    name_image = link.split("/")[-1].replace(".webp","")

    client = httpx.AsyncClient()
    response = await client.get(link)
    stream = BytesIO(response.content)

    image = Image.open(stream)
    image.save(f"/Users/oleksiiyudin/Documents/Backend/images/images_for_blog/{name_image}.png", "PNG")

    return name_image


async def info(link: str) -> dict:
    html = await get_response(link)

    data = BeautifulSoup(markup=html, features="lxml")

    time = data.find(name="span", class_="created").text
    all_info = data.find(name="div", class_="content").text.replace("\n","")

    info = [time,all_info]

    return info




async def get_info():
    posts = []

    for i in range(0,2):
        url = f"https://www.expats.cz/czech-news/daily-news/{i}"

        data = BeautifulSoup(markup=await get_response(url=url), features="lxml")

        blog = data.find(name="div", class_="content")  # general blocks
        title_subtext_view = [i.text.replace("\n", "") for i in blog.find_all(name="div", class_="info") if i.text != ""]

        image_block_and_link = blog.find_all(name="div", class_="image")

        more_info = [await info("https://www.expats.cz" + i.find_next(name="a").get("href")) for i in image_block_and_link]
        images_name = [await download_image("https://www.expats.cz" + i.find_next(name="img").get("src")) for i in image_block_and_link]

        """More info time - is 0, 1 - description"""
        new = [i for i in zip(more_info,images_name,title_subtext_view)]
        posts = []
        for post in new:
                new_post = {
                    "time": post[0][0],
                    "description":post[0][1],
                    "image_name": post[1],
                    "title": post[2]
                }
                posts.append(new_post)

    return posts




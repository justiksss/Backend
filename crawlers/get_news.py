import asyncio
import pprint
from datetime import datetime
from src.database.models import News
from PIL import Image
import httpx
from io import BytesIO
from bs4 import BeautifulSoup
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select



async def get_response(url: str) -> Union[httpx.Response,str]:
    try:
        response: httpx.Response = httpx.get(url, timeout=500)

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
    image.save(f"/Users/oleksiiyudin/Desktop/Backend/images/{name_image}.png", "PNG")

    return name_image


async def info(link: str) -> list:
    html = await get_response(link)

    data = BeautifulSoup(markup=html, features="lxml")

    time_info = data.find(name="span", class_="created").text
    time = time_info.replace("Published on ", "")
    datetime_format = "%d.%m.%Y %H:%M:%S"
    datetime_obj = datetime.strptime(time, datetime_format)
    all_info = data.find(name="div", class_="content")
    pag = [str(i.find_next(name="p")) for i in all_info.find_all(name="div", class_="widget text")]
    title = data.find(name="div",class_='title').text
    text = "".join(pag)
    title = title.split("\n")[1]
    info = [datetime_obj, text,title]

    return info


async def get_info() -> list:
    title_duplicate = []
    for i in range(0,5):
        url = f"https://www.expats.cz/czech-news/daily-news/{i}"

        data = BeautifulSoup(markup=await get_response(url=url), features="lxml")

        blog = data.find(name="div", class_="content")  # general blocks
        title_subtext_view = [i.text.replace("\n", "") for i in blog.find_all(name="div", class_="info") if i.text != ""]

        image_block_and_link = blog.find_all(name="div", class_="image")

        more_info = [await info("https://www.expats.cz" + i.find_next(name="a").get("href")) for i in image_block_and_link]
        images_name = [await download_image("https://www.expats.cz" + i.find_next(name="img").get("src")) for i in image_block_and_link]
        title = more_info[-1][-1]
        """More info, time - is 0, 1 - description"""
        new = [i for i in zip(more_info,images_name,title_subtext_view)]

        for post in new:




            news = News(
                title=post[0][-1],
                image_path=post[1],
                created_at=post[0][0],
                description=post[0][1]
            )

            await add_to_database(news)




async def add_to_database(post):
    DATABASE_URL = "postgresql+asyncpg://justiksss:HLGKrXbGHS7RFI2xv6aKmN9LbEl7tnPb@dpg-ci80c1enqql0ldenbru0-a.oregon-postgres.render.com/jobs_vgx8"

    engine = create_async_engine(
        DATABASE_URL,
        future=True,
        echo=True,
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession, autoflush=False
    )

    async with async_session() as session:
        async with session.begin():
            query = select(News).where(News.title == post.title)
            result = await session.execute(query)
            existing_news = result.scalar()

            if not existing_news:
                session.add(post)
                await session.flush()
            else:
                print("News post already exists:", post.title)















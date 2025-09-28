import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup

from schema import Article, create_get_category, add_article, cleanup_text


def extract_lapresse():
    url = "https://lapresse.ca"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        article_list = soup.find_all("article")

        for a in article_list:
            article_name = a.find("a", class_="storyCard__titleLink")
            article_name = article_name.text.strip() if article_name else None
            subtitle = a.find("a", class_="storyCard__suptitleLink")
            subtitle = subtitle.text.strip() if subtitle else None
            lead_text = a.find("a", class_="storyCard__leadLink")
            lead_text = lead_text.text.strip() if lead_text else None
            thumbnail = a.find("img", class_="storyCard__image")
            thumbnail = thumbnail.get("src") if thumbnail else None
            publish_date = a.find("span", class_="storyCard__publishedDate")
            publish_date = publish_date.text.strip() if publish_date else None
            category_name = a.find("a", class_="badge--section-INT")
            category_name = cleanup_text(category_name.text.strip()) if category_name else None

            article = Article()
            article.article_name = cleanup_text(article_name)
            article.subtitle = cleanup_text(subtitle)
            article.lead_text = cleanup_text(lead_text)
            article.thumbnail = thumbnail
            article.publish_date = cleanup_text(publish_date)

            if category_name is not None and category_name != "":
                category = create_get_category(category_name)
                article.categories.append(category)

            add_article(article)


if __name__ == '__main__':
    extract_lapresse()
    scheduler = BlockingScheduler()
    scheduler.add_job(extract_lapresse, 'cron', hour=8, minute=5)
    scheduler.start()

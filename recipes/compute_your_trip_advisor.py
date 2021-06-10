# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from bs4 import BeautifulSoup
import requests
import time
from googletrans import Translator
from deep_translator import GoogleTranslator

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def get_reviews(response):
    soup = BeautifulSoup(response.text, 'lxml')
    reviews = []
    review_container = soup.find_all(class_='review-container')
    for i in range(len(review_container)):
        review = review_container[i].find_all("p", class_='partial_entry')[0].text
        reviews.append(review)
    return reviews

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def translate_reviews(reviews):
    translator = GoogleTranslator(source='english', target='japanese')  # output -> Weiter so, du bist großartig

    #translator = Translator(service_urls=['translate.googleapis.com'])
    reviews_translated = []
    for review in reviews:
        translated = translator.translate(review)
        reviews_translated.append(translated)
    #translations = translator.translate(reviews, dest='ja')
    #for translation in translations:
    #    reviews_translated.append(translation.text)
    return reviews_translated

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def get_translated_reviews(url, max_page = 10):
    """
    対象のURLにアクセスする関数
    アクセスできない等のエラーが発生したら例外を投げる
    """
    # 接続確立の待機時間、応答待機時間を10秒とし、それぞれの値を超えた場合は例外が発生（ConnectTimeout）
    url_split = url.split('-Reviews-')
    reviews_all = []
    for i in range(max_page):
        page = i*10
        if page == 0:
            url_page = url
        else:
            url_page = url_split[0] + '-Reviews-or{}-'.format(page) + url_split[1]
        print(url_page)
        data = requests.get(url_page, timeout=10)
        data.encoding = data.apparent_encoding
        # アクセス過多を避けるため、2秒スリープ
        time.sleep(2)

        # レスポンスのステータスコードが正常(200番台)以外の場合は、例外を発生させる(HTTPError)
        if data.status_code != requests.codes.ok:
            break
        else:
            reviews = get_reviews(data)
            reviews_all.append(reviews)
    reviews_all = [item for sublist in reviews_all for item in sublist]
    reviews_translated = translate_reviews(reviews_all)
    zipped = zip(reviews_all, reviews_translated)
    trip_advisor_reviews_df = pd.DataFrame(set(zipped), columns=["en", "jp"])
    return trip_advisor_reviews_df

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#url = 'https://www.tripadvisor.com/Restaurant_Review-g187147-d10085290-Reviews-Kodawari_Ramen_Yokocho-Paris_Ile_de_France.html'
#url = 'https://www.tripadvisor.com.sg/Restaurant_Review-g294265-d8507071-Reviews-The_Ramen_Stall-Singapore.html'
#url = 'https://www.tripadvisor.com/Restaurant_Review-g294265-d5421132-Reviews-MENYA_SANJI_Singapore-Singapore.html'

client = dataiku.api_client()
project = client.get_project(dataiku.get_custom_variables()['projectKey'])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
project_variables = project.get_variables()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
project_variables

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
url = project_variables['local']['url']

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
trip_advisor_reviews_df = get_translated_reviews(url, max_page = 1)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
your_trip_advisor = dataiku.Dataset("your_trip_advisor")
your_trip_advisor.write_with_schema(trip_advisor_reviews_df)
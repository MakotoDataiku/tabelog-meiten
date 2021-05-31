# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
from bs4 import BeautifulSoup
import os
import re
import requests
import pandas as pd
import time
import dataiku
import bz2file

class TabelogScraping:
    """
    食べログから店名、ジャンル、評価点、口コミ件数、最新20件の口コミを取得する
    """
    def __init__(self, max_num):
        """
        インスタンス化した時点でスクレイピングを開始する
        食べログ（検索条件：東京都、バー、ランキング順）にアクセスする
        取得するページ件数は1ページ目からmax_numページ目までとする。
        """
        # スクレイピング対象となるお店のタグ
        self.TAGS = {'バー', 'ワインバー', 'バー・お酒（その他）', 'ラウンジ', 'ダイニングバー'}
        # スクレイピング対象となる評価点の下限値
        self.LOWER_LIMIT = 3.0
        # 口コミのURLへの不足部分
        self.RVW = 'dtlrvwlst/'
        # 取得したデータ一覧の保存場所
        # self.RESULT_PATH = folder_path
        # 取得したデータ一覧名
        self.RESULT_NAME = 'tabelog_summary.csv'
        # 取得した口コミデータフレームの列名
        self.COLUMNS = ['store_id', 'store_name', 'genre', 'rate', 'review_cnt', 'review', 'stars']
        # 検索するページ上限数
        self.max_num = max_num + 1
        self.shop_id = ''
        self.id_num = 1
        self.df = pd.DataFrame(columns = self.COLUMNS)

        try:
            first_time = time.time()
            for page_num in range(1, self.max_num):
                if page_num == 1:
                    # ランキング1ページ目
                    response = self.connect_url('https://tabelog.com/tokyo/rstLst/BC01/?SrtT=rt&Srt=D&sort_mode=1')
                else:
                    # ランキング2ページ目以降
                    response = self.connect_url('https://tabelog.com/tokyo/rstLst/BC01/' + str(page_num) + '/?SrtT=rt&Srt=D&sort_mode=1')

                # HTML解析用の変数
                soup = BeautifulSoup(response.text, 'lxml')

                # 一覧ページから以下の情報を取得する
                # ジャンルの取得
                genre_info = [genre.text.rstrip() for genre in soup.find_all('div', class_='list-rst__area-genre cpy-area-genre')]
                # 評価点の取得
                rate_list = [float(rate.text) for rate in soup.find_all('span', class_='c-rating__val c-rating__val--strong list-rst__rating-val')]
                # 口コミ件数の取得
                count_list = [count.text for count in soup.find_all('em', class_='list-rst__rvw-count-num cpy-review-count')]
                # 店名の取得
                raw_data = soup.find_all('a', class_='list-rst__rst-name-target cpy-rst-name js-ranking-num')
                shop_list = [name.text for name in raw_data]
                shop_url_list = [shop_url.get('href') for shop_url in raw_data]

                for i in range(20):
                    genre_tags = set(re.split('[\\s/、]+', genre_info[i].strip())[2:])
                    # ジャンル文字列が「バー、ワインバー、バー・お酒（その他）、ラウンジ、カフェ、ダイニングバー」の部分集合の場合、
                    # かつ評価点が「3.０以上」の場合、かつ、口コミ件数が１件以上存在する場合に処理を続ける
                    if not (genre_tags.issubset(self.TAGS) and rate_list[i] >= self.LOWER_LIMIT and int(count_list[i]) > 0):
                        continue

                    start_time = time.time()
                    self.shop_id = str(self.id_num).zfill(5)

                    # お店のURLに遷移し、口コミを20件(1ページ分)取得する
                    response = self.connect_url(shop_url_list[i] + self.RVW)
                    soup = BeautifulSoup(response.text, 'lxml')
                    review_url_list = soup.find_all('div', class_='rvw-item js-rvw-item-clickable-area')

                    # 各口コミページに遷移し、最新の口コミを取得する
                    for url in review_url_list:
                        review_detail_url = 'https://tabelog.com' + url.get('data-detail-url')
                        response = self.connect_url(review_detail_url)
                        soup = BeautifulSoup(response.text, 'lxml')
                        review = soup.find_all('div', class_='rvw-item__rvw-comment')
                        review = review[0].p.text.strip()
                        stars = soup.find_all('b', class_='c-rating-v2__val c-rating-v2__val--strong')
                        stars = stars[0].text.strip()
                        # pandasのデータフレームに格納
                        self.add_df(shop_list[i], genre_info[i].strip(), rate_list[i], count_list[i], review, stars)

                    # 1つのお店のスクレイピングが終了したら、その結果を保存する
                    self.write_result(shop_list[i], genre_info[i].strip(), rate_list[i], count_list[i])

                    process_time = time.time() - start_time
                    print('{}件目完了：　処理時間：{:.3f}秒'.format(self.id_num, process_time))

                    self.id_num += 1

        except requests.exceptions.HTTPError as e:
            print(e)
        except requests.exceptions.ConnectTimeout as e:
            print(e)
        finally:
            end_time = time.time() - first_time
            print('終了、処理時間：{:.3f}秒'.format(end_time))


    def connect_url(self, target_url):
        """
        対象のURLにアクセスする関数
        アクセスできない等のエラーが発生したら例外を投げる
        """
        # 接続確立の待機時間、応答待機時間を10秒とし、それぞれの値を超えた場合は例外が発生（ConnectTimeout）
        data = requests.get(target_url, timeout=10)
        data.encoding = data.apparent_encoding
        # アクセス過多を避けるため、2秒スリープ
        time.sleep(2)

        # レスポンスのステータスコードが正常(200番台)以外の場合は、例外を発生させる(HTTPError)
        if data.status_code == requests.codes.ok:
            return data
        else:
            data.raise_for_status()


    def write_result(self, name, genre, rate, count):
        """
        スクレイピング対象となるお店の一覧をログとして出力する関数
        
        file_path = os.path.join(self.RESULT_PATH, self.RESULT_NAME)
        with open(file_path, mode='a', encoding='utf-8') as f:
            f.write('{}, {}, {}, 評価：{}, 口コミ：{}件\n'.format(self.shop_id, name, genre, rate, count))
        """


    def add_df(self, name, genre, rate, count, comment, stars):
        """
        取得した口コミデータをデータフレームに格納する関数
        """
        se = pd.Series([self.shop_id, name, genre, rate, count, comment, stars], self.COLUMNS)
        self.df = self.df.append(se, self.COLUMNS)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# run this only once. It will take around 1 hour
result = TabelogScraping(5)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# file_path = dataiku.Folder("9FfqNxhm").get_path() + "/tabelog.csv"

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# result.df.to_csv(file_path, index=False)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
py_recipe_output = dataiku.Dataset("tabelog_w_stars")
py_recipe_output.write_with_schema(result.df)
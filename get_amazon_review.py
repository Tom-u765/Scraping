"""
ランサーズの案件ができるか実力を試してみる
https://www.lancers.jp/work/detail/3975668
参考
https://kamesuke-blog.com/programming/scraping_amazon/
"""
from time import sleep
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import textwrap
import csv
import chromedriver_binary

# mac
# chrome_path = 'C:/Users/デスクトップ/python/selenium_test/chromedriver'
# 　amazonのレビュー情報をseleniumで取得する_引数：amazonの商品URL
def get_amazon_page_info(url):
    text = ""  # 初期化
    # options = Options()  # オプションを用意
    # options.add_argument('--incognito')  # シークレットモードの設定を付与
    # 　chromedriverのパスとパラメータを設定
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(options=)
    driver.get(url)  # chromeブラウザでurlを開く
    driver.implicitly_wait(10)  # 指定したドライバの要素が見つかるまでの待ち時間を設定
    text = driver.page_source  # ページ情報を取得

    # driver.quit()  # chromeブラウザを閉じる

    return text  # 取得したページ情報を返す


# 全ページ分をリストにする
def get_all_reviews(url):
    review_list = []  # 初期化
    star_list = []
    title_list = []
    date_list = []

    i = 1  # ループ番号の初期化
    while True:
        print(i, 'page_search')  # 処理状況を表示
        i += 1  # ループ番号を更新
        text = get_amazon_page_info(url)  # amazonの商品ページ情報(HTML)を取得する
        amazon_bs = BeautifulSoup(text, features='lxml')  # HTML情報を解析する
        reviews = amazon_bs.select('.review-text')  # ページ内の全レビューのテキストを取得
        stars = amazon_bs.select('.a-icon-alt')
        titles = amazon_bs.select('.review-title-content')
        dates = amazon_bs.select('.review-date')#本当は日付だけとりたい
        for review, star, title, date in zip(reviews, stars, titles, dates):  # 取得したレビュー数分だけ処理を繰り返す
            review_list.append(review)  # レビュー情報をreview_listに格納
            star_list.append(star)
            title_list.append(title)
            date_list.append(date)

        next_page = amazon_bs.select('li.a-last a')  # 「次へ」ボタンの遷移先取得

        # 次のページが存在する場合
        if next_page != []:
            # 次のページのURLを生成
            next_url = 'https://www.amazon.co.jp/' + next_page[0].attrs['href']
            url = next_url  # 次のページのURLをセットする

            sleep(2)  # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:  # 次のページが存在しない場合は処理を終了
            break

    return review_list, star_list, title_list, date_list


# インポート時は実行されないように記載
if __name__ == '__main__':
    url_count = 0
    urls = [
        'https://www.amazon.co.jp/%E3%83%89%E3%82%A6%E3%82%B7%E3%82%B7%E3%83%A3-%E3%82%BF%E3%83%B3%E3%83%96%E3%83%A9%E3%83%BC-%E7%8C%AB%E8%88%8C%E5%B0%82%E7%A7%91%E3%82%BF%E3%83%B3%E3%83%96%E3%83%A9%E3%83%BC-320ml-%E3%82%B0%E3%83%AA%E3%83%BC%E3%83%B3/dp/B08MW6YQY5/ref=pd_rhf_cr_s_bmx_5?pd_rd_w=1MuoR&pf_rd_p=b35c88ee-075c-481c-ab75-32553855cd5b&pf_rd_r=W5W6QVTMA9PPK89776SH&pd_rd_r=49445fb8-416e-4f67-a3cf-6b650ea6659c&pd_rd_wg=mRwDl&pd_rd_i=B08MW6YQY5&psc=1',
        'https://www.amazon.co.jp/ステッドラー-多機能ペン-アバンギャルド-ブラストブラック-927AGL-MB/dp/B08KDZ6CK8/?_encoding=UTF8&pf_rd_p=937750cb-481a-4e61-8af9-3c5ed6ae80b9&pd_rd_wg=aXswQ&pf_rd_r=B5MC7RFBBGX9R9M5NB55&pd_rd_w=gZme2&pd_rd_r=819bc1cb-e41c-4ffb-a072-9bd73678e64f&ref_=pd_gw_bmx_gp_rg7jzt1o'

    ]
    for url in urls:

    # 　Amazon商品ページ
    #     url = 'https://www.amazon.co.jp/%E3%83%89%E3%82%A6%E3%82%B7%E3%82%B7%E3%83%A3-%E3%82%BF%E3%83%B3%E3%83%96%E3%83%A9%E3%83%BC-%E7%8C%AB%E8%88%8C%E5%B0%82%E7%A7%91%E3%82%BF%E3%83%B3%E3%83%96%E3%83%A9%E3%83%BC-320ml-%E3%82%B0%E3%83%AA%E3%83%BC%E3%83%B3/dp/B08MW6YQY5/ref=pd_rhf_cr_s_bmx_5?pd_rd_w=1MuoR&pf_rd_p=b35c88ee-075c-481c-ab75-32553855cd5b&pf_rd_r=W5W6QVTMA9PPK89776SH&pd_rd_r=49445fb8-416e-4f67-a3cf-6b650ea6659c&pd_rd_wg=mRwDl&pd_rd_i=B08MW6YQY5&psc=1'
        """
        アイデア1　for文で複数商品についてレビューの取得を行いたい 今回はやらんけどCSVにリンクを用意して読み込む形でもいいと思った
        アイデア2　今はレビュー本文しか取れてないけど、商品名・レビュータイトル・投稿日時・星・本文を取得したい
        
        """
        # URLをレビューページのものに書き換える
        review_url = url.replace('dp', 'product-reviews')
        # レビュー情報の取得
        review_list, star_list, title_list, date_list = get_all_reviews(review_url)
        print(get_all_reviews(review_url))
        # CSVにレビュー情報の書き出し
        # with open('data/sample.csv','w') as f:　#Windowsでエンコードエラーになる場合があるため下の行に変更
        with open(f'./reviews-{url_count}.csv', 'a', encoding='utf-8') as f: #フォルダは作れない？
            writer = csv.writer(f, lineterminator='\n')

            # 全データを表示
            for i in range(len(review_list)):
                csvlist = []
                review_text = textwrap.fill(review_list[i].text, 500)
                star_text = textwrap.fill(star_list[i].text, 500)
                title_text = textwrap.fill(title_list[i].text, 500)
                date_text = textwrap.fill(date_list[i].text, 500)
                # データ作成
                csvlist.append('No.{} : '.format(i + 1))  # 便宜上「No.XX」の文字列を作成
                csvlist.append(review_text.strip())  # レビューテキストの先頭・末尾の空白文字を除去
                csvlist.append(star_text) #appendは要素1つしか受け付けないのでとりあえず分ける
                csvlist.append(title_text)
                csvlist.append(date_text)
                # 出力
                writer.writerow(csvlist)
                # ファイルクローズ
            f.close()

        # driver.quit()
        url_count +=1
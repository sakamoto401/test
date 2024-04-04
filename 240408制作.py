import requests
from bs4 import BeautifulSoup
import os
#requestsを使って画像URLを取得し、BeautifulSoupを使ってHTMLを解析。

def fetch_image_urls(query, max_links_to_fetch, headers):
#Google Imagesから画像のURLを取得するための関数
    image_search_url = f"https://www.google.com/search?tbm=isch&q={query}"
    #Google Imagesの検索結果ページのURLを構築
    response = requests.get(image_search_url, headers=headers)
    response.raise_for_status()
    #構築したURLに対して画像検索結果ページのデータを取得
    #エラーがあれば例外を発生
    soup = BeautifulSoup(response.text, 'html.parser')
    #取得したHTMLデータをBeautifulSoupで解析し、HTMLの要素を取得
    

    image_urls = [] #画像のURLを格納するための空のリストを作成
    for img in soup.select('img'): #HTMLからすべてのimg要素を取得
        if 'src' in img.attrs: #取得したimg要素の属性にsrc、画像のURLが存在するか
            image_url = img.attrs['src'] #取得
            if image_url.startswith('http'):
                image_urls.append(image_url) #取得したURLがHTTPまたはHTTPSで始まるか確認し、追加

    return image_urls[:max_links_to_fetch] #指定された数の画像のURLのみが取得

def download_images(urls, save_dir): #ダウンロードする画像のURLリストを表す引数, 画像を保存するディレクトリ
    os.makedirs(save_dir, exist_ok=True) #指定された保存先ディレクトリの作成
    for i, url in enumerate(urls): #enumerate関数を使うことで、インデックスとURLを同時に取得
        response = requests.get(url)
        response.raise_for_status() #画像データを取得
        with open(f'{save_dir}/image_{i+1}.jpg', 'wb') as f:
            f.write(response.content) #バイナリーモードで保存するためのファイルを開き、書き込み

if __name__ == '__main__':
    search_query = '猫'  # 検索したいキーワードを設定
    max_images_to_download = 10  # ダウンロードする画像の最大数を設定
    save_directory = 'cat_images'  # 画像を保存するディレクトリを設定

    # ヘッダーを設定してHTTPリクエストを送信
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    image_urls = fetch_image_urls(search_query, max_images_to_download, headers)
    download_images(image_urls, save_directory)
    #先に定義されたfetch_image_urls関数とdownload_images関数を使って、
    #画像のURLを取得し、ダウンロードして保存する処理

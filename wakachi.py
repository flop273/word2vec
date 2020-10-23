from janome.tokenizer import Tokenizer
import re
import zipfile
import urllib.request
import os.path,glob

#ダウンロードしたいURLを入力する
URL = 'https://www.aozora.gr.jp/cards/001562/files/52410_ruby_51060.zip'
#分かち書き作成ファイル
WAKATI = 'wakachi_text.txt'


def main():
    download_text = download(URL)
    text = convert(download_text)

    #分かち書き作成
    write_wakachi_text(word_analyze(text))


def write_wakachi_text(results):
    write_file = WAKATI
    with open(write_file, 'w', encoding='utf-8') as fp:
        fp.write("\n".join(results))


def word_analyze(text):
    t = Tokenizer()
    results = []
    lines = text.split("\r\n")
 
    for line in lines:
        tokens = t.tokenize(line)
        r = []
        for token in tokens:
            w = token.surface
            ps = token.part_of_speech
            hinshi = ps.split(',')[0]
            r.append(w)
        rl = (" ".join(r)).strip()
        print(rl)
        results.append(rl)
 
    return results


def convert(download_text):
    binarydata = open(download_text, 'rb').read()
    text = binarydata.decode('shift_jis')
 
    # ルビ、注釈などの除去
    text = re.split(r'\-{5,}', text)[2]
    text = re.split(r'底本：', text)[0]
    text = re.sub(r'《.+?》', '', text)
    text = re.sub(r'［＃.+?］', '', text)
    text = text.strip()
    return text


def download(url):
    # データファイルをダウンロードする
    zip_file = re.split(r'/', url)[-1]
    
    if not os.path.exists(zip_file):
        print('Download URL')
        print('URL:',url)
        urllib.request.urlretrieve(url, zip_file)
    else:
        print('Download File exists')

    # フォルダの生成
    dir, ext = os.path.splitext(zip_file)
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    # zipファイルの展開
    zip_obj = zipfile.ZipFile(zip_file, 'r')
    zip_obj.extractall(dir)
    zip_obj.close()

    # zipファイルの削除
    os.remove(zip_file)

    # テキストファイルの抽出
    path = os.path.join(dir,'*.txt')
    list = glob.glob(path)
    return list[0]


if __name__ == "__main__":
    main()
# Pythonをインストールし、仮想環境を生成する

```sh
$ python -m venv env
$ env/Scripts/activate
```

# 必用なライブラリのインストール

```sh
$ python -m pip install --upgrade pip setuptools

# PyTorchのインストール
# 正確なインストールコマンドについては https://pytorch.org/get-started/locally/ を参照せよ
$ pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116

# diffuesersをインストール
$ pip install transformers ftfy diffusers
```


## Waifu Diffusionのために追加でインストールする

```sh
$ pip install scipy
```

# モデルへのアクセストークンを生成する

[https://huggingface.co/CompVis/stable-diffusion-v1-4](https://huggingface.co/CompVis/stable-diffusion-v1-4)へアクセスし、ログイン無いしアカウント生成をすると、同意ボタンがあらわれる

同意してトークンを生成すると、[自身の設定ページ(https://huggingface.co/settings/tokens)](https://huggingface.co/settings/tokens)にトークンが生成される

# `generate.py`を起動する

必要なライブラリをインストールする

```
$ pip install click dotenv
```

`.env`ファイルを作成し、`STABLE_DIFFUSION_TOKEN`というキーで前述のモデルへのアクセストークンを環境変数として登録する

生成ログを保存するためのJSONファイルを作成し、中身を`[]`という空リストにしておく

以下のフォルダを作成する

- stable
- stable/nsfw
- waifu
- waifu/nsfw

その後、起動する

起動例：

```
$ python generate.py stable --prompt "cat" -j "log.json"
$ python generate.py waifu --nsfw --prompt "two girls, bikini, beach, moon" -j "log.json" -n 10 -h 640
```


使うことができるオプションを知る場合には`--help`オプションを付けて起動せよ


# GUI版の起動

追加でライブラリをインストールする

```sh
$ pip install PySimpleGUI
```


その後、logファイルやフォルダの準備を`generate.py`のときと同様に準備した後、起動する

```sh
$ python generate_gui.py
```


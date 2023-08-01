# electry_datamap

## 目的

TODO: このシステムの作成目的を記述します


## Description

TODO: このシステムの概要・説明を入力します


## ローカル開発環境の構築手順

### 1. リポジトリのクローン

#### 1-1. プロジェクトを配置するディレクトリに移動します

```shell
cd path/to/your-project-directory
```

#### 1-2. GitHubリポジトリからクローンします

```shell
git clone git@github.com:Hirakawa-Kaishi-Zemi/electry_datamap.git
```

#### 1-3. プロジェクトディレクトリに移動する

```shell
cd electry_datamap
```

以降の作業は、プロジェクトディレクトリで行います。

### 2. Python 仮想環境のセットアップ (スキップ可)

**((( このステップは省略可能です )))**

#### 2-1. 仮想環境の作成

Pythonの仮想環境は、Pythonのプロジェクトごとに独立した環境を作成するためのツールです。
これにより、異なるプロジェクトで異なるバージョンのPythonやPythonのライブラリを使用することが可能になります。

```shell
python3 -m venv venv
```

このコマンドを実行すると、現在のディレクトリにvenvという名前の新しいディレクトリが作成されます。

このディレクトリ内には、Pythonのインタープリタや必要なライブラリがインストールされ、この環境は他のPythonの環境から完全に隔離されます。

Pythonの仮想環境は、プロジェクトごとにPythonの環境を分離し、プロジェクトの依存関係を管理するための非常に便利なツールです。

#### 2-2. 仮想環境を有効にする

- Unix/Linux/MacOS

```shell
source venv/bin/activate
```

- Windows

```shell
.\venv\Scripts\activate
```

ターミナルプロンプトに、`(venv)`などの接頭辞が付いていれば正常に起動しています。


---

なお、仮想環境を無効化するには、以下のコマンドを実行します。

```shell
deactivate
```

### 3. 依存関係のインストール

#### 3-1. pip の更新

パッケージ管理ツール`pip`を最新の状態に更新します。

```shell
python -m pip install -U pip
```

#### 3-2. `pip` による依存関係の解決

```shell
pip install -r requirements.txt
```

### 4. 電力データマップの起動

Pythonファイルを実行し、Webアプリを起動します。

```shell
python electry_map.py
```

# 金融データ分析による積立投資戦略の考察

yfinanceライブラリを用いて各種金融商品の価格推移データを取得し、市場平均を超えるパフォーマンスを目指す積立投資戦略について分析・考察するプロジェクトです。

---

## ✨ 主な内容

* **データ取得**: `yfinance`を利用して、S&P 500 (VOO)や全世界株式(VT)などの株価・ETFの時系列データを取得します。
* **データ分析**: Jupyter Notebookを使い、取得したデータを可視化し、リターンやリスクなどの基本的な分析を行います。
* **戦略考察**: 単純なドルコスト平均法（定期積立）に加え、下落局面で投資額を増やすなどの戦略がパフォーマンスに与える影響をシミュレーションし、比較・考察します。

---

## 🚀 必要なもの

* [Visual Studio Code](https://code.visualstudio.com/)
* [VS Code Dev Containers 拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) （**必ず起動しておいてください**）

---

## ✨ セットアップと使い方

1. **リポジトリをクローンする**

    ```bash
    git clone https://github.com/miuraDS/financial_analytics.git
    ```

2. **VS Codeで開く**
    クローンしたフォルダをVS Codeで開きます。
3. **コンテナで再度開く**
    VS Codeが`.devcontainer`フォルダを検知し、右下に表示される「**Reopen in Container**」ボタンをクリックします。

4. **分析を開始する**
    初回は環境構築に数分かかります。完了後、`notebooks/financial_analytics.ipynb`を開けば、すぐに分析を開始できます。ライブラリのインストールなどは一切不要です。

-----

## 📊 分析例

プロジェクト内のNotebookでは、以下のような分析を行っています。

**各金融資産の対数価格の回帰分析**
対数価格の回帰直線を可視化し、その傾きから平均的な年間リターン（ドリフト率）を概算します。

![分析結果の例](./images/apple_regression.png)

-----

## 📂 ディレクトリ構成

```plaintext
financial_analytics/
├── .devcontainer/         # Dev Container設定
│   ├── devcontainer.json  # VS Codeへの指示書
│   └── Dockerfile         # 環境の設計図
├── .venv/                 # 仮想環境 (ローカル用)
├── data/                  # 分析用データ
├── notebooks/             # Jupyter Notebook
├── src/                   # Pythonソースコード
├── images/                # README用画像
├── .gitignore             # Git無視リスト
├── pyproject.toml         # 依存関係リスト
├── uv.lock                # 依存関係ロックファイル
└── README.md              # このファイル
```

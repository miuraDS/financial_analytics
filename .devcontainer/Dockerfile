# Microsoftが提供する公式のPython 3.11開発コンテナイメージをベースにする
FROM mcr.microsoft.com/devcontainers/python:3.11

# Rust製ツールをインストールするための環境をセットアップ
# uvのインストールにpipxを使うため、先にpipxをインストール
RUN pip install --upgrade pip && \
    pip install pipx && \
    pipx ensurepath

# pipxを使ってuvをインストール
RUN pipx install uv

import pandas as pd
from pathlib import Path
from curl_cffi import requests
# session = requests.Session(impersonate="chrome")
import yfinance as yf
import time
import shutil
import os
from typing import Dict, Any

def update_and_load_asset_data(
    assets: dict,
    data_folder: Path,
    today_str: str,
    session: requests.Session
) -> dict:
    """
    各アセットのデータをファイルから読み込むか、なければダウンロードして更新する。

    Args:
        assets (dict): アセット名とティッカー情報を含む辞書。
        data_folder (Path): データを保存/読み込みするフォルダのパス。
        today_str (str): 今日の日付文字列 ('YYYYMMDD')。
        session (requests.Session): yfinanceダウンロード用のセッション。

    Returns:
        dict: アセット名をキー、DataFrameを値とするデータの辞書。
    """
    data_dict = {}
    for name, info in assets.items():
        # 保存ファイルパスを生成
        start_date_str = info['start'].replace('-', '')
        filename = f"{name}_day_{start_date_str}_{today_str}.parquet"
        filepath = data_folder / filename

        # ファイルが存在すれば読み込み、なければダウンロードと保存処理へ
        if filepath.exists():
            print(f"ローカルファイルから読み込み: {filename}")
            data_dict[name] = pd.read_parquet(filepath)
        else:
            data = _download_and_archive_data(
                name=name,
                info=info,
                filepath=filepath,
                data_folder=data_folder,
                session=session
            )
            # ダウンロードが成功した場合のみ辞書に格納
            if not data.empty:
                data_dict[name] = data
    return data_dict


def _download_and_archive_data(
    name: str,
    info: dict,
    filepath: Path,
    data_folder: Path,
    session: requests.Session
) -> pd.DataFrame:
    """
    データをダウンロードし、古いファイルをアーカイブ後、新しいデータを保存する。

    Args:
        name (str): アセット名。
        info (dict): ティッカーと開始日を含む情報辞書。
        filepath (Path): 新しいデータの保存先ファイルパス。
        data_folder (Path): データが保存されているフォルダのパス。
        session (requests.Session): yfinanceダウンロード用のセッション。

    Returns:
        pd.DataFrame: ダウンロードされたデータ。失敗した場合は空のDataFrame。
    """
    print(f"ダウンロード開始: {name} ({info['ticker']})")
    try:
        data = yf.download(
            info['ticker'],
            start=info['start'],
            auto_adjust=True,
            session=session
        )
        time.sleep(1)  # サーバーへの負荷を考慮

        if data.empty:
            print(f"ダウンロード失敗（データが空）: {name}")
            return pd.DataFrame()

        # 古いファイルをアーカイブ
        _archive_old_files(data_folder, name, info['start'])

        # 新しいデータを保存
        data.to_parquet(filepath)
        print(f"保存完了: {filepath.name}")
        return data

    except Exception as e:
        print(f"ダウンロード中にエラーが発生しました: {name} -> {e}")
        return pd.DataFrame()


def _archive_old_files(data_folder: Path, name: str, start_date: str):
    """
    指定されたアセットの古いデータファイルを 'old' サブフォルダに移動する。

    Args:
        data_folder (Path): データが保存されているフォルダのパス。
        name (str): アセット名。
        start_date (str): データ取得開始日 ('YYYY-MM-DD')。
    """
    old_folder = data_folder / "old"
    old_folder.mkdir(exist_ok=True)

    # 移動対象のファイルパターン
    pattern = f"{name}_day_{start_date.replace('-', '')}_*.parquet"

    # data_folder 直下の古いファイルを探して移動
    for old_file in data_folder.glob(pattern):
        if not old_file.is_file():
            continue

        destination = old_folder / old_file.name
        print(f"古いファイルを移動: {old_file.name} -> {destination}")
        try:
            # 移動先に同名ファイルがあれば上書きするため、先に削除は不要
            shutil.move(str(old_file), str(destination))
        except Exception as e:
            print(f"移動エラー: {old_file.name} -> {e}")

def load_latest_asset_data(
    assets: Dict[str, Any],
    data_folder: Path
) -> Dict[str, pd.DataFrame]:
    """
    各アセットについて、指定フォルダ内にある最新のParquetファイルを読み込む。

    ファイル名は 'アセット名_day_開始日_*.parquet' のパターンに従うと想定。
    パターンに一致するファイルの中から、最終更新日時が最も新しいものを選択します。

    Args:
        assets (Dict[str, Any]):
            キーがアセット名、値が情報（'start'キーを含む）の辞書。
        data_folder (Path):
            データファイルが保存されているフォルダのパス。

    Returns:
        Dict[str, pd.DataFrame]:
            アセット名をキー、読み込んだDataFrameを値とする辞書。

    Raises:
        FileNotFoundError:
            パターンに一致するファイルが1つも見つからなかった場合に発生。
    """
    data_dict = {}
    print("最新のローカルファイルを探しています...")

    for name, info in assets.items():
        # 検索用のファイル名パターンを生成
        start_date_str = info['start'].replace('-', '')
        pattern = f"{name}_day_{start_date_str}_*.parquet"

        # パターンに一致するファイルのリストを取得
        # （元のコードのglobジェネレータでは空の判定ができないためリスト化）
        matching_files = list(data_folder.glob(pattern))

        # ファイルが見つからない場合はエラーを発生させる
        if not matching_files:
            raise FileNotFoundError(
                f"'{name}' に一致するParquetファイルが見つかりません。(検索パターン: {pattern})"
            )

        # 更新日時が最新のファイルを選ぶ
        latest_file = max(matching_files, key=os.path.getmtime)

        print(f"読み込み中: {latest_file.name}")
        data = pd.read_parquet(latest_file)
        data_dict[name] = data

    return data_dict

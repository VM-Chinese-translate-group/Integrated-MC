import json
import os
import re
import sys
from pathlib import Path
from typing import Tuple

import requests

TOKEN = os.getenv("API_TOKEN", "")
PROJECT_ID = os.getenv("PROJECT_ID", "")
FILE_URL = f"https://paratranz.cn/api/projects/{PROJECT_ID}/files/"

file_id_list = []
file_path_list = []
zh_cn_list = []

if len(TOKEN) != 32 or not PROJECT_ID.isdigit():
    raise EnvironmentError("未设置有效的 API_TOKEN 或 PROJECT_ID 环境变量")


def fetch_json(url: str, headers: dict[str, str]) -> list[dict[str, str]]:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def translate(file_id: int) -> Tuple[list[str], list[str]]:
    """获取指定文件的翻译内容并返回键值对列表"""
    url = f"https://paratranz.cn/api/projects/{PROJECT_ID}/files/{file_id}/translation"
    headers = {"Authorization": TOKEN, "accept": "*/*"}
    translations = fetch_json(url, headers)

    keys, values = [], []
    for item in translations:
        keys.append(item["key"])
        translation = item.get("translation", "")
        original = item.get("original", "")
        values.append(
            original if not translation and item["stage"] in [0, -1] else translation
        )

    return keys, values


def get_files() -> None:
    """
    获取项目中的文件列表并提取文件ID和路径
    """
    headers = {"Authorization": TOKEN, "accept": "*/*"}
    files = fetch_json(FILE_URL, headers)
    for file in files:
        file_id_list.append(file["id"])
        file_path_list.append(file["name"])


def save_translation(zh_cn_dict: dict[str, str], path: Path) -> None:
    """
    保存翻译内容到指定的 JSON 文件

    :param zh_cn_dict: 翻译内容的字典
    :param path: 原始文件路径
    """
    dir_path = Path("CNPack") / path.parent
    Path(str(dir_path).replace("rename/", "")).mkdir(parents=True, exist_ok=True)
    file_path = dir_path / "zh_cn.json"
    source_path = (
        str(file_path).replace("zh_cn.json", "en_us.json").replace("CNPack", "Source")
    )
    if "rename" in str(file_path):
        file_path = str(file_path).replace("rename/", "")
    with open(file_path, "w", encoding="UTF-8") as f:
        try:
            with open(source_path, "r", encoding="UTF-8") as f1:
                source_json: dict = json.load(f1)
            keys = source_json.keys()
            for key in keys:
                source_json[key] = zh_cn_dict[key]
            json.dump(
                source_json, f, ensure_ascii=False, indent=4, separators=(",", ":")
            )
        except IOError:
            print(f"{source_path}路径不存在，文件按首字母排序！")
            json.dump(
                zh_cn_dict,
                f,
                ensure_ascii=False,
                indent=4,
                separators=(",", ":"),
                sort_keys=True,
            )


def process_translation(file_id: int, path: Path) -> dict[str, str]:
    """
    处理单个文件的翻译，返回翻译字典
    :param file_id: 文件ID
    :param path: 文件路径
    :return: 翻译内容字典
    """
    keys, values = translate(file_id)
    # 替换换行符
    zh_cn_dict = {key: re.sub(r"\\n", "\n", value) for key, value in zip(keys, values)}
    # 特殊处理：ftbquest 文件
    if "ftbquest" in path.name:
        zh_cn_dict = {
            key: value.replace(" ", "\u00A0") if "image" not in value else value
            for key, value in zip(keys, values)
        }
    return zh_cn_dict


def main() -> None:
    if sys.version_info < (3, 9):
        raise EnvironmentError("请使用 Python 3.9 及更高版本")
    get_files()
    for file_id, path in zip(file_id_list, file_path_list):
        if "TM" in path:  # 跳过 TM 文件
            continue
        zh_cn_dict = process_translation(file_id, Path(path))
        zh_cn_list.append(zh_cn_dict)

        save_translation(zh_cn_dict, Path(path))
        if "rename" in path:
            path = str(path).replace("rename/", "")
        print(f"已从Patatranz下载到仓库：{re.sub('en_us.json', 'zh_cn.json', path)}")


if __name__ == "__main__":
    main()

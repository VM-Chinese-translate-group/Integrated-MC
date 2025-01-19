import re
import json
from pathlib import Path

# 文件路径
js_file_path = Path("D:/mc/mod/Integrated-MC/CNPack/kubejs/client_scripts/jei_info.js")
lang_file_path = Path("D:/mc/mod/Integrated-MC/CNPack/kubejs/assets/lang/en_us.json")

# 读取 js 文件内容
with open(js_file_path, "r", encoding="UTF-8") as js_file:
    js_content = js_file.readlines()

# 正则表达式匹配 e.addItem 语句
pattern = re.compile(r"e\.addItem\('([^']+)', \['([^']+)'\]\)")

# 翻译字典
translations = {}

# 替换文本并生成翻译键
def replace_text(match):
    item_id = match.group(1)
    text = match.group(2)
    modid, itemid = item_id.split(":")
    key = f"info.{modid}.{itemid}"
    translations[key] = text
    return f"e.addItem('{item_id}', [Component.translate('{key}')])"

# 处理每一行，忽略注释行并替换文本
new_js_lines = []
for line in js_content:
    if line.strip().startswith("//"):
        new_js_lines.append(line)
    else:
        new_line = pattern.sub(lambda match: replace_text(match), line)
        new_js_lines.append(new_line)

# 保存新的 js 文件内容
with open(js_file_path, "w", encoding="UTF-8") as js_file:
    js_file.writelines(new_js_lines)

# 创建语言文件目录
lang_file_path.parent.mkdir(parents=True, exist_ok=True)

# 保存翻译内容到 JSON 文件
with open(lang_file_path, "w", encoding="UTF-8") as lang_file:
    json.dump(translations, lang_file, ensure_ascii=False, indent=4)

print("国际化完成，生成的语言文件已保存到", lang_file_path)
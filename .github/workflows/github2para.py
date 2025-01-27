'''只有项目第一次创建上传才需要这个！更新文件无法使用本程序！'''
import asyncio
import os

from pprint import pprint
import paratranz_client


configuration = paratranz_client.Configuration(host="https://paratranz.cn/api")
configuration.api_key["Token"] = os.environ["API_TOKEN"]


async def upload_file(path, file):
    async with paratranz_client.ApiClient(configuration) as api_client:
        api_instance = paratranz_client.FilesApi(api_client)
        project_id = int(os.environ["PROJECT_ID"])
        try:
            # 第一次创建文件
            api_response = await api_instance.create_file(
                project_id, file=file, path=path
            )
            pprint(api_response)
        except Exception as e:
            print(f"Exception when calling FilesApi->create_file: {e}\n")


def get_filelist(dir):
    filelist = []
    for root, _, files in os.walk(dir):
        for file in files:
            if file.endswith("en_us.json"):
                filelist.append(os.path.join(root, file))
    return filelist


async def main():
    files = get_filelist("./")
    tasks = []

    for file in files:
        path = (
            file.split("Source")[1]
            .replace("\\", "/")
            .replace(os.path.basename(file), "")
        )
        print(f"Uploading {file} to {path}")
        tasks.append(upload_file(path=path, file=file))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

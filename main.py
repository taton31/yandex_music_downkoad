import asyncio
import aiohttp
import os

from ls import tracks



INVALID_CHARS = '<>:"/\\|?*'

def sanitize_filename(filename: str) -> str:
    for ch in INVALID_CHARS:
        filename = filename.replace(ch, "")
    return filename

async def download_file(session, url, filename):
    async with session.get(url) as response:
        try:
            response.raise_for_status()
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            print(f'Загружен файл: {filename}')
        except:
            pass

async def main():
    if not os.path.exists('load'):
        os.makedirs('load')

    connector = aiohttp.TCPConnector(limit=5)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for track in tracks:
            title = sanitize_filename(track[0])
            url = track[1]
            filename = os.path.join('load', title + '.mp3')
            if not os.path.exists(filename):
                tasks.append(asyncio.create_task(download_file(session, url, filename)))

        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())

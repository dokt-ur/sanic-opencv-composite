import asyncio
from typing import List

import aiohttp
import cv2
import numpy as np

BLACK_IMAGE = np.zeros((32, 32, 3), dtype=np.uint8)
BLUE_IMAGE = np.zeros((32, 32, 3), dtype=np.uint8)
BLUE_IMAGE[:, :, 0] = 255  # Set the blue channel to 255 (full blue)
BLUE_IMAGE[:, :, 1] = 0  # Set the green channel to 0
BLUE_IMAGE[:, :, 2] = 0  # Set the red channel to 0


async def download_image_from_url(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                print(f"Failed to download {url}. Status code: {response.status}")
    except Exception as e:
        print(f"An error occurred while downloading {url}: {str(e)}")

    # If you get a fetching error you should substitue a black image tile in the composite
    image_bytes = cv2.imencode(".png", BLACK_IMAGE)[1].tobytes()
    return image_bytes


async def download_images(image_urls: List[str]):
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_from_url(session, url) for url in image_urls]
        image_data_list = await asyncio.gather(*tasks)

    # Now, image_data_list contains the image data as bytes for each URL
    # You can process or save these bytes as needed

    # convert to numpy arrays
    images = []
    for image_data in image_data_list:
        try:
            images.append(
                cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
            )
        except Exception as e:
            print(f"unable to decode image {e}")
            #  If you get a image decode error you should substitute a blue image
            images.append(BLUE_IMAGE)
    return images


if __name__ == "__main__":
    image_list = [
        "https://api.slingacademy.com/public/sample-photos/1.jpeg",
        "https://api.slingacademy.com/public/sample-photos/1.jpeg",
        "https://api.slingacademy.com/public/sample-photos/1.jpeg",
    ]
    result = asyncio.run(download_images(image_list))

    cv2.imwrite("test.jpg", result[0])
    print(len(result), type(result[0]))

from uuid import uuid4

import cv2
import numpy as np
from sanic import Sanic, response

from helper import download_images
from sling_api import get_image_urls

app = Sanic("my-app")


AUTO_DOWNLOAD = False


@app.route("/")
async def test(request):
    print("new api request")
    images = []

    #  TODO: use offset and limit params
    batch_count = 12
    for batch_num in range(batch_count):
        offset = batch_num * batch_count
        print(f"FETCHING IMAGES: OFFSET: {offset}, LIMIT: {batch_count}")
        try:
            # get image list from sling api
            batch_image_list = get_image_urls(offset=offset, limit=batch_count)
            # download images from url
            batch_images = await download_images(batch_image_list)

        except Exception as e:
            print(f"unable to fetch images {e}")
        else:
            images.extend(batch_images)

    if not images:
        return response.json("0 images found!")

    # resize
    resized_images = [cv2.resize(image, (32, 32)) for image in images]

    # create composite
    composite_height = 12 * 32
    composite_width = 12 * 32

    composite_img = np.zeros((composite_height, composite_width, 3), dtype=np.uint8)

    for i in range(132):
        row = i // 12  # Calculate the row index
        col = i % 12  # Calculate the column index
        x_start = col * 32  # Starting x-coordinate of the image placement
        y_start = row * 32  # Starting y-coordinate of the image placement

        # Copy the resized image to the composite at the specified position
        composite_img[
            y_start : y_start + 32, x_start : x_start + 32  # noqa: E203
        ] = resized_images[i]

    cv2.imwrite("test-composite.jpg", composite_img)

    # Encode the image as JPG
    _, composite_img = cv2.imencode(".jpg", composite_img)

    # Set the appropriate response headers for an image
    content_disposition = ""
    if AUTO_DOWNLOAD:
        content_disposition += "attachment; "
    content_disposition += f"filename=composition-{uuid4()}.jpg"

    headers = {"Content-Disposition": content_disposition}

    # Stream the image data as a response
    return response.raw(
        composite_img.tobytes(), headers=headers, content_type="image/jpg"
    )


if __name__ == "__main__":
    app.run()

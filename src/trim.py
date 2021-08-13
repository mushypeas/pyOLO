from os import system as terminal
from PIL import Image
import numpy as np
import requests

API_KEY = '60d841675c6eda8e560aab1bbce1653ccd81f105'

terminal("convert example.jpg -auto-orient -resize x256 temp.png")

# while True:
#     response = requests.post(
#         'https://api.pixmiller.com/v1/remove',
#         files={'image_file': open("temp.png", 'rb')},
#         headers={'X-Api-Key': API_KEY},
#     )
#     if response.status_code == 201:
#         with open('result.png', 'wb') as out:
#             img_removed_url = response.json()["url"]
#             out.write(requests.get(img_removed_url).content)
#             break
#     else:
#         print("\nError:", response.status_code, response.text, "Retrying...\n")

temp = Image.open("temp.png").convert("RGBA")
result = Image.open("result.png")
width = result.size[0]
height = result.size[1]

mask_arr = np.array(result)
mask_arr = 255 - mask_arr


mask = Image.fromarray(mask_arr, "RGBA")
bg_mask = Image.new("RGBA", (width, height), (0,0,0,0))
bg_mask.paste(temp, mask=mask)
bg_arr = np.array(bg_mask)
print(bg_arr.shape)
filter = bg_arr[:,:,3] > 0
print(bg_arr[filter].shape)
# Image.fromarray(filter_arr, "RGBA").save("final.png")

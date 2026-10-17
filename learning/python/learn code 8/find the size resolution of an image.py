# # import PIL
# # from PIL import image 
# # img = PIL .image.open("c:\Users\abhij\OneDrive\Pictures\wallpapersden.com_76961-2867x2016.jpg")
# # width ,height= img.size
# # print (width,"x",height)


# import requests
# from PIL import Image
# from io import BytesIO

# # URL of the image
# url = "https://img1.hscicdn.com/image/upload/f_auto/lsci/db/PICTURES/CMS/357900/357938.jpg"

# # Download the image
# response = requests.get(url)
# if response.status_code == 200:
#     img = Image.open(BytesIO(response.content))  # Use BytesIO to open the image
#     width, height = img.size
#     print(f"{width} x {height}")  # Print dimensions
# else:
#     print(f"Failed to download the image. Status code: {response.status_code}")




import requests
from PIL import Image
from io import BytesIO

# URL of the image
url = "https://img1.hscicdn.com/image/upload/f_auto/lsci/db/PICTURES/CMS/357900/357938.jpg"

# Download the image
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Open the image
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    print(f"Image Dimensions: {width} x {height}")  # Print dimensions

except requests.exceptions.RequestException as e:
    print(f"Failed to download the image: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

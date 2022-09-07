from PIL import Image
import urllib.request
urllib.request.urlretrieve('https://static.wikia.nocookie.net/honkaiimpact3_gamepedia_en/images/a/a7/Allan_Poe_%28T%29.png/revision/latest?cb=20220827111314', 'T.png')
urllib.request.urlretrieve('https://static.wikia.nocookie.net/honkaiimpact3_gamepedia_en/images/5/5f/Allan_Poe_%28Back%29.png/revision/latest?cb=20220827111252', 'T(back).png')

image = Image.open('T.png')
image2 = Image.open('T(back).png')
image2.paste(image, (0,0), image)
image2.save('T(stacked).png')
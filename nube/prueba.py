from word_cloud import WordCloud
from PIL import Image


#cloud = WordCloud(uri="https://pastebin.com/raw/X2aEejs4", type="internet")
cloud = WordCloud(uri="D:\\borrar2.txt", type="local", top_n_words=50)
img = cloud.get_word_cloud_as_image()
img.save("D:\\prueba.png")
# word_a = Word("caquita", 0, 40, 50, fnt_size)
# word_b = Word("penis", 0, 350, 50, fnt_size)
# wc.draw_word(word_a)
# wc.draw_word(word_b)
# wc.show_word_cloud()
# print(word_a.collides(word_b))
#create_word_cloud(None, width, height, fnt_size, bg_color, fg_color, xy)

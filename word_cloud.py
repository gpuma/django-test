# nlp library
from nltk.corpus import stopwords
# image library
from PIL import Image, ImageDraw, ImageColor, ImageFont
# for command line arguments
import sys
import re


def get_words(filename):
    """Returns a list of words extracted from the file"""
    # words are found by matching against a regex
    # then they're further filtered by excluding any
    # english stop words, according to nltk data
    # todo: remove pronouns
    # lastly, they're converted to lowercase
    file = open(filename)
    raw = file.read()
    file.close()
    words = re.findall(r'\w+', raw)

    # we cast the stopwords into a set to speed it up, since sets
    # are implemented as hash tables
    filtered_words = [w.lower() for w in words if w not in set(stopwords.words('english'))]
    return filtered_words


def get_word_freq(word_list, normalize=True):
    """Returns a sorted list of (word,word count) tuples in descending order.
    The frequency is normalized to values between 0 and 1 by default."""
    word_freq_dict = {}
    for w in word_list:
        if w in word_freq_dict:
            word_freq_dict[w] += 1
        else:
            word_freq_dict[w] = 1
    if normalize:
        # inplace update to avoid recreating the dictionary again
        word_freq_dict.update((key, round(val / len(word_list), 3)) for key, val in word_freq_dict.items())

    unsorted_word_freq = [(key, val) for key, val in word_freq_dict.items()]
    # sorting by word frequency in descending order
    word_freq = sorted(unsorted_word_freq, key=lambda tup: tup[1], reverse=True)
    return word_freq


def create_word_cloud(word_list, width, height, font_size, background, foreground, xy):
    word = "benis"
    img = Image.new("RGB", (width, height), ImageColor.getrgb(background))
    fnt = ImageFont.truetype(font_location, font_size)
    draw = ImageDraw.Draw(img)
    draw.text(xy, word, font=fnt, fill=ImageColor.getrgb(foreground))
    # create a rectangle around the word in order to detect collisions
    # let's break it down: at first I thought the x coordinates of the rectangles would be equal to
    # fontsize * number of letters. Turns out that's too big and that diving the length in half gives a decent result
    # however, the last letter is cut off, so to avoid that I add 1 (it sometimes leaves an empty space). I was going
    # with 0.5, which actually creates a tight fit, but it cuts off the last letter in some cases.
    # For the y coordinates, just adding the font_size worked fine except for letter like 'p' and 'q', which
    # have kind of like a tail. To accomodate for that, adding 0.25 to the font size works great.
    draw.rectangle([xy, (xy[0]+font_size*(len(word)//2+1), xy[1]+font_size*1.25)], outline=foreground)
    img.show()

# todo: put this in a config file
font_location = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
width = int(sys.argv[1])
height = int(sys.argv[2])
fnt_size = int(sys.argv[3])
bg_color = sys.argv[4]
fg_color = sys.argv[5]
xy = (int(sys.argv[6]), int(sys.argv[7]))

#words = get_words(filename)
#print (words)
#print("there's %d words" % len(words))
#print("this is the frequency")
#print(get_word_freq(words)[:10])
create_word_cloud(None, width, height, fnt_size, bg_color, fg_color, xy)
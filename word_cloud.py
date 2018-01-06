# nlp library
from nltk.corpus import stopwords
# image library
from PIL import Image, ImageDraw, ImageColor, ImageFont
# for command line arguments
import sys
import re


class WordCloud:
    def __init__(self, word_freq, x, y, max_font_size, background="white", foreground="black"):
        self.max_font_size = max_font_size
        self.canv_x = x
        self.canv_y = y
        self.bg_color = background
        self.fg_color = foreground
        self.img = Image.new("RGB", (self.canv_x, self.canv_y), ImageColor.getrgb(background))
        self.draw = ImageDraw.Draw(self.img)
        #self.fnt_location = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
        self.font_location = "C:\\Anaconda3\\Library\\lib\\fonts\\DejaVuSerif.ttf"
        #ImageFont.truetype(font_location, font_size)
        # todo: uncomment
        #self.words = [Word(w, f) for w, f in word_freq]

    def get_center_position(self, word):
        """given a word of type Word, it returns the coordinates at which it
        should be drawn on the current canvas, in order to appear in the center."""
        # todo: it's not actually the center, it's a bit off
        return self.canv_x / 2 - (word.length * word.font_size) / 2, self.canv_y / 2 - word.font_size / 2

    def draw_word(self, word):
        """draws a specific Word onto the canvas"""
        fnt = ImageFont.truetype(self.font_location, word.font_size)
        # todo: draw in actual position instead of center
        # word.x, word.y = self.get_center_position(word)
        self.draw.text((word.x, word.y), word.text, font=fnt, fill=ImageColor.getrgb(self.fg_color))
        self.draw.rectangle(word.get_box_coord(), outline=self.fg_color)

    def show_word_cloud(self):
        """generates an image with the words drawn over it"""
        self.img.show()


class Word:
    def __init__(self, word, freq, x, y, font_size=0):
        self.text = word
        self.length = len(word)
        self.freq = freq
        self.font_size = font_size
        self.x = x
        self.y = y
        # has the form: [x0, y0, x1, y1] (from PIL.ImageDraw)
        self.box = self.get_box_coord()

    def get_box_dimensions(self):
        """returns the width and height of the box around the word"""
        return self.box[2] - self.box[0], self.box[3] - self.box[1]

    def get_box_coord(self):
        # calculates the two coordinates required to draw a rectangle around the word in order to detect collisions
        # let's break it down: at first I thought the x coordinates of the rectangles would be equal to
        # fontsize * number of letters. Turns out that's too big and that diving the length in half
        # gives a decent result. however, the last letter is cut off so, in order to avoid that
        # I add 1 (it sometimes leaves an empty space). I was going with 0.5, which actually creates a tight fit,
        # but it cuts off the last letter in some cases.
        # For the y coordinates, just adding the font_size worked fine except for letter like 'p' and 'q', which
        # have kind of like a tail. To accomodate for that, adding 0.25 to the font size works great.
        return [self.x, self.y, self.x + self.font_size * (self.length // 2 + 1), self.y + self.font_size * 1.25]

    def get_center_coord(self):
        """returns the center point of the box"""
        # midpoint formula
        return (self.box[0] + self.box[2]) * 0.5, (self.box[1] + self.box[3]) * 0.5

    def collides(self, other_word):
        """returns True if the box around this word overlaps with the box of the other word."""
        (width_box_a, height_box_a), (width_box_b, height_box_b) = self.get_box_dimensions(), other_word.get_box_dimensions()
        # distance between the center points of both boxes
        length = abs(self.get_center_coord()[0] - other_word.get_center_coord()[0])
        height = abs(self.get_center_coord()[1] - other_word.get_center_coord()[1])
        gap_x = length - width_box_a * 0.5 - width_box_b * 0.5
        gap_y = height - height_box_a * 0.5 - height_box_b * 0.5

        # a negative gap in both axis indicates that the boxes are overlapping
        # not considering when the edges are just touching
        return gap_x < 0 and gap_y < 0


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


# w[0]-> word, w[1] -> frequency, w[2] -> coordinates, w[3] -> coordinates
def place_words(word_list, max_font, width, height):
    max_freq=word_list[0][1]
    word_list[0][2]=get_center_position(width, height, word_list[0])
    #for i in range(1,len(word_list) - 1)

# todo: put this in a config file
width = int(sys.argv[1])
height = int(sys.argv[2])
fnt_size = int(sys.argv[3])
#bg_color = sys.argv[4]
#fg_color = sys.argv[5]
#xy = (int(sys.argv[6]), int(sys.argv[7]))

#words = get_words(filename)
#print (words)
#print("there's %d words" % len(words))
#print("this is the frequency")
#print(get_word_freq(words)[:10])

wc = WordCloud(None, width, height, fnt_size)
word_a = Word("caquita", 0, 40, 50, fnt_size)
word_b = Word("penis", 0, 350, 50, fnt_size)
wc.draw_word(word_a)
wc.draw_word(word_b)
wc.show_word_cloud()
print(word_a.collides(word_b))
#create_word_cloud(None, width, height, fnt_size, bg_color, fg_color, xy)
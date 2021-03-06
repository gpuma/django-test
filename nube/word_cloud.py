# nlp library
from nltk.corpus import stopwords
# image library
from PIL import Image, ImageDraw, ImageColor, ImageFont
# for command line arguments
import sys
import re
# used for drawing the words
import random
import math
# for reading text from a url
import requests
# to generate a random filename
import uuid
import os
from .constants import *
# for article view
from readability import Document
from bs4 import BeautifulSoup


class WordCloud:
    def __init__(self, file_ref, type, max_font_size=120, top_n_words=0, x=0, y=0, background="white",
                 foreground="black", automatic_size=True):
        self.max_font_size = max_font_size
        self.bg_color = background
        self.fg_color = foreground
        self.font_location = FONT_LOCATION

        # two types for now: local file and internet filename
        word_freq = get_word_freq(get_words(file_ref, type))

        # if a limit on the word number is not specified or if it exceeds
        # the amount of words, we should use the whole word list
        if top_n_words == 0 or top_n_words > len(word_freq):
            top_n_words = len(word_freq)
        # list of word, frequency pairs
        self.word_freq = word_freq[:top_n_words]

        # list of Words (carries display information)
        self.words = self.initialize_word_list()

        # image dimensions can be calculated automatically
        if automatic_size:
            self.canv_x, self.canv_y = self.get_automatic_dimensions()
        else:
            self.canv_x = x
            self.canv_y = y
        self.img = Image.new("RGB", (self.canv_x, self.canv_y), ImageColor.getrgb(background))
        self.draw = ImageDraw.Draw(self.img)
        random.seed()
        # main function
        self.create_word_cloud()

    def get_center_position(self, word):
        """given a word of type Word, it returns the x, y coordinates at which it
        should be drawn on the current canvas, in order to appear in the center."""
        # 0.3 is a magic number that gives a good approximation to the center
        return self.canv_x / 2 - (word.length * word.font_size * 0.3), self.canv_y / 2 - word.font_size / 2

    def draw_word(self, word):
        """draws a specific Word onto the canvas"""
        fnt = ImageFont.truetype(self.font_location, word.font_size)
        self.draw.text((word.x, word.y), word.text, font=fnt, fill=ImageColor.getrgb(self.fg_color))

    def is_touching_edges(self, word):
        """returns True if the given word's collision box exceeds the canvas dimensions"""
        # possibilities:
        # we only check if the word exceeds the right or bottom edge since the randomly
        # generated dimensions start from (0,0) so they cannot exceed the left or top edge
        return word.box[2] > self.canv_x or word.box[3] > self.canv_y

    def get_relative_font_size(self, max_freq, freq):
        """returns the relative font size for the specified word frequency,
        given that the maximum frequency should correspond to the maximum font size."""
        # simple cross-multiplication
        # font should be integer
        return int(freq * self.max_font_size / max_freq)

    def initialize_word_list(self):
        """Creates the list of Words to be placed on the word cloud, using the given font,
         along with their collision boxes, their size based on their frequency"""

        # the most frequent word is at the beginning of the list
        most_freq_word = self.word_freq[0]
        max_freq = most_freq_word[1]

        # initializing list of Words
        return [Word(w, f, font_size=self.get_relative_font_size(max_freq, f)) for w, f in self.word_freq]

    def create_word_cloud(self):
        """Creates an image with a word cloud based on the initialized word list"""

        # most frequent word goes in the center
        self.words[0].set_coordinates(self.get_center_position(self.words[0]))
        self.draw_word(self.words[0])

        # rest of the words
        # algorithm: in descending order (from most frequent to least), randomly generate a position
        # for the word, check if it doesn't intersect with any of the previous words and place it
        # todo: create a more efficient algorithm, right now it's brute force, with an emphasis on brute
        for i in range(1, len(self.words)):
            # todo: DRY
            # might start at the edge of the screen but get cut off by the image limits
            rand_xy = random.randrange(self.canv_x), random.randrange(self.canv_y)
            self.words[i].set_coordinates(rand_xy)
            # todo: this could be  improved with dynamic programming
            while self.is_touching_edges(self.words[i]) or \
                    WordCloud.word_intersects_with_the_rest(self.words[i], self.words[0:i]):
                rand_xy = random.randrange(self.canv_x), random.randrange(self.canv_y)
                self.words[i].set_coordinates(rand_xy)
            self.draw_word(self.words[i])

    def show_word_cloud(self):
        """generates an image with the words drawn over it"""
        self.img.show()

    def get_word_cloud_as_image(self):
        """
        Returns an PIL.Image instance with the corresponding
        word cloud data, ready to be displayed.
        """
        return self.img

    def save_word_cloud_to_fs(self, folder):
        """
        Saves the Word Cloud as PNG image with a randomly generated
        filename, at the specified folder. It returns the filename only
        """
        filename = get_random_filename('.png', prefix=TMP_PREFIX)
        local_path = os.path.join(folder, filename)
        self.img.save(local_path)
        return filename

    # todo: check if necessary to be static
    @staticmethod
    def word_intersects_with_the_rest(word, other_words):
        """Returns True if the given word intersects with any of
        the other words' collision boxes"""
        for w in other_words:
            if word.collides(w):
                return True
        return False

    def get_automatic_dimensions(self):
        """Calculates the appropiate width and height of the image, in order
        to display the Word Cloud correctly, based on the list of Words"""
        sum_of_all_areas = sum([w.get_box_area() for w in self.words])
        # for now it's a square image
        # 1.3 is an arbitrary scale that gives good results
        edge_size = int(math.sqrt(sum_of_all_areas) * 1.3)
        return edge_size, edge_size


class Word:
    def __init__(self, word, freq, x=0, y=0, font_size=0):
        self.text = word
        self.length = len(word)
        self.freq = freq
        self.font_size = font_size
        self.x = x
        self.y = y
        # has the form: [x0, y0, x1, y1] (from PIL.ImageDraw)
        # which are the opposing coordinates required to draw a rectangle
        # todo: check, might not be necessary
        self.box = self.get_box_coord()

    def set_coordinates(self, xy):
        """Set the coordinates according to the xy tuple (in that order)
         and recalculates the collision box for the word."""
        self.x = xy[0]
        self.y = xy[1]
        self.box = self.get_box_coord()

    def get_box_dimensions(self):
        """returns the width and height of the box around the word"""
        return self.box[2] - self.box[0], self.box[3] - self.box[1]

    def get_box_area(self):
        """Returns the area of the collision box around the word."""
        width, height = self.get_box_dimensions()
        return width * height

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

    def get_center_point(self):
        """returns the center point of the box"""
        # midpoint formula
        return (self.box[0] + self.box[2]) * 0.5, (self.box[1] + self.box[3]) * 0.5

    def collides(self, other_word):
        """returns True if the box around this word overlaps with the box of the other word."""
        (width_box_a, height_box_a), (
            width_box_b, height_box_b) = self.get_box_dimensions(), other_word.get_box_dimensions()
        # distance between the center points of both boxes
        length = abs(self.get_center_point()[0] - other_word.get_center_point()[0])
        height = abs(self.get_center_point()[1] - other_word.get_center_point()[1])
        gap_x = length - width_box_a * 0.5 - width_box_b * 0.5
        gap_y = height - height_box_a * 0.5 - height_box_b * 0.5

        # a negative gap in both axis indicates that the boxes are overlapping
        # not considering when the edges are just touching
        return gap_x < 0 and gap_y < 0


def get_words(file_ref, type):
    """
    Returns a list of words extracted from a file.
    file_ref can be a local filename, a URL or a file
    stored in memory
    """
    # words are found by matching against a regex
    # then they're further filtered by excluding any
    # english stop words, according to nltk data
    # lastly, they're converted to lowercase
    if type == "local":
        file = open(file_ref, encoding="utf8")
        raw = file.read()
        file.close()
    elif type == "internet":
        response = requests.get(file_ref)

        # two supported cases:
        # url is regular html or url is plaintext
        if 'html' in response.headers['Content-Type']:
            raw = extract_content_from_html(response.text)
        # if maybe add 'text/plain' check
        else:
            raw = response.text
    elif type == "upload":
        # type is InMemoryFileUpload
        # read() returns html (a byte-like object)
        # thus, we need to decode
        raw = file_ref.read().decode('utf-8')
    else:
        raise ValueError("Type not supported.")
    words = re.findall(r'\w+', raw)

    # we cast the stopwords into a set to speed it up, since sets
    # are implemented as hash tables
    filtered_words = [w.lower() for w in words if w.lower() not in set(stopwords.words('english'))]
    return filtered_words


# todo: there's probably a more efficient way to do this
def extract_content_from_html(html):
    """
    Extracts the main content of a webpage. Similar to the
    Reader View in Firefox or Pocket.
    Main HTML content is extracted using python-readability (readability-lxml)
    HTML tags are removed using BeautifulSoup.
    """
    doc = Document(html)
    soup = BeautifulSoup(doc.content(), "lxml")
    plaintext = ''.join(soup.findAll(text=True))
    # the original soup comes with too many '\n', this messes up
    # word frequency calculation
    return plaintext.replace("\\n", "")


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
        word_freq_dict.update((key, round(val / len(word_list), 3))
                              for key, val in word_freq_dict.items())

    unsorted_word_freq = [(key, val) for key, val in word_freq_dict.items()]
    # sorting by word frequency in descending order
    word_freq = sorted(unsorted_word_freq, key=lambda tup: tup[1], reverse=True)
    return word_freq


def get_random_filename(ext, prefix=""):
    """
    Returns a randomly generated string with the specified
    extension `ext` appended at the end. `ext` should have a dot.
    A str `prefix` can also be prefixed to the filename.
    """
    # hex returns a string with no dashes
    return prefix + str(uuid.uuid4().hex) + ext

from . imp WordCloud

# todo: put this in a config file
filename = sys.argv[1]
word_count = int(sys.argv[2])
fnt_size = int(sys.argv[3])
#bg_color = sys.argv[4]
#fg_color = sys.argv[5]
#xy = (int(sys.argv[6]), int(sys.argv[7]))

words = get_word_freq(get_words(filename))
print(words)
#print("there's %d words" % len(words))
#print("this is the frequency")
#print()

# todo: since when processing many words the least frequent are too small
# to be readable, we might want to start using the min_font_size instead of max
wc = WordCloud(words, top_n_words=word_count,  max_font_size=fnt_size)
wc.create_word_cloud()
wc.show_word_cloud()
# word_a = Word("caquita", 0, 40, 50, fnt_size)
# word_b = Word("penis", 0, 350, 50, fnt_size)
# wc.draw_word(word_a)
# wc.draw_word(word_b)
# wc.show_word_cloud()
# print(word_a.collides(word_b))
#create_word_cloud(None, width, height, fnt_size, bg_color, fg_color, xy)

import collections
import pprint 

word_count = collections.defaultdict(int)
genre_amount = 0
with open('genre_info.txt', 'r') as data:
    lines = data.readlines()
    genre_amount = len(lines)
    for i in lines:
        for a in i.replace(r'\n', '').split():
            word_count[a] += 1

for key, value in word_count.items():
    word_count[key] = round(value/genre_amount * 100, 10)


word_count = sorted(word_count.items(), key= lambda x: x[1], reverse=True)
 
pp = pprint.PrettyPrinter(depth=2, indent=6)
pp.pprint(word_count)



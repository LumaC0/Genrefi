import collections
import functools
import pprint 

# dict with genres already populated
import process_dict

# decorator for automatic coroutine start
def initialize(func):
    @functools.wraps(func)
    def _initialize(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return _initialize
    

class GenreStats:
    def open_all(self):
        with open('text_files/all_genres.txt', 'r') as data:
            for i in data.readlines():
                try:
                    self.add_all().send(i)
                except StopIteration:
                    self.add_all().send(None)
    

    @initialize
    def add_all(self):
        """ adding genres one at a time to previously made dict"""
        while True:
            a = yield
            if a is None:
                break
            placed = False
            if '-' in a:
                a = a.replace('-', '')
            for i in a.split():
                if i in process_dict.genres:
                    if a not in process_dict.genres[i]:
                        process_dict.genres[i].append(a)
                        placed = True
                        break
            if not placed:
                process_dict.genres.setdefault('other', []).append(a)
                        

                   
# function to find frequency of main genres         
'''
for key, value in word_count.items():
    word_count[key] = round(value/genre_amount * 100, 10)

word_count = sorted(word_count.items(), key= lambda x: x[1], reverse=True)
'''
if __name__=='__main__':
    sort_the_fucking_genres = GenreStats()
    sort_the_fucking_genres.open_all()

pp = pprint.PrettyPrinter(depth=2, indent=6)
pp.pprint(process_dict.genres)



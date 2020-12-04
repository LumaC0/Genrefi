import pprint
import itertools

from py_data import main_genre_dict

PP = pprint.PrettyPrinter()

class Process:
    def __init__(self):
        self.genres = main_genre_dict.genres
        self.base_genres = list(self.genres.keys())
        self.subgenres = list(main_genre_dict.genres.values())
        self.hot_new_dict = {}

    def __call__(self):
        self.applying_processing()
        self.genre_seperation()

    def clean_words(self, words):
        """ This function's sole purpose is it clean strings of noisy values """
        return words.replace("\n", "").strip()

    def __iter__(self):
        """ iterator for dict of genres so I only have to parse once """
        for key in self.base_genres:
            for i, v in enumerate(self.genres[key]):
                yield key, i, v


    def applying_processing(self):
        for key, i, v in self.__iter__():
            self.genres[key][i] = self.clean_words(v)
            if 'dnb' in v:
                self.genres['drum and bass'].append(self.genres[key].pop(i))
            if ' psych ' in v:
                self.genres.setdefault('psychedelic rock', []).append(v)
            if ' ambient ' in v:
                self.genres.setdefault('ambient', []).append(v)


    def genre_seperation(self):
        for key, i, v in self.__iter__():
            self.hot_new_dict[v] = key 




if __name__=='__main__':
    genes = Process()
    genes()
    PP.pprint(genes.hot_new_dict)



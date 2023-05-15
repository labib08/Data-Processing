import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
from collections import defaultdict


def task4(bow: pd.DataFrame, output_plot_filename: str) -> Dict[str, List[str]]:
    # The bow dataframe is the output of Task 3, it has 
    # three columns, link_url, words and seed_url. The 
    # output plot should show which words are most common
    # for each seed_url. The visualisation is your choice,
    # but you should make sure it makes sense for what it
    # is meant to be.

    seed_url_words = {}
    # A dictionary is made where the key is the seed url and the value
    # is the list of words found from those seed url.
    for i in range(len(bow['words'])):
        for word in bow['words'][i].split():
            if bow['seed_url'][i] in seed_url_words.keys():
                seed_url_words[bow['seed_url'][i]].append(word)
            else:
                seed_url_words[bow['seed_url'][i]] = []
    # A dicionary of dictionary is created where the value stores the 
    # frequency of words.
    seed_url_word_count = {}
    for key, value in seed_url_words.items():
        word_freq = {}  
        for word in value:
            if word in word_freq.keys():
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        # The dicitonary is sorted in a descending order.
        sorted_word_freq = sorted(word_freq.items(), key=lambda x:x[1], reverse=True)[:10]
        sorted_word_freq = dict(sorted_word_freq)
        seed_url_word_count[key] = sorted_word_freq

    # A bar chart is created.
    fig,(ax1, ax2) = plt.subplots(2, 1, figsize=(11,7))
    title_1 = list(seed_url_word_count.keys())[0]
    title_2 = list(seed_url_word_count.keys())[1]
    
    ax1.bar(seed_url_word_count[title_1].keys(), seed_url_word_count[title_1].values())
    ax1.set_title(title_1)
    ax2.bar(seed_url_word_count[title_2].keys(), seed_url_word_count[title_2].values())
    ax2.set_title(title_2)
    ax1.set_xlabel('Words')
    ax1.set_ylabel('Occurrences')
    ax2.set_xlabel('Words')
    ax2.set_ylabel('Occurrences')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
        
    plt.tight_layout()
    # The bar chart is saved.
    plt.savefig(output_plot_filename)

    #The value in the dictionary, which was a dictionary is then converted
    # to a list.
    for key, value in seed_url_word_count.items():
        seed_url_word_count[key] = list(value.keys())

    return seed_url_word_count
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Union, List

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import Normalizer

import seaborn as sns

def task5(bow_df: pd.DataFrame, tokens_plot_filename: str, distribution_plot_filename: str) -> Dict[str, Union[List[str], List[float]]]:
    # bow_df is the output of Task 3, for this task you 
    # should generate a bag of words, normalisation of the 
    # data perform PCA decomposition to 2 components, and 
    # then plot all URLs in a way which helps you answer
    # the discussion questions. If you would like to verify 
    # your PCA results against the sample data, you can return
    # the PCA weights - containing the list of most positive
    # weighted words, most negatively weighted words and the 
    # weights in the PCA decomposition for each respective word.

    vectorizer = CountVectorizer()
    # The bag of word is fetched and then normalized
    vectorizer.fit(bow_df['words'])
    bow = vectorizer.fit_transform(bow_df['words'])
    
    normalized_bow = Normalizer(norm = 'max').fit_transform(bow)
    
    word_dict = vectorizer.vocabulary_
    
    sklearn_pca = PCA(n_components = 2, random_state = 535)
    x_pca = sklearn_pca.fit_transform(normalized_bow.toarray())
    
    weights = sklearn_pca.components_
    weight_dict = {}
    # Top ten tokens with positive weight and top ten tokens
    # with negative weight is found out along with their weights.
    for i in range(2):
        pos_word_list = []
        neg_word_list = []
        pos_word_weights = []
        neg_word_weights = []
        sub_weight_dict ={}
        weight_words =  sklearn_pca.components_[i]
        sorted_weights = np.argsort(weight_words)
        positive = sorted_weights[-10:]
        negative = sorted_weights[:10]
        positive_sorted = np.flip(positive)
        negative_sorted = np.flip(negative)
        for index in positive_sorted:
            for key, value in word_dict.items():
                if value == index:
                    pos_word_list.append(key)
        for index in negative_sorted:
            for key, value in word_dict.items():
                if value == index:
                    neg_word_list.append(key)
        
        for index in positive_sorted:
            pos_word_weights.append(weight_words[index])
        for index in negative_sorted:
            neg_word_weights.append(weight_words[index])
        
        sub_weight_dict["positive"] = pos_word_list
        sub_weight_dict["negative"] = neg_word_list
        sub_weight_dict["positive_weights"] = pos_word_weights
        sub_weight_dict["negative_weights"] = neg_word_weights
        
        weight_dict[str(i)] = sub_weight_dict
    
    # A bar graph is then drawn representing the words and its corresponding weight.
    x_values = weight_dict['0']['positive'] + weight_dict['0']['negative'] + weight_dict['1']['positive'] + weight_dict['1']['negative']
    y_values = weight_dict['0']['positive_weights'] + weight_dict['0']['negative_weights'] + weight_dict['1']['positive_weights'] + weight_dict['1']['negative_weights']
    bar_width = 0.001
    
    fig, ax = plt.subplots()
    bars = ax.bar(x_values, y_values, width=bar_width)

    # Create the bars
    bars = ax.bar(x_values, y_values)

    # Loop over the bars to set the colors based on the value
    for i, bar in enumerate(bars):
        if y_values[i] > 0:
            bar.set_color('green')
        else:
            bar.set_color('red')

    # Set the y-axis limits to include both positive and negative values
    ax.yaxis.set_major_formatter('{:.3f}'.format)
    ax.axhline(y= 0, color='black', linestyle='--', linewidth=1)
    ax.set_ylim(min(y_values)-1, max(y_values)+1)
    ax.set_xticklabels(x_values, rotation=90)
    ax.set_title("PCA COMPONENTS 1 AND 2")
    ax.set_xlabel('Words')
    ax.set_ylabel('Weight')
    plt.tight_layout()
    plt.savefig(tokens_plot_filename)
    plt.clf()
    # A scatterplot is made to show the distribution of articles
    # from each seed url
    seed_url_list = []
    for url in bow_df["seed_url"]:
        if url not in seed_url_list:
            seed_url_list.append(url)
    url_color_map = {seed_url_list[0]: 'blue', seed_url_list[1]: 'orange'}
    
    colors = []
    for url in bow_df['seed_url']:
        colors.append(url_color_map[url])
    plt.scatter(x=x_pca[:,0], y=x_pca[:,1], c = colors)
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=url, markerfacecolor=color, markersize=8)
                   for url, color in url_color_map.items()]
    plt.legend(handles=legend_elements, loc='upper right')
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("PCA distribution of articles")
    plt.tight_layout()
    plt.savefig(distribution_plot_filename)
    return weight_dict
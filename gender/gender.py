import pdb
import os, fnmatch
import pickle

def get_corpus_dict(corpus):
    """
        Fn which parses the right .txt file into a dictionary and
        return dictionary
    """

    # open the right file
    if corpus == "female_names":
        file_name = "all_female_names.txt"
    else:
        file_name = "all_explicit_words.txt"

    # put all names in a dictionary and return
    corpus_dict = {}
    corpus_dict['type'] = corpus
    with open("assets/" + file_name) as myfile:
        for line in myfile:
            corpus_dict[str(line).strip("\\\n").lower()] = ""
    return corpus_dict

def check_for_occurences(directory, artist_name, artist_dict, corpus_dict):
    """
        Fn which looks for occurences of target words and associates them
        with an artist name
    """
    dict_type = corpus_dict['type'] # either female_names or profanity

    with open(directory) as myfile:
        # loop through each line of lyrics
        for line in myfile:
            
            # search through the female names corpus
            if dict_type != "female_names":
                for word in line.split(" "):
                    if word.lower() in corpus_dict.keys():
                        artist_dict[artist_name][word] = (
                            artist_dict[artist_name].get(word,0) + 1
                            )

            # search through another corpus, word doesn't have to be capitalized
            else:
                for word in line.split(" "):
                    if word[0].upper() and word.lower() in corpus_dict.keys():
                        artist_dict[artist_name][word] = (
                            artist_dict[artist_name].get(word,0) + 1
                            )

def get_count(corpus):
    """
        Counts the # of occurences each artist makes to a word in the specified
        corpus, returns two dicts:
            K: artist_name V: count of references
            K: artist_name V: year they first reached top rap song
    """
    corpus_dict = get_corpus_dict(corpus)
    artist_dict = {}
    year_dict = {}

    # loop through all text files of song lyrics
    for root, dirs, files in os.walk("lyrics/"):
        for file in fnmatch.filter(files, "*.txt"):

            # pull out the artist name and compose file path
            directory = os.path.join(root,file)
            artist_name = str(directory).split("-")[1].strip(".txt")
            year = str(directory).split("/")[1].split("-")[0]

            # only record data for artist 1x, even if we see them more than once
            artist_dict[artist_name] = {}

            # store the year this artist first appeared in top
            if artist_name not in year_dict:
                year_dict[artist_name] = year

            check_for_occurences(directory, artist_name, artist_dict, corpus_dict)

    # print out the values for easy viewing in excel
    for artist in artist_dict.keys():
        s = sum(artist_dict[artist].values())
        year =year_dict[artist]
        print "%s, %s, %s"%(artist, year, s)

    pdb.set_trace()
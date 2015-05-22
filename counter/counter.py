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
        file_name = "female_explicit_words.txt"

    # put all names in a dictionary and return
    corpus_dict = {}
    corpus_dict['type'] = corpus
    with open("assets/" + file_name) as myfile:
        for line in myfile:
            corpus_dict[str(line).strip("\\\n").lower()] = ""
    return corpus_dict

def check_for_occurences(directory, song, song_dict, corpus_dict):
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
                        song_dict[song][word] = (
                            song_dict[song].get(word,0) + 1
                            )

            # search through another corpus, word doesn't have to be capitalized
            else:
                for word in line.split(" "):
                    if word[0].upper() and word.lower() in corpus_dict.keys():
                        song_dict[song][word] = (
                            song_dict[song].get(word,0) + 1
                            )

def get_count(corpus):
    """
        Counts the # of occurences each artist makes to a word in the specified
        corpus, returns two dicts:
            K: song_name V: count of references
            K: song_name V: year they first reached top rap song
    """
    corpus_dict = get_corpus_dict(corpus)
    song_dict = {}
    year_dict = {}
    
    # loop through all text files of song lyrics
    for root, dirs, files in os.walk("lyrics/"):
        for file in fnmatch.filter(files, "*.txt"):

            # pull out the artist name and compose file path
            directory = os.path.join(root,file)
            blocks = str(directory).split("#")
            year = blocks[0].strip(" lyrics/").strip()
            song = blocks[1]
            artist_name = blocks[2].strip(".txt")

            # only record data for a song 1x, even if we see them more than once
            song_dict[song] = {}

            # store the year this song appeared in top
            if song not in year_dict:
                year_dict[song] = year

            check_for_occurences(directory, song, song_dict, corpus_dict)

    # print out the values for easy viewing in excel
    # for song in song_dict.keys():
    #     s = sum(song_dict[song].values())
    #     year =year_dict[song]
    #     print "%s, %s, %s"%(song, year, s)
    return song_dict, year_dict
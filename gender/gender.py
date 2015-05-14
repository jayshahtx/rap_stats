import pdb
import os, fnmatch
import pickle

def get_name_dict():
    """
        Fn which  converts a text file of female names into a dictionary for
        easy parsing
    """
    names = {}
    with open("assets/all_female_names.txt") as myfile:
        for line in myfile:
            names[str(line).strip("\\\n").lower()] = ""
    return names

def check_for_names(names,artist_dict,artist_name, year_dict, year, directory):
    """
        Fn which looks for names of females and associates them with an
        artist name
    """

    with open(directory) as myfile:
        # loop through each line of lyrics
        for line in myfile:
            # check if each word in lyrics is a female name
            for word in line.split(" "):
                # check if word is capitalized and in our corpus of names
                if word[0].isupper() and word.lower() in names.keys():
                    artist_dict[artist_name][word] = artist_dict[artist_name].get(word,0) + 1
                    year_dict[year][word] = year_dict[year].get(word,0) + 1


def get_name_count():
    """
        Generates two dicts where K: rapper name[female_name], V: frequency
        and K: year[female_name] V:references
    """
    
    # dict of all names and names which artists refer to
    names = get_name_dict()
    artist_dict = {}
    year_dict = {}

    # loop through all text files of song lyrics
    for root, dirs, files in os.walk("lyrics/"):
        for file in fnmatch.filter(files, "*.txt"):
            
            # pull out the artist name and compose file path
            directory = os.path.join(root,file)
            artist_name = str(directory).split("-")[1].strip(".txt")
            year = str(directory).split("/")[1].split("-")[0]
            
            print "%s,%s"%(artist_name, year)
            # initialize artist name/year in the dict
            artist_dict[artist_name] = {}

            if year not in year_dict.keys():
                year_dict[year] = {}
            
            # check the lyrics for names with helper function
            check_for_names(
                names,
                artist_dict,
                artist_name,
                year_dict,
                year,
                directory
            )
    artist_list = []
    for artist in artist_dict.keys():
        female_count = sum(artist_dict[artist].values())
        artist_list.append((artist, female_count))
    
    print "\n\n\n"
    artist_list = sorted(artist_list, key=lambda x: x[1], reverse=True)
    for a in artist_list:
        print a[0] + ","+str(a[1])


    year_list = []
    for year in year_dict.keys():
        female_count = sum(year_dict[year].values())
        year_list.append((year, female_count))
    
    year_list = sorted(year_list, key=lambda x: x[1], reverse=True)
    # import json
    # print json.dumps(artist_list, indent=1)
    
    pickle.dump(artist_dict, open("females_in_songs.p", "wb"))
    pickle.dump(year_dict, open("females_in_years.p", "wb"))
    pdb.set_trace()
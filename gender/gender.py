import pdb
import os, fnmatch

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

def check_for_names(names,artist_dict,artist_name,directory):
    """
        Fn which looks for names of females and associates them with an
        artist name
    """

    with open(directory) as myfile:
        # loop through each line of lyrics
        for line in myfile:
            # check if each word in lyrics is a female name
            for word in line.split(" "):
                # update array of names associated with this artist, if any
                if word in names.keys():
                    artist_dict.setdefault( artist_name, [] ).append(word)
                    # artist_dict[artist_name] = artist_dict.get(
                    #     artist_name, default=[]).append(word)


def get_name_count():
    """
        Fn which generates a dict where K: rapper name, V: list of females
        mentioned, parses song lyrics in directory and looks for names
    """
    
    # dict of all names and names which artists refer to
    names = get_name_dict()
    artist_dict = {}

    # loop through all text files of song lyrics
    for root, dirs, files in os.walk("lyrics/"):
        for file in fnmatch.filter(files, "*.txt"):
            
            # pull out the artist name and compose file path
            directory = os.path.join(root,file)
            artist_name = str(directory).split("-")[1]
            
            # check the lyrics for names with helper function
            check_for_names(names, artist_dict, artist_name, directory)
            
        

    pdb.set_trace()
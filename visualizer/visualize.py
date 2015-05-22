import ipdb as pdb
import numpy as np
import matplotlib.pyplot as plt

def convert_to_csv(female_dict, profanity_dict, year_dict):
    """
        Returns two arrays, one with years (X val) and another with the # of
        occurences of a word type per song, per year
    """
    headers = ["Year, Female Names Per Song, Profanity Per Song"]
    # get a list of unique years in the dataset, sort list
    years = list(set(year_dict.values()))
    years = sorted(years)

    female_names_per_song_year = []
    profanity_per_song_year = []

    for year in years:
        
        # get all songs from that year
        songs = [key for key, value in year_dict.iteritems() if \
            value == year]
        song_count = len(songs)

        # get # of occurences per year based on songs from that year
        female_occurences = float(sum(sum(female_dict[song].values()) for song in songs))
        profanity_occurences = float(sum(sum(profanity_dict[song].values()) for song in songs))
        
        # calculate occurences/song
        f_occurences_per_song = female_occurences/song_count
        female_names_per_song_year.append(f_occurences_per_song)

        p_occurences_per_song = profanity_occurences/song_count
        profanity_per_song_year.append(p_occurences_per_song)
        
    return [headers, years, female_names_per_song_year, profanity_per_song_year]


def graph_from_file():
    
    # plotly sign in
    import plotly.plotly as py
    from plotly.graph_objs import *
    py.sign_in('jayshahtx','q3zs8ye8c8')
    
    import pandas

    # songs/year        
    # data = pandas.read_csv("assets/songs_per_year.csv")
    # trace1 = Bar(
    #     x=data['year'],
    #     y=data['songs']
    # )
    # xlabel = "Year"
    # ylabel = "Songs"
    # title = "#1 Billboard Rap Singles"
    # filename = "rapsongs/year"

    # expletives/year
    # data = pandas.read_csv("assets/profanity_per_year.csv")
    # trace1 = Scatter(
    #     x=data['year'],
    #     y=data['count/song'],
    #     name="Female profanity/song",
    #     mode='lines',
    #     line=Line(
    #         shape='spline',
    #         smoothing='1.2'
    #     )
    # )
    # xlabel = "Year"
    # ylabel =  "Expletives Per Song"
    # title = "Expletives Per Songs"
    # filename = "expletives"

    # female names/year
    data = pandas.read_csv("assets/names_per_year.csv")
    trace1 = Scatter(
        x=data['year'],
        y=data['count/song'],
        name="Female names/song",
        mode='lines',
        line=Line(
            shape='spline',
            smoothing='1.2'
        )
    )
    xlabel = "Year"
    ylabel = "Female Names per Song"
    title = "Female Names per Song"
    filename = "female_names" 

    # female profanity/song
    # data = pandas.read_csv("assets/female_profanity_per_year.csv")
    # trace1 = Scatter(
    #     x=data['year'],
    #     y=data['count/song'],
    #     name="Female profanity/song",
    #     mode='lines',
    #     line=Line(
    #         shape='spline',
    #         smoothing='1.2'
    #     )
    # )
    # xlabel = "Year"
    # ylabel = "Expletives per Song"
    # title = "Female Expletives Per Song"
    # filename = "female_expletives"
    

    # general layout for all graphs
    layout = Layout(
        title=title,
        xaxis=XAxis(
            title=xlabel,
            showgrid=False
        ),
        yaxis=YAxis(
            title=ylabel,
            showline=False
        )
    )

    data = Data([trace1])
    fig = Figure(data=data,layout=layout)
    plot_url = py.plot(fig, filename=filename)


    # female names/song
    # data = pandas.read_csv("assets/names_per_year.csv")
    # trace2 = Scatter(
    #     x=data['year'],
    #     y=data['count/song'],
    #     name="Female names/song",
    #     mode='lines',
    #     line=Line(
    #         shape='spline',
    #         smoothing='1.2'
    #     )
    # )

    # data = Data([trace1, trace2])
    # layout = Layout(
    #     title="Analysis of Song Lyrics"
    # )

   

def graph(csv):
    # x = np.linspace(int(csv[1][0]), int(csv[1][-1])) # range of years
    # line = plt.plot(csv[1], csv[2], csv[1], csv[3])
    # plt.show()

    import plotly.plotly as py
    from plotly.graph_objs import *
    # pdb.set_trace()
    py.sign_in('jayshahtx','q3zs8ye8c8')
    labes = csv[0]
    years = csv[1]
    names = csv[2]
    words = csv[3]

    trace1 = Scatter(
        x=years,
        y=names,
        name="Female names/song"
        )

    trace2 = Scatter(
        x=years,
        y=words,
        name="Explicit words/song"
    )

    data = Data([trace1, trace2])

    # limit the axis ranges
    layout = Layout(
        xaxis=XAxis(
            range=[1989, 2014]
        ),
        yaxis=YAxis(
            range=[1,20]
        ),
        title='Historical Analyis of Word Choice in Rap Songs'
    )

    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename="test-line")



def custom_data(female_dict, profanity_dict, year_dict):
    
    # get rap songs/year
    # years = list(set(year_dict.values()))
    # years = sorted(years)

    # for year in years:
    #     songs = [key for key, value in year_dict.iteritems() if \
    #         value == year]
    #     song_count = len(songs)
    #     print str(year)+","+str(song_count)

    # female names/year
    pass




def visualize(female_dict, profanity_dict, year_dict):
    csv = convert_to_csv(female_dict, profanity_dict, year_dict)
    for x in range(0, len(csv[1])):
        print str(csv[1][x]) + "," + str(csv[3][x])
    pdb.set_trace()
    # graph(csv)

    """
    song_dict {
        song1 {
            "word1": 12,
            "word2": 13
        },
        song2
        {
            ...  
        }
    }


    year_dict {
        song1 : 1989,
        song2 : 1990,
        ...
    }
    """
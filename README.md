# GETMUSIC 
>               " Why must I pay for what makes me Happy ? Why can't I `getmusic` for free ? "
<p align="center"><img width="200" src="https://github.com/derhnyel/getmusic/blob/build-engine/assets/logo.jpg?raw=true" alt="logo">
</p>
<hr>
Getmusic is a package that gives you access to a variety of music from your favourite artists. It lets you query popular music download sites and scrape for artists, songs and albums titles, download links to albums and tracks and albums/tracks details.
<hr>

## Supported Engines

Supported music engines include:
- SongsLover
- Mp3Juices
- NaijaMusic
- AceMusic
- JustNaija

View all supported engines [here](https://github.com/derhnyel/getmusic/blob/build-engine/docs/supported_engines.md?raw=true)

## Development

#### Clone the respository

- Clone this repo `git clone git@github.com:derhnyel/getmusic.git`

## Usage

#### Search
Engines can be searched with query string

```python

    import pprint

    from engine.songslover import SongsLover 
    from engine.justnaija import JustNaija
    from engine.naijamusic import NaijaMusic
    from engine.mp3juices import Mp3Juices
    from engine.ace import Ace

    search_args = ('Donda 2',1)
    jn = JustNaija()
    mj = Mp3Juices()
    ace = Ace() 
    sl = Songslover()
    nm = NaijaMusic()

    slresults = sl.search(*search_args)
    jnresults = jn.search(*search_args)
    aceresults = ace.search(*search_args)
    mjresults = mj.search(*search_args)
    nmresults = nm.serach(*search_args)

    results = dict(
              Songslover=slresults,
              JustNaija=jnresults,
              AceMusic=aceresults,
              NaijaMusic=nmresults,
              Mp3Juices=mjresults,
              )

    # pretty print the result from each engine
    for k, v in results.items():
        print(f"-------------{k}------------")
        for result in v:
            pprint.pprint(result)
```

#### Fetch
Latest Items can be fetched from engines based on categories eg. latest albums, tracks, gospel etc. Each engine allowed category is defined.
```python

    import pprint

    from engine.songslover import SongsLover 
    from engine.justnaija import JustNaija
    from engine.naijamusic import NaijaMusic

    jn = JustNaija()
    sl = Songslover()
    nm = NaijaMusic()
    
    # check the allowed category method to see the categories allowed for each engine
    slresults = sl.fetch(category='albums',page=1)
    jnresults = jn.fetch(category='album' ,page=1)
    nmresults = nm.fetch(category='albums-eps',page=1)

    results = dict(
              Songslover=slresults,
              JustNaija=jnresults,
              NaijaMusic=nmresults,
              )

    # pretty print the result from each engine
    for k, v in results.items():
        print(f"-------------{k}------------")
        for result in v:
            pprint.pprint(result)
```


## TODO's
- TODO: Creates Enum for some objects and results items.
- TODO: Create a Caching Mechanism for results.
- TODO: Handle Engine Errors and Exceptions.
- TODO: Make Request Handling Asynchronous.
- TODO: Seperate Engine's parse single object method from search method.
- TODO: Add more Music Engines.
- TODO: Scrape some existing Engines for more track details. 
- TODO: Put Summary for every Engine.




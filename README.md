# GETMUSIC 
>               "*Why must I pay for what makes me Happy ? Why can't I `getmusic` for free?*"
<p align="center"><img width="200" src="https://github.com/derhnyel/getmusic/blob/build-engine/assets/logo.jpg?raw=true" alt="logo">
</p>
<hr>
**Getmusic** is a package that gives you access to a Whole variety of Music from your favourite artists. It lets you query popular music download sites and scrape for song and album titles, download links to albums and tracks and albums/track details.
<hr>

### Supported Engines

Music Engines include:
- SongsLover
- Mp3Juices
- NaijaMusic
- AceMusic
- JustNaija

View all supported engines [here](https://github.com/derhnyel/getmusic/blob/build-engine/docs/supported_engines.md?raw=true)



### Development

#### Clone the respository

- Clone this repo `git clone git@github.com:derhnyel/getmusic.git`

## Usage
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



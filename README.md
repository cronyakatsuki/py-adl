# py-adl
My python version of the popular adl wrapper for trackma and anime downloader that currently only works for windblows 10.

I created this program because I really like the idea of the original [adl](https://github.com/RaitaroH/adl) wrapper script for [anime-downloader](https://github.com/anime-dl/anime-downloader) and [trackma](https://github.com/z411/trackma), but wasn't able to use once I got over to windows and now here I'm trying to port it to python.

This is not supposed to be one on one port so that it is easier on my sanity.

Current features:
- Choose trackma account
- retrieve list from trackma
- Choose what player to use from cli
- downloading
- watch next episode of an anime
- watch left episode
- watch all episodes
- watch custom interval
- rewatch current episode
- watch custom episode
- update anime meta
- use trackma for tracking your progress
- use anime downloader for streaming and downloading

There is more I wanna do, and would love to add some screenshots.

### How to use

To be able to use this python script you need to have python installed and have trackma and anime downloader installed. To download and install anime downloader on windows you should checkout out it's [install documentation](https://anime-downlader.readthedocs.io/en/latest/usage/installation.html#windows). To install trackma you have to simply run `pip install -U trackma`.

### How to compile

I have included an compile poweshell script that allows you to compile py-adl into a executable that you can find in the **dist** folder after running it. **But you need to have pyinstaller installed on your system**. To install it run `pip install pyinstaller`.

To run the compile.ps1 script all you have to do is open an powershell window in the directory of the script and type .\compile.ps1 **or** if you don't want to run the script you can run this command in a the powershell or cmd window `pyinstaller .\adl.py --onefile --add-data 'good_title.txt;.' --add-data '.\problem_title.txt;.' --add-data '.\print_fzf.py;.'` and that will compile it on any system.
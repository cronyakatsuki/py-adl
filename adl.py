import os, subprocess, sys, argparse
from iterfzf import iterfzf
from time import sleep

# global variables
account = "0" # trackma account
retrieve = True # retrieve new list
player = "mpv" # specific player
download = False # specify whether to download or not
msg = "watching" # msg for the watch prompt
good_title = open("good_title.txt").readlines() # the list of good titles
problematic_titles = open("problem_title.txt").readlines() # list of problematic titles

ap = argparse.ArgumentParser()

ap.add_argument("-a", "--account", required=False,
                help="By default trackma will use account 1. Use '-a 2' for example to change trackma account")
ap.add_argument("-p", "--player", required=False,
                help="Define player used for streaming. Ex: \033[0;36mpyadl -p mpv\033[0m")
ap.add_argument("-d", "--download", required=False, type=bool, nargs='?', const=True, default=False,
                help="Download instead of streaming")
ap.add_argument("-v", "--version", required=False, nargs='?', const=True,
                help="Display version and exit")

args = vars(ap.parse_args())

if args['account']:
    account = str(int(args["account"]) - 1)

if args["player"]:
    player = str(args["player"])

if args["download"]:
    download = True
    msg = "downloading"

if args["version"]:
    print("Pyadl version 0.1")
    sys.exit()
    
# colored print
def color_print(text):
    print("\033[0;36m" + text + " \033[0m")

# colored watch primpt
def watch_prompt(title, episode):
    print("Now " + msg + " \033[0;34m" + title + "\033[0m, episode \033[0;34m" + str(episode) + " \033[0m")

# colored input
def color_prommpt(text):
    return input("\033[0;34m" + text + "\033[0m")

# iter the list
def iter_list(alist):
    for anime in alist:
        yield anime.strip()
        sleep(0.01)

# retrieve new list
def retrieve_list():
    color_print ("Running trackma retrieve for account " + account + "...")
    os.system("trackma -a " + account + " retrieve")
    os.system("cls")
    
# retrieve updated list
def retrieve_list_update(account):
    color_print("Running trackma retrieve for account " + account + " to get the updated list...")
    os.system("trackma -a " + account + " retrieve")
    os.system("cls")

# load list
def load_list():
    alist = subprocess.getoutput("trackma -a " + account + " list").splitlines()
    alist.pop(0)
    alist.pop()
    return alist

# exit prompt
def exit_ask():
    while True:
        os.system("cls")
        choice = color_prommpt("Want to watch another anime? [Y/n]: ")
        if choice == "":
            sys.exit()
        elif choice == "N" or choice == "n":
            sys.exit()
        elif choice == "Y" or choice == "y":
            return

# check for problematic title
def check_title(title):
    for problem in problematic_titles:
        if problem.__contains__(title):
            title = good_title[problematic_titles.index(problem)]
    return title

# get your title
def get_title(full_choice):
    full_choice = full_choice[9:55]
    full_choice = full_choice.rstrip(".")
    title = check_title(full_choice)
    return title

# get episode
def get_episode(full_choice):
    full_choice = full_choice[58:60]
    return int(full_choice)

# get all episodes
def get_all_episodes(full_choice):
    full_choice = full_choice[63:65]
    return full_choice

# get score
def get_score(full_choice):
    full_choice = full_choice[68:71]
    return full_choice

# next episode
def next_episode(title,episode):
    if not download:
        watch_next = True
        while watch_next:
            episode = episode + 1
            watch_prompt(title, str(episode))
            os.system('anime dl "'  + title + '" --episodes ' + str(episode) + ' --play ' + player)
            while True:
                color_print("Current watched episode: " + str(episode))
                yn = color_prommpt("Wanna watch next episode? [Y/n]: ")
                if yn == "Y" or yn == "y":
                    break
                elif yn == "N" or yn == "n":
                    watch_next = False
                    break
    else:
        episode = episode + 1
        watch_prompt(title, str(episode))
        os.system('anime dl "'  + title + '" --episodes ' + str(episode))

# all from last watched
def all_from_last(title,episode):
    watch_prompt(title, str(episode) + " all left episodes")
    if not download:
        os.system('anime dl "'  + title + '" --episodes ' + str(episode + 1) + ': --play' + player)
    else:
        os.system('anime dl "'  + title + '" --episodes ' + str(episode + 1) + ':')

# all episode
def all_episodes(title):
    watch_prompt(title, "all")
    if not download:
        os.system('anime dl "'  + title + '" --episodes 1: --play ' + player)
    else:
        os.system('anime dl "'  + title + '" --episodes 1:')

# watch from custom range
def custom_episode_range(title):
    begginig = color_prommpt("Beggining of interval?: ")
    end = color_prommpt("End of interval?: ")
    watch_prompt(title, begginig + " to " + end)
    if not download:
        os.system('anime dl "' + title + '" --episodes ' + begginig + ':' + end +' --play ' + player)
    else:
        os.system('anime dl "' + title + '" --episodes ' + begginig + ':' + end)

# add to last watched m
def next_plus_n(title, episode, action):
    watch_prompt(title, str(episode + int(action)))
    if not download:
        os.system('anime dl "'  + title + '" --episodes ' + str(episode + int(action)) + ' --play ' + player)
    else:
        os.system('anime dl "'  + title + '" --episodes ' + str(episode + int(action)))

# rewatch current episode
def rewatch_episode(title, episode):
    watch_prompt(title, str(episode))
    if not download:
        os.system('anime dl "' + title + '" --episodes ' + str(episode) + ' --play ' + player)
    else:
        os.system('anime dl "' + title + '" --episodes ' + str(episode))

# watch custom episode
def custom_episode(title):
    episode = color_prommpt("Enter custom episode: ")
    watch_prompt(title, episode)
    if not download:
        os.system('anime dl "' + title + '" --episodes ' + episode + ' --play ' + player)
    else:
        os.system('anime dl "' + title + '" --episodes ' + episode)
    
# update title
def update_title(title, episode):
    color_print("Current episode for " + title + " is " + str(episode))
    custom = color_prommpt("Enter updated episode number: ")
    if custom != "":
        os.system('trackma -a ' + account + ' update "' + title + '" ' + custom)
        os.system('trackma -a' + account + ' send')
        retrieve_list_update(account)
    else:
        color_print("Skipping updating...")
  
# update score
def update_score(title, score):
    color_print("Current score for " + title + " is " + score)
    custom = color_prommpt("Enter updated score: ")
    if custom != "":
        os.system('trackma -a ' + account + ' score "' + title + '" ' + custom)
        os.system('trackma -a' + account + ' send')
        retrieve_list_update(account)
    else:
        color_print("Skipping updating...")

# update question
def update_question(title, episode, score):
    while True:
        color_print("Skipping watching episodes. Modifing entry.")
        choice = color_prommpt("Update episode number or update score [E/s]: ")
        if choice == "e" or choice == "E":
            update_title(title, episode)
            break
        elif choice == "s" or choice == "S":
            update_score(title, score)
            break

# ask if you wanna continus watching
def wanna_continu_watch():
    while True:
        if not download:
            yn = color_prommpt("Wanna continue watching? [Y/n]: ")
        else:
            yn = color_prommpt("Wanna continue downloading? [Y/n]: ")
        if yn == "y" or yn == "Y":
            return True
        elif yn == "n" or yn == "N":
            return False

# ask if you wanna update title meta after watch
def wanna_update_title_after_watch(title, episode, score):
    if not download:
        while True:
            yn = color_prommpt("Wanna update episode number or update score of watched anime? [N/e/s]: ")
            if yn == "E" or yn == "e":
                update_title(title, episode)
                break
            elif yn == "S" or yn == "s":
                update_score(title, score)
                break
            elif yn == "N" or yn == "n":
                break

# choose what to do with episode
def choose_episode():
    os.system("cls")
    color_print("Enter lowercase or uppercase to issue command:")
    color_print("   N - Next episode (default, press <ENTER>)")
    color_print("   L - from current to Last known:")
    color_print("   A - All available, from episode 1")
    color_print("   I - custom Interval (range) of episodes")
    color_print("  0-9 - Plus n episodes relative to last seen (type number)")
    color_print("   R - Rewatch/redownload current episode in list")
    color_print("   C - Custom episode")
    color_print("   U - Update entry chosen instead of streaming")
    color_print("   S - Skip. Choose another show.")
    return color_prommpt("Your choice? [N/l/a/i/0-9/r/c/u/s]: ")

# main loop
while True:
    # retrieving the list on start
    if retrieve:
        retrieve_list()
        retrieve = False
    
    # get the list of anime
    alist = load_list()
    # choose an anime from the list
    choice = iterfzf(iter_list(alist))
    
    if choice:
        # get the whole choice into a string
        full_choice = "".join(choice)
        # get the title
        title = get_title(full_choice)
        # get current episode
        episode = get_episode(full_choice)
        # get latest episode
        last_episode = get_all_episodes(full_choice)
        # get current score
        score = get_score(full_choice)
        
        # the watch loop
        while True:
            # choose what to do with the choosen anime
            action = choose_episode()
            # watch next episode
            if action == "":
                next_episode(title, episode)
                wanna_update_title_after_watch(title, episode, score)
                break
            # same
            elif action == "n" or action == "N":
                next_episode(title, episode)
                wanna_update_title_after_watch(title, episode, score)
                break
            # watch all left episodes
            elif action == "l" or action == "L":
                all_from_last(title, episode,last_episode)
                wanna_update_title_after_watch(title, episode, score)
                break
            # watch every episode available
            elif action == "a" or action == "A":
                all_episodes(title)
                wanna_update_title_after_watch(title, episode, score)
                break
            # custom range of episodes
            elif action == "i" or action == "I":
                custom_episode_range(title)
                if wanna_continu_watch():
                    continue
                else:
                    wanna_update_title_after_watch(title, episode, score)
                    break
            # something?
            elif action == "1" or action == "2" or action == "3" or action == "4" or action == "5" or action == "6" or action == "7" or action == "8" or action == "9":
                next_plus_n(title, episode, action)
                if wanna_continu_watch():
                    continue
                else:
                    wanna_update_title_after_watch(title, episode, score)
                    break
            # rewatch current episode
            elif action == "r" or action == "R":
                rewatch_episode(title, episode)
                if wanna_continu_watch():
                    continue
                else:
                    wanna_update_title_after_watch(title, episode, score)
                    break
            # watch custom episode
            elif action == "c" or action == "C":
                custom_episode(title)
                if wanna_continu_watch():
                    continue
                else:
                    wanna_update_title_after_watch(title, episode, score)
                    break
            # update anime meta
            elif action == "u" or action == "U":
                update_question(title, episode, score)
                break
            # skip the anime
            elif action == "s" or action == "S":
                break
    else:
        exit_ask()
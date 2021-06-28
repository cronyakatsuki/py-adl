import os, subprocess, sys
from symbol import continue_stmt
from iterfzf import iterfzf
from time import sleep

# global variables
account = "0" # choose an account
episode = "" # specific episode
retrieve = True # retrieve new list
player = "mpv" # specific player

# colored print
def color_print(text):
    print("\033[0;36m" + text + " \033[0m")

# colored watch primpt
def watch_prompt(title, episode):
    print("Now watching \033[0;34m" + title + "\033[0m, episode \033[0;34m" + str(episode) + " \033[0m")

# colored input
def color_prommpt(text):
    return input("\033[0;34m" + text + "\033[0m")

# iter the list
def iter_list(alist):
    for anime in alist:
        yield anime.strip()
        sleep(0.01)

# retrieve new list
def retrieve_list(account):
    color_print ("Running trackma retrieve for account " + account + "...")
    os.system("trackma -a " + account + " retrieve")
    os.system("cls")

# load list
def load_list(account):
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

# get your title
def get_title(full_choice):
    full_choice = full_choice[9:55]
    full_choice = full_choice.rstrip(".")
    return full_choice

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
def next_episode(title,episode,player):
    watch_prompt(title, str(episode))
    os.system('anime dl "'  + title + '" --episodes ' + str(episode + 1) + ' --play ' + player)

# all from last watched
def all_from_last(title,episode, player):
    watch_prompt(title, str(episode) + " all left episodes")
    os.system('anime dl "'  + title + '" --episodes ' + str(episode + 1) + ': --play' + player)

# all episode
def all_episodes(title, player):
    watch_prompt(title, "all")
    os.system('anime dl "'  + title + '" --episodes 1: --play ' + player)

# watch from custom range
def custom_episode_range(title, player):
    begginig = color_prommpt("Beggining of interval?: ")
    end = color_prommpt("End of interval?: ")
    watch_prompt(title, begginig + " to " + end)
    os.system('anime dl "' + title + '" --episodes ' + begginig + ':' + end +' --play ' + player)

# add to last watched m
def next_plus_n(title, episode, player, action):
    watch_prompt(title, str(episode + int(action)))
    os.system('anime dl "'  + title + '" --episodes ' + str(episode + int(action)) + ' --play ' + player)

# rewatch current episode
def rewatch_episode(title, episode, player):
    watch_prompt(title, str(episode))
    os.system('anime dl "' + title + '" --episodes ' + str(episode) + ' --play ' + player)

# watch custom episode
def custom_episode(title, player):
    episode = color_prommpt("Enter custom episode: ")
    watch_prompt(title, episode)
    os.system('anime dl "' + title + '" --episodes ' + episode + ' --play ' + player)
    
# update title
def update_title(title, episode):
    color_print("Current episode for " + title + " is " + str(episode))
    custom = color_prommpt("Enter updated episode number: ")
    if custom != "":
        os.system('trackma -a ' + account + ' update "' + title + '" ' + custom)
    else:
        color_print("Skipping updating...")

# update score
def update_score(title, score):
    color_print("Current score for " + title + " is " + score)
    custom = color_prommpt("Enter updated score: ")
    if custom != "":
        os.system('trackma -a ' + account + ' score "' + title + '" ' + custom)
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
        yn = color_prommpt("Wanna continus watching?: ")
        if yn == "y" or yn == "Y":
            return True
        elif yn == "n" or yn == "N":
            return False

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

while True:
    if retrieve:
        retrieve_list(account)
        retrieve = False
    
    alist = load_list(account)
    choice = iterfzf(iter_list(alist))
    
    if choice:
        full_choice = "".join(choice)
        title = get_title(full_choice)
        episode = get_episode(full_choice)
        last_episode = get_all_episodes(full_choice)
        score = get_score(full_choice)
        watching = True
        while True:
            action = choose_episode(watching)
            if action == "":
                next_episode(title, episode, player)
                if wanna_continu_watch():
                    continue
                else:
                    break
            elif action == "n" or action == "N":
                next_episode(title, episode, player)
                if wanna_continu_watch():
                    continue
                else:
                    break
            elif action == "l" or action == "L":
                all_from_last(title, episode,last_episode, player)
                break
            elif action == "a" or action == "A":
                all_episodes(title, player)
                break
            elif action == "i" or action == "I":
                custom_episode_range(title, player)
                if wanna_continu_watch():
                    continue
                else:
                    break
            elif action == "1" or action == "2" or action == "3" or action == "4" or action == "5" or action == "6" or action == "7" or action == "8" or action == "9":
                next_plus_n(title, episode, player, action)
                if wanna_continu_watch():
                    continue
                else:
                    break
            elif action == "r" or action == "R":
                rewatch_episode(title, episode, player)
                if wanna_continu_watch():
                    continue
                else:
                    break
            elif action == "c" or action == "C":
                custom_episode(title, player)
                if wanna_continu_watch():
                    continue
                else:
                    break
            elif action == "u" or action == "U":
                update_question(title, episode, score)
                break
            elif action == "s" or action == "S":
                break
    else:
        exit_ask()
import os, subprocess, sys
from iterfzf import iterfzf
from time import sleep
account = "0"
episode = ""
retrieve = True
player = "mpv"

def color_print(text):
    print("\033[0;36m" + text + " \033[0m")

def color_prommpt(text):
    return input("\033[0;34m" + text + "\033[0m")

def print_list(alist):
    for anime in alist:
        print(alist[alist.index(anime)])

def iter_list(alist):
    for anime in alist:
        yield anime.strip()
        sleep(0.01)

def retrieve_list(account):
    color_print ("Running trackma retrieve for account " + account + "...")
    os.system("trackma -a " + account + " retrieve")
    os.system("cls")

def load_list(account):
    alist = subprocess.getoutput("trackma -a " + account + " list").splitlines()
    alist.pop(0)
    alist.pop()
    return alist

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
    
def get_title(choice):
    full_choice = "".join(choice)
    full_choice = full_choice[9:55]
    full_choice = full_choice.rstrip(".")
    return full_choice

def get_episode(choice):
    full_choice = "".join(choice)
    full_choice = full_choice[58:60]
    return int(full_choice)

def get_all_episodes(choice):
    full_choice = "".join(choice)
    full_choice = full_choice[63:65]
    return full_choice

def next_episode(title,episode,player):
    os.system('anime dl "'  + title + '" --episodes ' + str(episode + 1) + ' --play ' + player)

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
        title = get_title(choice)
        episode = get_episode(choice)
        all_episodes = get_all_episodes(choice)
        while True:
            action = choose_episode()
            if action == "":
                next_episode(title, episode, player)
                break
            elif action == "n" or action == "N":
                break
            elif action == "l" or action == "L":
                break
            elif action == "a" or action == "A":
                break
            elif action == str(range(0,9)):
                break
            elif action == "r" or action == "R":
                break
            elif action == "c" or action == "C":
                break
            elif action == "u" or action == "U":
                break
            elif action == "s" or action == "S":
                break
    else:
        exit_ask()
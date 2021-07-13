import os, subprocess, sys, argparse, signal
from time import sleep

# argument parser
ap = argparse.ArgumentParser()

ap.add_argument("-a", "--account", required=False,
                help="By default trackma will use account 1. Use '-a 2' for example to change trackma account")
ap.add_argument("-p", "--player", required=False,
                help="Define player used for streaming. Ex: \033[0;36mpyadl -p mpv\033[0m")
ap.add_argument("-d", "--download", required=False, type=bool, nargs='?', const=True, default=False,
                help="Download instead of streaming")
ap.add_argument("-v", "--version", required=False, nargs='?', const=True,
                help="Display version and exit")
ap.add_argument("-r", "--retrieve", required=False, nargs='?', const=True,
                help="Don't retrieve trackma list on startup")

args = vars(ap.parse_args())

# get account
if args['account']:
    account = str(int(args["account"]) - 1) # take the account from input
else:
    account = "0" # default account

# get player
if args["player"]:
    player = str(args["player"]) # get player from user
else:
    player = "mpv" # default player
    
# enable downloading
if args["download"]:
    download = True # enable downloading
    msg = "downloading" # download message
else:
    download = False # specify whether to download or not
    msg = "watching" # msg for the watch prompt

# print the version
if args["version"]:
    print("Py-adl version 0.1.1")
    sys.exit()

# don't retrieve on startup
if args["retrieve"]:
    retrieve = False
else:
    retrieve = True # retrieve new list

# required files
dn = os.path.dirname(os.path.realpath(__file__)) # get current directory of the script
good_title = open(dn + "/good_title.txt").readlines() # the list of good titles
problematic_titles = open(dn + "/problem_title.txt").readlines() # list of problematic titles
fzf_file = open(dn + "/fzf.txt", "w+") # temp file for fzf
fzf_file_path = dn +"/fzf.txt" # path of the temp file
print_fzf_path = "python " + dn + "/print_fzf.py" # print the fzf file

# exit function
def exit_adl():
    fzf_file.close()
    os.remove(fzf_file_path)
    sys.exit()

def interupt_command(signum, frame):
    exit_adl()

signal.signal(signal.SIGINT, interupt_command)

# colored print
def color_print(text):
    print("\033[0;36m" + text + " \033[0m")

# colored watch primpt
def watch_prompt(title, episode):
    print("Now " + msg + " \033[0;34m" + title + "\033[0m, episode \033[0;34m" + str(episode) + " \033[0m")

# colored input
def color_prommpt(text):
    return input("\033[0;34m" + text + "\033[0m")

# retrieve new list
def retrieve_list():
    color_print ("Running trackma retrieve for account " + account + "...")
    subprocess.call("trackma -a " + account + " retrieve")
    subprocess.call("cls", shell=True)
    
# retrieve updated list
def retrieve_list_update():
    color_print("Running trackma retrieve for account " + account + " to get the updated list...")
    subprocess.call("trackma -a " + account + " retrieve")
    subprocess.call("cls", shell=True)

# load list
def load_list():
    alist = subprocess.getoutput("trackma -a " + account + " list").splitlines()
    alist.pop(0)
    alist.pop()
    return alist

# write list to a file
def list2file(list, file):
    for line in list:
        file.write(line)
        if not list.index(line) == len(list) - 1 :
            file.write("\n")

# exit prompt
def exit_ask():
    while True:
        subprocess.call("cls", shell=True)
        choice = color_prommpt("Want to watch another anime? [Y/n]: ")
        if choice == "N" or choice == "n":
            exit_adl()
        elif choice == "Y" or choice == "y" or choice == "":
            return

# check for problematic title
def check_title(title):
    for problem in problematic_titles:
        if problem.__contains__(title):
            title = good_title[problematic_titles.index(problem)]
    return title

# get your title
def get_title(choice):
    choice = choice[9:55]
    choice = choice.rstrip(".")
    title = check_title(choice)
    return title

# get episode
def get_episode(choice):
    choice = choice[58:60]
    return int(choice)

# get all episodes
def get_all_episodes(choice):
    choice = choice[63:65]
    return choice

# get score
def get_score(choice):
    choice = choice[68:71]
    return choice

# watch animes
def watch(cmd):
    subprocess.run(cmd)

# next episode
def next_episode(title,episode):
    if not download:
        watch_next = True
        while watch_next:
            episode = episode + 1
            watch_prompt(title, str(episode))
            watch('anime dl "'  + title + '" --episodes ' + str(episode) + ' --play ' + player)
            while True:
                color_print("Current watched episode: " + str(episode))
                yn = color_prommpt("Wanna watch next episode? [Y/n]: ")
                if yn == "Y" or yn == "y" or yn == "":
                    break
                elif yn == "N" or yn == "n":
                    watch_next = False
                    break
    else:
        episode = episode + 1
        watch_prompt(title, str(episode))
        watch('anime dl "'  + title + '" --episodes ' + str(episode))

# all from last watched
def all_from_last(title,episode):
    watch_prompt(title, str(episode) + " all left episodes")
    if not download:
        watch('anime dl "'  + title + '" --episodes ' + str(episode + 1) + ': --play s' + player)
    else:
        watch('anime dl "'  + title + '" --episodes ' + str(episode + 1) + ':')

# all episode
def all_episodes(title):
    watch_prompt(title, "all")
    if not download:
        watch('anime dl "'  + title + '" --episodes 1: --play ' + player)
    else:
        watch('anime dl "'  + title + '" --episodes 1:')

# watch from custom range
def custom_episode_range(title):
    begginig = color_prommpt("Beggining of interval?: ")
    end = color_prommpt("End of interval?: ")
    watch_prompt(title, begginig + " to " + end)
    if not download:
        watch('anime dl "' + title + '" --episodes ' + begginig + ':' + end +' --play ' + player)
    else:
        watch('anime dl "' + title + '" --episodes ' + begginig + ':' + end)

# add to last watched m
def next_plus_n(title, episode, action):
    watch_prompt(title, str(episode + int(action)))
    if not download:
        watch('anime dl "'  + title + '" --episodes ' + str(episode + int(action)) + ' --play ' + player)
    else:
        watch('anime dl "'  + title + '" --episodes ' + str(episode + int(action)))

# rewatch current episode
def rewatch_episode(title, episode):
    watch_prompt(title, str(episode))
    if not download:
        watch('anime dl "' + title + '" --episodes ' + str(episode) + ' --play ' + player)
    else:
        watch('anime dl "' + title + '" --episodes ' + str(episode))

# watch custom episode
def custom_episode(title):
    episode = color_prommpt("Enter custom episode: ")
    watch_prompt(title, episode)
    if not download:
        watch('anime dl "' + title + '" --episodes ' + episode + ' --play ' + player)
    else:
        watch('anime dl "' + title + '" --episodes ' + episode)
    
# update title
def update_title(title, episode):
    color_print("Current episode for " + title + " is " + str(episode))
    custom = color_prommpt("Enter updated episode number: ")
    if custom != "":
        subprocess.call('trackma -a ' + account + ' update "' + title + '" ' + custom)
        subprocess.call('trackma -a' + account + ' send')
        retrieve_list_update(account)
    else:
        color_print("Skipping updating...")

# update score
def update_score(title, score):
    color_print("Current score for " + title + " is " + score)
    custom = color_prommpt("Enter updated score: ")
    if custom != "":
        subprocess.call('trackma -a ' + account + ' score "' + title + '" ' + custom)
        subprocess.call('trackma -a' + account + ' send')
        retrieve_list_update(account)
    else:
        color_print("Skipping updating...")

# update question
def update_question(title, episode, score):
    while True:
        color_print("Skipping watching episodes. Modifing entry.")
        choice = color_prommpt("Update episode number or update score [E/s]: ")
        if choice == "e" or choice == "E" or choice == "":
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
        if yn == "y" or yn == "Y" or yn == "":
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
            elif yn == "N" or yn == "n" or yn == "":
                break


# choose what to do with episode
def choose_episode():
    subprocess.call("cls", shell=True)
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
    
    # write list to file
    list2file(alist, fzf_file)
    
    # reload file (I Guess ??)
    fzf_file.seek(0)
    
    # get choice from fzf
    choice = subprocess.getoutput(print_fzf_path + ' | fzf --ansi --reverse --prompt "Choose anime to watch: "')
    
    if choice:
        # get the title
        title = get_title(choice)
        # get current episode
        episode = get_episode(choice)
        # get latest episode
        last_episode = get_all_episodes(choice)
        # get current score
        score = get_score(choice)
        
        # the watch loop
        while True:
            # choose what to do with the choosen anime
            action = choose_episode()
            # watch next episode
            if action == "n" or action == "N" or action == "":
                next_episode(title, episode)
                wanna_update_title_after_watch(title, episode, score)
                break
            # watch all left episodes
            elif action == "l" or action == "L":
                all_from_last(title, episode)
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
#!/usr/bin/env python

import os, subprocess, sys, argparse, signal

# required files
CURRENT_DIR = os.getcwd()

if sys.platform == "win32":
    CONFIG_FILE_PATH = os.path.join('C:\\', 'Users', str(os.getlogin()), 'Documents', 'Adl', 'config.json')
    DEFAULT_DOWNLOAD_LOCATION = os.path.join('C:\\', 'Users', str(os.getlogin()), 'Videos', 'Anime')
    CLEAR = 'cls'
else:
    CONFIG_FILE_PATH = os.path.join('home', str(os.getlogin()), '.config', 'adl', 'config.json')
    DEFAULT_DOWNLOAD_LOCATION = os.path.join('home', str(os.getlogin()), 'Videos', 'Anime')
    CLEAR = 'clear'

PROBLEMATIC_TITLES = ['Komi-san wa, Komyushou desu ',
                'SKâˆž']
GOOD_TITLES = ['Komi-san wa, Komyushou desu.',
                'SK∞']
                
# exit function
def exit_adl():
    sys.exit()

# 
def interupt_command(signum, frame):
    exit_adl()

# colored print
def color_print(text):
    print(f"\033[0;36m{text } \033[0m")

# colored watch primpt
def watch_prompt(title, episode, msg):
    print(f"Now {msg} \033[0;34m{title}\033[0m, episode \033[0;34m{str(episode)} \033[0m")

# colored input
def color_prommpt(text):
    return input(f"\033[0;34m{text}\033[0m")

# retrieve new list
def retrieve_list(account):
    color_print (f"Running trackma retrieve for account {account}...")
    subprocess.run(["trackma", "-a", account, "retrieve"])
    subprocess.run(CLEAR)
    
# retrieve updated list
def retrieve_list_update(account):
    color_print(f"Running trackma retrieve for account {account} to get the updated list...")
    subprocess.run(["trackma", "-a", account, "retrieve"])
    subprocess.run(CLEAR)

# load list
def load_list(account):
    alist = subprocess.run(["trackma", "-a", account, "list"], stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()
    alist.pop(0)
    alist = alist[: len(alist) - 3]
    alist = "\n".join(alist)
    return alist

# exit prompt
def exit_ask():
    while True:
        subprocess.run(CLEAR)
        choice = color_prommpt("Want to watch another anime? [Y/n]: ")
        if choice == "N" or choice == "n":
            exit_adl()
        elif choice == "Y" or choice == "y" or choice == "":
            return

# check for problematic title
def check_title(title):
    for problem in PROBLEMATIC_TITLES:
        if problem == title:
            title = GOOD_TITLES[PROBLEMATIC_TITLES.index(problem)].encode('utf-8')
            title = title.decode('utf-8')
    return title

# get chosen anime info
def get_info(choice):
    # get index
    index = int(choice[4:7])

    # get title
    title = str(choice[9:-19])
    title = title.replace('.','')
    title = check_title(title)

    # get episode
    episode = int(choice[-19:-15])

    # get score
    score = int(choice[-10:-5])

    # print(f'/{title}/')
    # exit_adl()
    
    return index, title, episode, score

# watch animes
def watch(title, episode, download, provider, download_location):
    cmd = ['animdl']
    
    if download:
        cmd.append('download')
        if os.path.isdir(download_location):
            os.chdir(download_location)
        else:
            os.mkdir(download_location)
            os.chdir(download_location)
    else:
        cmd.append('stream')
    
    cmd.append(f'"{provider}:{title}"')
    cmd.append('-r')
    cmd.append(episode)

    subprocess.run(cmd)

    if download:
        os.chdir(CURRENT_DIR)

# next episode
def next_episode(title,episode, msg, download, provider, download_location):
    if not download:
        watch_next = True
        while watch_next:
            episode = episode + 1
            watch_prompt(title, str(episode), msg)
            watch(title, str(episode), download, provider, download_location)
            while True:
                color_print(f"Current watched episode: {str(episode)}")
                yn = color_prommpt("Wanna watch next episode? [Y/n]: ")
                if yn == "Y" or yn == "y" or yn == "":
                    break
                elif yn == "N" or yn == "n":
                    watch_next = False
                    break
    else:
        episode = episode + 1
        watch_prompt(title, str(episode), msg)
        watch(title, str(episode), download, provider, download_location)

# all from last watched
def all_from_last(title,episode, msg, download, provider, download_location):
    watch_prompt(title, f"{str(episode)} all left episodes", msg)
    watch(title, f'{str(episode + 1)}:', download, provider, download_location)

# all episode
def all_episodes(title, msg, download, provider, download_location):
    watch_prompt(title, "all", msg)
    watch(title, '1:', download, provider, download_location)

# watch from custom range
def custom_episode_range(title, msg, download, provider, download_location):
    begginig = color_prommpt("Beggining of interval?: ")
    end = color_prommpt("End of interval?: ")
    watch_prompt(title, f"{begginig} to {end}", msg)
    watch(title, f"{begginig}:{end}", download, provider, download_location)

# add to last watched m
def next_plus_n(title, episode, action, msg, download, provider, download_location):
    watch_prompt(title, str(episode + int(action)), msg)
    watch(title, str(episode + int(action)), download, provider, download_location)

# rewatch current episode
def rewatch_episode(title, episode, msg, download, provider, download_location):
    watch_prompt(title, str(episode), msg)
    watch(title, str(episode), download, provider, download_location)

# watch custom episode
def custom_episode(title, msg, download,provider, download_location):
    episode = color_prommpt("Enter custom episode: ")
    watch_prompt(title, episode, msg)
    watch(title, episode, download, provider, download_location)
    
# update title
def update_title(index, title, episode, account):
    color_print(f"Current episode for {title} is {str(episode)}")
    custom = color_prommpt("Enter updated episode number: ")
    if custom != "":
        subprocess.run(['trackma', '-a', account, 'update', str(index), custom])
        subprocess.run(['trackma', '-a', account, 'send'])
        retrieve_list_update(account)
    else:
        color_print("Skipping updating...")

# update score
def update_score(index, title, score, account):
    color_print(f"Current score for {title} is {score}")
    custom = color_prommpt("Enter updated score: ")
    if custom != "":
        subprocess.run(['trackma', '-a', account, 'score', str(index), custom])
        subprocess.run(['trackma', '-a', account, 'send'])
        retrieve_list_update(account)
    else:
        color_print("Skipping updating...")

# update question
def update_question(index, title, episode, score, account):
    while True:
        color_print("Skipping watching episodes. Modifing entry.")
        choice = color_prommpt("Update episode number or update score [E/s]: ")
        if choice == "e" or choice == "E" or choice == "":
            update_title(index, title, episode, account)
            break
        elif choice == "s" or choice == "S":
            update_score(index, title, score, account)
            break

# ask if you wanna continus watching
def wanna_continu_watch(download):
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
def wanna_update_title_after_watch(index, title, episode, score, download, account):
    if not download:
        while True:
            yn = color_prommpt("Wanna update episode number or update score of watched anime? [N/e/s]: ")
            if yn == "E" or yn == "e":
                update_title(index, title, episode, account)
                break
            elif yn == "S" or yn == "s":
                update_score(index, title, score, account)
                break
            elif yn == "N" or yn == "n" or yn == "":
                break

# choose what to do with episode
def choose_episode():
    subprocess.run(CLEAR)
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

def choose_episode_specific_show():
    subprocess.run(CLEAR)
    color_print("Enter lowercase or uppercase to issue command:")
    color_print("   A - All available, from episode 1")
    color_print("   I - custom Interval (range) of episodes")
    color_print("   C - Custom episode")
    color_print("   S - Skip. Exit adl.")
    return color_prommpt("Your choice? [A/i/c/s]: ")

def argument_and_config_parser():
    # config
    config = {}
    ConfigExists = False
    if os.path.exists(CONFIG_FILE_PATH):
        config_content = open(CONFIG_FILE_PATH, encoding='utf-8-sig').read()
        config = eval(config_content)
        ConfigExists = True

    # argument parser
    ap = argparse.ArgumentParser()

    ap.add_argument("-p", "--provider", required=False,
                    help="Define provider used for streaming (check \033[0;36m$anime dl --help\033[0m for providers list)")
    ap.add_argument("-s", "--show", required=False,
                    help='Watch custom show. Ep nr optional, careful with the quotes. Ex: \033[0;36m$adl -s "gegege 2018"\033[0m')
    ap.add_argument("-n", "--number", required=False,
                    help='Specify episode number that will be used with "-s / --show" option. Ex: \033[0;36m$adl -s "gegege 2018" -n "4"\033[0m')
    ap.add_argument("-a", "--account", required=False,
                    help="By default trackma will use account 1. Use '-a 2' for example to change trackma account")
    ap.add_argument("-d", "--download", required=False, type=bool, nargs='?', const=True, default=False,
                    help="Download instead of streaming")
    ap.add_argument("-l", "--download-location", required=False,
                    help="Define downloads location, Default location is in 'User folder/Videos/Anime'")
    ap.add_argument("-t", "--test-providers", required=False, type=bool, nargs='?', const=True, default=False,
                    help="Check the state of possible providers")
    ap.add_argument("-v", "--version", required=False, nargs='?', const=True,
                    help="Display version and exit")

    args = vars(ap.parse_args())
    
    # print the version
    if args["version"]:
        print("Py-adl version 1.1")
        sys.exit()

    # check if providers are working
    if args["test_providers"]:
        subprocess.run(["animdl", "test"])
        sys.exit()

    # get provider
    if args['provider']:
        provider = str(args["provider"])
    elif ConfigExists and 'provider' in config and config['provider']:
        provider = str(config["provider"])
    else:
        provider = "zoro"

    # get show
    if args['show']:
        show = str(args["show"])
    else:
        show = ""

    # get episode
    if args['number']:
        if args['number'] and args['show']:
            episode = int(args['number'])
        else:
            print("You need to also specify a show name to use this option")
            sys.exit()
    else:
        episode = 0

    # get account
    if args['account']:
        account = str(int(args["account"]) - 1) # take the account from input
    elif ConfigExists and 'account' in config and config["account"]:
        account = str(int(config["account"]) - 1) # take the account from config
    else:
        account = "0" # default account
        
    # enable downloading
    if args["download"]:
        download = True # enable downloading
        msg = "downloading" # download message
    else:
        download = False # specify whether to download or not
        msg = "watching" # msg for the watch prompt


    if not download and args["download_location"]:
        color_print("You need to be downloading to use this option!")
        exit_adl()
    elif download and args["download_location"]:
        download_location = str(args["download_location"])
    else:
        download_location = DEFAULT_DOWNLOAD_LOCATION


    return (provider, show, episode, account, download, msg, download_location)

def specific_show_loop(show, msg, download, provider, download_location):
    while True:
        # choose what to do with the choosen anime
        action = choose_episode_specific_show()
        if action == "a" or action == "A" or action == "":
            all_episodes(show, msg, download, provider, download_location)
            exit_adl()
        # custom range of episodes
        elif action == "i" or action == "I":
            custom_episode_range(show, msg, download, provider, download_location)
            if wanna_continu_watch(download):
                continue
            else:
                exit_adl()
        # watch custom episode
        elif action == "c" or action == "C":
            custom_episode(show, msg, download, provider, download_location)
            if wanna_continu_watch(download):
                continue
            else:
                exit_adl()
        # skip the anime
        elif action == "s" or action == "S":
            exit_adl()

def main_loop(retrieve, account, msg, download,provider, download_location):
    # main loop
    while True:
        # retrieving the list on start
        if retrieve:
            retrieve_list(account)
            retrieve = False
        
        # get the list of anime
        alist = load_list(account)
        
        # get choice from fzf
        choice = subprocess.run(["fzf", "--ansi", "--unicode", "--reverse", "--prompt", "Choose anime to watch: "], input=alist, stdout=subprocess.PIPE, encoding='utf-8').stdout
        
        if choice:
            # get needed info
            index, title, episode, score = get_info(choice)
            
            # the watch loop
            while True:
                # choose what to do with the choosen anime
                action = choose_episode()
                # watch next episode
                if action == "n" or action == "N" or action == "":
                    next_episode(title, episode, msg, download,provider, download_location)
                    wanna_update_title_after_watch(index, title, episode, score, download, account)
                    exit_ask()
                    break
                # watch all left episodes
                elif action == "l" or action == "L":
                    all_from_last(title, episode, msg, download,provider, download_location)
                    wanna_update_title_after_watch(index, title, episode, score, download, account)
                    exit_ask()
                    break
                # watch every episode available
                elif action == "a" or action == "A":
                    all_episodes(title, msg, download,provider, download_location)
                    wanna_update_title_after_watch(index, title, episode, score, download, account)
                    exit_ask()
                    break
                # custom range of episodes
                elif action == "i" or action == "I":
                    custom_episode_range(title, msg, download,provider, download_location)
                    if wanna_continu_watch(download):
                        continue
                    else:
                        wanna_update_title_after_watch(index, title, episode, score, download, account)
                        exit_ask()
                        break
                # something?
                elif action == "1" or action == "2" or action == "3" or action == "4" or action == "5" or action == "6" or action == "7" or action == "8" or action == "9":
                    next_plus_n(title, episode, action, msg, download,provider, download_location)
                    if wanna_continu_watch(download):
                        continue
                    else:
                        wanna_update_title_after_watch(index, title, episode, score, download, account)
                        exit_ask()
                        break
                # rewatch current episode
                elif action == "r" or action == "R":
                    rewatch_episode(title, episode, msg, download,provider, download_location)
                    if wanna_continu_watch(download):
                        continue
                    else:
                        wanna_update_title_after_watch(index, title, episode, score, download, account)
                        exit_ask()
                        break
                # watch custom episode
                elif action == "c" or action == "C":
                    custom_episode(title, msg, download,provider, download_location)
                    if wanna_continu_watch(download):
                        continue
                    else:
                        wanna_update_title_after_watch(index, title, episode, score, download, account)
                        exit_ask()
                        break
                # update anime meta
                elif action == "u" or action == "U":
                    update_question(index, title, episode, score, account)
                    exit_ask()
                    break
                # skip the anime
                elif action == "s" or action == "S":
                    break
        else:
            exit_ask()


def main():
    signal.signal(signal.SIGINT, interupt_command)
    # print("Inside")

    # setup env variables for better readability of outputs
    os.environ['LINES'] = '25'
    os.environ['COLUMNS'] = '120'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # get argument and config parameters
    (provider, show, episode, account, download, msg, download_location) = argument_and_config_parser()

    # retrieve the trackma list on run
    retrieve = True
    
    if not show == "" and not episode == 0:
        # watching just a specific show and episode only
         watch(show, str(episode), download, provider, download_location)
    elif not show == "":
        # choose want to do with a specific show
        specific_show_loop(show, msg, download, provider, download_location)
    else:
        # main loop that connets with your list with trackma
        main_loop(retrieve, account, msg, download,provider, download_location)
    exit_adl()

# run only if runned directly
if __name__ == "__main__" :
    main()

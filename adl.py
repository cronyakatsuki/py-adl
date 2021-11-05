import os, subprocess, sys, argparse, signal

# required files
DN = os.path.dirname(os.path.realpath(__file__)) # get current directory of the script
GOOD_TITLES = open(DN + "/good_title.txt").readlines() # the list of good titles
PROBLEMATIC_TITLES = open(DN + "/problem_title.txt").readlines() # list of problematic titles
FZF_FILE = open(DN + "/fzf.txt", "w+") # temp file for fzf
FZF_FILE_PATH = DN +"/fzf.txt" # path of the temp file
PRINT_FZF_PATH = "python " + DN + "/print_fzf.py" # print the fzf file

# exit function
def exit_adl():
    FZF_FILE.close()
    os.remove(FZF_FILE_PATH)
    sys.exit()

def interupt_command(signum, frame):
    exit_adl()

# colored print
def color_print(text):
    print("\033[0;36m" + text + " \033[0m")

# colored watch primpt
def watch_prompt(title, episode, msg):
    print("Now " + msg + " \033[0;34m" + title + "\033[0m, episode \033[0;34m" + str(episode) + " \033[0m")

# colored input
def color_prommpt(text):
    return input("\033[0;34m" + text + "\033[0m")

# retrieve new list
def retrieve_list(account):
    color_print ("Running trackma retrieve for account " + account + "...")
    subprocess.call("trackma -a " + account + " retrieve")
    subprocess.call("cls", shell=True)
    
# retrieve updated list
def retrieve_list_update(account):
    color_print("Running trackma retrieve for account " + account + " to get the updated list...")
    subprocess.call("trackma -a " + account + " retrieve")
    subprocess.call("cls", shell=True)

# load list
def load_list(account):
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
    for problem in PROBLEMATIC_TITLES:
        if problem.__contains__(title):
            title = GOOD_TITLES[PROBLEMATIC_TITLES.index(problem)]
    return title

# get your title
def get_title(choice):
    choice = choice[9:96]
    choice = choice.rstrip(".")
    title = check_title(choice)
    return title

# get episode
def get_episode(choice):
    choice = choice[98:100]
    return int(choice)

# get score
def get_score(choice):
    choice = choice[108:110]
    return choice

# watch animes
def watch(title, episode, download, provider, player):
    cmd = 'anime dl "' + title + '" --episodes ' + episode
    
    if not download:
        cmd += ' --play ' + player
    
    if not provider == "":
        cmd += ' --provider ' + provider
    
    subprocess.run(cmd)

# next episode
def next_episode(title,episode, msg, download, provider, player):
    if not download:
        watch_next = True
        while watch_next:
            episode = episode + 1
            watch_prompt(title, str(episode), msg)
            watch(title, str(episode), download, provider, player)
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
        watch_prompt(title, str(episode), msg)
        watch(title, str(episode), download, provider, player)

# all from last watched
def all_from_last(title,episode, msg, download, provider, player):
    watch_prompt(title, str(episode) + " all left episodes", msg)
    watch(title, str(episode + 1) + ':', download, provider, player)

# all episode
def all_episodes(title, msg, download, provider, player):
    watch_prompt(title, "all", msg)
    watch(title, '1:', download, provider, player)

# watch from custom range
def custom_episode_range(title, msg, download, provider, player):
    begginig = color_prommpt("Beggining of interval?: ")
    end = color_prommpt("End of interval?: ")
    watch_prompt(title, begginig + " to " + end, msg)
    watch(title, begginig + ':' + end, download, provider, player)

# add to last watched m
def next_plus_n(title, episode, action, msg, download, provider, player):
    watch_prompt(title, str(episode + int(action)), msg)
    watch(title, str(episode + int(action)), download, provider, player)

# rewatch current episode
def rewatch_episode(title, episode, msg, download, provider, player):
    watch_prompt(title, str(episode), msg)
    watch(title, str(episode), download, provider, player)

# watch custom episode
def custom_episode(title, msg, download,provider, player):
    episode = color_prommpt("Enter custom episode: ")
    watch_prompt(title, episode, msg)
    watch(title, episode, download, provider, player)
    
# update title
def update_title(title, episode, account):
    color_print("Current episode for " + title + " is " + str(episode))
    custom = color_prommpt("Enter updated episode number: ")
    if custom != "":
        subprocess.call('trackma -a ' + account + ' update "' + title + '" ' + custom)
        subprocess.call('trackma -a' + account + ' send')
        retrieve_list_update(account)
    else:
        color_print("Skipping updating...")

# update score
def update_score(title, score, account):
    color_print("Current score for " + title + " is " + score)
    custom = color_prommpt("Enter updated score: ")
    if custom != "":
        subprocess.call('trackma -a ' + account + ' score "' + title + '" ' + custom)
        subprocess.call('trackma -a' + account + ' send')
        retrieve_list_update(account)
    else:
        color_print("Skipping updating...")

# update question
def update_question(title, episode, score, account):
    while True:
        color_print("Skipping watching episodes. Modifing entry.")
        choice = color_prommpt("Update episode number or update score [E/s]: ")
        if choice == "e" or choice == "E" or choice == "":
            update_title(title, episode, account)
            break
        elif choice == "s" or choice == "S":
            update_score(title, score, account)
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
def wanna_update_title_after_watch(title, episode, score, download, account):
    if not download:
        while True:
            yn = color_prommpt("Wanna update episode number or update score of watched anime? [N/e/s]: ")
            if yn == "E" or yn == "e":
                update_title(title, episode, account)
                break
            elif yn == "S" or yn == "s":
                update_score(title, score, account)
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

def choose_episode_specific_show():
    subprocess.call("cls", shell=True)
    color_print("Enter lowercase or uppercase to issue command:")
    color_print("   A - All available, from episode 1")
    color_print("   I - custom Interval (range) of episodes")
    color_print("   C - Custom episode")
    color_print("   S - Skip. Exit adl.")
    return color_prommpt("Your choice? [A/i/c/s]: ")

def argument_parser():
    # argument parser
    ap = argparse.ArgumentParser()

    ap.add_argument("-p", "--player", required=False,
                    help="Define player used for streaming. Ex: \033[0;36mpyadl -p mpv\033[0m")
    ap.add_argument("-i", "--provider", required=False,
                    help="Define provider used for streaming (check \033[0;36m$anime dl --help\033[0m for providers list)")
    ap.add_argument("-s", "--show", required=False,
                    help='Watch custom show. Ep nr optional, careful with the quotes. Ex: \033[0;36m$adl -s "gegege 2018"\033[0m')
    ap.add_argument("-n", "--number", required=False,
                    help='Specify episode number that will be used with "-s / --show" option. Ex: \033[0;36m$adl -s "gegege 2018" -n "4"\033[0m')
    ap.add_argument("-a", "--account", required=False,
                    help="By default trackma will use account 1. Use '-a 2' for example to change trackma account")
    ap.add_argument("-d", "--download", required=False, type=bool, nargs='?', const=True, default=False,
                    help="Download instead of streaming")
    ap.add_argument("-t", "--test-providers", required=False, type=bool, nargs='?', const=True, default=False,
                    help="Check the state of possible providers")
    ap.add_argument("-v", "--version", required=False, nargs='?', const=True,
                    help="Display version and exit")

    args = vars(ap.parse_args())

    print(args)
    
    # print the version
    if args["version"]:
        print("Py-adl version 1.1")
        sys.exit()

    # check if providers are working
    if args["test_providers"]:
        subprocess.run("anime test")
        sys.exit()

    # get player
    if args["player"]:
        player = str(args["player"]) # get player from user
    else:
        player = "mpv" # default player

    # get provider
    if args['provider']:
        provider = str(args["provider"])
    else:
        provider = ""

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
    else:
        account = "0" # default account
        
    # enable downloading
    if args["download"]:
        download = True # enable downloading
        msg = "downloading" # download message
    else:
        download = False # specify whether to download or not
        msg = "watching" # msg for the watch prompt


    return (player, provider, show, episode, account, download, msg)

def specific_show_loop(show, msg, download, provider, player):
    while True:
        # choose what to do with the choosen anime
        action = choose_episode_specific_show()
        if action == "a" or action == "A" or action == "":
            all_episodes(show, msg, download, provider, player)
            exit_adl()
        # custom range of episodes
        elif action == "i" or action == "I":
            custom_episode_range(show, msg, download, provider, player)
            if wanna_continu_watch(download):
                continue
            else:
                exit_adl()
        # watch custom episode
        elif action == "c" or action == "C":
            custom_episode(show, msg, download, provider, player)
            if wanna_continu_watch(download):
                continue
            else:
                exit_adl()
        # skip the anime
        elif action == "s" or action == "S":
            exit_adl()

def main_loop(retrieve, account, msg, download,provider,player):
    # main loop
    while True:
        # retrieving the list on start
        if retrieve:
            retrieve_list(account)
            retrieve = False
        
        # get the list of anime
        alist = load_list(account)
        
        # write list to file
        list2file(alist, FZF_FILE)
        
        # reload file (I Guess ??)
        FZF_FILE.seek(0)
        
        # get choice from fzf
        choice = subprocess.getoutput(PRINT_FZF_PATH + ' | fzf --ansi --reverse --prompt "Choose anime to watch: "')
        
        if choice:
            # get the title
            title = get_title(choice)
            # get current episode
            episode = get_episode(choice)
            # get current score
            score = get_score(choice)
            
            # the watch loop
            while True:
                # choose what to do with the choosen anime
                action = choose_episode()
                # watch next episode
                if action == "n" or action == "N" or action == "":
                    next_episode(title, episode, msg, download,provider,player)
                    wanna_update_title_after_watch(title, episode, score, download, account)
                    exit_ask()
                    break
                # watch all left episodes
                elif action == "l" or action == "L":
                    all_from_last(title, episode, msg, download,provider,player)
                    wanna_update_title_after_watch(title, episode, score, download, account)
                    exit_ask()
                    break
                # watch every episode available
                elif action == "a" or action == "A":
                    all_episodes(title, msg, download,provider,player)
                    wanna_update_title_after_watch(title, episode, score, download, account)
                    exit_ask()
                    break
                # custom range of episodes
                elif action == "i" or action == "I":
                    custom_episode_range(title, msg, download,provider,player)
                    if wanna_continu_watch(download):
                        continue
                    else:
                        wanna_update_title_after_watch(title, episode, score, download, account)
                        exit_ask()
                        break
                # something?
                elif action == "1" or action == "2" or action == "3" or action == "4" or action == "5" or action == "6" or action == "7" or action == "8" or action == "9":
                    next_plus_n(title, episode, action, msg, download,provider,player)
                    if wanna_continu_watch(download):
                        continue
                    else:
                        wanna_update_title_after_watch(title, episode, score, download, account)
                        exit_ask()
                        break
                # rewatch current episode
                elif action == "r" or action == "R":
                    rewatch_episode(title, episode, msg, download,provider,player)
                    if wanna_continu_watch(download):
                        continue
                    else:
                        wanna_update_title_after_watch(title, episode, score, download, account)
                        exit_ask()
                        break
                # watch custom episode
                elif action == "c" or action == "C":
                    custom_episode(title, msg, download,provider,player)
                    if wanna_continu_watch(download):
                        continue
                    else:
                        wanna_update_title_after_watch(title, episode, score, download, account)
                        exit_ask()
                        break
                # update anime meta
                elif action == "u" or action == "U":
                    update_question(title, episode, score, account)
                    exit_ask()
                    break
                # skip the anime
                elif action == "s" or action == "S":
                    break
        else:
            exit_ask()


def main():
    signal.signal(signal.SIGINT, interupt_command)

    # setup env variables for better readability of outputs
    os.environ['LINES'] = '25'
    os.environ['COLUMNS'] = '120'
    
    # get argument parametes
    (player, provider, show, episode, account, download, msg) = argument_parser()

    # retrieve the trackma list on run
    retrieve = True
    
    if not show == "" and not episode == 0:
        # watching just a specific show and episode only
         watch(show, str(episode), download, provider, player)
    elif not show == "":
        # choose want to do with a specific show
        specific_show_loop(show, msg, download, provider, player)
    else:
        # main loop that connets with your list with trackma
        main_loop(retrieve, account, msg, download,provider,player)
    exit_adl()

# run only if runned directly
if __name__ == "__main__" :
    main()

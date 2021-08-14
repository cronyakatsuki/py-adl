import os,sys
#just a quick script to print the fzf.txt file content

dn = os.path.dirname(os.path.realpath(__file__))
fzf_file = open(dn + "/fzf.txt").read()
fzf_file = fzf_file.replace("[0;34m", "")
fzf_file = fzf_file.replace('[0m', '')

print(fzf_file)
sys.exit()
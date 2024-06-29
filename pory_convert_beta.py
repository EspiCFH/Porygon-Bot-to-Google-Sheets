import os
import sys
import re

path = os.getcwd()

# Retrieving Data from files

# format
fmlist = []
f_file = open(r'%s\format.txt' % path)
for line in f_file:
    try:
        fmap = line.replace('\t','[TAB]')
    except:
        fmap = line
    fmlist.append(fmap)
fmlist.pop(0)
f_file.close()
#print(fmlist)

# Get Porybot Data
print('Please paste the entire porybot message here')
print('(see example.png for what to paste)')
lines = []
while True:
    line = input()
    if line[:8] == 'History:':
        break
    lines.append(line)

pory_raw = '\n'.join(lines)
#print(pory_raw)

players = re.findall(r'.+(?=:\s?\n)',pory_raw)
print("\nWhich Player's Stats are you looking for?")
print(f'0 - {players[0]}')
print(f'1 - {players[1]}')
psearch = int(input(''))
print('')
if psearch == 0 or psearch == players[0]:
    player_var = 0
elif psearch == 1 or psearch == players[1]:
    player_var = 1
else:
    print('Invalid response')
    input('PRESS ENTER TO EXIT')
    exit()
# Parse Porybot Data
pattern = r'(?<='+players[player_var]+r':[\s\n]\n)[\s\S]+?(?=[\s\n]+?.+:)'
#print(pattern)
statlist = []
def getStats():
    global statlist, replay
    mondata = re.findall(pattern, pory_raw)[0].split('\n')
    #print(mondata)
    replay = re.findall(r'(?<=Replay:\s).+',pory_raw)[0]
    for ele in mondata:
        index = mondata.index(ele)+1
        mon = re.findall(r'^.+(?=\shas)',ele)[0]
        kill_list = re.findall(r'\d(?=.+kills)',ele)
        kills = str(int(kill_list[0])+int(kill_list[1]))
        deaths = re.findall(r'\d(?=\sdeaths)',ele)[0]
        statlist.append((mon,kills,deaths))

getStats()
# Output porybot data
format_elements = len(fmlist)
curr = 0
for line in fmlist:
    if 'Replay' in line:
        #print(fmlist[len(fmlist)-1].replace(r'RP',replay).replace('[TAB]','\t'))
        break
    outline = line.replace(f'Mon{curr+1}',statlist[curr][0]).replace(f'K{curr+1}',statlist[curr][1]).replace(f'D{curr+1}',statlist[curr][2])
    outline = outline.replace('\n','').replace('[TAB]','\t')
    print(outline)
    curr += 1
print('')
input('PRESS ENTER TO EXIT')

import os
import sys
import re
import csv, json

path = os.getcwd()

# Retrieving Data from files

# format
fmlist = []
f_file = open(r'%s\format.txt' % path)
for line in f_file:
    fmlist.append(line)
fmlist.pop(0)
f_file.close()
# config
with open('config.json') as confile:
            confjson = json.load(confile)
            PADLmode = confjson['PADL Mode']
            replaymode = confjson['Replays']

# dictionary
dictionary = open('_PADLDictionary.json','r+')
dictionary_json = json.load(dictionary)
dictionary.close()
def convert_PADL(mon):
    return dictionary_json[mon.lower()]

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
outfile = open('Output.txt','w')
outfile.write('# If the formatting looks weird I promise it will paste correctly\n')
outfile.write("# I tried to fix it but it's just tweaking\n")
outfile.write('# If there are any problems pasting contact me on GitHub or Discord (EspiCFH)\n\n')
for player in players:
    pattern = r'(?<='+player+r':[\s\n]\n)[\s\S]+?(?=[\s\n]+?.+:)'
    # Parse Porybot Data
    statlist = []
    
    mondata = re.findall(pattern, pory_raw)[0].split('\n')
    replay = re.findall(r'(?<=Replay:\s).+',pory_raw)[0]
    for ele in mondata:
        index = mondata.index(ele)+1
        mon = re.findall(r'^.+(?=\shas)',ele)[0]
        if PADLmode == 'on':
            mon = convert_PADL(mon)
        else:
            pass
        
        kill_list = re.findall(r'\d(?=.+kills)',ele)
        kills = str(int(kill_list[0])+int(kill_list[1]))
        deaths = re.findall(r'\d(?=\sdeaths)',ele)[0]
        statlist.append((mon,kills,deaths))

    #output Porybot Data
    curr = 0
    with open('Output.txt','a',newline='') as outfile:
        for line in fmlist:
            if 'Replay' in line:
                if replaymode != 'on':
                    break
                else:
                    outfile.write(line.replace('RP',replay))
                    break
            outline = line.replace(f'Mon{curr+1}',statlist[curr][0]).replace(f'K{curr+1}',statlist[curr][1]).replace(f'D{curr+1}',statlist[curr][2]).replace('\n','')
            #print(repr(outline))
            outfile.write(outline+'\n')
            curr += 1
        if player == players[0]:
            outfile.write('\n')
    statlist.clear()

print('Data successfully written.')
print('Check Output.txt for the result')
print('=-=-=-=-=')
input('PRESS ENTER TO EXIT')


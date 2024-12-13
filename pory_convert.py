import json
import re

#formatting and config
with open('format.txt','r') as formatfile:
    outformat = formatfile.readlines()
    outformat.pop(0)
    print(outformat)
#config
with open('config.json','r') as config:
    readjson = json.load(config)
    padlmode = readjson['PADL Mode'].lower()

# dictionary
dictionary = open('_PADLDictionary.json','r+')
dictionary_json = json.load(dictionary)
dictionary.close()
def convert_PADL(mon):
    return dictionary_json[mon.lower().replace(' ','-')]

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
players = re.findall(r'.+(?=:\s?\n)',pory_raw)

outfile = open('Output.txt','w')
outfile.write('# If the formatting looks weird I promise it will paste correctly\n')
outfile.write("# I tried to fix it but it's just tweaking\n")
outfile.write('# If there are any problems pasting contact me on GitHub or Discord (EspiCFH)\n')

for player in players:
    pattern = r'(?<='+player+r':[\s\n]\n)[\s\S]+?(?=[\s\n]+?.+:)'
    # Parse Porybot Data
    statlist = []

    data = re.findall(pattern,pory_raw)[0].split('\n')
    RP = re.findall(r'(?<=Replay:\s).+',pory_raw)[0]
    for ele in data:
        #Mon Name
        globals()[f'Mon{data.index(ele)+1}'] = re.findall(r'^.+(?=\shas)',ele)[0]     
        if padlmode == 'on':
            globals()[f'Mon{data.index(ele)+1}'] = convert_PADL(globals()[f'Mon{data.index(ele)+1}'])
        #Kills
        kill_list = re.findall(r'\d(?=.+kills)',ele)
        globals()[f'K{data.index(ele)+1}'] = str(int(kill_list[0])+int(kill_list[1]))
        #Deaths
        globals()[f'D{data.index(ele)+1}'] = re.findall(r'\d(?=\sdeaths)',ele)[0]
        kill_list.clear()
    #for i in range (1,7):
        #print(globals()[f'Mon{i}'],globals()[f'K{i}'],globals()[f'D{i}'])

    #Write Data
    appendage = []
    with open('Output.txt','a') as outfile:
        outfile.write('\n')
        try:
            for line in outformat:
                appendage.clear()
                variables = re.findall(r'[^\t\n]+',line)
                for v in variables:
                    try:
                        variables[variables.index(v)] = globals()[f'{v}']
                    except:
                        variables[variables.index(v)] = v
                subbed = re.sub(r'([^\t\n]+)',r'{}',line)
                out = subbed.format(*variables)
                outfile.write(out)
                print(repr(out))
                if outformat.index(line) == 5:
                    outfile.write('\n')
        except:
            input('An unexpected error occured.\nPlease DM EspiCFH for clarification')

input('Data successfully written\nPRESS ENTER TO EXIT')

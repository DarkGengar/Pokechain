# DarkGengar (C) 2018
# Date 05/06/18
# License GPL

# TODO: Refactor Code:
#           - split code in functions
#           - add argument handler

def charmap_interpreter(charmap, reverse):
    alphabetTable = []
    hexTable = []
    for i in range(len(charmap)):
        #if line begin with '//' then ignore the line
        if charmap[i].startswith('//'):
            continue
        #remove newline and split string into two pieces between '='
        string = charmap[i].strip('\n').strip('\r').split('=', 1)
        #create alphabet and hex table for string encoding
        for j in range(len(string)):
            #if index 0 then add the string to alphabetTable 
            if j < 1:
                alphabetTable.append(string[j])
            #if index 1 then add the string to hexTable
            else:
                hexTable.append(string[j])
    return charmap2dict(alphabetTable, hexTable, reverse)
    
# create charmap as dictionary
def charmap2dict(alphabetTable, hexTable, reverse):
    dictCharmap = {}
    if(reverse):
        for i in range(len(hexTable)):
            dictCharmap[int(hexTable[i],0)] = alphabetTable[i]
    else:
        for i in range(len(alphabetTable)):
            dictCharmap[alphabetTable[i]] = hex(int(hexTable[i],0))
    return dictCharmap
    
entries = 412

# open charmap
with open("pk_gen_III_ger_charmap.chmp", 'r') as infile:
    # create list of chars
    line = list(infile)
# get charmap as dictionary
dictCharmap = charmap_interpreter(line, True)

with open("bprd.gba", 'rb') as infile:
    infile.seek(0x245DB0)
    data = infile.read(11*entries)

strings = []
l_strings = []

for i in range(entries):
    string = ''
    byte_string = data[11*i:(11*i)+11]
    for j in range(len(byte_string)):
        if(byte_string[j] == 255):
            break;
        string += dictCharmap[byte_string[j]]
    strings.append(string)

for i in range(len(strings)):
    string = strings[i].lower().capitalize()
    l_strings.append(string)
    
print(l_strings)
with open("poke_name_list.str", 'w') as outfile:
    outfile.write("$tbl str_poke_name_list = {\n\t\"")
    for i in range(len(l_strings)):
        if(i == len(l_strings)-1):
             outfile.write("\n\t\t" + l_strings[i] + "\n\t\"\n}")
        else:
            outfile.write("\n\t\t" + l_strings[i] + "\n\n\t\t[+]\n")
            


input = 'kteb (hadchi) "Wesh, al3alam lbidawi, wes dima koukab" ;' 

inputAsList = input.split(" ")


printingQ = []
printingStage = False

for word in inputAsList:
    printingQ.append(word)
    if word == 'kteb':
        printingStage = True
        continue
    if word == '(hadchi)':
        if printingStage:
            printingStageQ = []
            continue
    if (word[0] == "'" or word[0] == '"') and printingStage:
        printingStageQ.append(word[1:])
        continue
    elif  (word[-1] == '"' or (word[-1]) == "'" ) and printingStage:
        printingStageQ.append(word[:len(word) - 1])
        printingStage = False
        #print(word[:len(word) - 1])
        continue
    if printingStage:
        printingStageQ.append(word)
    if word == ";":
        if len(printingStageQ) != 0:
            hadchi = " ".join(printingStageQ)
            print(hadchi)
    



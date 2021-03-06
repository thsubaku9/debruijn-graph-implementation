import generateDNA as data

read2int = dict()

def checkOverlap(preStr,postStr):
    _max = 0
    for k in range(1,len(preStr)+1,1):        
        overlap = 0
        r1 = ""
        r2 = ""
        while((overlap < len(postStr)) and (overlap < k) and (postStr[overlap] == preStr[len(preStr) - 1 - (k-1) + overlap])):
            r1+=preStr[len(postStr) - 1 + overlap - k]
            r2+=postStr[overlap]
            overlap+=1            
        if(overlap>_max and overlap == k):            
            _max = overlap

    return _max

def FBFS(adjMat,startNode,vertices):
    forwardQueue = list()
    backwardQueue = list()
    forwardParent = [None] * vertices
    backwardParent = [None] * vertices
    forwardVisited = [False] * vertices
    backwardVisited = [False] * vertices
    FnetOverlapScore = [0] * vertices
    BnetOverlapScore = [0] * vertices
    
    forwardQueue.append(startNode);backwardQueue.append(startNode);
    maxScore = 0;location = None
    
    while(len(forwardQueue)> 0 or len(backwardQueue)>0):
        
        if(len(forwardQueue)>0):
            currentNode = forwardQueue[0]
            forwardQueue.remove(forwardQueue[0])
            if(forwardVisited[currentNode]):
                continue
            forwardVisited[currentNode] = True
            for j in range(0,vertices):
                if(adjMat[currentNode][j]>0):
                    if(FnetOverlapScore[j] < FnetOverlapScore[currentNode] + adjMat[currentNode][j] and (not forwardVisited[j])):
                        forwardParent[j] = currentNode
                        FnetOverlapScore[j] = FnetOverlapScore[currentNode] + adjMat[currentNode][j]
                        forwardQueue.append(j)
            
        if(len(backwardQueue)>0):
            currentNode = backwardQueue[0]
            backwardQueue.remove(backwardQueue[0])
            if(backwardVisited[currentNode]):
                continue
            backwardVisited[currentNode] = True
            for j in range(0,vertices):
                if(adjMat[j][currentNode]>0):
                    if(BnetOverlapScore[j] < BnetOverlapScore[currentNode] + adjMat[j][currentNode] and (not backwardVisited[j])):
                        #backwardParent[currentNode] = j
                        backwardParent[j] = currentNode #
                        BnetOverlapScore[j] = BnetOverlapScore[currentNode] + adjMat[j][currentNode]
                        backwardQueue.append(j)

    # find a node which maximizes bnetOverlap and fnetOverlap
    # run the node sequence for this node

    maxScore = 0; centralNode = None
    for i in range(0,vertices):
        if(i!=startNode):
            if(BnetOverlapScore[i] + FnetOverlapScore[i] > maxScore and BnetOverlapScore[i] > 0 and FnetOverlapScore[i] > 0):
                maxScore = BnetOverlapScore[i] + FnetOverlapScore[i]; centralNode = i


    nodeSequence = []
    if (centralNode == None):
        return (0,nodeSequence)
    
    j = centralNode
    retScore = 0
    
    while(j != None):        
        nodeSequence.append(j)
        j = forwardParent[j]

    nodeSequence.reverse()
    j = centralNode
        
    while(j != None):        
        nodeSequence.append(j)
        j = backwardParent[j]

    for i in range(1,len(nodeSequence)):
        retScore+=adjMat[nodeSequence[i-1]][nodeSequence[i]]
    return (retScore,nodeSequence)
        
            
    #at the common vertex meet, we need to check whether all the vertices have been visited effectively
    #here effectively => highest overlap cost
    #ultimately you'll end up with a node from where you should return forward+backwards search sequence

for i in range(0,len(data.genReads)):
    read2int[data.genReads[i]] = i

adjMat = list()

for i in range(0,data.totalReads):
    tmp = [0] * data.totalReads
    adjMat.append(tmp)


for i in range(0,data.totalReads):
    for j in range(0,data.totalReads):
        adjMat[i][j] = checkOverlap(data.genReads[i],data.genReads[j])
        if(adjMat[i][j] == data.readLen):
            adjMat[i][j] = 0

best_possible_result = []

for i in range(0,data.totalReads):
    res = FBFS(adjMat,i,len(adjMat))
    best_possible_result.append(res)
    
bestNode = None; bestScore = 0
for i in range(0,data.totalReads):
    if(best_possible_result[i][0] > bestScore):
        bestScore = best_possible_result[i][0]
        bestNode = i        

 

bestResult = best_possible_result[bestNode][1]

DNA = ""
DNA += data.genReads[bestResult[0]]
score = 0
for i in range(1,len(bestResult)):
    score+= adjMat[bestResult[i-1]][bestResult[i]]
    DNA += data.genReads[bestResult[i]][adjMat[bestResult[i-1]][bestResult[i]]:]

print("Score of {} and DNA:\n{}".format(score,DNA))

def ScoreMatrix(Query,Reference,match_score,mismatch_penalty,gap_penalty):
    matrix = [[0 for x in range(len(Query) + 1)] for y in range(len(Reference) + 1)]
    for i in range(1,len(Reference)+1):
        for j in range(1,len(Query)+1):
            if Reference[i-1]==Query[j-1]:
                diagonalScore=matrix[i-1][j-1]+match_score
            else:
                diagonalScore=matrix[i-1][j-1]+mismatch_penalty
            leftScore=matrix[i][j-1]+gap_penalty
            upScore=matrix[i-1][j]+gap_penalty
            matrix[i][j]=max(diagonalScore,leftScore,upScore,0)
    max_score = 0
    max_index = "None"
    for i in range(1, len(Reference) + 1):
        for j in range(1, len(Query) + 1):
            if matrix[i][j]>max_score:
                max_score=matrix[i][j]
                max_index=(i,j)

    return matrix,str(max_score),max_index

def trace_back(Query,Reference,matrix,max_index):
    aligned_query=''
    aligned_reference=''
    x,y=max_index
    move=next_move(matrix,x,y)
    while move!='end':
        if move=='diag':
            aligned_query=''.join((Query[y-1],aligned_query))
            aligned_reference=''.join((Reference[x-1],aligned_reference))
            x-=1
            y-=1
        elif move=='up':
            aligned_query = ''.join(('-', aligned_query))
            aligned_reference = ''.join((Reference[x - 1], aligned_reference))
            x-=1
        elif move=='left':
            aligned_query = ''.join((Query[y-1], aligned_query))
            aligned_reference = ''.join(('-', aligned_reference))
            y-=1
        move=next_move(matrix,x,y)
    aligned_query = ''.join((Query[y - 1], aligned_query))
    aligned_reference = ''.join((Reference[x - 1], aligned_reference))
    return aligned_query,aligned_reference

def next_move(score_matrix,x,y):
    diag=score_matrix[x-1][y-1]
    up=score_matrix[x-1][y]
    left=score_matrix[x][y-1]
    if diag >= up and diag >= left:
        return 'diag' if diag != 0 else 'end'
    elif up > diag and up >= left:
        return 'up' if up != 0 else 'end'
    elif left > diag and left > up:
        return 'left' if left != 0 else 'end'

def string_alignment(aligned_query,aligned_reference):
    identity,gaps,mismatches=0,0,0
    alignment_string=''
    for base1,base2 in zip(aligned_query,aligned_reference):
        if base1==base2:
            alignment_string=''.join((alignment_string,'|'))
            identity+=1
        elif '-' in (base1,base2):
            alignment_string = ''.join((alignment_string, '-'))
            gaps+=1
        else:
            alignment_string = ''.join((alignment_string, ':'))
            mismatches+=1

    return alignment_string,identity,gaps,mismatches

def DataInput(Query,Reference,NuclorAA,match_score,mismatch_penalty,gap_penalty):
    aaSet={'X','A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V'}
    nuclSet={'A','T','C','G','U'}
    Query=Query.lstrip().rstrip().upper()
    Reference=Reference.lstrip().rstrip().upper()
    if NuclorAA==1:
        for nucl in Query:
            if nucl not in nuclSet:
                return "Wrong Input!"
        for nucl in Reference:
            if nucl not in nuclSet:
                return "Wrong Input!"
    elif NuclorAA==2:
        for aa in Query:
            if aa not in aaSet:
                return "Wrong Input!"
        for aa in Reference:
            if aa not in aaSet:
                return "Wrong Input!"

    matrix,max_score,max_index=ScoreMatrix(Query,Reference,match_score,mismatch_penalty,gap_penalty)
    aligned_query,aligned_reference=trace_back(Query,Reference,matrix,max_index)
    alignment_string,identity,gaps,mismatches=string_alignment(aligned_query,aligned_reference)
    max_score = ' '.join(('alignment score:', str(max_score)))
    aligned_query = ' '.join(('aligned query:', aligned_query))
    aligned_reference = ' '.join(('aligned reference:', aligned_reference))
    alignment_stringV1 = ' '.join(('alignment string:', alignment_string))
    identityV1 = ' '.join(('alignment identity:', str(identity)))
    identityV2 = ''.join((str(round(identity / len(alignment_string) * 100, 2)), '%'))
    identityV1 = ' '.join((identityV1, identityV2))
    gapsV1 = ' '.join(('alignment gaps:', str(gaps)))
    gapsV2 = ''.join((str(round(gaps / len(alignment_string) * 100, 2)), '%'))
    gapsV1 = ' '.join((gapsV1, gapsV2))
    mismatchesV1 = ' '.join(('alignment mismatches:', str(mismatches)))
    mismatchesV2 = ''.join((str(round(mismatches / len(alignment_string) * 100, 2)), '%'))
    mismatchesV1 = ' '.join((mismatchesV1, mismatchesV2))
    return (max_score, aligned_query, aligned_reference, alignment_stringV1, identityV1, gapsV1, mismatchesV1)


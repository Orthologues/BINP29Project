def Processing(QueryPath,ReferencePath):
    QueryList = []
    ReferenceList = []
    with open(QueryPath,"r") as query:
        NuclSeq1 = ''
        query.readline()
        for line in query:
            if line.startswith('>'):
                QueryList.append(NuclSeq1)
                NuclSeq1=''
            else:
                NuclSeq1 = ''.join((NuclSeq1, line.rstrip()))
        QueryList.append(NuclSeq1)

    with open(ReferencePath,"r") as Reference:
        Reference.readline()
        NuclSeq2 = ''
        for line in Reference:
            if line.startswith('>'):
                ReferenceList.append(NuclSeq2)
                NuclSeq2=''
            else:
                NuclSeq2 = ''.join((NuclSeq2, line.rstrip()))
        ReferenceList.append(NuclSeq2)
    if len(ReferenceList)==len(QueryList):
        return (QueryList,ReferenceList)
    else:
        return 'These two files are not paired!'

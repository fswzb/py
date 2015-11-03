#-*- coding: UTF-8 -*-
from lxml import etree
import  os
xml_file_name = os.path.join(os.getcwd(), "maServer.xml")
doc = etree.parse(xml_file_name)
root = doc.getroot()

qindegree = {}
qoutdegree = {}
mqset = set()
mqlist = []
matrix = []

def checkServiceId():
    print "checkServiceId"
    idset = set()
    for s in root.getiterator('services'):
        for sr in s.getiterator("service"):
            sid = s.getparent().tag + ":" + sr.get("id")
            print "id", sid
            if sid in idset:
                print ("error!!! services name:", sr.get("name"), "id:", sid, "is duplicated")
                return
            else:
                idset.add(sid)

def checkQueueId():
    print "checkQueueId"
    idset = set()
    for s in root.getiterator('queues'):
        for sr in s.getiterator("mqset"):
            sid = s.getparent().tag + ":" + sr.get("id")
            print ("id", sid)
            if sid in idset:
                print ("error!!! mqset name:", sr.get("name"), "id:", sid, "is duplicated")
                return
            else:
                idset.add(sid)

def findAllMsgQueueDegree():
    for s in root.getiterator('services'):
        for sr in s.getiterator("service"):
            for sf in sr.getiterator("svcfunc"):
                if sf.get("inqueue") != "":
                    for q in sf.get("inqueue").split(','):
                        mqset.add(s.getparent().tag + ":" + str(int(q)))
                if sf.get("outqueue") != "":
                    for q in sf.get("outqueue").split(','):
                        mqset.add(s.getparent().tag + ":" + str(int(q)))

                if sf.get("inqueue") == "" or sf.get("outqueue") == "":
                    genReplaceNullStr(s, sr, sf)
                    mqset.add(genReplaceNullStr(s, sr, sf))

def genReplaceNullStr(s, sr, sf):
    return s.getparent().tag + ":" + sr.get("id") + "_" + sf.get("id")

def addIndegree(node):
    if node in qindegree:
        qindegree[node] += 1
    else:
        qindegree[node] = 1

def addOutdegree(node):
    if node in qoutdegree:
        qoutdegree[node] += 1
    else:
        qoutdegree[node] = 1

def getSrvAdj():
    mat = [["" for i in range(len(mqlist))] for j in range(len(mqlist))]
    for s in root.getiterator('services'):
        for sr in s.getiterator("service"):
            for sf in sr.getiterator("svcfunc"):
                inqueuelist=[]
                outqueuelist=[]
                if not (sf.get("inqueue") is None or sf.get("inqueue") == ""):
                    inqueuelist = sf.get("inqueue").split(',')
                if not (sf.get("outqueue") is None or sf.get("outqueue") == ""):
                    outqueuelist = sf.get("outqueue").split(',')
                sr_adj_value = s.getparent().tag + " srvid:" + sr.get("id") + "_" + "funcid:" + sf.get("id") + "_" + "clsid:" + sf.get("clsid")
                if len(inqueuelist) > 0 and len(outqueuelist) > 0:
                    for iq in inqueuelist:
                        for oq in outqueuelist:
                            iqindex = s.getparent().tag + ":" + str(int(iq))
                            oqindex = s.getparent().tag + ":" + str(int(oq))
                            mat[mqlist.index(iqindex)][mqlist.index(oqindex)] = sr_adj_value
                            addIndegree(oqindex)
                            addOutdegree(iqindex)

                if len(inqueuelist) > 0 and len(outqueuelist) == 0:
                    for iq in inqueuelist:
                        iqindex = s.getparent().tag + ":" + str(int(iq))
                        mat[mqlist.index(iqindex)][mqlist.index(genReplaceNullStr(s, sr, sf))] = sr_adj_value
                        addIndegree(genReplaceNullStr(s, sr, sf))
                        addOutdegree(iqindex)

                if len(inqueuelist) == 0 and len(outqueuelist) > 0:
                    for oq in outqueuelist:
                        oqindex = s.getparent().tag + ":" + str(int(oq))
                        mat[mqlist.index(genReplaceNullStr(s, sr, sf))][mqlist.index(oqindex)] = sr_adj_value
                        addIndegree(oqindex)
                        addOutdegree(genReplaceNullStr(s, sr, sf))
    return mat

def isEnd(node, visit):
    for i in range(len(mqlist)):
        if matrix[mqlist.index(node)][i] != "" and not visit[i]:
            return False
    return  True


def traceRoute():
    print "traceRoute"
    startpoints = mqset - set(qindegree)
    endpoints = mqset - set(qoutdegree)

    print "startpoints:", startpoints
    print "endpoints", endpoints
    for s in startpoints:
        for e in endpoints:
            visit = [False for i in range(len(mqlist))]
            path = []
            schAllPath(s, e, visit, path)

def schAllPath(v, t, visit, path):
    if visit[mqlist.index(v)]:
        return
    path.append(v)

    if v == t:
        print "begin<<", path, ">>end"
    else:
        visit[mqlist.index(v)] = True
        for i in range(len(mqlist)):
            if matrix[mqlist.index(v)][i] != "" and not visit[i]:
                path.append(matrix[mqlist.index(v)][i])
                schAllPath(mqlist[i], t, visit, path)
        visit[mqlist.index(v)] = False


checkServiceId()
checkQueueId()
#traceRoute()
findAllMsgQueueDegree()
mqlist = list(mqset)
# print mqset
#print mqlist
matrix = getSrvAdj()
#print matrix
traceRoute()



# print "qindegree"
# for (k,v) in qindegree.items():
#     print "k",k,"v", v
#
# print "qoutdegree"
# for (k,v) in qoutdegree.items():
#     print "k",k,"v", v
#
# print sr_adj
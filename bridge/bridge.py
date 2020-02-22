#!/usr/bin/env python

from bottle import route, request, template, static_file, run
from bridgedb import t, sitOut,  delTab, allTab, saveTab, \
    loadOld, loadTour, saveTour, finishTour, saveScore, calculate

HOST = 'flaska'
PORT = 2014

@route('/image/:picture')
def do_image(picture):
    return static_file(picture, root='image')

def parm(p, method="GET"):
    if method == "GET":
          r = request.query.get(p)
    else: r = request.forms.get(p)
    if r: r = r.encode('iso-8859-1').decode()
    return r

def parInt(p, method="GET"):
    if method == "GET":
          r = request.query.get(p)
    else: r = request.forms.get(p)
    try:
        r = int(r)
    except:
        r = 0
    return r

@route('/')
def entry():
    if t.round == -1 or t.round == t.nRnd:
        return suspend()
    else:
        return doSeat(t.round)

@route('/stat')
def stat():
    if t.round == -1 or t.round == t.nRnd:
        return suspend()
    else:
        p = [0]*11
        p[0] = t.id
        p[1] = t.nick
        p[2] = t.dpr
        p[3] = t.pairs
        p[4] = t.total
        p[5] = t.round
        p[6] = t.nRnd
        p[7] = t.nTab
        p[8] = t.sitOut
        p[9] = str(t.tabDone)
        p[10] = str(t.tabOpen)
        return template("admin", names=t.names, par=p)


@route('/admin')
def admin():
    done = parm("done")
    open = parm("open")
    nas = parm("names")
    # try:
    nas = nas.replace("\r\n", "\n")
    nas = nas.split("\n");
    while nas[-1] == "": nas = nas[:-1]
    newnames = tuple(map(lambda x:x.strip() ,nas))
    if t.pairs != len(newnames):
        return template("msg", msg="Number of names cannot be changed")
    if done == "": t.tabDone.clear()
    else:
        t.tabDone = eval(done)
    if open == "": t.tabOpen.clear()
    else:
        t.tabOpen = eval(open)
    # except:
    #     return template("msg", msg="Bad input")
    t.names = newnames
    return doSeat(t.round)

@route('/init')
def init():
    return template("init")

@route('/suspend')
def suspend():
    lst = loadOld()
    if len(lst):
        return template("suspend", lst=lst)
    else:
        return init()


@route('/restart')
def restart():
    tour = parInt("tour")
    rnd = loadTour(tour)
    if rnd == t.nRnd:
        return result()                 # Final result
    else:
        return doSeat(rnd)

@route('/start')
def start():
    t.dpr = parInt("dpr")
    t.nick = parm("nick")
    nas = parm("names")
    t.names = tuple(nas.split(","))
    t.pairs = len(t.names)
    t.nTab = int(t.pairs / 2)
    t.nRnd = len(sitOut[t.nTab-2])
    t.total = t.nTab * t.nRnd * t.dpr
    t.round = 0
    t.sitOut = t.pairs % 2
    t.tabDone.clear()
    t.tabOpen.clear()
    t.id = saveTour()
    return doSeat(0)

@route('/seat')
def seat():
    rnd = parInt("round") - 1
    tab = parInt("tab") - 1
    if tab >= 0 :
        t.tabOpen.remove(tab)
    return doSeat(rnd)

def doSeat(rnd):
    if t.sitOut:
        so = "Bye :  " + t.names[sitOut[t.nTab-2][rnd]]
    else:
        so = ""
    if  t.nRnd == t.round:
        return result()
    elif rnd == t.round:
        n = rnd + 1
        if n == t.nRnd: n = t.round
    else: n = t.round
    tabs = allTab(rnd)
    return template("seat", round=rnd+1, tabs=tabs, sitout=so, next=n+1)

@route('/score')
def score():
    tab = parInt("tab") - 1
    rnd = parInt("round") - 1
    if tab in t.tabOpen :
        return template("msg", msg="Table in use")
    if rnd == t.round and tab in t.tabDone :
        return template("msg", msg="Table already done")
    if rnd != t.round and not tab in t.tabDone :
        return template("msg", msg="Table not finished previous round")
    tup = saveTab(rnd, tab)
    t.tabOpen.add(tab)
    return template("score", round=rnd+1, tab=tab+1, tup=tup, all=False)

@route('/save')
def save():
    rnd = parInt("round") - 1
    tab = parInt("tab") - 1
    brd = parm("deal")
    if not tab in t.tabOpen or rnd != t.round:
        return template("msg", msg="System msg")
    scr = (rnd, tab, brd, parm("c" + brd), parInt("s" + brd))
    res = saveScore(scr)
    return template("partial", round=rnd+1, tab=tab+1, lst=res)

@route('/goon')
def goon():
    rnd = parInt("round") - 1
    tab = parInt("tab") - 1
    tup = saveTab(rnd, tab)     # ("NS", "EW", ((1, contr, score), ...(3.)))
    all = True
    for i in tup[2]:
        all = all and len(i) > 1
    return template("score", round=rnd+1, tab=tab+1, tup=tup, all=all)

@route('/done')
def done():
    tab = parInt("tab") - 1
    t.tabOpen.remove(tab)
    t.tabDone.add(tab)
    if len(t.tabDone) == t.nTab:
        t.tabDone.clear()
        t.round += 1
        if t.round == t.nRnd:
            finishTour()
            return result()
    return doSeat(t.round)

@route('/erase')
def erase():
    rnd = parInt("round") - 1
    tab = parInt("tab") - 1
    t.tabDone.discard(tab)
    try:
        t.tabOpen.remove(tab)
    except:
        return template("msg", msg="Bad remove")
    delTab(rnd, tab)
    return doSeat(t.round)


@route('/result')
def result():
    rnd = t.round
    if rnd < 2:
        return template("msg", msg="Ranking is nonsense right now")
    pair = parm("pair")
    deal = parInt("deal")
    if deal and t.round < t.nRnd:
        return template("msg", msg="Available only after the tournament is finished")
    ls = calculate(t.round, pair, deal)
    if deal:
        return template("deal", lst=ls, pair=pair)
    elif pair:
        return template("privat", lst=ls, pair=pair)
    else:
        if t.round == t.nRnd :
            msg = "Final result"
        else : msg = "Ranking after " + str(t.round) + " round"
        return template("final", lst=ls, title=msg)


from gevent import monkey
monkey.patch_all()

run(port=PORT, host=HOST, server="gevent")
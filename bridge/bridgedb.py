#!/usr/bin/env python

from sqlalchemy import create_engine, Column, String, Integer, Boolean, func
import time

db_host = 'localhost'
db_dbname = 'lkldb'
db_user = 'lkluser'
db_password = 'kiskacsa'

db_connect_string = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (db_user, db_password, db_host, db_dbname)
engine = create_engine(db_connect_string, pool_recycle=60)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

MAXTAB = 6
THEDAY = 0      # (js.getDay() + 6) % 7

sitOut = ((3, 1, 2),               # 2 tables never bye 0
        (2, 3, 4, 5, 1),	       # 3 tables never bye 0 6
        (7, 1, 2, 3, 4, 5, 6),     # 4 tables never bye 0
        (8, 1, 2, 3, 4, 5, 6, 7),  # 5 tables never bye 0 9
        (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 1), # 6 tables 0
        );
# rounds = (5, 7, 8, 11);	# = len(sitOut[nTab-2]) or NWd(i).length / nTab
NWd = (
((0, 1, 1), (2, 3, 1), (0, 2, 2), (3, 1, 2), (0, 3, 3), (1, 2, 3)),
((0, 1, 1), (3, 4, 2), (5, 2, 4), (0, 2, 2), (4, 5, 3), (1, 3, 4), (2, 4, 1),
 (5, 1, 2), (0, 3, 3), (3, 5, 1), (1, 2, 3), (0, 4, 4), (0, 5, 5), (2, 3, 5), (4, 1, 5)),
((0, 1, 1), (4, 2, 3), (6, 5, 2), (7, 3, 5), (0, 2, 2), (1, 4, 6), (5, 3, 4), (7, 6, 3),
 (0, 3, 3), (1, 7, 4), (2, 5, 7), (6, 4, 5), (0, 4, 4), (2, 1, 5), (3, 6, 1), (7, 5, 6),
 (0, 5, 5), (1, 6, 7), (3, 2, 6), (4, 7, 2), (0, 6, 6), (2, 7, 1), (4, 3, 7), (5, 1, 3)),
((0, 1, 1), (2, 3, 4), (4, 7, 2), (6, 8, 5), (9, 5, 1), (0, 2, 2), (9, 6, 2), (3, 4, 5),
 (5, 8, 3), (7, 1, 6), (0, 3, 3), (9, 7, 3), (4, 5, 6), (6, 1, 4), (8, 2, 7), (0, 4, 4),
 (9, 8, 4), (1, 3, 8), (5, 6, 7), (7, 2, 5), (0, 5, 5), (9, 1, 5), (2, 4, 1), (6, 7, 8),
 (8, 3, 6), (0, 6, 6), (9, 2, 6), (1, 4, 7), (3, 5, 2), (7, 8, 1), (0, 7, 7), (9, 3, 7),
 (2, 5, 8), (4, 6, 3), (8, 1, 2), (0, 8, 8), (9, 4, 8), (1, 2, 3), (3, 6, 1), (5, 7, 4)),
((0, 1, 1), (3, 2, 8), (7, 4, 11), (8, 10, 9), (9, 5, 7), (11, 6, 3), (0, 2, 2), (1, 7, 4),
 (4, 3, 9), (8, 5, 1), (9, 11, 10), (10, 6, 8), (0, 3, 3), (2, 8, 5), (5, 4, 10), (9, 6, 2),
 (10, 1, 11), (11, 7, 9), (0, 4, 4), (1, 8, 10), (3, 9, 6), (6, 5, 11), (10, 7, 3), (11, 2, 1),
 (0, 5, 5), (1, 3, 2), (2, 9, 11), (4, 10, 7), (7, 6, 1), (11, 8, 4), (0, 6, 6), (1, 9, 5),
 (2, 4, 3), (3, 10, 1), (5, 11, 8), (8, 7, 2), (0, 7, 7), (2, 10, 6), (3, 5, 4), (4, 11, 2),
 (6, 1, 9), (9, 8, 3), (0, 8, 8), (3, 11, 7), (4, 6, 5), (5, 1, 3), (7, 2, 10), (10, 9, 4),
 (0, 9, 9), (4, 1, 8), (5, 7, 6), (6, 2, 4), (8, 3, 11), (11, 10, 5), (0, 10, 10), (1, 11, 6),
 (5, 2, 9), (6, 8, 7), (7, 3, 5), (9, 4, 1), (0, 11, 11), (2, 1, 7), (6, 3, 10), (7, 9, 8),
 (8, 4, 6), (10, 5, 2))
);

class Tournament:
  def __init__(self):
    self.id = 0
    self.names = ()
    self.nick = ""
    self.dpr = 0
    self.pairs = 0
    self.total = 0
    self.round = -1
    self.nRnd = 0
    self.nTab = 0
    self.sitOut = False
    self.tabDone = {1,2,3}
    self.tabOpen = {1,2,3}

t = Tournament()

def imp(sc):
    d = (10, 40, 80, 120, 160, 210, 260, 310, 360, 420, 490, 590, 740, 890,
           1090, 1290, 1490, 1740, 1990, 2240, 2490, 2990, 3490, 3990, 99999)
    im = -1
    if sc < 0 : sc *= im
    else      : im = 1
    return im * len(tuple(filter(lambda i:i<sc, d)))


class Btour(Base):
    __tablename__ = 'Btour'
    id    = Column(Integer, primary_key=True)
    nick = Column(String(48))
    day   = Column(Integer)
    names = Column(String(255))
    dpr   = Column(Integer)
    total = Column(Integer)
    round = Column(Integer)

class Bscore(Base):
    __tablename__ = 'Bscore'
    tid   = Column(Integer, primary_key=True)         # 0 = Monday
    round = Column(Integer, primary_key=True)
    table = Column(Integer, primary_key=True)
    deal  = Column(Integer, primary_key=True)
    contr = Column(String(16))
    score = Column(Integer)

def oneTab(round, tab):
    # returns ("NS", "EW", (1, 2, ...))
    nwd = NWd[t.nTab-2][round*t.nTab + tab]
    so = sitOut[t.nTab-2][round]
    if t.sitOut and so in nwd[:2]:
        last = t.pairs - 1
        if nwd[1] == so:
            nwd = (nwd[0], last, nwd[2])
        else:
            nwd = (last, nwd[1], nwd[2])
    d = tuple(range(t.dpr*nwd[2] + 1))[-t.dpr:]
    return (t.names[nwd[0]], t.names[nwd[1]], d)

def allTab(round):
    # returns ((t, "NS", "EW", (1, 2, 3)), ...)
    r = ()
    for i in range(t.nTab):
        r += ((i+1,) + oneTab(round, i),)
    return r

def delTab(rnd, tab):
    session = Session()
    session.query(Bscore).filter(Bscore.tid == t.id, Bscore.round == rnd,
                  Bscore.table == tab).delete(synchronize_session=False)
    session.commit()

def saveTab(rnd, tab):
    # returns ("NS", "EW", ((1, contr, score), ...(3.)))
    nwd = oneTab(rnd, tab)
    bigd = ()
    session = Session()
    for d in nwd[2]:
        small = (d,)
        q = session.query(Bscore).filter(Bscore.tid == t.id, Bscore.round == rnd,
                                         Bscore.table == tab, Bscore.deal == d).all()
        if q:
            small += (q[0].contr, q[0].score)
        bigd += ((small),)
    return (nwd[0], nwd[1], bigd)

def saveTour():
    session = Session()
    rec = Btour(
        nick  = t.nick,
        day   = int(time.time()),
        names = str(t.names),
        dpr   = t.dpr,
        total = t.total,
        round = t.round)
    session.add(rec)
    session.commit()
    session.refresh(rec)
    session.close()
    return rec.id

def loadTour(id):
    session = Session()
    tour = session.query(Btour).filter_by(id = id).one()
    rnd = session.query(Bscore.round).filter_by(tid = id).order_by(Bscore.round.desc()).first()
    if rnd: rnd = rnd[0]
    else :  rnd = 0
    q = session.query(Bscore.table, func.count(Bscore.deal)).filter(Bscore.tid == id,
                      Bscore.round == rnd).group_by(Bscore.table).all()
    session.close()
    t.id = tour.id
    t.nick = tour.nick
    t.names = eval(tour.names)
    t.dpr = tour.dpr
    t.total = tour.total
    t.pairs = len(t.names)
    t.round = rnd
    t.nTab = int(t.pairs / 2)
    t.nRnd = len(sitOut[t.nTab-2])
    t.sitOut = t.pairs % 2
    t.tabDone.clear()
    t.tabOpen.clear()
    for tab in q:
        if tab[1] == t.dpr:
            t.tabDone.add(tab[0])
    if len(t.tabDone) == t.nTab:
        t.tabDone.clear()
        t.round += 1
        rnd = t.round
    return rnd

def finishTour():
    session = Session()
    session.query(Btour).filter_by(id = t.id).update({"round":t.round})
    session.commit()
    session.close()

def loadOld():
    session = Session()
    q = session.query(Btour).order_by(Btour.day).all()
    ls = ()
    for r in q:
        if r.round > 0:
            st = "Finished " + str(r.round) + " round"
        else:
            c = session.query(Bscore.tid).filter_by(tid=r.id).all()
            st = str(len(c)) + " of " + str(r.total) + " played"
        session.close()
        ls += ((r.id, time.strftime("%a, %b %d %H:%M",time.localtime(r.day)), st, r.nick),)
    return ls

def saveScore(rin):
    # input: (rnd, tab, deal, contr, scr)
    # output (deal, ((pair, pair, contr, scr, imp), ...), avgIMP)
    session = Session()
    session.add(Bscore(
        tid   = t.id,
        round = rin[0],
        table = rin[1],
        deal  = rin[2],
        contr = rin[3],              #.replace("+", "\\\\+"),
        score = rin[4]    ))
    session.commit()
    q = session.query(Bscore).filter(Bscore.tid == t.id,
            Bscore.deal == rin[2]).order_by(Bscore.score).all()
    brd = ()
    sum = 0
    for r in q:
        nam = oneTab(r.round, r.table)
        im = imp(rin[4] - r.score)
        sum += im
        brd += ((nam[0], nam[1], r.contr, r.score, im),)
    n = len(brd) - 1
    if n > 0 : sum /= n
    res = (rin[2], brd, str(round(sum, 2)))
    session.close()
    return res

def calculate(nextr, pair, deal):
    session = Session()
    stat = ()
    for i in range(t.dpr * len(sitOut[t.nTab-2])):
        q = session.query(Bscore).filter(Bscore.tid == t.id, Bscore.round < nextr,
                Bscore.deal == i+1).order_by(Bscore.score).all()
        brd = ()
        for r in q:
            brd += ([i+1, r.round, r.table, r.contr, r.score, 0, 0],)
        i = 0
        fr = ()
        for r in q:                             # frequency
            if len(fr) == 0:
                fr += ([r.score, 1],)           # fr[0]
            elif r.score == fr[i][0]:
                fr[i][1] += 1
            else:
                fr += ([r.score, 1],)
                i += 1
        freq = {}
        mp = 0
        for f in fr:
            freq[f[0]] = f[1] + mp - 1
            mp += f[1] * 2
        for br in brd:
            if len(brd) > 1:
                  mp = freq[br[4]] / (len(brd)-1) / 2
            else: mp = 0.5
            br[6] = mp                              # MP
            for r in q:
                if r.score == br[4]: continue
                br[5] += imp(br[4] - r.score)       # IMP
        stat += brd
    for br in stat:
        tn = oneTab(br[1], br[2])
        br[1] = tn[0]
        br[2] = tn[1]
    # sitOut correction missing here
    if deal:                        # deal freqy
        fl = tuple(filter(lambda x: x[0]==deal, stat))
        for f in fl:
            f[6] = "{0:.2f}".format(f[6]*100,2)
        return fl
    elif pair:                      # private score
        fl = tuple(filter(lambda x: pair in x[1:3], stat))
        sum = 0
        for f in fl:
            if f[1] == pair:
                  sum += f[5]
            else: sum -= f[5]
            f[6] = "{0:.2f}".format(f[6]*100,2)
        return (sum, fl)
    else:                           # ranking
        result = {}
        for x in t.names : result[x] = [0, 0, 0]
        for br in stat:
            result[br[1]][0] += br[5]
            result[br[2]][0] -= br[5]
            result[br[1]][1] += br[6]
            result[br[1]][2] += 1
            result[br[2]][1] += 1 - br[6]
            result[br[2]][2] += 1
        ls = []
        for x in result:
            n = result[x][2]
            if n == 0 : result[x][2] = 1
            ls += [[result[x][0], x, n, "{0:.2f}".format(result[x][1]/result[x][2]*100,2)]]
        ls.sort(reverse=True)
        return ls

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # loadTour(2)
    # calculate(2, 0, 0)
else:
    t = Tournament()

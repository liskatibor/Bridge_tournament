<script>
var round = {{round}};
var table = {{tab}};
var tarn = "?tab=" + table + "&round=" + round

window.onbeforeunload = function(e) {
    cmCancel();
}

function disable(action) {
    var btns = document.getElementsByTagName("button");
    for (var i=0; i<btns.length; i++)
        btns[i].disabled = action;
}

function cmCancel() {
    disable(true);
    var n = [];
% for r in tup[2]:
  % if len(r) != 1:
    n.push({{r[0]}});
  % end
% end
    if (n.length == 0) {
        window.open("seat" + tarn, "_self");
        return;
    }
    if(confirm("Saved contract " + n + " will be discarded. Is it OK?"))
        window.open("erase" + tarn, "_self");
    disable(false);
}

function cmSave(brd) {
    disable(true);
    cmd = "save" + tarn + "&deal=" + brd;
    var i, val, contr = document.getElementById(brd);
    var NW, scr, made, bno;
    val = contr.value.replace("+", "%2B");
    bno = "Deal " + brd;
    NW = document.getElementById("d" + brd).value;
    try {
        scr = parseInt(document.getElementById("s" + brd).value);
        if (scr % 10 != 0 || scr == NaN) throw "stop";
        if (scr == 0)
            if (confirm(bno + " seems to be passed out. Is it OK?")) {
                 cmd += "&c" + brd + "=pass out&s" + brd + "=0";
                 window.open(cmd, "_self");
                 return;
           } else {
                disable(false);
                return;
           }
    }
    catch {
        alert(bno + " has a bad score value");
        disable(false);
        return;
    }
    made = 0 > val.indexOf("-");                   // contract made
    if (NW == "N" || NW == "S") {
        if (made && scr < 0 || !made && scr > 0) {
            alert(bno + " has bad score sign")
            disable(false);
            return;
        }
    } else {
        if (made && scr > 0 || !made && scr < 0) {
            alert(bno + " has bad score sign")
            disable(false);
            return;
        }
    }
    if (val) {
        cmd += '&c' + brd + '=' + NW + ' ' + val + '&s' + brd + '=' + scr;
    } else {
        alert(bno + " contract field is empty");
        disable(false);
        return;
    }
    window.open(cmd, "_self");
}
function cmDone() {
    disable(true);
    window.open("done" + tarn, "_self");
}
</script>
<span class="mid">Table {{tab}}. &nbsp; Round {{round}}.</span>
<p>
<table>
<tr><th>Seat</th><th colspan="3">Players</th></tr>
<tr><td>NS:</td><td colspan="3">{{tup[0]}}</td></tr>
<tr><td>EW:</td><td colspan="3">{{tup[1]}}</td></tr>
<tr><th>Deal</th><th>Contract</th><th>Score</th><th>Action</th></tr>
% for r in tup[2]:
    <tr><td align="center"> {{r[0]}}</td>
  % if len(r) == 1:
    <td><select id="d{{r[0]}}" size="1">
        <option value="N">N</option>
        <option value="S">S</option>
        <option value="E">E</option>
        <option value="W">W</option>
        </select> &nbsp;
         <input id="{{r[0]}}" type="text" size="8"/></td>
    <td><input id="s{{r[0]}}" type="text" size="2"/></td>
    <td><button onclick="cmSave({{r[0]}})">Save</button>
  % else:
    <td> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; {{r[1]}}</td><td>{{r[2]}}
  % end
    </td></tr>
% end
    <tr><td></td><td colspan="2">
<button class="greenbtn" onclick="cmCancel()">Cancel</button>
% if all:
    </td><td colspan="2">
<button class="greenbtn" onclick="cmDone()">Done</button>
% end
    </td></tr>
</table>
</p>

% rebase('layout.tpl')

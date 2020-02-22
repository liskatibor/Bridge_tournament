<script>
function disabl() {
    var btns = document.getElementsByTagName("button");
    for (var i=0; i<btns.length; i++) btns[i].disabled = true;
}
function send(p) {
    disabl();
    window.open(p , "_self");
}
function cmPair(n, p) {
    send("result?deal=" + n + "&pair=" + p);
}
</script>
<span class="mid">Private score for {{pair}}.</span>
<p>
<table>
<tr><td colspan="3"></td><td colspan="4">Scoring is according to North-South</td></tr>
<tr><th>Deal</th><th>North - South</th><th>East - West</th><th>Contract</th>
    <th>Score</th><th>IMP</th><th>MP %</th></tr>
% for r in lst[1]:
    <tr><td align="center"><button onclick="cmPair({{r[0]}},'{{pair}}')">{{r[0]}}</button></td>
    <td>{{r[1]}}</td><td>{{r[2]}}</td><td>{{r[3]}}</td>
    <td align="right">{{r[4]}}</td>
    <td align="right">{{r[5]}}</td>
    <td align="right">{{r[6]}}</td></tr>
% end
<tr><td></td><th colspan="4">Total IMP for &nbsp; {{pair}}</th><th>{{lst[0]}}</th></tr>
<tr><td colspan="7"><center>
<p class="red">Select deal number for details </p>
<button id="rnkbtn" class="greenbtn" onclick='send("result")'>Ranking</button>
&nbsp; &nbsp;
<button id="pribtn" class="greenbtn" onclick='send("/")'>Return</button>
</center></td></tr>
</table>
</p>

% rebase('layout.tpl')

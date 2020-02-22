<script>
var round = {{round}};
function disabl() {
    var btns = document.getElementsByTagName("button");
    for (var i=0; i<btns.length; i++) btns[i].disabled = true;
}
function send(p) {
    disabl();
    window.open(p , "_self");
}
function cmTab(n) {
    disabl();
    send("score?tab=" + n + "&round={{round}}");
}
</script>
<span class="mid">Seating Round {{round}}.</span>
<p>
<table>
<tr><th>Table</th><th>North - South</th><th>East - West</th><th>Deals to play</th></tr>
% for r in tabs:
    <tr><td><button onclick="cmTab({{r[0]}})">Table {{r[0]}}</button></td>
    <td>{{r[1]}}</td><td>{{r[2]}}</td><td>{{r[3]}}</td></tr>
% end
<tr><td colspan="4"><center><b>{{sitout}}</b>
<p class="red">Select table for scoring</p>
<button id="rnkbtn" class="greenbtn" onclick='send("result")'>Ranking</button>
&nbsp; &nbsp;
<button id="nxtbtn" class="greenbtn" onclick='send("seat?round=" + {{next}})'>Round {{next}}.</button>
</center></td></tr>
</table>
</p>

% rebase('layout.tpl')

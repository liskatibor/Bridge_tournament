﻿<script>
var tit = "{{title}}";
function disabl() {
    var btns = document.getElementsByTagName("button");
    for (var i=0; i<btns.length; i++) btns[i].disabled = true;
}
function cmPrivat(pr) {
    disabl();
    window.open('result?pair=' + pr, "_self");
}
function send() {
    disabl();
    var ret = "/";
    if (tit.length < 14) ret = "suspend"
    window.open(ret, "_self");
}
</script>
<span class="mid">{{title}}</span>
<p>
<table>
  <tr><th>Pair</th><th>Played</th><th>IMP</th><th>MP %</th></tr>
 % for r in lst:
    <tr><td><button onclick="cmPrivat('{{r[1]}}')">{{r[1]}}</button></td>
    <td align="center">{{r[2]}}</td><td align="right">{{r[0]}}
     &nbsp; </td><td align="right">{{r[3]}}</td></tr>
 % end
    <tr><td colspan="4" align="center">
    <p class="red">Select pair for private score</p>
    <button id="retbtn" class="greenbtn" onclick="send()">Return</button></td></tr>
</table>
</p>

% rebase('layout.tpl')

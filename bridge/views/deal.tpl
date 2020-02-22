<script>
function disabl() {
    document.getElementById("rnkbtn").disabled = true;
    document.getElementById("pribtn").disabled = true;
}
function send(p) {
    disabl();
    window.open(p , "_self");
}
</script>
<span class="mid">Scores details</span>
<p>
<table>
<tr><td colspan="3"></td><td colspan="4">Scoring is according to North-South</td></tr>
<tr><th>Deal</th><th>North - South</th><th>East - West</th><th>Contract</th>
    <th>Score</th><th>IMP</th><th>MP %</th></tr>
% for r in lst:
    <tr><td align="center">{{r[0]}}</td>
    <td>{{r[1]}}</td><td>{{r[2]}}</td><td>{{r[3]}}</td>
    <td align="right">{{r[4]}}</td>
    <td align="right">{{r[5]}}</td>
    <td align="right">{{r[6]}}</td></tr>
% end
<tr><td colspan="7"><center>
<button id="rnkbtn" class="greenbtn" onclick='send("result")'>Ranking</button>
&nbsp; &nbsp;
<button id="pribtn" class="greenbtn" onclick='send("result?pair={{pair}}")'>Return</button>
</center></td></tr>
</table>
</p>

% rebase('layout.tpl')

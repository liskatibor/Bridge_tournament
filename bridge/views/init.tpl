<style>
th {
	padding-left: 15px;
	text-align: left;
}
td {
	padding: 5px;
	text-align: center;
}
span {
	font-weight: bold;
}
div {
	border-style: solid;
	border-color: blue;
	width: 320px;
}
dir {
    margin-top: 30px;
    margin-left: 80px;
}
</style>
<script>
var pairs = 6;
var table = 3;
var bye   = 0;
var dpr   = 3;
var names = [];
var round = [3, 5, 7, 8, 11];

function setParm() {
	dpr = parseInt(document.getElementById('dpr').value);
	names = document.getElementById('nameIn').value;
	names = names.trim().replace(/\r\n/g,"\n").split("\n");
	pairs = names.length;
	table = parseInt(pairs / 2);
	bye = "No";
	if (pairs - table*2 > 0) bye = "One";
	if (table < 2 || table > 6) {
		alert("A párok száma 4 és 13 között legyen!");
		return;
	}
	var i, j;
	for (i=0; i<pairs; i++)
		for (j=i+1; j<pairs; j++)
			if (names[i] == names[j]) {
				alert(names[j] + " not unique")
				return
			}
	document.getElementById('pair').innerHTML = pairs;
	document.getElementById('table').innerHTML = table;
	document.getElementById('round').innerHTML = round[table-2];
	document.getElementById('bye').innerHTML = bye;
	document.getElementById('total').innerHTML = dpr*round[table-2];
}
function send() {
    setParm();
    nick = document.getElementById('nick').value;
    window.open("start?dpr=" + dpr + "&nick=" + nick + "&names=" + String(names), "_self");
}
</script>
<div>
<b class="mid"> &nbsp; Tournament <br> &nbsp; &nbsp; &nbsp; name
&nbsp; <input id="nick" type="text" size="24" />
 </b>
<table>
	<tr><th>Pairs</th><th>Deals per Tables</th></tr>
	<tr><td rowspan="2">
<textarea id="nameIn" cols="16" rows="14">
Kati - Juci
Kati - András
Márti - Jancsi
Márti - Péter
Éva - Laci
Éva - Ági
Anci - Gábor
Jocó - Attila
</textarea>
	</td><td><input id="dpr" type="text" size="2" value="2"/>
	</td></tr>
	<tr><td>

	<span id="pair">8</span> pairs
	<span id="table">4</span> tables<br>
	<span id="round">7</span> rounds.
	<span id="bye">No</span> sit out. <br>
	Each (non bye) pair plays all <span id="total">14</span> deals.
	<p><button class="greenbtn" onclick="setParm()" >Apply</button></p>
	<p><button class="greenbtn" onclick="send()" >Start</button></p>
</table>
</div>
<dir>
<button class="greenbtn" onclick='window.open("suspend", "_self")' >Cancel</button>
</dir>

% rebase('layout.tpl')

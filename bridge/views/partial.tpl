﻿<span class="mid">Partial results</span>
<p>
<table>
    <tr><td></td><th>Deal : {{lst[0]}}</th></tr>
    <tr><th>North - South</th><th>East - West</th><th>Contract</th><th>Score</th><th>IMP</th></tr>
    % for d in lst[1]:
        <tr><td>{{d[0]}}</td><td>{{d[1]}}</td><td>{{d[2]}}</td>
        <td aligm="right">{{d[3]}}</td><td aligm="center">{{d[4]}}</td></tr>
    % end
    <tr><td></td> <td colspan="3" aligm="right">Average IMP for North - South :</td>
    <th>{{lst[2]}}</th></tr>
    <tr><td></td> <td colspan="3">
<button class="greenbtn" onclick='window.open("goon?round={{round}}&tab={{tab}}", "_self")'>Go on</button>
    </td></tr>
</table>
</p>

% rebase('layout.tpl')

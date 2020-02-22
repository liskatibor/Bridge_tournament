﻿<span class="mid">Older Tournaments</span>
<p>
<table>
  <tr><th>Tournament</th><th>Date of start</th><th>Status</th><th>Action</th></tr>
 % for r in lst:
    <tr><td>{{r[3]}}</td><td>{{r[1]}} &nbsp;</td><td>{{r[2]}}</td>
    <td><button onclick='window.open("restart?tour={{r[0]}}", "_self")' disabled>
    % if r[2][:6] == "Finish":
        Show results
     % else:
        Continue
    % end
    </button></td></tr>
 % end
</table>
</p>
<button class="greenbtn" onclick='window.open("init", "_self")' disabled>New Tournament Setup</button>

% rebase('password.tpl')

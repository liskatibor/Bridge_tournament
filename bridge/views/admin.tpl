﻿<span class="mid">Admin page</span>
<form action="admin">
<table>
  <tr><th>Pairs</th><th>Other</th></tr>
  <tr><td>
<textarea name="names" cols="32" rows="14">
% for nam in names:
    {{nam}}
% end
</textarea>
  </td><td>
  id = {{par[0]}} <br>
  nick = {{par[1]}} <br>
  dpr = {{par[2]}}
  pairs = {{par[3]}} <br>
  total = {{par[4]}}
  round = {{par[5]}} <br>
  nRnd = {{par[6]}}
  nTab = {{par[7]}} <br>
  sitOut = {{par[8]}} <br>
  tabDone =
  <input name="done" type="text" value="{{par[9]}}" /> <br>
  tabOpen =
  <input name="open" type="text" value="{{par[10]}}" />
  </td></tr>
</table>
<button class="greenbtn" disabled>Save</button>
</form>
% rebase('password.tpl')

<script>
function disable(action) {
    var btns = document.getElementsByTagName("button");
    for (var i=0; i<btns.length; i++)
        btns[i].disabled = !action;
}
function cmAdmin() {
    var pw = Math.floor(Math.random() * 11)+1;
    var pr = prompt("Enter password", pw);
    disable(15 == (parseInt(pr) ^ parseInt(pw)));
}
</script>
{{!base}}
&nbsp; &nbsp;
<button class="greenbtn" onclick="cmAdmin()">Administrator</button>
% rebase("layout.tpl")

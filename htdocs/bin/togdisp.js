/*jslint browser:true*/
function toggle_visibility(tbid,lnkid)
{
 use "strict";
 if (document.getElementById(lnkid).value == "COLLAPSE")
 {
  document.getElementById(tbid).style.display = "none";
  document.getElementById(lnkid).value = "EXPAND";
  document.getElementById(lnkid).innerHTML = "EXPAND";
 }
 else
 {
  document.getElementById(tbid).style.display = "table";
  document.getElementById(lnkid).value = "COLLAPSE";
  document.getElementById(lnkid).innerHTML = "COLLAPSE";
 }
}

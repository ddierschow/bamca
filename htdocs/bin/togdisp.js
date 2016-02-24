/*jslint browser:true*/
function toggle_visibility(tbid, lnkid)
{
  "use strict";
  if (document.getElementById(lnkid).value === "collapse")
  {
    document.getElementById(tbid).style.display = "none";
    document.getElementById(lnkid).src = "../pic/gfx/but_expand.gif";
    document.getElementById(lnkid).onmouseover = "this.src='../pic/gfx/hov_expand.gif';";
    document.getElementById(lnkid).onmouseout = "this.src='../pic/gfx/but_expand.gif';";
    document.getElementById(lnkid).value = "expand";
  }
  else
  {
    document.getElementById(tbid).style.display = "table";
    document.getElementById(lnkid).src = "../pic/gfx/but_collapse.gif";
    document.getElementById(lnkid).onmouseover = "this.src='../pic/gfx/hov_collapse.gif';";
    document.getElementById(lnkid).onmouseout = "this.src='../pic/gfx/but_collapse.gif';";
    document.getElementById(lnkid).value = "collapse";
  }
}

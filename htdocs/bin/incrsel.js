
var tid = 0;
var speed = 200;
var fld = '';
var vec = 1;
var nmn = 0;
var nmx = 999;
function toggleOnSel(f,v){
    fld = f;
    vec = v;
  incrsel(fld,vec);
    speed = 300;
    if(tid==0){
        tid=window.setInterval("autoincrsel();",speed);
    }
}
function autoincrsel() {
  incrsel(fld,vec);
    if(speed>100){
	speed = speed - 20;
	toggleOff();
        tid=window.setInterval("autoincrsel();",speed);
    }
}
function toggleOnNum(f,v,mn,mx){
    fld = f;
    vec = v;
    nmn = mn;
    nmx = mx;
  incrnum(fld,vec,nmn,nmx);
    speed = 300;
    if(tid==0){
        tid=window.setInterval("autoincrnum();",speed);
    }
}
function autoincrnum() {
  incrnum(fld,vec,nmn,nmx);
    if(speed>100){
	speed = speed - 20;
	toggleOff();
        tid=window.setInterval("autoincrnum();",speed);
    }
}
function toggleOff(){
    if(tid!=0){
        window.clearInterval(tid);
        tid=0;
    }
}
function incrsel(f,v){
 var elem = document.getElementById(f);
 if (v > 0)
 {
  if (elem.selectedIndex < elem.length - 1)
   document.getElementById(f).selectedIndex = elem.selectedIndex + 1;
 }
 else
 {
  if (elem.selectedIndex > 0)
   document.getElementById(f).selectedIndex = elem.selectedIndex - 1;
 }
}

function settsel(f){
 var elem = document.getElementById(f);
 document.getElementById(f).selectedIndex = elem.length - 1;
}

function setbsel(f){
 document.getElementById(f).selectedIndex = 0;
}

function incrnum(f,v,mn,mx){
 var elem = document.getElementById(f);
 var nf = parseInt(document.getElementById(f).value, 10);
 if (v > 0)
 {
  if (nf < mx)
   document.getElementById(f).value = nf + 1;
 }
 else
 {
  if (nf > mn)
   document.getElementById(f).value = nf - 1;
 }
}

function settnum(f,v){
 document.getElementById(f).value = v;
}

var tid = 0;
var speed = 100;

function toggleOn(fn){
    if(tid==0){
        tid=setInterval(fn,speed);
    }
}
function toggleOff(){
    if(tid!=0){
        clearInterval(tid);
        tid=0;
    }
}


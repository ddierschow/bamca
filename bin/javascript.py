
def_reset_button_js = '''<script  language="Javascript">
function ResetForm(which){
 for (i=0;i<which.length;i++){
  var tempobj=which.elements[i];
  if (tempobj.type=="text"||tempobj.type=="textarea"||tempobj.type=="password"||tempobj.type=="file")
   tempobj.value=tempobj.defaultValue;
  else if (tempobj.type=="checkbox"||tempobj.type=="radio")
   tempobj.checked=tempobj.defaultChecked;
  else if (tempobj.type=="select-one")
   for (var j=0;j<tempobj.options.length;j++)
    if (tempobj.options[j].defaultSelected)
     tempobj.options[j].selected = true;
 }
 return false;
}
</script>
'''

def_increment_js = '''
<script  language="Javascript">
function incrfield(f,v){
 var id = document.getElementsByName(f)[0].value;
 var p = s= n= '';
 for (i=0; i < id.length; i = i + 1)
  if (id[i] >= '0' && id[i] <= '9')
   n = n + id[i];
  else if (n.length)
   s = s + id[i];
  else
   p = p + id[i];
 var nf = '00' + (parseInt(n, 10) + v);
 document.getElementsByName(f)[0].value = p + nf.substr(nf.length - n.length, n.length) + s;
}
</script>
'''

def_increment_select_js = '''
<script  language="Javascript">
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
</script>
'''

def_toggle_display_js = '''<script type="text/javascript">
function toggle_visibility(tbid,lnkid)
{
 if (document.getElementById(lnkid).value == "collapse")
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
</script>
'''

def_reset_button_js     = '''<script type="text/javascript" src="/bin/reset.js"></script>\n'''
def_increment_js        = '''<script type="text/javascript" src="/bin/increment.js"></script>\n'''
def_increment_select_js = '''<script type="text/javascript" src="/bin/incrsel.js"></script>\n'''
#def_toggle_display_js   = '''<script type="text/javascript" src="/bin/togdisp.js"></script>\n'''

def_google_analytics_js = '''
<script type="text/javascript">
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-24758340-2']);
_gaq.push(['_trackPageview']);
(function() {
 var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
 ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
 var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
</script>
'''

def_edit_js = '''
<script>
function getValueFromApplet()
{
  document.myForm.q.value = document.myApplet.getCoords();
  return true;
}
</script>
'''

def_edit_app = '''
<object name="myApplet" codetype="application/java" codebase="/java" classid="java:ImaWidget" width=%(width)s height=%(height)s>
<param name="file" value="%(file)s" valuetype="data"></object>
'''

def_edit_app = '''
<applet code="ImaWidget"
codebase="/java"
archive="ImaWidget.jar"
width=%(width)s height=%(height)s>
<param name="permissions" value="sandbox">
<param name="file" value="%(file)s" valuetype="data"></applet>
'''

def_edit_app = '''
<embed id="ImaWidget"
       name="myApplet"
       type="application/x-java-applet;version=1.6"
width="%(width)s" height="%(height)s"
       archive="/java/ImaWidget.jar"
       code="ImaWidget"
       pluginspage="http://java.com/download/"
permissions="sandbox"
file="%(file)s" />
'''

editformstart = '''
<form action="imawidget.cgi" name="myForm" onSubmit="return getValueFromApplet()">
'''

editformend = '''
  <input type="hidden" value="%(f)s" name="f">
  <input type="hidden" value="%(d)s" name="d">
  <input type="hidden" value="" name="q">
</form>
'''

def_map_link = '''
function maplink($arr)
{
    $st = $arr[0];
    unset($arr[0]);
    $to = '';
    $url = 'http://maps.google.com/maps?f=d&saddr=' . $st[0] . '&daddr=';
    $k = 1;
    $v = '';
    foreach ($arr as $d)
    {
        $url .= $to . $d[0];
        if (!$d[1])
        {
        }
        else if (!$v)
        {
            $v .= $k;
        }
        else
        {
            $v .= ',' . $k;
        }
        $k += 1;
        $to = '+to:';
    }
    $url .= '&hl=en&via=' . $v;
    return $url;
}
'''

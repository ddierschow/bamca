
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

def_reset_button_js = '''<script type="text/javascript" src="/bin/reset.js"></script>\n'''
def_increment_js = '''<script type="text/javascript" src="/bin/increment.js"></script>\n'''
def_increment_select_js = '''<script type="text/javascript" src="/bin/incrsel.js"></script>\n'''
#def_toggle_display_js = '''<script type="text/javascript" src="/bin/togdisp.js"></script>\n'''

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

def_edit_app = '''
<div style="display:none" id="ima_query">q</div>
<img id="ima_source" src="%(file)s" style="display:none">
<canvas id="ima_widget" width="%(width)s" height="%(height)s" style="border:0px;">
</canvas><br>
<script type="text/javascript" src="/bin/imawidget.js"></script>
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

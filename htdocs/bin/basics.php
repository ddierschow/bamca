<?php
include "db.php";

$pif = 0;

function CheckPerm($lev) {
    $retval = 0;
    if ($lev) {
	if (array_key_exists('id', $_COOKIE)) {
	    passthru('../bin/secure.py ' . $lev, $retval);
	}
    }
    else
	return 1;
    return $retval;
}

function NoAccess($pif, $access, $dest) {
    $retval = CheckPerm($access);
    if (!$retval) {
?> 

<script type="text/javascript">
<!--
window.location = "https://<?php echo $pif['host']; ?>/cgi-bin/login.cgi?dest=http://<?php echo $pif['host']; ?>/<?php echo $dest; ?>";
//document.write("dumpout!");
//-->
</script>

<?php
	exit();
    }
}

function CheckID() {
    $retval = 0;
    if (array_key_exists('id', $_COOKIE)) {
	passthru('../bin/secure.py id', $retval);
    }
    return $retval;
}

function DBConnect($pif) {
    $dbi = mysql_connect('localhost', $pif['dbuser'], $pif['dbpass']);
    if (!$dbi) {
	echo 'connect failed';
	return 0;
    }
    $r = mysql_select_db($pif['dbname'], $dbi);
    if (!$r) {
	echo 'select failed';
	return 0;
    }
    return $dbi;
}

function DBQuery($dbi, $query) {
    $ret = Array();
    $res = mysql_query($query, $dbi);
    #echo "<!-- query " . $query . " : ";
    #print_r($res);
    #echo "-->\n";
    if ($res && $res != 1) {
	while (1) {
	    $row = mysql_fetch_row($res);
	    if (!$row) {
		break;
	    }
	    $ret[] = $row;
	}
    }
    return $ret;
}

function DBClose($dbi) {
    if ($dbi)
	mysql_close($dbi);
}

function GetPageInfo($page_id) {
    global $pif;
    chdir(getenv('DOCUMENT_ROOT'));
    putenv('HTTP_COOKIE=' . apache_getenv('HTTP_COOKIE'));
    $pif = array();
    $pif['page_id'] = $page_id;
    $pif['styles'] = ['main', $page_id];
    $pif['hierarchy'] = array();
    $pif['host'] = getenv('SERVER_NAME');
    $pif['docroot'] = getenv('DOCUMENT_ROOT');
    $pif['cgibin'] = $pif['docroot'] . '/../cgi-bin';
    $pif['is_beta'] = 0;
    if (substr($pif['host'], 0, 5) == 'beta.')
	$pif['is_beta'] = 1;
    $cfg = BarFile($pif['cgibin'] . '/.config', 'bamca.org');
    foreach (array_slice($cfg[0], 1) as $c) {
	$nl = explode(',', trim($c));
	$pif[$nl[0]] = $nl[1];
    }
    $pif['dbi'] = $dbi = DBConnect($pif);
    if (!$dbi)
	return $pif;
    $q = "select page_info.format_type,page_info.title,page_info.pic_dir,page_info.tail,page_info.flags from page_info where page_info.id='" . $page_id . "'";
    $res = mysql_query($q, $dbi);
    if ($res) {
	while (1) {
	    $row = mysql_fetch_row($res);
	    if ($row) {
		$pif['format_type'] = $row[0];
		$pif['title'] = $row[1];
		$pif['pic_dir'] = $row[2];
		$pif['tail'] = $row[3];
		$pif['flags'] = $row[4];
		$pif['hide_title'] = $row[4] & 2;
	    }
	    else
		break;
	}
    }
    $bad_ip = DBQuery($dbi, "select count(*) from blacklist where reason='ip' and target='" . getenv('REMOTE_ADDR') . "'");
    $pif['bad_ip'] = $bad_ip[0][0];
    $pif['messages'] = '';
    return $pif;
}

function DoHead($pif) {
    echo "<head><meta charset=\"UTF-8\">
<title>" . $pif['title'] . "</title>
<meta http-equiv=\"content-type\" content=\"text/html; charset=ISO-8859-1\">
<script src=\"https://use.fontawesome.com/a21dc93072.js\"></script>
<link rel=\"icon\" href=\"http://www.bamca.org/pic/gfx/favicon.ico\" type=\"image/x-icon\" />
<link rel=\"shortcut icon\" href=\"http://www.bamca.org/pic/gfx/favicon.ico\" type=\"image/x-icon\" />
<link rel=\"stylesheet\" href=\"/styles/main.css\" type=\"text/css\">
<link rel=\"stylesheet\" href=\"/styles/fonts.css\" type=\"text/css\">
<link rel=\"stylesheet\" href=\"/styles/" . $pif['page_id'] . ".css\" type=\"text/css\">
";
}

function DoPageHeader($pif) {
    $IMG_DIR_ART = 'pic/gfx';
    if (!$pif['is_beta'])
	echo "<script type=\"text/javascript\">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-24758340-2']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
";
    echo "</head>\n\n<body>\n";
    $id = CheckID();
    echo '<table width="1024" class="body">' . "\n";
    if ($id > 0) {
	$username = Fetch('select name from buser.user where id=' . $id, $pif);
	$username = $username[0][0];
	echo '<tr><td class="loginbar">Welcome back, ' . $username . '! ('.$id.')';
	DoTextButtonLink('log_out', "https://" . $pif['host'] . "/cgi-bin/logout.cgi");
	DoTextButtonLink('change_password', "https://" . $pif['host'] . "/cgi-bin/chpass.cgi?dest=http://" . $pif['host'] . "/stuff.php");
	$retval = CheckPerm('u');
	if ($retval) {
	    DoTextButtonLink('upload', "http://" . $pif['host'] . "/cgi-bin/upload.cgi");
	}
	if (CheckPerm('a')) {
	    DoTextButtonLink('control_panel', "http://" . $pif['host'] . "/stuff.php");
	}
	echo "</td></tr>\n";
    }
    if ($pif['is_beta'])
	echo "<tr><td height=\"24\" class=\"beta\">&nbsp;</td></tr>\n";
    echo '<tr><td class="body">' . "\n";
    foreach ($pif['hierarchy'] as $hier) {
	echo '<a href="' . $hier[0] . '">' . $hier[1] . "</a> <i class=\"fa fa-chevron-right\"></i>\n";
    }
    if (!($pif['flags'] & 2))
	echo '<div class="title"><span class="titletext">' . $pif['title'] . "</span></div>\n";
}

function DoPageFooter($pif) {
    echo "</td></tr>\n";
    if ($pif['is_beta'])
	echo "<tr><td height=24 background=\"http://" . $pif['host'] . "/pic/gfx/beta.gif\">&nbsp;</td></tr>\n";
    echo "</table>\n";
}

//<tr><td class="bottombar2" colspan="2">
//<div class="bamcamark">
//<img src="/pic/gfx/bamca_sm.gif">
//</div>
//<div class="comment_box"><a href="../pages/comment.php?page=single&id=MB001&pic=&dir=&ref="><div onsubmit="this.disabled=true;" class="textbutton comment">COMMENT ON<BR>THIS PAGE</div></a>
//</div>
//</td></tr>

function DoFoot($pif) {
    echo "</body>\n";
    DBClose($pif['dbi']);
}

function DoTextButton($buttext, $classname="textbutton") {
    echo "<div class=\"$classname\">$buttext</div>";
}

function DoTextButtonLink($buttext, $linkloc, $classname="textbutton") {
    $buttext = strtoupper(str_replace('_', ' ', $buttext));
    echo "<a href=\"$linkloc\">";
    DoTextButton($buttext, $classname);
    echo "</a>\n";
}

function DoTextButtonReset($formid, $addl='') {
    echo '<div class="textbutton" onClick="ResetForm(document.' . $formid . ');' . $addl . '" alt="RESET" >RESET</div>';
}

function DoTextButtonSubmit($buttext, $submit) {
    echo "<input type=\"submit\" name=\"$submit\" value=\"$buttext\" class=\"textbutton\">\n";
}

function BarFile($fname, $prefix) {
    $sl = array();
    $sf = fopen($fname, "r");
    if (!$sf)
	return $sl;
    while (!feof($sf)) {
	$l = fgets($sf);
	if (!feof($sf)) {
	    $nl = explode('|', trim($l));
	    if ($nl[0] == $prefix)
		$sl[] = $nl;
	}
    }
    fclose($sf);
    return $sl;
}

function Fetch($query, $pif) {
    $ret = array();
    $dbi = $pif['dbi'];
    if (!$dbi)
	return $ret;
    $ret = DBQuery($dbi, $query);
    return $ret;
}

function DoShowHideJavascript($expand, $collapse) {
?>
<script type="text/javascript">
function toggle_visibility(tbid,lnkid)
{
 if (document.getElementById(lnkid).value == "<?php echo $collapse; ?>")
 {
  document.getElementById(tbid).style.display = "none";
  document.getElementById(lnkid).value = "<?php echo $expand; ?>";
  document.getElementById(lnkid).innerHTML = "<?php echo $expand; ?>";
 }
 else
 {
  document.getElementById(tbid).style.display = "table";
  document.getElementById(lnkid).value = "<?php echo $collapse; ?>";
  document.getElementById(lnkid).innerHTML = "<?php echo $collapse; ?>";
 }
}
</script>
<?php
}

function DoResetJavascript() {
    echo "<script  language=\"Javascript\">
function ResetForm(which){
 which.reset();
 return false;
}
</script>
";
}

function incrnum($id, $mn, $mx, $cl) {
    $but_max = '<div class="textbutton textupdown"><i class="fa fa-angle-double-up bold" title="TOP"></i></div>';
    $but_inc = '<div class="textbutton textupdown"><i class="fa fa-angle-up bold" title="UP"></i></div>';
    $but_dec = '<div class="textbutton textupdown"><i class="fa fa-angle-down bold" title="DOWN"></i></div>';
    $but_min = '<div class="textbutton textupdown"><i class="fa fa-angle-double-down bold" title="BOTTOM"></i></div>';
    echo "<a onclick=\"" . $cl . "settnum('" . $id . "'," . $mx . ");\">" . $but_max . "</a>\n";
    echo "<a onclick=\"" . $cl . "\" onmousedown=\"toggleOnNum('" . $id . "',1," . $mn . "," . $mx . ");\" onmouseup=\"toggleOff();\">" . $but_inc . "</a>\n";
    echo "<a onclick=\"" . $cl . "\" onmousedown=\"toggleOnNum('" . $id . "',-1," . $mn . "," . $mx . ");\" onmouseup=\"toggleOff();\">" . $but_dec . "</a>\n";
    echo "<a onclick=\"" . $cl . "settnum('" . $id . "'," . $mn . ");\">" . $but_min . "</a>\n";
}

function incrsel($id, $vl, $onchg="") {
    $but_max = '<div class="textbutton textupdown"><i class="fa fa-angle-double-up bold" title="TOP"></i></div>';
    $but_inc = '<div class="textbutton textupdown"><i class="fa fa-angle-up bold" title="UP"></i></div>';
    $but_dec = '<div class="textbutton textupdown"><i class="fa fa-angle-down bold" title="DOWN"></i></div>';
    $but_min = '<div class="textbutton textupdown"><i class="fa fa-angle-double-down bold" title="BOTTOM"></i></div>';
    if ($vl > 0) {
	echo "<a onclick=\"settsel('" . $id . "');" . $onchg ."\">" . $but_max . "</a>\n";
	echo "<a onmousedown=\"toggleOnSel('" . $id . "',1);" . $onchg ."\" onmouseup=\"toggleOff();" . $onchg . "\">" . $but_inc . "</a>\n";
	echo "<a onmousedown=\"toggleOnSel('" . $id . "',-1);" . $onchg ."\" onmouseup=\"toggleOff();" . $onchg . "\">" . $but_dec . "</a>\n";
	echo "<a onclick=\"setbsel('" . $id . "');" . $onchg ."\">" . $but_min . "</a>\n";
    }
    else {
	echo "<a onclick=\"setbsel('" . $id . "');" . $onchg . "\">" . $but_max . "</a>\n";
	echo "<a onmousedown=\"toggleOnSel('" . $id . "',-1);" . $onchg . "\" onmouseup=\"toggleOff();" . $onchg . "\">" . $but_inc . "</a>\n";
	echo "<a onmousedown=\"toggleOnSel('" . $id . "',1);" . $onchg . "\" onmouseup=\"toggleOff();" . $onchg . "\">" . $but_dec . "</a>\n";
	echo "<a onclick=\"settsel('" . $id . "');" . $onchg . "\">" . $but_min . "</a>\n";
    }
}

function DoIncDecJavascript() {
    echo '<script type="text/javascript" src="/bin/incrsel.js"></script>' . "\n";
}

function arr_get($array, $key, $default=null) {
    return isset($array[$key]) ? $array[$key] : $default;
}
function arr_get2($array, $key, $defaults, $default=null) {
    return isset($array[$key]) ? $array[$key] : (isset($defaults[$key]) ? $defaults[$key] : $default);
}

function Debug($something) {
    echo '<pre>'; print_r($something); echo '</pre>';
}

function LinksList($links, $star, $preface='', $post='', $prefix='') {
    global $IMG_DIR_ART;
    echo '   ';
    if ($preface)
	echo $preface . "\n";
    foreach ($links as $ent) {
	if ($ent['ty'] == 's')
	    echo $prefix . $star . '<a href="' . $ent['url'] . '">' . $ent['name'] . "</a>\n";
	else if ($ent['ty'] == 'l')
	    echo $prefix . '<a href="' . $ent['url'] . '">' . $ent['name'] . "</a>\n";
	else if ($ent['ty'] == 'b') 
	    $prefix . DoTextButtonLink($ent['name'], $ent['url']);
	else if ($ent['ty'] == 't') 
	    echo $ent['name'] . "\n";
	else
	    echo "<br>&nbsp;\n";
    }
    if ($post)
	echo $post . "\n";
}


function DoButtonComment($pif, $args='') {
    if ($args)
	$args = 'page_id=' . $pif['page_id'] . '&' . $args;
    else
	$args = 'page_id=' . $pif['page_id'];
    echo '<div class="comment_box">';
    DoTextButtonLink('comment on<br>this page', "/pages/comment.php?" . $args);
    echo "</div>\n";
}

?>

<?php
set_include_path(get_include_path() . PATH_SEPARATOR . $_SERVER['DOCUMENT_ROOT']);
set_include_path(get_include_path() . PATH_SEPARATOR . $_SERVER['DOCUMENT_ROOT'] . '/bin');
include "config.php";
include "db.php";

$pif = 0;

function CheckPerm($pif, $lev) {
    global $LOCKDOWN;
    $retval = !$LOCKDOWN && $lev == 'b';
    if (array_key_exists('id', $_COOKIE)) {
        if ($pif['privs']) {
            $retval = strpos($pif['privs'], $lev) != false;
        }
    }
    return $retval;
}

function NoAccess($pif, $access, $dest) {
    foreach(str_split($pif['privs']) as $c) {
        $retval = strpos($access, $c) != false;
        if ($retval)
            return;
    }
?> 

<script type="text/javascript">
<!--
window.location = "https://<?php echo $pif['host']; ?>/cgi-bin/login.cgi?dest=/<?php echo $dest; ?>";
-->
</script>

<?php
    exit();
}

function CheckID($pif) {
    global $LOCKDOWN;
    if ($LOCKDOWN)
        $pif['privs'] = '';
    else
        $pif['privs'] = 'b';
    $pif['user_id'] = 0;
    $retval = 0;
    if (array_key_exists('id', $_COOKIE)) {
        $cookie_id = $_COOKIE['id'];
        $ret = Fetch('select user.id, user.privs from buser.user,buser.cookie where user.id=cookie.user_id and cookie.ckey="' . $cookie_id . '"', $pif);
        if ($ret) {
            $pif['user_id'] = $retval = $ret[0]['id'];
            $pif['privs'] = $ret[0]['privs'];
        }
    }
    return $retval;
}

function DBConnect($pif) {
    //$dbi = mysqli_connect('localhost', $pif['dbuser'], $pif['dbpass'], $pif['dbname']);
    $dbi = mysqli_connect('', $pif['dbuser'], $pif['dbpass'], $pif['dbname'], 0, '/var/run/mysql/mysql.sock');
    if ($dbi->connect_error) {
	echo 'Connect Error (' . $dbi->connect_errno . ') ' . $dbi->connect_error;
	return 0;
    }
    return $dbi;
}

function DBQuery($dbi, $query) {
    $ret = Array();
    $res = $dbi->query($query);
    if ($res && $res->num_rows) {
	while (1) {
	    $row = $res->fetch_assoc();
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
	$dbi->close();
}

function GetPageInfo($page_id) {
    global $pif;
    chdir(getenv('DOCUMENT_ROOT'));
    $pif = array();
    $pif['page_id'] = $page_id;
    $pif['styles'] = ['main', $page_id];
    $pif['hierarchy'] = array();
    $pif['host'] = getenv('SERVER_NAME');
    $pif['docroot'] = getenv('DOCUMENT_ROOT');
    $pif['cgibin'] = $pif['docroot'] . '/../cgi-bin';
    $pif['is_beta'] = 0;
    $pif['is_alpha'] = 0;
    $pif['user_id'] = 0;
    if (substr($pif['host'], 0, 5) == 'beta.')
	$pif['is_beta'] = 1;
    if (substr($pif['host'], 0, 6) == 'alpha.')
	$pif['is_alpha'] = 1;
    $cfg = BarFile($pif['cgibin'] . '/.config', 'bamca.org');
    foreach (array_slice($cfg[0], 1) as $c) {
	$nl = explode(',', trim($c));
	$pif[$nl[0]] = $nl[1];
    }
    $pif['dbi'] = $dbi = DBConnect($pif);
    if (!$dbi)
	return $pif;
    $q = "select page_info.format_type,page_info.title,page_info.pic_dir,page_info.tail,page_info.flags from page_info where page_info.id='" . $page_id . "'";
    $res = $pif['dbi']->query($q);
    if ($res) {
	while (1) {
	    $row = $res->fetch_assoc();
	    if ($row) {
		$pif['format_type'] = $row['format_type'];
		$pif['title'] = $row['title'];
		$pif['pic_dir'] = $row['pic_dir'];
		$pif['tail'] = $row['tail'];
		$pif['flags'] = $row['flags'];
		$pif['hide_title'] = $row['flags'] & 2;
	    }
	    else
		break;
	}
    }
    global $LOCKDOWN;
    if ($LOCKDOWN)
        $pif['privs'] = '';
    else
        $pif['privs'] = 'b';
    $pif['user_id'] = 0;
    $retval = 0;
    if (array_key_exists('id', $_COOKIE)) {
        $cookie_id = $_COOKIE['id'];
        $ret = Fetch('select user.id, user.privs from buser.user,buser.cookie where user.id=cookie.user_id and cookie.ckey="' . $cookie_id . '"', $pif);
        if ($ret) {
            $pif['user_id'] = $retval = $ret[0]['id'];
            $pif['privs'] = $ret[0]['privs'];
        }
    }
    $bad_ip = DBQuery($dbi, "select count(*) from blacklist where reason='ip' and target='" . getenv('REMOTE_ADDR') . "'");
// not sure how to fix this yet
    $pif['bad_ip'] = $bad_ip[0]['count(*)'];
    $pif['messages'] = '';
    return $pif;
}

function DoHead($pif) {
    echo "<head><meta charset=\"UTF-8\">
<title>" . $pif['title'] . "</title>
<meta http-equiv=\"content-type\" content=\"text/html; charset=ISO-8859-1\">
<script defer src=\"https://use.fontawesome.com/releases/v5.0.8/js/all.js\"></script>
<script defer src=\"https://use.fontawesome.com/releases/v5.0.8/js/v4-shims.js\"></script>
<link rel=\"icon\" href=\"https://www.bamca.org/pic/gfx/favicon.ico\" type=\"image/x-icon\" />
<link rel=\"shortcut icon\" href=\"https://www.bamca.org/pic/gfx/favicon.ico\" type=\"image/x-icon\" />
<link rel=\"stylesheet\" href=\"/styles/main.css\" type=\"text/css\">
<link rel=\"stylesheet\" href=\"/styles/fonts.css\" type=\"text/css\">
<link rel=\"stylesheet\" href=\"/styles/" . $pif['page_id'] . ".css\" type=\"text/css\">
";
}

function DoPageHeader($pif) {
    $IMG_DIR_ART = 'pic/gfx';
    if (!$pif['is_beta'] && !$pif['is_alpha'])
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
//    if (!($pif['flags'] & 16)) {
//	NoAccess($pif, 'b', '');
//    }
    $id = CheckID($pif);
    echo '<table width="1024" class="body">' . "\n";
    if ($id > 0) {
	$username = Fetch('select name from buser.user where id=' . $id, $pif);
	$username = $username[0]['name'];
	echo '<tr><td class="loginbar">Welcome back, ' . $username . '! ('.$id.')';
	DoTextButtonLink('log_out', "https://" . $pif['host'] . "/cgi-bin/logout.cgi");
	DoTextButtonLink('user_profile', "https://" . $pif['host'] . "/cgi-bin/userprofile.cgi");
	if (CheckPerm($pif, 'u')) {
	    DoTextButtonLink('upload', "http://" . $pif['host'] . "/cgi-bin/upload.cgi");
	}
	if (CheckPerm($pif, 'a')) {
	    DoTextButtonLink('control_panel', "http://" . $pif['host'] . "/stuff.php");
	}
	echo "</td></tr>\n";
    }
    if ($pif['is_beta'])
	echo "<tr><td height=\"24\" class=\"beta\">&nbsp;</td></tr>\n";
    if ($pif['is_alpha'])
	echo "<tr><td height=\"24\" class=\"alpha\">&nbsp;</td></tr>\n";
    echo '<tr><td class="body">' . "\n";
    foreach ($pif['hierarchy'] as $hier) {
	echo '<a href="' . $hier[0] . '">' . $hier[1] . "</a> <i class=\"fas fa-chevron-right\"></i>\n";
    }
    if (!($pif['flags'] & 2))
	echo '<div class="title"><span class="titletext">' . $pif['title'] . "</span></div>\n";
}

function DoPageFooter($pif) {
    echo "</td></tr>\n";
    if ($pif['is_beta'])
	echo "<tr><td height=24 background=\"https://" . $pif['host'] . "/pic/gfx/beta.gif\">&nbsp;</td></tr>\n";
    if ($pif['is_alpha'])
	echo "<tr><td height=24 background=\"https://" . $pif['host'] . "/pic/gfx/alpha.gif\">&nbsp;</td></tr>\n";
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
    echo "<div class=\"$classname\">";
    echo "<a href=\"$linkloc\">";
    echo "$buttext";
    echo "</a>";
    echo "</div>\n";
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
    $but_max = '<div class="textbutton textupdown"><i class="fas fa-angle-double-up bold" title="TOP"></i></div>';
    $but_inc = '<div class="textbutton textupdown"><i class="fas fa-angle-up bold" title="UP"></i></div>';
    $but_dec = '<div class="textbutton textupdown"><i class="fas fa-angle-down bold" title="DOWN"></i></div>';
    $but_min = '<div class="textbutton textupdown"><i class="fas fa-angle-double-down bold" title="BOTTOM"></i></div>';
    echo "<a onclick=\"" . $cl . "settnum('" . $id . "'," . $mx . ");\">" . $but_max . "</a>\n";
    echo "<a onclick=\"" . $cl . "\" onmousedown=\"toggleOnNum('" . $id . "',1," . $mn . "," . $mx . ");\" onmouseup=\"toggleOff();\">" . $but_inc . "</a>\n";
    echo "<a onclick=\"" . $cl . "\" onmousedown=\"toggleOnNum('" . $id . "',-1," . $mn . "," . $mx . ");\" onmouseup=\"toggleOff();\">" . $but_dec . "</a>\n";
    echo "<a onclick=\"" . $cl . "settnum('" . $id . "'," . $mn . ");\">" . $but_min . "</a>\n";
}

function incrsel($id, $vl, $onchg="") {
    $but_max = '<div class="textbutton textupdown"><i class="fas fa-angle-double-up bold" title="TOP"></i></div>';
    $but_inc = '<div class="textbutton textupdown"><i class="fas fa-angle-up bold" title="UP"></i></div>';
    $but_dec = '<div class="textbutton textupdown"><i class="fas fa-angle-down bold" title="DOWN"></i></div>';
    $but_min = '<div class="textbutton textupdown"><i class="fas fa-angle-double-down bold" title="BOTTOM"></i></div>';
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

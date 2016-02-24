<?php
include "db.php";
include "fake.php";


function CheckPerm($lev)
{
    $retval = 0;
    if (array_key_exists('id', $_COOKIE))
    {
	passthru('../bin/secure.py ' . $lev, $retval);
    }
    return $retval;
}

function CheckID()
{
    $retval = 0;
    if (array_key_exists('id', $_COOKIE))
    {
	passthru('../bin/secure.py id', $retval);
    }
    return $retval;
}

function DBConnect($pif)
{
    $dbi = mysql_connect('localhost', $pif['dbuser'], $pif['dbpass']);
    if (!$dbi)
    {
	echo 'connect failed';
	return 0;
    }
    $r = mysql_select_db($pif['dbname'], $dbi);
    if (!$r)
    {
	echo 'select failed';
	return 0;
    }
    return $dbi;
}

function DBQuery($dbi, $query)
{
    $ret = Array();
    $res = mysql_query($query, $dbi);
    echo "<!-- query " . $query . " : ";
    print_r($res);
    echo "-->\n";
    if ($res && $res != 1)
    {
	while (1)
	{
	    $row = mysql_fetch_row($res);
	    if (!$row)
	    {
		break;
	    }
	    $ret[] = $row;
	}
    }
    return $ret;
}

function DBClose($dbi)
{
    mysql_close($dbi);
}

function GetPageInfo($page_id)
{
    putenv('HTTP_COOKIE=' . apache_getenv('HTTP_COOKIE'));
    //return FakeGetPageInfo($page_id);
    $pif = array();
    $pif['page_id'] = $page_id;
    $pif['hier'] = array();
    $pif['fake'] = 0;
    $pif['host'] = getenv('SERVER_NAME');
    $pif['docroot'] = getenv('DOCUMENT_ROOT');
    $pif['cgibin'] = $pif['docroot'] . '/../cgi-bin';
    $pif['isbeta'] = 0;
    if (substr($pif['host'], 0, 5) == 'beta.')
	$pif['isbeta'] = 1;
    $cfg = BarFile($pif['cgibin'] . '/.config', 'bamca.org');
    foreach (array_slice($cfg[0], 1) as $c)
    {
	$nl = explode(',', trim($c));
	$pif[$nl[0]] = $nl[1];
    }
    $dbi = DBConnect($pif);
    if (!$dbi)
	return $pif;
    $q = "select page_info.format_type,page_info.title,page_info.pic_dir,page_info.tail,page_info.flags from page_info where page_info.id='" . $page_id . "'";
    $res = mysql_query($q, $dbi);
    if ($res)
    {
	while (1)
	{
	    $row = mysql_fetch_row($res);
	    if ($row)
	    {
		$pif['format_type'] = $row[0];
		$pif['title'] = $row[1];
		$pif['pic_dir'] = $row[2];
		$pif['tail'] = $row[3];
		$pif['flags'] = $row[4];
	    }
	    else
		break;
	}
    }
    $bad_ip = DBQuery($dbi, "select count(*) from blacklist where reason='ip' and target='" . getenv('REMOTE_ADDR') . "'");
    $pif['bad_ip'] = $bad_ip[0][0];
    mysql_close($dbi);
    return $pif;
}

function DoHead($pif)
{
    echo "<head>
<title>" . $pif['title'] . "</title>
<link rel=\"icon\" href=\"http://www.bamca.org/pic/gfx/favicon.ico\" type=\"image/x-icon\" />
<link rel=\"shortcut icon\" href=\"http://www.bamca.org/pic/gfx/favicon.ico\" type=\"image/x-icon\" />
<link rel=\"stylesheet\" href=\"/styles/main.css\" type=\"text/css\">
<link rel=\"stylesheet\" href=\"/styles/" . $pif['page_id'] . ".css\" type=\"text/css\">
";
}

function DoPageHeader($pif)
{
    $IMG_DIR_ART = 'pic/gfx';
    if (!$pif['isbeta'])
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
    echo '<table width=100% class="body">' . "\n";
    if ($pif['fake'] == 1)
	;
    else if ($id > 0)
    {
	$username = Fetch('select name from user where id=' . $id, $pif);
	$username = $username[0][0];
	echo '<tr><td class="loginbar">Welcome back, ' . $username . '! ('.$id.')';
	DoButtonLink('log_out', $IMG_DIR_ART, "https://" . $pif['host'] . "/cgi-bin/logout.cgi");
	DoButtonLink('change_password', $IMG_DIR_ART, "https://" . $pif['host'] . "/cgi-bin/chpass.cgi?dest=http://" . $pif['host'] . "/stuff.php");
	$retval = CheckPerm('u');
	if ($retval)
	{
	    DoButtonLink('upload', $IMG_DIR_ART, "http://" . $pif['host'] . "/cgi-bin/upload.cgi");
	}
	if (CheckPerm('a'))
	{
	    DoButtonLink('control_panel', $IMG_DIR_ART, "http://" . $pif['host'] . "/stuff.php");
	}
	echo "</td></tr>\n";
    }
    if ($pif['isbeta'])
	echo "<tr><td height=24 background=\"http://" . $pif['host'] . "/pic/gfx/beta.gif\">&nbsp;</td></tr>\n";
    echo '<tr><td class="body">' . "\n";
    foreach ($pif['hier'] as $hier)
    {
	echo '<a href="' . $hier[0] . '">' . $hier[1] . "</a> &gt;\n";
    }
    if (!($pif['flags'] & 2))
	echo "<center><h1>" . $pif['title'] . "</h1></center>\n";
}

function DoPageFooter($pif)
{
    echo "</td></tr>\n";
    if ($pif['isbeta'])
	echo "<tr><td height=24 background=\"http://" . $pif['host'] . "/pic/gfx/beta.gif\">&nbsp;</td></tr>\n";
    echo "</table>\n";
}

function DoButton($butname, $artdir, $classname="button")
{
    $buttext = strtoupper(str_replace('_', ' ', $butname));
    echo '<img src="/' . $artdir . '/but_' . $butname . '.gif" alt="' . $buttext . '" onmouseover="this.src=\'/' . $artdir . '/hov_' . $butname . '.gif\';" onmouseout="this.src=\'/' . $artdir . '/but_' . $butname . '.gif\';" class="' . $classname . '">';
}

function DoButtonLink($butname, $artdir, $linkloc, $classname="button")
{
    echo '<a href="' . $linkloc . '">';
    DoButton($butname, $artdir, $classname);
    echo "</a>\n";
}

function DoButtonReset($artdir, $formid, $addl='')
{
    echo '<img src="' . $artdir . '/but_reset.gif" onmouseover="this.src=\'' . $artdir . '/hov_reset.gif\';" onmouseout="this.src=\'' . $artdir . '/but_reset.gif\';" border="0" onClick="ResetForm(document.' . $formid . ');' . $addl . '" alt="RESET" class="button">';
}

function DoButtonSubmit($butname, $artdir, $submit)
{
    $buttext = strtoupper(str_replace('_', ' ', $butname));
    echo '<input type="image" name="' . $submit . '" src="' . $artdir . '/but_' . $butname . '.gif" alt="' . $buttext . '" onmouseover="this.src=\'' . $artdir . '/hov_' . $butname . '.gif\';" onmouseout="this.src=\'' . $artdir . '/but_' . $butname . '.gif\';" class="button">' . "\n";
}

function BarFile($fname, $prefix)
{
    $sl = array();
    $sf = fopen($fname, "r");
    if (!$sf)
	return $sl;
    while (!feof($sf))
    {
	$l = fgets($sf);
	if (!feof($sf))
	{
	    $nl = explode('|', trim($l));
	    if ($nl[0] == $prefix)
		$sl[] = $nl;
	}
    }
    fclose($sf);
    return $sl;
}

function Fetch($query, $pif)
{
    $ret = array();
    $dbi = DBConnect($pif);
    if (!$dbi)
	return $ret;
    $ret = DBQuery($dbi, $query);
    DBClose($dbi);
    return $ret;
}

function DoResetJavascript()
{
    echo "<script  language=\"Javascript\">
function ResetForm(which){
 which.reset();
 return false;
}
</script>
";
}

function incrnum($id, $mn, $mx, $cl)
{
    echo "<a onclick=\"" . $cl . "settnum('" . $id . "'," . $mx . ");\"><img src=\"../pic/gfx/but_max.gif\" alt=\"TOP\" onmouseover=\"this.src='../pic/gfx/hov_max.gif';\" onmouseout=\"this.src='../pic/gfx/but_max.gif';\" ></a>\n";
    echo "<a onclick=\"" . $cl . "\" onmousedown=\"toggleOnNum('" . $id . "',1," . $mn . "," . $mx . ");\" onmouseup=\"toggleOff();\"><img src=\"../pic/gfx/but_inc.gif\" alt=\"UP\" onmouseover=\"this.src='../pic/gfx/hov_inc.gif';\" onmouseout=\"this.src='../pic/gfx/but_inc.gif';\" ></a>\n";
    echo "<a onclick=\"" . $cl . "\" onmousedown=\"toggleOnNum('" . $id . "',-1," . $mn . "," . $mx . ");\" onmouseup=\"toggleOff();\"><img src=\"../pic/gfx/but_dec.gif\" alt=\"DOWN\" onmouseover=\"this.src='../pic/gfx/hov_dec.gif';\" onmouseout=\"this.src='../pic/gfx/but_dec.gif';\" ></a>\n";
    echo "<a onclick=\"" . $cl . "settnum('" . $id . "'," . $mn . ");\"><img src=\"../pic/gfx/but_min.gif\" alt=\"BOTTOM\" onmouseover=\"this.src='../pic/gfx/hov_min.gif';\" onmouseout=\"this.src='../pic/gfx/but_min.gif';\" ></a>\n";
}

function incrsel($id, $vl, $onchg="")
{
    if ($vl > 0)
    {
	echo "<a onclick=\"settsel('" . $id . "');" . $onchg ."\"><img src=\"../pic/gfx/but_max.gif\" alt=\"TOP\" onmouseover=\"this.src='../pic/gfx/hov_max.gif';\" onmouseout=\"this.src='../pic/gfx/but_max.gif';\" ></a>\n";
	echo "<a onmousedown=\"toggleOnSel('" . $id . "',1);" . $onchg ."\" onmouseup=\"toggleOff();" . $onchg . "\"><img src=\"../pic/gfx/but_inc.gif\" alt=\"UP\" onmouseover=\"this.src='../pic/gfx/hov_inc.gif';\" onmouseout=\"this.src='../pic/gfx/but_inc.gif';\" ></a>\n";
	echo "<a onmousedown=\"toggleOnSel('" . $id . "',-1);" . $onchg ."\" onmouseup=\"toggleOff();" . $onchg . "\"><img src=\"../pic/gfx/but_dec.gif\" alt=\"DOWN\" onmouseover=\"this.src='../pic/gfx/hov_dec.gif';\" onmouseout=\"this.src='../pic/gfx/but_dec.gif';\" ></a>\n";
	//echo "<a onclick=\"incrsel('" . $id . "',1);\"><img src=\"../pic/gfx/but_inc.gif\" alt=\"UP\" onmouseover=\"this.src='../pic/gfx/hov_inc.gif';\" onmouseout=\"this.src='../pic/gfx/but_inc.gif';\" ></a>\n";
	//echo "<a onclick=\"incrsel('" . $id . "',-1);\"><img src=\"../pic/gfx/but_dec.gif\" alt=\"DOWN\" onmouseover=\"this.src='../pic/gfx/hov_dec.gif';\" onmouseout=\"this.src='../pic/gfx/but_dec.gif';\" ></a>\n";
	echo "<a onclick=\"setbsel('" . $id . "');" . $onchg ."\"><img src=\"../pic/gfx/but_min.gif\" alt=\"BOTTOM\" onmouseover=\"this.src='../pic/gfx/hov_min.gif';\" onmouseout=\"this.src='../pic/gfx/but_min.gif';\" ></a>\n";
    }
    else
    {
	echo "<a onclick=\"setbsel('" . $id . "');" . $onchg . "\"><img src=\"../pic/gfx/but_max.gif\" alt=\"TOP\" onmouseover=\"this.src='../pic/gfx/hov_max.gif';\" onmouseout=\"this.src='../pic/gfx/but_max.gif';\" ></a>\n";
	echo "<a onmousedown=\"toggleOnSel('" . $id . "',-1);" . $onchg . "\" onmouseup=\"toggleOff();" . $onchg . "\"><img src=\"../pic/gfx/but_inc.gif\" alt=\"UP\" onmouseover=\"this.src='../pic/gfx/hov_inc.gif';\" onmouseout=\"this.src='../pic/gfx/but_inc.gif';\" ></a>\n";
	echo "<a onmousedown=\"toggleOnSel('" . $id . "',1);" . $onchg . "\" onmouseup=\"toggleOff();" . $onchg . "\"><img src=\"../pic/gfx/but_dec.gif\" alt=\"DOWN\" onmouseover=\"this.src='../pic/gfx/hov_dec.gif';\" onmouseout=\"this.src='../pic/gfx/but_dec.gif';\" ></a>\n";
	//echo "<a onclick=\"incrsel('" . $id . "',-1);\"><img src=\"../pic/gfx/but_inc.gif\" alt=\"UP\" onmouseover=\"this.src='../pic/gfx/hov_inc.gif';\" onmouseout=\"this.src='../pic/gfx/but_inc.gif';\" ></a>\n";
	//echo "<a onclick=\"incrsel('" . $id . "',1);\"><img src=\"../pic/gfx/but_dec.gif\" alt=\"DOWN\" onmouseover=\"this.src='../pic/gfx/hov_dec.gif';\" onmouseout=\"this.src='../pic/gfx/but_dec.gif';\" ></a>\n";
	echo "<a onclick=\"settsel('" . $id . "');" . $onchg . "\"><img src=\"../pic/gfx/but_min.gif\" alt=\"BOTTOM\" onmouseover=\"this.src='../pic/gfx/hov_min.gif';\" onmouseout=\"this.src='../pic/gfx/but_min.gif';\" ></a>\n";
    }
}

function DoIncDecJavascript()
{
    echo '<script type="text/javascript" src="/bin/incrsel.js"></script>' . "\n";
}

function arr_get($array, $key, $default = null) {
    return isset($array[$key]) ? $array[$key] : $default;
}


function Debug($something)
{
    echo '<pre>'; print_r($something); echo '</pre>';
}

?>

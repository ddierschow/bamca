<?php

function Counter($pif)
{
    $dbi = mysql_connect('localhost', $pif['dbuser'], $pif['dbpass']);
    if (!$dbi)
    {
	echo 'connect failed';
	return $pif;
    }
    $r = mysql_select_db($pif['dbname'], $dbi);
    if (!$r)
    {
	echo 'select failed';
	return $pif;
    }
    $q = "select value from counter where id='". $pif['page_id'] . "'";
    $res = mysql_query($q, $dbi);
    $row = mysql_fetch_row($res);
    if ($row)
    {
	mysql_query("update counter set value=" . $row[0] + 1 . ", timestamp=now() where id='". $pif['page_id'] . "'", $dbi);
    }
    else
    {
	mysql_query("insert counter (id, value) values ('" . $pif['page_id'] . "', 1)", $dbi);
    }
}

?>

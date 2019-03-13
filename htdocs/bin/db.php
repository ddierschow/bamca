<?php

function Counter($pif)
{
    $dbi = mysqli_connect('localhost', $pif['dbuser'], $pif['dbpass'], $pif['dbname']);
    if (!$dbi)
    {
	echo 'connect failed';
	return $pif;
    }
    $q = "select value from counter where id='". $pif['page_id'] . "'";
    $res = $dbi->query($q);
    $row = $res->fetch_assoc();
    if ($row)
    {
	$dbi->query("update counter set value=" . $row[0] + 1 . ", timestamp=now() where id='". $pif['page_id'] . "'");
    }
    else
    {
	$dbi->query("insert counter (id, value) values ('" . $pif['page_id'] . "', 1)");
    }
}

?>

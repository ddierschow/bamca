<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("editor");
$pif['title'] = 'Submit a Comment';
DoHead($pif);
DoResetJavascript();

DoPageHeader($pif);

function reinput($arr) {
    foreach ($arr as $key => $val)
	echo '<input type="hidden" name="' . $key . '" value="' . $val . '">' . "\n";
}

if ($pif['bad_ip']) {
    echo "The IP address you're using has generated too much spam to our servers.\n";
    echo "The comment capability has been disabled.  You can try sending email if you really want to get through,\n";
    echo "but don't hope for too much.";
}
else if (!(strpos(arr_get($_POST, 'mycomment', ''), 'http://') === FALSE)) {
    echo 'Whoa there.  This is not the correct place to submit links.  Please use the "Suggest a Link" page on the main index.' . "\n";
}
else if (array_key_exists('submit_x', $_POST)) {
    echo "I am sending this comment for you. ";
    $fn = "../../logs/comment." . strftime('%Y%m%d.%H%M%S');
    echo "<dl><dt>My Subject</dt><dd>" . $_POST['mysubject'] . "</dd>\n";
    echo "<dl><dt>My Comment</dt><dd>" . $_POST['mycomment'] . "</dd>\n";
    echo "<dt>My Name</dt><dd>" . $_POST['myname'] . "</dd>\n";
    echo "<dt>My Email</dt><dd>" . $_POST['myemail'] . "</dd></dl>\n";
    $fh = fopen($fn, "w");
    fwrite($fh, "_POST\n\n" . print_r($_POST, True) . "\n\n");
    fwrite($fh, "REMOTE_ADDR=" . getenv('REMOTE_ADDR') . "\n");
    fclose($fh);
    echo "Thanks for sending that.  Now please use the BACK button on your browser to return to where you were.";
}
else {
    echo '<form action="comment.php" method="post" name="comment">' . "\n";
    reinput($_GET);
?>
We welcome any comments you might have on the website.  Everything will be read, and if you provide
an email address, we will try to respond.
<table>
<tr><td>My Subject</td><td><input type="text" name="mysubject" size=80 maxlength=80></td></tr>
<tr><td>My Comment</td><td><textarea name="mycomment" cols=80 rows=6></textarea></td></tr>
<tr><td>My Name</td><td><input type="text" name="myname" size=80 maxlength=80> (optional)</td></tr>
<tr><td>My E-mail Address</td><td><input type="text" name="myemail" size=80 maxlength=80> (optional)</td></tr>
</table>

<input type="image" name="submit" src="../pic/gfx/but_submit.gif" alt="Submit" onmouseover="this.src=\'../pic/gfx/hov_submit.gif\';" onmouseout="this.src=\'../pic/gfx/but_submit.gif\';" class="button"> -
<img src="../pic/gfx/but_reset.gif" onmouseover="this.src=\'../pic/gfx/hov_reset.gif\';" onmouseout="this.src=\'../pic/gfx/but_reset.gif\';" border="0" onClick="ResetForm(document.comment)" alt="RESET" class="button">

</form>
<?php
}

DoPageFooter($pif);
?>

</body>
</html>

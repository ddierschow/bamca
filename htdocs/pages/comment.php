<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("comment");
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
else {
    echo '<form action="/cgi-bin/comment.cgi" method="post" name="comment">' . "\n";
    reinput($_GET);
?>
We welcome any comments you might have on the website.  Everything will be read, and if you provide
an email address, we will try to respond.
<table>
<tr><td>My Subject</td><td><input type="text" name="mysubject" size=80 maxlength=80></td></tr>
<tr><td>My Comment</td><td><textarea name="mycomment" cols=80 rows=6></textarea></td></tr>
<tr><td>My Name</td><td><input type="text" name="myname" size=80 maxlength=80> (optional)</td></tr>
<tr><td>My E-mail Address</td><td><input type="text" name="myemail" size=80 maxlength=80> (optional)</td></tr>
<tr><td>A Relevant Picture</td><td><input type="file" name="pic" size=80 maxlength=80> (optional)</td></tr>
<tr><td>Photographer Credit</td><td><input type="text" name="credit" size=80 maxlength=80> (optional)</td></tr>
</table>

<?php DoTextButtonSubmit("SUBMIT", "submit"); ?> -
<?php DoTextButtonReset('comment', 'reset'); ?>


</form>
<?php
}

DoPageFooter($pif);
?>

<?php DoFoot($pif); ?>
</html>

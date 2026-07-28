<!DOCTYPE html>
<html>
<?php
include "../bin/basics.php";
include "../config.php";
$pif = GetPageInfo("error");
DoHead($pif);
DoPageHeader($pif);
?> 

<h2>Error 503 encountered:  Server error.</h2>

<img src="/pic/man/var/l_mb694-01.jpg" class="centered">
<div class="center"><i>Please enjoy this model instead.</i></div>

<?php
DoPageFooter($pif);
DoFoot($pif);
?>
</html>

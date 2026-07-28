<!DOCTYPE html>
<html>
<?php
include "../bin/basics.php";
include "../config.php";
$pif = GetPageInfo("error");
DoHead($pif);
DoPageHeader($pif);
?> 

<h2>Error 500 encountered:  Internal server error.</h2>

<img src="/pic/man/var/l_mb771-08.jpg" class="centered">
<div class="center"><i>Please enjoy this model instead.</i></div>

<?php
DoPageFooter($pif);
DoFoot($pif);
?>
</html>

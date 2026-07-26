<!DOCTYPE html>
<html>
<?php
include "../bin/basics.php";
include "../config.php";
$pif = GetPageInfo("error");
DoHead($pif);
DoPageHeader($pif);
?> 

<h2>Error 400 encountered:  Bad request.</h2>

<img src="/pic/man/var/l_mb188-10.jpg" class="centered">
<div class="center">Please enjoy this model instead.</div>

<?php
DoPageFooter($pif);
DoFoot($pif);
?>
</html>

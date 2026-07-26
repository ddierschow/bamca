<!DOCTYPE html>
<html>
<?php
include "../bin/basics.php";
include "../config.php";
$pif = GetPageInfo("error");
DoHead($pif);
DoPageHeader($pif);
?> 

<h2>Error 404 encountered:  Page not found.</h2>

<img src="/pic/man/var/l_mb439-09.jpg" class="centered">
<div class="center">Please enjoy this model instead.</div>

<?php
DoPageFooter($pif);
DoFoot($pif);
?>
</html>

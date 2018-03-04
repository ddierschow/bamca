<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("other");
DoHead($pif);
DoPageHeader($pif);
?>

<ul>
<li><a href="../../cgi-bin/sets.cgi?page=carry">Carry Cases</a>
<li><a href="../../cgi-bin/matrix.cgi?page=heritage">Heritage Series</a>
</ul>

<a href=".."><div class="textbutton">BACK</div> to the main index.</a>

<?php
DoButtonComment($pif);
DoFoot($pif); ?>
</html>

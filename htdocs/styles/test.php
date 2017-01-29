<html>
<head><meta charset="UTF-8">
<title>Style Tester : <?php echo $fn; ?></title>
<link rel="icon" href="http://www.bamca.org/pic/gfx/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="http://www.bamca.org/pic/gfx/favicon.ico" type="image/x-icon" />
<?php
// Quickie little script to test style files.  Mostly for looking
// at the pretty colors.
$fn = '';
if ($_GET['s']) {
    $fn = $_GET['s']; ?>
<link rel="stylesheet" href="/styles/main.css" type="text/css">
<link rel="stylesheet" href="/styles/<?php echo $fn; ?>" type="text/css">
<?php
}
else {
    foreach (glob("*.css") as $fn) {
?>
<link rel="stylesheet" href="/styles/<?php echo $fn; ?>" type="text/css">
<?php
    }
    $fn = '';
}
?>
</head>
<body>

<?php
if ($fn) {
    $sf = file($fn);
    foreach ($sf as $ln) {
	$ln = trim($ln);
	if (strlen($ln) == 0)
	    ;
	else if ($ln[0] == '.') {
	    $cname = substr($ln, 1, strpos($ln, ' ') - 1);
	    echo '<div class="' . $cname . '">' . $ln . "</div>\n";
	}
	else
	    echo $ln . "<br>\n";
    }
}
else {
    echo "Hi.  I'm a test file.<p><ul>";
    foreach (glob("*.css") as $fn) {
?>
<li><a  href="?s=<?php echo $fn; ?>"><?php echo $fn; ?></a>
<?php
    }
    echo "</ul>";
}
?>

</body>
</html>

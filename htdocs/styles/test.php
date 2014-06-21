<html>
<?php
// Quickie little script to test style files.  Mostly for looking
// at the pretty colors.
$fn = 'main';
if ($_GET['s'])
    $fn = $_GET['s'];
?>
<head>
<title>Style Tester : <?php echo $fn; ?></title>
<link rel="icon" href="http://www.bamca.org/pic/gfx/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="http://www.bamca.org/pic/gfx/favicon.ico" type="image/x-icon" />
<link rel="stylesheet" href="/styles/main.css" type="text/css">
<link rel="stylesheet" href="/styles/<?php echo $fn; ?>.css" type="text/css">
</head>
<body>

<?php
$sf = file($fn . '.css');
foreach ($sf as $ln) {
    $ln = trim($ln);
    if (strlen($ln) == 0)
	;
    else if ($ln[0] == '.') {
	$cname = substr($ln, 1, strstr($ln, ' ') - 1);
	echo '<div class="' . $cname . '">' . $ln . "</div>\n";
    }
    else
	echo $ln . "<br>\n";
}
?>

</body>
</html>

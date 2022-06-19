<!DOCTYPE html>
<html>

<body>
<?php
include "wikidat.php";
echo "<table>\n<tr style='vertical-align: top;'>\n<td width='50%'>\n";
echo "<ul>\n";

$c = 0;
foreach ($dat as $year => $links) {
    echo "<li>";
    $c = $c + 1;
    $base_url = '';
    foreach ($links as $key => $val) {
        if ($base_url == '') {
            echo '<a href="' . $val . '">' . $key . "</a>\n";
            $base_url = $val;
        }
        else {
            echo '<a href="' . $base_url . '#' . $key . '">' . $val . "</a>\n";
        }
    }
    if ($c == 40) {
        echo "</ul>\n</td>\n<td>\n<ul>\n";
    }
}

echo "</ul>\n";
echo "</td>\n</tr>\n</table>\n";
?>

</body>
</html>

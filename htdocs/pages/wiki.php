<!DOCTYPE html>
<html>

<body>
<ul>
<li><a href="https://matchbox.fandom.com/wiki/Matchbox_Cars_Wiki">Front Page</a>
<li><a href="https://matchbox.fandom.com/wiki/Models_of_Yesteryear">Models of Yesteryear</a>
<li><a href="https://matchbox.fandom.com/wiki/Sky_Busters">Skybusters</a>
<li><a href="https://matchbox.fandom.com/wiki/Speed_Kings">Speed Kings</a>
<li><a href="https://matchbox.fandom.com/wiki/Super_Kings">Super Kings</a>
<li><a href="https://matchbox.fandom.com/wiki/Sea_Kings">Sea Kings</a>
<li><a href="https://matchbox.fandom.com/wiki/Battle_Kings">Battle Kings</a>
<li><a href="https://matchbox.fandom.com/wiki/Convoy">Convoy</a>
</ul><hr>

<table>
<tr style='vertical-align: top;'>
<td width='50%'>

<ul>

<?php
include "wikidat.php";
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
?>

</ul>
</td>
</tr>
</table>

</body>
</html>

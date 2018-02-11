<!DOCTYPE html>
<html>
<?php
include "../bin/basics.php";
include "../config.php";
$pif = GetPageInfo("lsm");
DoHead($pif);
DoPageHeader($pif);
$mans = '/cgi-bin/manno.cgi?section=';
$sets = '/cgi-bin/sets.cgi?page=';

function show_div($css, $scr, $img, $lbl, $ttl='') {
    global $IMG_DIR_ART;
    echo ' <a href="' . $scr . '">' . "\n";
    echo '  <div class="tabc ' . $css . '">' . "\n";
    echo '   <div class="tabm">' . "\n";
    if ($img && file_exists('.' . $IMG_DIR_ART . '/' . $img)) {
	echo '    <img src="' . $IMG_DIR_ART . '/' . $img . '" title="' . $lbl . '">' . "\n";
    } else {
	echo '    ' . $lbl . "\n";
    }
    if ($ttl) {
	echo '    <br>' . $ttl . "\n";
    }
    echo "   </div>\n";
    echo "  </div>\n\n";
    echo " </a>\n";
}

echo "<center>\n";
echo '<div class="tabt">' . "\n\n";

show_div('ey',  $mans . 'early',  'early.gif', 'Early Lesney Toys');
show_div('mp',  $mans . 'maj',    'majorpack.gif', 'Major Pack');
show_div('ks',  $mans . 'ks',     'kingsize.gif', 'King Size');
show_div('sk',  $mans . 'sks',    'sksk.gif', 'Super King and Speed Kings');
show_div('bk',  $mans . 'bk',     'battlekings-s.gif', 'Battle Kings');
show_div('a2k', $mans . 'a2k',    'adventure2k-s.gif', 'Adventure 2000');
show_div('sea', $mans . 'sk',     'seakings.gif', 'Sea Kings');
show_div('cy',  '/convoy/',       'convoy.gif', 'Convoys');
show_div('rwr', $mans . 'rwr',    'rwr.gif', 'Real Working Rigs');
show_div('lyy', $mans . 'yy',     'moy3.gif', 'Models of Yesteryear', 'Lesney');
show_div('uyy', $mans . 'moy',    'moy3.gif', 'Models of Yesteryear', 'Post-Lesney');
show_div('dy',  $mans . 'dy',     'dinky-s.gif', 'Dinky Collection');
show_div('c43', $sets . 'coll43', 'collectibles.gif', 'Matchbox Collectibles');
show_div('c72', $sets . 'coll72', 'coll72.gif', 'Matchbox Collectibles', 'Aircraft');
show_div('acc', $mans . 'acc',    'acc-s.gif', 'ACCESSORIES');

echo "</div>\n";
echo "</center>\n\n";

DoPageFooter($pif);
DoFoot($pif);
?>
</html>

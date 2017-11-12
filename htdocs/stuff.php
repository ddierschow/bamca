<!DOCTYPE html>
<html>
<?php
include "bin/basics.php";
include "config.php";
include "version.txt";
$pif = GetPageInfo("stuff");
$pif['title'] .= ' ' . $version;
DoHead($pif);
DoPageHeader($pif);

function warn_number($num) {
    if ($num > 0)
	echo '<span class="warning">' . $num . '</span>';
    else
	echo '&nbsp;';
}

NoAccess($pif, 'a', 'stuff.php');
$links = Fetch("select section_id,link_type,name,url from link_line where page_id='links.stuff' order by display_order", $pif);
$cols = Fetch("select id,start,category from section where page_id='links.stuff' order by display_order", $pif);
$sections = array();
foreach ($links as $ent) {
    if (!isset($sections[$ent[0]]))
	$sections[$ent[0]] = array();
    $sections[$ent[0]][] = array("ty" => $ent[1], 'name' => $ent[2], 'url' => $ent[3]);
}
if ($pif['is_beta'])
    array_unshift($sections['l1'], array('ty' => 'b', 'name' => 'release', 'url' => "http://www.bamca.org/stuff.php"));
else
    array_unshift($sections['l1'], array('ty' => 'b', 'name' => 'beta', 'url' => "http://beta.bamca.org/stuff.php"));

$newerrors = Fetch("select id,health from counter where not health=0", $pif);
$newerrors += Fetch("select id,health from buser.counter where not health=0", $pif);
$errcounter = 0;
foreach ($newerrors as $ent)
    $errcounter = $errcounter + $ent[1];
$newusers = Fetch("select name from buser.user where state=1 and privs=''", $pif);
$newlinks = Fetch("select count(*) from link_line where ((flags&128)=128)", $pif);
$commentfiles = glob("../../comments/comment.*");
$imagefiles = glob("../../inc/*");
$imagename = $l = '';
$imagedescs = fopen('/home/bamca/logs/descr.log', "rt");
while (!feof($imagedescs)) {
    $l = fgets($imagedescs);
    if (strlen($l) > 8)
	$imagename = $l;
}
fclose($imagedescs);

// ---- End of the heavy lifting.  Now the fun begins. -----
?>

<table width=1024px cellpadding=0 cellspacing=0>
 <tr><td colspan=8 class="boxborder"></td></tr>
 <tr>
  <td class="boxborder" rowspan=4><img src="/pic/gfx/red4x4.gif"></td>
<?php
foreach ($cols as $col) {
    if ($col[0][0] == 'c') {
	echo '  <td class="linklist ' . $col[2] . '" rowspan=' . $col[1] . ">\n";
	LinksList($sections[$col[0]], '<li>', '<h3><ul>', '</ul></h3>');
	echo "  </td>\n";
    }
}
?>

  <td class="boxborder" rowspan=4><img src="/pic/gfx/red4x4.gif"></td>
 </tr>

 <tr><td colspan=2><div class="database high" id="dbc" onclick="document.getElementById('database').click();">
  <a href="database.php" id="database">database</a>
  </div></td></tr>

 <tr>

  <td colspan=6 class="high">
<?php LinksList($sections['l1'], '', '<center>', '</center>'); ?>
  </td>

 </tr>

 <tr>
  <td colspan=6>
<?php LinksList($sections['l2'], ' - ', '<center><i>', '</i></center>'); ?>
  </td>
 </tr>

 <tr><td colspan=8 class="boxborder"></td></tr>
 <tr><td colspan=8>&nbsp;</td></tr>
 <tr><td colspan=8 class="boxborder"></td></tr>
 <tr>
  <td class="boxborder"></td>
  <td colspan=6>
   <table><tr><td width="144">
   Errors found:</td><td width="48">
   <?php warn_number($errcounter); ?>
   </td>
   <td>
   <?php
DoTextButtonLink('see', "cgi-bin/traverse.cgi?d=../../logs");
DoTextButtonLink('clear', "cgi-bin/editor.cgi?clear=1");
?>
   </td>
   <td><span class="warning"><?php
if (count($newerrors) > 0)
{
    foreach ($newerrors as $ent)
	echo ' ' . $ent[0] . ' (' . $ent[1] . ')';
}
?></span>
   </td></tr>

   <tr><td>
   New users:</td><td><?php warn_number(count($newusers)); ?></td><td>
   <span class="warning"><?php
DoTextButtonLink('see', "https://" . $pif['host'] . "/cgi-bin/user.cgi");
if (count($newusers) > 0)
{
    foreach ($newusers as $ent)
	echo $ent[0] . ' ';
}
?></span></td>
   </tr>

   <tr><td>
   New links:</td><td><?php warn_number($newlinks[0][0]); ?></td><td><?php DoTextButtonLink('see', "cgi-bin/edlinks.cgi?sec=new"); ?></td>
   <td><?php LinksList($sections['l3'], ' - '); ?></td></tr>

   <tr><td>
   New comments:</td><td><?php warn_number(count($commentfiles)); ?></td><td>
   <?php DoTextButtonLink('see', "cgi-bin/traverse.cgi?d=../../comments"); ?></td>
   <td><?php LinksList($sections['l4'], ' - '); ?></td></tr>

   <tr><td>
   Uploaded images:</td><td><?php warn_number(count($imagefiles)); ?></td>
   <td>last <?php echo substr($imagename, 0, 9); ?></td></tr>
   </table>
  </td>
  <td class="boxborder"></td>
 </tr>
 <tr><td colspan=8 class="boxborder"></td></tr>

</table>

<?php DoPageFooter($pif); ?>
<img src="/pic/gfx/hruler1024.gif">

</body>
</html>

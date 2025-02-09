<!DOCTYPE html>
<html>
<?php
include "bin/basics.php";
include "config.php";
include "bin/forms.php";
$pif = GetPageInfo("database", 1);
DoHead($pif);
$pif['isadmin'] = CheckPerm($pif, 'a');
$pif['hierarchy'][0] = ['/', 'Home'];
$pif['hierarchy'][1] = ['/database.php', 'Database'];

DoResetJavascript();
DoShowHideJavascript('+', '-');
DoIncDecJavascript();
DoPageHeader($pif);

echo "<hr>\n";

echo "<table width=\"100%\">\n";
Section($pif, ["tag" => "ss", "name" => "Super Search", "fn" => 'SectionSearch', "scr" => "search.cgi"]);
echo "</table>\n";

PageFooter('search');
DoPageFooter($pif);
DoFoot($pif);

//---- support functions -----------------------------------------

// required: fn tag scr name  optional: reset
function Section($pif, $args) {
    echo "<tr id=\"{$args['tag']}\">\n  <td class=\"{$args['tag']}_head sel_head\">\n";
    echo "   <center><h2>{$args['name']}</h2></center>\n  </td>\n </tr>\n";
    if (!$args['fn'])
        return;
    echo " <tr><td class=\"spacer\"></td></tr>\n\n <tr><td class=\"{$args['tag']}_body sel_body\">\n";
    if (isset($args['scr'])) {
	echo "<form action=\"/cgi-bin/{$args['scr']}\" method=\"get\" name=\"{$args['tag']}\">\n";
    }
    else {
	echo "<i id=\"{$args['tag']}\"></i>\n";
    }
    if (isset($args['scr'])) {
	echo "Select what kind of Matchbox lineup you would like to see, then click \"SEE THE MODELS\".\n";
	echo "<p>\n";
	call_user_func($args['fn'], $pif);
	echo "<br>\n";
	DoTextButtonSubmit("SEE THE MODELS", "submit");
	DoTextButtonReset($args['tag'], arr_get($args, 'reset', ''));
	if ($pif['isadmin'])
	    Checks('checkbox', $args['tag'], 'verbose', [['1', '<i>Verbose</i>']], ''); 
    }
    else
	call_user_func($args['fn'], $pif);
    if (isset($args['scr'])) {
	echo "\n</form>\n\n";
    }
    echo "  </td>\n </tr>\n";
}

//---- beginning of sections -------------------------------------

function SectionSearch($pif) {
    $id = 'ss';

    echo "<hr><table><tr><td width=\"50%\">\n";
    echo "<h3>Casting Information</h3>\n";
    echo "<table><tr>\n";
    echo "<td>Manufacturing ID:</td><td colspan=\"2\"><input type=\"text\" name=\"cid\" id=\"idId\" value=\"\" size=\"12\">\n";
    Checks('radio', $id, 'cidx', [['0', 'partial', 1], ['1', 'exact']], '');
    echo "</td>\n";
    echo "</tr>";
    SimpleText("Casting name:", 'cname', 2);

    echo " <tr>\n";
    echo "  <td>Section:</td><td colspan=\"4\">\n";
    $q = "select 0 as flags, id as val, name as title from section where page_id='manno' order by display_order";
    $ql = Fetch($q, $pif);
    Select('section', 'manSection', array_merge(
        [['flags' => 64, 'val' => '', 'title' => 'All Sections']], $ql), '');
    echo "</td>\n";

    echo "</tr><tr>\n<td>Numbers:</td><td>";
    Checks('radio', $id, 'range', [['', 'All numbers', 1]]);
    echo "</td>\n<td>";
    Checks('radio', $id, 'range', [['some', 'Some numbers']]);
    echo "</td></tr>\n";
    echo "<tr><td colspan=\"2\"></td>\n<td>starting at:</td>\n";
    ChooseNum("idst", "manStart", 4, 1, "document.getElementById('manEnd').value", 1,
              'onFocus="document.ss.range[1].checked=true;"', "document.ss.range[1].checked=true;");
    echo " </tr>\n";
    echo " <tr><td colspan=\"2\">";
    echo "</td>\n";
    echo "  <td>ending at:</td>\n";
    ChooseNum("idend", "manEnd", 4, "document.getElementById('manStart').value", 9999, 9999,
              'onFocus="document.ss.range[1].checked=true;"', "document.ss.range[1].checked=true;");
    echo " </tr>\n";

    echo "<tr><td>Vehicle make:</td><td colspan=\"3\">\n";
    Checks('radio', $id, 'make', [['', 'any', 1], ['unk', 'unknown'], ['unl', 'unlicensed']]);
    Checks('radio', $id, 'make', [['makename', 'Specific make:']], '');
    echo "<input type=\"text\" name=\"makename\" onFocus=\"document.ss.make[3].checked=true;\">\n  </td>\n";
    echo " </tr>\n";
    echo "</table>\n";

    echo "Vehicle type:\n";
    YNMTable($pif, $id, 'ynm1');

    echo "</td><td>\n";
    echo "<h3>Variation Information</h3>\n";
    echo "<table>\n";
    echo "<tr><td>Variation ID:</td><td><input type=\"text\" name=\"vid\">";
    Checks('radio', $id, 'vidx', [['0', 'partial', 1], ['1', 'exact']], '');
    echo "</td></tr>\n";
    echo "<tr><td>Description:</td><td><input type=\"text\" name=\"description\"></td></tr>\n";
    SimpleText("Body:", 'body');
    SimpleText("Base:", 'base');
    SimpleText("Interior:", 'interior');
    SimpleText("Wheels:", 'wheels');
    SimpleText("Windows:", 'windows');
    SimpleText("Base text:", 'text');
    SimpleText("With:", 'with');
    echo "<tr><td>\n";
    echo "Manufacture location:\n";
    echo "</td><td>\n";
    SelectPlant('any location', $id);
    echo "</td></tr>\n";
    if ($pif['isadmin']) {
        SimpleText("<i>Area:</i>", 'area');
        SimpleText("<i>Category:</i>", 'category');
        SimpleText("<i>Date:</i>", 'date');
        SimpleText("<i>Note:</i>", 'note');
    }
    echo "<td>Codes:</td>\n";
    echo "<td>";
    Checks('checkbox', $id, 'codes', [['1', 'Code 1 Models', 1]], ' - ');
    Checks('checkbox', $id, 'codes', [['2', 'Code 2 Models', 1]], '');
    echo "</td></tr>\n";
    echo "</table>\n";

    echo "<hr><h3>List Selection</h3>\n";
    echo "<table><tr>\n";
    echo "<td class=\"hspacer\"></td>\n";
    echo "<td>";
    echo "Sort results by:</td><td>\n";
    Checks('radio', $id, 'stype', [['i', 'IDs', 1]]);
    Checks('radio', $id, 'stype', [['n', 'Casting name']]);
    Checks('radio', $id, 'stype', [['s', 'Casting section']]);
    echo "</td>\n";
    echo "<td>";
    echo "Show results as:</td><td>\n";
    Checks('radio', $id, 'ltype', [['c', 'Castings', 1]]);
    Checks('radio', $id, 'ltype', [['v', 'Variations']]);
    echo "</td>\n";
    echo "</tr></table><br>\n";
    echo "<table class=\"inset\"><tr><td>\n";
    echo "<b>A note on the results that will be returned:</b><br>\n";
    echo "If you specify variation search criteria, then select to show as castings, the list returned will be \n";
    echo "all the models that have one or more variations that match your search.  The entries shown will be \n";
    echo "the generic casting pictures, which you can click on to see the lists of matching variations.\n";
    echo "</td></tr></table>\n";
    echo "<p></td></tr></table>";
}

//---- end of sections -------------------------------------------

?>
</html>

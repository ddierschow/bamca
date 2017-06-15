<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
include "subs.php";
$pif = GetPageInfo("convoy");
$pif['title'] = $pif['title'] . ' - Convoy Definitions';
$desc = "Convoy Definitions";
$defaults = [];
DoHead($pif);
?>
  <meta name="author" content="John Baum and Dean Dierschow">
  <meta name="description" content="<?php echo $desc; ?>">
<?php
DoPageHeader($pif);
?>

The Matchbox Convoy Project - Definitions<br>
<br>
<div align="center"><font size="+3" face="Arial">Definitions -
Talking the Talk<br>
<font size="+1"><br>
This page let you know what we are talking about and what
we mean when we say it. <br>
First we will give you an example, then explain all the notes then
provide another example with more variations.<br>
</font></font></div>
<br>
<br>
<div align="center">
<?php
    start_table();
?>
    <tr align="center">
      <td valign="top" colspan="2">
	<b><font face="Arial">Series: CY009A - Kenworth Aerodyne Conventional Cab with Box Trailer</font></b>
      </td>
    </tr>
<?php
    show_convoy(['mod' => 'CY009A', 'var' => '29a',
	'cab' => 'MB103', 'tlr' => 'Box', 'mfg' => 'Thailand',
	'liv' => 'Skittles', 'cod' => '1', 'rar' => '',
	'cdt' => 'red',
	'tdt' => "red container and base, Thailand, SKITTLES labels",
    ]);
    end_table();
?>
</div>

<br>
<div align="left"><br>
<b>Series:</b> The top of each page will have the Convoy series number
with the common truck cab and trailer listed.
The series are as follows:<br>
<ol>
  <li>TP - The fore runners of the current Convoy series. The real name
of the series is Matchbox 900, but this line was given the nickname from
the "Two Pack" and "Twinpack" (TP) which it was part of.</li>
  <li>CY - The most common series, good old plain jane truck and
trailer combinations</li>
  <li>TM and TC - Team Matchbox was first introduced in 1985 as a secondary Convoy line which included team transporters and two vehicles. By 1988, the line was renamed Team Convoy. Team Convoy included some of the Team Matchbox, but also included a combination of one Convoy plus one miniature. Several models were never numbered, however in late 1992, a CY111A was issued for Australia which includes a Team Matchbox type issue. As this has a CY rather than a TM or TC number, these are listed in the Convoy section. White
Rose Collectibles introduced Team Convoy sets in 1990 with numbers starting at TC number 54.</li>
  <li>CCY - The most recently introduced line, these have more details
and are adult collectibles. This line is also known as Ultras</li>
  <li>DYM - Basically the same as the CCY's but issued under the Dinky
and Yesteryear lines.</li>
</ol>
<b>SIDE BOXES:</b> One the left hand side are a group of abbreviations
which defines the specific model pictured.
<ol>
  <li><b>Variation</b>: This stands for the common listed variation of the
series. The numbers are the previously published variation while the
letters are the sub-variation that had not been published. The
published variation will always be "a"</li>
  <li><b>Cab:</b> This is the specific truck/tractor MAN number
for this variation (see the <a href="cabs.php">"CABS"</a>
page for detailed listing).  Normally this will be the same as the
model listed at the top of the page, but there are exceptions
throughout the convoy line.</li>
  <li><b>Manufacture:</b> This is the country where the
Truck/Tractor was made. Normally it will be either England, Macau,
Thailand, or China. Sometimes this is the only difference between the
variations.</li>
  <li><b>Trailer:</b> This would be the specific trailer model of this
combination. While the top of the page provides the generic trailer
type, there are variations among the trailer. See the <a
 href="trailer.php"><font color="#3366ff">"TRAILERS"</font></a>
page for detailed listing.</li>
  <li><b>Livery: </b>This is the name found on the side of the Truck
and/or Trailer</li>
  <li><b>Code:</b> This defines who put the Livery on the
Truck/Trailer. The codes are as follows</li>
  <ol>
    <li><b>Code 1</b> - Regular issued model including most
WhiteRose models.<br>
    </li>
    <li><b>Code 2</b> - Limited issued of promotional nature made
by a third party but authorized by Matchbox. Normally produced by
A.S.A.P., ColorComp, or AdTrucks. These combinations normally
have white cabs and white trailer. <br>
    </li>
    <li><b>Code 3</b> - Any privatley labeled models, by companies
or individuals, that was not approved by
Matchbox<br>
    </li>
    <li><b>Code 4</b> - Matchbox limited quantity models
(one-offs) not put on general sale. Normally company issued gifts to
individuals or organization.<br>
    </li>
    <li><b>PP</b> - Pre-Production - Factory mockups of convoys issued
or a small production run that was not issued to the public normally
due to problems with licensing. This group also includes what
collectors
call as "lunch box specials," models made by one employee at the
factory that differed from the regular production run.</li>
  </ol>
  <li><b>Rarity</b>: This gives you an idea of how hard it is to find
this specific variation on a one to five scale, with one being going to
a local toy store and getting it off the self, and five being having to
wait until a collector dies or gets a divorce.</li>
</ol>
<b>BOTTOM BOXES:</b> One the bottom will be the specific details of the
Truck and Trailer and any differences found from the "a"
variation. Those differences would normally be in red for easy
identification. Follows is a list of what may be found in this
area.
<ol>
  <li><b>Truck:</b> Colors of the cab, chassis and base, if
different from the cab. Markings on the cab such as stripes, listed in
order from top to bottom, tampo (painted) printing, decals or other cab
markings. Window colors, exhaust coloring, an tires if different from
the norm.</li>
  <li><b>Trailer</b>: Color of the trailer base, the main
body, and body parts. The type of labeling on the trailer such as
paper or vinyl labels, decals or tempo printed, and a description of
the load, if any.</li>
  <li><b>Notes</b>: Additional information of interest or
history about the specific model.<br>
  </li>
</ol>

<br>
<div align="center">
<div align="center">
<?php
    start_table();
?>
    <tr align="center">
      <td valign="top" colspan="2">
        <b><font face="Arial">Series: CY017 - Scania T 142 Cab with Tanker Trailer</font></b>
      </td>
    </tr>
<?php
    show_convoy(['mod' => 'CY017A', 'var' => '08a',
	'cab' => 'MB147', 'tlr' => 'Tanker', 'mfg' => 'Thailand',
	'liv' => 'Feoso', 'cod' => '1', 'rar' => '',
	'cdt' => 'white, dark gray chassis, black base',
	'tdt' => 'white tank, dark gray base, FEOSO tampo',
    ]);
    end_table();
?>
</div>

<br>
<br>
<div align="center"><b><font size="+2" face="Arial">What is a
variation?<br>
</font></b>
<div align="left"><font size="+1" face="Arial"><br>
 That is the $50 question. Most
collectors would agree that a variation would be a change in any of the
components from the "a" variation. The Scania above was first issued
with a black base and this model has a silver base, this makes it a
variation. Different distinct color differences in cabs, chassis,
bases, roofs, exhaust and complete wheel sets (single axle sets changes
are normally classified as factory errors) and signage placements are
definite variations. Slight color changes are more attributable
to
factory paint mixing, and are generally not considered as a variation.</font><br>
</div>
</div>
<div align="center">
<br>
<hr width="100%" size="2"><br>
<font size="+1" color="#3333ff"><font color="#006600">One of the
first projects will be
to come up with a simple way of identifying the different models. We
are open to suggestions. The following is one plan that is based on the
current identifier system. Please send comments or suggestions
to: <a href="mailto:staff@bamca.org">staff@bamca.org</a><br>
<br>
</font>Numbering System Used in this Guide</font><br>
<br>
<font weight='bold' size='+2'>SSSNNNL-DDL</font><br>
<br>
Two or three letters representing the model Series (TP, CY, CCY, TM, TC, or DYM)<br>
Two or three Numbers followed by a Letter representing the Matchbox model number<br>
Two or three Digits followed by a Letter representing the different variations of that model<br>
<br>
<b><i><font color="#3333ff">Example:</font></i></b><br>
<br>
CY004A-01a - Scania box truck with white cab, white container, black
trailer with <font color="#ff6600">"Ansett" labels to the front</font>
<i><font color="#3366ff">(a documented variation)</font></i><br>
<br>
CY004A-02a - Scania box truck with white cab, white
container, black trailer with <font color="#ff6600">"Ansett" labels to
the rear</font> <font color="#3366ff"><i>(another documented
variation)</i><br>
</font><br>
<font color="#3333ff"> If we found and verified
the same model with one label to the front and the other label to the
rear it would be numbered as: </font><br>
<br>
CY-004-02b - Scania box truck with white cab, white
container, black trailer with <font color="#ff6600">one "Ansett"
labels to the front and the other label to the rear.</font> <font
 color="#3333ff">(a previously unreported variation)</font><br>
 <br>
<font color="#3333ff"> The variations that sets
these model apart from the other two models would be listed in a
contrasting color for easy identification.</font><br>
<br>
<a href="index.php"><font size="+1">RETURN TO INDEX</font></a><br>
</div>
</div>
</div>
</body>
</html>

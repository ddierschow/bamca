<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
include "subs.php";
$pif = GetPageInfo("convoy");
$desc = 'Semi Cabs';
$pif['title'] = $pif['title'] . ' - Semi Cabs';
DoHead($pif);
?>
  <meta name="author" content="John Baum and Dean Dierschow">
  <meta name="description" content="<?php echo $desc; ?>">
<?php
DoPageHeader($pif);
?>

The Matchbox Convoy Project - Basic Information<br>
<br>
<div align="center"><font size="+3" face="Arial">Truck Cabs<br>
<br>
</font>
<table border="7" cellspacing="5">
  <tbody>
    <tr>
      <td class="cabhead">Model #</td>
      <td class="cabhead">Standard Model</td>
      <td class="cabhead">Premiere &amp; Ultra Model</td>
      <td class="cabhead">Convoys</td>
    </tr>
    <tr>
      <td class="cabname bgwhite">MB-45C<br>Kenworth Cabover Aerodyne<br>Introduced 1982</td>
      <td class="cabcell bgwhite"><a href="/cgi-bin/single.cgi?id=MB045"><img src="/pic/man/s_mb045.jpg"></a></td>
      <td class="cabcell bgwhite"><a href="/cgi-bin/single.cgi?id=MB309"><img src="/pic/man/s_mb309.jpg"></a></td>
      <td class="cabcell bgwhite">
	<?php link_if_exists('CY001A'); ?><br>
	<?php link_if_exists('CY002A'); ?><br>
	<?php link_if_exists('CY003A'); ?><br>
	<?php link_if_exists('CY003B'); ?><br>
	<?php link_if_exists('CY007A'); ?><br>
	<?php link_if_exists('CY008A'); ?><br>
	<?php link_if_exists('CY009A'); ?><br>
	<?php link_if_exists('CY011A'); ?><br>
	<?php link_if_exists('CY012A'); ?><br>
	<?php link_if_exists('CY013A'); ?><br>
	<?php link_if_exists('CY014A'); ?><br>
	<?php link_if_exists('CY020A'); ?><br>
	<?php link_if_exists('CY038A'); ?><br>
	<?php link_if_exists('CY104A'); ?><br>
	<?php link_if_exists('CY105A'); ?><br>
	<?php link_if_exists('CY110A'); ?><br>
	<?php link_if_exists('TMTC', 'TC003A', 'TC003A'); ?><br>
	<?php link_if_exists('TMTC', 'TC005A', 'TC005A'); ?><br>
	<?php link_if_exists('TMTC', 'TC017A', 'TC017A'); ?><br>
        <?php link_if_exists('CCY', 'CCY03', 'CCY03'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgwhite"></td>
      <td class="cabname bgwhite">Man # 045</td>
      <td class="cabname bgwhite">Man # 309</td>
      <td class="cabname bgwhite"></td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite">MB-41D<br>Kenworth Aerodyne Conventional Cab<br>Introduced 1982</td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=MB103"><img src="/pic/man/s_mb103.jpg"></a></td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=MB310"><img src="/pic/man/s_mb310.jpg"></a></td>
      <td class="cabcell bgoffwhite">
	<?php link_if_exists('CY003A'); ?><br>
	<?php link_if_exists('CY004A'); ?><br>
	<?php link_if_exists('CY005A'); ?><br>
	<?php link_if_exists('CY006A'); ?><br>
	<?php link_if_exists('CY007A'); ?><br>
	<?php link_if_exists('CY008A'); ?><br>
	<?php link_if_exists('CY009A'); ?><br>
	<?php link_if_exists('CY036A'); ?><br>
	<?php link_if_exists('CY105A'); ?><br>
        <?php link_if_exists('CCY', 'CCY04', 'CCY04'); ?><br>
        <?php link_if_exists('CCY', 'CCY12', 'CCY12'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite"></td>
      <td class="cabname bgoffwhite">Man # 103</td>
      <td class="cabname bgoffwhite">Man # 310</td>
      <td class="cabname bgoffwhite"></td>
    </tr>
    <tr>
      <td class="cabname bgwhite">MB-43D<br>Peterbilt Conventional Sleeper Cab<br>Introduced 1982</td>
      <td class="cabcell bgwhite"><a href="/cgi-bin/single.cgi?id=MB106"><img src="/pic/man/s_mb106.jpg"></a></td>
      <td class="cabcell bgwhite"><a href="/cgi-bin/single.cgi?id=MB307"><img src="/pic/man/s_mb307.jpg"></a></td>
      <td class="cabcell bgwhite">
	<?php link_if_exists('CY003A'); ?><br>
	<?php link_if_exists('CY005A'); ?><br>
	<?php link_if_exists('CY007A'); ?><br>
	<?php link_if_exists('CY013A'); ?><br>
	<?php link_if_exists('CY015A'); ?><br>
	<?php link_if_exists('CY019A'); ?><br>
	<?php link_if_exists('CY034A'); ?><br>
	<?php link_if_exists('CY106A'); ?><br>
	<?php link_if_exists('CY106B'); ?><br>
	<?php link_if_exists('TMTC', 'TC001A', 'TC001A'); ?><br>
	<?php link_if_exists('TMTC', 'TC013A', 'TC013A'); ?><br>
        <?php link_if_exists('CCY', 'CCY01', 'CCY01'); ?><br>
	<?php link_if_exists('CCY', 'CCY06', 'CCY06'); ?><br>
        <?php link_if_exists('CCY', 'CCY09', 'CCY09'); ?><br>
	<?php link_if_exists('CCY', 'CCY14', 'CCY14'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgwhite"><br></td>
      <td class="cabname bgwhite">Man # 106</td>
      <td class="cabname bgwhite">Man # 307</td>
      <td class="cabname bgwhite"></td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite">Peterbilt Conventional Cab<br>Introduced 1984</td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=MI724"><img src="/pic/man/s_mi724.jpg"></a></td>
      <td class="cabcell bgoffwhite"></td>
      <td class="cabcell bgoffwhite">
	<?php link_if_exists('CY013A'); ?><br>
	<?php link_if_exists('CY203A'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite"><br></td>
      <td class="cabname bgoffwhite">Man # 724</td>
      <td class="cabname bgoffwhite"></td>
      <td class="cabname bgoffwhite"></td>
    </tr>
    <tr>
      <td class="cabname bgwhite">MB-08F<br>Scania T 142 Cab<br>Introduced 1985</td>
      <td class="cabcell bgwhite"><a href="/cgi-bin/single.cgi?id=MB147"><img src="/pic/man/s_mb147.jpg"></a></td>
      <td class="cabcell bgwhite"><a href="/cgi-bin/single.cgi?id=MB341"><img src="/pic/man/s_mb341.jpg"></a></td>
      <td class="cabcell bgwhite">
	<?php link_if_exists('CY004B'); ?><br>
	<?php link_if_exists('CY016A'); ?><br>
	<?php link_if_exists('CY017A'); ?><br>
	<?php link_if_exists('CY020A'); ?><br>
	<?php link_if_exists('CY021B'); ?><br>
	<?php link_if_exists('CY023A'); ?><br>
	<?php link_if_exists('CY104B'); ?><br>
	<?php link_if_exists('TMTC', 'TC002A', 'TC002A'); ?><br>
        <?php link_if_exists('CCY', 'CCY07', 'CCY07'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgwhite"><br></td>
      <td class="cabname bgwhite">Man # 147</td>
      <td class="cabname bgwhite">Man # 341</td>
      <td class="cabname bgwhite"><br></td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite">MB-15L<br>DAF 3300 Space Cab<br>Introduced 1999</td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=MB183"><img src="/pic/man/s_mb183.jpg"></a></td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=MB340"><img src="/pic/man/s_mb340.jpg"></a></td>
      <td class="cabcell bgoffwhite">
	<?php link_if_exists('CY007C'); ?><br>
	<?php link_if_exists('CY009A'); ?><br>
	<?php link_if_exists('CY018A'); ?><br>
	<?php link_if_exists('CY021A'); ?><br>
	<?php link_if_exists('CY022A'); ?><br>
	<?php link_if_exists('CY024A'); ?><br>
	<?php link_if_exists('CY025A'); ?><br>
	<?php link_if_exists('CY026A'); ?><br>
	<?php link_if_exists('CY108A'); ?><br>
	<?php link_if_exists('TMTC', 'TC004A', 'TC004A'); ?><br>
	<?php link_if_exists('TMTC', 'TC006A', 'TC006A'); ?><br>
	<?php link_if_exists('TMTC', 'TC014A', 'TC014A'); ?><br>
	<?php link_if_exists('TMTC', 'TC015A', 'TC015A'); ?><br>
	<?php link_if_exists('TMTC', 'TC016A', 'TC016A'); ?><br>
        <?php link_if_exists('CCY', 'CCY08', 'CCY08'); ?><br>
        <?php link_if_exists('CCY', 'CCY13', 'CCY13'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite"><br></td>
      <td class="cabname bgoffwhite">Man # 183</td>
      <td class="cabname bgoffwhite">Man # 340</td>
      <td class="cabname bgoffwhite"><br></td>
    </tr>
    <tr>
      <td class="cabname bgwhite">MB-54S<br>DAF XB95 Space Cab<br>Introduced 2007</td>
      <td class="cabcell bgwhite"><a href="/cgi-bin/single.cgi?id=MB702"><img src="/pic/man/s_mb702.jpg"></a></td>
      <td class="cabcell bgwhite"></td>
      <td class="cabcell bgwhite">
      </td>
    </tr>
    <tr>
      <td class="cabname bgwhite"><br></td>
      <td class="cabname bgwhite">Man # 702</td>
      <td class="cabname bgwhite"></td>
      <td class="cabname bgwhite"><br></td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite">MB-08H<br>Mack CH 600 Cab<br>Introduced 1990</td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=MB202"><img src="/pic/man/s_mb202.jpg"></a></td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=MB311"><img src="/pic/man/s_mb311.jpg"></a></td>
      <td class="cabcell bgoffwhite">
	<?php link_if_exists('CY027A'); ?><br>
	<?php link_if_exists('CY028A'); ?><br>
	<?php link_if_exists('CY029A'); ?><br>
	<?php link_if_exists('CY031A'); ?><br>
	<?php link_if_exists('CY032A'); ?><br>
	<?php link_if_exists('CY033A'); ?><br>
	<?php link_if_exists('CY035A'); ?><br>
	<?php link_if_exists('CY107A'); ?><br>
	<?php link_if_exists('TMTC', 'TC018A', 'TC018A'); ?><br>
        <?php link_if_exists('CCY', 'CCY05', 'CCY05'); ?><br>
        <?php link_if_exists('CCY', 'CCY11', 'CCY11'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite"><br></td>
      <td class="cabname bgoffwhite">Man # 202</td>
      <td class="cabname bgoffwhite">Man # 311</td>
      <td class="cabname bgoffwhite"><br></td>
      </td>
    </tr>
    <tr>
      <td class="cabname bgwhite">Ford Aeromax Cab<br>Introduced 1992</td>
      <td class="cabcell bgwhite"><a href="/cgi-bin/single.cgi?id=MB214"><img src="/pic/man/s_mb214.jpg"></a></td>
      <td class="cabcell bgwhite"><a href="/cgi-bin/single.cgi?id=MB308"><img src="/pic/man/s_mb308.jpg"></a></td>
      <td class="cabcell bgwhite">
	<?php link_if_exists('CY018B'); ?><br>
	<?php link_if_exists('CY037A'); ?><br>
	<?php link_if_exists('CY039A'); ?><br>
	<?php link_if_exists('CY109A'); ?><br>
	<?php link_if_exists('CY113A'); ?><br>
        <?php link_if_exists('CCY', 'CCY02', 'CCY02'); ?><br>
        <?php link_if_exists('CCY', 'CCY10', 'CCY10'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgwhite"><br></td>
      <td class="cabname bgwhite">Man # 214</td>
      <td class="cabname bgwhite">Man # 308</td>
      <td class="cabname bgwhite"><br></td>
      </td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite">MB-64J<br>Mercedes Actros 1857 Cab<br>Introduced 1999</td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=MB425"><img src="/pic/man/s_mb425.jpg"></a></td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=MB425"><img src="/pic/set/convoy/s_mb425p.jpg"></a></td>
      <td class="cabcell bgoffwhite">
	<?php link_if_exists('CY009C'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite"><br></td>
      <td class="cabname bgoffwhite">Man # 425</td>
      <td class="cabname bgoffwhite">Man # 425 w/upgraded tires</td>
      <td class="cabname bgoffwhite"><br></td>
    </tr>
    <tr>
      <td class="cabname bgwhite">Mercedes Actros 1857 Cab<br>Introduced 2007</td>
      <td class="cabcell bgwhite"><a href="/cgi-bin/single.cgi?id=MB725"><img src="/pic/man/s_mb725.jpg"></a></td>
      <td class="cabcell bgwhite"></td>
      <td class="cabcell bgwhite">
	<?php link_if_exists('CY121A'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgwhite"><br></td>
      <td class="cabname bgwhite">Man # 725</td>
      <td class="cabname bgwhite"></td>
      <td class="cabname bgwhite"><br></td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite">MB-13G<br>Kenworth T2000 Cab<br>Introduced 1999</td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=MB432"><img src="/pic/man/s_mb432.jpg"></a></td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=MB318"><img src="/pic/man/s_mb318.jpg"></a></td>
      <td class="cabcell bgoffwhite">
	<?php link_if_exists('CY002B'); ?><br>
	<?php link_if_exists('CY009B'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite"><br></td>
      <td class="cabname bgoffwhite">Man # 432</td>
      <td class="cabname bgoffwhite">Man # 318</td>
      <td class="cabname bgoffwhite"><br></td>
    </tr>
    <tr>
      <td class="cabname bgwhite">MB-31R<br>Generic Tractor Cab<br>Introduced 2005</td>
      <td class="cabcell bgwhite"><a href="/cgi-bin/single.cgi?id=MB664"><img src="/pic/man/s_mb664.jpg"></a></td>
      <td class="cabcell bgwhite"></td>
      <td class="cabcell bgwhite">
	<?php link_if_exists('CY114A'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite"></td>
      <td class="cabname bgoffwhite">Man # 664</td>
      <td class="cabname bgoffwhite"></td>
      <td class="cabname bgoffwhite"><br></td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite">Kenworth T600 Cab<br>Introduced 1994</td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=CY112"><img src="/pic/man/s_cy112.jpg"></a></td>
      <td class="cabcell bgoffwhite"></td>
      <td class="cabcell bgoffwhite">
	<?php link_if_exists('CY112A'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite"><br></td>
      <td class="cabname bgoffwhite"></td>
      <td class="cabname bgoffwhite"></td>
      <td class="cabname bgoffwhite"><br></td>
    </tr>
    <tr>
      <td colspan="4" class="cabhead">TP-900 Long Haul Cabs</td>
    </tr>
    <tr>
      <td class="cabname bgwhite">Peterbilt Conventional Cab<br>Introduced 1979</td>
      <td class="cabcell bgwhite"><a href="/cgi-bin/single.cgi?id=T9CC"><img src="/pic/man/s_t9cc.jpg"></a></td>
      <td class="cabcell bgwhite"></td>
      <td class="cabcell bgwhite">
	<?php link_if_exists('TP022A'); ?><br>
	<?php link_if_exists('TP024A'); ?><br>
	<?php link_if_exists('TP025A'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite"><br></td>
      <td class="cabname bgoffwhite">T9CC</td>
      <td class="cabname bgoffwhite"></td>
      <td class="cabname bgoffwhite"><br></td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite">Leyland Cabover<br>Introduced 1981</td>
      <td class="cabcell bgoffwhite"><a href="/cgi-bin/single.cgi?id=T9CO"><img src="/pic/man/s_t9co.jpg"></a></td>
      <td class="cabcell bgoffwhite"></td>
      <td class="cabcell bgoffwhite">
	<?php link_if_exists('TP002C'); ?><br>
	<?php link_if_exists('TP026A'); ?><br>
      </td>
    </tr>
    <tr>
      <td class="cabname bgoffwhite"><br></td>
      <td class="cabname bgoffwhite">T9CO</td>
      <td class="cabname bgoffwhite"></td>
      <td class="cabname bgoffwhite"></td>
    </tr>
  </tbody>
</table>
<font size="+3"><font face="Arial"><br>
<a href="index.php">Return to Index</a><br>
</font></font></div>
<?php DoFoot($pif); ?>
</html>

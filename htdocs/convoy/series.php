<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
include "subs.php";
$pif = GetPageInfo("convoy");
$desc = 'Cab and Trailer Cross-Reference';
$pif['title'] = $pif['title'] . ' - ' . $desc;
DoHead($pif);
?>
  <meta name="author" content="John Baum and Dean Dierschow">
  <meta name="description" content="<?php echo $desc; ?>">
<?php
DoPageHeader($pif);
?>

The Matchbox Convoy Project - Series Index

<div class="title"><span class="titletext">Picture Cross Reference</span></div>
<table class="seriestable">
  <tbody>
    <tr>
      <td class="serieshead ids0" rowspan="2"><img src="/pic/set/convoy/series_ul.gif"></td>
      <td class="serieshead ids1"><img src="/pic/man/t_mb425.jpg" width="60" height="36"><br>MB425<br>MB725</td>
      <td class="serieshead ids0"><img src="/pic/man/t_mb183.jpg" width="60" height="36"><br>MB183<br>MB340</td>
      <td class="serieshead ids1"><img src="/pic/man/t_mb702.jpg" width="60" height="36"><br>MB702</td>
      <td class="serieshead ids0"><img src="/pic/man/t_mb214.jpg" width="60" height="36"><br>MB214<br>MB308</td>
      <td class="serieshead ids1"><img src="/pic/man/t_mb045.jpg" width="60" height="36"><br>MB045<br>MB309</td>
      <td class="serieshead ids0"><img src="/pic/man/t_mb103.jpg" width="60" height="36"><br>MB103<br>MB310</td>
      <td class="serieshead ids1"><img src="/pic/man/t_mb432.jpg" width="60" height="36"><br>MB432<br>MB318</td>
      <td class="serieshead ids0"><img src="/pic/man/t_t9co.jpg"  width="60" height="36"><br>T9CO</td>
      <td class="serieshead ids1"><img src="/pic/man/t_mb202.jpg" width="60" height="36"><br>MB202<br>MB311</td>
      <td class="serieshead ids0"><img src="/pic/man/t_mb106.jpg" width="60" height="36"><br>MB106<br>MB307</td>
      <td class="serieshead ids1"><img src="/pic/man/t_mi724.jpg" width="60" height="36"><br>MI724</td>
      <td class="serieshead ids0"><img src="/pic/man/t_t9cc.jpg"  width="60" height="36"><br>T9CC</td>
      <td class="serieshead ids1"><img src="/pic/man/t_mb147.jpg" width="60" height="36"><br>MB147<br>MB341</td>
      <td class="serieshead ids0"><img src="/pic/man/t_mb664.jpg" width="60" height="36"><br>MB664</td>
    </tr>
    <tr>
      <td class="serieshead ids1">Mercedes<br>Actros</td>
      <td class="serieshead ids0">DAF<br>3300</td>
      <td class="serieshead ids1">DAF<br>FX95</td>
      <td class="serieshead ids0">Ford<br>Aeromax</td>
      <td class="serieshead ids1">Kenworth<br>COE</td>
      <td class="serieshead ids0">Kenworth<br>Conv</td>
      <td class="serieshead ids1">Kenworth<br>T2000</td>
      <td class="serieshead ids0">Leyland<br>COE</td>
      <td class="serieshead ids1">Mack<br>CH 600</td>
      <td class="serieshead ids0">Peterbilt<br>Conv</td>
      <td class="serieshead ids1">Peterbilt<br>Emerg.</td>
      <td class="serieshead ids0">Peterbilt<br>Long Haul</td>
      <td class="serieshead ids1">Scania<br>T142</td>
      <td class="serieshead ids0">Tractor<br>Cab</td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt12.jpg"><br>Airplane </td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolD3"><?php link_if_exists('CY021A'); ?><br><?php link_if_exists('CY108A'); ?><br>(modified)</td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY012A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolMA"><?php link_if_exists('CY029A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolSC"><?php link_if_exists('CY021B'); ?></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0"><img src="/pic/man/t_cyt14.jpg"><br>Boat</td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolD3"><?php link_if_exists('CY022A'); ?><br><?php link_if_exists('TMTC', 'TC006A', 'TC006A'); ?><br><?php link_if_exists('TMTC', 'TC016A', 'TC016A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY014A'); ?></td>
      <td class="seriesempty">see<br>Low Boy</td>
      <td class="seriesempty"></td>
      <td class="seriesempty">see<br>Low Boy</td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt04.jpg"><br>Box</td>
      <td class="seriesent seriescolAC"><?php link_if_exists('CY009C'); ?></td>
      <td class="seriesent seriescolD3"><?php link_if_exists('CY009A'); ?><br><?php link_if_exists('CY025A'); ?><br><?php link_if_exists('TMTC', 'TC004A', 'TC004A'); ?><br><?php link_if_exists('TMTC', 'TC013A', 'TC013A'); ?><br><?php link_if_exists('TMTC', 'TC015A', 'TC015A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolFA"><?php link_if_exists('CY039A'); ?></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY003B'); ?><br><?php link_if_exists('CY008A'); ?><br><?php link_if_exists('CY009A'); ?></td>
      <td class="seriesent seriescolKC"><?php link_if_exists('CY008A'); ?><br><?php link_if_exists('CY009A'); ?></td>
      <td class="seriesent seriescolKT"><?php link_if_exists('CY009B'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolMA"><?php link_if_exists('CY027A'); ?></td>
      <td class="seriesent seriescolPC"><?php link_if_exists('CY019A'); ?><br><?php link_if_exists('CY106B'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolPL"><?php link_if_exists('TP024A'); ?></td>
      <td class="seriesent seriescolSC"><?php link_if_exists('CY004B'); ?><br><?php link_if_exists('CY016A'); ?></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0"><img src="/pic/man/t_cyt03.jpg"><br>Covered</td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolKC"><?php link_if_exists('CY005A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolPC"><?php link_if_exists('CY005A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolPL"><?php link_if_exists('TP023A'); ?></td>
      <td class="seriesent seriescolSC"><?php link_if_exists('CY023A'); ?></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt02.jpg"><br><div align="center">Double Cont<br></div></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolD3"><?php link_if_exists('CY026A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolFA"><?php link_if_exists('CY018B'); ?></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY003A'); ?> </td>
      <td class="seriesent seriescolKC"><?php link_if_exists('CY003A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolMA"><?php link_if_exists('CY028A'); ?><br><?php link_if_exists('TMTC', 'TC018A', 'TC018A'); ?></td>
      <td class="seriesent seriescolPC"><?php link_if_exists('CY003A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolPL"><?php link_if_exists('TP022A'); ?></td>
      <td class="seriesent seriescolSC"><?php link_if_exists('CY018A'); ?></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0"><img src="/pic/man/t_cyt13.jpg"><br>Fire Ladder</td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY013A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolPC"><?php link_if_exists('CY013A'); ?></td>
      <td class="seriesent seriescolPE"><?php link_if_exists('CY013A'); ?><br><?php link_if_exists('TMTC', 'TC001A', 'TC001A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt28.jpg"><br><div align="center">Fishbelly<br></div></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolDS"><?php link_if_exists('CY120A'); ?> </td>
      <td class="seriesent seriescolFA"><?php link_if_exists('CY115A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolTC"><?php link_if_exists('CY114A'); ?></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0"><img src="/pic/man/t_cyt30.jpg"><br><div style="text-align: center;">Flatbed V2<br></div></td>
      <td class="seriesent seriescolAC"><?php link_if_exists('CY121A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolDS"><?php link_if_exists('CY122A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolTC"><?php link_if_exists('CY119A'); ?></td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt07.jpg"><br>Low Boy</td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY002A'); ?><br>w/ shuttle<br><?php link_if_exists('CY011A'); ?><br>w/ heli</td>
      <td class="seriesent seriescolKC"><?php link_if_exists('CY004A'); ?><br>with<br>boat</td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolLY"><?php link_if_exists('TP026A'); ?><br>with<br>boat</td>
      <td class="seriesent seriescolMA"><?php link_if_exists('CY032A'); ?><br>with<br>shovel</td>
      <td class="seriesent seriescolPC"><?php link_if_exists('CY032B'); ?><br>with<br>bulldozer</td>
      <td class="seriesent seriescolPE"><?php link_if_exists('CY203A'); ?><br>with<br>excavator</td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolSC"><?php link_if_exists('CY803A'); ?><br>with<br>cargo truck</td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0"><img src="/pic/man/t_cyt05.jpg"><br>Pipe Trailer</td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolMA"><?php link_if_exists('CY031A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolPL"><?php link_if_exists('TP025A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt10.jpg"><br>Rocket</td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY002A'); ?><br><?php link_if_exists('TMTC', 'TC005A', 'TC005A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolKT"><?php link_if_exists('CY002B'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0"><img src="/pic/man/t_cyt18.jpg"><br>Superstar</td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolFA"><?php link_if_exists('CY109A'); ?><br><?php link_if_exists('CY113A'); ?></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY110A'); ?></td>
      <td class="seriesent seriescolKC"><?php link_if_exists('CY104A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolMA"><?php link_if_exists('CY107A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolSC"><?php link_if_exists('CY104B'); ?></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt06.jpg"><br>Tanker</td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolD3"><?php link_if_exists('CY007C'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolFA"><?php link_if_exists('CY007B'); ?></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY007A'); ?><br><?php link_if_exists('CY105A'); ?></td>
      <td class="seriesent seriescolKC"><?php link_if_exists('CY007A'); ?><br><?php link_if_exists('CY105A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolLY"><?php link_if_exists('TP002C'); ?></td>
      <td class="seriesent seriescolMA"><?php link_if_exists('CY035A'); ?></td>
      <td class="seriesent seriescolPC"><?php link_if_exists('CY007A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolSC"><?php link_if_exists('CY017A'); ?><br><?php link_if_exists('TMTC', 'TC002A', 'TC002A'); ?></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0"><img src="/pic/man/t_cyt29.jpg"><br>Tanker V.2<br> </td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolDS"><?php link_if_exists('CY118A'); ?></td>
      <td class="seriesent seriescolFA"><?php link_if_exists('CY116A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolTC"><?php link_if_exists('CY117A'); ?></td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt16.jpg"><br>Tipper</td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY020A'); ?><br><?php link_if_exists('TMTC', 'TC003A', 'TC003A'); ?><br><?php link_if_exists('TMTC', 'TC017A', 'TC017A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolPC"><?php link_if_exists('CY106A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolSC"><?php link_if_exists('CY020A'); ?></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0"><img src="/pic/man/t_cyt17.jpg"><br>Transporter</td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolD3"><?php link_if_exists('CY024A'); ?><br><?php link_if_exists('TMTC', 'TC014A', 'TC014A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolFA"><?php link_if_exists('CY037A'); ?></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY038A'); ?></td>
      <td class="seriesent seriescolKC"><?php link_if_exists('CY036A'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriestable description" colspan="15">Collectible Convoy Trailers</td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt22.jpg"><br>Ultra Box</td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolD3"><?php link_if_exists('CCY', 'CCY08', 'CCY08'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolFA"><?php link_if_exists('CCY', 'CCY02', 'CCY02'); ?></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CCY', 'CCY03', 'CCY03'); ?></td>
      <td class="seriesent seriescolKC"><?php link_if_exists('CCY', 'CCY04', 'CCY04'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolMA"><?php link_if_exists('CCY', 'CCY05', 'CCY05'); ?></td>
      <td class="seriesent seriescolPC"><?php link_if_exists('CCY', 'CCY01', 'CCY01'); ?><br><?php link_if_exists('CCY', 'CCY06', 'CCY06'); ?><br><?php link_if_exists('CCY', 'CCY14', 'CCY14'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolSC"><?php link_if_exists('CCY', 'CCY07', 'CCY07'); ?></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0"><img src="/pic/man/t_cyt23.jpg"><br>Ultra Tanker</td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolD3"><?php link_if_exists('CCY', 'CCY13', 'CCY13'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolFA"><?php link_if_exists('CCY', 'CCY10', 'CCY10'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolKC"><?php link_if_exists('CCY', 'CCY12', 'CCY12'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesent seriescolMA"><?php link_if_exists('CCY', 'CCY11', 'CCY11'); ?></td>
      <td class="seriesent seriescolPC"><?php link_if_exists('CCY', 'CCY09', 'CCY09'); ?></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
      <td class="seriesempty"></td>
    </tr>
    <tr>
      <td></td>
      <td class="serieshead"><img src="/pic/man/t_mb425.jpg" width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_mb183.jpg" width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_mb702.jpg" width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_mb214.jpg" width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_mb045.jpg" width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_mb103.jpg" width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_mb432.jpg" width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_t9co.jpg"  width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_mb202.jpg" width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_mb106.jpg" width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_mi724.jpg" width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_t9cc.jpg"  width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_mb147.jpg" width="60" height="36"></td>
      <td class="serieshead"><img src="/pic/man/t_mb664.jpg" width="60" height="36"></td>
    </tr>
  </tbody>
</table>
<p>

<table class="seriestable"><tr><td valign="top" width="270">
<table class="seriestable">
  <tbody>
    <tr>
      <td colspan="3">
<div class="description">Cabs with limited use</div>
      </td>
    </tr>
    <tr>
      <td class="seriescol00 ids1" colspan="2"><img src="/pic/man/t_cy010.jpg"><br><font face="Arial Narrow">Racing Transporter</font></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY010A'); ?><br><?php link_if_exists('CY111A'); ?>
      <br><?php link_if_exists('TMTC', 'TM/TC'); ?></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0" colspan="2"><img src="/pic/man/t_cy030.jpg" border="2"><br><font face="Arial Narrow">Grove Crane</font></td>
      <td class="seriesent seriescolTC"><?php link_if_exists('CY030A'); ?></td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cy112.jpg" width="60" height="36"><br>CY112</td>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt17.jpg"><br>Transporter</td>
      <td class="seriesent seriescolKT"><?php link_if_exists('CY112A'); ?></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0" colspan="2"><img src="/pic/man/t_cy047.jpg" border="2"><br><font face="Arial Narrow">MCI Coach</font></td>
      <td class="seriesent seriescolMC"><?php link_if_exists('CY047A'); ?></td>
    </tr>
  </tbody>
</table>
</td>

<td valign="top" width="270">
<table class="seriestable">
  <tbody>
    <tr>
      <td colspan="3">
<div class="description">Trailers with limited use</div>
      </td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_mb045.jpg" width="60" height="36"><br>MB045</td>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt09.jpg"><br>Automobile</td>
      <td class="seriesent seriescolKO"><?php link_if_exists('CY001A'); ?></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0"><img src="/pic/man/t_mb106.jpg" width="60" height="36"><br>MB106</td>
      <td class="seriescol00 ids0"><img src="/pic/man/t_cyt20.jpg"><br>Emergency</td>
      <td class="seriesent seriescolPC"><?php link_if_exists('CY034A'); ?></td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_mb202.jpg" width="60" height="36"><br>MB202</td>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt21.jpg"><br>Helicopter</td>
      <td class="seriesent seriescolMA"><?php link_if_exists('CY033A'); ?></td>
    </tr>
    <tr>
      <td class="seriescol00 ids0"><img src="/pic/man/t_mb103.jpg" width="60" height="36"><br>MB103</td>
      <td class="seriescol00 ids0"><img src="/pic/man/t_cyt11.jpg"><br>Horse Box</td>
      <td class="seriesent seriescolKC"><?php link_if_exists('CY006A'); ?></td>
    </tr>
    <tr>
      <td class="seriescol00 ids1"><img src="/pic/man/t_mb106.jpg" width="60" height="36"><br>MB106</td>
      <td class="seriescol00 ids1"><img src="/pic/man/t_cyt15.jpg"><br>Tracking</td>
      <td class="seriesent seriescolPC"><?php link_if_exists('CY015A'); ?>
</td>
    </tr>
  </tbody>
</table>
</td>

<td valign="top" width="270">
<table class="seriestable">
  <tbody>
    <tr>
      <td colspan="3">
<div class="description">Team Matchbox and Team Convoy</div>
      </td>
    </tr>
    <tr>
      <td colspan="3">
Team Matchbox packaged various Convoys with other models starting in 1985.
This line was renamed Team Convoy in 1988.
      </td>
    </tr>
    <tr>
      <td class="seriescol00 ids1" colspan="2"><img src="/pic/man/t_cy010.jpg"><br><font face="Arial Narrow">Racing Transporter</font></td>
      <td class="seriesent seriescolKO"><?php link_if_exists('TMTC', 'TM/TC'); ?><br>(many)</td>
    </tr>
    <tr>
      <td class="seriescol00 ids0" width="100">
Other cab/trailer combinations
</td>
      <td class="seriesent ids1" colspan="2">
<?php link_if_exists('TMTC', 'TC001A includes CY013A', 'TC001A'); ?><br>
<?php link_if_exists('TMTC', 'TC002A includes CY017A', 'TC002A'); ?><br>
<?php link_if_exists('TMTC', 'TC003A includes CY020A', 'TC003A'); ?><br>
<?php link_if_exists('TMTC', 'TC004A includes CY025A', 'TC004A'); ?><br>
<?php link_if_exists('TMTC', 'TC005A includes CY002A', 'TC005A'); ?><br>
<?php link_if_exists('TMTC', 'TC006A includes CY022A', 'TC006A'); ?><br>
<?php link_if_exists('TMTC', 'TC013A includes CY015A', 'TC013A'); ?><br>
<?php link_if_exists('TMTC', 'TC014A includes CY024A', 'TC014A'); ?><br>
<?php link_if_exists('TMTC', 'TC015A includes CY025A', 'TC015A'); ?><br>
<?php link_if_exists('TMTC', 'TC016A includes CY022A', 'TC016A'); ?><br>
<?php link_if_exists('TMTC', 'TC017A includes CY020A', 'TC017A'); ?><br>
<?php link_if_exists('TMTC', 'TC018A includes CY028A', 'TC018A'); ?><br>
</td>
    </tr>
  </tbody>
</table>
</td></tr></table>

<br>
<font face="Arial" size="+1"><a href="index.php">Return to Front Page</a></font><br>
<?php DoFoot($pif); ?>
</html>

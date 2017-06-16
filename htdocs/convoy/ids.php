<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("convoy");
$pif['title'] = $pif['title'] . ' - Index by ID';
$desc = 'Index by ID';
DoHead($pif);
?>
  <meta name="author" content="John Baum and Dean Dierschow">
  <meta name="description" content="<?php echo $desc; ?>">
<?php
DoPageHeader($pif);
?>

The Matchbox Convoy Project - ID Index

<table class="seriestable">
  <tbody>
    <tr class="idsh">
      <th>ID</th>
      <th>Convoy Name</th>
      <th>Year</th>
      <th>Cab(s)</th>
      <th>Trailer</th>
      <th>Notes</th>
    </tr>
<?php

$entries = [
    ['i' => 'CCY01', 'r' => 'CCY', 'h' => 'CCY01', 'n' => 'Peterbilt Container Truck', 'y' => '1997', 'c' => ['MB307'], 't' => 'Ultra Container',],
    ['i' => 'CCY02', 'r' => 'CCY', 'h' => 'CCY02', 'n' => 'Ford Aeromax Container Truck', 'y' => '1997', 'c' => ['MB308'], 't' => 'Ultra Container',],
    ['i' => 'CCY03', 'r' => 'CCY', 'h' => 'CCY03', 'n' => 'Kenworth Container Truck', 'y' => '1997', 'c' => ['MB309'], 't' => 'Ultra Container',],
    ['i' => 'CCY04', 'r' => 'CCY', 'h' => 'CCY04', 'n' => 'Kenworth Container Truck', 'y' => '1997', 'c' => ['MB310'], 't' => 'Ultra Container',],
    ['i' => 'CCY05', 'r' => 'CCY', 'h' => 'CCY05', 'n' => 'Mack Container Truck', 'y' => '1997', 'c' => ['MB311'], 't' => 'Ultra Container',],
    ['i' => 'CCY06', 'r' => 'CCY', 'h' => 'CCY06', 'n' => 'Peterbilt Container Truck', 'y' => '1997', 'c' => ['MB307'], 't' => 'Ultra Container',],
    ['i' => 'CCY07', 'r' => 'CCY', 'h' => 'CCY07', 'n' => 'Scania Container Truck', 'y' => '1998', 'c' => ['MB341'], 't' => 'Ultra Container',],
    ['i' => 'CCY08', 'r' => 'CCY', 'h' => 'CCY08', 'n' => 'DAF Container Truck', 'y' => '1998', 'c' => ['MB340'], 't' => 'Ultra Container',],
    ['i' => 'CCY09', 'r' => 'CCY', 'h' => 'CCY09', 'n' => 'Peterbilt Tanker ', 'y' => '1998', 'c' => ['MB307'], 't' => 'Ultra Tanker',],
    ['i' => 'CCY10', 'r' => 'CCY', 'h' => 'CCY10', 'n' => 'Ford Aeromax Tanker', 'y' => '1998', 'c' => ['MB308'], 't' => 'Ultra Tanker',],
    ['i' => 'CCY11', 'r' => 'CCY', 'h' => 'CCY11', 'n' => 'Mack Tanker', 'y' => '1998', 'c' => ['MB311'], 't' => 'Ultra Tanker',],
    ['i' => 'CCY12', 'r' => 'CCY', 'h' => 'CCY12', 'n' => 'Kenworth Tanker', 'y' => '1998', 'c' => ['MB310'], 't' => 'Ultra Tanker',],
    ['i' => 'CCY13', 'r' => 'CCY', 'h' => 'CCY13', 'n' => 'DAF Tanker', 'y' => '1998', 'c' => ['MB340'], 't' => 'Ultra Tanker',],
    ['i' => 'CCY14', 'r' => 'CCY', 'h' => 'CCY14', 'n' => 'Peterbilt Box Truck', 'y' => '1999', 'c' => ['MB307'], 't' => 'Ultra Container',],
    ['i' => 'CY001A', 'c' => ['MB045'], 't' => 'Car Transporter', 'y' => '1982', 'n' => 'Kenworth Car Transporter',],
    ['i' => 'CY002A', 'c' => ['MB045'], 't' => 'Low Loader with Space Shuttle<br>Rocket Transporter', 'y' => '1982', 'n' => 'Kenworth Rocket Transporter',],
    ['i' => 'CY002B', 'c' => ['MB432'], 't' => 'Rocket Transporter', 'y' => '1999', 'n' => 'Kenworth T-2000 Rocket Transporter', 'm' => 'Rest of World',],
    ['i' => 'CY003A', 'c' => ['MB045','MB103','MB106','MB310'], 't' => 'Double Container', 'y' => '1982', 'n' => 'Double Container Truck',],
    ['i' => 'CY003B', 'c' => ['MB045'], 't' => 'Box', 'y' => '1985', 'n' => 'Kenworth Box Truck', 'm' => 'Australia',],
    ['i' => 'CY004A', 'c' => ['MB103'], 't' => 'Lowboy with Boat', 'y' => '1982', 'n' => 'Kenworth Boat Transporter',],
    ['i' => 'CY004B', 'c' => ['MB147'], 't' => 'Box', 'y' => '1985', 'n' => 'Scania Box Truck', 'm' => 'Australia',],
    ['i' => 'CY005A', 'c' => ['MB103','MB106'], 't' => 'Covered', 'y' => '1982', 'n' => 'Peterbilt Covered Truck',],
    ['i' => 'CY006A', 'c' => ['MB103'], 't' => 'Horse Box', 'y' => '1982', 'n' => 'Kenworth Horse Box',],
    ['i' => 'CY007A', 'c' => ['MB045','MB103','MB106','MB307'], 't' => 'Tanker', 'y' => '1982', 'n' => 'Peterbilt Gas Tanker',],
    ['i' => 'CY007B', 'c' => ['MB308'], 't' => 'Tanker', 'y' => '1998', 'n' => 'Ford Aeromax Gas Tanker',],
    ['i' => 'CY007C', 'c' => ['MB183'], 't' => 'Tanker', 'y' => '2001', 'n' => 'DAF Gas Tanker', 'm' => 'Rest of World',],
    ['i' => 'CY008A', 'c' => ['MB045','MB103'], 't' => 'Box', 'y' => '1982', 'n' => 'Kenworth Box Truck',],
    ['i' => 'CY009A', 'c' => ['MB045','MB103','MB183','MB310'], 't' => 'Box', 'y' => '1982', 'n' => 'Kenworth Box Truck',],
    ['i' => 'CY009B', 'c' => ['MB318','MB432'], 't' => 'Box', 'y' => '2000', 'n' => 'Kenworth T2000 Container Truck',],
    ['i' => 'CY009C', 'c' => ['MB425'], 't' => 'Box', 'y' => '2001', 'n' => 'Mercedes Benz Actross Container Truck',],
    ['i' => 'CY010A', 'c' => ['CY010'], 't' => 'Racing transporter', 'y' => '1983', 'n' => 'Racing Transporter',],
    ['i' => 'CY011A', 'c' => ['MB045'], 't' => 'Helicopter Transporter', 'y' => '1983', 'n' => 'Kenworth Helicopter Transporter',],
    ['i' => 'CY012A', 'c' => ['MB045'], 't' => 'Airplane transporter', 'y' => '1984', 'n' => 'Kenworth Plane Transporter',],
    ['i' => 'CY013A', 'c' => ['MB045','MB106','MI724'], 't' => 'Fire Ladder', 'y' => '1984', 'n' => 'Peterbilt Fire Engine',],
    ['i' => 'CY014A', 'c' => ['MB045'], 't' => 'Boat transporter', 'y' => '1985', 'n' => 'Kenworth Boat Transporter',],
    ['i' => 'CY015A', 'c' => ['MB106'], 't' => 'Tracking', 'y' => '1985', 'n' => 'Peterbilt Tracking Vehicle',],
    ['i' => 'CY016A', 'c' => ['MB147','MB341'], 't' => 'Box', 'y' => '1985', 'n' => 'Scania Box Truck',],
    ['i' => 'CY017A', 'c' => ['MB147'], 't' => 'Tanker', 'y' => '1985', 'n' => 'Scania Petrol Tanker',],
    ['i' => 'CY018A', 'c' => ['MB147'], 't' => 'Double Container', 'y' => '1986', 'n' => 'Scania Double Container Truck',],
    ['i' => 'CY018B', 'c' => ['MB214','MB308'], 't' => 'Box', 'y' => '1993', 'n' => 'Ford Aeromax Double Container Truck',],
    ['i' => 'CY019A', 'c' => ['MB106'], 't' => 'Box', 'y' => '1987', 'n' => 'Peterbilt Box Truck',],
    ['i' => 'CY020A', 'c' => ['MB045','MB147'], 't' => 'Tipper', 'y' => '1987', 'n' => 'Articulated Dump Truck',],
    ['i' => 'CY021A', 'c' => ['MB183'], 't' => 'Airplane Transporter', 'y' => '1987', 'n' => 'DAF Aircraft Transporter',],
    ['i' => 'CY021B', 'c' => ['MB147'], 't' => 'Airplane Transporter', 'y' => '2000', 'n' => 'Scania Plane Transporter',],
    ['i' => 'CY022A', 'c' => ['MB183'], 't' => 'Boat Transporter', 'y' => '1987', 'n' => 'Boat Transporter',],
    ['i' => 'CY023A', 'c' => ['MB147'], 't' => 'Covered Trailer', 'y' => '1988', 'n' => 'Scania Covered Truck',],
    ['i' => 'CY024A', 'c' => ['MB183'], 't' => 'Racing Transporter', 'y' => '1988', 'n' => 'DAF Box Truck',],
    ['i' => 'CY025A', 'c' => ['MB183','MB340'], 't' => 'Box', 'y' => '1989', 'n' => 'DAF Container Truck',],
    ['i' => 'CY026A', 'c' => ['MB183'], 't' => 'Double Container', 'y' => '1989', 'n' => 'DAF Double Container Truck',],
    ['i' => 'CY027A', 'c' => ['MB202','MB311'], 't' => 'Box', 'y' => '1990', 'n' => 'Mack Container Truck',],
    ['i' => 'CY028A', 'c' => ['MB202'], 't' => 'Double Container', 'y' => '1990', 'n' => 'Mack Double Container Truck',],
    ['i' => 'CY029A', 'c' => ['MB202'], 't' => 'Aircraft Transporter', 'y' => '1991', 'n' => 'Mack Aircraft Transporter',],
    ['i' => 'CY030A', 'c' => ['CY030'], 't' => 'Crane', 'y' => '1992', 'n' => 'Grove Crane',],
    ['i' => 'CY031A', 'c' => ['MB202'], 't' => 'Pipe', 'y' => '1992', 'n' => 'Mack Pipe Truck',],
    ['i' => 'CY032A', 'c' => ['MB202'], 't' => 'Lowboy with Shovel Nose Tractor', 'y' => '1992', 'n' => 'Mack Shovel Transporter',],
    ['i' => 'CY032B', 'c' => ['MB307'], 't' => 'Lowboy with Bulldozer', 'y' => '1998', 'n' => 'Peterbilt Lowloader w/Bulldozer',],
    ['i' => 'CY033A', 'c' => ['MB202'], 't' => 'Helicopter Transporter', 'y' => '1992', 'n' => 'Mack Helicopter Transporter',],
    ['i' => 'CY034A', 'c' => ['MB106'], 't' => 'Emergency Center', 'y' => '1992', 'n' => 'Peterbilt Emergency Center',],
    ['i' => 'CY035A', 'c' => ['MB202','MB311'], 't' => 'Tanker', 'y' => '1992', 'n' => 'Mack Tanker',],
    ['i' => 'CY036A', 'c' => ['MB103','MB310'], 't' => 'Racing Transporter', 'y' => '1992', 'n' => 'Kenworth Transporter',],
    ['i' => 'CY037A', 'c' => ['MB214','MB308'], 't' => 'Racing Transporter', 'y' => '1993', 'n' => 'Ford Aeromax Transporter',],
    ['i' => 'CY038A', 'c' => ['MB045'], 't' => 'Container', 'y' => '1993', 'n' => 'Kenworth Container Truck',],
    ['i' => 'CY039A', 'c' => ['MB214','MB308'], 't' => 'Box', 'y' => '1994', 'n' => 'Ford Aeromax Box Truck',],
    ['i' => 'CY047A', 'c' => ['MCI'], 't' => 'none', 'y' => '1999', 'n' => 'MCI Coach',],
    ['i' => 'CY104A', 'c' => ['MB103'], 't' => 'Superstar Transporter', 'y' => '1989', 'n' => 'Kenworth Superstar Transporter',],
    ['i' => 'CY104B', 'c' => ['MB147'], 't' => 'Box', 'y' => '1997', 'n' => 'Scania Box Truck',],
    ['i' => 'CY105A', 'c' => ['MB045','MB103'], 't' => 'Box', 'y' => '1989', 'n' => 'Kenworth Gas Truck',],
    ['i' => 'CY106A', 'c' => ['MB106'], 't' => 'Tipper', 'y' => '1990', 'n' => 'Peterbilt Articulated Tipper Truck',],
    ['i' => 'CY106B', 'c' => ['MB106','MB307'], 't' => 'Container', 'y' => '1997', 'n' => 'Peterbilt Container Truck',],
    ['i' => 'CY107A', 'c' => ['MB202','MB311'], 't' => 'Superstar Transporter', 'y' => '1990', 'n' => 'Mack Superstar Transporter',],
    ['i' => 'CY108A', 'c' => ['MB183'], 't' => 'Modified Aircraft Transporter', 'y' => '1992', 'n' => 'DAF Aircraft Transporter',],
    ['i' => 'CY109A', 'c' => ['MB214'], 't' => 'Superstar Transporter', 'y' => '1991', 'n' => 'Ford Aeromax Superstar Transporter',],
    ['i' => 'CY110A', 'c' => ['MB045','MB309'], 't' => 'Superstar Transporter', 'y' => '1992', 'n' => 'Kenworth Superstar Transporter',],
    ['i' => 'CY111A', 'c' => ['CY010'], 't' => 'Racing transporter', 'y' => '1989', 'n' => 'Team Transporter',],
    ['i' => 'CY112A', 'c' => ['CY112'], 't' => 'Superstar Transporter', 'y' => '1994', 'n' => 'Kenworth T600 Superstar Transporter',],
    ['i' => 'CY113A', 'c' => ['MB214'], 't' => 'Superstar Transporter', 'y' => '1994', 'n' => 'Ford Aeromax Superstar Transporter',],
    ['i' => 'CY114A', 'c' => ['MB664'], 't' => 'Fishbelly', 'y' => '2005', 'n' => 'Tractor Cab with Fishbelly',],
    ['i' => 'CY115A', 'c' => ['MB214'], 't' => 'Fishbelly', 'y' => '2005', 'n' => "Ford Aeromax with Fishbelly",],
    ['i' => 'CY116A', 'c' => ['MB214'], 't' => 'Tanker V2', 'n' => "Ford Aeromax with Tanker V2", 'y' => '2006',],
    ['i' => 'CY117A', 'c' => ['MB664'], 't' => 'Tanker V2', 'n' => "Tractor Cab with Tanker", 'y' => '2006',],
    ['i' => 'CY118A', 'c' => ['MB702'], 't' => 'Tanker V2', 'n' => "DAF Tanker", 'y' => '2006',],
    ['i' => 'CY119A', 'c' => ['MB664'], 't' => 'Flat Bed V2', 'n' => "Tractor Cab with Flat Bed", 'y' => '2007',],
    ['i' => 'CY120A', 'c' => ['MB702'], 't' => 'Fishbelly', 'n' => "DAF Fishbelly", 'y' => '2007',],
    ['i' => 'CY121A', 'c' => ['MB725'], 't' => 'Flat Bed V2', 'n' => "Actros Flat Bed", 'y' => '2008',],
    ['i' => 'CY122A', 'c' => ['MB702'], 't' => 'Box', 'n' => "DAF Space Cab with Flatbed", 'y' => '2008',],
    ['i' => 'CY203A', 'c' => ['MB724'], 't' => 'Lowboy with Excavator', 'y' => '1989', 'n' => 'Construction Low Loader',],
    ['i' => 'CY803A', 'c' => ['MB147'], 't' => 'Lowboy with Cargo Truck', 'y' => '1992', 'n' => 'Scania Low Loader',],
    ['i' => 'TC001A', 'r' => 'TMTC', 'h' => 'TC001A', 'n' => 'Fire Set', 'y' => '1988', 'c' => ['MI724'], 't' => 'Fire Ladder',],
    ['i' => 'TC002A', 'r' => 'TMTC', 'h' => 'TC002A', 'n' => 'Tanker Set', 'y' => '1988', 'c' => ['MB147'], 't' => 'Tanker',],
    ['i' => 'TC003A', 'r' => 'TMTC', 'h' => 'TC003A', 'n' => 'Construction Set', 'y' => '1988', 'c' => ['MB045'], 't' => 'Tipper',],
    ['i' => 'TC004A', 'r' => 'TMTC', 'h' => 'TC004A', 'n' => 'Cargo Set', 'y' => '1988', 'c' => ['MB183'], 't' => 'Box',],
    ['i' => 'TC005A', 'r' => 'TMTC', 'h' => 'TC005A', 'n' => 'NASA Set', 'y' => '1988', 'c' => ['MB045'], 't' => 'Rocket Transporter',],
    ['i' => 'TC005B', 'r' => 'TMTC', 'h' => 'TC005B', 'n' => 'Team Kelloggs', 'y' => '1994', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC006A', 'r' => 'TMTC', 'h' => 'TC006A', 'n' => 'Rescue Set', 'y' => '1988', 'c' => ['MB183'], 't' => 'Boat Transporter',],
    ['i' => 'TC007A', 'r' => 'TMTC', 'h' => 'TC007A', 'n' => 'Pepsi Team Racing Transporter', 'y' => '1988', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting', 'm' => "Rerelease of TM01A",],
    ['i' => 'TC007B', 'r' => 'TMTC', 'h' => 'TC007B', 'n' => 'Team Manheim', 'y' => '1994', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC008A', 'r' => 'TMTC', 'h' => 'TC008A', 'n' => '7 Up Team Racing Transporter', 'y' => '1985', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting', 'm' => "Rerelease of TM05A",],
    ['i' => 'TC008B', 'r' => 'TMTC', 'h' => 'TC008B', 'n' => 'Team DeWalt', 'y' => '1994', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC009A', 'r' => 'TMTC', 'h' => 'TC009A', 'n' => 'Duckhams Team Racing Transporter', 'y' => '1985', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting', 'm' => "Rerelease of TM06A",],
    ['i' => 'TC010A', 'r' => 'TMTC', 'h' => 'TC010A', 'n' => 'Team Fuji', 'y' => '1988', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC011A', 'r' => 'TMTC', 'h' => 'TC011A', 'n' => 'Pirelli Team', 'y' => '1989', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC012A', 'r' => 'TMTC', 'h' => 'TC012A', 'n' => 'Tizer Team Racing Transporter', 'y' => '1989', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC013A', 'r' => 'TMTC', 'h' => 'TC013A', 'n' => 'TV News Set', 'y' => '1990', 'c' => ['MB183'], 't' => 'Box',],
    ['i' => 'TC014A', 'r' => 'TMTC', 'h' => 'TC014A', 'n' => 'Ferrari Set', 'y' => '1990', 'c' => ['MB183'], 't' => 'Box',],
    ['i' => 'TC015A', 'r' => 'TMTC', 'h' => 'TC015A', 'n' => 'Pirelli Set', 'y' => '1990', 'c' => ['MB183'], 't' => 'Box',],
    ['i' => 'TC015B', 'r' => 'TMTC', 'h' => 'TC015B', 'n' => 'Team Quality Care Racing Transporter', 'y' => '1994', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC016A', 'r' => 'TMTC', 'h' => 'TC016A', 'n' => 'Coast Guard Set', 'y' => '1990', 'c' => ['MB183'], 't' => 'Boat Transporter',],
    ['i' => 'TC017A', 'r' => 'TMTC', 'h' => 'TC017A', 'n' => 'Farm Set', 'y' => '1988', 'c' => ['MB045'], 't' => 'Tipper',],
    ['i' => 'TC018A', 'r' => 'TMTC', 'h' => 'TC018A', 'n' => 'Transport Set', 'y' => '1988', 'c' => ['MB202'], 't' => 'Double COntainer',],
    ['i' => 'TC024A', 'r' => 'TMTC', 'h' => 'TC024A', 'n' => 'Team Dupont Racing Transporter', 'y' => '1993', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC040A', 'r' => 'TMTC', 'h' => 'TC040A', 'n' => 'Dirt Devil Team Racing Transporter', 'y' => '1993', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC043A', 'r' => 'TMTC', 'h' => 'TC043A', 'n' => 'Hulkster Team Racing Transporter', 'y' => '1985', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC054A', 'r' => 'TMTC', 'h' => 'TC054A', 'n' => 'Goodwrench Racing Team Transporter', 'y' => '1990', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC056A', 'r' => 'TMTC', 'h' => 'TC056A', 'n' => 'Purolator Racing Team Transporter', 'y' => '1991', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC057A', 'r' => 'TMTC', 'h' => 'TC057A', 'n' => 'Kodak Racing Team Transporter', 'y' => '1991', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC059A', 'r' => 'TMTC', 'h' => 'TC059A', 'n' => 'Schraeder Racing Team Transporter', 'y' => '1991', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC060A', 'r' => 'TMTC', 'h' => 'TC060A', 'n' => 'Pennzoil Racing Team Transporter', 'y' => '1992', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC061A', 'r' => 'TMTC', 'h' => 'TC061A', 'n' => 'STP (Petty) Racing Team Transporter', 'y' => '1992', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC062A', 'r' => 'TMTC', 'h' => 'TC062A', 'n' => 'Mello Yello Racing Team Transporter', 'y' => '1992', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC063A', 'r' => 'TMTC', 'h' => 'TC063A', 'n' => 'McDuffie Racing Team Transporter', 'y' => '1992', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC064A', 'r' => 'TMTC', 'h' => 'TC064A', 'n' => 'Pontiac Excitement Team Racing Transporter', 'y' => '1992', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC065A', 'r' => 'TMTC', 'h' => 'TC065A', 'n' => 'Bill Elliot Racing Team Transporter', 'y' => '1992', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC066A', 'r' => 'TMTC', 'h' => 'TC066A', 'n' => 'Texaco/Havoline Team Racing Transporter', 'y' => '1993', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC067A', 'r' => 'TMTC', 'h' => 'TC067A', 'n' => 'Hooters Team Racing Transporter', 'y' => '1993', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC068A', 'r' => 'TMTC', 'h' => 'TC068A', 'n' => 'Country Time Team Racing Transporter', 'y' => '1993', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC095A', 'r' => 'TMTC', 'h' => 'TC095A', 'n' => 'Auto Palace Racing Team Transporter', 'y' => '1995', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC095B', 'r' => 'TMTC', 'h' => 'TC095B', 'n' => 'Team Caterpillar Racing Transporter', 'y' => '1996', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC096A', 'r' => 'TMTC', 'h' => 'TC096A', 'n' => "Team McDonald's Racing Transporter", 'y' => '1996', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC098A', 'r' => 'TMTC', 'h' => 'TC098A', 'n' => 'Team Bo Jangles Racing Transporter', 'y' => '1994', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC098B', 'r' => 'TMTC', 'h' => 'TC098B', 'n' => 'Team Fingerhut Racing Transporter', 'y' => '1995', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TC111A', 'r' => 'TMTC', 'h' => 'TC111A', 'n' => 'Team Mitre 10 Racing Transporter', 'y' => '1993', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TM01A', 'r' => 'TMTC', 'h' => 'TM01A', 'n' => 'Pemsi Team Racing Transporter', 'y' => '1985', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TM02A', 'r' => 'TMTC', 'h' => 'TM02A', 'n' => 'Superstar Team Racing Transporter', 'y' => '1985', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TM03A', 'r' => 'TMTC', 'h' => 'TM03A', 'n' => 'Dr. Pepper Team Racing Transporter', 'y' => '1985', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TM04A', 'r' => 'TMTC', 'h' => 'TM04A', 'n' => 'Brut Team Racing Transporter', 'y' => '1985', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TM05A', 'r' => 'TMTC', 'h' => 'TM05A', 'n' => '7 Up Team Racing Transporter', 'y' => '1985', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TM06A', 'r' => 'TMTC', 'h' => 'TM06A', 'n' => 'Duckhams Team Racing Transporter', 'y' => '1985', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting',],
    ['i' => 'TMXXA', 'r' => 'TMTC', 'h' => 'TMXXA', 'n' => 'STP Team Racing Transporter', 'y' => '1985', 'c' => ['CY010'], 't' => 'Racing transporter, part of cab casting', 'm' => 'no identification number',],
    ['i' => 'TP002C', 'c' => ['T9CO'], 't' => 'Tanker', 'y' => '1981', 'n' => 'Articulated Petrol Tanker',],
    ['i' => 'TP022A', 'c' => ['T9CC'], 't' => 'Double Container', 'y' => '1979', 'n' => 'Double Container Truck',],
    ['i' => 'TP023A', 'c' => ['T9CC'], 't' => 'Covered Container', 'y' => '1979', 'n' => 'Covered Countaier Truck',],
    ['i' => 'TP024A', 'c' => ['T9CC'], 't' => 'Container', 'y' => '1979', 'n' => 'Container Truck',],
    ['i' => 'TP025A', 'c' => ['T9CC'], 't' => 'Pipe Trailer', 'y' => '1979', 'n' => 'Pipe Truck',],
    ['i' => 'TP026A', 'c' => ['T9CO'], 't' => 'Boat Transporter', 'y' => '1981', 'n' => 'Boat Transporter',],

];

$row = 0;
foreach ($entries as $ent) {
    echo '    <tr class="ids' . $row . "\">\n";
    echo '      <td class="ids">';
    $fn = arr_get($ent, 'r', $ent['i']);
    if (file_exists('convoy/' . $fn . '.php')) {
	echo '<a href="' . $fn . '.php';
	if (arr_get($ent, 'h'))
	    echo '#' . arr_get($ent, 'h');
	echo '">' . $ent['i'] . '</a>';
    }
    else {
	echo '<i>' . $fn . '</i>';
    }
    echo "</td>\n";
    echo '      <td class="ids">';
    echo $ent['n'] . "</td>\n";
    echo '      <td class="ids">';
    echo $ent['y'] . "</td>\n";
    echo '      <td class="ids">';
    foreach (arr_get($ent, 'c', []) as $cab) {
	echo '<a href="/cgi-bin/single.cgi?id=' . $cab . '">' . $cab . '</a> ';
    }
    echo "</td>\n";
    echo '      <td class="ids">';
    echo arr_get($ent, 't') . "</td>\n";
    echo '      <td class="ids">';
    echo arr_get($ent, 'm') . "</td>\n";
    echo "    </tr>\n";
    $row = ($row + 1) % 2;
}

?>
  </tbody>
</table>
<font face="Arial" size="+1"><a href="index.php">Return to Front Page</a></font><br>
</body>
</html>

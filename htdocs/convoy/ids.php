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
	echo '<a href="' . $fn . '.php">' . $fn . '</a>';
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

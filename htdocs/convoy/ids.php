<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("convoy");
$pif['title'] = $pif['title'] . ' - Index by ID';
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
    <tr>
      <th>ID</th>
      <th>Year</th>
      <th>Convoy Name</th>
      <th>Notes</th>
    </tr>
<?php
$entries = [
    ['TP002C', '1981', 'Articulated Petrol Tanker'],
    ['TP022A', '1979', 'Double Container Truck'],
    ['TP023A', '1979', 'Covered Countaier Truck'],
    ['TP024A', '1979', 'Container Truck'],
    ['TP025A', '1979', 'Pipe Truck'],
    ['TP026A', '1981', 'Boat Transporter'],
    ['CY001A', '1982', 'Kenworth Car Transporter'],
    ['CY002A', '1982', 'Kenworth Rocket Transporter'],
    ['CY002B', '1999', 'Kenworth T-2000 Rocket Transporter', 'Rest of World'],
    ['CY003A', '1982', 'Double Container Truck'],
    ['CY003B', '1985', 'Kenworth Box Truck', 'Australia'],
    ['CY004A', '1982', 'Kenworth Boat Transporter'],
    ['CY004B', '1985', 'Scania Box Truck', 'Australia'],
    ['CY005A', '1982', 'Peterbilt Covered Truck'],
    ['CY006A', '1982', 'Kenworth Horse Box'],
    ['CY007A', '1982', 'Peterbilt Gas Tanker'],
    ['CY007B', '1998', 'Ford Aeromax Gas Tanker'],
    ['CY007C', '2001', 'DAF Gas Tanker', 'Rest of World'],
    ['CY008A', '1982', 'Kenworth Box Truck'],
    ['CY009A', '1982', 'Kenworth Box Truck'],
    ['CY009B', '2000', 'Kenworth T2000 Container Truck'],
    ['CY009C', '2001', 'Mercedes Benz Actross Container Truck'],
    ['CY010A', '1983', 'Racing Transporter'],
    ['CY011A', '1983', 'Kenworth Helicopter Transporter'],
    ['CY012A', '1984', 'Kenworth Plane Transporter'],
    ['CY013A', '1984', 'Peterbilt Fire Engine'],
    ['CY014A', '1985', 'Kenworth Boat Transporter'],
    ['CY015A', '1985', 'Peterbilt Tracking Vehicle'],
    ['CY016A', '1985', 'Scania Box Truck'],
    ['CY017A', '1985', 'Scania Petrol Tanker'],
    ['CY018A', '1986', 'Scania Double Container Truck'],
    ['CY018B', '1993', 'Ford Aeromax Double Container Truck'],
    ['CY019A', '1987', 'Peterbilt Box Truck'],
    ['CY020A', '1987', 'Articulated Dump Truck'],
    ['CY021A', '1987', 'DAF Aircraft Transporter'],
    ['CY021B', '2000', 'Scania Plane Transporter'],
    ['CY022A', '1987', 'Boat Transporter'],
    ['CY023A', '1988', 'Scania Covered Truck'],
    ['CY024A', '1988', 'DAF Box Truck'],
    ['CY025A', '1989', 'DAF Container Truck'],
    ['CY026A', '1989', 'DAF Double Container Truck'],
    ['CY027A', '1990', 'Mack Container Truck'],
    ['CY028A', '1990', 'Mack Double Container Truck'],
    ['CY029A', '1991', 'Mack Aircraft Transporter'],
    ['CY030A', '1992', 'Grove Crane'],
    ['CY031A', '1992', 'Mack Pipe Truck'],
    ['CY032A', '1992', 'Mack Shovel Transporter'],
    ['CY032B', '1998', 'Peterbilt Lowloader w/Bulldozer'],
    ['CY033A', '1992', 'Mack Helicopter Transporter'],
    ['CY034A', '1992', 'Peterbilt Emergency Center'],
    ['CY035A', '1992', 'Mack Tanker'],
    ['CY036A', '1992', 'Kenworth Transporter'],
    ['CY037A', '1993', 'Ford Aeromax Transporter'],
    ['CY038A', '1993', 'Kenworth Container Truck'],
    ['CY039A', '1994', 'Ford Aeromax Box Truck'],
    ['CY104A', '1989', 'Kenworth Superstar Transporter'],
    ['CY104B', '1997', 'Scania Box Truck'],
    ['CY105A', '1989', 'Kenworth Gas Truck'],
    ['CY106A', '1990', 'Peterbilt Articulated Tipper Truck'],
    ['CY106B', '1997', 'Peterbilt Container Truck'],
    ['CY107A', '1990', 'Mack Superstar Transporter'],
    ['CY108A', '1992', 'DAF Aircraft Transporter'],
    ['CY109A', '1991', 'Ford Aeromax Superstar Transporter'],
    ['CY110A', '1992', 'Kenworth Superstar Transporter'],
    ['CY111A', '1989', 'Team Transporter'],
    ['CY112A', '1994', 'Kenworth T600 Superstar Transporter'],
    ['CY113A', '1994', 'Ford Aeromax Superstar Transporter'],
    ['CY114A', '2005', 'Tractor Cab with Fishbelly'],
    ['CY203A', '1989', 'Construction Low Loader'],
    ['CY803A', '1992', 'Scania Low Loader'],
# everything below here doesn't yet exist.
#    ['ADT01', '1998', 'Kenworth Racing Transporter'],
#    ['ADT02', '1998', 'Ford Aeromax Racing Transporter'],
#    ['MLBPA97', '1998', 'Ford Aeromax Team Mates Double Tandems'],
#    ['35236', '1998', 'Police K-9 Unit'],
#    ['35237', '1998', 'Launch Control'],
#    ['TALKING', '1999', 'Basketball Trucks'],
#    ['CCY01', '1997', 'Peterbilt Container Truck'],
#    ['CCY02', '1997', 'Ford Aeromax Container Truck'],
#    ['CCY03', '1997', 'Kenworth Container Truck'],
#    ['CCY04', '1997', 'Kenworth Container Truck'],
#    ['CCY05', '1997', 'Mack Container Truck'],
#    ['CCY06', '1997', 'Peterbilt Container Truck'],
#    ['CCY07', '1998', 'Scania Container Truck'],
#    ['CCY08', '1998', 'DAF Container Truck'],
#    ['CCY09', '1998', 'Peterbilt Tanker'],
#    ['CCY10', '1998', 'Ford Aeromax Tanker'],
#    ['CCY11', '1998', 'Mack Tanker'],
#    ['CCY12', '1998', 'Kenworth Tanker'],
#    ['CCY13', '1998', 'DAF Tanker'],
#    ['CCY14', '1999', 'Peterbilt Box Truck'],
#    ['TM01A', '1985', 'Pepsi Team'],
#    ['TM02A', '1985', 'Superstar Team'],
#    ['TM03A', '1985', 'Dr. Pepper Team'],
#    ['TM04A', '1985', 'Brut Team'],
#    ['TM05A', '1985', '7 Up Team'],
#    ['TM06A', '1985', 'Duckhams Team'],
#    ['TM07A', '1985', 'STP Teams'],
#    ['TC001A', '1988', 'Fire Set'],
#    ['TC002A', '1988', 'Tanker Set'],
#    ['TC003A', '1988', 'Construction Set'],
#    ['TC004A', '1988', 'Cargo Set'],
#    ['TC005A', '1988', 'NASA Set'],
#    ['TC005B', '1994', 'Team Kelloggs'],
#    ['TC006A', '1988', 'Rescue Set'],
#    ['TC007A', '1988', 'Pepsi Team', 'reissue' => 'TM01A'],
#    ['TC007B', '1994', 'Team Manheim Auctions'],
#    ['TC008A', '1988', '7 Up Team', 'reissue' => 'TM05A'],
#    ['TC008B', '1994', 'Team DeWalt'],
#    ['TC009A', '1988', 'Duckhams Team', 'reissue' => 'TM06A'],
#    ['TC010A', '1988', 'Fuji Team'],
#    ['TC011A', '1989', 'Pirelli Team'],
#    ['TC012A', '1989', 'Tizer Team'],
#    ['TC013A', '1990', 'TV News Set'],
#    ['TC014A', '1990', 'Ferrari Set'],
#    ['TC015A', '1990', 'Pirelli Set'],
#    ['TC015B', '1994', 'Team Quality Care'],
#    ['TC016A', '1990', 'Coast Guard Set'],
#    ['TC017A', '1991', 'Farm Set'],
#    ['TC018A', '1991', 'Transport Set'],
#    ['TC024A', '1993', 'Team Dupont'],
#    ['TC040A', '1993', 'Dirt Devil Team'],
#    ['TC043A', '1995', 'Hulkster Team'],
#    ['TC054A', '1990', 'Goodwrench Racing Team'],
#    ['TC056A', '1991', 'Purolator Racing Team'],
#    ['TC057A', '1991', 'Kodak Racing Team'],
#    ['TC059A', '1991', 'Schraeder Racing Team'],
#    ['TC060A', '1992', 'Pennzoil Racing Team'],
#    ['TC061A', '1992', 'STP (Petty) Team'],
#    ['TC062A', '1992', 'Mello Yello Racing Team'],
#    ['TC063A', '1992', 'J.D. McDuffie Racing Team'],
#    ['TC064A', '1992', 'Pontiac Excitement Team'],
#    ['TC065A', '1992', 'Bill Elliot Racing Team'],
#    ['TC066A', '1993', 'Texaco/Havoline Team'],
#    ['TC067A', '1993', 'Hooters Team'],
#    ['TC068A', '1993', 'Country Time Team'],
#    ['TC095A', '1995', 'Auto Palace Racing Team'],
#    ['TC095B', '1996', 'Team Caterpillar'],
#    ['TC096A', '1996', 'Team McDonalds'],
#    ['TC098A', '1994', 'Team Bo Jangles'],
#    ['TC098B', '1995', 'Team Fingerhut'],
#    ['TC111A', '1993', 'Team Mitre 10'],
];

foreach ($entries as $ent) {
    echo "    <tr>\n";
    echo "      <td>";
    $fn = arr_get($ent, 'reissue', $ent[0]);
    if (file_exists('convoy/' . $fn . '.php')) {
	echo '<a href="' . $fn . '.php">' . $fn . '</a>';
    }
    else {
	echo '<i>' . $fn . '</i>';
    }
    echo "</td>\n";
    echo "      <td>" . $ent[1] . "</td>\n";
    echo "      <td>" . $ent[2] . "</td>\n";
    echo "      <td>" . arr_get($ent, 3) . "</td>\n";
    echo "    </tr>\n";
}

?>
  </tbody>
</table>
<font face="Arial" size="+1"><a href="index.php">Return to Front Page</a></font><br>
</body>
</html>

<?php
$subtitle = 'TM and TC Models';
$desc = "Team Matchbox / Team Convoy";
$year = '';

// refers to: CY002A CY013A CY015A CY017A CY020A CY022A CY024A CY025A CY028A

$defaults = [];

include "cypage.php";

function body() {
?>
Team Matchbox was first introduced in 1985 as a secondary Convoy line which included team transporters and two vehicles. By 1988, the line was renamed Team Convoy. Team Convoy included some of the Team Matchbox, but also included a combination of one Convoy plus one miniature. Several models were never numbered, however in late 1992, a CY111A was issued for Australia which includes a Team Matchbox type issue. As this has a CY rather than a TM or TC number, these are listed in the Convoy section. White Rose Collectibles introduced Team Convoy sets in 1990 with numbers starting at TC-54.<p>

<?php
    start_table();

// TM-1-A PEPSI TEAM, issued 1985 TC-7-A PEPSI TEAM, reissued 1988
    show_tmtc(['id' => 'TM01A', 'name' => 'Pemsi Team Racing Transporter', 'year' => '1985', 'fmt' => 'tall',
	'models' => [
// 1. Yellow transporter with ramp clips toward rear; includes MB034 Prostocker and MB068 Chevy Van in "Pepsi" liveries 
	    ['mod' => 'TM01A', 'var' => '01a', 'liv' => 'Pepsi',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'yellow with ramp clips toward rear',
            'tdt' => 'includes MB034 Prostocker and MB068 Chevy Van with PEPSI tampos'],
// 2. Yellow transporter with ramp clips toward front; includes MB034 Prostocker and MB068 Chevy Van in "Pepsi" liveries 
	    ['note' => "Variation 01b is the same but with ramp clips towards front"],
	]]);

// TM-2-A SUPERSTAR TEAM, issued 1985
    show_tmtc(['id' => 'TM02A', 'name' => 'Superstar Team Racing Transporter', 'year' => '1985', 'fmt' => 'tall',
	'models' => [
// 1. White transporter with ramp clips toward rear; includes MB034 Prostocker and MB121 Ruff Trek in "Superstar" liveries 
	    ['mod' => 'TM02A', 'var' => '01a', 'liv' => 'Superstar',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'white with ramp clips toward rear',
            'tdt' => 'includes MB034 Prostocker and MB121 Ruff Trek with SUPERSTAR tampos',],
// 2. White transporter with ramp clips toward front; includes MB034 Prostocker and MB121 Ruff Trek in "Superstar" liveries 
	    ['note' => "Variation 01b is the same but with ramp clips towards front"],
	]]);

// TM-3-A DR. PEPPER TEAM, issued 1985
    show_tmtc(['id' => 'TM03A', 'name' => 'Dr. Pepper Team Racing Transporter', 'year' => '1985', 'fmt' => 'tall',
	'models' => [
// 1. White transporter with ramp clips toward rear; includes MB117 Prostocker and MB068 Chevy Van in "Dr. Pepper" liveries 
	    ['mod' => 'TM03A', 'var' => '01a', 'liv' => 'Dr. Pepper',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'white with ramp clips toward rear',
            'tdt' => 'includes MB117 Prostocker and MB068 Chevy Van with DR. PEPPER tampos',],
// 2. White transporter with ramp clips toward front; includes MB117 Prostocker and MB068 Chevy Van in "Dr. Pepper" liveries 
	    ['note' => "Variation 01b is the same but with ramp clips towards front"],
	]]);

// TM-4-A BRUT TEAM, issued 1985
    show_tmtc(['id' => 'TM04A', 'name' => 'Brut Team Racing Transporter', 'year' => '1985', 'fmt' => 'tall',
	'models' => [
// 1. White transporter with ramp clips toward rear; includes MB062 Corvette and MB121 Ruff Trek in "Brut" liveries 
	    ['mod' => 'TM04A', 'var' => '01a', 'liv' => 'Brut',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'white with ramp clips toward rear',
            'tdt' => 'includes MB062 Corvette and MB121 Ruff Trek in BRUT tampos',],
// 2. White transporter with ramp clips toward front; includes MB062 Corvette and MB121 Ruff Trek in "Brut" liveries 
	    ['note' => "Variation 01b is the same but with ramp clips towards front"],
	]]);

// TM-5-A 7 UP TEAM, issued 1985 TC-8-A 7 UP TEAM, reissued 1988
    show_tmtc(['id' => 'TM05A', 'name' => '7 Up Team Racing Transporter', 'year' => '1985', 'fmt' => 'tall',
	'models' => [
// 1. Green transporter with ramp clips toward rear; includes MB034 Prostocker and MB121 Ruff Trek in "7 Up" liveries 
	    ['mod' => 'TM05A', 'var' => '01a', 'liv' => '7 Up',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'green transporter with ramp clips toward rear',
            'tdt' => 'includes MB034 Prostocker and MB121 Ruff Trek in 7 UP tampos',],
// 2. Green transporter with ramp clips toward front; includes MB034 Prostocker and MB121 Ruff Trek in "7 Up" liveries 
	    ['note' => "Variation 01b is the same but with ramp clips towards front"],
	]]);

// TM-6-A DUCKHAMS TEAM, issued 1985 TC-9-A DUCKHAMS TEAM, reissued 1988
    show_tmtc(['id' => 'TM06A', 'name' => 'Duckhams Team Racing Transporter', 'year' => '1985', 'fmt' => 'tall',
	'models' => [
// 1. Dark blue transporter; includes MB120 Ford Sierra and MB166 Ford Supervan II in "Duckhams QXR" liveries 
	    ['mod' => 'TM06A', 'var' => '01a', 'liv' => 'Duckhams',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'dark blue transporter',
            'tdt' => 'includes MB120 Ford Sierra and MB166 Ford Supervan II in DUCKHAMS QXR tampos',], 
	]]);

// TM-X-A STP TEAMS, issued 1985 (no identification #)
    show_tmtc(['id' => 'TMXXA', 'name' => 'STP Team Racing Transporter', 'year' => '1985', 'fmt' => 'tall',
	'models' => [
// 1. Dark blue transporter; includes MB137 F.1 Racer and MB121 Ruff Trek in "STP 20" liveries (US)
	    ['mod' => 'TMXXA', 'var' => '01a', 'liv' => 'STP',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'nts' => 'no identification number',
            'cdt' => 'dark blue transporter',
            'tdt' => 'includes MB137 F.1 Racer and MB121 Ruff Trek in STP 20 tampos',],
// 2. Yellow transporter; includes MB155 Firebird Racer and MB068 Chevy Van in "STP Son of A Gun" liveries (US)
	    ['mod' => 'TMXXA', 'var' => '02a', 'liv' => 'STP',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'nts' => 'no identification number',
            'cdt' => 'yellow transporter',
            'tdt' => 'includes MB155 Firebird Racer and MB068 Chevy Van in STP SON OF A GUN liveries',],
	]]);

// TC-01-A FIRE SET, issued 1988
    show_tmtc(['id' => 'TC001A', 'name' => 'Fire Set', 'year' => '1988', 'fmt' => 'wide',
	'models' => [
// 1. Includes CY013A in red with MB054 Command Vehicle in red 
	    ['mod' => 'TC001A', 'var' => '01a', 'liv' => 'none',
	    'cab' => 'MI724', 'tlr' => 'Fire Ladder', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'red',
            'tdt' => 'red with yellow lettered 8 and FIRE DEPT. tampo, white ladder, with MB054 Command Vehicle in red',],
	]]);

// TC-02-A TANKER SET, issued 1988
    show_tmtc(['id' => 'TC002A', 'name' => 'Tanker Set', 'year' => '1988', 'fmt' => 'wide',
	'models' => [
// 1. Includes CY017A in "Shell" livery with MB100 Tanker in "Shell" livery 
	    ['mod' => 'TC002A', 'var' => '01a', 'liv' => 'Shell',
	    'cab' => 'MB147', 'tlr' => 'Tanker', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'white, dark gray chassis, chrome base',
            'tdt' => 'chrome tank with dark gray base, SHELL tampo, with MB100 Tanker in SHELL tampos',],
	]]);

// TC-03-A CONSTRUCTION SET, issued 1988
    show_tmtc(['id' => 'TC003A', 'name' => 'Construction Set', 'year' => '1988', 'fmt' => 'wide',
	'models' => [
// 1. Includes CY020A in yellow with MB029 Tractor Shovel in yellow 
	    ['mod' => 'TC003A', 'var' => '01a', 'liv' => 'none',
	    'cab' => 'MB045', 'tlr' => 'Tipper', 'mfg' => 'Macau', 'cod' => '1',
	    'cdt' => 'yellow, chrome exhausts',
	    'tdt' => 'yellow trailer with black base, black and white road design tampo, includes MB029 Tractor Shovel in yellow',],
	]]);

// TC-04-A CARGO SET, issued 1988
    show_tmtc(['id' => 'TC004A', 'name' => 'Cargo Set', 'year' => '1988', 'fmt' => 'wide',
	'models' => [
// 1. Includes CY025A DAF Box Truck and MB148 Volvo Container Truck in "TNT Ipec" liveries 
	    ['mod' => 'TC004A', 'var' => '01a', 'liv' => 'TNT Ipec',
	    'cab' => 'MB183', 'tlr' => 'Box', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'white and orange, orange chassis',
            'tdt' => 'white container with orange base, TNT IPEC tampo, includes MB148 Volvo Container Truck in TNT IPEC tampo',],
// 2. Includes CY025A DAF Box Truck and MB072 Dodge Delivery Truck in "XP Parcels" liveries 
	    ['mod' => 'TC004A', 'var' => '02a', 'liv' => 'XP Parcels',
	    'cab' => 'MB183', 'tlr' => 'Box', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'white, black chassis',
            'tdt' => 'white container with black base, XP tampo, includes MB072 Dodge Delivery Truck in XP PARCELS tampo',],
	]]);

// TC-05-A NASA SET, issued 1988
    show_tmtc(['id' => 'TC005A', 'name' => 'NASA Set', 'year' => '1988', 'fmt' => 'wide',
	'models' => [
// 1. Includes CY002A Rocket Transporter and MB054 Command Vehicle in "NASA" liveries 
	    ['mod' => 'TC005A', 'var' => '01a', 'liv' => 'NASA',
	    'cab' => 'MB045', 'tlr' => 'Rocket Transporter', 'mfg' => 'Macau', 'cod' => '1',
	    'cdt' => 'white, chrome exhausts',
	    'tdt' => 'includes MB054 Command Vehicle in NASA tampo',],
	]]);

// TC-05-B TEAM KELLOGGS, issued 1994
    show_tmtc(['id' => 'TC005B', 'name' => 'Team Kelloggs', 'year' => '1994', 'fmt' => 'wide',
	'models' => [
// 1. Dark blue transporter, Thailand casting; MB267 Lumina in yellow and red, China casting; MB267 Lumina in gray, China casting-all with "Kellogg's Racing 5" tampo (WR)
	    ['mod' => 'TC005B', 'var' => '01a', 'liv' => "Kellogg's",
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
	    'cdt' => "dark blue, chrome exhausts, KELLOGG'S RACING 5",
	    'tdt' => "includes MB267 Lumina in yellow and red, and MB267 Lumina in gray, both with KELLOGG'S RACING 5 tampo and CHina castings",],
	]]);

// TC-06-A RESCUE SET, issued 1988
    show_tmtc(['id' => 'TC006A', 'name' => 'Rescue Set', 'year' => '1988', 'fmt' => 'wide',
	'models' => [
// 1. Includes CY022A Boat Transporter and MB075 Helicopter in "Rescue" liveries 
	    ['mod' => 'TC006A', 'var' => '01a', 'liv' => 'Rescue',
	    'cab' => 'MB183', 'tlr' => 'Boat Transporter', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'white, florescent orange chassis, RESCUE 3 and checkers tampo',
            'tdt' => 'florescent orange, boat with florescent orange deck, white hull and MARINE RESCUE tampo, includes MB075 Helicopter in RESCUE tampo',],
	]]);

// TC-07-A PEPSI TEAM (see TM-1-A)
// TM-1-A PEPSI TEAM, issued 1985 TC-7-A PEPSI TEAM, reissued 1988
    show_tmtc(['id' => 'TC007A', 'name' => 'Pepsi Team Racing Transporter', 'year' => '1988', 'fmt' => 'wide',
	'models' => [
// 1. Yellow transporter with ramp clips toward rear; includes MB034 Prostocker and MB068 Chevy Van in "Pepsi" liveries 
	    ['mod' => 'TC007A', 'var' => '01a', 'liv' => 'Pepsi',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'yellow with ramp clips toward rear',
            'tdt' => 'includes MB034 Prostocker and MB068 Chevy Van with PEPSI tampos'],
// 2. Yellow transporter with ramp clips toward front; includes MB034 Prostocker and MB068 Chevy Van in "Pepsi" liveries 
	    ['note' => "Variation 01b is the same but with ramp clips towards front"],
	    ['note' => "Rerelease of TM01A"],
	]]);

// TC-07-B TEAM MANHEIM AUCTIONS, issued 1994
    show_tmtc(['id' => 'TC007B', 'name' => 'Team Manheim', 'year' => '1994', 'fmt' => 'wide',
	'models' => [
// 1. Fluorescent green transporter, Thailand casting; MB267 Luminas in fluorescent green-one with black lettering, other with white lettering, China castings-all with "Manheim Auctions 7" tampo (WR)
	    ['mod' => 'TC007B', 'var' => '01a', 'liv' => "Manheim",
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
	    'cdt' => 'fluorescent green, MANHEIM AUCTIONS tampo',
	    'tdt' => 'includes MB267 Luminas in fluorescent green--one with black lettering, other with white lettering, China castings--both with MANHEIM AUCTIONS 7 tampo',],
	]]);

// TC-08-A 7 UP TEAM (see TM-5-A)
// TM-5-A 7 UP TEAM, issued 1985 TC-8-A 7 UP TEAM, reissued 1988
    show_tmtc(['id' => 'TC008A', 'name' => '7 Up Team Racing Transporter', 'year' => '1985', 'fmt' => 'tall',
	'models' => [
// 1. Green transporter with ramp clips toward rear; includes MB034 Prostocker and MB121 Ruff Trek in "7 Up" liveries 
	    ['mod' => 'TC008A', 'var' => '01a', 'liv' => '7 Up',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'green transporter with ramp clips toward rear',
            'tdt' => 'includes MB034 Prostocker and MB121 Ruff Trek in 7 UP tampos',],
// 2. Green transporter with ramp clips toward front; includes MB034 Prostocker and MB121 Ruff Trek in "7 Up" liveries 
	    ['note' => "Variation 01b is the same but with ramp clips towards front"],
	    ['note' => "Rerelease of TM05A"],
	]]);

// TC-08-B TEAM DEWALT, issued 1994
    show_tmtc(['id' => 'TC008B', 'name' => 'Team DeWalt', 'year' => '1994', 'fmt' => 'wide',
	'models' => [
// 1. Orange-yellow transporter, Thailand casting; MB267 in orange-yellow, China casting; MB068 Chevy Van in orange-yellow, Thailand casting-all with "DeWalt 08" tampo (WR) TC-09-A DUCKHAMS TEAM (see TM-6-A)
	    ['mod' => 'TC008B', 'var' => '01a', 'liv' => "DeWalt",
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
	    'cdt' => 'orange-yellow transporter, DEWALT tampo',
	    'tdt' => 'includes MB267 in orange-yellow, China casting; MB068 Chevy Van in orange-yellow, Thailand casting, both with DEWALT 08 tampo',],
	]]);

// TC-09-A DUCKHAMS TEAM (see TM-6-A)
// TM-6-A DUCKHAMS TEAM, issued 1985 TC-9-A DUCKHAMS TEAM, reissued 1988
    show_tmtc(['id' => 'TC009A', 'name' => 'Duckhams Team Racing Transporter', 'year' => '1985', 'fmt' => 'tall',
	'models' => [
// 1. Dark blue transporter; includes MB120 Ford Sierra and MB166 Ford Supervan II in "Duckhams QXR" liveries 
	    ['mod' => 'TC009A', 'var' => '01a', 'liv' => 'Duckhams',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'dark blue transporter',
            'tdt' => 'includes MB120 Ford Sierra and MB166 Ford Supervan II in DUCKHAMS QXR tampos',], 
	    ['note' => "Rerelease of TM06A"],
	]]);

// TC-10-A FUJI TEAM, issued 1988
    show_tmtc(['id' => 'TC010A', 'name' => 'Team Fuji', 'year' => '1988', 'fmt' => 'wide',
	'models' => [
// 1. White and green transporter, chrome exhausts; includes MB077 Nissan 300ZX and MB166 Ford Supervan II in "Fuji Racing Team" liveries 
	    ['mod' => 'TC010A', 'var' => '01a', 'liv' => "Fuji",
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'cdt' => 'white and green transporter, chrome exhausts, FUJI RACING TEAM tampo',
	    'tdt' => 'includes MB077 Nissan 300ZX and MB166 Ford Supervan II in FUJI RACING TEAM tampos ',],
// 2. White and green transporter, gray exhausts; includes MB077 Nissan 300ZX and MB166 Ford Supervan II in "Fuji Racing Team" liveries 
	    ['mod' => 'TC010A', 'var' => '02a', 'liv' => "Fuji",
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'cdt' => 'white and green transporter, gray exhausts, FUJI RACING TEAM tampo',
	    'tdt' => 'includes MB077 Nissan 300ZX and MB166 Ford Supervan II in FUJI RACING TEAM tampos ',],
	]]);

// TC-11-A PIRELLI TEAM, issued 1989
    show_tmtc(['id' => 'TC011A', 'name' => 'Pirelli Team', 'year' => '1989', 'fmt' => 'wide',
	'models' => [
// 1. White transporter, chrome exhausts, includes MB173 Porsche 959 and MB072 Dodge Truck in "Pirelli Gripping Stuff "liveries 
	    ['mod' => 'TC011A', 'var' => '01a', 'liv' => "Pirelli",
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'cdt' => 'white transporter, chrome exhausts, PIRELLI GRIPPING STUFF tampo ',
	    'tdt' => 'includes MB173 Porsche 959 and MB072 Dodge Truck in PIRELLI GRIPPING STUFF tampos ',],
// 2. White transporter, gray exhausts, includes MB173 Porsche 959 and MB072 Dodge Truck in "Pirelli Gripping Stuff" liveries 
	    ['mod' => 'TC011A', 'var' => '02a', 'liv' => "Pirelli",
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'cdt' => 'white transporter, gray exhausts, PIRELLI GRIPPING STUFF tampo ',
	    'tdt' => 'includes MB173 Porsche 959 and MB072 Dodge Truck in PIRELLI GRIPPING STUFF tampos ',],
	]]);

// TC-12-A TIZER TEAM, issued 1989
    show_tmtc(['id' => 'TC012A', 'name' => 'Tizer Team Racing Transporter', 'year' => '1989', 'fmt' => 'tall',
	'models' => [
// 1. Red transporter, chrome exhausts, includes MB120 Ford Sierra and MB166 Ford Supervan II in "Tizer" liveries 
	    ['mod' => 'TC012A', 'var' => '01a', 'liv' => 'Tizer',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'red transporter, chrome exhausts, TIZER tampo',
            'tdt' => 'includes MB120 Ford Sierra and MB166 Ford Supervan II in TIZER tampos',], 
// 2. Red transporter, gray exhausts, includes MB120 Ford Sierra and MB166 Ford Supervan II in "Tizer" liveries 
	    ['mod' => 'TC012A', 'var' => '02a', 'liv' => 'Tizer',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'red transporter, gray exhausts, TIZER tampo',
            'tdt' => 'includes MB120 Ford Sierra and MB166 Ford Supervan II in TIZER tampos',], 
	]]);

// TC-13-A TV NEWS SET, issued 1990
    show_tmtc(['id' => 'TC013A', 'name' => 'TV News Set', 'year' => '1990', 'fmt' => 'wide',
	'models' => [
// 1. Includes CY015A Tracking Vehicle and MB205 TV Van in dark blue with "MB TV News" liveries 
	    ['mod' => 'TC013A', 'var' => '01a', 'liv' => 'MB TV News',
	    'cab' => 'MB183', 'tlr' => 'Box', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'dark blue with PETERBILT and bolt tampo, gray exhausts',
            'tdt' => 'dark blue container with pearly silver base, includes MB205 TV Van in dark blue, both with MB TV NEWS tampo ',],
// 2. Includes CY015A Tracking Vehicle and MB205 TV Van in white with "Sky Satellite TV" liveries 
	    ['mod' => 'TC013A', 'var' => '02a', 'liv' => 'MB TV News',
	    'cab' => 'MB183', 'tlr' => 'Box', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'white cab with SKY TV tampo',
            'tdt' => 'white container with pearly silver base, includes MB205 TV Van in white, both with SKY SATELLITE TV tampo ',],
	]]);

// TC-14-A FERRARI SET, issued 1990
    show_tmtc(['id' => 'TC014A', 'name' => 'Ferrari Set', 'year' => '1990', 'fmt' => 'wide',
	'models' => [
// 1. Includes CY024A in red and MB203 G.P Racer in red with "Ferrari" liveries 
	    ['mod' => 'TC014A', 'var' => '01a', 'liv' => 'Ferrari',
	    'cab' => 'MB183', 'tlr' => 'Box', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'red with black chassis',
            'tdt' => 'red container with pearly silver base, includes MB203 G.P Racer in red, both with FERRARI tampo',],
// 2. Includes CY024A in red and MB070 Ferrari in red with "Ferrari" liveries 
	    ['mod' => 'TC014A', 'var' => '02a', 'liv' => 'Ferrari',
	    'cab' => 'MB183', 'tlr' => 'Box', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'red with black chassis',
            'tdt' => 'red container with pearly silver base, includes MB070 Ferrari in red, both with FERRARI tampo ',],
	]]);

// TC-15-A PIRELLI SET, issued 1990
    show_tmtc(['id' => 'TC015A', 'name' => 'Pirelli Set', 'year' => '1990', 'fmt' => 'wide',
	'models' => [
// 1. Includes CY025A DAF Container and MB173 Porsche 959 in white with "Pirelli Gripping Stuff" liveries 
	    ['mod' => 'TC015A', 'var' => '01a', 'liv' => 'Pirelli',
	    'cab' => 'MB183', 'tlr' => 'Box', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'white, black chassis',
            'tdt' => 'white container with black base, PIRELLI GRIPPING STUFF tampo, includes MB173 Porsche 959 in white with PIRELLI GRIPPING STUFF tampos',],
	]]);

// TC-15-B TEAM QUALITY CARE, issued 1994
    show_tmtc(['id' => 'TC015B', 'name' => 'Team Quality Care Racing Transporter', 'year' => '1994', 'fmt' => 'tall',
	'models' => [
// 1. Bright blue transporter, Thailand casting; MB267 Lumina in bright blue, China casting; MB053 Flareside in bright blue, Thailand casting-all in "Quality Care 15" tampo (WR)
	    ['mod' => 'TC015B', 'var' => '01a', 'liv' => 'Quality Care',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'bright blue transporter with QUALITY CARE 15 tampo',
            'tdt' => 'includes MB267 Lumina in bright blue, China casting, and MB053 Flareside in bright blue, Thailand casting, both with QUALITY CARE 15 tampo',],
	]]);

// TC-16-A COAST GUARD SET, issued 1990
    show_tmtc(['id' => 'TC016A', 'name' => 'Coast Guard Set', 'year' => '1990', 'fmt' => 'wide',
	'models' => [
// 1. Includes CY022A DAF Boat Transporter and MB187 Ford Bronco II in "Coast Guard" liveries 
	    ['mod' => 'TC016A', 'var' => '01a', 'liv' => 'Coast Guard',
	    'cab' => 'MB183', 'tlr' => 'Boat Transporter', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'white, black chassis, COAST GUARD tampo',
            'tdt' => 'black trailer, boat with gray deck, white hull and COAST GUARD tampo, includes MB187 Ford Bronco II in COAST GUARD tampos',], 
	]]);

// TC-17-A FARM SET, issued 1991
    show_tmtc(['id' => 'TC017A', 'name' => 'Farm Set', 'year' => '1988', 'fmt' => 'wide',
	'models' => [
// 1. Includes CY020A Tipper Truck with green cab and yellow dump with "Eurobran" livery with MB218 Mercedes Tractor in yellow and green 
	    ['mod' => 'TC017A', 'var' => '01a', 'liv' => 'Eurobran',
	    'cab' => 'MB045', 'tlr' => 'Tipper', 'mfg' => 'Macau', 'cod' => '1',
	    'cdt' => 'green',
	    'tdt' => 'yellow with EUROBRAN tampo, includes MB218 Mercedes Tractor in yellow and green ',],
	]]);

// TC-18-A TRANSPORT SET, issued 1991
    show_tmtc(['id' => 'TC018A', 'name' => 'Transport Set', 'year' => '1988', 'fmt' => 'wide',
	'models' => [
// 1. Includes CY028A Mack Double Container in white with "DHL" livery with MB048 Fork Lift Truck in white with red stripes 
	    ['mod' => 'TC018A', 'var' => '01a', 'liv' => 'DHL',
	    'cab' => 'MB202', 'tlr' => 'Double COntainer', 'mfg' => 'Macau', 'cod' => '1',
            'cdt' => 'white, black chassis',
            'tdt' => 'black, white containers, DHL WORLDWIDE EXPRESS tampo, includes MB048 Fork Lift Truck in white with red stripes',],
	]]);

// TC-24-A TEAM DUPONT, issued 1993
    show_tmtc(['id' => 'TC024A', 'name' => 'Team Dupont Racing Transporter', 'year' => '1993', 'fmt' => 'tall',
	'models' => [
// 1. Metallic blue transporter, Thailand casting; MB221 Lumina in metallic blue and orange, China casting, MB221 Lumina in gold plate, China casting-all with "Dupont 24" tampo (WR)
	    ['mod' => 'TC024A', 'var' => '01a', 'liv' => 'Dupont',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'metallic blue transporter with DUPONT 24 tampo',
            'tdt' => 'includes MB221 Lumina in metallic blue and orange, China casting, MB221 Lumina in gold plate, China casting, both with DUPONT 24 tampo',],
	]]);

// TC-40-A DIRT DEVIL TEAM, issued 1993
    show_tmtc(['id' => 'TC040A', 'name' => 'Dirt Devil Team Racing Transporter', 'year' => '1993', 'fmt' => 'tall',
	'models' => [
// 1. Black transporter, Thailand casting: MB216 Pontiacs in black, one with white "40" and other with orange "40," Thailand castings-all in "Dirt Devil 40" tampo (WR)
	    ['mod' => 'TC040A', 'var' => '01a', 'liv' => 'Dirt Devil',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'black transporter with DIRT DEVIL 40 tampo',
            'tdt' => 'includes MB216 Pontiacs in black, one with white 40 and other with orange 40, Thailand castings, both with DIRT DEVIL 40 tampo',],
	]]);

// TC-43-A HULKSTER TEAM, issued 1995
    show_tmtc(['id' => 'TC043A', 'name' => 'Hulkster Team Racing Transporter', 'year' => '1985', 'fmt' => 'tall',
	'models' => [
// 1. Red transporter, Thailand casting; MB269 Pontiac in red, China casting; WR002 F800 Ford in red with orange/ yellow container, China casting; all with "Hulkster 43/ Hogan" liveries (WR)
	    ['mod' => 'TC043A', 'var' => '01a', 'liv' => 'Hulkster',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'red transporter with HULKSTER 43/HOGAN tampo',
            'tdt' => 'includes MB269 Pontiac in red, China casting, and WR002 F800 Ford in red with orange-yellow container, China casting, both with HULKSTER 43/HOGAN tampo',],
	]]);

// TC-54-A GOODWRENCH RACING TEAM, issued 1990
    show_tmtc(['id' => 'TC054A', 'name' => 'Goodwrench Racing Team Transporter', 'year' => '1990', 'fmt' => 'tall',
	'models' => [
// 1. Black transporter with "GM" roof tampo and no door tampo; MB221 Chevy Lumina in black with Goodyear slicks, plain trunk and no "Western Steer" emblem; MB068 Chevy Van in black-all with "Goodwrench Racing," Macau castings (WR)
	    ['mod' => 'TC054A', 'var' => '01a', 'liv' => 'Goodwrench',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'black transporter with GM roof tampo, no door tampo, with GOODWRENCH RACING tampo',
            'tdt' => 'includes MB221 Chevy Lumina in black with Goodyear slicks, plain trunk, and MB068 Chevy Van in black, both with GOODWRENCH RACING, Macau castings',], 
// 2. Black transporter with "GM" roof tampo and "1990 Champion" on door, Thailand casting; MB221 Chevy Lumina in black with Goodyear slicks, with trunk design and no "Western Steer" tampo, China casting; MB068 Chevy Van in black, Thailand casting-all with "Goodwrench Racing" (WR)
	    ['mod' => 'TC054A', 'var' => '02a', 'liv' => 'Goodwrench',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'black transporter with GM roof tampo and 1990 CHAMPION on door with GOODWRENCH RACING tampo',
            'tdt' => 'includes MB221 Chevy Lumina in black with Goodyear slicks, with trunk design tampo, China casting, and MB068 Chevy Van in black, Thailand casting, both with GOODWRENCH RACING tampo',],
// 3. Black transporter with "GM" on roof tampo and "1990 Champion" on doors, Thailand casting; MB221 Chevy Lumina in black with black disc and rubber tires, with trunk design and with "Western Steer" tampo, China casting; MB068 Chevy Van in black, Thailand casting-all with "Goodwrench Racing" (WR)
	    ['mod' => 'TC054A', 'var' => '03a', 'liv' => 'Goodwrench',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'black transporter with GM on roof tampo and 1990 CHAMPION on doors, with GOODWRENCH RACING tampo',
            'tdt' => 'includes MB221 Chevy Lumina in black with black disc and rubber tires, with trunk design and WESTERN STEER tampo, China casting, and MB068 Chevy Van in black, Thailand casting, both with GOODWRENCH RACING tampo',],
// 4. Black transporter with "GM" on roof tampo and "1990 Champion" on door, Thailand casting; MB221 Chevy Lumina in black with gray disc and rubber tires, with trunk design and with "Western Steer" tampo, China casting; MB068 Chevy Van in black, Thailand casting - all with "Goodwrench Racing" (WR)
	    ['mod' => 'TC054A', 'var' => '04a', 'liv' => 'Goodwrench',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'black transporter with GM on roof tampo and 1990 CHAMPION on doors, with GOODWRENCH RACING tampo',
            'tdt' => 'includes MB221 Chevy Lumina in black with black disc and rubber tires, with trunk design and WESTERN STEER tampo, China casting, and MB068 Chevy Van in black, Thailand casting, both with GOODWRENCH RACING tampo',],
// 5. Black transporter with "Dale Earnhardt" roof tampo and "1990 Champion" on doors, Thailand casting; MB221 Chevy Lumina in black with black disc and rubber tires, with trunk design and with "Western Steer" tampo, China casting; MB068 Chevy Van in black, Thailand casting -all with "Goodwrench Racing" (WR)
	    ['mod' => 'TC054A', 'var' => '05a', 'liv' => 'Goodwrench',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'black transporter with DALE EARNHARDT roof tampo and 1990 CHAMPION on doors, with GOODWRENCH RACING tampo',
            'tdt' => 'includes MB221 Chevy Lumina in black with black disc and rubber tires, with trunk design and with WESTERN STEER tampo, China casting, and MB068 Chevy Van in black, Thailand casting, both with GOODWRENCH RACING tampo',],
// 6. Black transporter with "Dale Earnhardt" on roof tampo and "1991 Champion" on doors, Thailand casting; MB221 Chevy Lumina in black with black disc and rubber tires, with trunk design and with "Western Steer" tampo, China casting; MB068 Chevy Van in black with "5 Time Champion" tampo, Thailand casting-all with "Goodwrench Racing" (WR)
	    ['mod' => 'TC054A', 'var' => '06a', 'liv' => 'Goodwrench',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'black transporter with DALE EARNHARDT on roof tampo and 1991 CHAMPION on doors, with GOODWRENCH RACING tampo',
            'tdt' => 'includes MB221 Chevy Lumina in black with black disc and rubber tires, with trunk design and with WESTERN STEER tampo, China casting, and MB068 Chevy Van in black with 5 TIME CHAMPION tampo, Thailand casting, both with GOODWRENCH RACING tampo',],
// 7. Black transporter with "Dale Earnhardt" roof signature and "1991 Champion" on door, Thailand casting; MB221 Chevy Lumina in black with gray disc and rubber tires, with trunk design and with "Western Steer," China casting; MB221 Chevy Lumina in matt black with "GM" on hood and "Goodwrench" on sides, slicks, Thailand casting - all with "Goodwrench Racing" tampo (WR)
	    ['mod' => 'TC054A', 'var' => '07a', 'liv' => 'Goodwrench',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'black transporter with DALE EARNHARDT roof signature and 1991 CHAMPION on door, with GOODWRENCH RACING tampo',
            'tdt' => 'includes MB221 Chevy Lumina in black with gray disc and rubber tires, with trunk design and with WESTERN STEER, China casting, and MB221 Chevy Lumina in matt black with GM on hood and GOODWRENCH on sides, slicks, Thailand casting, both with GOODWRENCH RACING tampo',],
	]]);

// TC-56-A PUROLATOR RACING TEAM, issued 1991
    show_tmtc(['id' => 'TC056A', 'name' => 'Purolator Racing Team Transporter', 'year' => '1991', 'fmt' => 'tall',
	'models' => [
// 1. White and florescent orange transporter, Thailand casting; MB221 Chevy Lumina in white and florescent orange, China casting; MB068 Chevy Van in white and florescent orange, Thailand casting - all with "Purolator 10 Racing Team" liveries (WR)
	    ['mod' => 'TC056A', 'var' => '01a', 'liv' => 'Purolator',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'white and florescent orange transporter with PUROLATOR 10 RACING TEAM tampo',
            'tdt' => 'includes includes MB221 Chevy Lumina in white and florescent orange, China casting, and MB068 Chevy Van in white and florescent orange, Thailand casting, both with PUROLATOR 10 RACING TEAM tampos',],
	]]);

// TC-57-A KODAK RACING TEAM, issued 1991
    show_tmtc(['id' => 'TC057A', 'name' => 'Kodak Racing Team Transporter', 'year' => '1991', 'fmt' => 'tall',
	'models' => [
// 1. Orange-yellow transporter, Thailand casting; MB221 Chevy Lumina in orange-yellow, China casting; MB068 Chevy Van in orange-yellow, Thailand casting - all with "Kodak 4 Racing" liveries (WR)
	    ['mod' => 'TC057A', 'var' => '01a', 'liv' => 'Kodak',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'orange-yellow transporter with KODAK 4 RACING tampo',
            'tdt' => 'includes MB221 Chevy Lumina in orange-yellow, China casting, and MB068 Chevy Van in orange-yellow, Thailand casting, both with KODAK 4 RACING tampos',],
	]]);

// TC-59-A SCHRAEDER RACING TEAM, issued 1991
    show_tmtc(['id' => 'TC059A', 'name' => 'Schraeder Racing Team Transporter', 'year' => '1991', 'fmt' => 'tall',
	'models' => [
// 1. White and green transporter, gold hubs, Thailand casting; MB221 Chevy Lumina in white and green with gold disc wheels, China casting; MB068 Chevy Van in white and green with gold hubs, Thailand casting - all with "Schraeder 25" liveries 
	    ['mod' => 'TC059A', 'var' => '01a', 'liv' => 'Schraeder',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
            'cdt' => 'white and green transporter, gold hubs with SCHRAEDER 25 tampo',
            'tdt' => 'includes MB221 Chevy Lumina in white and green with gold disc wheels, China casting, and MB068 Chevy Van in white and green with gold hubs, Thailand casting, both with SCHRAEDER 25 tampos',],
	]]);

// TC-60-A PENNZOIL RACING TEAM, issued 1992
    show_tmtc(['id' => 'TC060A', 'name' => 'Pennzoil Racing Team Transporter', 'year' => '1992', 'fmt' => 'tall',
	'models' => [
// 1. Yellow transporter, Thailand casting; MB216 Pontiac in yellow, China casting; MB068 Chevy Van in yellow, Thailand casting-all with "Pennzoil" liveries (WR)
	    ['mod' => 'TC060A', 'var' => '01a', 'liv' => 'Pennzoil',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'yellow transporter with PENNZOIL tampo',
            'tdt' => 'includes MB216 Pontiac in yellow, China casting, and MB068 Chevy Van in yellow, Thailand casting, both with PENNZOIL tampos',],
	]]);

// TC-61-A STP (PETTY) TEAM, issued 1992
    show_tmtc(['id' => 'TC061A', 'name' => 'STP (Petty) Racing Team Transporter', 'year' => '1992', 'fmt' => 'tall',
	'models' => [
// 1. Blue transporter, Thailand casting; MB216 Pontiac in blue with blue wheels, China casting; MB068 Chevy Van in blue, Thailand casting - all with "STP Oil Treatment" liveries (WR)
	    ['mod' => 'TC061A', 'var' => '01a', 'liv' => 'STP',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'blue transporter with STP OIL TREATMENT tampo',
            'tdt' => 'includes MB216 Pontiac in blue with blue wheels, China casting, and MB068 Chevy Van in blue, Thailand casting, both with STP OIL TREATMENT tampos',],
	]]);

// TC-62-A MELLO YELLO RACING TEAM, issued 1992
    show_tmtc(['id' => 'TC062A', 'name' => 'Mello Yello Racing Team Transporter', 'year' => '1992', 'fmt' => 'tall',
	'models' => [
// 1. Black and green transporter, Thailand casting; MB216 Pontiac in green and black, China casting; MB068 Chevy Van in black and green, Thailand casting - all with "Mello Yello 42" liveries (WR)
	    ['mod' => 'TC062A', 'var' => '01a', 'liv' => 'Mello Yello',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'black and green transporter with MELLO YELLO 42 tampo',
            'tdt' => 'includes MB216 Pontiac in green and black, China casting, and MB068 Chevy Van in black and green, Thailand casting, both with MELLO YELLO 42 tampos',],
	]]);

// TC-63-A J.D. McDUFFIE RACING TEAM, issued 1992
    show_tmtc(['id' => 'TC063A', 'name' => 'McDuffie Racing Team Transporter', 'year' => '1992', 'fmt' => 'tall',
	'models' => [
// 1. Blue transporter, Thailand casting; MB216 Pontiac in blue, China casting; MB034 Chevy Prostocker in blue and white, Thailand casting-all with "Rumple 70," "Son's" or "J.D. McDuffie" liveries (WR)
	    ['mod' => 'TC063A', 'var' => '01a', 'liv' => 'McDuffie',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'blue transporter with J.D. MCDUFFIE tampo',
            'tdt' => "includes MB216 Pontiac in blue, China casting, and MB034 Chevy Prostocker in blue and white, Thailand casting, both with RUMPLE 70, SON'S or J.D. MCDUFFIE tampos",],
	]]);

// TC-64-A PONTIAC EXCITEMENT TEAM, issued 1992
    show_tmtc(['id' => 'TC064A', 'name' => 'Pontiac Excitement Team Racing Transporter', 'year' => '1992', 'fmt' => 'tall',
	'models' => [
// 1. Black transporter, Thailand casting; MB216 Pontiac in black, China casting; MB068 Chevy Van in black, Thailand casting - all with "Pontiac Excitement" and "Rusty Wallace" liveries (WR)
	    ['mod' => 'TC064A', 'var' => '01a', 'liv' => 'Pontiac',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'black transporter with PONTIAC EXCITEMENT and RUSTY WALLACE tampos',
            'tdt' => 'includes MB216 Pontiac in black, China casting, and MB068 Chevy Van in black, Thailand casting, both with PONTIAC EXCITEMENT and RUSTY WALLACE tampos',],
	]]);

// TC-65-A BILL ELLIOT RACING TEAM, issued 1992
    show_tmtc(['id' => 'TC065A', 'name' => 'Bill Elliot Racing Team Transporter', 'year' => '1992', 'fmt' => 'tall',
	'models' => [
// 1. Red transporter, Thailand casting; MB212 Ford Thunder-bird in red, China casting; MB053 Flareside Pickup in red, Thailand casting - all with "Bill Elliot 11 Racing" liveries (WR)
	    ['mod' => 'TC065A', 'var' => '01a', 'liv' => 'Bill Elliot',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'red transporter with BILL ELLIOT 11 RACING tampos',
            'tdt' => 'includes MB212 Ford Thunderbird in red, China casting, and MB053 Flareside Pickup in red, Thailand casting, both with BILL ELLIOT 11 RACING tampos',],
	]]);

// TC-66-A TEXACO/HAVOLINE TEAM, issued 1993
    show_tmtc(['id' => 'TC066A', 'name' => 'Texaco/Havoline Team Racing Transporter', 'year' => '1993', 'fmt' => 'tall',
	'models' => [
// 1. Black transporter, Thailand casting; MB221 Lumina in black, Thailand casting; MB212 Ford Thunderbird in matt black, Thailand casting - all in "Texaco/Havoline 28" tampo (WR)
	    ['mod' => 'TC066A', 'var' => '01a', 'liv' => 'Texaco',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'black transporter with TEXACO/HAVOLINE 28 tampo',
            'tdt' => 'includes MB221 Lumina in black, Thailand casting and MB212 Ford Thunderbird in matt black, Thailand casting, both with TEXACO/HAVOLINE 28 tampo',],
	]]);

// TC-67-A HOOTERS TEAM, issued 1993
    show_tmtc(['id' => 'TC067A', 'name' => 'Hooters Team Racing Transporter', 'year' => '1993', 'fmt' => 'tall',
	'models' => [
// 1. White transporter, Thailand casting; MB221 Lumina in white and orange, Thailand casting; MB212 Ford Thunder-bird in gray, Thailand casting-all with "Hooters 7" tampo (WR)
	    ['mod' => 'TC067A', 'var' => '01a', 'liv' => 'Hooters',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'white transporter with HOOTERS 7 tampo',
            'tdt' => 'includes MB221 Lumina in white and orange, Thailand casting and MB212 Ford Thunderbird in gray, Thailand casting, both with HOOTERS 7 tampo',],
	]]);

// TC-68-A COUNTRY TIME TEAM, issued 1993
    show_tmtc(['id' => 'TC068A', 'name' => 'Country Time Team Racing Transporter', 'year' => '1993', 'fmt' => 'tall',
	'models' => [
// 1. Yellow transporter, Thailand casting; MB212 Thunderbird in yellow, Thailand casting; MB212 Thunderbird in pink, Thailand casting - all with "Country Time 68" tampo (WR)
	    ['mod' => 'TC068A', 'var' => '01a', 'liv' => 'Country Time',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'yellow transporter with COUNTRY TIME 68 tampo',
            'tdt' => 'includes MB212 Thunderbird in yellow, Thailand casting; MB212 Thunderbird in pink, Thailand casting, both with COUNTRY TIME 68 tampo',],
	]]);

// TC-95-A AUTO PALACE RACING TEAM, issued 1995
    show_tmtc(['id' => 'TC095A', 'name' => 'Auto Palace Racing Team Transporter', 'year' => '1995', 'fmt' => 'tall',
	'models' => [
// 1. Blue and silver transporter, Thailand casting; MB194 Modified Racer in blue and silver, China casting. Both in "Auto Palace 95" liveries (PR)
	    ['mod' => 'TC095A', 'var' => '01a', 'liv' => 'Auto Palace',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
            'cdt' => 'blue and silver transporter with AUTO PALACE 95 tampo',
            'tdt' => 'MB194 Modified Racer in blue and silver, China casting, with AUTO PALACE 95 tampo',],
	]]);

// TC-95-B TEAM CATERPILLAR, issued 1996
    show_tmtc(['id' => 'TC095B', 'name' => 'Team Caterpillar Racing Transporter', 'year' => '1996', 'fmt' => 'tall',
	'models' => [
// 1. Yellow and black transporter, China casting; MB283 Chevy Monte Carlo in black and yellow, China casting; WR002 Ford Delivery in white, China casting - all with "95 Cat Racing" liveries (WR)
	    ['mod' => 'TC095B', 'var' => '01a', 'liv' => 'Caterpillar',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'China', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'yellow and black transporter with 95 CAT RACING tampo',
            'tdt' => 'includes MB283 Chevy Monte Carlo in black and yellow, China casting, and WR002 Ford Delivery in white, China casting, both with 95 CAT RACING tampos',],
	]]);

// TC-96-A TEAM McDONALD'S, issued 1996
    show_tmtc(['id' => 'TC096A', 'name' => "Team McDonald's Racing Transporter", 'year' => '1996', 'fmt' => 'tall',
	'models' => [
// 1. Red transporter with red wheels, China casting; WRP02 Ford Thunderbird in red and white with red wheels, China casting; WR002 Ford Delivery with red cab and white container, silver wheels, China casting - all with "94 "McDonald's" or "Bill Elliot" liveries (WR)
	    ['mod' => 'TC096A', 'var' => '01a', 'liv' => "McDonald's",
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'China', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => '', "red transporter with red wheels, with 94 MCDONALD'S, BILL ELLIOT tampo",
            'tdt' => "with WRP02 Ford Thunderbird in red and white with red wheels, China casting and WR002 Ford Delivery with red cab and white container, silver wheels, China casting, both with 94 MCDONALD'S or BILL ELLIOT tampos",],
	]]);

// TC-98-A TEAM BO JANGLES, issued 1994
    show_tmtc(['id' => 'TC098A', 'name' => 'Team Bo Jangles Racing Transporter', 'year' => '1994', 'fmt' => 'tall',
	'models' => [
// 1. Yellow transporter, Thailand casting; MB212 Thunderbird in yellow, Thailand casting; MB212 Thunderbird in black, Thailand casting - all in "Bojangles 98" tampo (WR)
	    ['mod' => 'TC098A', 'var' => '01a', 'liv' => 'Bo Jangles',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'yellow transporter, with BOJANGLES 98 tampo',
            'tdt' => 'includes MB212 Thunderbird in yellow, Thailand casting, and MB212 Thunderbird in black, Thailand casting, both in BOJANGLES 98 tampo',],
	]]);

// TC-98-B TEAM FINGERHUT, issued 1995
    show_tmtc(['id' => 'TC098B', 'name' => 'Team Fingerhut Racing Transporter', 'year' => '1995', 'fmt' => 'tall',
	'models' => [
// 1. Black transporter, Thailand casting; MB268 Ford Thunder-bird in black, China casting; MB068 Chevy Van in black, Thailand casting - all with "Fingerhut 98" liveries (WR)
	    ['mod' => 'TC098B', 'var' => '01a', 'liv' => 'Fingerhut',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
	    'nts' => 'Manufactured for White Rose',
            'cdt' => 'black transporter',
            'tdt' => 'includes MB268 Ford Thunderbird in black, China casting, and MB068 Chevy Van in black, Thailand casting, both with FINGERHUT 98 tampo',],
	]]);

// TC-111-A TEAM MITRE 10, issued 1993 (AU)
    show_tmtc(['id' => 'TC111A', 'name' => 'Team Mitre 10 Racing Transporter', 'year' => '1993', 'fmt' => 'tall',
	'models' => [
// 1. CY010 transporter in blue with MB137 F.1 Racer -"Mitre 10" tampo (AU)
	    ['mod' => 'TC111A', 'var' => '01a', 'liv' => 'Mitre 10',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand', 'cod' => '1',
            'cdt' => 'blue transporter',
            'tdt' => 'includes MB137 F.1 Racer with MITRE 10 tampo',],
	]]);

    end_table();
}
?>

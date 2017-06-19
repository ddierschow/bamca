<?php // DONE
$subtitle = '';
$desc = "Collectible Convoys";
$year = '1997 - 1999';
include "cypage.php";

function body() {
    global $subtitle;

    start_table();

// CCY-01 PETERBILT CONTAINER TRUCK, issued 1997
    show_tmtc(['id' => 'CCY01', 'name' => 'Peterbilt Container Truck', 'year' => '1997', 'fmt' => 'wide',
	'models' => [
// 1. Black cab with chrome airfoil cast, black container with silver-gray base, "Miller Genuine Draft" tampo
	    ['mod' => 'CCY01', 'var' => '01a', 'liv' => 'Miller',
	    'cab' => 'MB307', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'black with chrome airfoil cast',
            'tdt' => 'black container with silver-gray base, MILLER GENUINE DRAFT tampo ',],
	]]);

// CCY-02 FORD AEROMAX CONTAINER TRUCK, issued 1997
    show_tmtc(['id' => 'CCY02', 'name' => 'Ford Aeromax Container Truck', 'year' => '1997', 'fmt' => 'wide',
	'models' => [
// 1. Red cab with black chassis, white container with silver-gray base, "Red Dog- you are your own dog" tampo
	    ['mod' => 'CCY02', 'var' => '01a', 'liv' => 'Red Dog',
	    'cab' => 'MB308', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'red cab with black chassis',
            'tdt' => 'white container with silver-gray base, RED DOG - YOU ARE YOUR OWN DOG tampo',],
// 2. Black cab with black chassis, black container with silver-gray base, "Dos Equis XX" tampo
	    ['mod' => 'CCY02', 'var' => '02a', 'liv' => 'Dos Equis',
	    'cab' => 'MB308', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'black with black chassis',
            'tdt' => 'black container with silver-gray base, DOS EQUIS XX tampo',],
// 3. Black and green cab, black chassis, black container with silver-gray base, "Tomorrow's Thrills Today! Action Sportster"
	    ['mod' => 'CCY02', 'var' => '03a', 'liv' => "Tomorrow's Thrills Today",
	    'cab' => 'MB308', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'black and green, black chassis',
            'tdt' => "black container with silver-gray base, TOMORROW'S THRILLS TODAY ACTION SPORTSTER",],
	]]);

// CCY-03 KENWORTH CONTAINER TRUCK, issued 1997
    show_tmtc(['id' => 'CCY03', 'name' => 'Kenworth Container Truck', 'year' => '1997', 'fmt' => 'wide',
	'models' => [
// 1. Dark green cab, dark green container with silver-gray base, "The Moose Is Loose" tampo
	    ['mod' => 'CCY03', 'var' => '01a', 'liv' => 'Moosehead',
	    'cab' => 'MB309', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'dark green',
            'tdt' => 'dark green container with silver-gray base, THE MOOSE IS LOOSE tampo',],
// 2. Dark beige and gray cab, green container, "The Harley Davidson Motorcycle 1909" tampo
	    ['mod' => 'CCY03', 'var' => '02a', 'liv' => 'Harley Davidson',
	    'cab' => 'MB309', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'dark beige and gray',
            'tdt' => 'green container, THE HARLEY DAVIDSON MOTORCYCLE 1909 tampo',],
	]]);

// CCY-04 KENWORTH CONTAINER TRUCK, issued 1997
    show_tmtc(['id' => 'CCY04', 'name' => 'Kenworth Container Truck', 'year' => '1997', 'fmt' => 'wide',
	'models' => [
// 1. White and blue cab, white container with blue roof and silver-gray base, "Longnecks Corona Extra" tampo
	    ['mod' => 'CCY04', 'var' => '01a', 'liv' => 'Corona',
	    'cab' => 'MB310', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'white and blue',
            'tdt' => 'white container with blue roof and silver-gray base, LONGNECKS CORONA EXTRA tampo',],
// 2. Light pea green and gray cab, light orange container with silver-gray base, "1929 WL 45" Twin Harley-Davidson" tampo
	    ['mod' => 'CCY04', 'var' => '02a', 'liv' => 'Harley Davidson',
	    'cab' => 'MB310', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'light pea green and gray',
            'tdt' => 'light orange container with silver-gray base, 1929 WL 45" TWIN HARLEY-DAVIDSON tampo',],
	]]);

// CCY-05 MACK CONTAINER TRUCK, issued 1997
    show_tmtc(['id' => 'CCY05', 'name' => 'Mack Container Truck', 'year' => '1997', 'fmt' => 'wide',
	'models' => [
// 1. Orange and red cab with black chassis, orange container with silver-gray base, "Honey Brown Lager" tampo
	    ['mod' => 'CCY05', 'var' => '01a', 'liv' => 'Honey Brown Lager',
	    'cab' => 'MB311', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'orange and red with black chassis',
            'tdt' => 'orange container with silver-gray base, HONEY BROWN LAGER tampo',],
// 2. Black cab and chassis, black container, with silver-gray base, "Built Like A Mack Truck" tampo
	    ['mod' => 'CCY05', 'var' => '02a', 'liv' => 'Mack',
	    'cab' => 'MB311', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'black and chassis',
            'tdt' => 'black container, with silver-gray base, BUILT LIKE A MACK TRUCK tampo',],
// 3. Dark blue cab with black chassis, dark blue container with silver-gray base, "Labatt Blue" tampo
	    ['mod' => 'CCY05', 'var' => '03a', 'liv' => 'Labatt',
	    'cab' => 'MB311', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'dark blue with black chassis',
            'tdt' => 'dark blue container with silver-gray base, LABATT BLUE tampo',],
// 4. Yellow cab with black chassis, yellow container with black base, "Harley-Davidson 1948 740HVTwin Panhead" tampo
	    ['mod' => 'CCY05', 'var' => '04a', 'liv' => 'Harley Davidson',
	    'cab' => 'MB311', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'yellow with black chassis',
            'tdt' => 'yellow container with black base, HARLEY-DAVIDSON 1948 740HVTWIN PANHEAD tampo',],
	]]);

// CCY-06 PETERBILT CONTAINER TRUCK, issued 1997
    show_tmtc(['id' => 'CCY06', 'name' => 'Peterbilt Container Truck', 'year' => '1997', 'fmt' => 'wide',
	'models' => [
// 1. White and red cab, red container with silver-gray base, "PBRme ASAP! Pabst Blue Ribbon" tampo
	    ['mod' => 'CCY06', 'var' => '01a', 'liv' => 'Pabst',
	    'cab' => 'MB307', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'white and red',
            'tdt' => 'red container with silver-gray base, PBRME ASAP! PABST BLUE RIBBON tampo',],
// 2. Black cab, black container with dark gray base, "Jim Beam" tampo
	    ['mod' => 'CCY06', 'var' => '02a', 'liv' => 'Jim Beam',
	    'cab' => 'MB307', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'black',
            'tdt' => 'black container with dark gray base, JIM BEAM tampo',],
// 3. Red cab, red container with silver-gray base, "Budweiser King of Beers" tampo
	    ['mod' => 'CCY06', 'var' => '03a', 'liv' => 'Budweiser',
	    'cab' => 'MB307', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'red',
            'tdt' => 'red container with silver-gray base, BUDWEISER KING OF BEERS tampo',],
// 4. Brown and beige cab, brown container with silver-gray base, "61 OHV Knucklehead Harley Davidson 1937" tampo
	    ['mod' => 'CCY06', 'var' => '04a', 'liv' => 'Harley Davidson',
	    'cab' => 'MB307', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'brown and beige',
            'tdt' => 'brown container with silver-gray base, 61 OHV KNUCKLEHEAD HARLEY DAVIDSON 1937 tampo',],
	]]);

// CCY-07 SCANIA CONTAINER TRUCK, issued 1998
    show_tmtc(['id' => 'CCY07', 'name' => 'Scania Container Truck', 'year' => '1998', 'fmt' => 'wide',
	'models' => [
// 1. White cab with black chassis, white container with black base, "Skol Skol" tampo
	    ['mod' => 'CCY07', 'var' => '01a', 'liv' => 'Skol',
	    'cab' => 'MB341', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'white with black chassis',
            'tdt' => 'white container with black base, SKOL SKOL tampo',],
// 2. White cab with black chassis, white container with black base, "XXXX Castlemaine" tampo
	    ['mod' => 'CCY07', 'var' => '02a', 'liv' => 'Castlemaine',
	    'cab' => 'MB341', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'white with black chassis',
            'tdt' => 'white container with black base, XXXX CASTLEMAINE tampo',],
	]]);

// CCY-08 DAF CONTAINER TRUCK, issued 1998
    show_tmtc(['id' => 'CCY08', 'name' => 'DAF Container Truck', 'year' => '1998', 'fmt' => 'wide',
	'models' => [
// 1. Dark green cab with black chassis, orange-yellow container with green roof and silver-gray base, "Holsten Pils" tampo
	    ['mod' => 'CCY08', 'var' => '01a', 'liv' => 'Holsten',
	    'cab' => 'MB340', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'dark green with black chassis',
            'tdt' => 'orange-yellow container with green roof and silver-gray base, HOLSTEN PILS tampo',],
	]]);

// CCY-09 PETERBILT TANKER, issued 1998
    show_tmtc(['id' => 'CCY09', 'name' => 'Peterbilt Tanker ', 'year' => '1998', 'fmt' => 'wide',
	'models' => [
// 1. Black cab, silver-gray tank and base, "Take It To The Star Texaco" tampo
	    ['mod' => 'CCY09', 'var' => '01a', 'liv' => 'Texaco',
	    'cab' => 'MB307', 'tlr' => 'Ultra Tanker', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'black',
            'tdt' => 'silver-gray tank and base, TAKE IT TO THE STAR TEXACO tampo',],
	]]);

// CCY-10 FORD AEROMAX TANKER, issued 1998
    show_tmtc(['id' => 'CCY10', 'name' => 'Ford Aeromax Tanker', 'year' => '1998', 'fmt' => 'wide',
	'models' => [
// 1. Dark blue cab with silver-gray chassis, silver-gray tank and base, "Sunoco Ultra 94 Octane" tampo
	    ['mod' => 'CCY10', 'var' => '01a', 'liv' => 'Sunoco',
	    'cab' => 'MB308', 'tlr' => 'Ultra Tanker', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'dark blue with silver-gray chassis',
            'tdt' => 'silver-gray tank and base, SUNOCO ULTRA 94 OCTANE tampo',],
	]]);

// CCY-11 MACK TANKER, issued 1998
    show_tmtc(['id' => 'CCY11', 'name' => 'Mack Tanker', 'year' => '1998', 'fmt' => 'wide',
	'models' => [
// 1. White cab with gray chassis, white tank with gray base, "Citgo the Sign of Quality" tampo
	    ['mod' => 'CCY11', 'var' => '01a', 'liv' => 'Citgo',
	    'cab' => 'MB311', 'tlr' => 'Ultra Tanker', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'white with gray chassis',
            'tdt' => 'white tank with gray base, CITGO THE SIGN OF QUALITY tampo',],
// 2. Yellow cab with light gray chassis, chrome tank with light gray base, "Formula Shell" tampo
	    ['mod' => 'CCY11', 'var' => '02a', 'liv' => 'Shell',
	    'cab' => 'MB311', 'tlr' => 'Ultra Tanker', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'yellow with light gray chassis',
            'tdt' => 'chrome tank with light gray base, FORMULA SHELL tampo',],
	]]);

// CCY-12 KENWORTH TANKER, issued 1998
    show_tmtc(['id' => 'CCY12', 'name' => 'Kenworth Tanker', 'year' => '1998', 'fmt' => 'wide',
	'models' => [
// 1. Gray cab, silver-gray tank and base, "Mobil" tampo
	    ['mod' => 'CCY12', 'var' => '01a', 'liv' => 'Mobil',
	    'cab' => 'MB310', 'tlr' => 'Ultra Tanker', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'gray',
            'tdt' => 'silver-gray tank and base, MOBIL tampo',],
	]]);

// CCY-13 DAF TANKER, issued 1998
    show_tmtc(['id' => 'CCY13', 'name' => 'DAF Tanker', 'year' => '1998', 'fmt' => 'wide',
	'models' => [
// 1. White and green cab with gray chassis, green and white tank with gray base, "BP" tampo
	    ['mod' => 'CCY13', 'var' => '01a', 'liv' => 'BP',
	    'cab' => 'MB340', 'tlr' => 'Ultra Tanker', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'white and green with gray chassis',
            'tdt' => 'green and white tank with gray base, BP tampo',],
	]]);

// CCY-14 PETERBILT BOX TRUCK, issued 1999
    show_tmtc(['id' => 'CCY14', 'name' => 'Peterbilt Box Truck', 'year' => '1999', 'fmt' => 'wide',
	'models' => [
// 1. Black cab with chrome roof airfoil, red container with silver-gray base, "Harley Davidson 1966 Electra-Glide" tampo
	    ['mod' => 'CCY14', 'var' => '01a', 'liv' => 'Harley Davidson',
	    'cab' => 'MB307', 'tlr' => 'Ultra Container', 'mfg' => 'China', 'cod' => '1',
            'cdt' => 'black with chrome roof airfoil',
            'tdt' => 'red container with silver-gray base, HARLEY DAVIDSON 1966 ELECTRA-GLIDE tampo',],
	]]);

    end_table();
}
?>

<?php // DONE
$subtitle = 'CY024A';
// CY-24-A DAF BOX TRUCK, issued 1988
$desc = "DAF Box Truck";
$year = '1988';
include "cypage.php";

function body() {
    global $subtitle;

    echo "<small>Most of these convoys were issued as part of <br> sets and not as single models</small><b><br>\n";

    show_table([
// 1. Red cab with black chassis, red container with pearly silver base, "Ferrari" tampo, Macau
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Macau',
	    'liv' => 'Ferrari', 'cod' => '1', 'rar' => '2',
            'cdt' => 'red with black chassis',
            'tdt' => 'red container with pearly silver base, FERRARI tampo',
	],
// 2. Blue cab with black chassis, blue container with black base, "Pickfords" tampo, Macau
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Macau',
	    'liv' => 'Pickfords', 'cod' => '1', 'rar' => '2',
            'cdt' => 'blue with black chassis',
            'tdt' => 'blue container with black base, PICKFORDS tampo',
	],
// 3. White cab with black chassis, white container with pearly silver base, "Porsche" labels, Macau
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Macau',
	    'liv' => 'Porsche', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white with black chassis',
            'tdt' => 'white container with pearly silver base, PORSCHE labels',
	],
// 4. White cab with black chassis, white container with pearly silver base, "Porsche" tampo, Thailand
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Porsche', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white with black chassis',
            'tdt' => 'white container with pearly silver base, PORSCHE labels',
	],
// 5. Red cab with black chassis, dark red container with pearly silver base, "Ferrari" tampo, Thailand
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Ferrari', 'cod' => '1', 'rar' => '2',
            'cdt' => 'red with black chassis',
            'tdt' => 'dark red container with pearly silver base, FERRARI tampo',
	],
// 6. White cab with red chassis, white container with red base, "Circus Circus" labels, Thailand (MC)
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Circus Circus', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white with red chassis',
            'tdt' => 'white container with red base, CIRCUS CIRCUS labels',
	],
// 7. White cab with black chassis, white container with black base, Thailand, "Saudia" labels (SU)
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Saudia', 'cod' => '1', 'rar' => '3',
            'cdt' => 'white with black chassis',
            'tdt' => 'white container with black base, SAUDIA labels',
	],
// 8. Blue body with black chassis, blue container with black base, Thailand, "Mitre 10 Racing" labels (AU)(TC)
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Mitre 10', 'cod' => '1', 'rar' => '2',
            'cdt' => 'blue with black chassis',
            'tdt' => 'blue container with black base, MITRE 10 RACING labels',
	],
// 9. White body with black chassis, black container with black base, Thailand, "Bassett's Liquorice Allsorts" labels (UK)
	['mod' => $subtitle, 'var' => '09a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Basset', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white with black chassis',
            'tdt' => "black container with black base, BASSETT'S LIQUORICE ALLSORTS labels",
	],
// 10. White body with black chassis, yellow container with black base, Thailand, "Bassett's Jelly Babies" labels (UK)
	['mod' => $subtitle, 'var' => '10a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Basset', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white body with black chassis',
            'tdt' => "yellow container with black base, BASSETT'S JELLY BABIES labels",
	],
// 11. Dark green body with green chassis, dark green container with black base, Thailand, "Jaguar" tampo (GS)
	['mod' => $subtitle, 'var' => '11a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Jaguar', 'cod' => '1', 'rar' => '2',
            'cdt' => 'dark green body with green chassis',
            'tdt' => 'dark green container with black base, JAGUAR tampo',
	],
// 12. Orange/red cab with white roof with black chassis, orange/red container with black base, Thailand, "Parcel Post" labels (AU)(GS)
	['mod' => $subtitle, 'var' => '12a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Parcel Post', 'cod' => '1', 'rar' => '2',
            'cdt' => 'orange-red with white roof, black chassis',
            'tdt' => 'orange-red container with black base, PARCEL POST labels',
	],
// 13. White cab with dark blue chassis, white container with dark blue base, Thailand, "Renault Elf/Canon Williams" labels (MN)
	['mod' => $subtitle, 'var' => '13a',
	    'cab' => 'MB183', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Renault', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white with dark blue chassis',
            'tdt' => 'white container with dark blue base, RENAULT ELF/CANON WILLIAMS labels',
	],
    ]);
}
?>

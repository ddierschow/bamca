<?php // DONE
$subtitle = 'CY024A';
// CY-24-A DAF BOX TRUCK, issued 1988
$desc = "DAF Box Truck";
$year = '1988';

$defaults = ['mod' => $subtitle, 'cab' => 'MB183', 'tlr' => 'CYT17', 'cod' => '1'];

include "cypage.php";

function body() {
    echo "<small>Most of these convoys were issued as part of sets and not as single models</small><br>\n";

    show_table([
// 1. Red cab with black chassis, red container with pearly silver base, "Ferrari" tampo, Macau
	['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Ferrari', 'rar' => '2',
            'cdt' => 'red with black chassis',
            'tdt' => 'red container with pearly silver base, FERRARI tampo',
	],
// 2. Blue cab with black chassis, blue container with black base, "Pickfords" tampo, Macau
	['var' => '02a', 'mfg' => 'Macau', 'liv' => 'Pickfords', 'rar' => '2',
            'cdt' => 'blue with black chassis',
            'tdt' => 'blue container with black base, PICKFORDS tampo',
	],
// 3. White cab with black chassis, white container with pearly silver base, "Porsche" labels, Macau
	['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Porsche', 'rar' => '2',
            'cdt' => 'white with black chassis',
            'tdt' => 'white container with pearly silver base, PORSCHE labels',
	],
// 4. White cab with black chassis, white container with pearly silver base, "Porsche" tampo, Thailand
	['var' => '04a', 'mfg' => 'Thailand', 'liv' => 'Porsche', 'rar' => '2',
            'cdt' => 'white with black chassis',
            'tdt' => 'white container with pearly silver base, PORSCHE labels',
	],
// 5. Red cab with black chassis, dark red container with pearly silver base, "Ferrari" tampo, Thailand
	['var' => '05a', 'mfg' => 'Thailand', 'liv' => 'Ferrari', 'rar' => '2',
            'cdt' => 'red with black chassis',
            'tdt' => 'dark red container with pearly silver base, FERRARI tampo',
	],
// 6. White cab with red chassis, white container with red base, "Circus Circus" labels, Thailand (MC)
	['var' => '06a', 'mfg' => 'Thailand', 'liv' => 'Circus Circus', 'rar' => '2',
            'cdt' => 'white with red chassis',
            'tdt' => 'white container with red base, CIRCUS CIRCUS labels',
	],
// 7. White cab with black chassis, white container with black base, Thailand, "Saudia" labels (SU)
	['var' => '07a', 'mfg' => 'Thailand', 'liv' => 'Saudia', 'rar' => '3',
            'cdt' => 'white with black chassis',
            'tdt' => 'white container with black base, SAUDIA labels',
	],
// 8. Blue body with black chassis, blue container with black base, Thailand, "Mitre 10 Racing" labels (AU)(TC)
	['var' => '08a', 'mfg' => 'Thailand', 'liv' => 'Mitre 10', 'rar' => '2',
            'cdt' => 'blue with black chassis',
            'tdt' => 'blue container with black base, MITRE 10 RACING labels',
	],
// 9. White body with black chassis, black container with black base, Thailand, "Bassett's Liquorice Allsorts" labels (UK)
	['var' => '09a', 'mfg' => 'Thailand', 'liv' => 'Basset', 'rar' => '2',
            'cdt' => 'white with black chassis',
            'tdt' => "black container with black base, BASSETT'S LIQUORICE ALLSORTS labels",
	],
// 10. White body with black chassis, yellow container with black base, Thailand, "Bassett's Jelly Babies" labels (UK)
	['var' => '10a', 'mfg' => 'Thailand', 'liv' => 'Basset', 'rar' => '2',
            'cdt' => 'white body with black chassis',
            'tdt' => "yellow container with black base, BASSETT'S JELLY BABIES labels",
	],
// 11. Dark green body with green chassis, dark green container with black base, Thailand, "Jaguar" tampo (GS)
	['var' => '11a', 'mfg' => 'Thailand', 'liv' => 'Jaguar', 'rar' => '2',
            'cdt' => 'dark green body with green chassis',
            'tdt' => 'dark green container with black base, JAGUAR tampo',
	],
// 12. Orange/red cab with white roof with black chassis, orange/red container with black base, Thailand, "Parcel Post" labels (AU)(GS)
	['var' => '12a', 'mfg' => 'Thailand', 'liv' => 'Parcel Post', 'rar' => '2',
            'cdt' => 'orange-red with white roof, black chassis',
            'tdt' => 'orange-red container with black base, PARCEL POST labels',
	],
// 13. White cab with dark blue chassis, white container with dark blue base, Thailand, "Renault Elf/Canon Williams" labels (MN)
	['var' => '13a', 'mfg' => 'Thailand', 'liv' => 'Renault', 'rar' => '2',
            'cdt' => 'white with dark blue chassis',
            'tdt' => 'white container with dark blue base, RENAULT ELF/CANON WILLIAMS labels',
	],
    ]);
}
?>

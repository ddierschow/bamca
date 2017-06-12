<?php // DONE
$subtitle = 'CY011A';
// CY-11-A KENWORTH HELICOPTER TRANSPORTER, issued 1983
$desc = "Kenworth Helicopter Transporters";
$year = '1983';
include "cypage.php";

function body() {
    global $subtitle;

// NOTE: Helicopter comes in combinations of clear or amber windows, orange or black base, and gray or black interior to make additional permutations to this list.
    show_table([
// 1. Silver-gray cab with "Ace Hire" tampo, chrome exhausts; MB75-D Helicopter in silver-gray with "-600-" tampo, silver-gray trailer, England
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB045', 'tlr' => 'Helicopter Transporter', 'mfg' => 'England',
	    'liv' => 'Ace Hire', 'cod' => '1', 'rar' => '',
            'cdt' => 'silver-gray with ACE HIRE tampo, chrome exhausts',
            'tdt' => 'silver-gray with silver MB075 helicopter, 600 tampo',
	],
// 2. Pearly silver cab with "Ace Hire" tampo, chrome exhausts; MB75-D Helicopter in pearly silver with "-600-" tampo, pearly silver trailer, Macau
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB045', 'tlr' => 'Helicopter Transporter', 'mfg' => 'Macau',
	    'liv' => 'Ace Hire', 'cod' => '1', 'rar' => '',
            'cdt' => 'silver-gray with ACE HIRE tampo, chrome exhausts',
            'tdt' => 'pearly silver with pearly silver MB075 helicopter, 600 tampo',
	],
// 3. Black cab with "Air Car" tampo, chrome exhausts; MB75-D Helicopter in black with "Air Car" tampo, pearly silver trailer, Macau
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB045', 'tlr' => 'Helicopter Transporter', 'mfg' => 'Macau',
	    'liv' => 'Air Car', 'cod' => '1', 'rar' => '',
            'cdt' => 'black with AIR CAR tampo, chrome exhausts',
            'tdt' => 'MB075 helicopter in black with AIR CAR tampo, pearly silver trailer',
	],
// 4. Black cab with "Air Car" tampo, gray exhausts; MB75-D Helicopter in black with "Air Car" tampo, pearly silver trailer, Macau
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB045', 'tlr' => 'Helicopter Transporter', 'mfg' => 'Macau',
	    'liv' => 'Air Car', 'cod' => '1', 'rar' => '',
            'cdt' => 'black with AIR CAR tampo, gray exhausts',
            'tdt' => 'MB075 helicopter in black with AIR CAR tampo, pearly silver trailer',
	],
// 5. Dark blue cab with white and gold stripes tampo, chrome exhausts; MB75-D Helicopter in white with "Rescue" tampo, pearly silver trailer, Macau (MC)
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB045', 'tlr' => 'Helicopter Transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark blue cab with white and gold stripes tampo, chrome exhausts',
            'tdt' => 'MB075 helicopter in white with RESCUE tampo, pearly silver trailer',
	],
// 6. Dark blue cab with white and gold stripes tampo, gray exhausts; MB75-D Helicopter in white with "Rescue" tampo, pearly silver trailer, Macau (MC)
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB045', 'tlr' => 'Helicopter Transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark blue cab with white and gold stripes tampo, gray exhausts',
            'tdt' => 'MB075 helicopter in white with RESCUE tampo, pearly silver trailer',
	],
// 7. Black cab with "Air Car" tampo, gray exhausts; MB75-D Helicopter in black with "Air Car" tampo, pearly silver trailer, Thailand
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB045', 'tlr' => 'Helicopter Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Air Car', 'cod' => '1', 'rar' => '',
            'cdt' => 'black with AIR CAR tampo, gray exhausts',
            'tdt' => 'MB075 helicopter in black with AIR CAR tampo, pearly silver trailer',
	],
// 8. Dark blue cab with white and gold stripes tampo, gray exhausts; MB75-D Helicopter in white with "Rescue" tampo, pearly silver trailer, Thailand (MC)
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB045', 'tlr' => 'Helicopter Transporter', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark blue cab with white and gold stripes tampo, gray exhausts',
            'tdt' => 'MB075 helicopter in white with RESCUE tampo, pearly silver trailer',
	],
    ]);
}
?>

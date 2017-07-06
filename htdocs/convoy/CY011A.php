<?php // DONE
$subtitle = 'CY011A';
// CY-11-A KENWORTH HELICOPTER TRANSPORTER, issued 1983
$desc = "Kenworth Helicopter Transporters";
$year = '1983';

$defaults = ['mod' => $subtitle, 'cab' => 'MB045', 'tlr' => 'CYT07', 'cod' => '1'];

// NOTE: Helicopter comes in combinations of clear or amber windows, orange or black base, and gray or black interior to make additional permutations to this list.
$models = [
// 1. Silver-gray cab with "Ace Hire" tampo, chrome exhausts; MB75-D Helicopter in silver-gray with "-600-" tampo, silver-gray trailer, England
    ['var' => '01a', 'mfg' => 'England', 'liv' => 'Ace Hire',
	'cdt' => 'silver-gray with ACE HIRE tampo, chrome exhausts', 'cva' => '010',
	'tdt' => 'silver-gray with silver MB075 helicopter, 600 tampo',
    ],
// 2. Pearly silver cab with "Ace Hire" tampo, chrome exhausts; MB75-D Helicopter in pearly silver with "-600-" tampo, pearly silver trailer, Macau
    ['var' => '02a', 'mfg' => 'Macau', 'liv' => 'Ace Hire',
	'cdt' => 'silver-gray with ACE HIRE tampo, chrome exhausts', 'cva' => '010',
	'tdt' => 'pearly silver with pearly silver MB075 helicopter, 600 tampo',
    ],
// 3. Black cab with "Air Car" tampo, chrome exhausts; MB75-D Helicopter in black with "Air Car" tampo, pearly silver trailer, Macau
    ['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Air Car',
	'cdt' => 'black with AIR CAR tampo, chrome exhausts', 'cva' => '023',
	'tdt' => 'MB075 helicopter in black with AIR CAR tampo, pearly silver trailer',
    ],
// 4. Black cab with "Air Car" tampo, gray exhausts; MB75-D Helicopter in black with "Air Car" tampo, pearly silver trailer, Macau
    ['var' => '04a', 'mfg' => 'Macau', 'liv' => 'Air Car',
	'cdt' => 'black with AIR CAR tampo, gray exhausts', 'cva' => '051',
	'tdt' => 'MB075 helicopter in black with AIR CAR tampo, pearly silver trailer',
    ],
// 5. Dark blue cab with white and gold stripes tampo, chrome exhausts; MB75-D Helicopter in white with "Rescue" tampo, pearly silver trailer, Macau (MC)
    ['var' => '05a', 'mfg' => 'Macau', 'liv' => 'none',
	'cdt' => 'dark blue cab with white and gold stripes tampo, chrome exhausts', 'cva' => '024',
	'tdt' => 'MB075 helicopter in white with RESCUE tampo, pearly silver trailer',
    ],
// 6. Dark blue cab with white and gold stripes tampo, gray exhausts; MB75-D Helicopter in white with "Rescue" tampo, pearly silver trailer, Macau (MC)
    ['var' => '06a', 'mfg' => 'Macau', 'liv' => 'none',
	'cdt' => 'dark blue cab with white and gold stripes tampo, gray exhausts', 'cva' => '055',
	'tdt' => 'MB075 helicopter in white with RESCUE tampo, pearly silver trailer',
    ],
// 7. Black cab with "Air Car" tampo, gray exhausts; MB75-D Helicopter in black with "Air Car" tampo, pearly silver trailer, Thailand
    ['var' => '07a', 'mfg' => 'Thailand', 'liv' => 'Air Car',
	'cdt' => 'black with AIR CAR tampo, gray exhausts', 'cva' => '051',
	'tdt' => 'MB075 helicopter in black with AIR CAR tampo, pearly silver trailer',
    ],
// 8. Dark blue cab with white and gold stripes tampo, gray exhausts; MB75-D Helicopter in white with "Rescue" tampo, pearly silver trailer, Thailand (MC)
    ['var' => '08a', 'mfg' => 'Thailand', 'liv' => 'none',
	'cdt' => 'dark blue cab with white and gold stripes tampo, gray exhausts', 'cva' => '055',
	'tdt' => 'MB075 helicopter in white with RESCUE tampo, pearly silver trailer',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>

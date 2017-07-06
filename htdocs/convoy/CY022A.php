<?php // DONE
$subtitle = 'CY022A';
// CY-22-A DAF BOAT TRANSPORTER, issued 1987
$desc = "DAF Boat Transporter";
$year = '1987';

$defaults = ['mod' => $subtitle, 'cab' => 'MB183', 'tlr' => 'CYT14', 'cod' => '1'];

$models = [
// 1. White cab, blue chassis with "Lakeside" tampo, dark blue trailer, boat with white deck, red hull and "Shark" tampo, Macau casting 
    ['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Lakeside',
	'cdt' => 'white, blue chassis, LAKESIDE tampo', 'cva' => '03',
	'tdt' => 'dark blue, boat with white deck, red hull and SHARK tampo',
    ],
// 2. White cab, blue chassis with "P and G" tampo, dark blue trailer, boat with white deck, orange-brown hull and "CG22" tampo, Macau casting 
    ['var' => '02a', 'mfg' => 'Macau', 'liv' => 'P and G',
	'cdt' => 'white, blue chassis, P&amp;G tampo', 'cva' => '06',
	'tdt' => 'dark blue, boat with white deck, orange-brown hull and CG22 tampo',
    ],
// 3. White cab, black chassis with "Coast Guard" tampo, black trailer, boat with gray deck, white hull and "Coast Guard" tampo, Macau casting 
    ['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Coast Guard',
	'cdt' => 'white, black chassis, COAST GUARD tampo', 'cva' => '14',
	'tdt' => 'black trailer, boat with gray deck, white hull and COAST GUARD tampo',
    ],
// 4. White cab, black chassis with "Coast Guard" tampo, black trailer, boat with gray deck, white hull and "Coast Guard" tampo, Thailand casting 
    ['var' => '04a', 'mfg' => 'Thailand', 'liv' => 'Coast Guard',
	'cdt' => 'white, black chassis, COAST GUARD tampo', 'cva' => '14',
	'tdt' => 'black trailer, boat with gray deck, white hull and COAST GUARD tampo',
    ],
// 5. White cab, florescent orange chassis with "Rescue 3" and checkers tampo, florescent orange trailer, boat with florescent orange deck, white hull and "Marine Rescue" tampo, Thailand casting (EM)
    ['var' => '05a', 'mfg' => 'Thailand', 'liv' => 'Rescue',
	'cdt' => 'white, florescent orange chassis, RESCUE 3 and checkers tampo', 'cva' => '38',
	'tdt' => 'florescent orange, boat with florescent orange deck, white hull and MARINE RESCUE tampo',
    ],
// 6. Turquoise cab, black chassis with white splash tampo, black trailer, boat with white deck and hull and two-tone blue tampo, China and "Mattel" casting (ROW)
    ['var' => '06a', 'mfg' => 'China, MATTEL', 'liv' => 'none',
	'cdt' => 'turquoise, black chassis, white splash tampo', 'cva' => '56',
	'tdt' => 'black, boat with white deck and hull and two-tone blue tampo',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>

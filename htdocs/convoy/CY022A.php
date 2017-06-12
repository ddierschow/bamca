<?php // DONE
$subtitle = 'CY022A';
// CY-22-A DAF BOAT TRANSPORTER, issued 1987
$desc = "DAF Boat Transporter";
$year = '1987';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. White cab, blue chassis with "Lakeside" tampo, dark blue trailer, boat with white deck, red hull and "Shark" tampo, Macau casting 
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB183', 'tlr' => 'Boat Transporter', 'mfg' => 'Macau',
	    'liv' => 'Lakeside', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, blue chassis, LAKESIDE tampo',
            'tdt' => 'dark blue, boat with white deck, red hull and SHARK tampo',
	],
// 2. White cab, blue chassis with "P and G" tampo, dark blue trailer, boat with white deck, orange-brown hull and "CG22" tampo, Macau casting 
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB183', 'tlr' => 'Boat Transporter', 'mfg' => 'Macau',
	    'liv' => 'P and G', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, blue chassis, P&amp;G tampo',
            'tdt' => 'dark blue, boat with white deck, orange-brown hull and CG22 tampo',
	],
// 3. White cab, black chassis with "Coast Guard" tampo, black trailer, boat with gray deck, white hull and "Coast Guard" tampo, Macau casting 
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB183', 'tlr' => 'Boat Transporter', 'mfg' => 'Macau',
	    'liv' => 'Coast Guard', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, black chassis, COAST GUARD tampo',
            'tdt' => 'black trailer, boat with gray deck, white hull and COAST GUARD tampo',
	],
// 4. White cab, black chassis with "Coast Guard" tampo, black trailer, boat with gray deck, white hull and "Coast Guard" tampo, Thailand casting 
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB183', 'tlr' => 'Boat Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Coast Guard', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, black chassis, COAST GUARD tampo',
            'tdt' => 'black trailer, boat with gray deck, white hull and COAST GUARD tampo',
	],
// 5. White cab, florescent orange chassis with "Rescue 3" and checkers tampo, florescent orange trailer, boat with florescent orange deck, white hull and "Marine Rescue" tampo, Thailand casting (EM)
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB183', 'tlr' => 'Boat Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Rescue', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, florescent orange chassis, RESCUE 3 and checkers tampo',
            'tdt' => 'florescent orange, boat with florescent orange deck, white hull and MARINE RESCUE tampo',
	],
// 6. Turquoise cab, black chassis with white splash tampo, black trailer, boat with white deck and hull and two-tone blue tampo, China and "Mattel" casting (ROW)
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB183', 'tlr' => 'Boat Transporter', 'mfg' => 'China, MATTEL',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'turquoise, black chassis, white splash tampo',
            'tdt' => 'black, boat with white deck and hull and two-tone blue tampo',
	],
    ]);
}
?>

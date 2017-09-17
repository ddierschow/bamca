<?php // DONE
$subtitle = 'CY110A';
// CY-110-A KENWORTH SUPERSTAR TRANSPORTER, issued 1992
$desc = "Kenworth Superstar Transporter";
$year = '1992';

$defaults = ['mod' => $subtitle, 'cab' => 'MB045', 'tlr' => 'CYT18', 'cod' => '1'];

// NOTE: All models with 8-spoke wheels and no antennas cast unless otherwise noted.
$models = [
// 1. Black cab, black container, "Rusty Wallace-Pontiac" labels (WR)
    ['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Pontiac', 'cod' => '2',
	'cdt' => 'black', 'cva' => '066',
	'tdt' => "black container, RUSTY WALLACE-PONTIAC labels",
	'nts' => 'Manufactured for White Rose',
    ],
// 2. Black cab, black container, "TIC Racing 8" labels (WR)
    ['var' => '02a', 'mfg' => 'Macau', 'liv' => 'TIC Racing', 'cod' => '2',
	'cdt' => 'black', 'cva' => '068',
	'tdt' => "black container, TIC RACING 8 labels",
	'nts' => 'Manufactured for White Rose',
    ],
// 3. Orange cab, black container, "Pic N Pay Shoes" labels (WR)
    ['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Pic N Pay Shoes', 'cod' => '2',
	'cdt' => 'orange', 'cva' => '070',
	'tdt' => "black container, PIC N PAY SHOES labels",
	'nts' => 'Manufactured for White Rose',
    ],
// NOTE: Versions 4-6 with rubber tires and antennas cast
// 4. Green cab, green container, "Mayflower" tempa (PC)
    ['var' => '04a', 'cab' => 'MB309', 'mfg' => 'Macau', 'liv' => 'Mayflower',
	'cdt' => 'green', 'cva' => '084',
	'tdt' => "green container, MAYFLOWER tempa",
    ],
// 5. Black cab, black container, "Jiffy Lube-Drive In Drive Out Drive On" tempa (PC)
    ['var' => '05a', 'cab' => 'MB309', 'mfg' => 'Macau', 'liv' => 'Jiffy Lube',
	'cdt' => 'black', 'cva' => 'F01',
	'tdt' => "black container, JIFFY LUBE-DRIVE IN DRIVE OUT DRIVE ON tempa",
    ],
// 6. Gray cab, white container, "Snap-On" tempa (PC)
    ['var' => '06a', 'cab' => 'MB309', 'mfg' => 'Macau', 'liv' => 'Snap-On',
	'cdt' => 'gray', 'cva' => '',
	'tdt' => "white container, SNAP-ON tempa",
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>

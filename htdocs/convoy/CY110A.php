<?php // DONE
$subtitle = 'CY110A';
// CY-110-A KENWORTH SUPERSTAR TRANSPORTER, issued 1992
$desc = "Kenworth Superstar Transporter";
$year = '1992';

$defaults = ['mod' => $subtitle, 'cab' => 'MB045', 'tlr' => 'Superstar Transporter', 'cod' => '1'];

include "cypage.php";

function body() {
// NOTE: All models with 8-spoke wheels and no antennas cast unless otherwise noted.
    show_table([
// 1. Black cab, black container, "Rusty Wallace-Pontiac" labels (WR)
	['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Pontiac', 'cod' => '2',
	    'cdt' => 'black',
	    'tdt' => "black container, RUSTY WALLACE-PONTIAC labels",
        ],
// 2. Black cab, black container, "TIC Racing 8" labels (WR)
	['var' => '02a', 'mfg' => 'Macau', 'liv' => 'TIC Racing', 'cod' => '2',
	    'cdt' => 'black',
	    'tdt' => "black container, TIC RACING 8 labels",
        ],
// 3. Orange cab, black container, "Pic N Pay Shoes" labels (WR)
	['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Pic N Pay Shoes', 'cod' => '2',
	    'cdt' => 'orange',
	    'tdt' => "black container, PIC N PAY SHOES labels",
        ],
// NOTE: Versions 4-6 with rubber tires and antennas cast
// 4. Green cab, green container, "Mayflower" tempa (PC)
	['var' => '04a', 'cab' => 'MB309', 'mfg' => 'Macau', 'liv' => 'Mayflower',
	    'cdt' => 'green',
	    'tdt' => "green container, MAYFLOWER tempa",
        ],
// 5. Black cab, black container, "Jiffy Lube-Drive In Drive Out Drive On" tempa (PC)
	['var' => '05a', 'cab' => 'MB309', 'mfg' => 'Macau', 'liv' => 'Jiffy Lube',
	    'cdt' => 'black',
	    'tdt' => "black container, JIFFY LUBE-DRIVE IN DRIVE OUT DRIVE ON tempa",
        ],
// 6. Gray cab, white container, "Snap-On" tempa (PC)
	['var' => '06a', 'cab' => 'MB309', 'mfg' => 'Macau', 'liv' => 'Snap-On',
	    'cdt' => 'gray',
	    'tdt' => "white container, SNAP-ON tempa",
        ],
    ]);
}
?>

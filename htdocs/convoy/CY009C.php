<?php // DONE
$subtitle = 'CY009C';
// CY-9-C MERCEDES BENZ ACTROSS CONTAINER TRUCK, issued 2001
$desc = "Actros Container Truck";
$year = '2001';
include "cypage.php";

function body() {
    global $subtitle;

// NOTE: Below models with black cab base, smoke windows, chrome disc with rubber tires, & China & "Mattel" casting unless otherwise noted.
    show_table([
// 1. Red cab, red container with black chassis, "Coca Cola" with Chinese lettering labels (PC)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB425', 'tlr' => 'Box', 'mfg' => 'China',
	    'liv' => 'Coca-Cola', 'cod' => '1', 'rar' => '2',
            'cdt' => 'red',
            'tdt' => 'red container with black chassis, COCA COLA with Chinese lettering labels'
	],
// 2. Red cab, red container with black chassis, "Coca Cola Herbstfreuden warten auf Dich!" labels (PC)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB425', 'tlr' => 'Box', 'mfg' => 'China',
	    'liv' => 'Coca-Cola', 'cod' => '1', 'rar' => '2',
            'cdt' => 'red',
            'tdt' => 'red container with black chassis, COCA COLA HERBSTFREUDEN WARTEN AUF DICH! labels',
	],
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB425', 'tlr' => 'Box', 'mfg' => 'China',
	    'liv' => 'Michelin', 'cod' => '1', 'rar' => '2',
            'cdt' => 'blue cab, white chassis with yellow stripe, gray base, blue cab/chassis divider, white interior, clear windows, MICHELIN tampo',
            'tdt' => ' silver base, blue box, roof and doors, labels, nail head hitch pin',
	],
    ]);
}
?>

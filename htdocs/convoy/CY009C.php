<?php // DONE
$subtitle = 'CY009C';
// CY-9-C MERCEDES BENZ ACTROSS CONTAINER TRUCK, issued 2001
$desc = "Actros Container Truck";
$year = '2001';

$defaults = ['mod' => $subtitle, 'cab' => 'MB425', 'tlr' => 'CYT04', 'mfg' => 'China', 'cod' => '1'];

// NOTE: Below models with black cab base, smoke windows, chrome disc with rubber tires, & China & "Mattel" casting unless otherwise noted.
$models = [
// 1. Red cab, red container with black chassis, "Coca Cola" with Chinese lettering labels (PC)
    ['var' => '01a', 'liv' => 'Coca-Cola', 'rar' => '2',
	'cdt' => 'red', 'cva' => '',
	'tdt' => 'red container with black chassis, COCA COLA with Chinese lettering labels'
    ],
// 2. Red cab, red container with black chassis, "Coca Cola Herbstfreuden warten auf Dich!" labels (PC)
    ['var' => '02a', 'liv' => 'Coca-Cola', 'rar' => '2',
	'cdt' => 'red', 'cva' => '',
	'tdt' => 'red container with black chassis, COCA COLA HERBSTFREUDEN WARTEN AUF DICH! labels',
    ],
    ['var' => '03a', 'liv' => 'Michelin', 'rar' => '2',
	'cdt' => 'blue cab, white chassis with yellow stripe, gray base, blue cab/chassis divider, white interior, colorless windows, MICHELIN tampo', 'cva' => '',
	'tdt' => ' silver base, blue box, roof and doors, labels, nail head hitch pin',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>

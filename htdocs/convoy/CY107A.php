<?php // DONE
$subtitle = 'CY107A';
// CY-107-A MACK SUPERSTAR TRANSPORTER, issued 1990
$desc = "Mack Superstar Transporter";
$year = '1990';

$defaults = ['mod' => $subtitle, 'cab' => 'MB202', 'tlr' => 'Superstar Transporter', 'cod' => '2'];

include "cypage.php";

function body() {
// NOTE: All models with 8-spoke wheels 8 no antennas cast unless otherwise noted.
    show_table([
// 1. Orange cab, black container, "Baltimore Orioles" labels (WR)
	['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Baltimore Orioles',
	    'cdt' => 'orange',
            'tdt' => "black container, BALTIMORE ORIOLES labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 2. Red cab, white container, "Melling Racing 9" labels (WR)
	['var' => '02a', 'mfg' => 'Macau', 'liv' => 'Melling Racing',
	    'cdt' => 'red',
            'tdt' => "white container, MELLING RACING 9 labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 3. Red and white cab, maroon container, "Nascar-America's Ultimate Motorsport" labels (WR)
	['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Nascar',
	    'cdt' => 'red and white',
            'tdt' => "maroon container, NASCAR-AMERICA'S ULTIMATE MOTORSPORT labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 4. Blue cab, white container, "Bill Elliot 9" labels (WR)
	['var' => '04a', 'mfg' => 'Macau', 'liv' => 'Bill Elliot',
	    'cdt' => 'blue',
            'tdt' => "white container, BILL ELLIOT 9 labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 5. White and blue cab, white container, "ADAP/Auto Palace" labels (WR)
	['var' => '05a', 'mfg' => 'Macau', 'liv' => 'ADAP',
	    'cdt' => 'white and blue',
            'tdt' => "white container, ADAP/AUTO PALACE labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 6. White cab, white container, "Ferree Chevrolet 49" labels (WR)
	['var' => '06a', 'mfg' => 'Macau', 'liv' => 'Ferree Chevrolet',
	    'cdt' => 'white',
            'tdt' => "white container, FERREE CHEVROLET 49 labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 7. Black cab, black container, "Interstate Batteries" labels (WR)
	['var' => '07a', 'mfg' => 'Macau', 'liv' => 'Interstate',
	    'cdt' => 'black',
            'tdt' => "black container, INTERSTATE BATTERIES labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 8. Black cab, black container, "Active Racing 32" labels (WR)
	['var' => '08a', 'mfg' => 'Macau', 'liv' => 'Active Racing',
	    'cdt' => 'black',
            'tdt' => "black container, ACTIVE RACING 32 labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 9. White cab, white container, "MW Windows Racing" labels (WR)
	['var' => '09a', 'mfg' => 'Macau', 'liv' => 'MW Windows Racing',
	    'cdt' => 'white',
            'tdt' => "white container, MW WINDOWS RACING labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 10. Red cab, red container, "Fiddle Faddle" labels (WR)
	['var' => '10a', 'mfg' => 'Macau', 'liv' => 'Fiddle Faddle',
	    'cdt' => 'red',
            'tdt' => "red container, FIDDLE FADDLE labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 11. Black cab, black container, "Armor All" tampo, rubber tires, antennas cast (PC)
	['var' => '11a', 'cab' => 'MB311', 'mfg' => 'Macau', 'liv' => 'Armor All', 'cod' => '1',
	    'cdt' => 'black',
            'tdt' => "black container, ARMOR ALL tampo",
	],
    ]);
}
?>

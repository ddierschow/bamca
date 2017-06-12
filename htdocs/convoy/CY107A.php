<?php // DONE
$subtitle = 'CY107A';
// CY-107-A MACK SUPERSTAR TRANSPORTER, issued 1990
$desc = "Mack Superstar Transporter";
$year = '1990';
include "cypage.php";

function body() {
    global $subtitle;

// NOTE: All models with 8-spoke wheels 8 no antennas cast unless otherwise noted.
    show_table([
// 1. Orange cab, black container, "Baltimore Orioles" labels (WR)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB202', 'tlr' => 'Superstar Transporter', 'mfg' => 'Macau',
	    'liv' => 'Baltimore Orioles', 'cod' => '2', 'rar' => '',
	    'cdt' => 'orange',
            'tdt' => "black container, BALTIMORE ORIOLES labels",
	],
// 2. Red cab, white container, "Melling Racing 9" labels (WR)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB202', 'tlr' => 'Superstar Transporter', 'mfg' => 'Macau',
	    'liv' => 'Melling Racing', 'cod' => '2', 'rar' => '',
	    'cdt' => 'red',
            'tdt' => "white container, MELLING RACING 9 labels",
	],
// 3. Red and white cab, maroon container, "Nascar-America's Ultimate Motorsport" labels (WR)
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB202', 'tlr' => 'Superstar Transporter', 'mfg' => 'Macau',
	    'liv' => 'Nascar', 'cod' => '2', 'rar' => '',
	    'cdt' => 'red and white',
            'tdt' => "maroon container, NASCAR-AMERICA'S ULTIMATE MOTORSPORT labels",
	],
// 4. Blue cab, white container, "Bill Elliot 9" labels (WR)
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB202', 'tlr' => 'Superstar Transporter', 'mfg' => 'Macau',
	    'liv' => 'Bill Elliot', 'cod' => '2', 'rar' => '',
	    'cdt' => 'blue',
            'tdt' => "white container, BILL ELLIOT 9 labels",
	],
// 5. White and blue cab, white container, "ADAP/Auto Palace" labels (WR)
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB202', 'tlr' => 'Superstar Transporter', 'mfg' => 'Macau',
	    'liv' => 'ADAP', 'cod' => '2', 'rar' => '',
	    'cdt' => 'white and blue',
            'tdt' => "white container, ADAP/AUTO PALACE labels",
	],
// 6. White cab, white container, "Ferree Chevrolet 49" labels (WR)
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB202', 'tlr' => 'Superstar Transporter', 'mfg' => 'Macau',
	    'liv' => 'Ferree Chevrolet', 'cod' => '2', 'rar' => '',
	    'cdt' => 'white',
            'tdt' => "white container, FERREE CHEVROLET 49 labels",
	],
// 7. Black cab, black container, "Interstate Batteries" labels (WR)
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB202', 'tlr' => 'Superstar Transporter', 'mfg' => 'Macau',
	    'liv' => 'Interstate', 'cod' => '2', 'rar' => '',
	    'cdt' => 'black',
            'tdt' => "black container, INTERSTATE BATTERIES labels",
	],
// 8. Black cab, black container, "Active Racing 32" labels (WR)
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB202', 'tlr' => 'Superstar Transporter', 'mfg' => 'Macau',
	    'liv' => 'Active Racing', 'cod' => '2', 'rar' => '',
	    'cdt' => 'black',
            'tdt' => "black container, ACTIVE RACING 32 labels",
	],
// 9. White cab, white container, "MW Windows Racing" labels (WR)
	['mod' => $subtitle, 'var' => '09a',
	    'cab' => 'MB202', 'tlr' => 'Superstar Transporter', 'mfg' => 'Macau',
	    'liv' => 'MW Windows Racing', 'cod' => '2', 'rar' => '',
	    'cdt' => 'white',
            'tdt' => "white container, MW WINDOWS RACING labels",
	],
// 10. Red cab, red container, "Fiddle Faddle" labels (WR)
	['mod' => $subtitle, 'var' => '10a',
	    'cab' => 'MB202', 'tlr' => 'Superstar Transporter', 'mfg' => 'Macau',
	    'liv' => 'Fiddle Faddle', 'cod' => '2', 'rar' => '',
	    'cdt' => 'red',
            'tdt' => "red container, FIDDLE FADDLE labels",
	],
// 11. Black cab, black container, "Armor All" tampo, rubber tires, antennas cast (PC)
	['mod' => $subtitle, 'var' => '11a',
	    'cab' => 'MB311', 'tlr' => 'Superstar Transporter', 'mfg' => 'Macau',
	    'liv' => 'Armor All', 'cod' => '1', 'rar' => '',
	    'cdt' => 'black',
            'tdt' => "black container, ARMOR ALL tampo",
	],
    ]);
}
?>

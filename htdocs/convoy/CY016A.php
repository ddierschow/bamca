<?php // DONE
$subtitle = 'CY016A';
// CY-16-A SCANIA BOX TRUCK, issued 1985
$desc = "Scania T142 Box Truck";
$year = '1985';

$defaults = ['mod' => $subtitle,
	    'cab' => 'MB147', 'tlr' => 'CYT04', 'mfg' => 'Macau',
	    'liv' => '7 Up', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, green chassis',
            'tdt' => 'white container with black base, 7 UP (towards rear) labels',
	];

// NOTE: All cabs with chrome base unless otherwise noted
$models = [
// 1. White cab, green chassis, white container with black base, "7 Up" (towards rear) labels, Macau (US)
    ['var' => '01a', 'mfg' => 'Macau', 'liv' => '7 Up', 'rar' => '2',
	'cdt' => 'white, green chassis', 'cva' => '04',
	'tdt' => 'white container with black base, 7 UP (towards rear) labels',
    ],
// 2. White cab, green chassis, white container with black base, "7 Up" (towards front) labels, Macau
    ['var' => '02a', 'mfg' => 'Macau', 'liv' => '7 Up', 'rar' => '3',
	'cdt' => 'white, green chassis', 'cva' => '04',
	'tdt' => 'white container with black base, 7 UP (towards front) labels',
    ],
// 3. White cab, green chassis, white container with black base, "7 Up" (upside down) labels, Macau (US)
    ['var' => '03a', 'mfg' => 'Macau', 'liv' => '7 Up', 'rar' => '4',
	'cdt' => 'white, green chassis', 'cva' => '04',
	'tdt' => 'white container with black base, 7 UP (upside down) labels',
	'nts' => 'This should be considered more as a factory error than a variation',
    ],
// 4. White cab, dark blue chassis, dark blue container with white base, "Duckham's Oils" tampo, Macau
    ['var' => '04a', 'mfg' => 'Macau', 'liv' => "Duckham's", 'rar' => '2',
	'cdt' => 'white, dark blue chassis', 'cva' => '03',
	'tdt' => "dark blue container with white base, DUCKHAM'S OILS tampo",
    ],
// 5. Purple cab and chassis, white container with purple base, "Edwin Shirley" tampo, Macau (UK)
    ['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Edwin Shirley', 'rar' => '2',
	'cdt' => 'purple, purple chassis', 'cva' => '09',
	'tdt' => 'white container with purple base, EDWIN SHIRLEY tampo',
    ],
// 6. White cab, black chassis, white container with black base, "Wimpey" tampo, Macau (UK)
    ['var' => '06a', 'mfg' => 'Macau', 'liv' => 'Wimpey', 'rar' => '2',
	'cdt' => 'white, black chassis,', 'cva' => '15',
	'tdt' => 'white container with black base, WIMPEY tampo',
    ],
// 7. Red cab, white chassis, red container with white base, "Kentucky Fried Chicken" tampo, Macau (UK)
    ['var' => '07a', 'mfg' => 'Macau', 'liv' => 'KFC', 'rar' => '2',
	'cdt' => 'red, white chassis', 'cva' => '13',
	'tdt' => 'red container with white base, KENTUCKY FRIED CHICKEN tampo',
    ],
// 8. White cab, blue chassis, white container with blue base, "Signal Toothpaste" tampo, Macau (UK)
    ['var' => '08a', 'mfg' => 'Macau', 'liv' => 'Signal Toothpaste', 'rar' => '2',
	'cdt' => 'white, blue chassis', 'cva' => '20',
	'tdt' => 'white container with blue base, SIGNAL TOOTHPASTE tampo',
    ],
// 9. White cab, red chassis, red container with red base, "Heinz Tomato Ketchup Squeezable" labels, Macau (UK)
    ['var' => '09a', 'mfg' => 'Macau', 'liv' => 'Heinz', 'rar' => '2',
	'cdt' => 'white, red chassis', 'cva' => '21',
	'tdt' => 'red container with red base, HEINZ TOMATO KETCHUP SQUEEZABLE labels',
    ],
// 10. Yellow cab, white chassis, white container with red base, "Weetabix" labels, Macau (UK)
    ['var' => '10a', 'mfg' => 'Macau', 'liv' => 'Weetabix', 'rar' => '2',
	'cdt' => 'yellow, white chassis', 'cva' => '16',
	'tdt' => 'white container with red base, WEETABIX labels',
    ],
// 11. Blue cab, white chassis, blue container with blue base, "Matey Bubble Bath" tampo, Macau (UK)
    ['var' => '11a', 'mfg' => 'Macau', 'liv' => 'Matey', 'rar' => '2',
	'cdt' => 'blue, white chassis', 'cva' => '17',
	'tdt' => 'blue container with blue base, MATEY BUBBLE BATH tampo',
    ],
// 12. White cab, black chassis, white container with black base, "Golden Wonder Potato Crisps" tampo, Macau (UK)
    ['var' => '12a', 'mfg' => 'Macau', 'liv' => 'Golden Wonder', 'rar' => '2',
	'cdt' => 'white, black chassis', 'cva' => '26',
	'tdt' => 'white container with black base, GOLDEN WONDER POTATO CRISPS tampo',
    ],
// 13. White cab, red chassis, white container with red base, "Merchant Tire Auto and Auto Centers" tampo, Macau (US)
    ['var' => '13a', 'mfg' => 'Macau', 'liv' => 'Merchants Tire', 'rar' => '2',
	'cdt' => 'white, red chassis', 'cva' => '28',
	'tdt' => 'white container with red base, MERCHANT TIRE AUTO AND AUTO CENTERS tampo',
    ],
// 14. White cab, red chassis, white container with red base, "Merry Christmas 1988 MICA Members" with calendar roof label, Macau (C2)
    ['var' => '14a', 'mfg' => 'Macau', 'liv' => 'MICA', 'cod' => '2', 'rar' => '3',
	'cdt' => 'white, red chassis', 'cva' => '28',
	'tdt' => 'white container with red base, MERRY CHRISTMAS 1988 MICA MEMBERS with calendar roof label',
    ],
// 15. Yellow cab, white chassis, black base, yellow container and yellow base, "Weetabix" tampo, Macau (UK)
    ['var' => '15a', 'mfg' => 'Macau', 'liv' => 'Weetabix', 'rar' => '2',
	'crd' => 'Picture from Simon Rogers - AU',
	'cdt' => 'yellow, white chassis, black base', 'cva' => '30',
	'tdt' => 'yellow container and yellow base, WEETABIX tampo',
	'nts' => 'Reports of some models with red or blue doors on trailer and no printing on cab wind deflector.',
    ],
// 16. Purple cab, red chassis, black base, purple container with red base, "Ribena" tampo, Macau (UK)
    ['var' => '16a', 'mfg' => 'Macau', 'liv' => 'Ribena', 'rar' => '2',
	'cdt' => 'purple, red chassis, black base', 'cva' => '31',
	'tdt' => 'purple container with red base, RIBENA tampo',
    ],
// 17. Red cab, white chassis, black base, red container with white base, "Kentucky Fried Chicken" tampo, Macau (UK)
    ['var' => '17a', 'mfg' => 'Macau', 'liv' => 'KFC', 'rar' => '2',
	'cdt' => 'red, white chassis, black base', 'cva' => '32',
	'tdt' => 'red container with white base, KENTUCKY FRIED CHICKEN tampo',
    ],
// 18. White cab, green chassis, white container with black base, "Merry Christmas 1989 MICA Members" with calendar roof label (C2)
    ['var' => '18a', 'mfg' => 'Thailand', 'liv' => 'MICA', 'cod' => '2', 'rar' => '3',
	'crd' => 'Picture from Simon Rogers - AU',
	'cdt' => 'white, green chassis', 'cva' => '04',
	'tdt' => 'white container with black base, MERRY CHRISTMAS 1989 MIcA MEMBERS with calendar roof label',
    ],
// 19. White cab, blue chassis, white container with black base, "Goodyear Vector" tampo, Thailand
    ['var' => '19a', 'mfg' => 'Thailand', 'liv' => 'Goodyear', 'rar' => '2',
	'cdt' => 'white, blue chassis', 'cva' => '36',
	'tdt' => 'white container with black base, GOODYEAR VECTOR tampo',
    ],
// 20. White cab, dark gray chassis and chrome base, white container with black trailer, Thailand, "Saudia" labels (SU)
    ['var' => '20a', 'mfg' => 'Thailand', 'liv' => 'Saudia', 'rar' => '3',
	'cdt' => 'white, dark gray chassis and chrome base', 'cva' => '41',
	'tdt' => 'white container with black trailer, SAUDIA labels',
    ],
// 21. White cab, green chassis and chrome base, white container with green trailer, Macau "Baas Aufzuge GmBh-Frohliche Weihnachten" labels (C2)
    ['var' => '21a', 'mfg' => 'Macau', 'liv' => 'Baas Aufzuge GmBh', 'cod' => '2', 'rar' => '4',
	'cdt' => 'white, green chassis, chrome base', 'cva' => '04',
	'tdt' => 'white container with green trailer, BAAS AUFZUGE GMBH-FROHLICHE WEIHNACHTEN labels',
    ],
// 22. Red cab, black chassis and chrome base, yellow container with black trailer, China and "Mattel", "Nestle Smarties" labels (ROW)
    ['var' => '22a', 'mfg' => 'China, MATTEL', 'liv' => 'Nestle', 'rar' => '4',
	'cdt' => 'red, black chassis, chrome base', 'cva' => '43',
	'tdt' => 'yellow container with black trailer, NESTLE SMARTIES labels',
    ],
// 23. Blue cab, yellow chassis and chrome base, yellow container and rear doors with blue roof with yellow trailer, China and "Mattel", "Rice Krispies" labels (ROW)
    ['var' => '23a', 'mfg' => 'China, MATTEL', 'liv' => 'Rice Krispies', 'rar' => '4',
	'cdt' => 'blue, yellow chassis, chrome base', 'cva' => '',
	'tdt' => 'yellow container and rear doors with blue roof with yellow trailer, RICE KRISPIES labels',
    ],
// 24. Red cab, black chassis and chrome base, red container with black trailer, China and "Mattel", "a la pause Coca Cola desaltere le miex" labels, antennas cast, chrome disc with rubber tires (PC)
    ['var' => '24a', 'cab' => 'MB341', 'mfg' => 'China, MATTEL', 'liv' => 'Coca-Cola', 'rar' => '4',
	'cdt' => 'red, black chassis, chrome base', 'cva' => '',
	'tdt' => 'red container with black trailer, A LA PAUSE COCA COLA DESALTERE LE MIEX labels',
    ],
// 25. Red cab, black chassis and chrome base, red container with black trailer, China and "Mattel", "All over the world Coca Cola brings refreshment" labels, antennas cast, chrome disc with rubber tires (PC)
    ['var' => '25a', 'cab' => 'MB341', 'mfg' => 'China, MATTEL', 'liv' => 'Coca-Cola', 'rar' => '4',
	'cdt' => 'red, black chassis, chrome base', 'cva' => '',
	'tdt' => 'red container with black trailer, ALL OVER THE WORLD COCA COLA BRINGS REFRESHMENT labels',
    ],

    ['var' => '26a', 'mfg' => 'China, MATTEL', 'liv' => 'Matchbox', 'rar' => '2',
	'cdt' => 'dark yellow, orange chassis, orange plastic base, with silver grill guard and exhaust, clear windows, MATCHBOX 50TH ANNIVERSARY logo on sides', 'cva' => '',
	'tdt' => 'black base, yellow box, roof and doors, labels applied to sides',
    ],

    ['var' => '27a', 'cab' => 'MB341', 'mfg' => 'China, MATTEL', 'liv' => 'Coca-Cola', 'rar' => '2',
	'cdt' => 'brown, dark green chassis, silver plastic base, grill guard, exhaust and antennas, smoke windows, COCA COLA CALENDAR GIRLS on the side and painted details', 'cva' => '',
	'tdt' => 'dark green base, brown box and doors, dark green roof and painted door hardware, SEPTEMBER AND OCTOBER, 1947 calendar labels on sides',
	'nts' => 'Part of the "Coke Calendar Girls" series - 2002',
    ],

    ['var' => '28a', 'cab' => 'MB341', 'mfg' => 'China, MATTEL', 'liv' => 'Coca-Cola', 'rar' => '2',
	'cdt' => 'maroon, black chassis, silver plastic base, grill guard, exhaust and antennas, smoke windows, COCA COLA CALENDAR GIRLS on the side and painted details', 'cva' => '',
	'tdt' => 'black base, rust colored box and doors, black roof and painted door hardware, NOVEMBER AND DECEMBER, 1947 calendar labels on side',
	'nts' => 'Part of the "Coke Calendar Girls" series - 2002',
    ],

];

include "cypage.php";

function body() {
?>
<a href="CY004A.php">Also see CY004B </a><br>
<a href="#Code3">Code 3 Models</a><br>

<?php
    global $models;
    show_table($models);
?>

<div class="center" id="Code3">
CODE 3's<br>
<img src="/pic/set/convoy/m_cy016a-c3a.jpg"><br>
Picture from Jim Jenkins - USA<p>
<img src="/pic/set/convoy/m_cy016a-c3b.jpg"><br>
Picture from Simon Rogers - AU<p>
<img src="/pic/set/convoy/m_cy016a-c3c.jpg"><br>
Picture from Simon Rogers - AU<p>
<img src="/pic/set/convoy/m_cy016a-c3d.jpg"><br>
Picture from Lee James - UK<p>
<img src="/pic/set/convoy/m_cy016a-c3e.jpg"><br>
Picture from Jim Jenkins - USA<p>
</div>

<?php
}
?>

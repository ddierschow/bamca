<?php // DONE
$subtitle = 'CY016A';
// CY-16-A SCANIA BOX TRUCK, issued 1985
$desc = "Scania T142 Box Truck";
$year = '1985';
include "cypage.php";

function body() {
    global $subtitle;

?>
<a href="CY004A.php">Also see CY004B </a><br>
<a href="#Code3">Code 3 Models</a><br>
<?php

// NOTE: All cabs with chrome base unless otherwise noted
    show_table([
// 1. White cab, green chassis, white container with black base, "7 Up" (towards rear) labels, Macau (US)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => '7 Up', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, green chassis',
            'tdt' => 'white container with black base, 7 UP (towards rear) labels',
	],
// 2. White cab, green chassis, white container with black base, "7 Up" (towards front) labels, Macau
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => '7 Up', 'cod' => '1', 'rar' => '3',
            'cdt' => 'white, green chassis',
            'tdt' => 'white container with black base, 7 UP (towards front) labels',
	],
// 3. White cab, green chassis, white container with black base, "7 Up" (upside down) labels, Macau (US)
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => '7 Up', 'cod' => '1', 'rar' => '4',
            'cdt' => 'white, green chassis',
            'tdt' => 'white container with black base, 7 UP (upside down) labels',
	    'nts' => 'This should be considered more as a factory error than a variation',
	],
// 4. White cab, dark blue chassis, dark blue container with white base, "Duckham's Oils" tampo, Macau
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => "Duckham's", 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, dark blue chassis',
            'tdt' => "dark blue container with white base, DUCKHAM'S OILS tampo",
	],
// 5. Purple cab and chassis, white container with purple base, "Edwin Shirley" tampo, Macau (UK)
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Edwin Shirley', 'cod' => '1', 'rar' => '2',
            'cdt' => 'purple, purple chassis',
            'tdt' => 'white container with purple base, EDWIN SHIRLEY tampo',
	],
// 6. White cab, black chassis, white container with black base, "Wimpey" tampo, Macau (UK)
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Wimpey', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, black chassis,',
            'tdt' => 'white container with black base, WIMPEY tampo',
	],
// 7. Red cab, white chassis, red container with white base, "Kentucky Fried Chicken" tampo, Macau (UK)
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'KFC', 'cod' => '1', 'rar' => '2',
            'cdt' => 'red, white chassis',
            'tdt' => 'red container with white base, KENTUCKY FRIED CHICKEN tampo',
	],
// 8. White cab, blue chassis, white container with blue base, "Signal Toothpaste" tampo, Macau (UK)
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Signal Toothpaste', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, blue chassis',
            'tdt' => 'white container with blue base, SIGNAL TOOTHPASTE tampo',
	],
// 9. White cab, red chassis, red container with red base, "Heinz Tomato Ketchup Squeezable" labels, Macau (UK)
	['mod' => $subtitle, 'var' => '09a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Heinz', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, red chassis',
            'tdt' => 'red container with red base, HEINZ TOMATO KETCHUP SQUEEZABLE labels',
	],
// 10. Yellow cab, white chassis, white container with red base, "Weetabix" labels, Macau (UK)
	['mod' => $subtitle, 'var' => '10a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Weetabix', 'cod' => '1', 'rar' => '2',
            'cdt' => 'yellow, white chassis',
            'tdt' => 'white container with red base, WEETABIX labels',
	],
// 11. Blue cab, white chassis, blue container with blue base, "Matey Bubble Bath" tampo, Macau (UK)
	['mod' => $subtitle, 'var' => '11a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Matey', 'cod' => '1', 'rar' => '2',
            'cdt' => 'blue, white chassis',
            'tdt' => 'blue container with blue base, MATEY BUBBLE BATH tampo',
	],
// 12. White cab, black chassis, white container with black base, "Golden Wonder Potato Crisps" tampo, Macau (UK)
	['mod' => $subtitle, 'var' => '12a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Golden Wonder', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, black chassis',
            'tdt' => 'white container with black base, GOLDEN WONDER POTATO CRISPS tampo',
	],
// 13. White cab, red chassis, white container with red base, "Merchant Tire Auto and Auto Centers" tampo, Macau (US)
	['mod' => $subtitle, 'var' => '13a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Merchants Tire', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, red chassis',
            'tdt' => 'white container with red base, MERCHANT TIRE AUTO AND AUTO CENTERS tampo',
	],
// 14. White cab, red chassis, white container with red base, "Merry Christmas 1988 MICA Members" with calendar roof label, Macau (C2)
	['mod' => $subtitle, 'var' => '14a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'MICA', 'cod' => '2', 'rar' => '3',
            'cdt' => 'white, red chassis',
            'tdt' => 'white container with red base, MERRY CHRISTMAS 1988 MICA MEMBERS with calendar roof label',
	],
// 15. Yellow cab, white chassis, black base, yellow container and yellow base, "Weetabix" tampo, Macau (UK)
	['mod' => $subtitle, 'var' => '15a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Weetabix', 'cod' => '1', 'rar' => '2',
	    'crd' => 'Picture from Simon Rogers - AU',
            'cdt' => 'yellow, white chassis, black base',
            'tdt' => 'yellow container and yellow base, WEETABIX tampo',
	    'nts' => 'Reports of some models with red or blue doors on trailer and no printing on cab wind deflector.',
	],
// 16. Purple cab, red chassis, black base, purple container with red base, "Ribena" tampo, Macau (UK)
	['mod' => $subtitle, 'var' => '16a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Ribena', 'cod' => '1', 'rar' => '2',
            'cdt' => 'purple, red chassis, black base',
            'tdt' => 'purple container with red base, RIBENA tampo',
	],
// 17. Red cab, white chassis, black base, red container with white base, "Kentucky Fried Chicken" tampo, Macau (UK)
	['mod' => $subtitle, 'var' => '17a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'KFC', 'cod' => '1', 'rar' => '2',
            'cdt' => 'red, white chassis, black base',
            'tdt' => 'red container with white base, KENTUCKY FRIED CHICKEN tampo',
	],
// 18. White cab, green chassis, white container with black base, "Merry Christmas 1989 MICA Members" with calendar roof label (C2)
	['mod' => $subtitle, 'var' => '18a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Thailand',
	    'liv' => 'MICA', 'cod' => '2', 'rar' => '3',
	    'crd' => 'Picture from Simon Rogers - AU',
            'cdt' => 'white, green chassis',
            'tdt' => 'white container with black base, MERRY CHRISTMAS 1989 MIcA MEMBERS with calendar roof label',
	],
// 19. White cab, blue chassis, white container with black base, "Goodyear Vector" tampo, Thailand
	['mod' => $subtitle, 'var' => '19a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Thailand',
	    'liv' => 'Goodyear', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, blue chassis',
            'tdt' => 'white container with black base, GOODYEAR VECTOR tampo',
	],
// 20. White cab, dark gray chassis and chrome base, white container with black trailer, Thailand, "Saudia" labels (SU)
	['mod' => $subtitle, 'var' => '20a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Thailand',
	    'liv' => 'Saudia', 'cod' => '1', 'rar' => '3',
            'cdt' => 'white, dark gray chassis and chrome base',
            'tdt' => 'white container with black trailer, SAUDIA labels',
	],
// 21. White cab, green chassis and chrome base, white container with green trailer, Macau "Baas Aufzuge GmBh-Frohliche Weihnachten" labels (C2)
	['mod' => $subtitle, 'var' => '21a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Baas Aufzuge GmBh', 'cod' => '2', 'rar' => '4',
            'cdt' => 'white, green chassis, chrome base',
            'tdt' => 'white container with green trailer, BAAS AUFZUGE GMBH-FROHLICHE WEIHNACHTEN labels',
	],
// 22. Red cab, black chassis and chrome base, yellow container with black trailer, China and "Mattel", "Nestle Smarties" labels (ROW)
	['mod' => $subtitle, 'var' => '22a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'China, MATTEL',
	    'liv' => 'Nestle', 'cod' => '1', 'rar' => '4',
            'cdt' => 'red, black chassis, chrome base',
            'tdt' => 'yellow container with black trailer, NESTLE SMARTIES labels',
	],
// 23. Blue cab, yellow chassis and chrome base, yellow container and rear doors with blue roof with yellow trailer, China and "Mattel", "Rice Krispies" labels (ROW)
	['mod' => $subtitle, 'var' => '23a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'China, MATTEL',
	    'liv' => 'Rice Krispies', 'cod' => '1', 'rar' => '4',
            'cdt' => 'blue, yellow chassis, chrome base',
            'tdt' => 'yellow container and rear doors with blue roof with yellow trailer, RICE KRISPIES labels',
	],
// 24. Red cab, black chassis and chrome base, red container with black trailer, China and "Mattel", "a la pause Coca Cola desaltere le miex" labels, antennas cast, chrome disc with rubber tires (PC)
	['mod' => $subtitle, 'var' => '24a',
	    'cab' => 'MB341', 'tlr' => 'Box', 'mfg' => 'China, MATTEL',
	    'liv' => 'Coca-Cola', 'cod' => '1', 'rar' => '4',
            'cdt' => 'red, black chassis, chrome base',
            'tdt' => 'red container with black trailer, A LA PAUSE COCA COLA DESALTERE LE MIEX labels',
	],
// 25. Red cab, black chassis and chrome base, red container with black trailer, China and "Mattel", "All over the world Coca Cola brings refreshment" labels, antennas cast, chrome disc with rubber tires (PC)
	['mod' => $subtitle, 'var' => '25a',
	    'cab' => 'MB341', 'tlr' => 'Box', 'mfg' => 'China, MATTEL',
	    'liv' => 'Coca-Cola', 'cod' => '1', 'rar' => '4',
            'cdt' => 'red, black chassis, chrome base',
            'tdt' => 'red container with black trailer, ALL OVER THE WORLD COCA COLA BRINGS REFRESHMENT labels',
	],

	['mod' => $subtitle, 'var' => '26a',
	    'cab' => 'MB147', 'tlr' => 'Box', 'mfg' => 'China, MATTEL',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '2',
            'cdt' => 'dark yellow, orange chassis, orange plastic base, with silver grill guard and exhaust, clear windows, MATCHBOX 50TH ANNIVERSARY logo on sides',
            'tdt' => 'black base, yellow box, roof and doors, labels applied to sides',
	],

	['mod' => $subtitle, 'var' => '27a',
	    'cab' => 'MB341', 'tlr' => 'Box', 'mfg' => 'China, MATTEL',
	    'liv' => 'Coca-Cola', 'cod' => '1', 'rar' => '2',
            'cdt' => 'brown, dark green chassis, silver plastic base, grill guard, exhaust and antennas, smoke windows, COCA COLA CALENDAR GIRLS on the side and painted details',
            'tdt' => 'dark green base, brown box and doors, dark green roof and painted door hardware, SEPTEMBER AND OCTOBER, 1947 calendar labels on sides',
	    'nts' => 'Part of the "Coke Calendar Girls" series - 2002',
	],

	['mod' => $subtitle, 'var' => '28a',
	    'cab' => 'MB341', 'tlr' => 'Box', 'mfg' => 'China, MATTEL',
	    'liv' => 'Coca-Cola', 'cod' => '1', 'rar' => '2',
            'cdt' => 'maroon, black chassis, silver plastic base, grill guard, exhaust and antennas, smoke windows, COCA COLA CALENDAR GIRLS on the side and painted details',
            'tdt' => 'black base, rust colored box and doors, black roof and painted door hardware, NOVEMBER AND DECEMBER, 1947 calendar labels on side',
	    'nts' => 'Part of the "Coke Calendar Girls" series - 2002',
	],

    ]);

?>

<div class="center">
<a name="Code3"></a>
CODE 3's<br>
<img src="/pic/convoy/m_cy016a_c3a.jpg"><br>
Picture from Jim Jenkins - USA<p>
<img src="/pic/convoy/m_cy016a_c3b.jpg"><br>
Picture from Simon Rogers - AU<p>
<img src="/pic/convoy/m_cy016a_c3c.jpg"><br>
Picture from Simon Rogers - AU<p>
<img src="/pic/convoy/m_cy016a_c3d.jpg"><br>
Picture from Lee James - UK<p>
<img src="/pic/convoy/m_cy016a_c3e.jpg"><br>
Picture from Jim Jenkins - USA<p>
</div>

<?php
}
?>

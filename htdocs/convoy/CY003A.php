<?php // DONE
$subtitle = 'CY003A';
// CY-3-A DOUBLE CONTAINER TRUCK, issued 1982
$desc = "Double Container Truck";
$year = '1982';

$defaults = ['mod' => $subtitle, 'cab' => 'MB106', 'tlr' => 'Double Container', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. MB103 cab in red, chrome exhausts, clear windows, beige containers, black trailer, "Uniroyal" labels, England
	['var' => '01a', 'cab' => 'MB103', 'mfg' => 'England', 'liv' => 'Uniroyal',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'black, beige containers, UNIROYAL labels',
	    'add' => [
['<b>Container Colors from left to right: <br>Brown, Tan, Beige &amp;<br> Cream</b>',
'<img src="/pic/set/convoy/m_cy003a-box2.jpg">'],
['This series has both Peterbilt and Mack cabs in it and the Uniroyal containers could any one of four different colors.',
'<img src="/pic/set/convoy/m_cy003a-box1.jpg"']],
        ],
// 2. MB106 cab in red, chrome exhausts, amber windows, beige containers, black trailer, "Uniroyal" labels, England
	['var' => '02a', 'mfg' => 'England', 'liv' => 'Uniroyal',
            'cdt' => 'red, chrome exhausts, amber windows',
            'tdt' => 'black, beige containers, UNIROYAL labels',
        ],
// 3. MB106 cab in red, chrome exhausts, clear windows, beige containers, black trailer, "Uniroyal" labels, England
	['var' => '03a', 'mfg' => 'England', 'liv' => 'Uniroyal',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'black, beige containers, UNIROYAL labels',
        ],
// 4. MB106 cab in red, chrome exhausts, clear windows, light tan containers, black trailer, "Uniroyal" labels, England
	['var' => '04a', 'mfg' => 'England', 'liv' => 'Uniroyal',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'black, light tan containers, UNIROYAL labels',
        ],
// 5. MB106 cab in red, chrome exhausts, clear windows, beige containers, white trailer, "Uniroyal" labels, England
	['var' => '05a', 'mfg' => 'England', 'liv' => 'Uniroyal',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'white, beige containers, UNIROYAL labels',
        ],
// 6. MB106 cab in red, chrome exhausts, clear windows, cream containers, white trailer, "Uniroyal" labels, England
	['var' => '06a', 'mfg' => 'England', 'liv' => 'Uniroyal',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'white, cream containers, UNIROYAL labels',
        ],
// 7. MB103 cab in red, chrome exhausts, clear windows, beige containers, white trailer, "Uniroyal" labels, England
	['var' => '07a', 'cab' => 'MB103', 'mfg' => 'England', 'liv' => 'Uniroyal',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'white, beige containers, UNIROYAL labels',
        ],
// 8. MB106 cab in red, chrome exhausts, clear windows, brown containers, black trailer, "Uniroyal" labels, England
	['var' => '08a', 'mfg' => 'England', 'liv' => 'Uniroyal',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'black, brown containers, UNIROYAL labels',
        ],
// 9. MB045 cab in white, chrome exhausts, amber windows, beige containers, "Pepsi" labels, Macau
	['var' => '09a', 'cab' => 'MB045', 'mfg' => 'Macau', 'liv' => 'Pepsi',
            'cdt' => 'white, chrome exhausts, amber windows',
            'tdt' => 'beige containers, PEPSI labels',
        ],
// 10. MB106 cab in black, chrome exhausts, clear windows, cream containers, "Pepsi" labels, England
	['var' => '10a', 'mfg' => 'England', 'liv' => 'Pepsi',
            'cdt' => 'black, chrome exhausts, clear windows',
            'tdt' => 'cream containers, PEPSI labels',
        ],
// 11. MB106 cab in black, chrome exhausts, clear windows, cream containers, black trailer, "Federal Express" labels, Macau
	['var' => '11a', 'mfg' => 'Macau', 'liv' => 'Federal Express',
            'cdt' => 'black, chrome exhausts, clear windows',
            'tdt' => 'black, cream containers, FEDERAL EXPRESS labels',
        ],
// 12. MB106 cab in white, chrome exhausts, clear windows, beige containers, black trailer, "Federal Express" labels, England
	['var' => '12a', 'mfg' => 'England', 'liv' => 'Federal Express',
            'cdt' => 'white, chrome exhausts, clear windows',
            'tdt' => 'black, beige containers, FEDERAL EXPRESS labels',
        ],
// 13. MB106 cab in white, chrome exhausts, clear windows, white containers, black trailer, "Federal Express" tampo, Macau
	['var' => '13a', 'mfg' => 'Macau', 'liv' => 'Federal Express',
            'cdt' => 'white, chrome exhausts, clear windows',
            'tdt' => 'black, white containers, FEDERAL EXPRESS tampo',
        ],
// 14. MB103 cab in red, chrome exhausts, clear windows, light tan containers, white trailer, "Mayflower" labels, England
	['var' => '14a', 'cab' => 'MB103', 'mfg' => 'England', 'liv' => 'Mayflower', 'rar' => '5',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'white, light tan containers, MAYFLOWER labels',
        ],
// 15. MB106 cab in white, gray exhausts, clear windows, white containers, black trailer, "Federal Express" tampo, Macau
	['var' => '15a', 'mfg' => 'Macau', 'liv' => 'Federal Express',
            'cdt' => 'white, gray exhausts, clear windows',
            'tdt' => 'black, white containers, FEDERAL EXPRESS tampo',
        ],
// 16. MB106 cab in white, gray exhausts, clear windows, white containers, black trailer, "Federal Express" tampo, Thailand
	['var' => '16a', 'mfg' => 'Thailand', 'liv' => 'Federal Express',
            'cdt' => 'white, gray exhausts, clear windows',
            'tdt' => 'black, white containers, FEDERAL EXPRESS tampo',
        ],
// 17. MB045 cab in white, chrome exhausts, amber windows, beige containers, black trailer, "Smith's Crisps" labels, Macau
	['var' => '17a', 'cab' => 'MB045', 'mfg' => 'Macau', 'liv' => "Smith's",
            'cdt' => 'white, chrome exhausts, amber windows',
            'tdt' => "black, beige containers, SMITH'S CRISPS labels",
        ],
// 18. MB103 cab in red, chrome exhausts and antennas, clear windows, black containers, yellow trailer, "Matchbox" tampo, China, rubber tires (PC)
	['var' => '18a', 'cab' => 'MB310', 'mfg' => 'China', 'liv' => 'Matchbox',
            'cdt' => 'red, chrome exhausts and antennas, clear windows',
            'tdt' => 'yellow, black containers, MATCHBOX tampo',
        ],
    ]);
?>

<?php
}
?>

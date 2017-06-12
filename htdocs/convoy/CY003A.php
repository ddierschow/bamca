<?php // DONE
$subtitle = 'CY003A';
// CY-3-A DOUBLE CONTAINER TRUCK, issued 1982
$desc = "Double Container Truck";
$year = '1982';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. MB103 cab in red, chrome exhausts, clear windows, beige containers, black trailer, "Uniroyal" labels, England
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB103', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'Uniroyal', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'black, beige containers, UNIROYAL labels',
        ],
// 2. MB106 cab in red, chrome exhausts, amber windows, beige containers, black trailer, "Uniroyal" labels, England
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB106', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'Uniroyal', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, chrome exhausts, amber windows',
            'tdt' => 'black, beige containers, UNIROYAL labels',
        ],
// 3. MB106 cab in red, chrome exhausts, clear windows, beige containers, black trailer, "Uniroyal" labels, England
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB106', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'Uniroyal', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'black, beige containers, UNIROYAL labels',
        ],
// 4. MB106 cab in red, chrome exhausts, clear windows, light tan containers, black trailer, "Uniroyal" labels, England
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB106', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'Uniroyal', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'black, light tan containers, UNIROYAL labels',
        ],
// 5. MB106 cab in red, chrome exhausts, clear windows, beige containers, white trailer, "Uniroyal" labels, England
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB106', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'Uniroyal', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'white, beige containers, UNIROYAL labels',
        ],
// 6. MB106 cab in red, chrome exhausts, clear windows, cream containers, white trailer, "Uniroyal" labels, England
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB106', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'Uniroyal', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'white, cream containers, UNIROYAL labels',
        ],
// 7. MB103 cab in red, chrome exhausts, clear windows, beige containers, white trailer, "Uniroyal" labels, England
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB103', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'Uniroyal', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'white, beige containers, UNIROYAL labels',
        ],
// 8. MB106 cab in red, chrome exhausts, clear windows, brown containers, black trailer, "Uniroyal" labels, England
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB106', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'Uniroyal', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'black, brown containers, UNIROYAL labels',
        ],
// 9. MB045 cab in white, chrome exhausts, amber windows, beige containers, "Pepsi" labels, Macau
	['mod' => $subtitle, 'var' => '09a',
	    'cab' => 'MB045', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'Pepsi', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, chrome exhausts, amber windows',
            'tdt' => 'beige containers, PEPSI labels',
        ],
// 10. MB106 cab in black, chrome exhausts, clear windows, cream containers, "Pepsi" labels, England
	['mod' => $subtitle, 'var' => '10a',
	    'cab' => 'MB106', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'Pepsi', 'cod' => '1', 'rar' => '',
            'cdt' => 'black, chrome exhausts, clear windows',
            'tdt' => 'cream containers, PEPSI labels',
        ],
// 11. MB106 cab in black, chrome exhausts, clear windows, cream containers, black trailer, "Federal Express" labels, Macau
	['mod' => $subtitle, 'var' => '11a',
	    'cab' => 'MB106', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'Federal Express', 'cod' => '1', 'rar' => '',
            'cdt' => 'black, chrome exhausts, clear windows',
            'tdt' => 'black, cream containers, FEDERAL EXPRESS labels',
        ],
// 12. MB106 cab in white, chrome exhausts, clear windows, beige containers, black trailer, "Federal Express" labels, England
	['mod' => $subtitle, 'var' => '12a',
	    'cab' => 'MB106', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'Federal Express', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, chrome exhausts, clear windows',
            'tdt' => 'black, beige containers, FEDERAL EXPRESS labels',
        ],
// 13. MB106 cab in white, chrome exhausts, clear windows, white containers, black trailer, "Federal Express" tampo, Macau
	['mod' => $subtitle, 'var' => '13a',
	    'cab' => 'MB106', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'Federal Express', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, chrome exhausts, clear windows',
            'tdt' => 'black, white containers, FEDERAL EXPRESS tampo',
        ],
// 14. MB103 cab in red, chrome exhausts, clear windows, light tan containers, white trailer, "Mayflower" labels, England
	['mod' => $subtitle, 'var' => '14a',
	    'cab' => 'MB103', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'Mayflower', 'cod' => '1', 'rar' => '5',
            'cdt' => 'red, chrome exhausts, clear windows',
            'tdt' => 'white, light tan containers, MAYFLOWER labels',
        ],
// 15. MB106 cab in white, gray exhausts, clear windows, white containers, black trailer, "Federal Express" tampo, Macau
	['mod' => $subtitle, 'var' => '15a',
	    'cab' => 'MB106', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'Federal Express', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, gray exhausts, clear windows',
            'tdt' => 'black, white containers, FEDERAL EXPRESS tampo',
        ],
// 16. MB106 cab in white, gray exhausts, clear windows, white containers, black trailer, "Federal Express" tampo, Thailand
	['mod' => $subtitle, 'var' => '16a',
	    'cab' => 'MB106', 'tlr' => 'Double Container', 'mfg' => 'Thailand',
	    'liv' => 'Federal Express', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, gray exhausts, clear windows',
            'tdt' => 'black, white containers, FEDERAL EXPRESS tampo',
        ],
// 17. MB045 cab in white, chrome exhausts, amber windows, beige containers, black trailer, "Smith's Crisps" labels, Macau
	['mod' => $subtitle, 'var' => '17a',
	    'cab' => 'MB045', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => "Smith's", 'cod' => '1', 'rar' => '',
            'cdt' => 'white, chrome exhausts, amber windows',
            'tdt' => "black, beige containers, SMITH'S CRISPS labels",
        ],
// 18. MB103 cab in red, chrome exhausts and antennas, clear windows, black containers, yellow trailer, "Matchbox" tampo, China, rubber tires (PC)
	['mod' => $subtitle, 'var' => '18a',
	    'cab' => 'MB310', 'tlr' => 'Double Container', 'mfg' => 'China',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, chrome exhausts and antennas, clear windows',
            'tdt' => 'yellow, black containers, MATCHBOX tampo',
        ],
    ]);
?>

<p>
<table cellspacing="5" border="5" width="800" align="center">
  <tbody>
    <tr>
      <td valign="top"><b>Container Colors from left to right: <br>
	Brown, Tan, Beige &amp;<br> Cream</b></td>
      <td valign="top"><img src="/pic/convoy/m_cy003a_box2.jpg" title="" alt="" width="400" height="62"><br>
      </td>
    </tr>
    <tr>
      <td valign="top"><b></b>This series has both Peterbilt &amp; Mack
	cabs in it and the Uniroyal containers could any one of four different colors. <br>
      </td>
      <td valign="top"><img src="/pic/convoy/m_cy003a_box1.jpg" title="" alt="" width="400" height="202"><br>
      </td>
    </tr>
  </tbody>
</table>

<?php
}
?>

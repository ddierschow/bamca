<?php
$subtitle = 'CY047A';
$desc = "MCI Coach";
$year = '1999';

$defaults = ['mod' => $subtitle, 'cab' => 'CY047', 'tlr' => 'CY047', 'mfg' => '', 'cod' => '1', 'tdt' => ''];

include "cypage.php";

// MCI Coaches
// This series of buses is a sideline to the Convoy/Rig series consisting all of the same bus casting with different liveries. All models come with chrome disc with rubber wheels unless otherwise noted.

function body() {
    show_table([
// 37039 Coca Cola - red with 8-spoke wheels
	['var' => '01a', 'liv' => 'Coca-Cola',
            'cdt' => 'red, COCA-COLA',
	    'nts' => 'Product #37039',
	],
// 36798 McDonald's - yellow with 8-spoke wheels
	['var' => '02a', 'liv' => "McDonald's",
            'cdt' => "dark yellow, MCDONALD'S",
	    'nts' => 'Product #36798',
	],
// 37961 Jaws - powder blue
	['var' => '03a', 'liv' => 'Jaws',
            'cdt' => 'powder blue, JAWS',
	    'nts' => 'Product #37961',
	],
// 37962 Animal House -white
	['var' => '04a', 'liv' => 'Animal House',
            'cdt' => 'white, ANIMAL HOUSE',
	    'nts' => 'Product #37962',
	],
// 37964 Bewitched - dark blue
	['var' => '05a', 'liv' => 'Bewitched',
            'cdt' => 'dark blue, BEWITCHED',
	    'nts' => 'Product #37964',
	],
// 37965 Austin Powers - yellow
	['var' => '06a', 'liv' => 'Austin Powers',
            'cdt' => 'yellow, AUSTIN POWERS',
	    'nts' => 'Product #37965',
	],
// 37966 I Dream of Jeannie - white
	['var' => '07a', 'liv' => 'I Dream of Jeannie',
            'cdt' => 'white, I DREAM OF JEANNIE',
	    'nts' => 'Product #37966',
	],
// Scooby-Doo - lime
	['var' => '08a', 'liv' => 'Scooby-Doo',
            'cdt' => 'lime, SCOOBY-DOO',
	],
// 36767 Sydney 2000 - dark blue, 8-spoke wheels
	['var' => '09a', 'liv' => 'Sydney 2000',
            'cdt' => 'dark blue, SYDNEY 2000',
	    'nts' => 'Product #36767',
	],
// 38013 Disney 2000-white
	['var' => '10a', 'liv' => 'Disney',
            'cdt' => 'white, DISNEY 2000',
	    'nts' => 'Product #38013',
	],
// 35995 Disney 2001 - black, 8-spoke wheels
	['var' => '11a', 'liv' => 'Disney',
            'cdt' => 'black, DISNEY 2001',
	    'nts' => 'Product #35995',
	],
// 12.  orange, Walt Disney World 2002
	['var' => '12a', 'liv' => 'Disney',
            'cdt' => 'orange, DISNEY 2002',
	],
// 13.  powder blue, Walt Disney World 2003
	['var' => '13a', 'liv' => 'Disney',
            'cdt' => 'powder blue, DISNEY 2003',
	],
// 14.  metallic red, Looney Tunes
	['var' => '14a', 'liv' => 'Looney Tunes',
            'cdt' => 'metallic red, LOONEY TUNES',
	],
// 15.  white, Walt Disney World 2004
	['var' => '15a', 'liv' => 'Disney',
            'cdt' => 'white, DISNEY 2004',
	],
// 16.  white, Walt Disney World 2005
	['var' => '16a', 'liv' => 'Disney',
            'cdt' => 'white, DISNEY 2005',
	],
// 17.  dark yellow, Walt Disney World 2006
	['var' => '17a', 'liv' => 'Disney',
            'cdt' => 'dark yellow, DISNEY 2006',
	],
// 18.  wilver-gray, Walt Disney World 2007
	['var' => '18a', 'liv' => 'Disney',
            'cdt' => 'silver-gray, DISNEY 2007',
	],
// 19.  blue, Walt Disney World 2008
	['var' => '19a', 'liv' => 'Disney',
            'cdt' => 'blue, DISNEY 2008',
	],
// 20.  white, Walt Disney World 2009
	['var' => '20a', 'liv' => 'Disney',
            'cdt' => 'white, DISNEY 2009',
	],
// 21.  orange, Walt Disney World 2010
	['var' => '20a', 'liv' => 'Disney',
            'cdt' => 'orange, DISNEY 2010',
	],
// 22.  lime, Walt Disney World 2011
	['var' => '20a', 'liv' => 'Disney',
            'cdt' => 'lime, DISNEY 2011',
	],
// 23.  gray, Walt Disney World 2012
	['var' => '20a', 'liv' => 'Disney',
            'cdt' => 'gray, DISNEY 2012',
	],
// 24.  light blue, Walt Disney World 2013
	['var' => '20a', 'liv' => 'Disney',
            'cdt' => 'light blue, DISNEY 2013',
	],
// 25.  white, MCI Company Bus
	['var' => '20a', 'liv' => 'none',
            'cdt' => 'white',
	],
// 26.  blue, MCI Company Bus
	['var' => '20a', 'liv' => 'MCI',
            'cdt' => 'blue, MCI',
	],
// 27.  metallic green, Walt Disney World 2014
	['var' => '20a', 'liv' => 'Disney',
            'cdt' => 'metallic green, DISNEY 2014',
	],
// 28.  orange, Walt Disney World 2015
	['var' => '20a', 'liv' => 'Disney',
            'cdt' => 'orange, DISNEY 2015',
	],
    ]);
}
?>

<?php // DONE
$subtitle = 'CY111A';
// CY-111-A TEAM TRANSPORTER, issued 1989
$desc = "Team Transporter";
$year = '1989';

$defaults = ['mod' => $subtitle, 'cab' => 'CY010', 'tlr' => 'CY010', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. White transporter, gray exhausts, "Pioneer Racing Team" tampo; includes MB137 F.1 in white with "Matchbox" tampo (MC)
	['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Pioneer Racing Team',
	    'cdt' => 'white, gray exhausts, PIONEER RACING TEAM tampo',
	    'tdt' => 'MB137 F.1 in white with MATCHBOX tampo',
        ],
// 2. Orange transporter, chrome exhausts; includes MB224 Chevy Lumina in orange-both with "Hardees 18" tampo (DT)
	['var' => '02a', 'mfg' => 'Macau', 'liv' => 'Hardees',
	    'cdt' => 'orange, chrome exhausts',
	    'tdt' => 'MB224 Chevy Lumina in orange-both with HARDEES 18 tampo',
        ],
// 3. Orange transporter, chrome exhausts; includes MB221 Chevy Lumina in orange-both with "Hardees 18" tampo (DT)
	['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Hardees',
	    'cdt' => 'orange, chrome exhausts',
	    'tdt' => 'MB221 Chevy Lumina in orange-both with HARDEES 18 tampo',
        ],
// 4. Black and green transporter, chrome exhausts; includes MB224 Chevy Lumina in black and green-both with "Mello Yello 51" tampo (DT)
	['var' => '04a', 'mfg' => 'Macau', 'liv' => 'Mello Yello',
	    'cdt' => 'black and green, chrome exhausts',
	    'tdt' => 'MB224 Chevy Lumina in black and green-both with MELLO YELLO 51 tampo',
        ],
// 5. Black and green transporter, chrome exhausts; includes MB221 Chevy Lumina in black and green-both with "Mello Yello 51" tampo (DT)
	['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Mello Yello',
	    'cdt' => 'black and green, chrome exhausts',
	    'tdt' => 'MB221 Chevy Lumina in black and green-both with MELLO YELLO 51 tampo',
        ],
// 6. Blue and white transporter, chrome exhausts; includes MB137 F.1 Racer in blue and white-both with "Valvoline" tampo (IN)
	['var' => '06a', 'mfg' => 'Macau', 'liv' => 'Valvoline',
	    'cdt' => 'blue and white, chrome exhausts',
	    'tdt' => 'MB137 F.1 Racer in blue and white-both with VALVOLINE tampo',
        ],
// 7. Yellow transporter, chrome exhausts; includes MB203 G.R Racer in yellow-both with "Pennzoil 4" livery (IN)
	['var' => '07a', 'mfg' => 'Macau', 'liv' => 'Pennzoil',
	    'cdt' => 'yellow, chrome exhausts',
	    'tdt' => 'MB203 G.R Racer in yellow-both with PENNZOIL 4 livery',
        ],
// 8. Pink/white/blue transporter, chrome exhausts; includes MB137 F.1 Racer in pink/white/blue-both with "Amway" tampo (IN)
	['var' => '08a', 'mfg' => 'Macau', 'liv' => 'Amway',
	    'cdt' => 'pink/white/blue, chrome exhausts',
	    'tdt' => 'MB137 F.1 Racer in pink/white/blue-both with AMWAY tampo',
        ],
// 9. White and black transporter, chrome exhausts; includes MB203 G.R Racer in white and black both with "Havoline 5" tampo (IN)
	['var' => '09a', 'mfg' => 'Macau', 'liv' => 'Havoline',
	    'cdt' => 'white and black, chrome exhausts',
	    'tdt' => 'MB203 G.R Racer in white and black both with HAVOLINE 5 tampo',
        ],
// 10. Lemon transporter, chrome exhausts; includes MB203 G.R Racer in lemon-both with "Pennzoil 2" tampo (IN)
	['var' => '10a', 'mfg' => 'Macau', 'liv' => 'Pennzoil',
	    'cdt' => 'lemon, chrome exhausts',
	    'tdt' => 'MB203 G.R Racer in lemon-both with PENNZOIL 2 tampo',
        ],
// 11. Lavender/orange/white transporter, chrome exhausts; includes MB203 G.R Racer in lavender/orange/white-both with "Indy 1" tampo (IN)
	['var' => '11a', 'mfg' => 'Macau', 'liv' => 'Indy',
	    'cdt' => 'lavender/orange/white, chrome exhausts',
	    'tdt' => 'MB203 G.R Racer in lavender/orange/white-both with INDY 1 tampo',
        ],
// 12. White transporter, chrome exhausts; includes MB224 Chevy Lumina-both with no tampo (GF)
	['var' => '12a', 'mfg' => 'Macau', 'liv' => 'none',
	    'cdt' => 'white, chrome exhausts',
	    'tdt' => 'MB224 Chevy Lumina-both with no tampo',
        ],
// 13. Blue and white transporter, chrome exhausts; includes MB137 F.1 Racer in blue and white-both with "Mitre 10" tampo (AU)
	['var' => '13a', 'mfg' => 'Macau', 'liv' => 'Mitre 10',
	    'cdt' => 'blue and white, chrome exhausts',
	    'tdt' => 'MB137 F.1 Racer in blue and white-both with MITRE 10 tampo',
        ],
// 14. White/black transporter with chrome exhausts; includes MB203 G.R Racer in white/black with "Havoline 6" livery $8-12)(MN)
	['var' => '14a', 'mfg' => 'Macau', 'liv' => 'Havoline',
	    'cdt' => 'white/black transporter with chrome exhausts',
	    'tdt' => 'MB203 G.R Racer in white/black with HAVOLINE 6 livery',
        ],
// 15. White and dark blue transporter with chrome exhausts, "Valvoline Kraco 3" tampo; includes MB203 G.R Racer in dark blue/white, "Valvoline 3" tampo, Thailand castings (IN)
	['var' => '15a', 'mfg' => 'Thailand', 'liv' => 'Valvoline',
	    'cdt' => 'white and dark blue transporter with chrome exhausts, VALVOLINE KRACO 3 tampo',
	    'tdt' => 'MB203 G.R Racer in dark blue/white, VALVOLINE 3 tampo',
        ],
// 16. Red transporter with chrome exhausts, "Target/Scotch 9" tampo; includes MB203 G.R Racer in red with "Scotch 9" tampo, Thailand castings (IN)
	['var' => '16a', 'mfg' => 'Thailand', 'liv' => 'Target',
	    'cdt' => 'red transporter with chrome exhausts, TARGET/SCOTCH 9 tampo',
	    'tdt' => 'MB203 G.R Racer in red with SCOTCH 9 tampo',
        ],
// 17. Blue transporter with chrome exhausts, "Panasonic 11" tampo; includes MB203 G.R Racer in blue with "Panasonic 11" tampo, Thailand castings (IN)
	['var' => '17a', 'mfg' => 'Thailand', 'liv' => 'Panasonic',
	    'cdt' => 'blue transporter with chrome exhausts, PANASONIC 11 tampo',
	    'tdt' => 'MB203 G.R Racer in blue with PANASONIC 11 tampo',
        ],
// 18. Blue transporter with chrome exhausts, "Mackenzie 15" tampo; includes MB203 G.R Racer in blue with "Mackenzie 15" tampo, Thailand castings (IN)
	['var' => '18a', 'mfg' => 'Thailand', 'liv' => 'Mackenzie',
	    'cdt' => 'blue transporter with chrome exhausts, MACKENZIE 15 tampo',
	    'tdt' => 'MB203 G.R Racer in blue with MACKENZIE 15 tampo',
        ],
// 19. Red transporter with chrome exhausts, "Ferrari" tampo; MB246 Formula 1 in red with "Fiat 27" tampo, Thailand castings (FI)
	['var' => '19a', 'mfg' => 'Thailand', 'liv' => 'Ferrari',
	    'cdt' => 'red transporter with chrome exhausts, FERRARI tampo',
	    'tdt' => ' MB246 Formula 1 in red with FIAT 27 tampo',
        ],
// 20. White and dark blue transporter with chrome exhausts, "Canon Williams 0/Renault Elf" tampo; MB246 Formula 1 in dark blue and white, "Canon Williams 0" tampo, Thailand castings (FI)
	['var' => '20a', 'mfg' => 'Thailand', 'liv' => 'Canon Williams',
	    'cdt' => 'white and dark blue transporter with chrome exhausts, CANON WILLIAMS 0/RENAULT ELF tampo',
	    'tdt' => ' MB246 Formula 1 in dark blue and white, CANON WILLIAMS 0 tampo',
        ],
// 21. Red transporter with chrome exhausts and black ramp, "Ferrari 27" tampo, MB246 in red with "Ferrari 27" tampo, Thailand castings (F1)
	['var' => '21a', 'mfg' => 'Thailand', 'liv' => 'Ferrari',
	    'cdt' => 'red transporter with chrome exhausts and black ramp, FERRARI 27 tampo',
	    'tdt' => 'MB246 in red with FERRARI 27 tampo',
        ],
// 22. White and blue transporter with chrome exhausts, "Renault Elf 0" tampo, MB246 in white and blue with "Elf Renault 0" tampo, Thailand castings (F1)
	['var' => '22a', 'mfg' => 'Thailand', 'liv' => 'Renault',
	    'cdt' => 'white and blue transporter with chrome exhausts, RENAULT ELF 0 tampo',
	    'tdt' => 'MB246 in white and blue with ELF RENAULT 0 tampo',
        ],
// 23. Blue and white transporter with chrome exhausts and blue ramp, "Arrows" tampo, MB246 in white with "Uliveto 9" tampo, Thailand castings (F1)
	['var' => '23a', 'mfg' => 'Thailand', 'liv' => 'Arrows',
	    'cdt' => 'blue and white transporter with chrome exhausts and blue ramp, ARROWS tampo',
	    'tdt' => 'MB246 in white with ULIVETO 9 tampo',
        ],
// 24. Red transporter with chrome exhausts and black ramp, "Ferrari 27" tampo, MB246 in red with "Ferrari 27" tampo, China castings (F1)
	['var' => '24a', 'mfg' => 'China', 'liv' => 'Ferrari',
	    'cdt' => 'red transporter with chrome exhausts and black ramp, FERRARI 27 tampo',
	    'tdt' => 'MB246 in red with FERRARI 27 tampo',
        ],
// 25. Blue and white transporter with chrome exhausts and blue ramp, "Arrows" tampo, MB246 in white with "Uliveto 9" tampo, China castings (F1)
	['var' => '25a', 'mfg' => 'China', 'liv' => 'Arrows',
	    'cdt' => 'blue and white transporter with chrome exhausts and blue ramp, ARROWS tampo',
	    'tdt' => 'MB246 in white with ULIVETO 9 tampo',
        ],
// 26. White and blue transporter with chrome exhausts, "Renault Elf 0" tampo, MB246 in white and blue with "Elf Renault 0" tampo, China castings (F1)
	['var' => '26a', 'mfg' => 'China', 'liv' => 'Renault',
	    'cdt' => 'white and blue transporter with chrome exhausts, RENAULT ELF 0 tampo',
	    'tdt' => 'MB246 in white and blue with ELF RENAULT 0 tampo',
        ],
    ]);
}
?>

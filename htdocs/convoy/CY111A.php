<?php // DONE
$subtitle = 'CY111A';
// CY-111-A TEAM TRANSPORTER, issued 1989
$desc = "Team Transporter";
$year = '1989';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. White transporter, gray exhausts, "Pioneer Racing Team" tampo; includes MB137 F.1 in white with "Matchbox" tampo (MC)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white, gray exhausts, PIONEER RACING TEAM tampo',
	    'tdt' => 'MB137 F.1 in white with MATCHBOX tampo',
        ],
// 2. Orange transporter, chrome exhausts; includes MB224 Chevy Lumina in orange-both with "Hardees 18" tampo (DT)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'orange, chrome exhausts',
	    'tdt' => 'MB224 Chevy Lumina in orange-both with HARDEES 18 tampo',
        ],
// 3. Orange transporter, chrome exhausts; includes MB221 Chevy Lumina in orange-both with "Hardees 18" tampo (DT)
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'orange, chrome exhausts',
	    'tdt' => 'MB221 Chevy Lumina in orange-both with HARDEES 18 tampo',
        ],
// 4. Black and green transporter, chrome exhausts; includes MB224 Chevy Lumina in black and green-both with "Mello Yello 51" tampo (DT)
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'black and green, chrome exhausts',
	    'tdt' => 'MB224 Chevy Lumina in black and green-both with MELLO YELLO 51 tampo',
        ],
// 5. Black and green transporter, chrome exhausts; includes MB221 Chevy Lumina in black and green-both with "Mello Yello 51" tampo (DT)
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'black and green, chrome exhausts',
	    'tdt' => 'MB221 Chevy Lumina in black and green-both with MELLO YELLO 51 tampo',
        ],
// 6. Blue and white transporter, chrome exhausts; includes MB137 F.1 Racer in blue and white-both with "Valvoline" tampo (IN)
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'blue and white, chrome exhausts',
	    'tdt' => 'MB137 F.1 Racer in blue and white-both with VALVOLINE tampo',
        ],
// 7. Yellow transporter, chrome exhausts; includes MB203 G.R Racer in yellow-both with "Pennzoil 4" livery (IN)
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'yellow, chrome exhausts',
	    'tdt' => 'MB203 G.R Racer in yellow-both with PENNZOIL 4 livery',
        ],
// 8. Pink/white/blue transporter, chrome exhausts; includes MB137 F.1 Racer in pink/white/blue-both with "Amway" tampo (IN)
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'pink/white/blue, chrome exhausts',
	    'tdt' => 'MB137 F.1 Racer in pink/white/blue-both with AMWAY tampo',
        ],
// 9. White and black transporter, chrome exhausts; includes MB203 G.R Racer in white and black both with "Havoline 5" tampo (IN)
	['mod' => $subtitle, 'var' => '09a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white and black, chrome exhausts',
	    'tdt' => 'MB203 G.R Racer in white and black both with HAVOLINE 5 tampo',
        ],
// 10. Lemon transporter, chrome exhausts; includes MB203 G.R Racer in lemon-both with "Pennzoil 2" tampo (IN)
	['mod' => $subtitle, 'var' => '10a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'lemon, chrome exhausts',
	    'tdt' => 'MB203 G.R Racer in lemon-both with PENNZOIL 2 tampo',
        ],
// 11. Lavender/orange/white transporter, chrome exhausts; includes MB203 G.R Racer in lavender/orange/white-both with "Indy 1" tampo (IN)
	['mod' => $subtitle, 'var' => '11a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'lavender/orange/white, chrome exhausts',
	    'tdt' => 'MB203 G.R Racer in lavender/orange/white-both with INDY 1 tampo',
        ],
// 12. White transporter, chrome exhausts; includes MB224 Chevy Lumina-both with no tampo (GF)
	['mod' => $subtitle, 'var' => '12a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white, chrome exhausts',
	    'tdt' => 'MB224 Chevy Lumina-both with no tampo',
        ],
// 13. Blue and white transporter, chrome exhausts; includes MB137 F.1 Racer in blue and white-both with "Mitre 10" tampo (AU)
	['mod' => $subtitle, 'var' => '13a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'blue and white, chrome exhausts',
	    'tdt' => 'MB137 F.1 Racer in blue and white-both with MITRE 10 tampo',
        ],
// 14. White/black transporter with chrome exhausts; includes MB203 G.R Racer in white/black with "Havoline 6" livery $8-12)(MN)
	['mod' => $subtitle, 'var' => '14a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white/black transporter with chrome exhausts',
	    'tdt' => 'MB203 G.R Racer in white/black with HAVOLINE 6 livery',
        ],
// 15. White and dark blue transporter with chrome exhausts, "Valvoline Kraco 3" tampo; includes MB203 G.R Racer in dark blue/white, "Valvoline 3" tampo, Thailand castings (IN)
	['mod' => $subtitle, 'var' => '15a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white and dark blue transporter with chrome exhausts, VALVOLINE KRACO 3 tampo',
	    'tdt' => 'MB203 G.R Racer in dark blue/white, VALVOLINE 3 tampo',
        ],
// 16. Red transporter with chrome exhausts, "Target/Scotch 9" tampo; includes MB203 G.R Racer in red with "Scotch 9" tampo, Thailand castings (IN)
	['mod' => $subtitle, 'var' => '16a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'red transporter with chrome exhausts, TARGET/SCOTCH 9 tampo',
	    'tdt' => 'MB203 G.R Racer in red with SCOTCH 9 tampo',
        ],
// 17. Blue transporter with chrome exhausts, "Panasonic 11" tampo; includes MB203 G.R Racer in blue with "Panasonic 11" tampo, Thailand castings (IN)
	['mod' => $subtitle, 'var' => '17a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'blue transporter with chrome exhausts, PANASONIC 11 tampo',
	    'tdt' => 'MB203 G.R Racer in blue with PANASONIC 11 tampo',
        ],
// 18. Blue transporter with chrome exhausts, "Mackenzie 15" tampo; includes MB203 G.R Racer in blue with "Mackenzie 15" tampo, Thailand castings (IN)
	['mod' => $subtitle, 'var' => '18a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'blue transporter with chrome exhausts, MACKENZIE 15 tampo',
	    'tdt' => 'MB203 G.R Racer in blue with MACKENZIE 15 tampo',
        ],
// 19. Red transporter with chrome exhausts, "Ferrari" tampo; MB246 Formula 1 in red with "Fiat 27" tampo, Thailand castings (FI)
	['mod' => $subtitle, 'var' => '19a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'red transporter with chrome exhausts, FERRARI tampo',
	    'tdt' => ' MB246 Formula 1 in red with FIAT 27 tampo',
        ],
// 20. White and dark blue transporter with chrome exhausts, "Canon Williams 0/Renault Elf" tampo; MB246 Formula 1 in dark blue and white, "Canon Williams 0" tampo, Thailand castings (FI)
	['mod' => $subtitle, 'var' => '20a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white and dark blue transporter with chrome exhausts, CANON WILLIAMS 0/RENAULT ELF tampo',
	    'tdt' => ' MB246 Formula 1 in dark blue and white, CANON WILLIAMS 0 tampo',
        ],
// 21. Red transporter with chrome exhausts and black ramp, "Ferrari 27" tampo, MB246 in red with "Ferrari 27" tampo, Thailand castings (F1)
	['mod' => $subtitle, 'var' => '21a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'red transporter with chrome exhausts and black ramp, FERRARI 27 tampo',
	    'tdt' => 'MB246 in red with FERRARI 27 tampo',
        ],
// 22. White and blue transporter with chrome exhausts, "Renault Elf 0" tampo, MB246 in white and blue with "Elf Renault 0" tampo, Thailand castings (F1)
	['mod' => $subtitle, 'var' => '22a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white and blue transporter with chrome exhausts, RENAULT ELF 0 tampo',
	    'tdt' => 'MB246 in white and blue with ELF RENAULT 0 tampo',
        ],
// 23. Blue and white transporter with chrome exhausts and blue ramp, "Arrows" tampo, MB246 in white with "Uliveto 9" tampo, Thailand castings (F1)
	['mod' => $subtitle, 'var' => '23a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'blue and white transporter with chrome exhausts and blue ramp, ARROWS tampo',
	    'tdt' => 'MB246 in white with ULIVETO 9 tampo',
        ],
// 24. Red transporter with chrome exhausts and black ramp, "Ferrari 27" tampo, MB246 in red with "Ferrari 27" tampo, China castings (F1)
	['mod' => $subtitle, 'var' => '24a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'China',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'red transporter with chrome exhausts and black ramp, FERRARI 27 tampo',
	    'tdt' => 'MB246 in red with FERRARI 27 tampo',
        ],
// 25. Blue and white transporter with chrome exhausts and blue ramp, "Arrows" tampo, MB246 in white with "Uliveto 9" tampo, China castings (F1)
	['mod' => $subtitle, 'var' => '25a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'China',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'blue and white transporter with chrome exhausts and blue ramp, ARROWS tampo',
	    'tdt' => 'MB246 in white with ULIVETO 9 tampo',
        ],
// 26. White and blue transporter with chrome exhausts, "Renault Elf 0" tampo, MB246 in white and blue with "Elf Renault 0" tampo, China castings (F1)
	['mod' => $subtitle, 'var' => '26a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => 'China',
	    'liv' => '', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white and blue transporter with chrome exhausts, RENAULT ELF 0 tampo',
	    'tdt' => 'MB246 in white and blue with ELF RENAULT 0 tampo',
        ],
    ]);
}
?>

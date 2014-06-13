<?php

function FakeGetPageInfo($page_id)
{
    $pif = array();
    $pif['fake'] = 1;
    $pif['host'] = getenv('SERVER_NAME');
    $pif['docroot'] = getenv('DOCUMENT_ROOT');
    $pif['cgibin'] = $pif['docroot'] . '/../cgi-bin';
    $pif['isbeta'] = 0;
    $pif['format_type'] = 'php';
    $pif['pic_dir'] = 'pics';
    $pif['tail'] = '';
    $pif['flags'] = 0;
    if (substr($pif['host'], 0, 5) == 'beta.')
	$pif['isbeta'] = 1;
    $cfg = BarFile($pif['cgibin'] . '/.config', 'bamca.org');
    foreach (array_slice($cfg[0], 1) as $c)
    {
	$nl = explode(',', trim($c));
	$pif[$nl[0]] = $nl[1];
    }
    $pif['style'] = array();

    if ($page_id == "stuff")
    {
	$pif['title'] = 'BAMCA STUFF';
	$pif['style']['body'] = 'bgc,#CCCCCC';
	$pif['style']['tr'] = 'bgc,#FFFFFF';
    }

    if ($page_id == "index")
    {
	$pif['title'] = 'Bay Area Matchbox Collectors Association';
	$pif['flags'] = 2;
	$pif['style']['body'] = "bgi,url('gfx/bg10.gif');bgr,repeat-x;bgc,#D84905;c,#FFFFFF";
	$pif['style']['li'] = 'fz,16px';
	$pif['style']['a:link'] = 'c,#FFFF00';
	$pif['style']['a:visited'] = 'c,#FFFF99';
	$pif['style']['a:active'] = 'c,#FFFFFF';
	$pif['style']['a:hover'] = 'c,#FFFF99';
	$pif['style']['h1'] = 'ta,center';
    }

    if ($page_id == "about")
    {
	$pif['title'] = 'About the Bay Area Matchbox Collectors Association Website';
	$pif['flags'] = 2;
	$pif['style']['body'] = 'bgc,#000000';
	$pif['style']['table'] = 'bw,0;p,0;bsp,0';
	$pif['style']['td'] = 'bsp,0';
	$pif['style']['tr'] = 'bsp,0';
	$pif['style']['img'] = 'bw,0;va,middle';
	$pif['style']['.int'] = 'bgc,#FFFF00';
	$pif['style']['.horiz'] = 'bgi,url(../gfx/box-h.gif)';
	$pif['style']['.vert'] = 'bgi,url(../gfx/box-v.gif)';
	$pif['style']['.boxend'] = 'bgc,#000040;ta,center;va,middle;h,200px ';
    }

    if ($page_id == "3inch")
    {
	$pif['title'] = 'Matchbox Lineups';
	$pif['flags'] = 2;
	$pif['style']['.tdleft'] = 'ta,center;bs,solid;bw,1px;brw,0';
	$pif['style']['.tdright'] = 'ta,center;bs,solid;bw,1px;blw,0';
	$pif['style']['.tdboth'] = 'ta,center;bs,solid;bw,1px;ta,center;fw,bold';
    }

    if ($page_id == "series")
    {
	$pif['title'] = 'Matchbox Special Series';
	$pif['style']['body'] = 'bgc,#FFFFCC';
    }


    return $pif;
}

?>

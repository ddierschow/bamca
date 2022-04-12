<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("clubhist");
$pif['title'] = 'Bay Area <img src="/pic/gfx/matchboxw.gif" class="mblogo"> Collectors Association History';
DoHead($pif);
DoPageHeader($pif);
?>

<table class="framed">

<tr>
<th class="leftbar">1971</th>
<td class="bgwhite">
<a href="/pic/pages/club_certificate.jpg"><img src="/pic/pages/m_club_certificate.jpg" class="righty"></a>
BAMCA was founded April 15, 1971.
It was originally a chapter of the Matchbox Collectors Club, but persisted
long after that entity disappeared.
</td>
</tr>

<tr>
<th class="leftbar">1994</th>
<td class="bgoffwhite">
The website was started.
Originally it was just a list of links to other websites, but
one year Matchbox announced their new lineup in advance, and we thought it
would be cool to show it on the site.  Things snowballed from there.
</td>
</tr>

<tr>
<th class="leftbar">1996</th>
<td class="bgwhite">
<a href="/cgi-bin/vars.cgi?mod=MX113&var=03"><img src="/pic/man/var/m_mx113-03.jpg" class="righty"></a>
1996 was the 25th anniversary of the club.
We did a special club model that year, where we took the Matchbox Originals
Bedford Van and put different decals on it.
<p>
This was also when we got the official approval to use the Matchbox logo on
the website.
<p>
In December, an <a href="1996_12_18-paw.html">article</a> was published in the Palo Alto Weekly about one of our club members.
</td>
</tr>

<tr>
<th class="leftbar">1998</th>
<td class="bgoffwhite">
We bought the domain name.  Real work began on creating a
comprehensive information site about Matchbox Toys.  Most of the
scripting was written in PERL.
<p>
In December, an <a href="1998_12_24-nyt.html">article</a> was published in the New York Times that mentioned one of our club members.
</td>
</tr>

<tr>
<th class="leftbar">2000</th>
<td class="bgwhite">
The entire site was converted to Python.
</td>
</tr>

<tr>
<th class="leftbar">2004</th>
<td class="bgoffwhite">
The entire site was rewritten again to create a web
framework and use a more cohesive design.
</td>
</tr>

<tr>
<th class="leftbar">2010</th>
<td class="bgwhite">
In 2009 an effort was begun to convert the site to run off a MySQL
database.  This work completed in 2010.
There are still some old pages that run off of text files, but
almost everything that has to do with 3-inch models is in the DB.
<p>
We also added a <a href="https://www.facebook.com/Bay-Area-Matchbox-Collectors-Association-BAMCA-106213056100271/">FaceBook page</a>.  Feel free to "like" it!
</td>
</tr>

<tr>
<th class="leftbar">2014</th>
<td class="bgoffwhite">
At this point all the scripts that run the site were put into GitHub.
Anyone who is intereted in seeing this can contact us for more information.
</td>
</tr>

<tr>
<th class="leftbar">2015</th>
<td class="bgwhite">
The site was rewritten (again!) to use the Jinja2 rendering
engine.  This nakes much of the site simpler and easier to maintain.
</td>
</tr>

<tr>
<th class="leftbar">2016</th>
<td class="bgoffwhite">
All new pictures added to the site started being posted to our
<a href="http://bamca.tumblr.com/">tumblr account</a>.
</td>
</tr>

<tr>
<th class="leftbar">2017</th>
<td class="bgwhite">
Photographer credits were added to the site.  As the photographers were identified,
credits were added to the pictures.
</td>
</tr>

<tr>
<th class="leftbar">2018</th>
<td class="bgoffwhite">
A <a href="http://blog.bamca.org/">blog</a> was added to the site, for announcing website changes, meets, and other
club milestones.
<a href="http://blog.bamca.org/"><img src="/pic/misc/banner67_m.jpg" class="righty"></a>
</td>
</tr>

<tr>
<th class="leftbar">2020</th>
<td class="bgwhite">
The site changed servers and support infrastructure, requiring everything to be upgraded.
It was now running on a faster server with a newer database and newer versions of Python and
PHP.
</td>
</tr>

<tr>
<th class="leftbar">The Future</th>
<td class="bgoffwhite">
There's still much to do.  If you want to find out more, or how to contribute,
look at our <a href="status.php">website status page</a>.
</td>
</tr>

</table>
<hr>

This page is maintained by members of BAMCA.
<a href="faq.php">See here for information on contacting us.</a>

<?php
DoButtonComment($pif);
DoFoot($pif); ?>
</html>

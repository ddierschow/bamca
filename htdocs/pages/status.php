<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("status");
DoHead($pif);
DoPageHeader($pif);
?>

<h2 class="section">There are Several Projects Going On</h2>

Going forward, there are many plans for things to add, but they require time, which
is in short supply.  We'll do them when we can.

<ul>
<li><h4>The Category Project</h4>

There are categories associated with each variation.  I am currently working on populating this, and
building out the supporting machinery for this field.  Plus, there are many newer categories that
need to be added.

<li><h4>The Catalog Project</h4>

The catalog is incomplete, even for the mainline 3-inch models.  I am trying to get this
updated and newer variations inserted.  I also want to be able to allow download of
variation lists in JSON and CSV formats, and have multiple pictures of variations.
Also, many external links are currently broken.

<li><h4>The Lineup Project</h4>

There are several flaws with the current yearly lineups.  These fixes need to happen, among others:
<ul>
<li>fix Japan and Australia listings
<li>add Germany listings
<li>build out transitional models in 1969/1970
<li>add Challenger/Viper no. 1 transition around 1996, and similar transitions
<li>add previous year / next year buttons
</ul>

<li><h4>The Convoy Project</h4>

This is an import and update of John Baum's Convoy Project website.  It is complete as it sits,
but will need to be completely redone when I can add the trailers to the castings database.
Then the Convoys themselves will be added as a new kind of multi-packs.

<li><h4>The Collectibles Project</h4>

This should be a new division of the website, much like the Convoy Project.  I don't have a clear idea
of what it will look like.

<li><h4>The Skybusters Project</h4>

Another unbegun division of the website.  Perhaps to be based off of Alexander Veitch's work, if he will
give me permission to use it.

<li><h4>The Credits Project</h4>

This is mostly done, I just need to add credits where they are known but
not currently in the database.

<li><h4>The Restoration/Customization Project</h4>

There is a lot of information around on how to customize and restore diecast.  I'd like to add a curated customization how-to
section to the website to gather this information.

<li><h4>The Factories Project</h4>

You can now display lists of models by where they were manufactured.  Unfortunately,
a lot of variations are still missing this information.  I'd like to complete these lists.

<li><h4>The Programming Project</h4>

Much still needs to be done in the realm of the programming that supports this site.
Some of this includes:
<ul>
<li>Convert more rendering code to Jinja2
<li>Add an API
<li>Create a mobile-frendly site
<li>Redesign the database schema
<li>Document the BAMCA library
</ul>

</ul>

So, still one or two things to do...

<h2 class="section">Want to Help?</h2>

There is a lot of work still to be done on the site.

<ul>
<li>Pictures of variations that we don't have pictures for are helpful.  I prefer a shot taken over the left front fender, like
<a href="/pic/man/var/m_mx113-03.jpg">this</a>.  For Code 2's, I am much less picky.  The largest size I use is 600 pixels wide,
so if your pictures are at least that large, that's great.

<li>Product pictures are also always handy, especially for items in the database that don't have pictures yet.
The size varies by the format of the page I'm using, but the widest is no more than 800 pixels,
so anything bigger than that is good.
Product pictures should be as close to straight on forward as possible, without introducing glare from a flash.

<li>If you're interested in being a curator for one of the sections mentioned, please get in touch with me.
I'd love to work with others on these projects.

<li>I need information, and particularly publications, which would become property of BAMCA.<br>
I am missing the following Matchbox USA newsletters:
<ul>
<li>all issues from 1977, 1978, and 1979
<li>issues from 1980: January, February, March, May, and June
<li>issues from 1981: June through December
<li>issues from 2012: March through December
<li>all issues from 2013
<li>issues from 2015: January and February
<li>issues from 2016: February and April 
<li>issue from 2017: January
</ul>

I am missing the following AIM newsletters:
<ul>
<li>May, 1970 to April, 1972
<li>June, September, December of 1972
<li>January, April, November of 1973
<li>June, August, October of 1986
<li>April, 1987
<li>March, 1988 onward
</ul>

I am missing the following MICA newsletters:
<ul>
<li>Volume 1, issues 1, 2, 4
<li>Volume 2, issue 3
<li>Volume 7, issue 6
<li>Volume 8, issues 3, 6
<li>Volume 9, issues 2, 3
<li>Volume 12, issues 2, 3, 4, 5, 6
<li>Volume 13, issues 1, 3, 4, 5
<li>Volume 14, issue 3
<li>Volume 15, issue 4
<li>Volume 16, issue 3
<li>Volume 17, issues 1 and 3 onward
</ul>

<li>If you're a programmer and want to take part in script development, by all means get in touch.
The site is developed in Python for the cgi-bin scripts, with some PHP thrown in.  The data is stored
in a MySQL database, and the repository resides at GitHub.
These skills would be intrinsic to most of the work going on here.
Front-end help to make the site look snazzier would also be welcome.

</ul>

<h4>Contact me by using the "COMMENT ON THIS PAGE" button, or by sending an email to 
<b>volunteer@bamca.org</b>.  I'll respond as soon as I can.</h4>

<?php
DoButtonComment($pif);
DoFoot($pif);
?>
</html>

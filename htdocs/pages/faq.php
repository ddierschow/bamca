<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("faq");
$is_logged_in = CheckPerm('b');
DoHead($pif);
DoPageHeader($pif);
?>

We welcome correspondence.  We just ask that you read these questions and
answers first, to see if any of them meet your needs.   Please note that
if you send us email asking us a question that is on this list, it will
probably be ignored.  Sorry about that.
<p>

<table>
<tr><th width=24></th><th width=90%></th>

<tr><th valign="top">Q:</td>
<td valign="top">Who are you, anyway?
</td></tr>
<tr><th valign="top">A:</td>
<td valign="top">We are a bunch of collectors, probably like yourself.  For the most part,
we are not dealers; if we sell at all, it is whatever extras we picked up
along the way, or some other selling we might be dabbling with.  We are
<u>not</u> a company or a dealer.  The stuff you see on these webpages
are <u>not</u> to be interpreted as stuff we're selling.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">I have some toys.  How much are they worth?
</td></tr>
<tr><th valign="top">A:</td>
<td valign="top">There doesn't seem to be any clear authority as to the value of toys,
particularly older ones.  The methods that seem to work include:
<ol><li>Showing them to someone who is more experienced.
<li>Checking a book.  For Matchboxes, the best books seem to be the ones by
Charles Mack.
<li>Keep track of what similar pieces go for.  Look at what dealers of similar
toys are selling for, or how much people spend to buy them in an auction.</ol>
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">Where can I sell toys I own?
<tr><th valign="top">A:</td>
<td valign="top">We would recommend trying any of several places.  Perhaps, eBay or
other auction services; dealers that sell used toys; or groups of collectors.
If you are going to sell them, you should probably make up a list of what
you have, including conditions, and asking prices, if any.  These will help
garner interest in what you have.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">Where can I buy a particular brand of toys?
<tr><th valign="top">A:</td>
<td valign="top">We have tried to put our sources on these web pages.  We can only
encourage you to keep looking.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">How can I contact Matchbox?
<tr><th valign="top">A:</td>
<td valign="top">Mattel's headquarters are at 333 Continental Blvd., El Segundo, CA,
90245, USA.  That would probably be a good place to start.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>


<?php if ($is_logged_in) { ?>

<tr><th valign="top">Q:</td>
<td valign="top">How can I get in touch with another particular manufacturer?
<tr><th valign="top">A:</td>
<td valign="top">The ones we have information about are in the <a href="../cgi-bin/links.cgi?page=manuf">Manufacturers List.</a>
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>

<?php } ?>


<tr><th valign="top">Q:</td>
<td valign="top">What models of a particular car have been made?
<tr><th valign="top">A:</td>
<td valign="top">We don't really know of any comprehensive lists like this.  Over time, we
will be improving the lists we have for Matchbox, but there are so many
manufacturers that have made so many different models, that a good
comprehensive list will be a very large undertaking.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">How do I find other collectors to interact with?
<tr><th valign="top">A:</td>
<td valign="top">The best community on the internet that we've found is at
<a href="http://www.matchboxforum.co.uk/">the Matchobx Collectors Forum</a>.
That would be an excellent place to start meeting other collectors of Matchbox toys,
as well as other diecast toys.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">Why are Matchboxes from the 60's going for so much less than Hot Wheels
in similar condition?
<tr><th valign="top">A:</td>
<td valign="top">This is not really a question we can answer.  The best we can say is that
there seems to be more of a mystique about HotWheels that drives up the
price.  Also, this may be affected by the fact that HotWheels were only
introduced in the late 60's, so the first few years are much harder to
find, as nobody knew they were going to be popular.  The Matchbox line
had been in existance since 1953, so the people who were collecting them
at that time were pretty well established.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">What does the Lesney name mean?  Is this who made Matchboxes in the 60's?
<tr><th valign="top">A:</td>
<td valign="top">The name comes from the "Les" of Leslie Smith and the "Ney" of Rodney
Smith (no relation to each other) who founded the company.  This was the
name of the company until 1982, when it was sold to Universal Toys and
subsequently marketed under just the Matchbox name.  There is an excellent
history of Matchbox at
<a href="http://www.shabbir.com/matchbox/mbmenu.html">http://www.shabbir.com/matchbox/mbmenu.html</a>.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">I have a model that is plainly an error in manufacturing or packaging.  Is it worth more?
</td></tr>
<tr><th valign="top">A:</td>
<td valign="top">In this case, it entirely depends on the collector.  Some people love these and will
pay for them; others place no greater value on them than on any similar model.  Sorry, but we can't
give you any better estimate than this.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>


<?php if ($is_logged_in) { ?>

<tr><th valign="top">Q:</td>
<td valign="top">I have an old Matchbox, but I'm not sure which revision it is.  Can you help me figure this out?
</td></tr>
<tr><th valign="top">A:</td>
<td valign="top">On some of the early models, identifying which variation one is can be very difficult.
We have put together <a href="../cgi-bin/compare.cgi">this handy guide</a> to help determine the differences.<p>
Feel free to ask for clarification on any others.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>

<?php } ?>


<tr><th valign="top">Q:</td>
<td valign="top">Can I get the Manufacturing Number List in spreadsheet form?
</td></tr>
<tr><th valign="top">A:</td>
<td valign="top">You can get it in "csv" (Comma Seperated Value) form by selecting "List Type: CSV" and saving the page,
which can then be loaded into your spreadsheet application.  You can also download it in JSON format.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">How do I know if a model has been modified?
<tr><th valign="top">A:</td>
<td valign="top">Just for fun we've restored or modified a few old Matchbox cars
over the years, but doing a good job means taking them apart and
that means messing up the rivets which hold it together.  A good
clue that a model has been repainted is that the rivets on the base
look tampered with, or that the ends of the axles look tampered
with, or that there are any masking lines where windows, etc. have
been taped off.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">Can you tell me when a particular item will become available?
<tr><th valign="top">A:</td>
<td valign="top">Unfortunately, no.  Availability varies from region to region and
from country to country.  You'll just have to do what we do, loitering around
stores in your area waiting for trucks to come in, or hitting eBay yet again.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">Can you please sell me a particular toy?
<tr><th valign="top">A:</td>
<td valign="top">Probably not.  Remember, this website is not the instrument of a
company, but rather of a club of collectors like yourself.  If we have
anything for sale, we've put it up on a web page, referred within.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>


<?php if ($is_logged_in) { ?>

<tr><th valign="top">Q:</td>
<td valign="top">How can I find a particular model to buy?
<tr><th valign="top">A:</td>
<td valign="top">We have no magic sources for particular toys.  Keep looking.  Many older
toys can be found up for auction, particularly on eBay.  Keep
trying there, or checking other sites listed on the
<a href="../cgi-bin/links.cgi">toylinks pages</a>.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>

<?php } ?>


<tr><th valign="top">Q:</td>
<td valign="top">I have some toys I would like to sell.  Are your members interested
in buying them?
<tr><th valign="top">A:</td>
<td valign="top">Probably.  If you can make it to a meeting, that would be best.  Otherwise,
send me a list, and I'll forward it to the club members.  In either case,
send e-mail to us.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>


<?php if ($is_logged_in) { ?>

<tr><th valign="top">Q:</td>
<td valign="top">How do I find what updates have been done to the site recently?
<tr><th valign="top">A:</td>
<td valign="top">
Going forward, major site updates will announced on our <a href="http://blog.bamca.org/">Blog</a> page.
Minor updates will probably still not be logged anywhere.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">How do I find what pictures have been added to the site most recently?
<tr><th valign="top">A:</td>
<td valign="top">You can see the most recently added pictures by looking at our <a href="http://bamca.tumblr.com/">Tumblr</a> page.
Pictures are automatically posted there when they're added to the site.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">Would you add a link to my page on your toy links index?
<tr><th valign="top">A:</td>
<td valign="top">We'd be happy to.  <a href="../cgi-bin/addlink.cgi">Please use this page to send us the URL.</a>
Links sent via email will probably be delayed or ignored.
Please also don't get frustrated if it takes me a long time to put it up, as maintaining this
site isn't my Real Job.
We only add links to sites that have something to do with this hobby.  So if the site you want to add is,
for example, about hotel reservations, just go away.  Seriously.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>

<?php } ?>


<tr><th valign="top">Q:</td>
<td valign="top">Can we buy advertising space on your site?
<tr><th valign="top">A:</td>
<td valign="top">Not at present.  If or when BAMCA achieves 503(c) status, we will
consider selling ads at that time.  If that happens, we will put up a
notice on the <a href="about.php">"About this website" page</a>.
We will add links to our links pages upon request, however, but only if it is for a site related to the subject of this website.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">Can I place an ad in your newsletter?
<tr><th valign="top">A:</td>
<td valign="top">We don't really have a newsletter anymore.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">I live in Northern California, and wish to join your club.  How can I
join?
<tr><th valign="top">A:</td>
<td valign="top">Look on the <a href="contact.html">"How to join or contact the club"</a> page for directions.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">I live just about anywhere else and wish to join your club.  How can I
join?
<tr><th valign="top">A:</td>
<td valign="top">We have been mostly limiting our membership to people who live within
a few hours driving distance of the San Francisco Bay Area.  We haven't
been publishing a regular newsletter for a while, and as such, most of the
benefit from joining comes from being in the area.  However, if you still
really want to send us your $10, go ahead and follow the instructions on the
<a href="contact.html">"How to join or contact the club"</a> page.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>


<?php if ($is_logged_in) { ?>

<tr><th valign="top">Q:</td>
<td valign="top">I live somewhere outside if BAMCA's area.  Are there any clubs near me?
<tr><th valign="top">A:</td>
<td valign="top">The ones we know about are listed on our <a href="/cgi-bin/links.cgi?page=clubs">"clubs" page</a>.
Perhaps your best bet would be to join a national club.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>

<?php } ?>


<tr><th valign="top">Q:</td>
<td valign="top">Can you give me information on match boxes and match book covers?
<tr><th valign="top">A:</td>
<td valign="top">Sorry, no.  Our club is for small pieces of metal with wheels attached,
not small pieces of cardboard that can cause themselves to become on fire.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">I have information that I'd like to see added to this website.
What should I do?
<tr><th valign="top">A:</td>
<td valign="top">By all means, send it along!  Email is preferred, to
<b>staff@bamca.org</b>.  If you want to contribute images, you will find
an upload link on the main page for each casting.  Or, you can upload using
any the comment form, linked from almost every page.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">Even after reading these questions and answers, I still really want to
contact you.  How can I do it?
<tr><th valign="top">A:</td>
<td valign="top">You can feel free to write to us at
<b>staff@bamca.org</b>.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>



<tr><th valign="top">Q:</td>
<td valign="top">I tried sending you email but never got a response.  Why?
<tr><th valign="top">A:</td>
<td valign="top">We either never received it or just never responded.
We have heavy spam filters on our email, so if your message looked too
much like spam, it got dumped without being read.  Feel free to try again.
We've also had trouble with some providers (particularly AOL) dropping
email from us.
Keep in mind as well that this isn't our Real Job.  We also have Lives and
Families, and do this in our Copious Spare Time.  So, likewise, feel free
to try again.
</td></tr>

<tr><td colspan=2>&nbsp;</td></tr>

</table>

<?php
DoButtonComment($pif);
DoFoot($pif); ?>
</html>

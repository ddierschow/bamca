bamca
=====

Bay Area Matchbox Collectors Association

This repository contains much of the source code that runs "bamca.org".
There is still much missing but this is a start.  This repository
does not, and will not, contain the pictures from the site.
Absent that, the goal is to have enough recorded here that the
site could be recreated.

Please note that this was written by one person, and was never
intended to be shared or passed on, so the documentation is rare
to nonexistant.  I will be fixing that as I can.  It was also
written over the course of many years and represents much of my
learning process.

Milestones:

1994 - V1 - This project was started as a page of links to sites
that would be of interest to Matchbox collectors.

1998 - V2 - We bought the domain name, and I started working on the
lineup pages, writing the scripts in PERL.

2001 - V3 - I converted the entire site to Python.

2004ish - V4 - I substantially rewrote the site to use a web framework
and a more cohesive design.

2010 - V5 - The site was rewritten to run off of a MySql database.
There are still some old pages that run off of text files, but
almost everything that has to do with 3-inch models is in the DB.

    5.0 published Sunday, 11 July 2010 at 12:01 AM PDT
    5.1 published Monday, 12 April 2011 at 12:01 AM PDT
    5.2 published Monday, 16 May 2011 at 12:01 AM PDT
    5.3 published Monday, 01 August 2011 at 12:01 AM PDT
    5.4 published Monday, 07 September 2011 at 12:01 AM PDT
    5.5 published -- date not recorded
    5.6 published Sunday, 22 June 2014 at 12:01 AM PDT

2015 - V6 - This revision implements the Jinja2 rendering engine.
Most of the pages that are grids or lists have been switched over
to these new templates, and more will follow as I have time.

    6.0 published Sunday, 10 May 2015 at 12:01 AM PDT
    6.1 published Sunday, 6 September 2015 at 12:01 AM PDT
    6.2 published Sunday, 14 February 2016 at 12:01 AM PDT
    6.3 published Sunday, 17 April 2016 at 12:01 AM PDT
    6.4 published Sunday, 9 October 2016 at 12:01 AM PDT
    6.5 published Sunday, 13 November 2016 at 12:01 AM PST
    6.6 published Sunday, 29 January 2017 at 12:01 AM PST
    6.7 published Sunday, 18 June 2017 at 12:01 AM PDT
    6.8 published Sunday, 18 September 2017 at 12:01 AM PDT
    6.9 published Sunday, 19 November 2017 at 12:01 AM PST
    6.10 published Sunday, 11 February 2018 at 12:01 AM PST
    6.11 published Sunday, 11 March 2018 at 12:01 AM PST
    6.12 published Sunday, 14 October 2018 at 12:01 AM PDT
    6.13 published Sunday, 2 June 2019 at 12:01 AM PDT

2020 - V7 - A server migration forced a rewrite to Python 3.

    7.0 published Thursday, 20 February 2020 at 12:01 AM PST
    7.1 published Sunday, 8 May 2022 at 12:01 AM PDT
    7.2 published Sunday, 22 May 2022 at 12:01 AM PDT
    7.3 published Sunday, 29 May 2022 at 12:01 AM PDT
    7.4 published Sunday, 19 June 2022 at 12:01 AM PDT
    7.5 published Sunday, 26 February 2023 at 12:01 AM PST
    7.6 published Sunday, 1 August 2024 at 12:01 AM PDT
    7.7 published Sunday, 9 February 2025 at 12:01 AM PST


There are many plans for things to add, but they require time, which
is in short supply.  I'll do them when I can.  The most pressing
projects are to fill in more variation and product pictures, and
to add more models and products to the database.

Current and planned projects:

   * Add more entries to the annual lineup pages
   * Allow multiple pictures per variation
   * Link related variations
   * Add support for publications, playsets, packaging, etc.
   * Comparisons are getting better but still need work
   * Need to add support for packs limited to region
   * Matrix items with no ID aren't well supported
   * Add support for multiple castings at a number in a year (the 1969SE problem)

...BIG things:

   * Convert more rendering code to Jinja2
   * Add an API
   * Create a mobile-frendly site
   * Redesign the database schema

Projects independent of software version:

   * Build out data for related castings
   * Add larger-scale castings
   * Document the BAMCA library
   * Add more pictures!


Dean Dierschow
BAMCA Webmaster

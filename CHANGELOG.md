### 7.7.1  - 2025-02-09

- Tweaks and bugfixes

### 7.7.0  - 2025-02-08

- Added super search
- Renamed and rearranged several things
- moved a bunch of strings to f-strings
- implemented formatters for font-awesome icons
- added flags for exact/partial ids on supersearch

### 7.6.3  - 2024-09-28

- Add subname to pack models
- Switch lineup models to use link format rather than image format (as it should have)
- Make the pack list significantly faster
- Fix accent graphics on annual lineups

### 7.6.2  - 2024-09-21

- Add subname to lineup models
- Debugging variation selection in a lot of places
- Add styles to pack models
- More support for promotional models in lineups
- Completely remove var from pack model
- Move a lot of stuff to new background color styles

### 7.6.1  - 2024-08-15

- Lots of work on administration scripts
- Minor tweaks to UI
- Added material "plastic"
- Better implementation of variation selection on lineups
- Bugfixing
- Trying to add additional model sequences (moving parts, promos) to lineups,
  but it's still not working right

### 7.6 - 2024-08-01

- Many improvements to the administration scripts
- Added CSV with variations

### 7.5 - 2023-02-25

- Many improvements to the database editor
- Started development on a readers guide
- Security improvements

### 7.4 - 2022-06-19

- Added transitional King Size models to the Super Kings list
- Minor revision to single casting page when showing an associated product

### 7.3 - 2022-05-29

- Rewrite a lot of attribute formatting, including better deco and wheels
- Add more base logos

### 7.2 - 2022-05-22

- Rewriting of lots of internals
- Begin redesign of tampo/labels/deco/etc
- Made model icons work again
- Fix advertisements
- Add database tables for readers' guide

### 7.1 - 2022-05-08

- Rewriting of lots of internals
- Redesign vehicle makes list
- Minor changes to single model page

### 7.0.1 - 2022-04-09

- Minor fixes

### 7.0 - 2020-02-19

- Python3!
- flake8 compliant (see .flake8 file)
- Better error handling, including HTTP status codes
- Cookie management completely rewritten
- Added alpha site

### 6.13.1 - 2019-06-06

- Improve code for counts
- Add directory masking in urls
- Reconfigure some logs

### 6.13 - 2019-06-02

- Build out login mechanism
- Add photographer list to user profile
- Convert to using requests instead of urllib2
- Fix tumblr API calls
- Add mass lineup model
- Bulletproof form entry a little more
- Add filetypes for var lists
- Upgrade PHP version

### 6.12.5 - 2018-12-14

- Casting toy id changed to casting tool id
- Add variation list long form page

### 6.12.4 - 2018-12-10

- Revised Matchbox USA Ids page, to call out dupliate and missing IDs better
- Call out revised castings on "single" page
- Add basenames to "single" page
- Add editor support for bitfield columns
- Update use of dates in admin man lists
- Bugfix variation flags
- Support for base logos (phase 1)
- Call out primary Mack number in "single"
- Revise titles in "tables"
- Extend base attributes, like, a lot
- Add capability to copy base attributes from one var to another

### 6.12.3 - 2018-12-02

- Substantially rewrote the Matchbox USA ID pages, adding text format.
- Many small fixes and tweaks to help with entering info from MBUSA.
- Add variation verified/incorrect/unverified.

### 6.12.2 - 2018-11-11

- Substantial rewriting to the handling of Mack numbers
- Revised the datesearch page
- Add aliases editor

### 6.12.1 - 2018-10-31

- Minor change to display of Mack lists (more coming)
- Fix bug in searching for casting aliases
- Add Tumblr spool
- In traverse image pages, allow compact to be used with forms
- Add Alanstoys shoutout and auto credit
- Add ISBN to publication table
- Reword matrix images
- Add "blank" image support
- Allow merging multiple series appearances in single
- Better exception handling on file operations

### 6.12 - 2018-10-14

- Switch http references to https.
- Much rearranging of picture directory structure.
- Rewrite variation select to be more rigorous.
- Add support for playsets.
- Add relationship between playsets and the models they contain.
- Build out support for variation categories, with new category list.
- Improve showing the variation appearances significantly.
- Build out publications considerably, including puzzles, games, etc.
- Add database counts page (admin only).
- Add "Tilley" pages.
- A bunch of tweaking to the image editor.
- Officially phase out the "c" picture size (now "p").
- Add "contents" pictures to packs and playsets.
- Made multiyear lineup work again.
- Made variation by category lists considerably stronger.
- Add better icon support (separate from gfx).

### 6.11.1 - 2018-03-15

- Fixed code 2 bug for single model page
- Limit width on imgaes for the file system editor
- Show directory name, not path, for categories in imawidget
- Convert to fontawesome 5.0.5
- Fix box graphics on database page
 
### 6.11 - 2018-03-11

- Rewrote and extended the textual materials on the site
- Reformatted the "date" field on (most) variations
- Progress on the Category Project
    - Massive rewriting of category handling
    - Add category-style matrix pages
    - Add "by category" to the database page
- Rewrote the comment form, includinig adding upload image
- Quite a bit of rewriting of variation code
- Added credits to the "about" page
- Added the site status page
- Added the blog

### 6.10
6.10.2 - 2018-02-11
6.10.1 - 2018-02-11
6.10 - 2018-02-11

- Renamed a bunch of files in bin.
- Redo command line utilities, merging a bunch of little utilities
  into purpose-related scripts, or into unittests.
- Pounded on Result/Results, added them to a bunch of dbhand calls.
- Move page errors to counter table.
- Add paging support to dbhand.
- Add "by plants" pages.
- Add photographer pages.
- Add "with" to variations.
- Add mass attrpics and photogs.
- Add vehicle types building and horse-drawn.
- Add customized models page.
- Make php pages actually disconnect from database.
- Create new large scale models page to replace the models page.
- Redo look of main index page.
- Publish variation search page.

### 6.9.1 - 2019-03-13
### 6.9 - 2017-11-12

- Add functools.wraps to decorators
- Implement Results object for database queries
    Still not exactly right, but getting there.
    Moved a lot of random query logic into these objects.
- Implement use of Results object in several places
- Add database setting to tables entries
    Querying tables should now route to proper database transparently.
- Add user item table
    Haven't started implementing use of this yet.
- Add photographer couonts page
    Not ready for release.
- Promote credit on all photo promotions
- Multiyear lineup now calculates product properly
- Add "group" picture type
    Not currently in use anywhere.
- Build out more credits
- Implement radio buttons for image list types
- Add radio support to web forms
- Images now classified as Code 2 before "F"
- Add auto pic detection to the Tilley option
- Upload picture now checks '?' in url
- Add more command line options to variation lists
- Minor style changes, mainly for single
    Biggest difference is that var description now has beige backgroun.

### 6.8.3 - 2017-11-20
### 6.8.2 - 2017-10-01
### 6.8.1 - 2017-09-19
### 6.8 - 2017-09-17

- Add some nsa.gov dumpouts for scriptkiddies
- Move user table to buser
- Add command line user list to busers.py
- Add ckcat.py to help with cate => vs conversion
- Add ckcred.py to help with photo credits
- Add ckdup.py to help with keeping out duplicate database entries
- Rearrange pics to add "prod" and "set" levels
- Update ckschema.py
- Add ckvs.py to help with maintaining vs's
- Split out Mack listings into their own file
- Add variation by category
    Not complete yet.
- Massively rewrite annual lineups
    Seriously.  Threw it all out and started over.

### 6.7.1 - 2017-07-01

### 6.7 - 2017-06-18

- Added form tokens to deduplicate form submissions
- Work on user creation
- Add ebay aliasing to upload
- Add photographers and photo credits
- Add "revised casting"
- Add multipacks to matrix
- Work on model search
- Make var editor work bettee
- Added the Convoy Project
- Add var id to specific man id on database page

### 6.6.5 - 2017-05-07
### 6.6.4 - 2017-04-30
### 6.6.3 - 2017-02-19
### 6.6.2 - 2017-02-12
### 6.6.1 - 2017-02-04
### 6.6 - 2017-01-29
### 6.5.1 - 2016-11-13
### 6.5 - 2016-11-13
### 6.4 - 2016-10-09
### 6.3 - 2016-04-17
### 6.2 - 2016-02-14
### 6.1 - 2015-09-06
### 6.0.1 - 2015-05-10
### 6.0 - 2015-05-10

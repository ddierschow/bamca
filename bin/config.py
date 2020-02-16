#!/usr/local/bin/python
# flake8: noqa

CGI_BIN  	        = '../cgi-bin'
HTDOCS                  = '../htdocs'
LOG_ROOT                = '/home/bamca/logs'
ENV                     = 'unset'

IMG_DIR_ACC             = '/pic/set/acc'
IMG_DIR_ADD             = '/pic/man/add'
IMG_DIR_ADS             = '/pic/pub/ads'
IMG_DIR_ART             = '/pic/gfx'
IMG_DIR_BLISTER         = '/pic/pub/blister'
IMG_DIR_BOOK            = '/pic/pub/book'
IMG_DIR_BOX             = '/pic/pub/box'
IMG_DIR_CAT             = '/pic/pub/cat'
IMG_DIR_COLL_43         = '/pic/set/mcoll'
IMG_DIR_CONVOY          = '/pic/set/convoy'
IMG_DIR_ERRORS          = '/pic/set/error'
IMG_DIR_GAME            = '/pic/pub/game'
IMG_DIR_ICON            = '/pic/icon'
IMG_DIR_KING            = '/pic/set/king'
IMG_DIR_LESNEY          = '/pic/set/lesney'
IMG_DIR_MAKE            = '/pic/make'
IMG_DIR_MAN             = '/pic/man'
IMG_DIR_MAN_ICON        = '/pic/man/icon'
IMG_DIR_PACKAGE         = '/pic/pub/pkg'
IMG_DIR_PICS            = '/pic/pics'
IMG_DIR_PROD_BOOK       = '/pic/prod/book'
IMG_DIR_PROD_CODE_2     = '/pic/prod/code2'
IMG_DIR_PROD_COLL_64    = '/pic/prod/prem'
IMG_DIR_PROD_EL_SEG     = '/pic/prod/elseg'
IMG_DIR_PROD_LRW        = '/pic/prod/lrw'
IMG_DIR_PROD_LSF        = '/pic/prod/lsf'
IMG_DIR_PROD_MT_LAUREL  = '/pic/prod/mtlaurel'
IMG_DIR_PROD_MWORLD     = '/pic/prod/mworld'
IMG_DIR_PROD_ODDS       = '/pic/prod/odds'
IMG_DIR_PROD_PLAYSET    = '/pic/prod/playset'
IMG_DIR_SET_PLAYSET     = '/pic/set/playset'
IMG_DIR_SET_PACK        = '/pic/set/pack'
IMG_DIR_PROD_PACK       = '/pic/prod/pack'
IMG_DIR_PROD_SERIES     = '/pic/prod/series'
IMG_DIR_PROD_TYCO       = '/pic/prod/tyco'
IMG_DIR_PROD_UNIV       = '/pic/prod/univ'
IMG_DIR_SKY             = '/pic/set/sky'
IMG_DIR_VAR             = '/pic/man/var'

SRC_DIR                 = '/src'
BIN_DIR                 = '/bin'
LIB_DIR                 = '/lib'
LIB_MAN_DIR             = '/lib/man'
TRASH_DIR               = '/lib/trash'
FLAG_DIR                = '/pic/flags'
INC_DIR                 = '/home/bamca/inc'
PAGE_DIR                = '/pages'

CSS_DIR                 = '/styles'
CSS_FILE                = '/styles/main.css'
FONTS_FILE              = '/styles/fonts.css'

DEFAULT_X_SIZE          = 200
DEFAULT_Y_SIZE          = 120
MAX_MACK_NUMBER         = 125

LOG_PATH                = '../logs'
LOGGING_CONFIG_FILE     = '/src/logging.conf'

# constants for dealing with flags
FLAG_MODEL_NOT_MADE                     = 0x0001
FLAG_MODEL_CODE_2                       = 0x0002
FLAG_MODEL_NO_VARIATION                 = 0x0004
FLAG_MODEL_NO_ID                        = 0x0008
FLAG_MODEL_ID_INCORRECT                 = 0x0008
FLAG_MODEL_SHOW_ALL_VARIATIONS          = 0x0010
FLAG_MODEL_HIDE_IMAGE                   = 0x0020
FLAG_MODEL_NO_SPECIFIC_MODEL            = 0x0040
FLAG_MODEL_CASTING_REVISED              = 0x0080
FLAG_MODEL_VARIATION_VERIFIED           = 0x0080
FLAG_MODEL_BASEPLATE_VISIBLE            = 0x0100

FLAG_SECTION_HIDDEN                     = 0x0001
FLAG_SECTION_DEFAULT_IDS                = 0x0002
FLAG_SECTION_NO_FIRSTS                  = 0x0004
FLAG_SECTION_SHOW_IDS                   = 0x0008
FLAG_SECTION_HIDE_IMAGE                 = 0x0010
FLAG_SECTION_GROUP_SINGLES              = 0x0020

FLAG_ALIAS_PRIMARY                      = 0x0002
FLAG_MAKE_PRIMARY                       = 0x0002
FLAG_CASTING_RELATED_SHARED             = 0x0002
FLAG_LINEUP_MODEL_MULTI_VARS            = 0x0002

FLAG_ATTRIBUTE_SPARSE                   = 0x0001
FLAG_ATTRIBUTE_VISUAL                   = 0x0002

FLAG_CATEGORY_INDEXED                   = 0x0004

FLAG_PAGE_INFO_HIDDEN                   = 0x0001
FLAG_PAGE_INFO_HIDE_TITLE               = 0x0002
FLAG_PAGE_INFO_PUBLIC                   = 0x0010
FLAG_PAGE_INFO_ADMIN_ONLY               = 0x0080

FLAG_LINK_LINE_HIDDEN                   = 0x0001
FLAG_LINK_LINE_RECIPROCAL               = 0x0002
FLAG_LINK_LINE_PAYPAL                   = 0x0004
FLAG_LINK_LINE_INDENTED                 = 0x0008
FLAG_LINK_LINE_FORMAT_LARGE             = 0x0010
FLAG_LINK_LINE_NOT_VERIFIABLE           = 0x0020
FLAG_LINK_LINE_ASSOCIABLE               = 0x0040
FLAG_LINK_LINE_NEW                      = 0x0080
FLAG_LINK_LINE_DISABLED                 = 0x0100

FLAG_PHOTOGRAPHER_PRIVATE               = 0x0002

FLAG_ITEM_HIDDEN                        = 0x0001

FLAG_USER_BAMCA_MEMBER                  = 0x0010
FLAG_USER_VERIFIED                      = 0x0020
FLAG_USER_NEW                           = 0x0080
FLAG_USER_PASSWORD_RECOVERY             = 0x0100

LOCKDOWN = 0

# just puttin' this out here for future use
USER_ID = 0
IS_BETA = False
IS_ALPHA = False
GURU_ID = '__________'

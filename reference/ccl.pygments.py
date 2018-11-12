# -*- coding: utf-8 -*-
"""
    pygments.lexers.ccl
    ~~~~~~~~~~~~~~~~~~~

    Lexer for Cerner Command Language (CCL)

    Cerner Command Language (CCL) is a propietary SQL-like programming language
    which is used to interact with the Cerner Millenniuim database.
"""

import re

from pygments.lexer import Lexer, RegexLexer, bygroups, words
from pygments.token import *

__all__ = ['CclLexer']

# Compile-time conditional macro directives
# (Used only in the backend Discern Explorer (ccl) application?)
MACRO_DIRECTIVES = (
    'DEFINE', 'UNDEF',
    'IFDEF', 'IFNDEF',
    'ELSE', 'ENDIF'
) # END MACRO_DIRECTIVES #

# Built-in tables
BUILTIN_TABLES = ( 'DUMMYT' )

# Built-in fields
BUILTIN_FIELDS = ( 'SEQ' )

# Built-in variables
BUILTIN_VARS = (
    'COL',
    'CURACCEPT',
    'CURBATCH',
    'CURBEDROCK',
    'CURCCLREV',
    'CURCCLVER',
    'CURCLIENTID',
    'CURCLK',
    'CURDATE',
    'CURDOMAIN',
    'CURECHO',
    'CURENDREPORT',
    'CURENV',
    'CURGROUP',
    'CURHELP',
    'CURIMAGE',
    'CURLOCALE',
    'CURLOGDOMAIN',
    'CURMAXVARLEN',
    'CURMEM',
    'CURNETDOMAIN',
    'CURLOGDOMAINID',
    'CURNETDOMAIN',
    'CURNODE',
    'CURPAGE',
    'CURPRCNAME',
    'CURPROG',
    'CURQUAL',
    'CURRDB',
    'CURRDBACCESS',
    'CURRDBHANDLE',
    'CURRDBLINK',
    'CURRDBNAME',
    'CURRDBOPT',
    'CURRDBSYS',
    'CURRDBUSESR',
    'CURREF',
    'CURRETURN',
    'CURREV',
    'CURREVHNAM',
    'CURREVMINOR',
    'CURREVMINOR2',
    'CURRDBVER',
    'CURSCROLL',
    'CURSERVER',
    'CURSOURCE',
    'CURSYS',
    'CURSYS2',
    'CURSYSBIT',
    'CURTIME',
    'CURTIME2',
    'CURTIME3',
    'CURTIMEZONE',
    'CURTIMEZONEAPP',
    'CURTIMEZONEDEF',
    'CURTIMEZONESYS',
    'CURUSER',
    'CURUTC',
    'CURUTCDIFF',
    'CURWORK',
    'MAXCOL',
    'MAXROW',
    'ROW',
    'SYSDATE',
    'SYSTIMESTAMP'
) # END BUILTIN_VARS #

# Built-in functions
BUILTIN_FUNCS = (
    'ABS',
    'AESDECRYPT',
    'AESDECRYPTFILE',
    'AESENCRYPT',
    'AESENCRYPTFILE',
    'ALTER', 'ALTER2', 'ALTER3',
    'ALTERLIST',
    'ASIS',
    'ASSIGN', 'ASSIGN2', 'ASSIGN3',
    'BAND', 'BNOT', 'BOR', 'BXOR',
    'BLOBGET', 'BLOBGETLEN',
    'BSHIFT',
    'BTEST',
    'BUILD', 'BUILD2', 'BUILDCHK',
    'CALCPOS',
    'CALLPRG',
    'CCLIO',
    'CCLFMT',
    'CCLTIMER',
    'CEIL',
    'CHAR',
    'CHECK',
    'CHECKDIC',
    'CHECKFUN',
    'CHECKPRG',
    'CHECKQUEUE',
    'CLASS',
    'CLASSREF',
    'CNVTACC',
    'CNVTAGE', 'CNVTAGE2',
    'CNVTAGEDATETIME',
    'CNVTALIAS',
    'CNVTALPHANUM',
    'CNVTBOOL',
    'CNVTB10B16', 'CNVTB16B10',
    'CNVTB10B36', 'CNVTB36B10',
    'CNVTCAP',
    'CNVTDATE', 'CNVTDATE2',
    'CNVTDATETIME', 'CNVTDATETIME2',
    'CNVTDATETIMERDB',
    'CNVTDATETIMEUTC', 'CNVTDATETIMEUTC2', 'CNVTDATETIMEUTC3',
    'CNVTHEXRAW', 'CNVTRAWHEX',
    'CNVTINT',
    'CNVTJSONTOREC', 'CNVTRECTOJSON',
    'CNVTXMLTOREC', 'CNVTRECTOXML',
    'CNVTLOOKAHEAD',
    'CNVTLOOKBEHIND',
    'CNVTLONG',
    'CNVTLOWER',
    'CNVTMIN', 'CNVTMIN2',
    'CNVTNLS',
    'CNVTNLSSORT',
    'CNVTPHONE',
    'CNVTREAL',
    'CNVTSTRING', 'CNVTSTRINGCHK',
    'CNVTTIME','CNVTTIME2','CNVTTIME3',
    'CNVTTIMESTAMP',
    'CNVTUPPER',
    'CONCAT',
    'COPYREC',
    'COST',
    'CUBE',
    'CUME_DIST',
    'CURCODECOVER',
    'CURFILE',
    'CURLOB',
    'CURLOCALE',
    'CURPROG',
    'DATETIMEADD',
    'DATETIMECMP',
    'DATETIMECMPUTC',
    'DATETIMEDIFF'
    'DATETIMEFIND',
    'DATETIMEPART',
    'DATETIMETRUNC',
    'DATETIMEZONE',
    'DATETIMEZONEBYINDEX',
    'DATETIMEZONEBYNAME',
    'DATETIMEZONEFORMAT',
    'DATETIMEZONEUTC',
    'DAY',
    'DECODE',
    'DENSE_RANK',
    'ERROR',
    'EVALUATE', 'EVALUATE2',
    'EVEN',
    'EXP',
    'EXPAND',
    'FILLSTRING',
    'FINDFILE',
    'FINDSTRING',
    'FLOOR',
    'FORMAT',
    'GREATEST',
    'HOUR',
    'ICHAR',
    'INITARRAY',
    'INITREC',
    'ISNUMERIC',
    'JULIAN',
    'LEAST',
    'LIST',
    'LISTAGG',
    'LOCATEVAL',
    'LOCATEVALSORT',
    'LOG',
    'LOG10',
    'LOGICAL',
    'MAP',
    'MAXREC',
    'MAXVAL',
    'MEDIAN',
    'MEMALLOC',
    'MEMFREE',
    'MEMREALLOC',
    'MINUTE',
    'MINVAL',
    'MOD',
    'MODIFY',
    'MODCHECK',
    'MONTH',
    'MOVREC',
    'MOVRECLIST',
    'MOVESTRING',
    'NEGATE',
    'NOPATSTRING',
    'NORDBBIND',
    'NOTRIM',
    'NTILE',
    'NULL',
    'NULLCHECK',
    'NULLIND',
    'NULLTERM',
    'NULLVAL',
    'OPERATOR',
    'OUTERJOIN',
    'PARAMETER', 'PARAMETER2',
    'PARSER',
    'PATSTRING',
    'PERCENT_RANK',
    'PERCENTILE',
    'PIECE',
    'PROXYUSER',
    'RAND',
    'RANK',
    'RDBBIND',
    'RECTRAVERSE',
    'REFLECT',
    'REMOVE',
    'RENAMEREC',
    'REPLACE',
    'REPORTINFO',
    'REPORTMOVE',
    'REPORTROW',
    'ROLLUP',
    'ROUND',
    'ROW_NUMBER',
    'SELECTIVITY',
    'SEQ',
    'SIZE',
    'SORT',
    'SORTSEARCH',
    'SOUND',
    'SOUNDEX',
    'SQLPASSTHRU',
    'SUBSTRING',
    'TDBEXECUTE',
    'TEXT',
    'TEXTLEN',
    'TIMESTAMPDIFF',
    'TRACE',
    'TRIM',
    'TRIMBIND',
    'TYPE',
    'UAR_GET_CODE_BY',
    'UAR_GET_CODE_DESCRIPTION',
    'UAR_GET_CODE_DISPLAY',
    'UAR_GET_CODE_MEANING',
    'UAR_GET_DEFINITION',
    'UAR_GET_DISPLAYKEY',
    'UAR_GET_MEANING_BY_CODESET',
    'UAR_RTF',
    'UAR_RTF2',
    'VALIDATE',
    'VALUE',
    'WEEKDAY',
    'WTMODCHECK',
    'YEAR'
) # END BUILTIN_FUNCS #

# Built-in Aggregate Functions
BUILTIN_AGGREGATE_FUNCS = (
    'AVG',
    'COUNT',
    'MAX',
    'MEDIAN',
    'MIN',
    'PERCENT',
    'STDDEV',
    'SUM',
    'VARIANCE'
) # END BUILTIN_AGGREGATE_FUNCS #

# Command-line directives (used only in backend 'ccl' application)
CLI_DIRECTIVES = (
    'B', 'BANNER',
    'C', 'CLEAR',
    'D', 'DISPLAY',
    'E', 'EDIT',
    'H', 'HELP',
    'I', 'INCLUDE',
    'J', 'JOURNAL',
    'K', 'KEDIT',
    'L', 'LEDIT',
    'O', 'OUTPUT',
    'P', 'PRINT',
    'R', 'RUN',
    'S', 'SHOW',
    'T', 'TERMINAL',
    'V', 'VERSION',
    'Z'
) # END CLI_DIRECTIVES #

# Command-line commands (used only in backend 'ccl' application)
CLI_COMMANDS = (
    'RESET',
) # END CLI_COMMANDS #

# CALL Commands (used only in backend 'ccl' application)
CALL_COMMANDS = (
    'ACCEPT',
    'BOX',
    'CANCEL',
    'CCLEXCEPTION',
    'CENTER',
    'CLEAR',
    'COMPILE',
    'DCL',
    'DEBUG',
    'ECHO',
    'ECHOJSON',
    'ECHORECORD',
    'ECHOXML',
    'EDIT',
    'LINE',
    'PARSER',
    'PAUSE',
    'PRINT',
    'PRINTIMAGE',
    'SCROLLDOWN', 'SCROLLUP',
    'SCROLLINIT',
    'SCROLLTEXT',
    'TEXT',
    'TRACE',
    'VIDEO',
) # END CALL_COMMANDS #

# SET Commands
SET_COMMANDS = (
    'ACCEPT',
    'COMPILE',
    'CURACCEPT',
    'CURALIAS',
    'CURBEDROCK',
    'CURHELP',
    'CURLOCALE',
    'CURLOGDOMAIN',
    'CURNETDOMAIN',
    'CURNAMESPACE',
    'CURSCOPE',
    'DIR',
    'DOC',
    'ERROR',
    'HELP',
    'HOME',
    'LOGICAL',
    'MAXCOLWIDTH',
    'MESSAGE',
    'MODIFY',
    'PRIORITY',
    'SPOOL',
    'TRACE',
    'TRANSACTION',
    'VALIDATE',
    'VIEWS',
    'WARNING',
    'WIDTH',
) # END SET_COMMANDS #

# CREATE/DROP Commands (used to create/destroy database objects)
CREATE_COMMANDS = (
    'CCLMENU',
    'CCLTAM',
    'CCLUSER',
    'CLASS',
    'DATABASE',
    'DDLRECORD',
    'GENLINK',
    'PROGRAM',
    'RECORD',
    'TABLE',
    'VIEW'
) # END CREATE_COMMANDS #

# FREE Commands (used to release resources)
FREE_COMMANDS = (
    'DEFINE',
    'RANGE',
    'RECORD',
    'SELECT', 'DISTINCT', 'INTO', 'TABLE',
    'SET',
    'SUBROUTINE',
) # END FREE_COMMANDS #

# Database Commands (used on database object)
DB_COMMANDS = (
    'BROWSE',
    'DELETE',
    'INSERT',
    'SELECT', # + SELECT IF and SELECT INTO and SELECT INTO TABLE
    'UPDATE',
    'COMMIT', 'ROLLBACK',
    'DEFINE',
    'GENERATE', # + GENERATE DATABASE and GENERATE RECORD
    'GRANT', 'REVOKE',
    'MERGE',
    'RDB', # (sends SQL commands directly to the underlying relational database)
    'TRANSLATE',
) # END DB_COMMANDS #

# ReportWriter Commands (used only within a ReportWriter section)
RW_COMMANDS = (
    'BREAK',
    'COL',
    'ROW',
) # END RW_COMMANDS #

# Program Commands (used only outside a ReportWriter section)
PRG_COMMANDS = (
    'CASE', 'OF', 'ENDCASE',
    'DECLARE',
    'EXECUTE',
    'EXIT',
    'FOR', 'TO', 'BY', 'ENDFOR',
    'GO TO',
    'IF', 'ELSE', 'ELSIF', 'ENDIF',
    'MACRO',
    'RANGE',
    'RECORD',
    'RETURN',
    'SET',
    'SUBROUTINE',
    'WHILE', 'ENDWHILE',
) # END PRG_COMMANDS #

# Command Clauses
CMD_CLAUSES = (
    'WITH',
    'FROM',
    'PLAN', 'JOIN', 'ORJOIN',
    'WHERE',
    'GROUP BY',
    'HAVING',
    'ORDER', 'ORDER BY',
) # END CMD_CLAUSES #

# Operators
WORD_OPS = (
    'AND',
    'OR',
    'NOT',
    'BETWEEN',
    'IS',
    'LIKE'
) # END WORD_OPS #

line_re = re.compile('.*?\n')

var_datatype_re = r'(?:DM12|DQ8|F4|F8|U?I(?:1|2|4)|VC|W8|C\d+)'
var_name_re = r'[a-z0-9][a-z0-9_]*'

class CclLexer(RegexLexer):
    """
    Lexer for Cerner Command Language (CCL)
    """

    name = 'CCL'
    aliases = ['ccl']
    filenames = ['*.ccl', '*.prg']

    flags = re.IGNORECASE
    tokens = {
        # Root Level
        'root': [
            # Whitespace Characters
            (r'\s+', Text),
            # Single-line Comments
            #   Begin with ';' or '!' character
            #   Can be continued onto the next line by ending the line with backslash
            (r'[;!].*?(\\\n.*?)*\n', Comment.Single),
            # Multiple-line Comments
            #   Begin with '/*' and end with '*/'
            (r'/\*', Comment.Multiline, 'comment-multi'),
            # Command-line Directives (begin with '%' character)
            (words(CLI_DIRECTIVES, prefix=r'(?<=\n)( *)(%)', suffix=r'\b'), bygroups(Text,Operator,Keyword.Pseudo)),
            # Macro Directives (begin with '%#' characters)
            (words(MACRO_DIRECTIVES, prefix=r'(?<=\n)( *)(%#)', suffix=r'\b'), bygroups(Text,Operator,Keyword.Pseudo)),
            # Labels (begin with '#' character)
            (r'(?<=\n)( *)(#)(' + var_name_re + ')(\s*?\n)', bygroups(Text,Operator,Name.Label,Text)),
            # Operating System Directives (begin with '$' character)
            (r'(?<=\n)( *)(\$)(.*?\n)', bygroups(Text,Operator,Text)),
            # Built-In Variables/Constants
            (words(BUILTIN_VARS, prefix=r'\b', suffix=r'\b'), Name.Builtin),
            # Built-In Functions
            (words(BUILTIN_FUNCS, prefix=r'\b', suffix=r'\b'), Name.Builtin),
            (words(BUILTIN_AGGREGATE_FUNCS, prefix=r'\b', suffix=r'\b'), Name.Builtin),
            # END Command
            (r'\bEND\b', Keyword),
            # Go Command
            (r'\bGO\b', Keyword),
            # CALL Commands
            (words(CALL_COMMANDS, prefix=r'\b(CALL)(\s+)', suffix=r'\b'), bygroups(Keyword,Text,Keyword)),
            # CREATE Statement
            (words(CREATE_COMMANDS, prefix=r'\b(CREATE)(\s+)', suffix=r'(\s+)(' + var_name_re + ')'), bygroups(Keyword,Text,Keyword,Text,Name)),
            # DROP Statements
            (words(CREATE_COMMANDS, prefix=r'\b(DROP)(\s+)', suffix=r'(\s+)(' + var_name_re + ')'), bygroups(Keyword,Text,Keyword,Text,Name)),
            # FREE Statements
            (words(FREE_COMMANDS, prefix=r'\b(FREE)(\s+)', suffix=r'\b'), bygroups(Keyword,Text,Keyword)),
            # SET Statements
            (words(SET_COMMANDS, prefix=r'\b(SET)(\s+)', suffix=r'\b'), bygroups(Keyword,Text,Keyword)),
            # Standard Commands
            (words(DB_COMMANDS, prefix=r'\b', suffix=r'\b'), Keyword),
            (words(RW_COMMANDS, prefix=r'\b', suffix=r'\b'), Keyword),
            (words(PRG_COMMANDS, prefix=r'\b', suffix=r'\b'), Keyword),
            # User-Defined Variable/Constant Declaration
            (r'(DECLARE)(\s+)(' + var_name_re + ')(\s*)(\=)(\s*)(' + var_datatype_re + ')', bygroups(Keyword,Text,Name,Text,Operator,Text,Keyword.Type)),
            # Clauses
            (words(CMD_CLAUSES, prefix=r'\b', suffix=r'\b'), Keyword),
            # ReportWriter Clauses
            (r'(?<=\n)(\s*)(HEAD|FOOT)( +)(REPORT|PAGE)(\s*?\n)', bygroups(Text, Keyword, Text, Keyword, Text)),
            (r'(?<=\n)(\s*)(HEAD|FOOT)( +.*?\n)', bygroups(Text, Keyword, Text)),
            (r'(?<=\n)(\s*)(DETAIL)(\s*?\n)', bygroups(Text, Keyword, Text)),
            # String (Double Quotation Mark Delimited)
            (r'"[^"]*"', String.Double),
            # String (Single Quotation Mark Delimited)
            (r"'[^']*'", String.Single),
            # String (Caret Delimited)
            (r'\^[^\^]*\^', String),
            # String (Vertical Bar Delimited)
            (r'\|[^\|]*\|', String),
            # String (Tilde Delimited)
            (r'~[^~]*~', String),
            # String (At Sign Delimited with Numeric Length)
            (r'(@)(\d+)(:)([^@]*@)', bygroups(String,Number.Integer,Punctuation,String)),
            # Number (Decimal)
            (r'\b(\+|-)?(\d+\.\d+)\b', bygroups(Operator, Number.Float)),
            # Number (Whole Integer)
            (r'\b(\+|-)?(\d+)\b', bygroups(Operator, Number.Integer)),
            # Symbols (Operators)
            (r'[+*/<>=~!@#%^&|`?-]+', Operator),
            (words(('AND','OR','NOT','BETWEEN', 'IN','IS', 'LIKE'), prefix=r'\b', suffix=r'\b'), Operator.Word),
            # Symbols (Punctuation Marks)
            (r'[;:()\[\]{},.]', Punctuation),
        ],
        # Multiple-line Comment
        'comment-multi': [
            # Begin nested multiple-line comment
            (r'/\*', Comment.Multiline, 'comment-multi'),
            # End multiple-line comment
            (r'\*/', Comment.Multiline, '#pop'),
            # Non-terminating text within the multiple-line comment
            (r'[^/*]+', Comment.Multiline),
            # Non-terminating '/' and '*' characters within the multiple-line comment
            (r'[/*]+', Comment.Multiline)
        ],
        # ReportWriter Section
    }

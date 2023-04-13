#include "pch.h" 
#include "framework.h" 
#include "Compress.h" 
#include "CompressDlg.h" 
#include "afxdialogex.h" 
#include<iostream> 
#include<string> 
#include<map> 
#include<fstream> 
using namespace std ; 
#ifdef _DEBUG 
#define new DEBUG_NEW 
#endif 
void encode ( ) ; 
string uncompress ( string file_path , map <string, unsigned char> map_ , unsigned char num ) ; 
string compress ( string file_path , map <string, unsigned char> & map_ , unsigned char num ) ; 
string del_indent ( string file_path ) ; 
string del_notes ( string file_path ) ; 
map <string, unsigned char> map_ ; 
unsigned char num = 0 ; 
string file_path = "test.cpp" ; 
class CAboutDlg : public CDialogEx 
{ 
public : 
CAboutDlg ( ) ; 
#ifdef AFX_DESIGN_TIME 
enum { IDD = IDD_ABOUTBOX } ; 
#endif 
protected : 
virtual void DoDataExchange ( CDataExchange * pDX ) ; 
protected : 
DECLARE_MESSAGE_MAP ( ) 
} ; 
CAboutDlg :: CAboutDlg ( ) : CDialogEx ( IDD_ABOUTBOX ) 
{ 
} 
void CAboutDlg :: DoDataExchange ( CDataExchange * pDX ) 
{ 
CDialogEx :: DoDataExchange ( pDX ) ; 	 
} 
BEGIN_MESSAGE_MAP ( CAboutDlg , CDialogEx ) 
END_MESSAGE_MAP ( ) 
CCompressDlg :: CCompressDlg ( CWnd * pParent 
: CDialogEx ( IDD_COMPRESS_DIALOG , pParent ) 
, m_showcpp ( _T ( "" ) ) 
{ 
m_hIcon = AfxGetApp ( ) -> LoadIcon ( IDR_MAINFRAME ) ; 
} 
void CCompressDlg :: DoDataExchange ( CDataExchange * pDX ) 
{ 
CDialogEx :: DoDataExchange ( pDX ) ; 
DDX_Text ( pDX , IDC_COMPRESS_EDIT , m_showcpp ) ; 
} 
BEGIN_MESSAGE_MAP ( CCompressDlg , CDialogEx ) 
ON_WM_SYSCOMMAND ( ) 
ON_WM_PAINT ( ) 
ON_WM_QUERYDRAGICON ( ) 
ON_BN_CLICKED ( IDC_BROWSE_BUTTON , & CCompressDlg :: OnBnClickedBrowseButton ) 
ON_BN_CLICKED ( IDC_COMPRESS_BUTTON , & CCompressDlg :: OnBnClickedCompressButton ) 
ON_BN_CLICKED ( IDC_UNCOMPRESS_BUTTON , & CCompressDlg :: OnBnClickedUncompressButton ) 
END_MESSAGE_MAP ( ) 
BOOL CCompressDlg :: OnInitDialog ( ) 
{ 
CDialogEx :: OnInitDialog ( ) ; 
ASSERT ( ( IDM_ABOUTBOX & 0xFFF0 ) == IDM_ABOUTBOX ) ; 
ASSERT ( IDM_ABOUTBOX < 0xF000 ) ; 
CMenu * pSysMenu = GetSystemMenu ( FALSE ) ; 
if ( pSysMenu != nullptr ) 
{ 
BOOL bNameValid ; 
CString strAboutMenu ; 
bNameValid = strAboutMenu . LoadString ( IDS_ABOUTBOX ) ; 
ASSERT ( bNameValid ) ; 
if ( ! strAboutMenu . IsEmpty ( ) ) 
{ 
pSysMenu -> AppendMenu ( MF_SEPARATOR ) ; 
pSysMenu -> AppendMenu ( MF_STRING , IDM_ABOUTBOX , strAboutMenu ) ; 
} 
} 
SetIcon ( m_hIcon , TRUE ) ; 	 	 	 
SetIcon ( m_hIcon , FALSE ) ; 	 	 
return TRUE ; 
} 
void CCompressDlg :: OnSysCommand ( UINT nID , LPARAM lParam ) 
{ 
if ( ( nID & 0xFFF0 ) == IDM_ABOUTBOX ) 
{ 
CAboutDlg dlgAbout ; 
dlgAbout . DoModal ( ) ; 
} 
else 
{ 
CDialogEx :: OnSysCommand ( nID , lParam ) ; 
} 
} 
void CCompressDlg :: OnPaint ( ) 
{ 
if ( IsIconic ( ) ) 
{ 
CPaintDC dc ( this ) ; 
SendMessage ( WM_ICONERASEBKGND , reinterpret_cast <WPARAM> ( dc . GetSafeHdc ( ) ) , 0 ) ; 
int cxIcon = GetSystemMetrics ( SM_CXICON ) ; 
int cyIcon = GetSystemMetrics ( SM_CYICON ) ; 
CRect rect ; 
GetClientRect ( & rect ) ; 
int x = ( rect . Width ( ) - cxIcon + 1 ) / 2 ; 
int y = ( rect . Height ( ) - cyIcon + 1 ) / 2 ; 
dc . DrawIcon ( x , y , m_hIcon ) ; 
} 
else 
{ 
CDialogEx :: OnPaint ( ) ; 
} 
} 
HCURSOR CCompressDlg :: OnQueryDragIcon ( ) 
{ 
return static_cast <HCURSOR> ( m_hIcon ) ; 
} 
CString ConvertUTF8ToCString ( std :: string utf8str ) 
{ 
int nLen = :: MultiByteToWideChar ( CP_UTF8 , NULL , 
utf8str . data ( ) , utf8str . size ( ) , NULL , 0 ) ; 
std :: wstring wbuffer ; 
wbuffer . resize ( nLen ) ; 
:: MultiByteToWideChar ( CP_UTF8 , NULL , utf8str . data ( ) , utf8str . size ( ) , 
( LPWSTR ) ( wbuffer . data ( ) ) , wbuffer . length ( ) ) ; 
#ifdef UNICODE 
return ( CString ( wbuffer . data ( ) , wbuffer . length ( ) ) ) ; 
#else 
nLen = WideCharToMultiByte ( CP_ACP , 0 , 
wbuffer . data ( ) , wbuffer . length ( ) , NULL , 0 , NULL , NULL ) ; 
std :: string ansistr ; 
ansistr . resize ( nLen ) ; 
WideCharToMultiByte ( CP_ACP , 0 , ( LPWSTR ) ( wbuffer . data ( ) ) , wbuffer . length ( ) , 
( LPSTR ) ( ansistr . data ( ) ) , ansistr . size ( ) , NULL , NULL ) ; 
return ( CString ( ansistr . data ( ) , ansistr . length ( ) ) ) ; 
#endif 
} 
void CCompressDlg :: OnBnClickedBrowseButton ( ) 
{ 
UpdateData ( TRUE ) ; 
ifstream ifs ( "test.cpp" , ios :: in ) ; 
string str1 ; 
string read_str ; 
while ( ! ifs . eof ( ) ) { 
getline ( ifs , read_str ) ; 
str1 += read_str ; 
str1 += "\r\n" ; 
} 
m_showcpp = ConvertUTF8ToCString ( str1 ) ; 
UpdateData ( FALSE ) ; 
} 
string compress ( string file_path , map <string, unsigned char> & map_ , unsigned char num = 0 ) { 
string file_path_encode = file_path ; 
int pos = file_path_encode . find ( "." ) ; 
file_path_encode . insert ( pos , "_encode" ) ; 
file_path = del_notes ( file_path ) ; 
string file_path_del = del_indent ( file_path ) ; 
ifstream ifs ; 
ifs . open ( file_path_del , ios :: in ) ; 
ofstream ofs ; 
ofs . open ( file_path_encode , ios :: out | ios :: binary ) ; 
char read_c ; 
while ( ! ifs . eof ( ) && ifs . get ( read_c ) ) 
{ 
if ( isalpha ( read_c ) || read_c == '_' ) 
{ 
int length = 0 ; 
char word [ 20 ] ; 
word [ length ++ ] = read_c ; 
while ( true ) 
{ 
ifs . get ( read_c ) ; 
if ( ( ! isalpha ( read_c ) ) && ( ! isalnum ( read_c ) ) && ( read_c != '_' ) ) 
break ; 
else 
word [ length ++ ] = read_c ; 
} 
word [ length ] = '\0' ; 
string word_str = word ; 
string read_str = string ( 1 , read_c ) ; 
if ( map_ . find ( word_str ) != map_ . end ( ) ) 
ofs . write ( ( char * ) & ( map_ [ word_str ] ) , sizeof ( map_ [ word_str ] ) ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ "IDENTIFIER" ] , sizeof ( map_ [ "IDENTIFIER" ] ) ) ; 
unsigned char length_uc = length ; 
ofs . write ( ( char * ) & length_uc , 1 ) ; 
ofs . write ( ( char * ) word , length * sizeof ( char ) ) ; 
} 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
else if ( isalnum ( read_c ) ) 
{ 
int length = 0 ; 
char word [ 20 ] ; 
word [ length ++ ] = read_c ; 
while ( ifs . get ( read_c ) ) 
{ 
if ( ( ! isalnum ( read_c ) ) && ( ! isalpha ( read_c ) ) && ( read_c != '.' ) && ( read_c != '-' ) ) 
break ; 
else 
word [ length ++ ] = read_c ; 
} 
string read_str = string ( 1 , read_c ) ; 
ofs . write ( ( char * ) & map_ [ "NUMBER" ] , sizeof ( map_ [ "NUMBER" ] ) ) ; 
unsigned char length_uc = length ; 
ofs . write ( ( char * ) & length_uc , 1 ) ; 
ofs . write ( ( char * ) word , length * ( sizeof ( char ) ) ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
else if ( read_c == '+' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '+' ) 
ofs . write ( ( char * ) & map_ [ "++" ] , 1 ) ; 
else if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ "+=" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ "+" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '-' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '-' ) 
ofs . write ( ( char * ) & map_ [ "--" ] , 1 ) ; 
else if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ "-=" ] , 1 ) ; 
else if ( read_c == '>' ) 
ofs . write ( ( char * ) & map_ [ "->" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ "-" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '*' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ "*=" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ "*" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '%' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ "%=" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ "%" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '=' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ "==" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ "=" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '/' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ "/=" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ "/" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '&' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '&' ) 
ofs . write ( ( char * ) & map_ [ "&&" ] , 1 ) ; 
else if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ "&=" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ "&" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '|' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '|' ) 
ofs . write ( ( char * ) & map_ [ "||" ] , 1 ) ; 
else if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ "|=" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ "|" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '!' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ "!=" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ "!" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '^' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ "^=" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ "^" ] , 1 ) ; 
} 
} 
else if ( read_c == '<' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '<' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ "<<=" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ "<<" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ "<=" ] , 1 ) ; 
else if ( isalpha ( read_c ) ) 
{ 
int length = 0 ; 
char word [ 50 ] ; 
word [ length ++ ] = '<' ; 
word [ length ++ ] = read_c ; 
while ( ifs . get ( read_c ) ) 
{ 
word [ length ++ ] = read_c ; 
if ( read_c == '>' ) 
break ; 
} 
unsigned char length_uc = length ; 
ofs . write ( ( char * ) & map_ [ "STRING" ] , 1 ) ; 
ofs . write ( ( char * ) & length_uc , 1 ) ; 
ofs . write ( ( char * ) word , length * sizeof ( char ) ) ; 
} 
else 
{ 
ofs . write ( ( char * ) & map_ [ "<" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '>' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '>' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '=' ) 
ofs . write ( ( char * ) & map_ [ ">>=" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ ">>" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '=' ) 
{ 
ofs . write ( ( char * ) & map_ [ ">=" ] , 1 ) ; 
} 
else 
{ 
ofs . write ( ( char * ) & map_ [ ">" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else if ( read_c == '\"' ) 
{ 
int length = 0 ; 
char word [ 50 ] ; 
word [ length ++ ] = read_c ; 
while ( ifs . get ( read_c ) ) 
{ 
word [ length ++ ] = read_c ; 
if ( read_c == '\"' ) 
break ; 
} 
word [ length ++ ] = '\0' ; 
unsigned char length_uc = length ; 
ofs . write ( ( char * ) & map_ [ "STRING" ] , 1 ) ; 
ofs . write ( ( char * ) & length_uc , 1 ) ; 
ofs . write ( ( char * ) word , length * sizeof ( char ) ) ; 
} 
else if ( read_c == '\'' ) 
{ 
int length = 0 ; 
char word [ 6 ] ; 
word [ length ++ ] = read_c ; 
while ( ifs . get ( read_c ) ) 
{ 
if ( int ( read_c ) == 92 ) 
{ 
word [ length ++ ] = read_c ; 
ifs . get ( read_c ) ; 
word [ length ++ ] = read_c ; 
} 
else if ( read_c == '\'' ) 
{ 
word [ length ++ ] = read_c ; 
break ; 
} 
else 
word [ length ++ ] = read_c ; 
} 
unsigned char length_uc = length ; 
ofs . write ( ( char * ) & map_ [ "CHAR" ] , 1 ) ; 
ofs . write ( ( char * ) & length_uc , 1 ) ; 
ofs . write ( ( char * ) word , length * sizeof ( char ) ) ; 
} 
else if ( read_c == ' ' ) 
continue ; 
else if ( read_c == '#' ) 
{ 
int length = 0 ; 
char word [ 30 ] ; 
word [ length ++ ] = '#' ; 
while ( ifs . get ( read_c ) ) 
{ 
if ( read_c == '\r' || read_c == '\n' ) 
break ; 
else 
word [ length ++ ] = read_c ; 
} 
ofs . write ( ( char * ) & map_ [ "IDENTIFIER" ] , 1 ) ; 
unsigned char length_uc = length ; 
ofs . write ( ( char * ) & length_uc , 1 ) ; 
ofs . write ( ( char * ) word , length * ( sizeof ( char ) ) ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
else if ( read_c == ':' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == ':' ) 
ofs . write ( ( char * ) & map_ [ "::" ] , 1 ) ; 
else 
{ 
ofs . write ( ( char * ) & map_ [ ":" ] , 1 ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
} 
else 
{ 
string read_str = string ( 1 , read_c ) ; 
ofs . write ( ( char * ) & map_ [ read_str ] , 1 ) ; 
} 
} 
ifs . close ( ) ; 
ofs . close ( ) ; 
remove ( file_path . c_str ( ) ) ; 
remove ( file_path_del . c_str ( ) ) ; 
return file_path_encode ; 
} 
string del_notes ( string file_path ) 
{ 
ifstream ifs ; 
ifs . open ( file_path , ios :: in ) ; 
int pos = file_path . find ( '.' ) ; 
file_path . insert ( pos , "_del_notes" ) ; 
ofstream ofs ; 
ofs . open ( file_path , ios :: out ) ; 
char read_c ; 
while ( ! ifs . eof ( ) && ifs . get ( read_c ) ) 
{ 
if ( read_c == '\'' ) 
{ 
ofs << read_c ; 
while ( ifs . get ( read_c ) ) 
{ 
if ( int ( read_c ) == 92 ) { 
ofs << read_c ; 
ifs . get ( read_c ) ; 
ofs << read_c ; 
} 
else if ( read_c != '\'' ) 
ofs << read_c ; 
else 
{ 
ofs << read_c ; 
break ; 
} 
} 
} 
else if ( read_c == '\"' ) 
{ 
ofs << read_c ; 
while ( ifs . get ( read_c ) ) 
{ 
if ( read_c != '\"' ) 
ofs << read_c ; 
else 
{ 
ofs << read_c ; 
break ; 
} 
} 
} 
else if ( read_c == '/' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '/' ) 
{ 
ifs . get ( read_c ) ; 
while ( read_c != '\n' ) 
ifs . get ( read_c ) ; 
ifs . seekg ( - 1 , ios :: cur ) ; 
} 
else if ( read_c == '*' ) 
{ 
while ( true ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '*' ) 
{ 
ifs . get ( read_c ) ; 
if ( read_c == '/' ) 
{ 
ifs . get ( read_c ) ; 
break ; 
} 
} 
else if ( read_c == EOF ) 
break ; 
else 
continue ; 
} 
} 
else 
ofs << '/' ; 
} 
else 
ofs << read_c ; 
} 
return file_path ; 
} 
string del_indent ( string file_path ) 
{ 
ifstream ifs ; 
ifs . open ( file_path , ios :: in ) ; 
int pos = file_path . find ( '.' ) ; 
file_path . insert ( pos , "_del_indent" ) ; 
ofstream ofs ; 
ofs . open ( file_path , ios :: out ) ; 
string str_line ; 
while ( ! ifs . eof ( ) ) 
{ 
getline ( ifs , str_line ) ; 
string :: iterator pos_str = str_line . begin ( ) ; 
while ( pos_str != str_line . end ( ) ) 
{ 
if ( ( ( * pos_str ) != '\t' ) && ( ( * pos_str ) != ' ' ) ) 
break ; 
else 
pos_str = str_line . erase ( pos_str ) ; 
} 
if ( ( str_line . length ( ) == 0 ) || str_line == "\r" ) 
; 
else 
{ 
ofs << str_line << '\n' ; 
} 
} 
ifs . close ( ) ; 
ofs . close ( ) ; 
return file_path ; 
} 
string uncompress ( string file_path , map <string, unsigned char> map_ , unsigned char num = 0 ) 
{ 
string file_path_decode = file_path ; 
int pos = file_path_decode . find ( "encode" ) ; 
file_path_decode [ pos ] = 'd' ; 
file_path_decode [ pos + 1 ] = 'e' ; 
fstream ifs ( file_path , ios :: in | ios :: binary ) ; 
fstream ofs ( file_path_decode , ios :: out ) ; 
if ( ! ifs || ! ofs ) 
cerr << "open txt failure" << endl ; 
unsigned char i ; 
map <string, unsigned char> :: iterator it ; 
string word ; 
while ( ! ifs . eof ( ) && ifs . read ( ( char * ) & i , sizeof ( i ) ) ) 
{ 
for ( it = map_ . begin ( ) ; it != map_ . end ( ) ; it ++ ) 
{ 
if ( it -> second == i ) 
{ 
word = it -> first ; 
break ; 
} 
} 
if ( ( word == "IDENTIFIER" ) || ( word == "NUMBER" ) || ( word == "STRING" ) || ( word == "CHAR" ) ) 
{ 
int length ; 
unsigned char length_uc ; 
char word_c [ 50 ] ; 
ifs . read ( ( char * ) & length_uc , 1 ) ; 
length = int ( length_uc ) ; 
ifs . read ( ( char * ) word_c , length * sizeof ( char ) ) ; 
word_c [ length ] = '\0' ; 
ofs << word_c << " " ; 
} 
else if ( word == "\n" || word == "\r" || word == "\r\n" ) 
ofs << word ; 
else 
ofs << word << " " ; 
} 
ifs . close ( ) ; 
ofs . close ( ) ; 
return file_path_decode ; 
} 
void encode ( ) 
{ 
string keyword_arr [ ] = { "asm" , "else" , "new" , "this" , "bool" , "explicit" , "private" , "true" , "break" , 
"export" , "protected" , "try" , "case" , "extern" , "public" , "typedef" , "catch" , 
"false" , "register" , "typeid" , "char" , "float" , "reinterpret_cast" , "typename" , 
"class" , "for" , "return" , "union" , "const" , "friend" , "short" , "unsigned" , 
"const_cast" , "goto" , "signed" , "using" , "continue" , "if" , "sizeof" , "virtual" , 
"default" , "inline" , "static" , "void" , "delete" , "int" , "static_cast" , "volatile" , 
"do" , "long" , "struct" , "wchar_t" , "double" , "mutable" , "switch" , "while" , "dynamic_cast" , "namespace" , "template" , 
"#include" , "main" } ; 
for ( unsigned char i = 0 ; i < sizeof ( keyword_arr ) / sizeof ( keyword_arr [ 0 ] ) ; i ++ ) 
map_ [ keyword_arr [ i ] ] = num ++ ; 
string operator_arr [ ] = { 
"+" , "-" , "*" , "/" , "%" , "++" , "--" , 
"==" , "!=" , ">" , "<" , ">=" , "<=" , 
"&&" , "||" , "!" , 
"&" , "|" , "^" , "~" , "<<" , ">>" , 
"=" , "+=" , "-=" , "*=" , "/=" , "%=" , "<<=" , ">>=" , "&=" , "^=" , "|=" , 
"." , "->" , 
";" , "," , 
":" , "::" , 
"\a" , "\b" , "\f" , "\n" , "\r" , "\t" , "\v" , "\\" , "\'" , "\?" , "\0" , 
"[" , "]" , "{" , "}" , "(" , ")" } ; 
for ( unsigned char i = 0 ; i < sizeof ( operator_arr ) / sizeof ( operator_arr [ 0 ] ) ; i ++ ) 
map_ [ operator_arr [ i ] ] = num ++ ; 
string my_arr [ ] = { "IDENTIFIER" , "NUMBER" , "STRING" , "CHAR" } ; 
for ( unsigned char i = 0 ; i < sizeof ( my_arr ) / sizeof ( my_arr [ 0 ] ) ; i ++ ) 
map_ [ my_arr [ i ] ] = num ++ ; 
} 
void CCompressDlg :: OnBnClickedCompressButton ( ) 
{ 
encode ( ) ; 
file_path = compress ( file_path , map_ , num ) ; 
} 
void CCompressDlg :: OnBnClickedUncompressButton ( ) 
{ 
file_path = uncompress ( file_path , map_ , num ) ; 
} 

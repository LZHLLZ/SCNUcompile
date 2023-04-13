
// CompressDlg.cpp: 实现文件
//

#include "pch.h"
#include "framework.h"
#include "Compress.h"
#include "CompressDlg.h"
#include "afxdialogex.h"
#include<iostream>
#include<string>
#include<map>
#include<fstream>
using namespace std;

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


void encode();
string uncompress(string file_path, map<string, unsigned char> map_, unsigned char num);
string compress(string file_path, map<string, unsigned char>& map_, unsigned char num);
string del_indent(string file_path);
string del_notes(string file_path);

map<string, unsigned char> map_;
unsigned char num = 0;
string file_path="test.cpp";

// 用于应用程序“关于”菜单项的 CAboutDlg 对话框

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_ABOUTBOX };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

// 实现
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialogEx(IDD_ABOUTBOX)
{
   
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);	
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()


// CCompressDlg 对话框



CCompressDlg::CCompressDlg(CWnd* pParent /*=nullptr*/)
	: CDialogEx(IDD_COMPRESS_DIALOG, pParent)
	, m_showcpp(_T(""))
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CCompressDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Text(pDX, IDC_COMPRESS_EDIT, m_showcpp);
}

BEGIN_MESSAGE_MAP(CCompressDlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_BROWSE_BUTTON, &CCompressDlg::OnBnClickedBrowseButton)
    ON_BN_CLICKED(IDC_COMPRESS_BUTTON, &CCompressDlg::OnBnClickedCompressButton)
    ON_BN_CLICKED(IDC_UNCOMPRESS_BUTTON, &CCompressDlg::OnBnClickedUncompressButton)
END_MESSAGE_MAP()


// CCompressDlg 消息处理程序

BOOL CCompressDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// 将“关于...”菜单项添加到系统菜单中。

	// IDM_ABOUTBOX 必须在系统命令范围内。
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != nullptr)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// 设置此对话框的图标。  当应用程序主窗口不是对话框时，框架将自动
	//  执行此操作
	SetIcon(m_hIcon, TRUE);			// 设置大图标
	SetIcon(m_hIcon, FALSE);		// 设置小图标

	// TODO: 在此添加额外的初始化代码

	return TRUE;  // 除非将焦点设置到控件，否则返回 TRUE
}

void CCompressDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// 如果向对话框添加最小化按钮，则需要下面的代码
//  来绘制该图标。  对于使用文档/视图模型的 MFC 应用程序，
//  这将由框架自动完成。

void CCompressDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // 用于绘制的设备上下文

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// 使图标在工作区矩形中居中
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// 绘制图标
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

//当用户拖动最小化窗口时系统调用此函数取得光标
//显示。
HCURSOR CCompressDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}


CString ConvertUTF8ToCString(std::string utf8str)
{
    /* 预转换，得到所需空间的大小 */
    int nLen = ::MultiByteToWideChar(CP_UTF8, NULL,
        utf8str.data(), utf8str.size(), NULL, 0);
    /* 转换为Unicode */
    std::wstring wbuffer;
    wbuffer.resize(nLen);
    ::MultiByteToWideChar(CP_UTF8, NULL, utf8str.data(), utf8str.size(),
        (LPWSTR)(wbuffer.data()), wbuffer.length());

#ifdef UNICODE
    return(CString(wbuffer.data(), wbuffer.length()));
#else
    /*
     * 转换为ANSI
     * 得到转换后长度
     */
    nLen = WideCharToMultiByte(CP_ACP, 0,
        wbuffer.data(), wbuffer.length(), NULL, 0, NULL, NULL);

    std::string ansistr;
    ansistr.resize(nLen);

    /* 把unicode转成ansi */
    WideCharToMultiByte(CP_ACP, 0, (LPWSTR)(wbuffer.data()), wbuffer.length(),
        (LPSTR)(ansistr.data()), ansistr.size(), NULL, NULL);
    return(CString(ansistr.data(), ansistr.length()));
#endif
}

void CCompressDlg::OnBnClickedBrowseButton()
{
	// TODO: 在此添加控件通知处理程序代码
	
	UpdateData(TRUE);//将控件中的数据更新到相应的变量

	////开始从文件读取数据
	//CStdioFile file_read;
	//file_read.Open(_T("test.cpp"), CFile::modeCreate | CFile::modeNoTruncate | CFile::typeText | CFile::modeRead);
	//CString read_str;
	//
	//while (file_read.ReadString(read_str)) {
	//	m_showcpp += read_str;
	//	m_showcpp += "\r\n";
	//}
    ifstream ifs("test.cpp", ios::in);
    string str1;
    string read_str;
    while (!ifs.eof()) {
        getline(ifs, read_str);
        str1 += read_str;
        str1 += "\r\n";
    }
    m_showcpp = ConvertUTF8ToCString(str1);
    
	UpdateData(FALSE);
}





string compress(string file_path, map<string, unsigned char>& map_, unsigned char num = 0) {

    //生成压缩文件名
    string file_path_encode = file_path;
    int pos = file_path_encode.find(".");
    file_path_encode.insert(pos, "_encode");

    file_path = del_notes(file_path);//删除注释
    string file_path_del = del_indent(file_path);//删除缩进和空行

    ifstream ifs;
    ifs.open(file_path_del, ios::in);
    ofstream ofs;
    ofs.open(file_path_encode, ios::out | ios::binary);
    char read_c;
    while (!ifs.eof() && ifs.get(read_c)) //判断是否读到文件末尾、读取一个字符，存储到read_c
    {
        // ifs.get(read_c);
        //主控代码，不使用switch-case 使用if-else分支
        // switch (ch)
        // {
        // case 字母:
        // case 数字:
        // case '[':
        // case '=':
        // case '] ':
        // case '+':
        //     …
        // }

        //判断一个字符是否为字母或者_
        if (isalpha(read_c) || read_c == '_')
        {
            //如果是字母或者_的话，有可能是关键字或者标识符
            //关键字：已经存储在程序中，直接找到对应的编号，将编号写入文件
            //标识符：以字符串的形式直接写入文件
            // fstream ifs("word.txt", ios::in);
            // fstream ofs("word_encode.txt", ios::out | ios::binary);

            // if (!ifs || !ofs)
            //     cerr << "open txt failure" << endl;
            int length = 0;
            char word[20];
            word[length++] = read_c;
            while (true)
            {
                ifs.get(read_c);
                //如果不是字母、不是数字、不是下划线则break
                if ((!isalpha(read_c)) && (!isalnum(read_c)) && (read_c != '_'))
                    break;
                else
                    word[length++] = read_c;
            }
            word[length] = '\0';
            string word_str = word;
            string read_str = string(1, read_c); //将char数据类型转换为string类型
            //如果该单词是C++的关键字，直接将编码写入到文件中
            if (map_.find(word_str) != map_.end())
                ofs.write((char*)&(map_[word_str]), sizeof(map_[word_str]));
            //如果是标识符，，然后再以二进制写入标识符
            else
            {
                //先写入IDENTIFIER对应的编码
                ofs.write((char*)&map_["IDENTIFIER"], sizeof(map_["IDENTIFIER"]));
                //然后写入数字的总长度:length
                unsigned char length_uc = length;
                ofs.write((char*)&length_uc, 1);
                //最后将标识符以二进制的形式写入到文件，写入的大小为标识符的长度
                ofs.write((char*)word, length * sizeof(char));
            }
            // //最后将读多余的字符写入
            // ofs.write((char *)&(map_[read_str]), sizeof(map_[read_str]));

            ifs.seekg(-1, ios::cur); //将文件指针前移一字节
        }
        //该函数用于判断一个字符是否为数字或字母
        //由于字母已经在上面筛选过了，所以这里只会筛选数字
        else if (isalnum(read_c))
        {
            int length = 0;
            char word[20];
            word[length++] = read_c;
            while (ifs.get(read_c))
            {
                //如果不是数字、不是字母、不是'.'、不是‘-’则break
                if ((!isalnum(read_c)) && (!isalpha(read_c)) && (read_c != '.') && (read_c != '-'))
                    break;
                else
                    word[length++] = read_c;
            }

            string read_str = string(1, read_c);

            //先写入NUMBER对应的编码
            ofs.write((char*)&map_["NUMBER"], sizeof(map_["NUMBER"]));
            //然后写入数字的总长度:length
            unsigned char length_uc = length;
            ofs.write((char*)&length_uc, 1);
            //最后将数字以二进制的形式写入到文件，写入的大小为数字的长度
            ofs.write((char*)word, length * (sizeof(char)));
            //将文件指针前移一字节
            ifs.seekg(-1, ios::cur);
        }
        //"+" "++" "+="
        else if (read_c == '+')
        {
            ifs.get(read_c);
            if (read_c == '+')
                ofs.write((char*)&map_["++"], 1);
            else if (read_c == '=')
                ofs.write((char*)&map_["+="], 1);
            else
            {
                ofs.write((char*)&map_["+"], 1);
                ifs.seekg(-1, ios::cur);
            }
        }
        //"-" "--" "-=" "->"
        else if (read_c == '-')
        {
            ifs.get(read_c);
            if (read_c == '-')
                ofs.write((char*)&map_["--"], 1);
            else if (read_c == '=')
                ofs.write((char*)&map_["-="], 1);
            else if (read_c == '>')
                ofs.write((char*)&map_["->"], 1);
            else
            {
                ofs.write((char*)&map_["-"], 1);
                ifs.seekg(-1, ios::cur);
            }
        }
        //"*" "*=" 指针&解引用
        else if (read_c == '*')
        {
            ifs.get(read_c);
            if (read_c == '=')
                ofs.write((char*)&map_["*="], 1);
            else
            {
                ofs.write((char*)&map_["*"], 1);
                ifs.seekg(-1, ios::cur);
            }
        }
        //"%" "%="
        else if (read_c == '%')
        {
            ifs.get(read_c);
            if (read_c == '=')
                ofs.write((char*)&map_["%="], 1);
            else
            {
                ofs.write((char*)&map_["%"], 1);
                ifs.seekg(-1, ios::cur);
            }
        }
        //"==" "="
        else if (read_c == '=')
        {
            ifs.get(read_c);
            if (read_c == '=')
                ofs.write((char*)&map_["=="], 1);
            else
            {
                ofs.write((char*)&map_["="], 1);
                ifs.seekg(-1, ios::cur);
            }
        }
        //"/" "/=" "//" "/*"
        else if (read_c == '/')
        {
            /*
            1、"/"：除法运算符
            2、"/="：除等于运算符
            */
            ifs.get(read_c);
            if (read_c == '=')
                ofs.write((char*)&map_["/="], 1);
            else
            {
                ofs.write((char*)&map_["/"], 1);
                ifs.seekg(-1, ios::cur);
            }
        }
        //"&" "&&" "&="
        else if (read_c == '&')
        {
            ifs.get(read_c);
            if (read_c == '&')
                ofs.write((char*)&map_["&&"], 1);
            else if (read_c == '=')
                ofs.write((char*)&map_["&="], 1);
            else
            {
                ofs.write((char*)&map_["&"], 1);
                ifs.seekg(-1, ios::cur);
            }
        }
        //"|" "||" "|="
        else if (read_c == '|')
        {
            ifs.get(read_c);
            if (read_c == '|')
                ofs.write((char*)&map_["||"], 1);
            else if (read_c == '=')
                ofs.write((char*)&map_["|="], 1);
            else
            {
                ofs.write((char*)&map_["|"], 1);
                ifs.seekg(-1, ios::cur);
            }
        }
        //"!" "!="
        else if (read_c == '!')
        {
            ifs.get(read_c);
            if (read_c == '=')
                ofs.write((char*)&map_["!="], 1);
            else
            {
                ofs.write((char*)&map_["!"], 1);
                ifs.seekg(-1, ios::cur);
            }
        }
        //"^" "^="
        else if (read_c == '^')
        {
            ifs.get(read_c);
            if (read_c == '=')
                ofs.write((char*)&map_["^="], 1);
            else
            {
                ofs.write((char*)&map_["^"], 1);
            }
        }
        //"<" "<<" "<<=" "<="
        else if (read_c == '<')
        {
            ifs.get(read_c);
            if (read_c == '<')
            {
                ifs.get(read_c);
                if (read_c == '=')
                    ofs.write((char*)&map_["<<="], 1);
                else
                {
                    ofs.write((char*)&map_["<<"], 1);
                    ifs.seekg(-1, ios::cur);
                }
            }
            else if (read_c == '=')
                ofs.write((char*)&map_["<="], 1);
            else if (isalpha(read_c))
            {
                int length = 0;
                char word[50];
                word[length++] = '<';
                word[length++] = read_c;
                while (ifs.get(read_c))
                {
                    word[length++] = read_c;
                    if (read_c == '>')
                        break;
                }
                unsigned char length_uc = length;
                ofs.write((char*)&map_["STRING"], 1);
                ofs.write((char*)&length_uc, 1);
                ofs.write((char*)word, length * sizeof(char));
            }
            else
            {
                ofs.write((char*)&map_["<"], 1);
                ifs.seekg(-1, ios::cur);
            }
        }
        //">" ">>" ">>=" ">="
        else if (read_c == '>')
        {
            ifs.get(read_c);
            if (read_c == '>')
            {
                ifs.get(read_c);
                if (read_c == '=')
                    ofs.write((char*)&map_[">>="], 1);
                else
                {
                    ofs.write((char*)&map_[">>"], 1);
                    ifs.seekg(-1, ios::cur);
                }
            }
            else if (read_c == '=')
            {
                ofs.write((char*)&map_[">="], 1);
            }
            else
            {
                ofs.write((char*)&map_[">"], 1);
                ifs.seekg(-1, ios::cur);
            }
        }
        //" 说明是字符串
        else if (read_c == '\"')
        {
            int length = 0;
            char word[50];
            word[length++] = read_c;
            while (ifs.get(read_c))
            {
                word[length++] = read_c;
                //读到"，说明字符串已经结束
                if (read_c == '\"')
                    break;
            }
            word[length++] = '\0';
            unsigned char length_uc = length;
            ofs.write((char*)&map_["STRING"], 1);
            ofs.write((char*)&length_uc, 1);
            ofs.write((char*)word, length * sizeof(char));
        }
        //' 说明是字符
        else if (read_c == '\'')
        {
            int length = 0;
            char word[6];
            word[length++] = read_c;
            while (ifs.get(read_c))
            {
                //反斜杠对应的转义字符是92
                if (int(read_c) == 92)
                {
                    word[length++] = read_c;
                    ifs.get(read_c);
                    word[length++] = read_c;
                }
                else if (read_c == '\'')
                {
                    word[length++] = read_c;
                    break;
                }
                else
                    word[length++] = read_c;
            }
            unsigned char length_uc = length;
            ofs.write((char*)&map_["CHAR"], 1);
            ofs.write((char*)&length_uc, 1);
            ofs.write((char*)word, length * sizeof(char));
        }
        else if (read_c == ' ')
            continue;
        // else if (read_c == '#')
        // {
        //     while (ifs.get(read_c))
        //     {
        //         if (read_c == ' ')
        //             break;
        //     }
        //     ofs.write((char *)&map_["#include"], 1);
        //     int length = 0;
        //     char word[20];
        //     while (ifs.get(read_c))
        //     {
        //         if (read_c == '\r' || read_c == '\n')
        //             break;
        //         else
        //             word[length++] = read_c;
        //     }
        //     //先写入IDENTIFIER对应的编码
        //     ofs.write((char *)&map_["IDENTIFIER"], 1);
        //     //然后写入数字的总长度:length
        //     unsigned char length_uc = length;
        //     ofs.write((char *)&length_uc, 1);
        //     //最后将数字以二进制的形式写入到文件，写入的大小为数字的长度
        //     ofs.write((char *)word, length * (sizeof(char)));
        //     //将文件指针前移一字节
        //     ifs.seekg(-1, ios::cur);
        // }

        //不压缩
        else if (read_c == '#')
        {
            int length = 0;
            char word[30];
            word[length++] = '#';
            while (ifs.get(read_c))
            {
                if (read_c == '\r' || read_c == '\n')
                    break;
                else
                    word[length++] = read_c;
            }
            //先写入IDENTIFIER对应的编码
            ofs.write((char*)&map_["IDENTIFIER"], 1);
            //然后写入数字的总长度:length
            unsigned char length_uc = length;
            ofs.write((char*)&length_uc, 1);
            //最后将数字以二进制的形式写入到文件，写入的大小为数字的长度
            ofs.write((char*)word, length * (sizeof(char)));
            //将文件指针前移一字节
            ifs.seekg(-1, ios::cur);
        }
        else if (read_c == ':')
        {
            ifs.get(read_c);
            if (read_c == ':')
                ofs.write((char*)&map_["::"], 1);
            else
            {
                ofs.write((char*)&map_[":"], 1);
                ifs.seekg(-1, ios::cur);
            }
        }
        else
        {
            string read_str = string(1, read_c);
            ofs.write((char*)&map_[read_str], 1);
        }
    }
    ifs.close();
    ofs.close();
    remove(file_path.c_str());
    remove(file_path_del.c_str());
    return file_path_encode;
}

string del_notes(string file_path)
{
    ifstream ifs;
    ifs.open(file_path, ios::in);
    int pos = file_path.find('.');
    file_path.insert(pos, "_del_notes");
    ofstream ofs;
    ofs.open(file_path, ios::out);
    char read_c;
    while (!ifs.eof() && ifs.get(read_c))
    {
        if (read_c == '\'')
        {
            ofs << read_c;
            while (ifs.get(read_c))
            {
                if (int(read_c) == 92) {
                    ofs << read_c;
                    ifs.get(read_c);
                    ofs << read_c;
                }
                else if (read_c != '\'')
                    ofs << read_c;
                else
                {
                    ofs << read_c;
                    break;
                }
            }
        }
        else if (read_c == '\"')
        {
            ofs << read_c;
            while (ifs.get(read_c))
            {
                if (read_c != '\"')
                    ofs << read_c;
                else
                {
                    ofs << read_c;
                    break;
                }
            }
        }
        else if (read_c == '/')
        {

            ifs.get(read_c);
            // 1、"//：行注释
            if (read_c == '/')
            {
                ifs.get(read_c);
                //把该行的注释全部读入
                while (read_c != '\n')
                    ifs.get(read_c);
                ifs.seekg(-1, ios::cur);
            }
            // 2、"/*...."：块注释
            else if (read_c == '*')
            {
                while (true)
                {
                    ifs.get(read_c);
                    if (read_c == '*')
                    {
                        ifs.get(read_c);
                        if (read_c == '/')
                        {
                            ifs.get(read_c); //  读到/后 要把紧接的"\r\n"也读掉
                            // ifs.get(read_c);
                            break;
                        }
                    }
                    //读取到文件尾
                    else if (read_c == EOF)
                        break;
                    //如果既没有读到文件末尾，也没有读到*，则继续读
                    else
                        continue;
                }
            }
            else
                ofs << '/';
        }
        else
            ofs << read_c;
    }
    return file_path;
}
string del_indent(string file_path)
{
    ifstream ifs;
    ifs.open(file_path, ios::in);
    int pos = file_path.find('.');
    file_path.insert(pos, "_del_indent");
    ofstream ofs;
    ofs.open(file_path, ios::out);
    string str_line;
    while (!ifs.eof())
    {
        getline(ifs, str_line);
        string::iterator pos_str = str_line.begin();

        //删除缩进
        while (pos_str != str_line.end()) //从头开始遍历字符串
        {
            //循环结束的条件是：开头的空格和'\t'全部被删除了
            if (((*pos_str) != '\t') && ((*pos_str) != ' '))
                break;
            else
                pos_str = str_line.erase(pos_str);
        }

        //删除空行
        if ((str_line.length() == 0) || str_line == "\r") //空行则删除，不必写入到文件中
            ;
        else
        {
            //如果不是空行，则将整行写入到文件中，但是要补上'\n'，因为getline()不会将'\n'读入
            ofs << str_line << '\n';
        }
    }
    ifs.close();
    ofs.close();
    return file_path;
}

string uncompress(string file_path, map<string, unsigned char> map_, unsigned char num = 0)
{
    //生成压缩文件名
    string file_path_decode = file_path;
    int pos = file_path_decode.find("encode");
    file_path_decode[pos] = 'd';
    file_path_decode[pos + 1] = 'e';

    fstream ifs(file_path, ios::in | ios::binary);
    fstream ofs(file_path_decode, ios::out);
    if (!ifs || !ofs)
        cerr << "open txt failure" << endl;

    unsigned char i;
    map<string, unsigned char>::iterator it;
    string word;
    while (!ifs.eof() && ifs.read((char*)&i, sizeof(i)))
    {
        for (it = map_.begin(); it != map_.end(); it++)
        {
            if (it->second == i)
            {
                word = it->first;
                break;
            }
        }
        if ((word == "IDENTIFIER") || (word == "NUMBER") || (word == "STRING") || (word == "CHAR"))
        {
            int length;
            unsigned char length_uc;
            char word_c[50];
            ifs.read((char*)&length_uc, 1);
            length = int(length_uc);
            ifs.read((char*)word_c, length * sizeof(char));
            word_c[length] = '\0';
            ofs << word_c << " ";
        }
        else if (word == "\n" || word == "\r" || word == "\r\n")
            ofs << word;
        else
            ofs << word << " ";
    }
    ifs.close();
    ofs.close();
    return file_path_decode;
}

void encode()
{
    // C++关键字
    string keyword_arr[] = { "asm", "else", "new", "this", "bool", "explicit", "private", "true", "break",
                            "export", "protected", "try", "case", "extern", "public", "typedef", "catch",
                            "false", "register", "typeid", "char", "float", "reinterpret_cast", "typename",
                            "class", "for", "return", "union", "const", "friend", "short", "unsigned",
                            "const_cast", "goto", "signed", "using", "continue", "if", "sizeof", "virtual",
                            "default", "inline", "static", "void", "delete", "int", "static_cast", "volatile",
                            "do", "long", "struct", "wchar_t", "double", "mutable", "switch", "while", "dynamic_cast", "namespace", "template",
                            "#include", "main" };

    for (unsigned char i = 0; i < sizeof(keyword_arr) / sizeof(keyword_arr[0]); i++)
        map_[keyword_arr[i]] = num++;
    // C++标识符：以_或者字母开头，后面可以接_或字母或数字
    //例如：_temp2 _arr_2 __abd

    /*C++运算符
        算术运算符：+  -  *  /  %  ++  --
        关系运算符：==  ！=  >  <  >=  <=
        逻辑运算符：&&  ||  !
        位运算符：&  |  ^  ~  <<  >>
        赋值运算符：=  +=  -=  *=  /=  %=  <<=  >>=  &=  ^=  |=
        杂项运算符： sizeof（在关键字中已存在） .（用于引用类、结构体的成员）  ->（用于引用类、结构体的成员） &  *（这两个已经在上面有了）
        []
    */

    //已处理：+ - * / = % & | ! ^

    string operator_arr[] = {
        "+", "-", "*", "/", "%", "++", "--",
        "==", "!=", ">", "<", ">=", "<=",
        "&&", "||", "!",
        "&", "|", "^", "~", "<<", ">>",
        "=", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "^=", "|=",
        ".", "->",
        ";", ",",
        ":", "::",
        "\a", "\b", "\f", "\n", "\r", "\t", "\v", "\\", "\'", "\?", "\0",
        "[", "]", "{", "}", "(", ")" };
    for (unsigned char i = 0; i < sizeof(operator_arr) / sizeof(operator_arr[0]); i++)
        map_[operator_arr[i]] = num++;

    /*
        自定义：1、标识符：IDENTIFIER，如果需要存储标识符比方说 string read_str中的 read_str，
        则写入 7"read_str"，假设IDENTIFIER对应的编码为7
    */
    string my_arr[] = { "IDENTIFIER", "NUMBER", "STRING", "CHAR" };
    for (unsigned char i = 0; i < sizeof(my_arr) / sizeof(my_arr[0]); i++)
        map_[my_arr[i]] = num++;
}

void CCompressDlg::OnBnClickedCompressButton()
{
    // TODO: 在此添加控件通知处理程序代码
    encode();
    file_path=compress(file_path,map_, num);
}



void CCompressDlg::OnBnClickedUncompressButton()
{
    // TODO: 在此添加控件通知处理程序代码
    file_path=uncompress(file_path,map_, num);
}

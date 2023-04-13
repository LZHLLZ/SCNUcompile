
// CompressDlg.h: 头文件
//

#pragma once


// CCompressDlg 对话框
class CCompressDlg : public CDialogEx
{
// 构造
public:
	CCompressDlg(CWnd* pParent = nullptr);	// 标准构造函数

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_COMPRESS_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 支持


// 实现
protected:
	HICON m_hIcon;

	// 生成的消息映射函数
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	CString m_showcpp;
	afx_msg void OnBnClickedBrowseButton();
	afx_msg void OnBnClickedCompressButton();
	afx_msg void OnBnClickedButton2();
	afx_msg void OnBnClickedUncompressButton();
	afx_msg void OnEnChangeEdit1();
	CString m_file_path;
	afx_msg void OnBnClickedOpenButton();
	afx_msg void OnEnChangeOpenEdit();
	afx_msg void OnBnClickedCancel();
private:
	CFont cfont1;
	CFont cfont2;
	CFont cfont3;
public:
	CString M_OPEN_EDIT;
	afx_msg void OnEnChangeCompressEdit();
};

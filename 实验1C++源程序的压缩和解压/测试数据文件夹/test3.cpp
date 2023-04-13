#pragma once
#include "E:\code\C++\Data structure experiment\Ex3\minHeap.h"
#include <algorithm>
#include <iostream>
#include <fstream>
#include <iomanip>
using namespace std;
struct HuffManNode
{
    int weight;
    int parent, lch, rch;
    HuffManNode(int weight)
    {
        this->weight = weight;
        this->parent = this->lch = this->rch = 0;
    }
    HuffManNode()
    {
        this->weight = 0;
        this->parent = this->lch = this->rch = 0;
    }
};

struct char_num
{
    char c;
    int num;
    char_num()
    {
        this->num = 0;
    }
};
struct HuffManCode
{
    char c;
    string code;
    HuffManCode()
    {
        this->code = "";
    }
};

template <typename T>
class HuffmanTree
{
public:
    //默认构造函数，调用构造哈夫曼树函数
    HuffmanTree()
    {
        // //如果文件中已经有构造好的哈夫曼树和编码则直接读入
        // if (this->readHfmTree() == true)
        //     cout << "读取HfmTree.txt文件初始化成功！" << endl;
        // //否则从终端输入，重新建立
        // else
        // {
        //     cout << "请输入字符集的大小" << endl;
        //     cin >> num;
        //     this->CreateHuffmanTree(num);
        // }
    }
    void Initialization()
    {
        //如果文件中已经有构造好的哈夫曼树和编码则直接读入
        if (this->readHfmTree() == true)
            cout << "读取HfmTree.txt文件初始化成功！" << endl;
        //否则从终端输入，重新建立
        else
        {
            cout << "请输入字符集的大小" << endl;
            cin >> num;
            this->CreateHuffmanTree(num);
        }
    }

    //构造哈夫曼树
    void CreateHuffmanTree(int n)
    {
        if (n <= 1)
            return;
        else
        {
            minHeap<HuffManNode> hp(n);
            HuffManNode first, second;               //声明两个哈夫曼节点用来接收堆中的两个最小节点
            this->arr_node = new HuffManNode[2 * n]; //分配空间，实际使用的长度为1-2*n-1,调用默认构造函数，将节点中的数据全部置为0
            this->arr_code = new HuffManCode[n + 1];
            cout << "请输入n个字符及其对应的权值：";
            getchar();
            for (int i = 1; i <= n; i++)
            {
                arr_code[i].c = getchar(); //输入n个字符
                getchar();
                // cin >> arr_code[i].c;      //输入n个字符
                cin >> arr_node[i].weight; //输入前n个元素（叶子节点）的weight值
                arr_node[i].parent = i * -1;
                getchar();
                cout << arr_code[i].c << " " << arr_node[i].weight << endl;
                hp.insert(arr_node[i]); //最小堆的建立
            }
            int i;
            for (i = n + 1; i <= 2 * n - 1; i++)
            {
                hp.remove(first);
                hp.remove(second);
                int s1 = 1, s2 = 1;
                //在已有的哈夫曼节点中搜索与first、second相同的节点，并记录其对应的下标
                for (int j = 1; j <= i - 1; j++)
                {
                    if (arr_node[j].weight == first.weight && arr_node[j].lch == first.lch && arr_node[j].rch == first.rch && arr_node[j].parent == first.parent)
                        s1 = j;
                    if (arr_node[j].weight == second.weight && arr_node[j].lch == second.lch && arr_node[j].rch == second.rch && arr_node[j].parent == second.parent)
                        s2 = j;
                }
                arr_node[i].weight = first.weight + second.weight;
                arr_node[s1].parent = arr_node[s2].parent = i;
                arr_node[i].lch = s1;
                arr_node[i].rch = s2;
                hp.insert(arr_node[i]);
            }
            this->root = i - 1;
            arr_node[root].parent = 0;
        }
    }


    //对字符开始编码，思路：从叶子节点往父节点循环遍历，若为父节点的左孩子则字符串+0，反之+1
    //直到父节点为0时，说明已经遍历到根节点了，编码结束。然后将字符串做一次反转
    void CreateHuffManCode()
    {
        string temp;
        int father;
        int current;
        for (int i = 1; i <= num; i++)
        {
            temp = "";
            current = i;
            father = arr_node[i].parent;
            //判断是否遍历至根节点
            while (father != 0)
            {
                //如果为左孩子，则+0
                if (arr_node[father].lch == current)
                    temp += '0';
                //如果为左孩子，则+1
                else
                    temp += '1';
                //向上遍历
                current = father;
                father = arr_node[current].parent;
            }
            //反转字符串
            reverse(temp.begin(), temp.end());
            arr_code[i].code = temp;
        }
        //将编码完的结果写入到文件HfmTree.txt中
        this->saveHfmTree();
    }

    //打印创建好的哈夫曼编码
    void printCode()
    {
        for (int i = 1; i <= num; i++)
        {
            cout << arr_code[i].c << " 编码为：" << arr_code[i].code << endl;
        }
    }

    //将ToBeTran.txt的英语文章按照已经创建好的哈夫曼进行编码并存储到CodeFile.txt
    bool encodefile()
    {
        ifstream ifs(this->ToBeTran, ios::in);
        ofstream ofs(this->CodeFile, ios::out);
        //将所有01写入到CodeFile.txt
        if (!ifs.is_open())
        {
            cout << "ToBeTran.txt打开失败！" << endl;
            return false;
        }
        if ( !ofs.is_open())
        {
            cout << "CodeFile.txt打开失败！" << endl;
            return false;
        }
        else
        {
            char c;
            while ((c = ifs.get()) != EOF)
            {
                for (int i = 1; i <= this->num; i++)
                {
                    if (c == arr_code[i].c)
                    {
                        ofs << arr_code[i].code;
                        break;
                    }
                }
            }
            ifs.close();
            ofs.close();
            cout << "已将正文ToBeTran.txt中的内容编码并存入到CodeFile.txt中" << endl;
            return true;
        }
    }
    //将CodeFile.txt中的二进制代码以每行50个01代码输出到终端，同时存储到CodePrin.txt中
    void print()
    {
        ifstream ifs(this->CodeFile, ios::in);
        ofstream ofs(this->CodePrin, ios::out);
        int num = 0;
        //然后读取01每50个01换一次行
        char c;
        while ((c = ifs.get()) != EOF)
        {
            num++;
            ofs << c;
            cout << c;
            if (num == 50)
            {
                cout << endl;
                ofs << endl;
                num = 0;
            }
        }
        ifs.close();
        ofs.close();
        cout<<endl;
        cout << "已写入到CodePrin.txt" << endl;
    }
    //读取CodeFile.txt中的存放的01，然后译码为字符写入到TextFile.txt
    bool decodefile()
    {
        ifstream ifs(this->CodeFile, ios::in);
        ofstream ofs(this->TextFile, ios::out);
        if (!ifs.is_open() || !ofs.is_open())
        {
            cout << "文件打开失败！" << endl;
            return false;
        }
        else
        {
            char c;
            int pos = this->root;
            while (ifs >> c)
            {
                //遇到0走左子树
                if (c == '0')
                {
                    pos = this->arr_node[pos].lch;
                }
                //遇到1走右子树
                else
                    pos = this->arr_node[pos].rch;
                //遇到叶子节点，则输出字符
                if (arr_node[pos].lch == 0)
                {
                    ofs << arr_code[pos].c;
                    pos = this->root;
                }
            }
        }
        ifs.close();
        ofs.close();
        cout << "已将CodeFile.txt中的编码译码并存入到TextFile.txt" << endl;
        return true;
    }

    void printTree()
    {
        int level = 0;
        this->printTree(this->root, level);
    }
    void printTree(int p, int level)
    {
        if (p == 0)
            return;
        else
        {

            this->printTree(arr_node[p].rch, ++level);
            for (int i = 0; i < level; i++)
            {
                printf("   ");
            }
            cout << arr_node[p].weight << endl;
            this->printTree(arr_node[p].lch, ++level);
        }
    }

    //统计文本中字符的总数，以及每个字符对应的频数
    //统计fileName中每个字符出现的频数，并写入到data.txt文件中
    bool articleChar(string fileName)
    {
        ifstream ifs(fileName, ios::in);
        if (!ifs.is_open())
        {
            cout << "文件打开失败！" << endl;
            return false;
        }
        int amount = 0;//出现不同字符的数目
        char c;
        char_num *arr = new char_num[100];//因为英语文章中可能出现的字符不会从超过100，所以开辟长度位100的数组足够
        while ((c = ifs.get()) != EOF) //一个字符一个字符的读取，且判断是否读到文件末尾
        {
            cout << c; //在终端中输出读取到的字符
            int i;
            //循环遍历，看是否该字符已被加入到数组中
            for (i = 0; i < amount; i++)
            {
                if (arr[i].c == c)
                    break;
            }
            if (arr[i].c == c)
                arr[i].num++;//频数加1
            else
            {
                amount++;//字符的数目加1
                arr[i].c = c;//将新的字符加入到字符数组中
                arr[i].num++;//频数加1
            }
        }
        string name = "data.txt";
        ofstream ofs(name, ios::out);
        ofs << amount << endl;
        //将字符的数目，以及每个字符及其对应的频数写入到data.txt
        for (int i = 0; i < amount; i++)
        {
            ofs << arr[i].c << " " << arr[i].num << endl;
        }
        ifs.close();
        ofs.close();
        return true;
    }

    void Menu()
    {
        cout << "欢迎使用文本压缩与解压系统" << endl;
        cout << "1、初始化（Initialization）" << endl;
        cout << "2、编码（Encoding）" << endl;
        cout << "3、译码（Decoding）" << endl;
        cout << "4、打印代码文件（Print）" << endl;
        cout << "5、打印哈夫曼树（TreePrinting）" << endl;
    }
    void run()
    {
        int choice = 0;
        while (true)
        {
            this->Menu();
            cout << "请输入选择：";
            cin >> choice;
            switch (choice)
            {
            case 1:
                this->Initialization();
                this->CreateHuffManCode();
                system("pause");
                system("cls");
                break;
            case 2:
                this->encodefile();
                system("pause");
                system("cls");
                break;
            case 3:
                this->decodefile();
                system("pause");
                system("cls");
                break;
            case 4:
                this->print();
                system("pause");
                system("cls");
                break;
            default:
                break;
            }
        }
    }

private:
    HuffManNode *arr_node;
    HuffManCode *arr_code;
    string hfmTree = "HfmTree.txt";
    string ToBeTran = "ToBeTran.txt";
    string CodeFile = "CodeFile.txt";
    string TextFile = "TextFile.txt";
    string CodePrin = "CodePrin.txt";
    // string hfmTree = "E:\\code\\C++\\Data structure experiment\\Ex3\\HfmTree.txt";
    int root;
    int num;
    //将已经生成好的哈夫曼树和编码保存到文件HfmTree.txt中
    void saveHfmTree()
    {
        ofstream ofs(this->hfmTree, ios::out);
        if (!ofs.is_open())
        {
            cout << "文件打开失败！" << endl;
            return;
        }
        ofs << num << endl;
        for (int i = 1; i < 2 * num; i++)
            ofs << arr_node[i].weight << " " << arr_node[i].parent << " " << arr_node[i].lch << " " << arr_node[i].rch << endl;
        for (int i = 1; i <= num; i++)
            ofs << arr_code[i].c << " " << arr_code[i].code << endl;
        ofs.close();
    }
    //从文件HfmTree.txt中读入哈夫曼树和编码
    bool readHfmTree()
    {
        ifstream ifs(this->hfmTree, ios::in);
        if (!ifs.is_open())
            return false;
        ifs >> num;
        if (this->num == 0)
            return false;
        this->arr_node = new HuffManNode[2 * num];
        this->arr_code = new HuffManCode[num + 1];
        for (int i = 1; i < 2 * num; i++)
            ifs >> arr_node[i].weight >> arr_node[i].parent >> arr_node[i].lch >> arr_node[i].rch;
        ifs.get();
        for (int i = 1; i <= num; i++)
        {
            arr_code[i].c = ifs.get();
            ifs >> arr_code[i].code;
            ifs.get();
        }
        this->root = 2 * num - 1;
        ifs.close();
        return true;
    }
};

bool operator<(HuffManNode &h1, HuffManNode &h2)
{
    return h1.weight < h2.weight;
}

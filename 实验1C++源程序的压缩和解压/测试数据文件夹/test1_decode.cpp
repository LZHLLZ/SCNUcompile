#include<iostream> 
using namespace std ; 
int main ( ) { 
int num1 = 0 ; 
int num2 = 0x1b2 ; 
int num3 = 0Xabc ; 
int num4 = 0.344e-4 ; 
string keyword_arr [ ] = { asm , else , new , this , bool , explicit , private , true , break , 
export , protected , try , case , extern , public , typedef , catch , 
false , register , typeid , char , float , reinterpret_cast , typename , 
class , for , return , union , const , friend , short , unsigned , 
const_cast , goto , signed , using , continue , if , sizeof , virtual , 
default , inline , static , void , delete , int , static_cast , volatile , 
do , long , struct , wchar_t , double , mutable , switch , while , dynamic_cast , namespace , template , 
#include, main }; 
string operator_arr [ ] = { 
+ , - , * , / % , ++ , -- , 
== , != , > , < , >= , <= , 
&& , || , ! , 
& , | , ^ , ~ , << , >> , 
= , += , -= , *= , / , &= , <<= , >>= , &= , ^= , |= , 
. , -> , 
; , , , 
: , :: , 
[ , ] , { , } , ( , ) } ; 
return 0 ; 
} 

#include <iostream>
#include <fstream>
#include <cstring>

using namespace std;

bool check(string Word);

int main()
{

    ofstream outFile;
    outFile.open("D:\\list.txt");

    string Word;
    char word_u_want_start_with;
    int len_of_word, got = 0;
    
    cout << "Chu cai bat dau: ";
    cin >> word_u_want_start_with;
    cout << "Nhap do dai mong muon: ";
    cin >> len_of_word;

    freopen("dictionary.inp","r",stdin);
    
    while(getline(cin, Word))
    {
        if(check(Word))
        if(Word[0] == word_u_want_start_with)
        if((int)Word.length() == len_of_word)
            outFile << Word << '\n',
            got ++;
        if(got==45)
            break;
    }
    outFile.close();
    cout << "Done!";
    return 0;
}

bool check(string Word)
{
    for(int i = 0; i < (int)Word.length(); i++)
    {
        if( Word[i] > 'z' || Word[i] < 'a' ) 
            return false;
    }
    return true;
}
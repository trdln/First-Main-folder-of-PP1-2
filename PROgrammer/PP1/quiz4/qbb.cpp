#include <bits/stdc++.h>
using namespace std;
int main(){
    string word;
    cin>>word;
    for(int i=0;i<word.size();++i){
        word[i]='a'+'z'-word[i];
    }
    cout<<word;
}
#include <iostream>
#include <climits>

using namespace std;

int main(){

    int n, m;
    cin >> n >> m;

    int a[n][m];

    for(int i = 0; i < n; ++i){
        for(int j = 0; j < m; ++j){
            a[i][j]=i*j;
            cout<<a[i][j]<<" ";
        }
        cout<< endl;
    }





return 0;
}
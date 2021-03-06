#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <algorithm>
#include <functional>
#include <vector>
#include <queue>
#include <stack>
#include <map>
#include <set>
#include <deque>
#include <string>
#include <cassert>

using namespace std;

typedef long long llint;

const int INF = 0x3f3f3f3f;
const llint INFLL = 0x3f3f3f3f3f3f3f3fLL;

void print() { cout << "\n"; }

template <typename...T, typename X>
void print(X&& x, T... args) { cout << x << " "; print(args...); }

int input() { return 0; }

template <typename...T, typename X>
int input(X& x, T&... args) {
    if (!(cin >> x)) return 0;
    return input(args...) + 1;
}

int main() {
    int n;
    while (input(n)) {
        int a = -1;
        string b = "-1";
        char c = -1;
        float d = -1;
        
        assert(input(a, b, c, d) == n);
        print(a, b, c, d);
    }

    return 0;
}

/*

^^^TEST^^^
4
1 2 3 4
3
1 2 3
-----
1 2 3 4 
1 2 3 -1 
$$$TEST$$$

*/

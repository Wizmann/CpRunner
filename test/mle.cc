#include <cstdio>
#include <vector>

int main() {
    std::vector<int> ns;
    for (int i = 0; /* pass */; i++) {
        ns.push_back(i);
    }
    return 0;
}

/*
^^^TEST^^^
foo
---
bar
$$$TEST$$$
*/

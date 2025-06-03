#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;

    const int64_t NEG_INF = -1e15;
    vector<int64_t> dp(3, NEG_INF);
    dp[0] = dp[1] = dp[2] = NEG_INF;

    // Satisfaction lookup
    int s[3][3] = {
        {0, 2, 3},
        {4, 0, 5},
        {1, 6, 0}
    };

    for (int c : a) {
        vector<int64_t> new_dp = dp;
        if (new_dp[c] < 0) new_dp[c] = 0; // start subsequence here

        for (int prev = 0; prev < 3; prev++) {
            if (dp[prev] == NEG_INF) continue;
            int64_t val = dp[prev] + s[prev][c];
            if (val > new_dp[c]) new_dp[c] = val;
        }

        dp = move(new_dp);
    }

    cout << max({dp[0], dp[1], dp[2]}) << "\n";
    return 0;
}

# Elijah's Sequential CTF
This challenge provided mainly an instructional pdf file. This is a dynamic programming problem variation of maximum scoring subsequence with transitions. Mainly, we are:
- given a sequence of elements (of categories 0, 1, 2)
- allowed to choose any subsequence (i.e. keep or drop elements)
- the score increases only between 2 consecutive chosen elements, based on a transition rule between category pairs.
Our goal is to choose a subsequence that maximises total transition score.

Let's go through the code writing process step by step. Initially, when I tried to use python, it was simply too inefficient to bypass the remote judge's test cases. Therefore, we will proceed with C++.

### Step 1: Read input

```cpp
    int n; cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;
```
This reads integer `n` and a list `a` of size `n`.

### Step 2: Set up transition scores, using a 2D array to reperesent the scoring between categories
```cpp
    int s[3][3] = {
        {0, 2, 3},    // from 0 to 0,1,2
        {4, 0, 5},    // from 1 to 0,1,2
        {1, 6, 0}     // from 2 to 0,1,2
    };
```

### Step 3: Dynamic Programming

```cpp
    vector<int64_t> dp(3, NEG_INF);
    dp[0] = dp[1] = dp[2] = NEG_INF;
```
We define `dp[c]` = max satisfaction ending with category `c`, and will update it based on possible transitions from any `prev` category.

```cpp
const int64_t NEG_INF = -1e15;
```
For initialization, we use a big negative number here to represent an uninitialized or invalid state. 

### Step 4: Process each challenge
```cpp
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
```
This code block loops through the sequence `a`, and for each challenge category `c`, we:
1. make a copy of the current `dp` to `new_dp`
2. if `new_dp[c] is uninitialized, set it to 0 (such that it starts the subsequence here)
3. try to transition from all previous categories to `c`, and update `new_dp[c]` if it is gives higher satisfaction score.

4. ### Step 5: Output the result
5. ```cpp
   cout << max({dp[0], dp[1], dp[2]}) << "\n";
   ```

This gives us the flag:
![alt text](https://github.com/qmkoh/Greyctf2025-writeups/blob/main/misc/dist-elijahs_sequential_ctf/flag.jpg)

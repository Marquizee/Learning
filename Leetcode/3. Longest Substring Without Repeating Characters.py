# Given a string s, find the length of the longest substring without repeating characters.

# Example 1:
# Input: s = "abcabcbb"
# Output: 3
# Explanation: The answer is "abc", with the length of 3.

# Example 2:
# Input: s = "bbbbb"
# Output: 1
# Explanation: The answer is "b", with the length of 1.

# Example 3:
# Input: s = "pwwkew"
# Output: 3
# Explanation: The answer is "wke", with the length of 3.
# Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

# Example 4:
# Input: s = ""
# Output: 0

# Constraints:

# 0 <= s.length <= 5 * 104
# s consists of English letters, digits, symbols and spaces.


def find_longest_substring(instring):
    sub = ''
    all_sub_lengths = []
    for j in range(len(instring)):
        for i in range(j, len(instring)):
            if not instring[i] in sub:
                sub += instring[i]
            else:
                break
        all_sub_lengths.append(len(sub))
        sub = ''
    return 0 if not all_sub_lengths else max(all_sub_lengths)


def main() -> int:
    instring = 'pwwkewa'
    result = find_longest_substring(instring=instring)
    print(result)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

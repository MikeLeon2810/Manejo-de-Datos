def lcs_subcadena(s1, s2): #longest common substring
    max_sub = ""

    for i in range(len(s1)):
        for j in range(i + 1, len(s1) + 1):
            sub = s1[i:j]
            if sub in s2 and len(sub) > len(max_sub):
                max_sub = sub

    return max_sub


if __name__ == '__main__':
    s1 = "AATAGCACTTACA"
    s2=  "AGCTACGCACTTGAC"
    print(lcs_subcadena(s1, s2))
    print(f"La subcadena más larga tiene una longitud de", len(lcs_subcadena(s1, s2)))
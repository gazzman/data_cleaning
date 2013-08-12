# include <stdio.h>

int main(void) {
    int chars[256] = {0}, c;
    while ((c = getchar()) != EOF)
        chars[c] = 1;
    for (c = 32; c < 127; c++) {
        if (chars[c])
            putchar(c);
    }
    putchar('\n');
    return 0;
}

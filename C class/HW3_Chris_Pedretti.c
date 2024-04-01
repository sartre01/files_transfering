/******************************************************************************

                            Online C Compiler.
                Code, Compile, Run and Debug C program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <stdio.h>

int main() {
    int num, negated;
    printf("Enter a signed int: ");
    scanf("%d", &num);

    // Negate the signed integer using bitwise operators, bitwise not + 1 equates to negated int
    negated = (~num) + 1;
    
    printf("Negated value: %d\n", negated);

    return 0;
}
#include <stdio.h>
int main() {
    int num;
    printf("Enter a number: ");
    scanf("%d", &num);
    int lastBits = (num >> 31) & 0b1;
    //right shifts and uses mask to get leftmost bit
    
    printf("The leftmost bit of %d is: %d\n", num, lastBits);

    return 0;
}
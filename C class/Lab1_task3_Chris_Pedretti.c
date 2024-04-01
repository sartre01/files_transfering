#include <stdio.h>
int main() {
    int num;
    printf("Enter a number: ");
    scanf("%d", &num);
    int lastBits = num & 0b111;
    //mask for 3 bits
    
    printf("The last bit of %d is: %d\n", num, lastBits);

    return 0;
}
#include <stdio.h>

int main()
{
    float income, tax, amount;
    //takes income, tax, and amount as floats
    printf("Enter amount of taxable income ($): ");
    scanf("%f", &income);
    //if statements for calculating tax, used
    //amount variable to calculate amount over x for tax
    if (income <= 750.00f)
        tax = 0.01f * income;
    else if (income <= 2250.00f) {
        amount = 0.02f * (income - 750.00f);
        tax = 7.50f + amount;
    }
    else if (income <= 3750.00f) {
        amount = 0.03f * (income - 2250.00f);
        tax = 37.50f + amount;
    }
    else if (income <= 5250.00f) {
        amount = 0.04f * (income - 3750.00f);
        tax = 82.50f + amount;
    }
    else if (income <= 7000.00f) {
        amount = 0.05f * (income - 5250.00f);
        tax = 142.50f + amount;
    }
    else {
        amount = 0.06f * (income - 7000.00f);
        tax = 230.00f + amount;
    }
    
    printf("Tax due: $%.2f\n", tax);

    return 0;
}


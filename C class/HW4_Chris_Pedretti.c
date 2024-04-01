#include <string.h>
#include <stdio.h>

int main() {
    char *validChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    char *lowers = "abcdefghijklmnopqrstuvwxyz";
    char *uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    char *nums = "0123456789";
    char *badChars[] = {
        "password",
        "secret",
        "1234"
    };
    char pw[100];
    int i;
    printf("Enter a password: ");
    scanf("%s", pw);
    int len = strlen(pw);
    int validity = strspn(pw, validChars);

    if (len > 8 && len < 20) {
        // Between 8 and 20 characters
        int foundBadChar = 0;
        for (i = 0; i < 3; i++) {
            // Check for bad characters
            if (strstr(pw, badChars[i]) != NULL) {
                foundBadChar = 1;
                break;
            }
        }
        if (foundBadChar) {
            printf("Invalid password, contains a bad string.");
        } else if (validity == len) {
            if ((strstr(pw, lowers) != NULL) && (strstr(pw, uppers) != NULL)  && (strstr(pw, nums) != NULL)){
                printf("Strong password.\n");
            }
            else{
                printf("Valid password.\n");
            }
        } else {
            printf("Invalid password, contains chars outside validchars.");
        }
    } else {
        printf("Invalid password, improper length (8-20 chars).");
    }

    return 0;
}

// Test case #1:
// Description: test to verify that the length condition (greater than 8 characters) is enforced.
// Input: apple
// Expected result: Invalid password, improper length (8-20 chars). 
// Test case #2:
// Description: test to verify that the length condition (less than 20 characters) is enforced.
// Input: appleappleappleappleappleapple
// Expected result: Invalid password, improper length (8-20 chars).
// Test case #3:
// Description: test to verify that the badChars condition is enforced.
// Input: thisissecret12409
// Expected result: Invalid password, contains a bad string. 
// Test case #4:
// Description: test to verify that the validChars condition is enforced.
// Input: }}??>>
// Expected result: Invalid password, contains chars outside validchars. 
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(){
    char str[11];
    scanf("%s", str);
    //printf("%c \n", str[3]);

    bool foundERROR = false;

    int num;
    while (scanf("%d", &num) != EOF){
        //Logic block
        if(num == -1){ printf("%s\n", str); }
        else if (num < -1 || num > 9){ 
            printf("%s\n", "ERROR"); 
            foundERROR = true;
        }
        else { printf("%c\n", str[num]); }
    }

    if (foundERROR){ 
        return 1;
    }
    
    return 0;
}
#include <stdio.h>
#include <stdlib.h>

int main(){
   // doPhoneThings();
   char str[11];
   scanf("%s", str);
   //printf("%c \n", str[3]);
   
   int num;
   scanf("%d", &num);
   //printf("%d \n", num);

   if(num == -1){ printf("%s \n", str); }
   else if (num < -1 || num > 9){ printf("ERROR \n"); }
   else { printf("%c \n", str[num]); }
}
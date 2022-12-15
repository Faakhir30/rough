#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>
int main() {
char input[128];int count=1;
  
   printf("Enter a multi line string( press ';' to end input)\n");
   scanf("%[^;]s", input);
   char *token=strtok(input," ");    
   while(token!=NULL){
    count++;
    token=strtok(NULL," ");
   }
    token2=strtok(NULL,"\n");
   }
printf("\n\n%d",count);
   return 0;}
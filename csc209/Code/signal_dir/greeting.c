#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>

char *name;

void sing(int code){
    printf("HAPPY BDAY %s! \n", name);
    //kill(getpid(), code); //Kill sends any signal to the current process
}


int main(int argc, char** argv){
    if(argc != 2){ 
        perror("Usage");
    }

    name = argv[1];

    struct sigaction sa;
    sa.sa_handler = sing;
    sa.sa_flags = 0;
    sigemptyset(&sa.sa_mask);
    sigaction(SIGUSR1, &sa, NULL);

    int i = 1;
    while(i == 1){
        i = 1;
    }

    return 0;
}
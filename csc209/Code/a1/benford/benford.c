#include <stdio.h>
#include <stdlib.h>

#include "benford_helpers.h"

/*
 * The only print statement that you may use in your main function is the following:
 * - printf("%ds: %d\n")
 *
 */
int main(int argc, char **argv) {
    int tally[BASE];

    //Populate tally with all 0s
    int i;
    for(i = 0; i < BASE; i++){
        tally[i] = 0;
    }

    //Get target index value
    int targeti = strtol(argv[1], NULL, 10);

    //If too little or too many args given
    if (argc < 2 || argc > 3) {
        fprintf(stderr, "benford position [datafile]\n");
        return 1;
    } 

    //Reads from stdin
    else if (argc == 2){
        //Do input stuff
        int targetNum;
        while(scanf("%d", &targetNum) != EOF){
            add_to_tally(targetNum, targeti, tally);
        }

        int i;
        for (i = 0; i < BASE; i++){
            printf("%ds: %d\n", i, tally[i]);
        }
    }

    //Reads from file at given path
    else if(argc == 3){
        //Do file stuff 
        FILE *numfile = fopen(argv[2], "r");

        int targetNum;;
        while(fscanf(numfile, "%d", &targetNum) != EOF){
            add_to_tally(targetNum, targeti, tally);
        }

        fclose(numfile);

        int i;
        for (i = 0; i < BASE; i++){
            printf("%ds: %d\n", i, tally[i]);
        }
    }

    return 0;
}

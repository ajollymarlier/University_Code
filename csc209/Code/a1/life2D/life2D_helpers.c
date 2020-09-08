#include <stdio.h>
#include <stdlib.h>


void print_state(int *board, int num_rows, int num_cols) {
    for (int i = 0; i < num_rows * num_cols; i++) {
        printf("%d", board[i]);
        if (((i + 1) % num_cols) == 0) {
            printf("\n");
        }
    }
    printf("\n");
}

//TODO Seems to be working but needs further testing
void checkNeighbours(int *board, int num_rows, int num_cols, int rowi, int coli, int *numNeighboursArr){
    int numNeighbours = 0;

    //Top row checks
    if(board[(rowi - 1) * num_cols + (coli - 1)] == 1){ //Top left case
        numNeighbours++;
    }
    if(board[(rowi - 1) * num_cols + coli] == 1){ //Top mid case
        numNeighbours++;
    }
    if (board[(rowi - 1) * num_cols + (coli + 1)] == 1){ //Top right case
        numNeighbours++;
    }

    //Mid row checks
    if(board[(rowi) * num_cols + (coli - 1)] == 1){ //Mid left case
        numNeighbours++;
    }
    
    if(board[(rowi) * num_cols + (coli + 1)] == 1){ //Mid right case
        numNeighbours++;
    }

    //Bottom row checks
    if(board[(rowi + 1) * num_cols + (coli - 1)] == 1){ //Bottom left case
        numNeighbours++;
    }
    if(board[(rowi + 1) * num_cols + (coli)] == 1){ //Bottom mid case
        numNeighbours++;
    }
    if(board[(rowi + 1) * num_cols + (coli + 1)] == 1){ //Bottom right case
        numNeighbours++;
    }

    numNeighboursArr[(rowi) * num_cols + coli] = numNeighbours; //Saves value of num neighbours to corresponding array index
}

//Functional
void updateValues(int *board, int *numNeighboursArr, int num_rows, int num_cols){
    //This iterates through all indices and keeps 2d array configuration
    int rowi;
    for(rowi = 1; rowi < num_rows - 1; rowi++){
        int coli;
        for (coli = 1; coli < num_cols - 1; coli++){
            if(board[(rowi) * num_cols + coli] == 0 && (numNeighboursArr[(rowi) * num_cols + coli] == 2 
                    || numNeighboursArr[(rowi) * num_cols + coli] == 3)){

                board[(rowi) * num_cols + coli] = 1;
            }
            else if(board[(rowi) * num_cols + coli] == 1 && (numNeighboursArr[(rowi) * num_cols + coli] < 2 
                    || numNeighboursArr[(rowi) * num_cols + coli] > 3)){

                board[(rowi) * num_cols + coli] = 0;
            }
        }
    }
}

void update_state(int *board, int num_rows, int num_cols) {
    //NOTE: board is a flattened version of regular 2D array
    int numNeighboursArr[num_rows * num_cols];

    int rowi;
    for(rowi = 1; rowi < num_rows - 1; rowi++){
        int coli;
        for (coli = 1; coli < num_cols - 1; coli++){
            checkNeighbours(board, num_rows, num_cols, rowi, coli, numNeighboursArr);
        }
    }
    
    updateValues(board, numNeighboursArr, num_rows, num_cols);
    
    //TODO for testing contents of numNeighboursArr
    /*printf("\n");
    print_state(numNeighboursArr, num_rows, num_cols);
    printf("\n");*/
}

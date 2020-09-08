#include <stdio.h>
#include <stdlib.h>

#include "life2D_helpers.h" // Getting unresolved reference to function in this h file when compiling

int main(int argc, char **argv) {

    if (argc != 4) {
        fprintf(stderr, "Usage: life2D rows cols states\n");
        return 1;
    }

    int boardHeight = strtol(argv[1], NULL, 10);
    int boardWidth = strtol(argv[2], NULL, 10);
    int numStates = strtol(argv[3], NULL, 10);

    int board[boardHeight * boardWidth];

    int i;
    for(i = 0; i < boardHeight * boardWidth; i++){
        scanf("%d", &board[i]);
    }

    print_state(board, boardHeight, boardWidth);
    for(i = 0; i < numStates - 1; i++){
        update_state(board, boardHeight, boardWidth);
        print_state(board, boardHeight, boardWidth);
    }

    return 0;
}

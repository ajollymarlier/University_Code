#include <stdio.h>

#include "benford_helpers.h"

int count_digits(int num) {
    int count = 0;

    while(num != 0){
        count++;
        num = num / BASE;
    }

    return count;
}

int get_ith_from_right(int num, int i) {
    int modVal = 1;
    int j;
    for (j = 0; j < i + 1; j++){
        modVal *= BASE;
    }

    int divVal = 1;
    for(j = 0; j < i; j++){
        divVal *= BASE;
    }

    num = num % modVal;
    num = num / divVal;

    return num;
}

int get_ith_from_left(int num, int i) {
    int numDigits = count_digits(num);

    return get_ith_from_right(num, (numDigits - 1) - i); //Flips i value and calls get from right
}

void add_to_tally(int num, int i, int *tally) {
    if(count_digits(num) > i){ //Handles out of bunds i values
        int selectDigit = get_ith_from_left(num, i);
        tally[selectDigit]++;
    }

    return;
}

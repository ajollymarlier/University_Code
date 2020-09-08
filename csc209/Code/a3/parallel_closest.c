#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#include "point.h"
#include "serial_closest.h"
#include "utilities_closest.h"

void child_helper(int *fd, double *closest_dest, struct Point *p, int split_arr_size, int pdmax, int *pcount);

/*
 * Multi-process (parallel) implementation of the recursive divide-and-conquer
 * algorithm to find the minimal distance between any two pair of points in p[].
 * Assumes that the array p[] is sorted according to x coordinate.
 */
double closest_parallel(struct Point *p, int n, int pdmax, int *pcount) {
    struct Point *left_p = malloc(sizeof(struct Point) * (n / 2)); 
    struct Point *right_p = malloc(sizeof(struct Point) * (n - (n / 2))); 

    if(left_p == NULL || right_p == NULL){
        perror("malloc");
        exit(1);
    }
    
    //Splits left and right p arrays
    if(n < 4 || pdmax == 0){
        double base_dist = closest_serial(p, n);
        return base_dist;
    }else{
        int i;
        for(i = 0; i < n; i++){
            if(i < n / 2){
                left_p[i] = p[i];
            }else{
                right_p[i - (n / 2)] = p[i];
            }
        }
    }

    //////////////////////////////////////// Left Child Logic //////////////////////////////////////////////////////s

    //Pipes left child and forks
    int left_fd[2];
    if(pipe(left_fd) == -1){
        perror("pipe");
        exit(1);
    }
    
    int left_res = fork();
    if (left_res == -1) {
        perror("fork");
        exit(1);
    }

    double left_closest;
    //Current process is a child
    if(left_res == 0){
        child_helper(left_fd, &left_closest, left_p, n / 2, pdmax, pcount);
    }

    ////////////////////////////// Right Child Logic //////////////////////////////////////////////////////

    //Fork right child
    int right_fd[2];
    if(pipe(right_fd) == -1){
        perror("pipe");
        exit(1);
    }

    int right_res = fork();
    if (right_res == -1) {
        perror("fork");
        exit(1);
    }

    double right_closest;
    //Current process is a child
    if(right_res == 0){
        child_helper(right_fd, &right_closest, right_p, n - (n / 2), pdmax, pcount);
    }

    //////////////////////////////////// Parent Logic ///////////////////////////////////////////////////

    //If current is a parent process
    close(left_fd[1]);
    close(right_fd[1]);

    int left_status;
    int right_status;

    if(waitpid(left_res, &left_status, 0) == -1 || waitpid(right_res, &right_status, 0) == -1){
        perror("wait");
        exit(1);
    }

    //Gets both child processes pcount values and adds them
    if(WIFEXITED(left_status) && WIFEXITED(right_status)){
        *pcount += WEXITSTATUS(left_status) + WEXITSTATUS(right_status) + 2;
    }

    if(read(left_fd[0], &left_closest, sizeof(double)) == -1 || read(right_fd[0], &right_closest, sizeof(double)) == -1){
        perror("read");
        exit(1);
    }

    close(left_fd[0]);
    close(right_fd[0]);
    
    ////////////////////////////////// Below code taken from serial_closest.c ////////////////////////////////////////

    // Gets minimum dist of cross-split points
    // Build an array strip[] that contains points close (closer than d) to the line passing through the middle point.
    struct Point *strip = malloc(sizeof(struct Point) * n);
    if (strip == NULL) {
        perror("malloc");
        exit(1);
    }

    double d = min(left_closest, right_closest);

    int j = 0;
    for (int i = 0; i < n; i++) {
        if (abs(p[i].x - p[n/2].x) < d) {
            strip[j] = p[i], j++;
        }
    }

    free(left_p);
    free(right_p);   
    
    return min(strip_closest(strip, j, d), d);
}

/* Helper Function for all child process logic */
void child_helper(int *fd, double *closest_dest, struct Point *p, int split_arr_size, int pdmax, int *pcount){
    close(fd[0]);
    *closest_dest = closest_parallel(p, split_arr_size, pdmax - 1, pcount);

    if(write(fd[1], closest_dest, sizeof(double)) == -1){
        perror("write to pipe");
        exit(1);
    }

    close(fd[1]);

    exit(*pcount);
}


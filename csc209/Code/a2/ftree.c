#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include "ftree.h"

//Declarations for helper functions
struct dirent *readdir_parser(DIR *target_dir, struct dirent *dir_entry);
struct TreeNode *generator(const char *fname, char *path);
void dir_helper(struct TreeNode* target_node, char *target_path);


/*
 * Filters "." and ".." from readdir results and returns first valid result
 * 
 */
struct dirent *readdir_parser(DIR *target_dir, struct dirent *dir_entry){
    dir_entry = readdir(target_dir);

    if(dir_entry == NULL){
        return NULL;
    }

    while(strncmp(dir_entry->d_name, ".", 1) == 0){
        dir_entry = readdir(target_dir);

        if(dir_entry == NULL){
            return NULL;
        }
    }

    return dir_entry;
}


/*
 * Helper function for taht iterates through directory elements and constructs a sub-ftree with target_node at root
 * 
 */
void dir_helper(struct TreeNode* target_node, char *target_path){
    target_node->type = 'd';

    DIR *target_dir = opendir(target_path);

    //Error checking for opening directory
    if(target_dir == NULL){
        fprintf(stderr, "An error occurred while tring to open the directory at (%s)!\n", target_path);
        exit(1);
    }

    //Gets first entry in target directories
    struct dirent *dir_entry = NULL;
    dir_entry = readdir_parser(target_dir, dir_entry);

    //Adds "/" to end of path for recursive use in dirs
    strncat(target_path, "/", 1);

    if(dir_entry != NULL){ //Checks if something exists within directory
        struct TreeNode *first_entry_node = NULL;
        struct TreeNode *curr_entry_node = NULL;

        first_entry_node = generator(dir_entry->d_name, target_path);
        curr_entry_node = first_entry_node;

        dir_entry = readdir_parser(target_dir, dir_entry);
        while(dir_entry != NULL){
            curr_entry_node->next = generator(dir_entry->d_name, target_path);
            curr_entry_node = curr_entry_node->next;
            dir_entry = readdir_parser(target_dir, dir_entry);
        }

        target_node->contents = first_entry_node;
        free(dir_entry);
    }

    //Closing directory error check
    if(closedir(target_dir) == -1){
        fprintf(stderr, "An error occured while tring to close the directory at (%s)!\n", target_path);  
        exit(1);
    }
}


/*
 * Recursive function that creates a sub-ftree at the path (path + "/" + fname);
 */
struct TreeNode *generator(const char *fname, char *path){
    //Gets full path
    char target_path[strlen(fname) + strlen(path) + 1 + 1]; //Length of fname + length of path + extra "/" + null terminator
    strcpy(target_path, path);
    strcat(target_path, fname);
    target_path[strlen(fname) + strlen(path) + 1] = '\0';

    //Gets stats on target
    struct stat target_stat;
    if(lstat(target_path, &target_stat) == -1){
        fprintf(stderr, "The path (%s) does not point to an existing entry!\n", fname);
        return NULL;
    }

    //Creates TreeNode and fills in common attributes
    struct TreeNode *target_node = malloc(sizeof(struct TreeNode));
    target_node->fname = malloc(sizeof(char) * strlen(fname) + 2);  
    strcpy(target_node->fname, fname);

    target_node->permissions = target_stat.st_mode & 0777;
    target_node->type = 'N'; //Placeholder variable for undetected file
    target_node->contents = NULL;
    target_node->next = NULL;

    //If target is a regular file
    if(S_ISREG(target_stat.st_mode)){
        target_node->type = '-';
    }

    //If target is a directory
    else if(S_ISDIR(target_stat.st_mode)){
        dir_helper(target_node, target_path);
    }

    //If target is a link
    else if(S_ISLNK(target_stat.st_mode)){
        target_node->type = 'l';
    }

    return target_node;
}


/*
 * Returns the FTree rooted at the path fname.
 *
 * Use the following if the file fname doesn't exist and return NULL:
 * fprintf(stderr, "The path (%s) does not point to an existing entry!\n", fname);
 *
 */
struct TreeNode *generate_ftree(const char *fname) {
    char *path = "";
    return generator(fname, path);
}


/*
 * Prints the TreeNodes encountered on a preorder traversal of an FTree.
 *
 * The only print statements that you may use in this function are:
 * printf("===== %s (%c%o) =====\n", root->fname, root->type, root->permissions)
 * printf("%s (%c%o)\n", root->fname, root->type, root->permissions)
 *
 */
void print_ftree(struct TreeNode *root) {
    if (root != NULL){
        // Here's a trick for remembering what depth (in the tree) you're at
        // and printing 2 * that many spaces at the beginning of the line.
        static int depth = 0;
        printf("%*s", depth * 2, "");

        if(root->type == 'd'){ //If root is a directory
            printf("===== %s (%c%o) =====\n", root->fname, root->type, root->permissions);
            depth++;
            print_ftree(root->contents);

            depth--;
            print_ftree(root->next);
        }
        else{ //If root is a file
            printf("%s (%c%o)\n", root->fname, root->type, root->permissions);
            print_ftree(root->next);
        }
    }
}


/* 
 * Deallocate all dynamically-allocated memory in the FTree rooted at node.
 * 
 */
void deallocate_ftree (struct TreeNode *node) {
    if(node != NULL){
        if(node->contents != NULL){ //If node is a directory
            deallocate_ftree(node->contents);
        }

        deallocate_ftree(node->next);

        free(node->fname);
        free(node);

        node = NULL; //Removes original node and all sub-nodes from FTree
    }
}

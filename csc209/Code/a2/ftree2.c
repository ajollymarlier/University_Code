#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include "ftree.h"

void *safe_malloc(size_t size);
char *formulate_full_path(const char *fname, char *path);
struct TreeNode *generate_ftree_helper(const char *fname, char *path);
struct TreeNode *ftree_dir_helper(const char *fname, char *path);

// Malloc helper function that deals with error
void *safe_malloc(size_t size){
    void *ptr = malloc(size);

    if(ptr == NULL){
        //Deal with failed MALLOC call
    }
    
    return ptr;
}


//Helper function that forms full path from fname and gicen previous path
char *formulate_full_path(const char *fname, char *path){
    //This block formulates current path string
    int full_path_len = strlen(path) + strlen(fname);
    char *full_path = malloc(sizeof(char) * (full_path_len + 1));

    strncpy(full_path, path, strlen(path)); //TODO am i using this right?
    strncat(full_path, "/", 1); //Adds extra backlash
    strncat(full_path, fname, strlen(fname)); //Appends current fname to path

    return full_path;
}

struct TreeNode *ftree_dir_helper(const char *fname, char *path){
    char *curr_path = formulate_full_path(fname, path);
    DIR *dir_ptr = opendir(curr_path);

    if(dir_ptr == NULL){
        fprintf(stderr, "The path (%s) does not point to an existing entry!\n", curr_path);
        return NULL;
    }

    struct dirent *entry_ptr;
    entry_ptr = readdir(dir_ptr);
    
    struct TreeNode *curr_file_node = malloc(sizeof(struct TreeNode));
    while(entry_ptr != NULL){
        curr_file_node->next = generate_ftree_helper(fname, path);
        curr_file_node = curr_file_node->next;
    }

    //Error checking for closed directory
    if(closedir(dir_ptr) == -1){
        fprintf(stderr, "Error closing directory at %s", curr_path);
    }

    return curr_file_node;
}


//TODO consider splitting into multiple functions
//Helper recursive function for generate_ftree
struct TreeNode *generate_ftree_helper(const char *fname, char *path){
    struct TreeNode *curr_node = malloc(sizeof(struct TreeNode));
    strncpy(curr_node->fname, fname, strlen(fname));

    char *curr_path = formulate_full_path(fname, path);

    //This block gets file information
    struct stat curr_stat;
    if(lstat(curr_path, &curr_stat) == -1){
        fprintf(stderr, "The path (%s) does not point to an existing entry!\n", fname);
        return NULL;
        //TODO WHAT DO I DO AFTER ERROR IS CAUGHT?
    }

    //This block loads TreeNode data
    if(S_ISREG(curr_stat.st_mode)){ //If path leads to regular file
        curr_node->permissions = curr_stat.st_mode & 0777;
        curr_node->type = '-';
        curr_node->contents = NULL;
    }

    else if(S_ISDIR(curr_stat.st_mode)){ //If path leads to directory
        curr_node->permissions = curr_stat.st_mode & 0777;
        curr_node->type = 'd';
        curr_node->contents = ftree_dir_helper(fname, path);
    }

    else if(S_ISLNK(curr_stat.st_mode)){ //If path leads to link
        curr_node->permissions = curr_stat.st_mode & 0777;
        curr_node->type = 'l';
        curr_node->contents = NULL;
    }
    //TODO should we deal with other type?

    curr_node->next = generate_ftree_helper(curr_node->fname, curr_path);

    //free(curr_path);
    return curr_node;
}


/*
 * Returns the FTree rooted at the path fname.
 *
 * Use the following if the file fname doesn't exist and return NULL:
 * fprintf(stderr, "The path (%s) does not point to an existing entry!\n", fname);
 *
 */
struct TreeNode *generate_ftree(const char *fname) {

    // Your implementation here.
    return generate_ftree_helper(fname, "");

    /*struct TreeNode *testTree = malloc(sizeof(struct TreeNode));
    testTree->fname = "Hello";
    testTree->permissions = 412;
    testTree->type = '-';
    testTree->contents = NULL;
    
    testTree->next = NULL;
    return testTree;

    struct TreeNode *testSubTree = malloc(sizeof(struct TreeNode));
    testSubTree->fname = "Goodbye";
    testSubTree->permissions = 888;
    testSubTree->type = 'l';
    testSubTree->contents = NULL;
    //testTree = NULL;

    testTree->next = testSubTree;

    return testTree;*/

    // Hint: consider implementing a recursive helper function that
    // takes fname and a path.  For the initial call on the 
    // helper function, the path would be "", since fname is the root
    // of the FTree.  For files at other depths, the path would be the
    // file path from the root to that file.
    
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
	//TODO needs to be tested


    // Here's a trick for remembering what depth (in the tree) you're at
    // and printing 2 * that many spaces at the beginning of the line.
    static int depth = 0;
    printf("%*s", depth * 2, "");

    if (root != NULL){
        if(root->contents != NULL){ //If root is a directory
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
   
   // Your implementation here.
    if(node != NULL){
        if(node->contents != NULL){ //If node is a directory
            deallocate_ftree(node->contents);

            free(node);
        }
        else{ //If node is a file
            deallocate_ftree(node->next);

            free(node);
        }

        node = NULL; //removes original node and all sub-nodes from FTree //TODO needs testing
    }
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <signal.h>
#include "socket.h"

#ifndef PORT
    #define PORT 56309
#endif

#define LISTEN_SIZE 5
#define WELCOME_MSG "Welcome to CSC209 Twitter! Enter your username: \r\n"
#define SEND_MSG "send"
#define SHOW_MSG "show"
#define FOLLOW_MSG "follow"
#define UNFOLLOW_MSG "unfollow"
#define INVALID_USERNAME_MSG "That is an invalid username. Please enter another: \r\n"
#define BUF_SIZE 256
#define MSG_LIMIT 8
#define FOLLOW_LIMIT 5

struct client {
    int fd;
    struct in_addr ipaddr;
    char username[BUF_SIZE];
    char message[MSG_LIMIT][BUF_SIZE];
    struct client *following[FOLLOW_LIMIT]; // Clients this user is following
    struct client *followers[FOLLOW_LIMIT]; // Clients who follow this user
    char inbuf[BUF_SIZE]; // Used to hold input from the client
    char *in_ptr; // A pointer into inbuf to help with partial reads
    struct client *next;
};


// Provided functions. 
void add_client(struct client **clients, int fd, struct in_addr addr);
void remove_client(struct client **clients, int fd);

// These are some of the function prototypes that we used in our solution 
// You are not required to write functions that match these prototypes, but
// you may find them helpful when thinking about operations in your program.

// Send the message in s to all clients in active_clients. 
void announce(struct client *active_clients, char *username){
    struct client *curr_client = active_clients;
    while(curr_client != NULL){
        char announce_msg[BUF_SIZE];

        for(int i = 0; i < BUF_SIZE; i++){
            announce_msg[i] = '\0';
        }

        strncat(announce_msg, "User ", 5);
        strncat(announce_msg, username, strlen(username));
        strncat(announce_msg, " has just joined! \r\n", 21);

        if(write(curr_client->fd, announce_msg, strlen(announce_msg)) == -1){
                fprintf(stderr, "Error writing announcement of new client %s \n", curr_client->username);
                exit(1);
        }

        curr_client = curr_client->next;
    }
    
}

// Move client c from new_clients list to active_clients list. 
//TODO pretty sure its working, but also needs server messages
void activate_client(struct client *c, 
    struct client **active_clients_ptr, struct client **new_clients_ptr){
        struct client *prev_client = *new_clients_ptr;
        struct client *curr_client = (*new_clients_ptr)->next;

        while(curr_client != NULL){
            if(curr_client->fd == c->fd){
                //Removes client from new_clients
                prev_client->next = curr_client->next;

                //Adds client to active_clients
                curr_client->next = *(active_clients_ptr);
                *active_clients_ptr = curr_client;

                printf("User %s logged in. \n", inet_ntoa(c->ipaddr));
                break;
            }

            prev_client = curr_client;
            curr_client = curr_client->next;
        }

        //One New Client Check
        if((*new_clients_ptr)->fd == c->fd && *new_clients_ptr != NULL){
            struct client *temp = *active_clients_ptr;
            *active_clients_ptr = c;
            (*active_clients_ptr)->next = temp;
            (*new_clients_ptr) = (*new_clients_ptr)->next;

            printf("User %s logged in. \n", inet_ntoa(c->ipaddr));
            announce(*active_clients_ptr, c->username);
        }
    }

//Code taken from lab 10
int find_network_newline(const char *buf, int n) {
    //Find the network newline //TODO idk if working properly
    for(int i = 0; i < n - 1; i++){
        if(buf[i] == '\r' && buf[i + 1] == '\n'){
            return i;
        }
    }

    return -1;
}

//Helper method to check valid username
//TODO Dont know if not working, or testing is wrong
//TODO needs server messages
int valid_username_check(int *cur_fd, char *temp_inbuf, struct client *clients){
    int nbytes;
    if((nbytes = read(*cur_fd, temp_inbuf, BUF_SIZE)) > 0){ //Reads username from socket
        printf("Checking username %s with %d bytes read\n", temp_inbuf, nbytes); //TODO for testing only

        //TODO need to change behaviour of this loop so that it stores all data until \r\n is found
        //Terminating Read String
        int where = -1;
        while((where = find_network_newline(temp_inbuf, nbytes)) == -1){
            //TODO need to move pointer to following string
        }

        temp_inbuf[where] = '\0';

        //Checking Username
        struct client *curr_client = clients;
        while(curr_client != NULL){
            if(strcmp(temp_inbuf, curr_client->username) == 0){
                printf("Username %s already exists\n", temp_inbuf); //TODO for testing only
                return -1;
            }

            curr_client = curr_client->next;
        }

        return 0;
    }  

    fprintf(stderr, "Error reading username data");
    return -1;
}

//Helper method to check if found client is in searcher list already
//mode is either 'following' or 'followers'
int contains_user(struct client *c, struct client *target_client){
    for(int i = 0; i < FOLLOW_LIMIT; i++){
        if(c->followers[i] != NULL && strcmp((c->followers)[i]->username, target_client->username) == 0){
            char *already_followed_msg = "Target User already followed \r\n";
            if(write(c->fd, already_followed_msg, strlen(already_followed_msg)) == -1){
                fprintf(stderr, "Error writing following limit error to client \n");
                exit(1);
            }

            printf("User %s already followed by %s \n", target_client->username, c->username);

            return 1;
        }
    }

    return 0;
}

//Helper function for processing follow command
//TODO need to add server messages
//TODO needs testing
void follow_handler(char *arg, struct client **active_clients, struct client *c){
    struct client *curr_client = *active_clients;

    int found_client = 0;
    while(curr_client != NULL){
        if(strcmp(curr_client->username, arg) == 0){
            found_client = 1;
            if(contains_user(c, curr_client) == 1){

            }
            else if((c->following)[FOLLOW_LIMIT - 1] != NULL){
                char *follow_limit_msg = "Cannot follow. You're following limit has already been reached. \r\n";
                if(write(c->fd, follow_limit_msg, strlen(follow_limit_msg)) == -1){
                    fprintf(stderr, "Error writing following limit error to client \n");
                    exit(1);
                }

                //Records follow failure on server side
                printf("%s failed to follow %s due to following limit\n", c->username, curr_client->username);
            }
            else if((curr_client->followers)[FOLLOW_LIMIT - 1] != NULL){
                char *follow_limit_msg = "Cannot follow. You're target's followers limit has already been reached. \r\n";
                if(write(c->fd, follow_limit_msg, strlen(follow_limit_msg)) == -1){
                    fprintf(stderr, "Error writing follower limit error to client \n");
                    exit(1);
                }

                //Records follow failure on server side
                printf("%s failed to follow %s due to followers limit\n", c->username, curr_client->username);
            }
            else{
                int following_size = sizeof(c->following) / sizeof((c->following)[0]);
                int followers_size = sizeof(curr_client->followers) / sizeof((curr_client->followers)[0]);

                (c->following)[following_size] = curr_client;
                (curr_client->followers)[followers_size] = c;

                char *follow_confirm_msg = "User Followed \r\n";
                if(write(c->fd, follow_confirm_msg, strlen(follow_confirm_msg)) == -1){
                    fprintf(stderr, "Error writing follower limit error to client \n");
                    exit(1);
                }

                //Records follow on server side
                printf("%s followed %s\n", c->username, curr_client->username);

                break;
            }
        }

        curr_client = curr_client->next;
    }

    if(found_client == 0){
        char *not_found_msg = "User not found\r\n";
        if(write(c->fd, not_found_msg, strlen(not_found_msg)) == -1){
            fprintf(stderr, "Error writing follower limit error to client \n");
            exit(1);
        }

        printf("User %s not found \n", arg);
    }
}

//Helper function for processing unfollow command
//TODO need add server and client messages
void unfollow_handler(char *arg, struct client **active_clients, struct client *c){
    struct client *curr_client = *active_clients;

    while(curr_client != NULL){
        //Removes c from target followers list
        if(strcmp(curr_client->username, arg) == 0){
            int i = 0;
            while(curr_client->followers[i] != NULL){
                if(strcmp(curr_client->followers[i]->username, c->username) == 0){
                    memmove(&(curr_client->followers[i]), &(curr_client->followers[i + 1]), FOLLOW_LIMIT - (i + 1));
                    break;
                }

                i++;
            }

            //Removes curr_client from c's following list
            int j = 0;
            while(c->following[j] != NULL){
                if(strcmp(c->following[j]->username, curr_client->username) == 0){
                    memmove(&(c->following[j]), &(c->following[j + 1]), FOLLOW_LIMIT - (j + 1));
                    break;
                }

                j++;
            }
        }

        curr_client = curr_client->next;
    }
}

//Helper function for processing show command
void show_handler(struct client **active_clients, struct client *c){
    int i = 0;
    while(c->followers[i] != NULL){
        int j = 0;
        while(strlen(c->following[i]->message[j]) != 0){
            char tweet_msg[BUF_SIZE];

            for (int i = 0; i < MSG_LIMIT; i++) {
               tweet_msg[i] = '\0';
            }

            strncat(tweet_msg, c->following[i]->username, strlen(c->following[i]->username));
            strncat(tweet_msg, " wrote: ", 8);
            strncat(tweet_msg, c->following[i]->message[j], strlen(c->following[i]->message[j]));
            strncat(tweet_msg, "\r\n", 2);

            if(write(c->fd, tweet_msg, strlen(tweet_msg)) == -1){
                fprintf(stderr, "Error reporting followed tweet \n");
                exit(1);
            }

            j++;
        }

        i++;      
    }
}

//Helper function for processing send command
void send_handler(char *arg, struct client **active_clients, struct client *c){
    if(strlen(arg) > 140){
        char *msg_limit_msg = "Message character limit exceeded! \r\n";
        if(write(c->fd, msg_limit_msg, strlen(msg_limit_msg)) == -1){
                fprintf(stderr, "Error writing character limit error to client \n");
                exit(1);
        }
    } //TODO need to add MSG_LIMIT check
    else if(strlen(c->message[MSG_LIMIT]) != 0){
        char *msg_limit_msg = "Message publishing limit exceeded! \r\n";
        if(write(c->fd, msg_limit_msg, strlen(msg_limit_msg)) == -1){
                fprintf(stderr, "Error writing publishing limit error to client \n");
                exit(1);
        }
    }
    else{

        int i = 0;
        while(c->followers[i] != NULL){
            strncat(arg, "\r\n", 2);
            if(write(c->followers[i]->fd, arg, strlen(arg)) == -1){ //TODO seg fault occurs here after following, sending, unfollowing, sending
                fprintf(stderr, "Error sending message to %s failed \n", c->followers[i]->username);
                exit(1);
            }

            i++;
        }

        for(int i = 0; i < FOLLOW_LIMIT; i++){
            if(strlen(c->message[i]) == 0){
                strncat(c->message[i], arg, strlen(arg));
            }
        }
    }
}

//Helper function for processing quit command
void quit_handler(struct client **active_clients, struct client *c){
    remove_client(active_clients, c->fd);
    
    printf("User %s from %s logged out. \n", c->username, inet_ntoa(c->ipaddr));
}


// Helper control method 
void handle_command(char *command, char *arg, struct client **active_clients, struct client *c){
    if(strcmp(command, "follow") == 0){
        follow_handler(arg, active_clients, c);
    }
    else if (strcmp(command, "unfollow") == 0){
        unfollow_handler(arg, active_clients, c);
    }
    else if(strcmp(command, "show") == 0){
        show_handler(active_clients, c);
    }
    else if(strcmp(command, "send") == 0 && strlen(arg) > 0){
        send_handler(arg, active_clients, c);
    }
    else if(strcmp(command, "quit") == 0){
        quit_handler(active_clients, c);
    }
    else{
        char *invalid_cmd_msg = "Invalid Command! \r\n";
        if (write(c->fd, invalid_cmd_msg, strlen(invalid_cmd_msg)) == -1) {
                fprintf(stderr, 
                    "Write to client %s failed\n", c->username);
                    exit(1);
        }

        printf("User %s entered an invalid command \n", c->username);
    }
}


// The set of socket descriptors for select to monitor.
// This is a global variable because we need to remove socket descriptors
// from allset when a write to a socket fails. 
fd_set allset;

/* 
 * Create a new client, initialize it, and add it to the head of the linked
 * list.
 */
void add_client(struct client **clients, int fd, struct in_addr addr) {
    struct client *p = malloc(sizeof(struct client));
    if (!p) {
        perror("malloc");
        exit(1);
    }

    printf("Adding client %s\n", inet_ntoa(addr));
    p->fd = fd;
    p->ipaddr = addr;
    p->username[0] = '\0';
    p->in_ptr = p->inbuf;
    p->inbuf[0] = '\0';
    p->next = *clients;

    // initialize messages to empty strings
    for (int i = 0; i < MSG_LIMIT; i++) {
        p->message[i][0] = '\0';
    }

    *clients = p;
}

/* 
 * Remove client from the linked list and close its socket.
 * Also, remove socket descriptor from allset.
 */
void remove_client(struct client **clients, int fd) {
    struct client **p;

    for (p = clients; *p && (*p)->fd != fd; p = &(*p)->next)
        ;

    // Now, p points to (1) top, or (2) a pointer to another client
    // This avoids a special case for removing the head of the list

    //Removes the client from followers and following in all clients
    if (*p) {
        struct client *curr_client = (*(clients));
        while(curr_client != NULL){
            for(int i = 0; i < FOLLOW_LIMIT; i++){
                //Remove from followers
                if(curr_client->followers[i] != NULL && strcmp(curr_client->followers[i]->username, (*(p))->username) == 0){
                    curr_client->followers[i] = curr_client->followers[i + 1];
                } 

                //Remove from following
                if(curr_client->followers[i] != NULL && strcmp(curr_client->following[i]->username, (*(p))->username) == 0){ //TODO seg fault here
                    curr_client->following[i] = curr_client->following[i + 1];
                } 
            }
        }


        // Remove the client
        struct client *t = (*p)->next;
        printf("Removing client %d %s\n", fd, inet_ntoa((*p)->ipaddr));
        FD_CLR((*p)->fd, &allset);
        close((*p)->fd);
        free(*p);
        *p = t;
    } else {
        fprintf(stderr, 
            "Trying to remove fd %d, but I don't know about it\n", fd);
    }
}


int main (int argc, char **argv) {
    int clientfd, maxfd, nready;
    struct client *p;
    struct sockaddr_in q;
    fd_set rset;

    // If the server writes to a socket that has been closed, the SIGPIPE
    // signal is sent and the process is terminated. To prevent the server
    // from terminating, ignore the SIGPIPE signal. 
    struct sigaction sa;
    sa.sa_handler = SIG_IGN;
    sa.sa_flags = 0;
    sigemptyset(&sa.sa_mask);
    if (sigaction(SIGPIPE, &sa, NULL) == -1) {
        perror("sigaction");
        exit(1);
    }

    // A list of active clients (who have already entered their names). 
    struct client *active_clients = NULL;

    // A list of clients who have not yet entered their namxx`es. This list is
    // kept separate from the list of active clients, because until a client
    // has entered their name, they should not issue commands or 
    // or receive announcements. 
    struct client *new_clients = NULL;

    struct sockaddr_in *server = init_server_addr(PORT);
    int listenfd = set_up_server_socket(server, LISTEN_SIZE);
    free(server);

    // Initialize allset and add listenfd to the set of file descriptors
    // passed into select 
    FD_ZERO(&allset);
    FD_SET(listenfd, &allset);

    // maxfd identifies how far into the set to search
    maxfd = listenfd;

    while (1) {
        // make a copy of the set before we pass it into select
        rset = allset;

        nready = select(maxfd + 1, &rset, NULL, NULL, NULL);
        if (nready == -1) {
            perror("select");
            exit(1);
        } else if (nready == 0) {
            continue;
        }

        // check if a new client is connecting
        if (FD_ISSET(listenfd, &rset)) {
            printf("A new client is connecting\n");
            clientfd = accept_connection(listenfd, &q);

            FD_SET(clientfd, &allset);
            if (clientfd > maxfd) {
                maxfd = clientfd;
            }
            printf("Connection from %s\n", inet_ntoa(q.sin_addr));
            add_client(&new_clients, clientfd, q.sin_addr);
            char *greeting = WELCOME_MSG;
            if (write(clientfd, greeting, strlen(greeting)) == -1) {
                fprintf(stderr, 
                    "Write to client %s failed\n", inet_ntoa(q.sin_addr));
                remove_client(&new_clients, clientfd);
            }
        }

        // Check which other socket descriptors have something ready to read.
        // The reason we iterate over the rset descriptors at the top level and
        // search through the two lists of clients each time is that it is
        // possible that a client will be removed in the middle of one of the
        // operations. This is also why we call break after handling the input.
        // If a client has been removed, the loop variables may no longer be 
        // valid.
        int cur_fd, handled;
        for (cur_fd = 0; cur_fd <= maxfd; cur_fd++) {
            if (FD_ISSET(cur_fd, &rset)) {
                handled = 0;

                // Check if any new clients are entering their names
                for (p = new_clients; p != NULL; p = p->next) {
                    if (cur_fd == p->fd) {
                        // TODO: handle input from a new client who has not yet
                        // entered an acceptable name
                        char user_inbuf[BUF_SIZE];

                        printf("Handling new client \n"); //TODO for testing only

                        while(valid_username_check(&cur_fd, user_inbuf, active_clients) == -1){
                            char *bad_uname_msg = INVALID_USERNAME_MSG;

                            if(write(clientfd, bad_uname_msg, strlen(bad_uname_msg)) == -1){
                                    fprintf(stderr, 
                                                "Write to client %s of username failed\r\n", inet_ntoa(q.sin_addr));
                                                exit(1);
                            }

                        }

                        strcpy(p->username, user_inbuf);
                        activate_client(p, &active_clients, &new_clients);

                        printf("User %s logged in \n",  active_clients->username); //TODO for testing only
                        
                        handled = 1;
                        break;
                    }
                }

                if (!handled) {
                    // Check if this socket descriptor is an active client
                    for (p = active_clients; p != NULL; p = p->next) {
                        if (cur_fd == p->fd) {
                            int num_read;
                            if((num_read = read(cur_fd, p->in_ptr, BUF_SIZE - strlen(p->inbuf))) > 0){

                                //Handles partial reads
                                int where;
                                if((where = find_network_newline(p->inbuf, BUF_SIZE)) != -1){
                                    char *pre_command = strtok(p->inbuf, " ");
                                    char *pre_rest = strtok(NULL, "");
                                    if(pre_rest == NULL){
                                        if(pre_command[strlen(pre_command) - 1 - 1] == '\r' && pre_command[strlen(pre_command) - 1] == '\n'){
                                            pre_command[strlen(pre_command) - 1 - 1] = '\0';
                                        }

                                        char command[BUF_SIZE];

                                        for(int i = 0; i < BUF_SIZE; i++){
                                            command[i] = '\0';
                                        }

                                        strncat(command, pre_command, strlen(pre_command));

                                        printf("Command Read: %s\n", command);

                                        handle_command(command, "", &active_clients, p);

                                        p->in_ptr = p->inbuf;
                                        for(int i = 0; i < BUF_SIZE; i++){
                                            p->inbuf[i] = '\0';
                                        }

                                    }else{
                                        if(pre_rest[strlen(pre_rest) - 1 - 1] == '\r' && pre_rest[strlen(pre_rest) - 1] == '\n'){
                                            pre_rest[strlen(pre_rest) - 1 - 1] = '\0';
                                        }

                                        char command[BUF_SIZE];
                                        char rest[BUF_SIZE];

                                        for(int i = 0; i < BUF_SIZE; i++){
                                            command[i] = '\0';
                                            rest[i] = '\0';
                                        }

                                        strncat(command, pre_command, strlen(pre_command));
                                        strncat(rest, pre_rest, strlen(pre_rest));



                                        printf("Command Read: %s, with arg: %s\n", command, rest);

                                        handle_command(command, rest, &active_clients, p);

                                        p->in_ptr = p->inbuf;
                                        for(int i = 0; i < BUF_SIZE; i++){
                                            p->inbuf[i] = '\0';
                                        }
                                    }

                                    
                                }else{
                                    p->in_ptr += num_read;

                                }
                                
                               

                            }else{
                                fprintf(stderr, "Read of active client command failed");
                                exit(1);
                            }
                            break;
                        }
                    }
                }
            }
        }
    }
    return 0;
}

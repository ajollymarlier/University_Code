#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>


#ifndef PORT
  #define PORT 56309
#endif
#define BUF_SIZE 128

int main(void) {
    // Read username
    char username[BUF_SIZE +1];
    //printf("Username: ");
    // fflush(stdin);
    int numb_read = read(STDIN_FILENO, username, BUF_SIZE);
    
    username[numb_read - 1] = '\0'; // remove newline

    // Create the socket FD.
    int sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0) {
        perror("client: socket");
        exit(1);
    }

    // Set the IP and port of the server to connect to.
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);
    if (inet_pton(AF_INET, "127.0.0.1", &server.sin_addr) < 1) {
        perror("client: inet_pton");
        close(sock_fd);
        exit(1);
    }

    // Connect to the server.
    if (connect(sock_fd, (struct sockaddr *)&server, sizeof(server)) == -1) {
        perror("client: connect");
        close(sock_fd);
        exit(1);
    }


    int numb_written = write(sock_fd, username, numb_read);
    if (numb_written != numb_read) {
        perror("Client username write");
        close(sock_fd);
        exit(1);
    }
    // Read input from the user, send it to the server, and then accept the
    // echo that returns. Exit when stdin is closed.
    int max_fd = sock_fd; // This should be the servers fd
    fd_set all_fds;
    FD_ZERO(&all_fds);
    FD_SET(sock_fd, &all_fds);
    FD_SET(STDIN_FILENO, &all_fds);

    char buf[BUF_SIZE + 1];
    while (1) {
        fd_set listen_fds = all_fds;
        int nready = select(max_fd + 1, &listen_fds, NULL, NULL, NULL);
        if (nready == -1) {
            perror("client: select");
            exit(1);
        }

        // Is it from the server?
        if (FD_ISSET(sock_fd, &listen_fds)) {
            int num_read = read(sock_fd, buf, BUF_SIZE);                                
            buf[num_read] = '\0';
            if (num_read == 0 ){ 
                perror("client: nothing retrieved from server");
                exit(1);
            }
            // FD_CLR(sock_fd, &listen_fds);
            // FD_SET(sock_fd, &all_fds);            
            
            printf("Received from server: %s", buf);
        }
        // int num_read;
        // Is it from standard in?       
        if (FD_ISSET(STDIN_FILENO, &listen_fds)) {
            int num_read = read(STDIN_FILENO, buf, BUF_SIZE);
            //FD_SET(STDIN_FILENO, &all_fds);
            // FD_CLR(STDIN_FILENO, &all_fds)
            if (num_read == 0) {
                break;
            }
            
            buf[num_read] = '\0';         

            int num_written = write(sock_fd, buf, num_read);
            if (num_written != num_read) {
                perror("client: write");
                close(sock_fd);
                exit(1);
            }
        
        }
        //for (int i=0; i < 2; i++;) {
        //if (FD_ISSET(sock_fd, &listen
            
        //}
        // num_read = read(sock_fd, buf, BUF_SIZE);
        // buf[num_read] = '\0';
        // printf("Received from server: %s", buf);
    }

    close(sock_fd);
    return 0;
}
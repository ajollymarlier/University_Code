#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define MAXLINE 256
#define MAX_PASSWORD 10

#define SUCCESS "Password verified\n"
#define INVALID "Invalid password\n"
#define NO_USER "No such user\n"

int main(void) {
  char user_id[MAXLINE];
  char password[MAXLINE];

  /* The user will type in a user name on one line followed by a password 
     on the next.
     DO NOT add any prompts.  The only output of this program will be one 
	 of the messages defined above.
   */

  if(fgets(user_id, MAXLINE, stdin) == NULL) {
      perror("fgets");
      exit(1);
  }
  if(fgets(password, MAXLINE, stdin) == NULL) {
      perror("fgets");
      exit(1);
  }

  int fd[2];
  if(pipe(fd) == -1){
    perror("pipe");
  }

  //If fork fails
  int pid = fork();
  if (pid == -1) {
    perror("fork");
  }
  
  //Current process is child
  else if (pid == 0){
    close(fd[1]);
     dup2(fd[0], 0);

    int result = execl("./validate", "validate", NULL);

    if(result == -1){
      perror("exec");
      exit(1);
    }

    exit(0);
  }
  
  //Current process is parent
  else{
    close(fd[0]);

    if(write(fd[1], user_id, MAX_PASSWORD) == -1){
      perror("write to pipe");
    }

    //TODO password not saving correct value
    if(write(fd[1], password, MAX_PASSWORD) == -1){
      perror("write to pipe");
    }

    int status;
    if(waitpid(pid, &status, 0) == -1){
      exit(1);
    }

    else{
      if(WIFEXITED(status)){
        if(WEXITSTATUS(status) == 0){
          printf("%s", SUCCESS);
        } else if(WEXITSTATUS(status) == 2){
          printf("%s", INVALID);
        } else if(WEXITSTATUS(status) == 3){
          printf("%s", NO_USER);
        }
      }
    }
  }

  return 0;
}
/*
* This file demonstrates how to use sockets in C to connect to a server
* and send a HTTP GET request to the ser
*
* The server is our web service which we created in Python
*/  

#include <stdio.h>
#include <errno.h>      // library containing error codes
#include <stdlib.h>
#include <string.h>


#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>

// in C, we need to make sure that we have enough space for the message
// and the reply
#define MSG_SIZE 1024
#define REPLY_SIZE 65536

// Function to URL encode a string
void url_encode(char *dest, const char *src, size_t dest_size) {
    char *d = dest;
    const char *s = src;
    char hex[] = "0123456789ABCDEF";

    // for each character
    // if it is a letter, then we leave it
    while (*s && (d - dest < dest_size - 4)) {
        if (('a' <= *s && *s <= 'z') || ('A' <= *s && *s <= 'Z') || ('0' <= *s && *s <= '9')) {
            *d++ = *s;
        // otherwise we encode it
        // for example space is %20
        } else {
            *d++ = '%';
            *d++ = hex[*s >> 4];
            *d++ = hex[*s & 15];
        }
        s++;
    }
    // we have to manually end the string with 0 (\0 in C)
    *d = '\0';
}

/*
* The main function of the program
*/
int main(int argc, char* argv[])
{
    int iSocket = -1;               // id of the socket, -1 indicates that the socket does not exist
    struct sockaddr_in addrServer;  // address of the server as a dedicated structure
    char strMessage[MSG_SIZE] = { 0 };  // message to send (will be a HTTP GET)        
    char strReply[REPLY_SIZE] = { 0 };  // buffer for the reply
    int recv_size = 0;

    if (argc != 2) {
        printf("Usage: %s <seed_text>\n", argv[0]);
        exit(1);
    }

    char *seed_text = argv[1];
    char encoded_seed_text[MSG_SIZE/2] = { 0 };

    // URL encode the seed_text
    url_encode(encoded_seed_text, seed_text, sizeof(encoded_seed_text));

    // Create a socket, but not yet bind it to the address yet
    // i.e we only create the "file" which will help us to get the data from the 
    // internet
    // AF_INET means that we can communicate with all addresses on the internet using IPv4
    // SOCK_STREAM means that we will use TCP, SOCK_DGRAM means that we use UDP
    if ((iSocket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("Error: Could not create socket: %s. Exiting...\n", strerror(errno));
        exit(1);
    }

    // reserving the place for the server address
    // and filling it with 0s (memset)
    memset(&addrServer, 0, sizeof(addrServer));

    // fill in the server address
    addrServer.sin_addr.s_addr = inet_addr("127.0.0.1");      // One of public DNS servers
    addrServer.sin_family = AF_INET;
    addrServer.sin_port = htons(5000);

    // Here we connect to the server, but we do not send/request anything yet
    if (connect(iSocket, (struct sockaddr*)(&addrServer), sizeof(addrServer)) < 0) {
        printf("Error: Could not connect to server: %s. Exiting..\n", strerror(errno));
        exit(1);
    }

    // Here we send the data to the server
    // first we copy a string to the message buffer
    snprintf(strMessage, MSG_SIZE, "GET /prompt?seed_text=%s HTTP/1.0\r\n\r\n", encoded_seed_text);

    printf("Sending message to server:\n\n%s\n", strMessage);

    // and we send the content of the buffer to the socket
    if (send(iSocket, strMessage, strlen(strMessage), 0) < 0) {
        printf("Error: Could not send http request to server: %s. Exiting..\n", strerror(errno));
        exit(1);
    }

    // Receive a reply from the server
    printf("\nWaiting for server reply..\n");

    // here we receive the data and put it into the buffer again
    // which is a character array in our case
    if ((recv_size = recv(iSocket, strReply, REPLY_SIZE, 0)) < 0) {
        printf("Error: Something wrong happened while getting reply from server: %s. Exiting..\n", strerror(errno));
        exit(1);
    }
    
	printf("Response size: %d\n", recv_size);

    // we add the 0 to the end of the string
    //strReply[REPLY_SIZE - 1] = 0;

    // print the server reply
    printf("\nServer Reply:\n\n");
    printf("%s\n", strReply);

    close(iSocket);

    exit(0);
} 
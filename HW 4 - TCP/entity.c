/******************************************************************************/
/*                                                                            */
/* ENTITY IMPLEMENTATIONS                                                     */
/*                                                                            */
/******************************************************************************/

// Student names:
// Student computing IDs:
//
//
// This file contains the actual code for the functions that will implement the
// reliable transport protocols enabling entity "A" to reliably send information
// to entity "B".
//
// This is where you should write your code, and you should submit a modified
// version of this file.
//
// Notes:
// - One way network delay averages five time units (longer if there are other
//   messages in the channel for GBN), but can be larger.
// - Packets can be corrupted (either the header or the data portion) or lost,
//   according to user-defined probabilities entered as command line arguments.
// - Packets will be delivered in the order in which they were sent (although
//   some can be lost).
// - You may have global state in this file, BUT THAT GLOBAL STATE MUST NOT BE
//   SHARED BETWEEN THE TWO ENTITIES' FUNCTIONS. "A" and "B" are simulating two
//   entities connected by a network, and as such they cannot access each
//   other's variables and global state. Entity "A" can access its own state,
//   and entity "B" can access its own state, but anything shared between the
//   two must be passed in a `pkt` across the simulated network. Violating this
//   requirement will result in a very low score for this project (or a 0).
//
// To run this project you should be able to compile it with something like:
//
//     $ gcc entity.c simulator.c -o myproject
//
// and then run it like:
//
//     $ ./myproject 0.0 0.0 10 500 3 test1.txt
//
// Of course, that will cause the channel to be perfect, so you should test
// with a less ideal channel, and you should vary the random seed. However, for
// testing it can be helpful to keep the seed constant.
//
// The simulator will write the received data on entity "B" to a file called
// `output.dat`.

#include <stdio.h>
#include <string.h>
#include "simulator.h"

#define BUFFER_SIZE 100000
#define WINDOW_SIZE 8
float INCREMENT = 200.0;

/*For entity A*/
int nextSeqNum, base;
struct pkt buffer[BUFFER_SIZE];

/*For entity B*/
int expectedSeqNum;
struct pkt lastSentPacket;

/*Helper functions*/
int checksum(struct pkt packet){
    int checksum = packet.seqnum + packet.acknum + packet.length;
    for (int i = 0; i < 20; i++){
        checksum += packet.payload[i];
    }
    return checksum;
}

/**** A ENTITY ****/

void A_init() {
    nextSeqNum = 1;
    base = 1;
    // for (int i = 0; i < BUFFER_SIZE; i++){
    //     buffer[i].seqnum = -1;
    // }

}

void A_output(struct msg message) {
    if (nextSeqNum < base + WINDOW_SIZE) {
        struct pkt packet;
        packet.seqnum = nextSeqNum;
        packet.acknum = nextSeqNum;
        // packet.acknum = -1;
        // packet.acknum = nextSeqNum;
        for (int i  = 0; i < 20; i++){
            packet.payload[i] = message.data[i];
        }
        
        packet.length = message.length;
        packet.checksum = checksum(packet);
        buffer[nextSeqNum] = packet;

        tolayer3_A(packet);

        if (base == nextSeqNum){
            starttimer_A(INCREMENT);
        }

        nextSeqNum++;
    }

    return;
}

void A_input(struct pkt packet) {
    if (packet.checksum == checksum(packet)){
        // if (packet.seqnum < base + WINDOW_SIZE){
            base = packet.acknum + 1;
            if (base == nextSeqNum){
                stoptimer_A();
            }
            else{
                starttimer_A(INCREMENT);
            }
        // }
    }

    return;
}

void A_timerinterrupt() {
    starttimer_A(INCREMENT);
    for (int seq = base; seq < nextSeqNum; seq++){
        tolayer3_A(buffer[seq]);
    }

    return;
}


/**** B ENTITY ****/

void B_init() {
    expectedSeqNum = 1;
}

void B_input(struct pkt packet) {
    if (packet.checksum == checksum(packet) && packet.seqnum == expectedSeqNum){
        struct msg newMessage;
        int length = packet.length;
        for (int i  = 0; i < 20; i++){
            newMessage.data[i] = packet.payload[i];
        }
        newMessage.length = length;
        tolayer5_B(newMessage);

        struct pkt newPacket = packet;
        newPacket.acknum = expectedSeqNum;
        tolayer3_B(newPacket);
        expectedSeqNum += 1;
        lastSentPacket = packet;
    }

    else{
        tolayer3_B(lastSentPacket);
    }

    return;
}

void B_timerinterrupt() {
}

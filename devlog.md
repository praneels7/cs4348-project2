# CS 4348 Project 2 Development Log

## Session 1 — Teller and customer synchronization

### Plan
I’ll start with one teller thread and one customer thread. I’ll use semaphores to control when each thread can proceed, then run a deposit to check that the messages appear in order and both threads exit.
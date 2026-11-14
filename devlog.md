# CS 4348 Project 2 Development Log

## Session 1 — Teller and customer synchronization

### Plan
I’ll start with one teller thread and one customer thread. I’ll use semaphores to control when each thread can proceed, then run a deposit to check that the messages appear in order and both threads exit.

## Session 2 — Three tellers and a shared customer line

### Plan

I’ll expand the single-customer version to three tellers and six customers. I’ll use a shared FIFO queue for the customer line and give each customer their own semaphore so only that customer wakes up when a teller is assigned. I’ll keep every transaction as a deposit for this test.

### Reflection

I ran `python3 project2.py` and saw all three tellers report ready before the first customer entered. All six customers completed one deposit and left the bank. All three tellers signed off before the closing message, and the terminal prompt returned.

Customer 1 joined the line last even though they had a low ID. Thread scheduling determines when each customer reaches the line, and the queue serves them in the order they join.

## Session 3 — Door, manager, and safe

### Plan

I’ll add semaphores for the bank door, manager, and safe. I’ll keep the simulation at six customers so I can follow the deposit and withdrawal paths in the terminal output.

### Reflection

I added semaphores that allow two customers to use the door, one teller to request manager approval, and two tellers to use the safe at a time. I replaced the fixed deposit and test delay with random transaction choices and delays. Both transaction types use the safe, and withdrawals require manager approval first.

### Testing

I still need to run the updated version and follow one deposit and one withdrawal by customer ID. I’ll check that the deposit skips the manager, the withdrawal gets approval before entering the safe, and all six customers and three tellers leave before the bank closes.
from collections import deque
from random import choice, randint
from threading import Semaphore, Thread
from time import sleep


TELLER_COUNT = 3
CUSTOMER_COUNT = 6


class CustomerVisit:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.teller_id = None
        self.transaction = None
        self.assigned = Semaphore(0)
        self.introduced = Semaphore(0)
        self.transaction_requested = Semaphore(0)
        self.transaction_provided = Semaphore(0)
        self.transaction_complete = Semaphore(0)
        self.left_teller = Semaphore(0)


def main():
    line = deque()
    line_lock = Semaphore(1)
    customers_waiting = Semaphore(0)
    tellers_ready = Semaphore(0)
    door = Semaphore(2)
    manager = Semaphore(1)
    safe = Semaphore(2)

    def teller(teller_id):
        print(f"Teller {teller_id} []: ready to serve")
        tellers_ready.release()

        while True:
            print(f"Teller {teller_id} []: waiting for a customer")
            customers_waiting.acquire()

            with line_lock:
                visit = line.popleft()

            # Main adds one shutdown marker per teller after all customers leave.
            if visit is None:
                print(f"Teller {teller_id} []: leaving for the day")
                return

            visit.teller_id = teller_id
            visit.assigned.release()
            visit.introduced.acquire()

            actor = f"Teller {teller_id} [Customer {visit.customer_id}]"
            print(f"{actor}: asks for transaction")
            visit.transaction_requested.release()
            visit.transaction_provided.acquire()

            print(f"{actor}: handling {visit.transaction} transaction")

            if visit.transaction == "withdrawal":
                print(f"{actor}: going to the manager")
                with manager:
                    print(f"{actor}: getting manager's permission")
                    sleep(randint(5, 30) / 1000)
                    print(f"{actor}: got manager's permission")

            print(f"{actor}: going to safe")
            with safe:
                print(f"{actor}: enter safe")
                sleep(randint(10, 50) / 1000)
                print(f"{actor}: leaving safe")

            print(f"{actor}: finishes {visit.transaction} transaction")
            print(f"{actor}: waiting for customer to leave")
            visit.transaction_complete.release()
            visit.left_teller.acquire()

    def customer(visit):
        customer_id = visit.customer_id
        visit.transaction = choice(("deposit", "withdrawal"))

        print(f"Customer {customer_id} []: wants to perform a {visit.transaction} transaction")
        print(f"Customer {customer_id} []: waiting to go to the bank")
        sleep(randint(0, 100) / 1000)
        print(f"Customer {customer_id} []: going to bank.")

        print(f"Customer {customer_id} []: waiting to enter through the door")
        with door:
            print(f"Customer {customer_id} []: entering bank.")

        with line_lock:
            print(f"Customer {customer_id} []: getting in line")
            line.append(visit)

        customers_waiting.release()
        visit.assigned.acquire()

        actor = f"Customer {customer_id} [Teller {visit.teller_id}]"
        print(f"{actor}: selects teller")
        print(f"{actor}: introduces itself")
        visit.introduced.release()
        visit.transaction_requested.acquire()

        print(f"{actor}: asks for {visit.transaction} transaction")
        visit.transaction_provided.release()
        visit.transaction_complete.acquire()

        print(f"{actor}: leaves teller")
        visit.left_teller.release()

        print(f"Customer {customer_id} []: goes to door")
        with door:
            print(f"Customer {customer_id} []: leaves the bank")

    tellers = [
        Thread(target=teller, args=(teller_id,))
        for teller_id in range(TELLER_COUNT)
    ]
    for thread in tellers:
        thread.start()

    for _ in tellers:
        tellers_ready.acquire()

    customers = [
        Thread(target=customer, args=(CustomerVisit(customer_id),))
        for customer_id in range(CUSTOMER_COUNT)
    ]
    for thread in customers:
        thread.start()
    for thread in customers:
        thread.join()

    with line_lock:
        for _ in tellers:
            line.append(None)

    for _ in tellers:
        customers_waiting.release()
    for thread in tellers:
        thread.join()

    print("The bank closes for the day.")


if __name__ == "__main__":
    main()
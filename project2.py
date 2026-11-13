from threading import Semaphore, Thread


def main():
    introduced = Semaphore(0)
    transaction_requested = Semaphore(0)
    transaction_provided = Semaphore(0)
    transaction_complete = Semaphore(0)
    customer_left = Semaphore(0)
    transaction = None

    def teller():
        print("Teller 0 []: ready to serve")
        print("Teller 0 []: waiting for a customer")
        introduced.acquire()

        print("Teller 0 [Customer 0]: asks for transaction")
        transaction_requested.release()
        transaction_provided.acquire()

        print(f"Teller 0 [Customer 0]: finishes {transaction} transaction")
        transaction_complete.release()

        print("Teller 0 [Customer 0]: waiting for customer to leave")
        customer_left.acquire()
        print("Teller 0 []: leaving for the day")

    def customer():
        nonlocal transaction

        print("Customer 0 [Teller 0]: introduces itself")
        introduced.release()
        transaction_requested.acquire()

        transaction = "deposit"
        print(f"Customer 0 [Teller 0]: asks for {transaction} transaction")
        transaction_provided.release()
        transaction_complete.acquire()

        print("Customer 0 [Teller 0]: leaves teller")
        customer_left.release()

    teller_thread = Thread(target=teller)
    customer_thread = Thread(target=customer)

    teller_thread.start()
    customer_thread.start()

    customer_thread.join()
    teller_thread.join()
    print("The bank closes for the day.")


if __name__ == "__main__":
    main()
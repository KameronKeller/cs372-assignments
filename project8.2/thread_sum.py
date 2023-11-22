import threading

def runner(thread_id, starting_val, ending_val, result):
    sum = 0

    # Add up the sum for the range - the Fast Way
    sum_of_int_end_val = ending_val * ( ending_val + 1 ) // 2
    # Note: Must subtract 1 from starting val to ensure the end result is inclusive of the starting value
    sum_of_int_start_val = (starting_val - 1) * ((starting_val - 1) + 1) // 2

    sum = sum_of_int_end_val - sum_of_int_start_val

    # Add up the sum for the range - the Slow Way
    # for value in range(starting_val, ending_val + 1):
        # sum += value

    # Save the result in the global result variable
    result[thread_id] = sum

def main():
    threads = []

    # Sample range #1
    # ranges = [
    #     [1,5],
    #     [20,22]
    # ]

    # Sample range #2
    ranges = [
        [10, 20],
        [1, 5],
        [70, 80],
        [27, 92],
        [0, 16]
    ]

    # One thread for each range
    num_threads = len(ranges)

    # Create an empty list to store results
    result = [0] * num_threads

    for i in range(num_threads):
        
        # Get the range for the current thread
        r = ranges[i]

        # Get the starting value of the range
        starting_val = r[0]

        # Get the ending value of the range
        ending_val = r[-1]

        # Create the thread
        t = threading.Thread(target=runner, args=(i, starting_val, ending_val, result))

        # Start the thread
        t.start()

        # Keep track of the thread
        threads.append(t)

    # Join all the threads once they finish
    for t in threads:
        t.join()

    # Print the results
    print(result)
    print(sum(result))

if __name__ == "__main__":
    main()
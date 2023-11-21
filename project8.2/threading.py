def main():
    ranges = [
        [1,5],
        [20,22]
    ]

    # One thread for each range
    num_threads = len(ranges)

    result = [0] * num_threads
    print(result)

if __name__ == "__main__":
    main()
from argparse import ArgumentParser
from cProfile import label
from thresh import main
import matplotlib.pyplot as plt


def run(traces_path: str, addr_bits: int):

    hits = []
    acc = []
    for addr_bits in range(10, 22):
        accuracy, hit_rate = main(traces_path=traces_path, addr_bits=addr_bits, hist_bits=4, threshold=6)

        acc.append(accuracy)
        hits.append(hit_rate)

    plt.figure(figsize=(12, 8))
    plt.plot(range(10,22), acc, '-o', color='red', label='accuracy')
    plt.plot(range(10,22), hits, '-o', color='blue', label='hit_rate')
    plt.title("Accuracy & Hit Rate vs Length of address bits when history bits = 4 and threshold = 6")
    plt.legend()
    plt.show()

    hits = []
    acc = []
    for hist_bits in range(4, 11):
        accuracy, hit_rate = main(traces_path=traces_path, addr_bits=18, hist_bits=hist_bits, threshold=6)

        acc.append(accuracy)
        hits.append(hit_rate)

    plt.figure(figsize=(12, 8))
    plt.plot(range(4,11), acc, '-o', color='red', label='accuracy')
    plt.plot(range(4,11), hits, '-o', color='blue', label='hit_rate')
    plt.title("Accuracy & Hit Rate vs Length of history bits when address bits = 18 and threshold = 6")
    plt.legend()
    plt.show()

    hits = []
    acc = []
    for threshold in range(4, 33):
        accuracy, hit_rate = main(traces_path=traces_path, addr_bits=18, hist_bits=5, threshold=threshold)

        acc.append(accuracy)
        hits.append(hit_rate)

    plt.figure(figsize=(12, 8))
    plt.plot(range(4,33), acc, '-o', color='red', label='accuracy')
    plt.plot(range(4,33), hits, '-o', color='blue', label='hit_rate')
    plt.title("Accuracy & Hit Rate vs Threshold when address bits = 18 and history bits = 5")
    plt.legend()
    plt.show()


    print(f"Address bits = 18, history bits = 5, threshold = 4")
    accuracy, hit_rate = main(traces_path=traces_path, addr_bits=18, hist_bits=5, threshold=4)
    


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--trace-file", dest='trace_path',
                        default="traces/pinatrace.txt", help="Path of the traces file", type=str)
    parser.add_argument("-a", "--address-bits", dest='addr_bits', default=16,
                        help="Length of the bits of Address to be considered", type=int)
    args = parser.parse_args()
    run(traces_path=args.trace_path, addr_bits=args.addr_bits)

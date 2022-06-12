from argparse import ArgumentParser


def read_traces(traces_path: str):
    output = []
    with open(traces_path, 'r') as f:
        for line in f:
            if (line == '#eof\n'):
                break
            output.append([line.split(':')[0], line.split()[1],
                          line.split()[2][:-1], line.split(',')[1][:-1]])
            # output.append(line.split())
    return output


def exp2(m):
    return (1 << m)


def process(trace: list, load_val_hist: list, counter_table: list, addr_bits: int, hist_bits: int, threshold: int) -> bool:
    src_addr, op_mode, dst_addr, hex_val = trace
    # print(src_addr, op_mode, dst_addr, hex_val)

    addr = int(dst_addr, 16)
    actual = int(hex_val, 16)
    # print(addr, actual)

    index = addr & (exp2(addr_bits)-1)

    count_index = load_val_hist[index][0]
    pred = load_val_hist[index][1]

    count = counter_table[count_index]

    true_positive, true_negative, false_positive, false_negative = False, False, False, False

    if (pred == actual):
        if (count > threshold):
            true_positive = True
        else:
            false_positive = True
        count_index = (count_index << 1 | 0) & hist_bits
        count = count + 1 if count != (len(counter_table)-1) else count
    else:
        if (count > threshold):
            true_negative = True
        else:
            false_negative = True
        count = count - 1 if count != 0 else 0
        count_index = (count_index << 1 | 1) & hist_bits

    # update the actual
    load_val_hist[index][1] = actual
    # update the history
    load_val_hist[index][0] = count_index
    # update the count
    counter_table[count_index] = count

    return true_positive, true_negative, false_positive, false_negative


def main(traces_path: str, addr_bits: int, hist_bits: int, threshold: int) -> str:
    # print(traces_path, addr_bits, hist_bits, threshold)
    traces = read_traces(traces_path=traces_path)

    load_val_hist = []
    for i in range(exp2(addr_bits)):
        load_val_hist.append([0, 0])  # [hist_bits, val]

    counter_table = []
    for i in range(exp2(hist_bits)):
        counter_table.append(0)  # [counter]

    correct_count = 0
    false_positive_count = 0
    for i, trace in enumerate(traces):
        correct_prediction, _, false_positive, _ = process(
            trace, load_val_hist, counter_table, addr_bits, hist_bits, threshold)
        if correct_prediction:
            correct_count = correct_count + 1
        if false_positive:
            false_positive_count = false_positive_count + 1

    hit_rate = (correct_count/len(traces))*100
    print(f"Hit Rate: {hit_rate}")
    accuracy = (correct_count / (false_positive_count + correct_count)) * 100
    print(f"Accuracy: {accuracy}")

    return accuracy, hit_rate


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-i", "--trace-file", dest='trace_path',
                        default="traces/pinatrace.txt", help="Path of the traces file", type=str)
    parser.add_argument("-a", "--address-bits", dest='addr_bits', default=10,
                        help="Length of the bits of Address to be considered", type=int)
    parser.add_argument("-c", "--hist-bits", dest='hist_bits', default=4,
                        help="Length of bits of the History Table", type=int)
    parser.add_argument("-t", "--threshold", dest='threshold', default=6,
                        help="Threshold of the prediction confidence", type=int)

    args = parser.parse_args()
    main(traces_path=args.trace_path, addr_bits=args.addr_bits,
         hist_bits=args.hist_bits, threshold=args.threshold)

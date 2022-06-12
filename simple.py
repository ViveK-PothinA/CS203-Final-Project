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


def process(trace: list, prev_value: int) -> bool:
    src_addr, op_mode, dst_addr, hex_val = trace
    # print(src_addr, op_mode, dst_addr, hex_val)
    actual = int(hex_val, 16)
    # print(addr, actual)

    if (prev_value == actual):
        return True, actual
    else:
        return False, actual


def main(traces_path: str) -> str:

    traces = read_traces(traces_path=traces_path)

    prev_value = 0

    correct_count = 0
    total = 0
    for i, trace in enumerate(traces):
        correct_prediction, prev_value = process(trace, prev_value)
        # print(prev_value, end='\r')
        total = total + 1
        if correct_prediction:
            correct_count = correct_count + 1

    print(f"Hit Rate: {(correct_count/total)*100}")


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-i", "--trace-file", dest='trace_path',
                        default="traces/pinatrace.txt", help="Path of the traces file", type=str)

    args = parser.parse_args()
    main(traces_path=args.trace_path)

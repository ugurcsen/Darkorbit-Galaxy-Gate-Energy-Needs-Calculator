import random

import matplotlib.pyplot as plt
import numpy
import numpy as np


def calculate_gg_tries(gate_size, ratios, gate_part_count_which_already_have=0, show_charts=False, tries=100):
    all_results = []
    for x in range(2, 7):
        use_multiplier_when = x

        results_arr = []
        gate_part_counts_matrix = []
        for j in range(tries):
            gate_part_counts = []
            gate_parts = np.zeros(gate_size)
            gate_parts[:gate_part_count_which_already_have] = 1
            multiplier = 1
            i = 0
            while not all(gate_parts == 1):
                r = random.randrange(0, 100)
                is_gate_part = (r < 100 * ratios["gate_part"])
                if is_gate_part:
                    if multiplier == use_multiplier_when:
                        multiplier += 1
                        while multiplier > 1 and not all(gate_parts == 1):
                            gate_part_number = random.randrange(0, gate_size)
                            if gate_parts[gate_part_number] == 0:
                                gate_parts[gate_part_number] = 1
                                multiplier -= 1
                    else:
                        gate_part_number = random.randrange(0, gate_size)
                        if gate_parts[gate_part_number] == 0:
                            gate_parts[gate_part_number] = 1
                        else:
                            multiplier += 1

                elif multiplier == use_multiplier_when:
                    multiplier = 1

                gate_part_counts.append(gate_parts.sum())
                i += 1
            results_arr.append(i)
            gate_part_counts_matrix.append(gate_part_counts)

        result = np.array(results_arr)
        print("Multiplier:", use_multiplier_when, "/ Avg GG Energy:", result.mean(), "/ Min GG Energy:", result.min(),
              "/ Max GG Energy:", result.max())
        all_results.append(result.mean())
        if show_charts:
            max_tries = max(map(len, gate_part_counts_matrix))
            gate_parts_count_avg = []
            for i in range(max_tries):
                summ = 0
                c = 0
                t = []
                for j in range(tries):
                    if len(gate_part_counts_matrix[j]) > i:
                        summ += gate_part_counts_matrix[j][i]
                        c += 1
                gate_parts_count_avg.append(summ / c)
            plt.plot(range(1, max_tries + 1), gate_parts_count_avg)
    if show_charts:
        plt.legend(["x2", "x3", "x4", "x5", "x6"])
        plt.ylabel("Part Counts")
        plt.xlabel("GG Energy")
        plt.title("Part Counts Every GG Energy Spends")
        plt.show()
    return all_results

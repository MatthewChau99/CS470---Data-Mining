import itertools
import sys
import time

# Variable Initialization
file = open(sys.argv[1], 'r', encoding='utf-8')
subset_mapping = {}
freq_count = {}


def singles(threshold):
    removeSet = set()
    # input singles data into subset_mapping and freq_count
    count = 1
    for line in file:
        row = tuple(map(int, line.strip().split()))
        subset_mapping.update({count: set([x for x in row])})
        count = count + 1
        for x in row:
            freq_count.update({x: 1 if x not in freq_count else freq_count.get(x) + 1})

    # remove infrequent singles
    for single in freq_count:
        if freq_count.get(single) < threshold:
            removeSet.add(single)

    for row in subset_mapping:
        subset_mapping.update({row: subset_mapping.get(row) - removeSet})

    for infrequent_set in removeSet:
        freq_count.pop(infrequent_set)


def multiples(threshold):
    while subset_mapping:
        removeSet = set()
        freq_count_local = {}

        # updating k + 1 subsets
        for row in list(subset_mapping.keys()):
            k_subsets = subset_mapping[row]
            # remove row if it does not have any frequent subsets
            if not k_subsets:
                subset_mapping.pop(row)
                continue

            # generating k + 1 subsets
            if isinstance(list(subset_mapping.get(row))[0], int):
                k_plus_subsets = set(itertools.combinations(sorted(k_subsets), 2))
            else:
                k_plus_subsets = set(
                    [tuple(sorted(set(set1).union(set2))) for set1, set2 in itertools.product(k_subsets, k_subsets) if
                     len(set(set1) - set(set2)) == 1])

            # remove row if it's not generating anymore k + 1 subsets
            if not k_plus_subsets:
                subset_mapping.pop(row)
                continue

            # pruning
            if len(list(k_plus_subsets)[0]) > 2:
                for k_plus_subset in list(k_plus_subsets):
                    if not set(itertools.combinations(k_plus_subset, len(k_plus_subset) - 1)).issubset(k_subsets):
                        k_plus_subsets.remove(k_plus_subset)

            # replacing k + 1 subsets with k subsets in subset_mapping
            subset_mapping.update({row: set(k_plus_subsets)})

            # updating k + 1 subsets to local freq count
            for k_plus_subset in k_plus_subsets:
                freq_count_local.update({
                    k_plus_subset: 1 if k_plus_subset not in freq_count_local else freq_count_local.get(
                        k_plus_subset) + 1})

        # removing infrequent k + 1 subsets from local freq count
        for k_plus_subset in list(freq_count_local.keys()):
            if freq_count_local.get(k_plus_subset) < threshold:
                removeSet.add(k_plus_subset)
                freq_count_local.pop(k_plus_subset)
        print("freq_count_local: ", len(freq_count_local))

        if len(freq_count_local) == 0:
            break

        # updating infrequent k + 1 subsets from subset_mapping
        for row in subset_mapping:
            subset_mapping.update({row: subset_mapping.get(row) - removeSet})
        print("subset_mapping: ", len(subset_mapping))

        freq_count.update(freq_count_local)


# Execution of the program
def apriori(threshold):
    singles(threshold)
    multiples(threshold)


start_time = time.time()

apriori(int(sys.argv[2]))

print("--- %s seconds ---" % (time.time() - start_time))


# Output file
def output():
    list_output = list(freq_count.keys())
    for i in range(len(list_output)):
        if isinstance(list_output[i], int):
            list_output[i] = (list_output[i],)
    list_output = sorted(list_output)

    output_file = open(sys.argv[3], "w")
    for i in range(len(list_output)):
        freq_set = list_output[i] if len(list_output[i]) > 1 else list_output[i][0]
        output_file.write(
            str((freq_set if isinstance(freq_set, int) else " ".join(map(str, freq_set)))) + (
                    " (%d) " % freq_count[freq_set]))
        output_file.write("\n")
    print(len(freq_count))


output()

from collections import defaultdict

def minimize(dfa):
    print("\nDurum indirgeme işlemi başlatıldı...")

    non_accepting = dfa.states - dfa.accept_states
    partitions = [dfa.accept_states, non_accepting]

    new_partitions = []

    while True:
        new_partitions = []
        for partition in partitions:
            split = split_partition(dfa, partition, partitions)
            new_partitions.extend(split)

        if partitions == new_partitions:
            break
        partitions = new_partitions[:]

    minimized_states = {",".join(sorted(p)) for p in partitions}

    minimized_start_state = next(
        ",".join(sorted(partition))
        for partition in partitions
        if dfa.start_state in partition
    )
    minimized_accept_states = {
        ",".join(sorted(partition))
        for partition in partitions
        if any(state in dfa.accept_states for state in partition)
    }

    minimized_transition_function = {}
    for partition in partitions:
        representative = next(iter(partition))
        for symbol in dfa.alphabet:
            next_state = dfa.transition_function.get((representative, symbol))
            if next_state:
                for new_partition in partitions:
                    if next_state in new_partition:
                        minimized_transition_function[
                            (",".join(sorted(partition)), symbol)
                        ] = ",".join(sorted(new_partition))
                        break

    print("\n--- İndirgenmiş DFA ---")
    print("Yeni Durumlar:")
    for state in minimized_states:
        print(f"{state}")
    print("\nBaşlangıç Durumu:")
    print(f"{minimized_start_state}")
    print("\nKabul Durumları:")
    for state in minimized_accept_states:
        print(f"{state}")
    print("\nGeçiş Fonksiyonu:")
    for (state, symbol), next_state in minimized_transition_function.items():
        print(f"{state} --{symbol}--> {next_state}")

    dfa.states = minimized_states
    dfa.start_state = minimized_start_state
    dfa.accept_states = minimized_accept_states
    dfa.transition_function = minimized_transition_function


def split_partition(dfa, partition, partitions):
    splits = defaultdict(list)
    for state in partition:
        key = tuple(
            next((i for i, p in enumerate(partitions) if dfa.transition_function.get((state, a)) in p), None)
            for a in dfa.alphabet
        )
        splits[key].append(state)
    return [set(s) for s in splits.values()]

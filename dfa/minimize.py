from collections import defaultdict
from typing import Set


def minimize(dfa):
    print("\nDurum indirgeme işlemi başlatıldı...")
    states: Set[str] = dfa.states
    accept_states: Set[str] = dfa.accept_states

    non_accepting = states - accept_states
    partitions = [accept_states, non_accepting]

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
        if any(state in accept_states for state in partition)
    }

    minimized_transition_function = {}
    for partition in partitions:
        representative = next(iter(partition))
        for symbol in dfa.alphabet:
            next_state = dfa.transition_function.get((representative, symbol))
            if next_state:
                for new_partition in partitions:
                    if next_state in new_partition:
                        partition_key: str = ",".join(sorted(partition))
                        new_partition_key: str = ",".join(sorted(new_partition))
                        transition_key: tuple[str, str] = (partition_key, symbol)

                        minimized_transition_function[transition_key] = new_partition_key
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

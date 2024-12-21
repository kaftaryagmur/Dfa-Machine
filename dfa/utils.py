def get_user_input():
    states = input("DFA Makinesi oluşturmak için durumları virgülle ayırarak girin (örn: q0,q1,q2): ").split(',')
    states = set(states)

    alphabet = input("Alfabeyi virgülle ayırarak girin (örn: a,b): ").split(',')
    alphabet = set(alphabet)

    print("\nGeçiş fonksiyonunu belirtin (örn: q0,a,q1). 'bitti' yazarak çıkın.")
    transition_function = {}

    while True:
        transition = input("Geçiş: ")
        if transition.lower() == 'bitti':
            missing_transitions = []
            for state in states:
                for symbol in alphabet:
                    if (state, symbol) not in transition_function:
                        missing_transitions.append((state, symbol))

            if missing_transitions:
                print("\nEksik geçişler bulundu:")
                for state, symbol in missing_transitions:
                    print(f"({state}, {symbol}) -> ?")
                print("Lütfen eksik geçişleri tamamlayın.")
                continue
            else:
                break

        try:
            current_state, symbol, next_state = transition.split(',')
            if current_state not in states or next_state not in states:
                print(f"Hata: '{current_state}' veya '{next_state}' durumu tanımlı değil.")
                continue
            if symbol not in alphabet:
                print(f"Hata: '{symbol}' sembolü alfabede tanımlı değil.")
                continue
            if (current_state, symbol) in transition_function:
                print(f"Hata: '{current_state}' durumunda '{symbol}' sembolü için zaten bir geçiş tanımlandı!")
                continue
            transition_function[(current_state, symbol)] = next_state
        except ValueError:
            print("Geçiş formatı hatalı. Lütfen 'q0,a,q1' formatında girin.")

    start_state = input("\nBaşlangıç durumunu girin: ")
    while start_state not in states:
        print(f"Hata: '{start_state}' tanımlı değil. Tekrar deneyin.")
        start_state = input("\nBaşlangıç durumunu girin: ")

    accept_states = input("Kabul durumlarını virgülle ayırarak girin (örn: q1,q2): ").split(',')
    accept_states = set(accept_states)
    invalid_accept_states = [state for state in accept_states if state not in states]
    if invalid_accept_states:
        print(f"Hata: Kabul durumları içinde tanımlı olmayan durumlar var: {', '.join(invalid_accept_states)}")
        return get_user_input()

    return states, alphabet, transition_function, start_state, accept_states

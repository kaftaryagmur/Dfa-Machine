from graphviz import Digraph

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
def visualize_dfa(states, alphabet, transition_function, start_state, accept_states, filename="dfa_graph"):
    """
    DFA'yı görselleştir ve bir dosya olarak kaydet.
    :param states: DFA'nın durumları (set)
    :param alphabet: DFA'nın alfabesi (set)
    :param transition_function: Geçiş fonksiyonu (dict)
    :param start_state: Başlangıç durumu (str)
    :param accept_states: Kabul durumları (set)
    :param filename: Oluşturulacak dosyanın adı (str)
    """
    dot = Digraph()
    dot.attr(rankdir='LR')  # Sol-sağ yönlü çizim
    dot.attr('node', shape='circle')

    # Kabul durumlarını çift çemberle göster
    for state in accept_states:
        dot.node(state, shape='doublecircle')

    # Diğer durumları ekle
    for state in states - accept_states:
        dot.node(state)

    # Geçişleri ekle
    for (state, symbol), next_state in transition_function.items():
        dot.edge(state, next_state, label=symbol)

    # Başlangıç durumunu göster
    dot.node('', shape='none')  # Boş düğüm
    dot.edge('', start_state)

    # Çizimi kaydet
    dot.render(filename, format="png", cleanup=True)
    print(f"DFA çizimi '{filename}.png' olarak kaydedildi.")

def edit_dfa(dfa):
    """
    DFA üzerinde düzenlemeler yapar.
    Kabul durumu çıkarma işlemine, yalnızca bir kabul durumu varsa veya seçilen durum kabul durumu değilse izin verilmez.
    """
    while True:
        print("\n--- DFA Düzenleme ---")
        print("1) Yeni durum ekle")
        print("2) Kabul durumu ekle")
        print("3) Kabul durumu çıkar")
        print("4) Çıkış")

        choice = input("Seçiminizi yapın: ")

        if choice == '1':
            new_state = input("Yeni durumu girin: ")
            if new_state in dfa.states:
                print(f"Hata: '{new_state}' zaten tanımlı.")
            else:
                dfa.states.add(new_state)
                print(f"'{new_state}' durumu başarıyla eklendi.")

                # Yeni durum için eksik geçişleri tamamlama
                for symbol in dfa.alphabet:
                    if (new_state, symbol) not in dfa.transition_function:
                        next_state = input(f"Geçişi tamamlayın: ({new_state}, {symbol}) -> ")
                        while next_state not in dfa.states:
                            print(f"Hata: '{next_state}' DFA'nın durumları arasında değil.")
                            next_state = input(f"Geçişi tekrar girin: ({new_state}, {symbol}) -> ")
                        dfa.transition_function[(new_state, symbol)] = next_state
                        print(f"Geçiş eklendi: ({new_state}, {symbol}) -> {next_state}")

        elif choice == '2':
            state = input("Kabul durumuna eklenecek durumu girin: ")
            if state not in dfa.states:
                print(f"Hata: '{state}' DFA'nın durumları arasında değil.")
            else:
                dfa.accept_states.add(state)
                print(f"'{state}' kabul durumlarına başarıyla eklendi.")

        elif choice == '3':
            if len(dfa.accept_states) == 1:
                print("Hata: Tek bir kabul durumu olduğundan, bu işlem gerçekleştirilemez.")
                continue

            state = input("Kabul durumlarından çıkarılacak durumu girin: ")
            if state not in dfa.accept_states:
                print(f"Hata: '{state}' kabul durumlarında değil.")
            else:
                dfa.accept_states.remove(state)
                print(f"'{state}' kabul durumlarından başarıyla çıkarıldı.")

        elif choice == '4':
            print("DFA düzenleme menüsünden çıkılıyor.")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

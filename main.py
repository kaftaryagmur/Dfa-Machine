from dfa.core import DFA
from dfa.utils import get_user_input, visualize_dfa, edit_dfa   # visualize_dfa işlevi eklendi
from dfa.minimize import minimize

def main():
    states, alphabet, transition_function, start_state, accept_states = get_user_input()
    dfa = DFA(states, alphabet, transition_function, start_state, accept_states)

    while True:
        print("\n----- DFA Menü -----")
        print("1) DFA makinesi için karakter katarı denemesi")
        print("2) Durum indirgeme")
        print("3) DFA geçiş tablosunu göster")
        print("4) Yeni DFA tanımla")
        print("5) DFA'yı Çiz")
        print("6) DFA'yı Düzenle")
        print("7) Çıkış")

        choice = input("Seçiminizi yapın: ")

        if choice == '1':
            input_string = input("\nGiriş dizisini girin: ")
            if dfa.process(input_string):
                print("Girdi dizisi kabul edildi.")
            else:
                print("Girdi dizisi reddedildi.")
        elif choice == '2':
            minimize(dfa)
        elif choice == '3':
            dfa.display_ascii_dfa()
        elif choice == '4':
            states, alphabet, transition_function, start_state, accept_states = get_user_input()
            dfa = DFA(states, alphabet, transition_function, start_state, accept_states)
        elif choice == '5':
            visualize_dfa(
                states=dfa.states,
                alphabet=dfa.alphabet,
                transition_function=dfa.transition_function,
                start_state=dfa.start_state,
                accept_states=dfa.accept_states,
                filename="dfa_graph"
            )
        elif choice == '6':
            edit_dfa(dfa)
        elif choice == '7':
            print("Program sonlandırılıyor...")
            break
        else:
            print("Geçersiz seçim! Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()

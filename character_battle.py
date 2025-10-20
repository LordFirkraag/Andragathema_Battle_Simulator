import tkinter as tk
from tkinter import ttk
import random

class Character:
    def __init__(self, name, stats, indomitable=False, overexertion=True, never_stunned=False, is_minion=False):
        self.name = name
        self.base_stats = stats.copy()
        self.current_stats = stats.copy()
        self.wounds = 0
        self.fatigue = 0
        self.indomitable = indomitable
        self.overexertion = overexertion
        self.never_stunned = never_stunned
        self.is_minion = is_minion
        self.stunned_turns = 0  # Πόσες σειρές χάνει
        self.defense_penalty = 0  # Ποινή στην άμυνα
        self.outnumbered_penalty = 0  # Ποινή από πολλαπλούς εχθρούς

    def get_effective_stat(self, stat_name):
        """Υπολογίζει το τελικό stat με penalties"""
        base_value = self.current_stats[stat_name]

        # Ποινή άμυνας από υπερπροσπάθεια
        if stat_name == "Άμυνα" and self.defense_penalty < 0:
            return self.defense_penalty  # Αγνοεί τον συντελεστή

        # Penalty από λαβωματιές για άμυνα/αντοχή
        if stat_name in ["Άμυνα", "Αντοχή"]:
            base_value -= self.wounds

        # Penalty από πολλαπλούς εχθρούς για άμυνα
        if stat_name == "Άμυνα":
            base_value -= self.outnumbered_penalty

        # Penalty από κόπωση για επίθεση/ζημιά
        if stat_name in ["Επίθεση", "Ζημιά"]:
            # Αν είναι ακατάβλητος και έχει μόνο 1 κόπωση, δεν παίρνει penalty
            if self.indomitable and self.fatigue == 1:
                pass  # Καμία penalty
            else:
                base_value -= self.fatigue

        return base_value

    def add_wound(self, apply_fatigue=True):
        self.wounds += 1
        if apply_fatigue:
            self.add_fatigue()

    def add_fatigue(self):
        if self.never_stunned:
            # Ποτέ εμβρόντητος: δεν παίρνει ποτέ κόπωση ούτε χάνει σειρές
            return
        elif not self.overexertion:
            # Χωρίς υπερπροσπάθεια: δεν παίρνει κόπωση αλλά χάνει σειρές
            self.stunned_turns = 2  # Χάνει τις επόμενες 2 σειρές
            self.defense_penalty = -2  # Άμυνα -2 (αγνοώντας τον συντελεστή)
        else:
            self.fatigue += 1

    def is_stunned(self):
        return self.stunned_turns > 0

    def reduce_stun(self):
        if self.stunned_turns > 0:
            self.stunned_turns -= 1
            if self.stunned_turns == 0:
                self.defense_penalty = 0  # Αφαίρεση penalty όταν τελειώνει το stun

    def is_defeated(self):
        return self.wounds >= 2

class CharacterBattleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Μάχη Χαρακτήρων")
        self.root.geometry("800x600")

        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

        # Character labels
        ttk.Label(main_frame, text="Χαρακτήρας 1", font=("Arial", 14, "bold")).grid(row=0, column=1, pady=10)
        ttk.Label(main_frame, text="Χαρακτήρας 2", font=("Arial", 14, "bold")).grid(row=0, column=2, pady=10)

        # Stats labels and entries
        self.stats = ["Πρωτοβουλία", "Επίθεση", "Ζημιά", "Άμυνα", "Αντοχή"]
        self.char1_entries = {}
        self.char2_entries = {}
        self.char1_indomitable = tk.BooleanVar()
        self.char2_indomitable = tk.BooleanVar()
        self.char1_overexertion = tk.BooleanVar(value=True)  # Checked by default
        self.char2_overexertion = tk.BooleanVar(value=True)  # Checked by default
        self.char1_never_stunned = tk.BooleanVar()
        self.char2_never_stunned = tk.BooleanVar()

        for i, stat in enumerate(self.stats):
            row = i + 1

            # Stat label
            ttk.Label(main_frame, text=stat).grid(row=row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

            # Character 1 entry
            entry1 = ttk.Entry(main_frame, width=10)
            entry1.grid(row=row, column=1, padx=10, pady=5)
            self.char1_entries[stat] = entry1

            # Character 2 entry
            entry2 = ttk.Entry(main_frame, width=10)
            entry2.grid(row=row, column=2, padx=10, pady=5)
            self.char2_entries[stat] = entry2

        # Ακατάβλητος checkboxes
        indomitable_row = len(self.stats) + 1
        ttk.Label(main_frame, text="Ακατάβλητος").grid(row=indomitable_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        checkbox1 = ttk.Checkbutton(main_frame, variable=self.char1_indomitable)
        checkbox1.grid(row=indomitable_row, column=1, padx=10, pady=5)

        checkbox2 = ttk.Checkbutton(main_frame, variable=self.char2_indomitable)
        checkbox2.grid(row=indomitable_row, column=2, padx=10, pady=5)

        # Υπερπροσπάθεια checkboxes
        overexertion_row = len(self.stats) + 2
        ttk.Label(main_frame, text="Υπερπροσπάθεια").grid(row=overexertion_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        overexertion_checkbox1 = ttk.Checkbutton(main_frame, variable=self.char1_overexertion)
        overexertion_checkbox1.grid(row=overexertion_row, column=1, padx=10, pady=5)

        overexertion_checkbox2 = ttk.Checkbutton(main_frame, variable=self.char2_overexertion)
        overexertion_checkbox2.grid(row=overexertion_row, column=2, padx=10, pady=5)

        # Ποτέ εμβρόντητος checkboxes
        never_stunned_row = len(self.stats) + 3
        ttk.Label(main_frame, text="Ποτέ εμβρόντητος").grid(row=never_stunned_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        never_stunned_checkbox1 = ttk.Checkbutton(main_frame, variable=self.char1_never_stunned)
        never_stunned_checkbox1.grid(row=never_stunned_row, column=1, padx=10, pady=5)

        never_stunned_checkbox2 = ttk.Checkbutton(main_frame, variable=self.char2_never_stunned)
        never_stunned_checkbox2.grid(row=never_stunned_row, column=2, padx=10, pady=5)

        # Αριθμός χαρακτήρων 2
        number_row = len(self.stats) + 4
        ttk.Label(main_frame, text="Αριθμός").grid(row=number_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        # Empty space for Character 1 column
        ttk.Label(main_frame, text="").grid(row=number_row, column=1, padx=10, pady=5)

        # Number entry for Character 2
        self.char2_number_entry = ttk.Entry(main_frame, width=10)
        self.char2_number_entry.grid(row=number_row, column=2, padx=10, pady=5)
        self.char2_number_entry.insert(0, "1")  # Default value

        # Πόσοι μάχονται
        engaged_row = len(self.stats) + 5
        ttk.Label(main_frame, text="Πόσοι μάχονται").grid(row=engaged_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        # Empty space for Character 1 column
        ttk.Label(main_frame, text="").grid(row=engaged_row, column=1, padx=10, pady=5)

        # Engaged entry for Character 2
        self.char2_engaged_entry = ttk.Entry(main_frame, width=10)
        self.char2_engaged_entry.grid(row=engaged_row, column=2, padx=10, pady=5)
        self.char2_engaged_entry.insert(0, "1")  # Default value

        # Τσιράκι checkbox
        minion_row = len(self.stats) + 6
        ttk.Label(main_frame, text="Τσιράκι").grid(row=minion_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        # Empty space for Character 1 column
        ttk.Label(main_frame, text="").grid(row=minion_row, column=1, padx=10, pady=5)

        # Minion checkbox for Character 2
        self.char2_minion = tk.BooleanVar()
        minion_checkbox2 = ttk.Checkbutton(main_frame, variable=self.char2_minion)
        minion_checkbox2.grid(row=minion_row, column=2, padx=10, pady=5)

        # Battle buttons
        single_battle_btn = ttk.Button(main_frame, text="Μονομαχία", command=self.single_battle)
        single_battle_btn.grid(row=len(self.stats) + 7, column=0, columnspan=3, pady=10)

        thousand_battles_btn = ttk.Button(main_frame, text="1000 μάχες", command=self.thousand_battles)
        thousand_battles_btn.grid(row=len(self.stats) + 8, column=0, columnspan=3, pady=10)

        hundred_thousand_battles_btn = ttk.Button(main_frame, text="100000 μάχες", command=self.hundred_thousand_battles)
        hundred_thousand_battles_btn.grid(row=len(self.stats) + 9, column=0, columnspan=3, pady=10)

        # Result text area
        result_frame = ttk.LabelFrame(main_frame, text="Αποτέλεσμα", padding="10")
        result_frame.grid(row=len(self.stats) + 10, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        self.result_text = tk.Text(result_frame, height=10, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)

        # Enable text selection and copying
        self.result_text.bind("<Control-a>", self.select_all)
        self.result_text.bind("<Control-c>", self.copy_text)

        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(len(self.stats) + 10, weight=1)

    def select_all(self, event):
        """Select all text in result area"""
        self.result_text.tag_add(tk.SEL, "1.0", tk.END)
        return "break"

    def copy_text(self, event):
        """Copy selected text to clipboard"""
        try:
            text = self.result_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
        except tk.TclError:
            pass  # No selection
        return "break"

    def get_character_stats(self, entries):
        """Συλλέγει τα στατιστικά από τα entry fields"""
        stats = {}
        for stat, entry in entries.items():
            try:
                value = int(entry.get()) if entry.get() else 0
                stats[stat] = value
            except ValueError:
                stats[stat] = 0
        return stats

    def get_char2_number(self):
        """Παίρνει τον αριθμό των χαρακτήρων 2 (τουλάχιστον 1)"""
        try:
            number = int(self.char2_number_entry.get()) if self.char2_number_entry.get() else 1
            return max(1, number)  # Τουλάχιστον 1
        except ValueError:
            return 1

    def get_char2_engaged(self):
        """Παίρνει τον αριθμό των χαρακτήρων 2 που μάχονται ταυτόχρονα (τουλάχιστον 1)"""
        try:
            engaged = int(self.char2_engaged_entry.get()) if self.char2_engaged_entry.get() else 1
            return max(1, engaged)
        except ValueError:
            return 1

    def roll_d20(self, modifier=0):
        """Ρίχνει d20 με modifier"""
        dice_result = random.randint(1, 20)
        total = dice_result + modifier
        return dice_result, modifier, total

    def format_dice_roll(self, stat_name, dice_result, modifier, total):
        """Μορφοποιεί την εμφάνιση της ζαριάς"""
        if modifier >= 0:
            return f"{stat_name} d20({dice_result}) + {modifier} = {total}"
        else:
            return f"{stat_name} d20({dice_result}) - {abs(modifier)} = {total}"

    def initiative_phase(self, char1, char2):
        """Καθορίζει ποιος παίζει πρώτος"""
        result = ""

        while True:
            dice1, mod1, init1 = self.roll_d20(char1.get_effective_stat("Πρωτοβουλία"))
            dice2, mod2, init2 = self.roll_d20(char2.get_effective_stat("Πρωτοβουλία"))

            init1_display = self.format_dice_roll("Πρωτοβουλία", dice1, mod1, init1)
            init2_display = self.format_dice_roll("Πρωτοβουλία", dice2, mod2, init2)

            result += f"{char1.name}: {init1_display}\n"
            result += f"{char2.name}: {init2_display}\n"

            if init1 > init2:
                result += f"{char1.name} παίζει πρώτος!\n\n"
                return char1, char2, result
            elif init2 > init1:
                result += f"{char2.name} παίζει πρώτος!\n\n"
                return char2, char1, result
            else:
                result += "Ισοβαθμία! Ξαναρίχνουμε...\n"

    def attack_turn(self, attacker, defender, attack_type="Επίθεση"):
        """Εκτελεί μια επίθεση"""
        result = f"--- {attack_type} {attacker.name} ---\n"

        # Ζαριά επίθεσης vs άμυνας
        att_dice, att_mod, attack_roll = self.roll_d20(attacker.get_effective_stat("Επίθεση"))
        def_dice, def_mod, defense_roll = self.roll_d20(defender.get_effective_stat("Άμυνα"))

        attack_display = self.format_dice_roll("Επίθεση", att_dice, att_mod, attack_roll)
        defense_display = self.format_dice_roll("Άμυνα", def_dice, def_mod, defense_roll)

        result += f"{attack_display} vs {defense_display}\n"

        if attack_roll >= defense_roll:  # Ισοβαθμία κερδίζει επιτιθέμενος
            result += "Επιτυχής επίθεση! Ρίχνουμε ζημιά...\n"

            # Ζαριά ζημιάς vs αντοχής
            dmg_dice, dmg_mod, damage_roll = self.roll_d20(attacker.get_effective_stat("Ζημιά"))
            end_dice, end_mod, endurance_roll = self.roll_d20(defender.get_effective_stat("Αντοχή"))

            damage_display = self.format_dice_roll("Ζημιά", dmg_dice, dmg_mod, damage_roll)
            endurance_display = self.format_dice_roll("Αντοχή", end_dice, end_mod, endurance_roll)

            result += f"{damage_display} vs {endurance_display}\n"

            damage_diff = damage_roll - endurance_roll
            had_two_wounds = defender.wounds >= 2  # Ελέγχουμε ΠΡΙΝ την ζημιά

            # Τσιράκι: πεθαίνει με οποιαδήποτε επιτυχή ζημιά
            if defender.is_minion and damage_diff >= 0:
                result += f"Τσιράκι! (+{damage_diff}) Ο {defender.name} νικιέται!\n"
                defender.wounds = 10  # Σημάδι θανάτου
                return result, True  # Νίκη
            elif damage_diff >= 10:
                result += f"ΘΑΝΑΤΗΦΟΡΟ ΧΤΥΠΗΜΑ! (+{damage_diff}) Ο {defender.name} νικιέται!\n"
                defender.wounds = 10  # Σημάδι θανάτου
                return result, True  # Νίκη
            elif damage_diff >= 5:
                result += f"Σοβαρή ζημιά! (+{damage_diff}) 2 λαβωματιές, 1 κόπωση\n"
                defender.wounds += 2
                defender.add_fatigue()
            elif damage_diff >= 0:  # Ισοβαθμία ή +1 έως +4
                result += f"Ζημιά! (+{damage_diff}) 1 λαβωματιά, 1 κόπωση\n"
                defender.add_wound()  # Η add_wound καλεί ήδη την add_fatigue
            else:
                result += f"Αντέχει τη ζημιά! ({damage_diff})\n"

            # Έλεγχος αν ο defender είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά (μόνο αν δεν είναι τσιράκι)
            if not defender.is_minion and had_two_wounds and damage_diff >= 0:
                result += f"Ο {defender.name} έχει πάρει πολλές λαβωματιές και νικιέται!\n"
                defender.wounds = 10  # Σημάδι θανάτου
                return result, True

        else:
            result += "Αποτυχημένη επίθεση!\n"

        result += f"Κατάσταση {defender.name}: {defender.wounds} λαβωματιές, {defender.fatigue} κόπωση\n\n"
        return result, False

    def simulate_battle_silent(self, char1_stats, char2_stats, char1_indomitable, char2_indomitable, char1_overexertion, char2_overexertion, char1_never_stunned, char2_never_stunned, char2_number=1, char2_engaged=1, char2_minion=False):
        """Προσομοιώνει μια μάχη χωρίς output - επιστρέφει (νικητής, γύροι)"""
        # Δημιουργία χαρακτήρων
        char1 = Character("Χαρακτήρας 1", char1_stats, char1_indomitable, char1_overexertion, char1_never_stunned)

        if char2_number == 1:
            # Κανονική μάχη 1v1
            char2 = Character("Χαρακτήρας 2", char2_stats, char2_indomitable, char2_overexertion, char2_never_stunned, char2_minion)
            winner, turns = self.simulate_1v1_silent(char1, char2)
            rounds = max(1, turns // 4)  # Μετατροπή turns σε γύρους
            return winner, rounds
        else:
            # Μάχη 1 vs πολλοί
            char2_list = []
            for i in range(char2_number):
                char_name = f"Χαρακτήρας 2.{i+1}"
                char2_opponent = Character(char_name, char2_stats, char2_indomitable, char2_overexertion, char2_never_stunned, char2_minion)
                char2_list.append(char2_opponent)

            return self.simulate_1vMany_silent(char1, char2_list, char2_engaged)

    def simulate_1v1_silent(self, char1, char2):
        # Φάση πρωτοβουλίας
        first_player, second_player = self.initiative_phase_silent(char1, char2)

        # Μάχη
        turn_count = 0
        current_attacker = first_player
        current_defender = second_player
        is_first_turn = True
        current_player_attacks = 0

        while turn_count < 400:  # Safety limit
            turn_count += 1

            # Έλεγχος αν ο τρέχων επιτιθέμενος είναι stunned
            if current_attacker.is_stunned():
                current_attacker.reduce_stun()
                # Αλλάζουμε αμέσως παίκτη
                if is_first_turn:
                    current_attacker, current_defender = current_defender, current_attacker
                    current_player_attacks = 0
                    is_first_turn = False
                else:
                    if current_player_attacks >= 2:
                        current_attacker, current_defender = current_defender, current_attacker
                        current_player_attacks = 0
                    else:
                        current_player_attacks += 1
                continue

            current_player_attacks += 1

            # Εκτέλεση επίθεσης
            battle_ended = self.attack_turn_silent(current_attacker, current_defender)

            if battle_ended:
                if current_attacker.name == "Χαρακτήρας 1":
                    return 1, turn_count
                else:
                    return 2, turn_count

            # Καθορισμός επόμενου παίκτη
            if is_first_turn:
                # Η πρώτη κίνηση τελείωσε, αλλάζουμε παίκτη
                current_attacker, current_defender = current_defender, current_attacker
                current_player_attacks = 0
                is_first_turn = False
            else:
                # Όλες οι άλλες κινήσεις είναι διπλές
                if current_player_attacks >= 2:
                    # Ο παίκτης τελείωσε τις 2 επιθέσεις του, αλλάζουμε
                    current_attacker, current_defender = current_defender, current_attacker
                    current_player_attacks = 0

        return 0, turn_count  # Ισοπαλία

    def simulate_1vMany_silent(self, char1, char2_list, char2_engaged):
        """Προσομοιώνει μάχη 1 vs πολλοί αντιπάλους χωρίς output με reserves - επιστρέφει (νικητής, γύροι)"""
        import random

        # Φάση πρωτοβουλίας
        _, _, char1_initiative = self.roll_d20(char1.get_effective_stat("Πρωτοβουλία"))
        _, _, opponents_initiative = self.roll_d20(char2_list[0].get_effective_stat("Πρωτοβουλία"))

        char1_wins_init = char1_initiative >= opponents_initiative
        round_count = 0

        # Προσομοίωση μάχης
        while round_count < 200:  # Safety limit
            round_count += 1

            # Έλεγχος αν υπάρχουν ζωντανοί εχθροί
            alive_opponents = [char for char in char2_list if char.wounds < 10]
            if not alive_opponents:
                return 1, round_count  # Char1 νικάει

            if char1.wounds >= 10:
                return 2, round_count  # Char1 χάνει

            # Χωρίζουμε σε engaged και reserves
            engaged_enemies = alive_opponents[:char2_engaged]

            # Ενημέρωση penalty για πολλαπλούς εχθρούς - βασισμένο σε engaged
            # -1 για κάθε εχθρό μετά τον πρώτο, μέχρι -5
            num_enemies = len(engaged_enemies)
            char1.outnumbered_penalty = min(num_enemies - 1, 5)

            # Char1 επιτίθεται σε 1 εχθρό από τους engaged → ο στόχος αντεπιτίθεται
            if engaged_enemies:
                target = random.choice(engaged_enemies)
                # Επίθεση char1
                char1_killed_target = self.attack_turn_silent(char1, target)
                # Αντεπίθεση του στόχου (αν δεν πέθανε)
                if not char1_killed_target and target.wounds < 10:
                    target_killed_char1 = self.attack_turn_silent(target, char1)
                    if target_killed_char1:
                        return 2, round_count

            # Όλοι οι ΥΠΟΛΟΙΠΟΙ engaged εχθροί επιτίθενται → char1 αντεπιτίθεται
            current_alive = [char for char in char2_list if char.wounds < 10]
            current_engaged = current_alive[:char2_engaged]
            for enemy in current_engaged:
                if enemy == target:
                    continue  # Ο στόχος ήδη αντεπιτέθηκε

                if char1.wounds >= 10:
                    return 2, round_count

                # Επίθεση εχθρού
                enemy_killed_char1 = self.attack_turn_silent(enemy, char1)
                if enemy_killed_char1:
                    return 2, round_count

                # Αντεπίθεση char1 (αν δεν πέθανε και δεν είναι stunned)
                if char1.wounds < 10 and not char1.is_stunned():
                    self.attack_turn_silent(char1, enemy)

        return 0, round_count  # Ισοπαλία

    def initiative_phase_silent(self, char1, char2):
        """Καθορίζει ποιος παίζει πρώτος χωρίς output"""
        while True:
            _, _, init1 = self.roll_d20(char1.get_effective_stat("Πρωτοβουλία"))
            _, _, init2 = self.roll_d20(char2.get_effective_stat("Πρωτοβουλία"))

            if init1 > init2:
                return char1, char2
            elif init2 > init1:
                return char2, char1
            # Ισοβαθμία - ξαναρίχνουμε

    def attack_turn_silent(self, attacker, defender):
        """Εκτελεί μια επίθεση χωρίς output - επιστρέφει True αν τελειώνει η μάχη"""
        # Ζαριά επίθεσης vs άμυνας
        _, _, attack_roll = self.roll_d20(attacker.get_effective_stat("Επίθεση"))
        _, _, defense_roll = self.roll_d20(defender.get_effective_stat("Άμυνα"))

        if attack_roll >= defense_roll:
            # Ζαριά ζημιάς vs αντοχής
            _, _, damage_roll = self.roll_d20(attacker.get_effective_stat("Ζημιά"))
            _, _, endurance_roll = self.roll_d20(defender.get_effective_stat("Αντοχή"))

            damage_diff = damage_roll - endurance_roll
            had_two_wounds = defender.wounds >= 2  # Ελέγχουμε ΠΡΙΝ την ζημιά

            # Τσιράκι: πεθαίνει με οποιαδήποτε επιτυχή ζημιά
            if defender.is_minion and damage_diff >= 0:
                defender.wounds = 10  # Σημάδι θανάτου
                return True
            elif damage_diff >= 10:
                defender.wounds = 10  # Σημάδι θανάτου
                return True  # Θανατηφόρος χτύπημα
            elif damage_diff >= 5:
                defender.wounds += 2
                defender.add_fatigue()
            elif damage_diff >= 0:
                defender.add_wound()  # Η add_wound καλεί ήδη την add_fatigue

            # Έλεγχος αν ο defender είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά (μόνο αν δεν είναι τσιράκι)
            if not defender.is_minion and had_two_wounds and damage_diff >= 0:
                defender.wounds = 10  # Σημάδι θανάτου
                return True

        return False

    def thousand_battles(self):
        """Εκτελεί 1000 μάχες και εμφανίζει στατιστικά"""
        char1_stats = self.get_character_stats(self.char1_entries)
        char2_stats = self.get_character_stats(self.char2_entries)
        char2_number = self.get_char2_number()
        char2_engaged = self.get_char2_engaged()

        char1_wins = 0
        char2_wins = 0
        draws = 0
        total_rounds = 0
        min_rounds = float('inf')
        max_rounds = 0

        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        if char2_number == 1:
            self.result_text.insert(tk.END, "Εκτελούνται 1000 μάχες...\n\n")
        else:
            self.result_text.insert(tk.END, f"Εκτελούνται 1000 μάχες (1 vs {char2_number}, max {char2_engaged} engaged)...\n\n")
        self.root.update()

        for i in range(1000):
            winner, rounds = self.simulate_battle_silent(
                char1_stats, char2_stats,
                self.char1_indomitable.get(), self.char2_indomitable.get(),
                self.char1_overexertion.get(), self.char2_overexertion.get(),
                self.char1_never_stunned.get(), self.char2_never_stunned.get(),
                char2_number, char2_engaged, self.char2_minion.get()
            )
            total_rounds += rounds
            min_rounds = min(min_rounds, rounds)
            max_rounds = max(max_rounds, rounds)
            if winner == 1:
                char1_wins += 1
            elif winner == 2:
                char2_wins += 1
            else:
                draws += 1

        # Αποτελέσματα
        avg_rounds = total_rounds / 1000
        result = f"=== ΑΠΟΤΕΛΕΣΜΑΤΑ 1000 ΜΑΧΩΝ ===\n"
        if char2_number > 1:
            result += f"(Χαρακτήρας 1 εναντίον {char2_number} αντιπάλων)\n"
        result += "\n"
        result += f"Χαρακτήρας 1: {char1_wins} νίκες ({char1_wins/10:.1f}%)\n"
        if char2_number == 1:
            result += f"Χαρακτήρας 2: {char2_wins} νίκες ({char2_wins/10:.1f}%)\n"
        else:
            result += f"Οι αντίπαλοι: {char2_wins} νίκες ({char2_wins/10:.1f}%)\n"
        if draws > 0:
            result += f"Ισοπαλίες: {draws} ({draws/10:.1f}%)\n"
        result += f"Μέσος όρος γύρων ανά μάχη: {avg_rounds:.2f} (εύρος: {min_rounds}-{max_rounds})\n\n"

        if char1_wins > char2_wins:
            result += f"🏆 Συνολικός νικητής: Χαρακτήρας 1! 🏆\n"
        elif char2_wins > char1_wins:
            if char2_number == 1:
                result += f"🏆 Συνολικός νικητής: Χαρακτήρας 2! 🏆\n"
            else:
                result += f"🏆 Συνολικοί νικητές: Οι αντίπαλοι! 🏆\n"
        else:
            result += "🤝 Ισοπαλία! 🤝\n"

        self.result_text.insert(tk.END, result)

    def hundred_thousand_battles(self):
        """Εκτελεί 100000 μάχες και εμφανίζει στατιστικά"""
        char1_stats = self.get_character_stats(self.char1_entries)
        char2_stats = self.get_character_stats(self.char2_entries)
        char2_number = self.get_char2_number()
        char2_engaged = self.get_char2_engaged()

        char1_wins = 0
        char2_wins = 0
        draws = 0
        total_rounds = 0
        min_rounds = float('inf')
        max_rounds = 0

        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        if char2_number == 1:
            self.result_text.insert(tk.END, "Εκτελούνται 100000 μάχες...\n\n")
        else:
            self.result_text.insert(tk.END, f"Εκτελούνται 100000 μάχες (1 vs {char2_number}, max {char2_engaged} engaged)...\n\n")
        self.root.update()

        for i in range(100000):
            winner, rounds = self.simulate_battle_silent(
                char1_stats, char2_stats,
                self.char1_indomitable.get(), self.char2_indomitable.get(),
                self.char1_overexertion.get(), self.char2_overexertion.get(),
                self.char1_never_stunned.get(), self.char2_never_stunned.get(),
                char2_number, char2_engaged, self.char2_minion.get()
            )
            total_rounds += rounds
            min_rounds = min(min_rounds, rounds)
            max_rounds = max(max_rounds, rounds)
            if winner == 1:
                char1_wins += 1
            elif winner == 2:
                char2_wins += 1
            else:
                draws += 1

        # Αποτελέσματα
        avg_rounds = total_rounds / 100000
        result = f"=== ΑΠΟΤΕΛΕΣΜΑΤΑ 100000 ΜΑΧΩΝ ===\n"
        if char2_number > 1:
            result += f"(Χαρακτήρας 1 εναντίον {char2_number} αντιπάλων)\n"
        result += "\n"
        result += f"Χαρακτήρας 1: {char1_wins} νίκες ({char1_wins/1000:.1f}%)\n"
        if char2_number == 1:
            result += f"Χαρακτήρας 2: {char2_wins} νίκες ({char2_wins/1000:.1f}%)\n"
        else:
            result += f"Οι αντίπαλοι: {char2_wins} νίκες ({char2_wins/1000:.1f}%)\n"
        if draws > 0:
            result += f"Ισοπαλίες: {draws} ({draws/1000:.1f}%)\n"
        result += f"Μέσος όρος γύρων ανά μάχη: {avg_rounds:.2f} (εύρος: {min_rounds}-{max_rounds})\n\n"

        if char1_wins > char2_wins:
            result += f"🏆 Συνολικός νικητής: Χαρακτήρας 1! 🏆\n"
        elif char2_wins > char1_wins:
            if char2_number == 1:
                result += f"🏆 Συνολικός νικητής: Χαρακτήρας 2! 🏆\n"
            else:
                result += f"🏆 Συνολικοί νικητές: Οι αντίπαλοι! 🏆\n"
        else:
            result += "🤝 Ισοπαλία! 🤝\n"

        self.result_text.insert(tk.END, result)

    def single_battle(self):
        """Εκτελεί μια αναλυτική μάχη"""
        char1_stats = self.get_character_stats(self.char1_entries)
        char2_stats = self.get_character_stats(self.char2_entries)
        char2_number = self.get_char2_number()

        # Clear previous results
        self.result_text.delete(1.0, tk.END)

        # Δημιουργία χαρακτήρων
        char1 = Character("Χαρακτήρας 1", char1_stats, self.char1_indomitable.get(), self.char1_overexertion.get(), self.char1_never_stunned.get())

        # Δημιουργία πολλαπλών χαρακτήρων 2
        char2_list = []
        for i in range(char2_number):
            char2 = Character(f"Χαρακτήρας 2.{i+1}", char2_stats, self.char2_indomitable.get(), self.char2_overexertion.get(), self.char2_never_stunned.get(), self.char2_minion.get())
            char2_list.append(char2)

        if char2_number == 1:
            # Κανονική μάχη 1 vs 1
            result = self.single_battle_1v1(char1, char2_list[0])
        else:
            # Μάχη 1 vs πολλοί
            result = self.single_battle_1vMany(char1, char2_list)

        self.result_text.insert(tk.END, result)

    def single_battle_1v1(self, char1, char2):
        """Κανονική μάχη 1 vs 1"""
        result = "=== ΜΑΧΗ ΧΑΡΑΚΤΗΡΩΝ ===\n\n"

        # Φάση πρωτοβουλίας
        first_player, second_player, init_result = self.initiative_phase(char1, char2)
        result += init_result

        # Μάχη με το σύστημα σειράς: Μόνο η πρώτη κίνηση είναι μονή, όλες οι άλλες διπλές
        turn_count = 0
        current_attacker = first_player
        current_defender = second_player
        is_first_turn = True  # Η πρώτη κίνηση είναι μονή
        current_player_attacks = 0  # Πόσες φορές έχει επιτεθεί ο τρέχων παίκτης

        while True:
            turn_count += 1

            # Έλεγχος αν ο τρέχων επιτιθέμενος είναι stunned
            if current_attacker.is_stunned():
                result += f"--- {current_attacker.name} χάνει τη σειρά του (stunned) ---\n"
                current_attacker.reduce_stun()
                # Αλλάζουμε αμέσως παίκτη
                if is_first_turn:
                    current_attacker, current_defender = current_defender, current_attacker
                    current_player_attacks = 0
                    is_first_turn = False
                else:
                    if current_player_attacks >= 2:
                        current_attacker, current_defender = current_defender, current_attacker
                        current_player_attacks = 0
                    else:
                        current_player_attacks += 1
                continue

            current_player_attacks += 1

            # Εκτέλεση επίθεσης
            if is_first_turn:
                attack_type = "Επίθεση"
            elif current_player_attacks == 1:
                attack_type = "Αντεπίθεση"
            else:
                attack_type = "Επίθεση"

            turn_result, battle_ended = self.attack_turn(current_attacker, current_defender, attack_type)
            result += turn_result

            if battle_ended:
                result += f"\n🏆 ΝΙΚΗΤΗΣ: {current_attacker.name}! 🏆\n"
                break

            # Καθορισμός επόμενου παίκτη
            if is_first_turn:
                # Η πρώτη κίνηση τελείωσε, αλλάζουμε παίκτη
                current_attacker, current_defender = current_defender, current_attacker
                current_player_attacks = 0
                is_first_turn = False
            else:
                # Όλες οι άλλες κινήσεις είναι διπλές
                if current_player_attacks >= 2:
                    # Ο παίκτης τελείωσε τις 2 επιθέσεις του, αλλάζουμε
                    current_attacker, current_defender = current_defender, current_attacker
                    current_player_attacks = 0

            # Έλεγχος για άπειρο loop (safety)
            if turn_count > 100:
                result += "\nΗ μάχη διαρκεί πολύ! Ισοπαλία.\n"
                break

        return result

    def single_battle_1vMany(self, char1, char2_list):
        """Μάχη 1 vs πολλοί με turn-based σύστημα"""
        result = f"=== ΜΑΧΗ ΧΑΡΑΚΤΗΡΩΝ - 1 vs {len(char2_list)} ===\n\n"

        # Φάση πρωτοβουλίας - μόνο ο char1 ρίχνει
        init1_dice, init1_mod, init1_total = self.roll_d20(char1.get_effective_stat("Πρωτοβουλία"))
        init1_display = self.format_dice_roll("Πρωτοβουλία", init1_dice, init1_mod, init1_total)
        result += f"{char1.name}: {init1_display}\n"

        # Όλοι οι χαρακτήρες 2 ρίχνουν πρωτοβουλία
        enemies_init = []
        for i, char2 in enumerate(char2_list):
            init2_dice, init2_mod, init2_total = self.roll_d20(char2.get_effective_stat("Πρωτοβουλία"))
            init2_display = self.format_dice_roll("Πρωτοβουλία", init2_dice, init2_mod, init2_total)
            result += f"{char2.name}: {init2_display}\n"
            enemies_init.append((char2, init2_total))

        # Καθορισμός σειράς
        char1_wins_init = True
        for char2, init_total in enemies_init:
            if init1_total <= init_total:
                char1_wins_init = False
                break

        if char1_wins_init:
            result += f"\n{char1.name} κερδίζει την πρωτοβουλία!\n\n"
        else:
            result += f"\nΟι αντίπαλοι κερδίζουν την πρωτοβουλία!\n\n"

        # Μετρητής γύρων
        round_count = 0
        turn_count = 0

        while turn_count < 200:  # Safety limit
            # Νέος γύρος: όταν έχουν παίξει όλοι από μια φορά
            if turn_count % (len(char2_list) + 1) == 0:
                round_count += 1
                result += f"=== ΓΥΡΟΣ {round_count} ===\n"

                # Ενημέρωση penalty για πολλαπλούς εχθρούς
                alive_opponents = [c for c in char2_list if not self.is_dead(c)]
                num_enemies = len(alive_opponents)
                char1.outnumbered_penalty = min(num_enemies - 1, 5)
                if char1.outnumbered_penalty > 0:
                    result += f"({char1.name} έχει -{char1.outnumbered_penalty} Άμυνα λόγω {num_enemies} εχθρών)\n"

            turn_count += 1

            # Καθορισμός ποιος παίζει
            if char1_wins_init:
                # Char1 παίζει πρώτος
                if (turn_count - 1) % (len(char2_list) + 1) == 0:
                    # Σειρά του char1
                    result += self.char1_attack_phase(char1, char2_list)
                    if self.check_enemies_defeated(char2_list):
                        result += f"\n🏆 ΝΙΚΗΤΗΣ: {char1.name}! 🏆\n"
                        result += f"Συνολικοί γύροι: {round_count}\n"
                        break
                else:
                    # Σειρά εχθρού
                    enemy_index = ((turn_count - 2) % len(char2_list))
                    if enemy_index < len([c for c in char2_list if not self.is_dead(c)]):
                        living_enemies = [c for c in char2_list if not self.is_dead(c)]
                        if enemy_index < len(living_enemies):
                            attacker = living_enemies[enemy_index]
                            result += self.enemy_attack_phase(attacker, char1)
                            if self.is_dead(char1):
                                result += f"\n🏆 ΝΙΚΗΤΕΣ: Οι αντίπαλοι! 🏆\n"
                                result += f"Συνολικοί γύροι: {round_count}\n"
                                break
            else:
                # Εχθροί παίζουν πρώτοι
                if (turn_count - 1) % (len(char2_list) + 1) < len(char2_list):
                    # Σειρά εχθρού
                    enemy_index = (turn_count - 1) % (len(char2_list) + 1)
                    living_enemies = [c for c in char2_list if not self.is_dead(c)]
                    if enemy_index < len(living_enemies):
                        attacker = living_enemies[enemy_index]
                        result += self.enemy_attack_phase(attacker, char1)
                        if self.is_dead(char1):
                            result += f"\n🏆 ΝΙΚΗΤΕΣ: Οι αντίπαλοι! 🏆\n"
                            result += f"Συνολικοί γύροι: {round_count}\n"
                            break
                else:
                    # Σειρά του char1
                    result += self.char1_attack_phase(char1, char2_list)
                    if self.check_enemies_defeated(char2_list):
                        result += f"\n🏆 ΝΙΚΗΤΗΣ: {char1.name}! 🏆\n"
                        result += f"Συνολικοί γύροι: {round_count}\n"
                        break

        if turn_count >= 200:
            result += "\nΗ μάχη διαρκεί πολύ! Ισοπαλία.\n"
            result += f"Συνολικοί γύροι: {round_count}\n"

        return result

    def char1_attack_phase(self, char1, char2_list):
        """Φάση επίθεσης του χαρακτήρα 1 με αντεπίθεση του στόχου"""
        result = f"\n--- {char1.name} επιτίθεται ---\n"

        # Επιλογή στόχου: προτεραιότητα σε όποιον έχει >1 λαβωματιά
        target = self.select_target(char2_list)
        if target is None:
            result += "Δεν υπάρχουν ζωντανοί εχθροί!\n"
            return result

        turn_result, battle_ended = self.attack_turn(char1, target, "Επίθεση")
        result += turn_result

        if battle_ended:
            return result

        # Αντεπίθεση του στόχου (αν είναι ακόμη ζωντανός)
        if not self.is_dead(target):
            result += f"\n--- {target.name} αντεπιτίθεται ---\n"
            counter_result, counter_ended = self.attack_turn(target, char1, "Αντεπίθεση")
            result += counter_result

        return result

    def enemy_attack_phase(self, attacker, char1):
        """Φάση επίθεσης εχθρού με αντεπίθεση"""
        result = f"\n--- {attacker.name} επιτίθεται ---\n"

        # Επίθεση εχθρού
        turn_result, battle_ended = self.attack_turn(attacker, char1, "Επίθεση")
        result += turn_result

        if battle_ended:
            return result

        # Αντεπίθεση του char1 (αν είναι ζωντανός)
        if not self.is_dead(char1):
            result += f"\n--- {char1.name} αντεπιτίθεται ---\n"
            counter_result, counter_ended = self.attack_turn(char1, attacker, "Αντεπίθεση")
            result += counter_result

        return result

    def select_target(self, char2_list):
        """Επιλέγει στόχο για τον char1"""
        living_enemies = [c for c in char2_list if not self.is_dead(c)]
        if not living_enemies:
            return None

        # Προτεραιότητα σε όποιον έχει >1 λαβωματιά
        wounded_enemies = [c for c in living_enemies if c.wounds > 1]
        if wounded_enemies:
            return wounded_enemies[0]  # Επιλέγει τον πρώτο με >1 λαβωματιά

        # Αλλιώς τυχαίος
        import random
        return random.choice(living_enemies)

    def check_enemies_defeated(self, char2_list):
        """Ελέγχει αν όλοι οι εχθροί νικήθηκαν"""
        return all(self.is_dead(c) for c in char2_list)

    def is_dead(self, character):
        """Ελέγχει αν ένας χαρακτήρας είναι νεκρός"""
        return character.wounds >= 10  # Χρησιμοποιώ 10 ως σημάδι θανάτου όπως στο alternative

def main():
    root = tk.Tk()
    app = CharacterBattleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
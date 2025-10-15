import tkinter as tk
from tkinter import ttk
import random
import re

class Character:
    def __init__(self, name, stats, surprised=False):
        self.name = name
        self.stats = stats.copy()
        self.current_hp = stats["Πόντοι αντοχής"]
        self.max_hp = stats["Πόντοι αντοχής"]
        self.surprised = surprised
        self.shields_used_this_round = 0

    def is_alive(self):
        return self.current_hp > 0

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0

    def reset_shields(self):
        """Reset shield counter at the start of each round"""
        self.shields_used_this_round = 0

class CharacterBattleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Μάχη Χαρακτήρων - Κρύπτες")
        self.root.geometry("800x700")

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
        self.stats = ["Πόντοι αντοχής", "Ζαριά μάχης", "Ζαριά ζημιάς", "Θωράκιση", "Ασπίδες/γύρο", "Αριθμός επιθέσεων"]
        self.char1_entries = {}
        self.char2_entries = {}

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

        # Αιφνιδιασμός checkboxes
        surprised_row = len(self.stats) + 1
        ttk.Label(main_frame, text="Αιφνιδιασμός").grid(row=surprised_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        self.char1_surprised = tk.BooleanVar()
        surprised_checkbox1 = ttk.Checkbutton(main_frame, variable=self.char1_surprised)
        surprised_checkbox1.grid(row=surprised_row, column=1, padx=10, pady=5)

        self.char2_surprised = tk.BooleanVar()
        surprised_checkbox2 = ttk.Checkbutton(main_frame, variable=self.char2_surprised)
        surprised_checkbox2.grid(row=surprised_row, column=2, padx=10, pady=5)

        # Πρώτο χτύπημα checkboxes
        first_strike_row = len(self.stats) + 2
        ttk.Label(main_frame, text="Πρώτο χτύπημα").grid(row=first_strike_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        self.char1_first_strike = tk.BooleanVar()
        first_strike_checkbox1 = ttk.Checkbutton(main_frame, variable=self.char1_first_strike)
        first_strike_checkbox1.grid(row=first_strike_row, column=1, padx=10, pady=5)

        self.char2_first_strike = tk.BooleanVar()
        first_strike_checkbox2 = ttk.Checkbutton(main_frame, variable=self.char2_first_strike)
        first_strike_checkbox2.grid(row=first_strike_row, column=2, padx=10, pady=5)

        # Αριθμός χαρακτήρων 2
        number_row = len(self.stats) + 3
        ttk.Label(main_frame, text="Αριθμός").grid(row=number_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        # Empty space for Character 1 column
        ttk.Label(main_frame, text="").grid(row=number_row, column=1, padx=10, pady=5)

        # Number entry for Character 2
        self.char2_number_entry = ttk.Entry(main_frame, width=10)
        self.char2_number_entry.grid(row=number_row, column=2, padx=10, pady=5)
        self.char2_number_entry.insert(0, "1")  # Default value

        # Battle buttons
        single_battle_btn = ttk.Button(main_frame, text="Μονομαχία", command=self.single_battle)
        single_battle_btn.grid(row=len(self.stats) + 4, column=0, columnspan=3, pady=10)

        thousand_battles_btn = ttk.Button(main_frame, text="1000 μάχες", command=self.thousand_battles)
        thousand_battles_btn.grid(row=len(self.stats) + 5, column=0, columnspan=3, pady=10)

        ten_thousand_battles_btn = ttk.Button(main_frame, text="10000 μάχες", command=self.ten_thousand_battles)
        ten_thousand_battles_btn.grid(row=len(self.stats) + 6, column=0, columnspan=3, pady=10)

        # Result text area
        result_frame = ttk.LabelFrame(main_frame, text="Αποτέλεσμα", padding="10")
        result_frame.grid(row=len(self.stats) + 7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        self.result_text = tk.Text(result_frame, height=15, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)

        # Enable text selection and copying
        self.result_text.bind("<Control-a>", self.select_all)
        self.result_text.bind("<Control-c>", self.copy_text)

        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(len(self.stats) + 7, weight=1)

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
            value = entry.get().strip() if entry.get() else ""

            # Ειδική διαχείριση για Ζαριά ζημιάς και Αριθμός επιθέσεων
            if stat == "Ζαριά ζημιάς":
                stats[stat] = value if value else "1d6"
            elif stat == "Αριθμός επιθέσεων":
                stats[stat] = value if value else "1"
            elif stat == "Ασπίδες/γύρο":
                try:
                    stats[stat] = int(value) if value else 0
                except ValueError:
                    stats[stat] = 0
            else:
                try:
                    stats[stat] = int(value) if value else 0
                except ValueError:
                    stats[stat] = 0
        return stats

    def get_char2_number(self):
        """Παίρνει τον αριθμό των χαρακτήρων 2 (τουλάχιστον 1)"""
        try:
            number = int(self.char2_number_entry.get()) if self.char2_number_entry.get() else 1
            return max(1, number)
        except ValueError:
            return 1

    def parse_damage_die(self, damage_die_str):
        """
        Αναλύει ένα damage die string της μορφής XD6+Y ή XD6-Y ή XD6
        Επιστρέφει (num_dice, bonus)
        Πάντα d6!
        """
        damage_die_str = damage_die_str.strip().upper()

        # Pattern: XD6+Y ή XD6-Y ή XD6
        match = re.match(r'(\d+)D6(([+-])(\d+))?', damage_die_str)

        if match:
            num_dice = int(match.group(1))
            bonus = 0

            if match.group(2):  # Υπάρχει bonus
                sign = match.group(3)
                bonus_value = int(match.group(4))
                bonus = bonus_value if sign == '+' else -bonus_value

            return num_dice, bonus
        else:
            # Default αν δεν μπορούμε να το parse
            return 1, 0

    def roll_damage(self, damage_die_str):
        """Ρίχνει damage dice και επιστρέφει το αποτέλεσμα"""
        num_dice, bonus = self.parse_damage_die(damage_die_str)

        total = 0
        rolls = []
        for _ in range(num_dice):
            roll = random.randint(1, 6)
            rolls.append(roll)
            total += roll

        total += bonus

        return total, rolls, bonus

    def parse_attacks(self, attacks_str):
        """
        Αναλύει το Αριθμός επιθέσεων string
        Μπορεί να είναι: "1", "2", "3/2", "5/2", κλπ
        Επιστρέφει float
        """
        attacks_str = attacks_str.strip()

        # Έλεγχος για κλάσμα
        if '/' in attacks_str:
            parts = attacks_str.split('/')
            try:
                numerator = float(parts[0])
                denominator = float(parts[1])
                return numerator / denominator
            except (ValueError, IndexError, ZeroDivisionError):
                return 1.0
        else:
            try:
                return float(attacks_str)
            except ValueError:
                return 1.0

    def get_attacks_for_round(self, character, round_number):
        """
        Υπολογίζει πόσες επιθέσεις έχει ένας χαρακτήρας σε αυτόν τον γύρο
        Επιστρέφει αριθμό επιθέσεων
        """
        attacks_per_round = self.parse_attacks(character.stats["Αριθμός επιθέσεων"])

        if attacks_per_round >= 1:
            total_attacks = int(attacks_per_round)

            # Για fractional attacks (πχ 3/2 = 1.5)
            if attacks_per_round % 1 != 0:
                # Για 3/2 (1.5): κάθε δεύτερο γύρο παίρνει +1 επίθεση
                if round_number % 2 == 0:  # Ζυγοί γύροι
                    total_attacks += 1

            return total_attacks
        else:
            return 1

    def roll_d6(self):
        """Ρίχνει 1d6"""
        return random.randint(1, 6)

    def roll_2d6(self):
        """Ρίχνει 2d6"""
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        return die1, die2, die1 + die2

    def initiative_phase(self, char1, char2):
        """Καθορίζει ποιος παίζει πρώτος με initiative roll (1d6)"""
        result = ""

        dice1 = self.roll_d6()
        dice2 = self.roll_d6()

        result += f"{char1.name}: 1d6 = {dice1}\n"
        result += f"{char2.name}: 1d6 = {dice2}\n"

        if dice1 > dice2:
            result += f"{char1.name} παίζει πρώτος!\n\n"
            return char1, char2, result
        elif dice2 > dice1:
            result += f"{char2.name} παίζει πρώτος!\n\n"
            return char2, char1, result
        else:
            result += "Ισοβαθμία στην πρωτοβουλία! Παίζουν ταυτόχρονα.\n\n"
            return None, None, result  # Ταυτόχρονες επιθέσεις

    def attack_roll(self, attacker, defender):
        """
        Εκτελεί attack roll
        Επιστρέφει (hit, roll_result, target_number, description)
        """
        die1, die2, roll_result = self.roll_2d6()

        # Ελέγχουμε αν ο αμυνόμενος έχει ασπίδες διαθέσιμες
        base_armor = defender.stats["Θωράκιση"]
        effective_armor = base_armor
        shields_per_round = defender.stats.get("Ασπίδες/γύρο", 0)

        if defender.shields_used_this_round < shields_per_round:
            effective_armor += 1
            defender.shields_used_this_round += 1
            shield_bonus = True
        else:
            shield_bonus = False

        # Target number = Ζαριά μάχης του επιτιθέμενου + Θωράκιση του αμυνόμενου
        target_number = attacker.stats["Ζαριά μάχης"] + effective_armor

        hit = roll_result >= target_number

        desc = f"Επίθεση: 2d6 = {die1}+{die2} = {roll_result} "
        if shield_bonus:
            desc += f"(χρειάζεται {target_number}, Θωράκιση {base_armor}+1 από ασπίδα)\n"
        else:
            desc += f"(χρειάζεται {target_number})\n"

        return hit, roll_result, target_number, desc

    def perform_attack(self, attacker, defender, attack_type="Επίθεση"):
        """Εκτελεί μια πλήρη επίθεση"""
        result = f"--- {attack_type} από {attacker.name} ---\n"

        hit, roll_result, target_number, attack_desc = self.attack_roll(attacker, defender)
        result += attack_desc

        if hit:
            result += "Επιτυχής επίθεση!\n"

            # Roll damage
            damage, rolls, bonus = self.roll_damage(attacker.stats["Ζαριά ζημιάς"])

            result += f"Ζημιά: {attacker.stats['Ζαριά ζημιάς']} = {rolls}"
            if bonus != 0:
                result += f" {'+' if bonus > 0 else ''}{bonus}"
            result += f" = {damage}\n"

            defender.take_damage(damage)
            result += f"{defender.name} Πόντοι αντοχής: {defender.current_hp}/{defender.max_hp}\n"

            if not defender.is_alive():
                result += f"{defender.name} νικιέται!\n"
                return result, True
        else:
            result += "Αποτυχημένη επίθεση!\n"

        result += "\n"
        return result, False

    def simulate_round(self, char1, char2, round_number, char1_first_strike=False, char2_first_strike=False):
        """Προσομοιώνει έναν γύρο μάχης"""
        result = f"=== ΓΥΡΟΣ {round_number} ===\n"

        # Reset shield counters at the start of each round
        char1.reset_shields()
        char2.reset_shields()

        # Έλεγχος για αιφνιδιασμένους χαρακτήρες στον πρώτο γύρο
        if round_number == 1:
            char1_can_act = not char1.surprised
            char2_can_act = not char2.surprised

            if char1.surprised:
                result += f"{char1.name} είναι αιφνιδιασμένος και δεν παίζει αυτόν τον γύρο!\n"
            if char2.surprised:
                result += f"{char2.name} είναι αιφνιδιασμένος και δεν παίζει αυτόν τον γύρο!\n"

            # Αν και οι δύο είναι αιφνιδιασμένοι, δεν γίνεται τίποτα
            if not char1_can_act and not char2_can_act:
                result += "\n"
                return result, False, None

            # Αν μόνο ο ένας είναι αιφνιδιασμένος, ο άλλος παίζει μόνος του
            if not char1_can_act:
                result += "\n"
                num_attacks = self.get_attacks_for_round(char2, round_number)
                for attack_num in range(num_attacks):
                    attack_type = "Επίθεση" if attack_num == 0 else f"Επιπλέον επίθεση {attack_num}"
                    attack_result, defeated = self.perform_attack(char2, char1, attack_type)
                    result += attack_result
                    if defeated:
                        return result, True, char2
                return result, False, None

            if not char2_can_act:
                result += "\n"
                num_attacks = self.get_attacks_for_round(char1, round_number)
                for attack_num in range(num_attacks):
                    attack_type = "Επίθεση" if attack_num == 0 else f"Επιπλέον επίθεση {attack_num}"
                    attack_result, defeated = self.perform_attack(char1, char2, attack_type)
                    result += attack_result
                    if defeated:
                        return result, True, char1
                return result, False, None

        # Έλεγχος για "Πρώτο χτύπημα" - ισχύει μόνο στον πρώτο "κανονικό" γύρο
        # (αν υπήρχε surprise round, τότε στον επόμενο γύρο)
        first_normal_round = 1
        if char1.surprised or char2.surprised:
            first_normal_round = 2

        if round_number == first_normal_round:
            # Έλεγχος για πρώτο χτύπημα
            if char1_first_strike and not char2_first_strike:
                result += f"{char1.name} έχει Πρώτο χτύπημα!\n\n"
                first_player = char1
                second_player = char2
                init_result = ""
            elif char2_first_strike and not char1_first_strike:
                result += f"{char2.name} έχει Πρώτο χτύπημα!\n\n"
                first_player = char2
                second_player = char1
                init_result = ""
            else:
                # Και οι δύο έχουν ή κανένας - κανονικό initiative roll
                first_player, second_player, init_result = self.initiative_phase(char1, char2)
                result += init_result
        else:
            # Κανονικό initiative roll για όλους τους άλλους γύρους
            first_player, second_player, init_result = self.initiative_phase(char1, char2)
            result += init_result

        simultaneous = (first_player is None)

        # Υπολογίζουμε πόσες επιθέσεις έχει ο καθένας
        char1_attacks = self.get_attacks_for_round(char1, round_number)
        char2_attacks = self.get_attacks_for_round(char2, round_number)

        result += f"{char1.name} έχει {char1_attacks} επιθέσεις αυτόν τον γύρο\n"
        result += f"{char2.name} έχει {char2_attacks} επιθέσεις αυτόν τον γύρο\n\n"

        if simultaneous:
            # Ταυτόχρονες επιθέσεις - όλες μαζί
            # Και οι δύο παίζουν ΟΛΑ τα χτυπήματά τους, ακόμα και αν ο αντίπαλός τους πεθάνει!

            # Char1 κάνει όλες τις επιθέσεις του
            for attack_num in range(char1_attacks):
                if char2.is_alive():  # Μόνο αν ο στόχος ζει
                    attack_type = "Επίθεση" if attack_num == 0 else f"Επιπλέον επίθεση {attack_num}"
                    attack_result, defeated = self.perform_attack(char1, char2, attack_type)
                    result += attack_result

            # Char2 κάνει όλες τις επιθέσεις του
            for attack_num in range(char2_attacks):
                if char1.is_alive():  # Μόνο αν ο στόχος ζει
                    attack_type = "Επίθεση" if attack_num == 0 else f"Επιπλέον επίθεση {attack_num}"
                    attack_result, defeated = self.perform_attack(char2, char1, attack_type)
                    result += attack_result

            # Τώρα ελέγχουμε ποιος ζει
            char1_alive = char1.is_alive()
            char2_alive = char2.is_alive()

            if not char1_alive and not char2_alive:
                # Και οι δύο πέθαναν - ΙΣΟΠΑΛΙΑ!
                result += "\nΚαι οι δύο χαρακτήρες νικιούνται ταυτόχρονα!\n"
                return result, True, None  # None = ισοπαλία
            elif not char1_alive:
                return result, True, char2
            elif not char2_alive:
                return result, True, char1
        else:
            # Κανονική σειρά - πρώτος παίζει ο first_player με όλες τις επιθέσεις του
            if first_player == char1:
                num_attacks = char1_attacks
            else:
                num_attacks = char2_attacks

            for attack_num in range(num_attacks):
                if not second_player.is_alive():
                    break
                attack_type = "Επίθεση" if attack_num == 0 else f"Επιπλέον επίθεση {attack_num}"
                attack_result, defeated = self.perform_attack(first_player, second_player, attack_type)
                result += attack_result
                if defeated:
                    return result, True, first_player

            # Μετά παίζει ο δεύτερος με όλες τις επιθέσεις του
            if second_player == char1:
                num_attacks = char1_attacks
            else:
                num_attacks = char2_attacks

            for attack_num in range(num_attacks):
                if not first_player.is_alive():
                    break
                attack_type = "Επίθεση" if attack_num == 0 else f"Επιπλέον επίθεση {attack_num}"
                attack_result, defeated = self.perform_attack(second_player, first_player, attack_type)
                result += attack_result
                if defeated:
                    return result, True, second_player

        return result, False, None

    def simulate_battle(self, char1_stats, char2_stats, char1_surprised, char2_surprised, char1_first_strike=False, char2_first_strike=False, verbose=True):
        """Προσομοιώνει μια πλήρη μάχη"""
        char1 = Character("Χαρακτήρας 1", char1_stats, char1_surprised)
        char2 = Character("Χαρακτήρας 2", char2_stats, char2_surprised)

        result = ""

        if verbose:
            result += "=== ΜΑΧΗ ΧΑΡΑΚΤΗΡΩΝ - ΚΡΥΠΤΕΣ ===\n\n"

        round_number = 0
        while round_number < 100:  # Safety limit
            round_number += 1

            round_result, battle_ended, winner = self.simulate_round(char1, char2, round_number, char1_first_strike, char2_first_strike)

            if verbose:
                result += round_result

            if battle_ended:
                if winner is None:
                    # Ισοπαλία - και οι δύο πέθαναν ταυτόχρονα
                    if verbose:
                        result += f"\n🤝 ΙΣΟΠΑΛΙΑ! 🤝\n"
                        result += f"Συνολικοί γύροι: {round_number}\n"
                    return result, 0, round_number
                else:
                    if verbose:
                        result += f"\n🏆 ΝΙΚΗΤΗΣ: {winner.name}! 🏆\n"
                        result += f"Συνολικοί γύροι: {round_number}\n"

                    winner_num = 1 if winner == char1 else 2
                    return result, winner_num, round_number

        # Ισοπαλία
        if verbose:
            result += "\nΗ μάχη διαρκεί πολύ! Ισοπαλία.\n"
        return result, 0, round_number

    def simulate_battle_1vMany(self, char1_stats, char2_stats, char2_number, char1_surprised, char2_surprised, char1_first_strike=False, char2_first_strike=False, verbose=True):
        """Προσομοιώνει μάχη 1 vs πολλοί"""
        char1 = Character("Χαρακτήρας 1", char1_stats, char1_surprised)
        char2_list = []

        for i in range(char2_number):
            char = Character(f"Χαρακτήρας 2.{i+1}", char2_stats, char2_surprised)
            char2_list.append(char)

        result = ""
        if verbose:
            result += f"=== ΜΑΧΗ ΧΑΡΑΚΤΗΡΩΝ - ΚΡΥΠΤΕΣ (1 vs {char2_number}) ===\n\n"

        round_number = 0
        while round_number < 100:  # Safety limit
            round_number += 1

            # Reset shield counters at the start of each round
            char1.reset_shields()
            for enemy in char2_list:
                enemy.reset_shields()

            # Έλεγχος αν υπάρχουν ζωντανοί εχθροί
            alive_enemies = [c for c in char2_list if c.is_alive()]
            if not alive_enemies:
                if verbose:
                    result += f"\n🏆 ΝΙΚΗΤΗΣ: {char1.name}! 🏆\n"
                    result += f"Συνολικοί γύροι: {round_number}\n"
                return result, 1, round_number

            if not char1.is_alive():
                if verbose:
                    result += f"\n🏆 ΝΙΚΗΤΕΣ: Οι αντίπαλοι! 🏆\n"
                    result += f"Συνολικοί γύροι: {round_number}\n"
                return result, 2, round_number

            if verbose:
                result += f"=== ΓΥΡΟΣ {round_number} ===\n"
                result += f"Ζωντανοί εχθροί: {len(alive_enemies)}\n\n"

            # Έλεγχος για αιφνιδιασμό στον πρώτο γύρο
            if round_number == 1:
                char1_can_act = not char1.surprised
                enemies_can_act = not char2_surprised

                if char1.surprised:
                    if verbose:
                        result += f"{char1.name} είναι αιφνιδιασμένος!\n"
                if char2_surprised:
                    if verbose:
                        result += f"Οι εχθροί είναι αιφνιδιασμένοι!\n"

                # Αν και οι δύο αιφνιδιάζονται
                if not char1_can_act and not enemies_can_act:
                    if verbose:
                        result += "\n"
                    continue

                # Μόνο char1 αιφνιδιάζεται
                if not char1_can_act and enemies_can_act:
                    if verbose:
                        result += "\n"
                    for enemy in alive_enemies:
                        num_attacks = self.get_attacks_for_round(enemy, round_number)
                        for attack_num in range(num_attacks):
                            attack_type = "Επίθεση" if attack_num == 0 else f"Επιπλέον επίθεση {attack_num}"
                            attack_result, defeated = self.perform_attack(enemy, char1, attack_type)
                            if verbose:
                                result += attack_result
                            if defeated:
                                if verbose:
                                    result += f"\n🏆 ΝΙΚΗΤΕΣ: Οι αντίπαλοι! 🏆\n"
                                    result += f"Συνολικοί γύροι: {round_number}\n"
                                return result, 2, round_number
                    continue

                # Μόνο εχθροί αιφνιδιάζονται
                if char1_can_act and not enemies_can_act:
                    if verbose:
                        result += "\n"
                    target = min(alive_enemies, key=lambda c: c.current_hp)
                    num_attacks = self.get_attacks_for_round(char1, round_number)

                    for attack_num in range(num_attacks):
                        if not target.is_alive():
                            alive_enemies = [c for c in char2_list if c.is_alive()]
                            if not alive_enemies:
                                break
                            target = min(alive_enemies, key=lambda c: c.current_hp)

                        attack_type = "Επίθεση" if attack_num == 0 else f"Επιπλέον επίθεση {attack_num}"
                        attack_result, defeated = self.perform_attack(char1, target, attack_type)
                        if verbose:
                            result += attack_result

                    alive_enemies = [c for c in char2_list if c.is_alive()]
                    if not alive_enemies:
                        if verbose:
                            result += f"\n🏆 ΝΙΚΗΤΗΣ: {char1.name}! 🏆\n"
                            result += f"Συνολικοί γύροι: {round_number}\n"
                        return result, 1, round_number
                    continue

            # Έλεγχος για "Πρώτο χτύπημα" - ισχύει μόνο στον πρώτο "κανονικό" γύρο
            first_normal_round = 1
            if char1.surprised or char2_surprised:
                first_normal_round = 2

            if round_number == first_normal_round:
                # Έλεγχος για πρώτο χτύπημα
                if char1_first_strike and not char2_first_strike:
                    if verbose:
                        result += f"{char1.name} έχει Πρώτο χτύπημα!\n\n"
                    char1_first = True
                    simultaneous = False
                elif char2_first_strike and not char1_first_strike:
                    if verbose:
                        result += "Οι εχθροί έχουν Πρώτο χτύπημα!\n\n"
                    char1_first = False
                    simultaneous = False
                else:
                    # Και οι δύο έχουν ή κανένας - κανονικό initiative roll
                    dice1 = self.roll_d6()
                    dice2 = self.roll_d6()

                    if verbose:
                        result += f"{char1.name}: 1d6 = {dice1}\n"
                        result += f"Εχθροί: 1d6 = {dice2}\n"

                    char1_first = dice1 > dice2
                    simultaneous = dice1 == dice2

                    if verbose:
                        if simultaneous:
                            result += "Ισοβαθμία στην πρωτοβουλία! Παίζουν ταυτόχρονα.\n\n"
                        elif char1_first:
                            result += f"{char1.name} παίζει πρώτος!\n\n"
                        else:
                            result += "Οι εχθροί παίζουν πρώτοι!\n\n"
            else:
                # Κανονικό initiative roll για όλους τους άλλους γύρους
                dice1 = self.roll_d6()
                dice2 = self.roll_d6()

                if verbose:
                    result += f"{char1.name}: 1d6 = {dice1}\n"
                    result += f"Εχθροί: 1d6 = {dice2}\n"

                char1_first = dice1 > dice2
                simultaneous = dice1 == dice2

                if verbose:
                    if simultaneous:
                        result += "Ισοβαθμία στην πρωτοβουλία! Παίζουν ταυτόχρονα.\n\n"
                    elif char1_first:
                        result += f"{char1.name} παίζει πρώτος!\n\n"
                    else:
                        result += "Οι εχθροί παίζουν πρώτοι!\n\n"

            # Επιλογή στόχου: ο πιο χτυπημένος
            target = min(alive_enemies, key=lambda c: c.current_hp)

            # Ανάλογα με την πρωτοβουλία
            if char1_first or simultaneous:
                # Char1 επιτίθεται πρώτος με όλες τις επιθέσεις του
                num_attacks = self.get_attacks_for_round(char1, round_number)

                for attack_num in range(num_attacks):
                    if not target.is_alive():
                        # Αλλάζουμε στόχο
                        alive_enemies = [c for c in char2_list if c.is_alive()]
                        if not alive_enemies:
                            break
                        target = min(alive_enemies, key=lambda c: c.current_hp)

                    attack_type = "Επίθεση" if attack_num == 0 else f"Επιπλέον επίθεση {attack_num}"
                    attack_result, defeated = self.perform_attack(char1, target, attack_type)

                    if verbose:
                        result += attack_result

                # Έλεγχος αν όλοι οι εχθροί νικήθηκαν
                alive_enemies = [c for c in char2_list if c.is_alive()]
                if not alive_enemies:
                    if verbose:
                        result += f"\n🏆 ΝΙΚΗΤΗΣ: {char1.name}! 🏆\n"
                        result += f"Συνολικοί γύροι: {round_number}\n"
                    return result, 1, round_number

                # Μετά οι εχθροί
                for enemy in alive_enemies:
                    if not char1.is_alive():
                        break

                    num_attacks = self.get_attacks_for_round(enemy, round_number)

                    for attack_num in range(num_attacks):
                        if not char1.is_alive():
                            break

                        attack_type = "Επίθεση" if attack_num == 0 else f"Επιπλέον επίθεση {attack_num}"
                        attack_result, defeated = self.perform_attack(enemy, char1, attack_type)

                        if verbose:
                            result += attack_result

                        if defeated:
                            if verbose:
                                result += f"\n🏆 ΝΙΚΗΤΕΣ: Οι αντίπαλοι! 🏆\n"
                                result += f"Συνολικοί γύροι: {round_number}\n"
                            return result, 2, round_number
            else:
                # Εχθροί επιτίθενται πρώτοι
                for enemy in alive_enemies:
                    if not char1.is_alive():
                        break

                    num_attacks = self.get_attacks_for_round(enemy, round_number)

                    for attack_num in range(num_attacks):
                        if not char1.is_alive():
                            break

                        attack_type = "Επίθεση" if attack_num == 0 else f"Επιπλέον επίθεση {attack_num}"
                        attack_result, defeated = self.perform_attack(enemy, char1, attack_type)

                        if verbose:
                            result += attack_result

                        if defeated:
                            if verbose:
                                result += f"\n🏆 ΝΙΚΗΤΕΣ: Οι αντίπαλοι! 🏆\n"
                                result += f"Συνολικοί γύροι: {round_number}\n"
                            return result, 2, round_number

                # Μετά ο char1
                num_attacks = self.get_attacks_for_round(char1, round_number)

                for attack_num in range(num_attacks):
                    if not target.is_alive():
                        # Αλλάζουμε στόχο
                        alive_enemies = [c for c in char2_list if c.is_alive()]
                        if not alive_enemies:
                            break
                        target = min(alive_enemies, key=lambda c: c.current_hp)

                    attack_type = "Επίθεση" if attack_num == 0 else f"Επιπλέον επίθεση {attack_num}"
                    attack_result, defeated = self.perform_attack(char1, target, attack_type)

                    if verbose:
                        result += attack_result

                # Έλεγχος αν όλοι οι εχθροί νικήθηκαν
                alive_enemies = [c for c in char2_list if c.is_alive()]
                if not alive_enemies:
                    if verbose:
                        result += f"\n🏆 ΝΙΚΗΤΗΣ: {char1.name}! 🏆\n"
                        result += f"Συνολικοί γύροι: {round_number}\n"
                    return result, 1, round_number

        # Ισοπαλία
        if verbose:
            result += "\nΗ μάχη διαρκεί πολύ! Ισοπαλία.\n"
        return result, 0, round_number

    def single_battle(self):
        """Εκτελεί μια αναλυτική μάχη"""
        char1_stats = self.get_character_stats(self.char1_entries)
        char2_stats = self.get_character_stats(self.char2_entries)
        char2_number = self.get_char2_number()

        # Clear previous results
        self.result_text.delete(1.0, tk.END)

        if char2_number == 1:
            result, winner, rounds = self.simulate_battle(
                char1_stats, char2_stats,
                self.char1_surprised.get(), self.char2_surprised.get(),
                self.char1_first_strike.get(), self.char2_first_strike.get(),
                verbose=True
            )
        else:
            result, winner, rounds = self.simulate_battle_1vMany(
                char1_stats, char2_stats, char2_number,
                self.char1_surprised.get(), self.char2_surprised.get(),
                self.char1_first_strike.get(), self.char2_first_strike.get(),
                verbose=True
            )

        self.result_text.insert(tk.END, result)

    def thousand_battles(self):
        """Εκτελεί 1000 μάχες και εμφανίζει στατιστικά"""
        char1_stats = self.get_character_stats(self.char1_entries)
        char2_stats = self.get_character_stats(self.char2_entries)
        char2_number = self.get_char2_number()

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
            self.result_text.insert(tk.END, f"Εκτελούνται 1000 μάχες (1 vs {char2_number})...\n\n")
        self.root.update()

        for i in range(1000):
            if char2_number == 1:
                _, winner, rounds = self.simulate_battle(
                    char1_stats, char2_stats,
                    self.char1_surprised.get(), self.char2_surprised.get(),
                    self.char1_first_strike.get(), self.char2_first_strike.get(),
                    verbose=False
                )
            else:
                _, winner, rounds = self.simulate_battle_1vMany(
                    char1_stats, char2_stats, char2_number,
                    self.char1_surprised.get(), self.char2_surprised.get(),
                    self.char1_first_strike.get(), self.char2_first_strike.get(),
                    verbose=False
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
        result = f"=== ΑΠΟΤΕΛΕΣΜΑΤΑ 1000 ΜΑΧΩΩΝ ===\n"
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

    def ten_thousand_battles(self):
        """Εκτελεί 10000 μάχες και εμφανίζει στατιστικά"""
        char1_stats = self.get_character_stats(self.char1_entries)
        char2_stats = self.get_character_stats(self.char2_entries)
        char2_number = self.get_char2_number()

        char1_wins = 0
        char2_wins = 0
        draws = 0
        total_rounds = 0
        min_rounds = float('inf')
        max_rounds = 0

        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        if char2_number == 1:
            self.result_text.insert(tk.END, "Εκτελούνται 10000 μάχες...\n\n")
        else:
            self.result_text.insert(tk.END, f"Εκτελούνται 10000 μάχες (1 vs {char2_number})...\n\n")
        self.root.update()

        for i in range(10000):
            if char2_number == 1:
                _, winner, rounds = self.simulate_battle(
                    char1_stats, char2_stats,
                    self.char1_surprised.get(), self.char2_surprised.get(),
                    self.char1_first_strike.get(), self.char2_first_strike.get(),
                    verbose=False
                )
            else:
                _, winner, rounds = self.simulate_battle_1vMany(
                    char1_stats, char2_stats, char2_number,
                    self.char1_surprised.get(), self.char2_surprised.get(),
                    self.char1_first_strike.get(), self.char2_first_strike.get(),
                    verbose=False
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
        avg_rounds = total_rounds / 10000
        result = f"=== ΑΠΟΤΕΛΕΣΜΑΤΑ 10000 ΜΑΧΩΩΝ ===\n"
        if char2_number > 1:
            result += f"(Χαρακτήρας 1 εναντίον {char2_number} αντιπάλων)\n"
        result += "\n"
        result += f"Χαρακτήρας 1: {char1_wins} νίκες ({char1_wins/100:.1f}%)\n"
        if char2_number == 1:
            result += f"Χαρακτήρας 2: {char2_wins} νίκες ({char2_wins/100:.1f}%)\n"
        else:
            result += f"Οι αντίπαλοι: {char2_wins} νίκες ({char2_wins/100:.1f}%)\n"
        if draws > 0:
            result += f"Ισοπαλίες: {draws} ({draws/100:.1f}%)\n"
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

def main():
    root = tk.Tk()
    app = CharacterBattleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

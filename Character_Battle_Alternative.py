import tkinter as tk
from tkinter import ttk
import random

class Character:
    def __init__(self, name, stats, is_minion=False):
        self.name = name
        self.base_stats = stats.copy()
        self.current_stats = stats.copy()
        self.is_minion = is_minion
        self.wounds = 0

    def get_effective_stat(self, stat_name):
        """Υπολογίζει το τελικό stat"""
        return self.current_stats[stat_name]

class CharacterBattleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Μάχη Χαρακτήρων - Εναλλακτικό Σύστημα")
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

        # Stats labels and entries - Νέο σύστημα: Μάχη, Ζημιά, Αντοχή
        self.stats = ["Μάχη", "Ζημιά", "Αντοχή"]
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

        # Αριθμός χαρακτήρων 2
        number_row = len(self.stats) + 1
        ttk.Label(main_frame, text="Αριθμός").grid(row=number_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        # Empty space for Character 1 column
        ttk.Label(main_frame, text="").grid(row=number_row, column=1, padx=10, pady=5)

        # Number entry for Character 2
        self.char2_number_entry = ttk.Entry(main_frame, width=10)
        self.char2_number_entry.grid(row=number_row, column=2, padx=10, pady=5)
        self.char2_number_entry.insert(0, "1")  # Default value

        # Πόσοι μάχονται
        engaged_row = len(self.stats) + 2
        ttk.Label(main_frame, text="Πόσοι μάχονται").grid(row=engaged_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        # Empty space for Character 1 column
        ttk.Label(main_frame, text="").grid(row=engaged_row, column=1, padx=10, pady=5)

        # Engaged entry for Character 2
        self.char2_engaged_entry = ttk.Entry(main_frame, width=10)
        self.char2_engaged_entry.grid(row=engaged_row, column=2, padx=10, pady=5)
        self.char2_engaged_entry.insert(0, "1")  # Default value

        # Τσιράκι checkbox
        minion_row = len(self.stats) + 3
        ttk.Label(main_frame, text="Τσιράκι").grid(row=minion_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        # Empty space for Character 1 column
        ttk.Label(main_frame, text="").grid(row=minion_row, column=1, padx=10, pady=5)

        # Minion checkbox for Character 2
        self.char2_minion = tk.BooleanVar()
        minion_checkbox2 = ttk.Checkbutton(main_frame, variable=self.char2_minion)
        minion_checkbox2.grid(row=minion_row, column=2, padx=10, pady=5)

        # Όχι καίρια χτυπήματα checkbox
        no_crit_row = len(self.stats) + 4
        ttk.Label(main_frame, text="Όχι καίρια χτυπήματα").grid(row=no_crit_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        # No critical hits checkbox for Character 1
        self.char1_no_crit = tk.BooleanVar()
        no_crit_checkbox1 = ttk.Checkbutton(main_frame, variable=self.char1_no_crit)
        no_crit_checkbox1.grid(row=no_crit_row, column=1, padx=10, pady=5)

        # No critical hits checkbox for Character 2
        self.char2_no_crit = tk.BooleanVar()
        no_crit_checkbox2 = ttk.Checkbutton(main_frame, variable=self.char2_no_crit)
        no_crit_checkbox2.grid(row=no_crit_row, column=2, padx=10, pady=5)

        # Battle buttons
        single_battle_btn = ttk.Button(main_frame, text="Μονομαχία", command=self.single_battle)
        single_battle_btn.grid(row=len(self.stats) + 5, column=0, columnspan=3, pady=10)

        thousand_battles_btn = ttk.Button(main_frame, text="1000 μάχες", command=self.thousand_battles)
        thousand_battles_btn.grid(row=len(self.stats) + 6, column=0, columnspan=3, pady=10)

        hundred_thousand_battles_btn = ttk.Button(main_frame, text="100000 μάχες", command=self.hundred_thousand_battles)
        hundred_thousand_battles_btn.grid(row=len(self.stats) + 7, column=0, columnspan=3, pady=10)

        # Result text area
        result_frame = ttk.LabelFrame(main_frame, text="Αποτέλεσμα", padding="10")
        result_frame.grid(row=len(self.stats) + 8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        self.result_text = tk.Text(result_frame, height=10, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)

        # Enable text selection and copying
        self.result_text.bind("<Control-a>", self.select_all)
        self.result_text.bind("<Control-c>", self.copy_text)
        # Allow normal text selection and copying
        self.result_text.bind("<Button-1>", self.on_text_click)
        self.result_text.bind("<B1-Motion>", self.on_text_drag)

        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(len(self.stats) + 8, weight=1)

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

    def on_text_click(self, event):
        """Handle text click for selection"""
        return None  # Allow default behavior

    def on_text_drag(self, event):
        """Handle text drag for selection"""
        return None  # Allow default behavior

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
            return max(1, engaged)  # Τουλάχιστον 1
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

    def apply_damage(self, attacker, defender, attacker_battle_dice, defender_no_crit, result_text=""):
        """Εφαρμόζει ζημιά από τον attacker στον defender.
        Αν attacker_battle_dice == 20 και defender_no_crit == False, ρίχνει 2 ζαριές ζημιάς.
        Επιστρέφει: (result_text, battle_ended, winner, wounds_dealt)"""

        is_critical = (attacker_battle_dice == 20 and not defender_no_crit)
        num_damage_rolls = 2 if is_critical else 1

        if is_critical:
            result_text += "⚔️ ΚΑΙΡΙΟ ΧΤΥΠΗΜΑ! Ρίχνει 2 ζαριές ζημιάς!\n"

        total_wounds = 0

        for roll_num in range(num_damage_rolls):
            dmg_dice, dmg_mod, damage_roll = self.roll_d20(attacker.get_effective_stat("Ζημιά"))
            end_dice, end_mod, endurance_roll = self.roll_d20(defender.get_effective_stat("Αντοχή"))

            damage_display = self.format_dice_roll("Ζημιά", dmg_dice, dmg_mod, damage_roll)
            endurance_display = self.format_dice_roll("Αντοχή", end_dice, end_mod, endurance_roll)

            if is_critical:
                result_text += f"Ζημιά {roll_num + 1}/2: {damage_display} vs {endurance_display}\n"
            else:
                result_text += f"{damage_display} vs {endurance_display}\n"

            damage_diff = damage_roll - endurance_roll
            had_two_wounds = defender.wounds >= 2

            # Τσιράκι: πεθαίνει με οποιαδήποτε επιτυχή ζημιά
            if defender.is_minion and damage_diff >= 0:
                result_text += f"Τσιράκι! (+{damage_diff}) Ο {defender.name} νικιέται!\n"
                defender.wounds = 10  # Σημάδι νίκης
                return result_text, True, attacker, total_wounds
            elif damage_diff >= 10:
                result_text += f"ΘΑΝΑΤΗΦΟΡΟ ΧΤΥΠΗΜΑ! (+{damage_diff}) Ο {defender.name} νικιέται!\n"
                defender.wounds = 10  # Σημάδι νίκης
                return result_text, True, attacker, total_wounds
            elif damage_diff >= 5:
                result_text += f"Σοβαρή ζημιά! (+{damage_diff}) 2 λαβωματιές\n"
                defender.wounds += 2
                total_wounds += 2
            elif damage_diff >= 0:
                result_text += f"Ζημιά! (+{damage_diff}) 1 λαβωματιά\n"
                defender.wounds += 1
                total_wounds += 1
            else:
                result_text += f"Αντέχει τη ζημιά! ({damage_diff})\n"

            # Έλεγχος αν ο defender είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά (μόνο αν δεν είναι τσιράκι)
            if not defender.is_minion and had_two_wounds and damage_diff >= 0:
                result_text += f"Ο {defender.name} έχει πάρει πολλές λαβωματιές και νικιέται!\n"
                defender.wounds = 10  # Σημάδι νίκης
                return result_text, True, attacker, total_wounds

        # Αν δεν νικήθηκε, εμφάνισε κατάσταση
        if defender.wounds < 10:
            result_text += f"Κατάσταση {defender.name}: {defender.wounds} λαβωματιές\n"

        return result_text, False, None, total_wounds

    def battle_round_multiple(self, char1, char2_list, max_engaged):
        """Εκτελεί έναν γύρο μάχης με πολλαπλούς αντιπάλους και σύστημα reserves"""
        result = f"--- Γύρος Μάχης ---\n"

        # Βρίσκουμε τους ζωντανούς εχθρούς
        alive_enemies = [char2 for char2 in char2_list if char2.wounds != 10]

        # Χωρίζουμε σε engaged και reserves
        engaged_enemies = alive_enemies[:max_engaged]
        reserves = alive_enemies[max_engaged:]

        if reserves:
            result += f"Μάχονται: {len(engaged_enemies)}, Reserves: {len(reserves)}\n"
        else:
            result += f"Μάχονται: {len(engaged_enemies)}\n"
        result += "\n"

        # Ζαριά μάχης του χαρακτήρα 1
        battle1_dice, battle1_mod, battle1_total = self.roll_d20(char1.get_effective_stat("Μάχη"))
        battle1_display = self.format_dice_roll("Μάχη", battle1_dice, battle1_mod, battle1_total)
        result += f"{char1.name}: {battle1_display}\n"

        # Ζαριές μάχης μόνο των engaged χαρακτήρων 2
        char2_results = []
        char1_wins = True

        for char2 in engaged_enemies:
            battle2_dice, battle2_mod, battle2_total = self.roll_d20(char2.get_effective_stat("Μάχη"))
            battle2_display = self.format_dice_roll("Μάχη", battle2_dice, battle2_mod, battle2_total)
            # Βρίσκουμε το index στο αρχικό list
            original_index = char2_list.index(char2)
            result += f"Χαρακτήρας 2.{original_index+1}: {battle2_display}\n"

            char2_results.append((char2, original_index, battle2_total, battle2_mod, battle2_dice))

            # Έλεγχος αν ο χαρακτήρας 1 νικάει αυτόν τον αντίπαλο
            if battle1_total < battle2_total:
                char1_wins = False
            elif battle1_total == battle2_total and battle1_mod <= battle2_mod:
                char1_wins = False

        if char1_wins:
            result += f"\n{char1.name} νικάει όλους τους engaged!\n"

            # Ο χαρακτήρας 1 ρίχνει ζημιά σε όλους τους engaged (με πιθανό καίριο)
            result += f"\n{char1.name} ρίχνει ζημιά σε όλους τους engaged...\n"

            for (char2, original_index, _, _, _) in char2_results:
                result += f"\nΣτον Χαρακτήρα 2.{original_index+1}:\n"

                damage_result, battle_ended, final_winner, _ = self.apply_damage(
                    char1, char2, battle1_dice, self.char2_no_crit.get(), ""
                )
                result += damage_result

                if battle_ended:
                    # Έλεγχος αν όλοι οι χαρακτήρες 2 νικήθηκαν
                    living_enemies = [c for c in char2_list if c.wounds != 10]
                    if len(living_enemies) == 0:
                        return result, True, char1

        else:
            result += f"\nΟι αντίπαλοι νικούν!\n"

            # Όλοι οι engaged χαρακτήρες 2 ρίχνουν ζημιά (με πιθανά καίρια)
            result += f"\nΌλοι οι engaged αντίπαλοι ρίχνουν ζημιά...\n"

            for (char2, original_index, _, _, battle2_dice) in char2_results:
                result += f"\nΧαρακτήρας 2.{original_index+1}:\n"

                damage_result, battle_ended, final_winner, _ = self.apply_damage(
                    char2, char1, battle2_dice, self.char1_no_crit.get(), ""
                )
                result += damage_result

                if battle_ended:
                    return result, True, char2_list[0]  # Οποιοσδήποτε από τους νικητές

            result += f"Κατάσταση {char1.name}: {char1.wounds} λαβωματιές\n\n"

        return result, False, None

    def battle_round(self, char1, char2):
        """Εκτελεί έναν γύρο μάχης με το νέο σύστημα"""
        result = f"--- Γύρος Μάχης ---\n"

        # Ζαριές μάχης και των δύο
        battle1_dice, battle1_mod, battle1_total = self.roll_d20(char1.get_effective_stat("Μάχη"))
        battle2_dice, battle2_mod, battle2_total = self.roll_d20(char2.get_effective_stat("Μάχη"))

        battle1_display = self.format_dice_roll("Μάχη", battle1_dice, battle1_mod, battle1_total)
        battle2_display = self.format_dice_roll("Μάχη", battle2_dice, battle2_mod, battle2_total)

        result += f"{char1.name}: {battle1_display}\n"
        result += f"{char2.name}: {battle2_display}\n"

        # Καθορισμός νικητή
        winner = None
        loser = None
        winner_battle_dice = None
        loser_no_crit = None

        if battle1_total > battle2_total:
            winner = char1
            loser = char2
            winner_battle_dice = battle1_dice
            loser_no_crit = self.char2_no_crit.get()
            result += f"{char1.name} νικάει τον γύρο!\n"
        elif battle2_total > battle1_total:
            winner = char2
            loser = char1
            winner_battle_dice = battle2_dice
            loser_no_crit = self.char1_no_crit.get()
            result += f"{char2.name} νικάει τον γύρο!\n"
        else:
            # Ισοβαθμία - νικάει όποιος έχει μεγαλύτερο συντελεστή
            if battle1_mod > battle2_mod:
                winner = char1
                loser = char2
                winner_battle_dice = battle1_dice
                loser_no_crit = self.char2_no_crit.get()
                result += f"Ισοβαθμία! {char1.name} νικάει λόγω μεγαλύτερου συντελεστή ({battle1_mod} vs {battle2_mod})!\n"
            elif battle2_mod > battle1_mod:
                winner = char2
                loser = char1
                winner_battle_dice = battle2_dice
                loser_no_crit = self.char1_no_crit.get()
                result += f"Ισοβαθμία! {char2.name} νικάει λόγω μεγαλύτερου συντελεστή ({battle2_mod} vs {battle1_mod})!\n"
            else:
                result += f"Πλήρης ισοβαθμία (ζάρι και συντελεστές)! Ξαναρίχνουμε...\n\n"
                return result, False, None  # Ξαναρίχνουμε

        # Ο νικητής ρίχνει ζημιά (με πιθανό καίριο χτύπημα)
        result += f"\n{winner.name} ρίχνει ζημιά...\n"

        damage_result, battle_ended, final_winner, _ = self.apply_damage(
            winner, loser, winner_battle_dice, loser_no_crit, ""
        )
        result += damage_result

        if battle_ended:
            return result + "\n", True, final_winner
        else:
            return result + "\n", False, None

    def apply_damage_silent(self, attacker, defender, attacker_battle_dice, defender_no_crit):
        """Εφαρμόζει ζημιά χωρίς output. Επιστρέφει (battle_ended, winner)"""
        is_critical = (attacker_battle_dice == 20 and not defender_no_crit)
        num_damage_rolls = 2 if is_critical else 1

        for roll_num in range(num_damage_rolls):
            _, _, damage_roll = self.roll_d20(attacker.get_effective_stat("Ζημιά"))
            _, _, endurance_roll = self.roll_d20(defender.get_effective_stat("Αντοχή"))

            damage_diff = damage_roll - endurance_roll
            had_two_wounds = defender.wounds >= 2

            # Τσιράκι: πεθαίνει με οποιαδήποτε επιτυχή ζημιά
            if defender.is_minion and damage_diff >= 0:
                defender.wounds = 10
                return True, attacker
            elif damage_diff >= 10:
                defender.wounds = 10
                return True, attacker
            elif damage_diff >= 5:
                defender.wounds += 2
            elif damage_diff >= 0:
                defender.wounds += 1

            # Έλεγχος αν ο defender είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά
            if not defender.is_minion and had_two_wounds and damage_diff >= 0:
                defender.wounds = 10
                return True, attacker

        return False, None

    def battle_round_silent(self, char1, char2, char1_no_crit, char2_no_crit):
        """Εκτελεί έναν γύρο μάχης χωρίς output"""
        # Ζαριές μάχης
        battle1_dice, _, battle1_total = self.roll_d20(char1.get_effective_stat("Μάχη"))
        battle2_dice, _, battle2_total = self.roll_d20(char2.get_effective_stat("Μάχη"))

        winner = None
        loser = None
        winner_battle_dice = None
        loser_no_crit = None

        if battle1_total > battle2_total:
            winner = char1
            loser = char2
            winner_battle_dice = battle1_dice
            loser_no_crit = char2_no_crit
        elif battle2_total > battle1_total:
            winner = char2
            loser = char1
            winner_battle_dice = battle2_dice
            loser_no_crit = char1_no_crit
        else:
            # Ισοβαθμία - ελέγχουμε συντελεστές
            char1_mod = char1.get_effective_stat("Μάχη")
            char2_mod = char2.get_effective_stat("Μάχη")
            if char1_mod > char2_mod:
                winner = char1
                loser = char2
                winner_battle_dice = battle1_dice
                loser_no_crit = char2_no_crit
            elif char2_mod > char1_mod:
                winner = char2
                loser = char1
                winner_battle_dice = battle2_dice
                loser_no_crit = char1_no_crit
            else:
                return False, None  # Ξαναρίχνουμε

        # Ζημιά με πιθανό καίριο
        return self.apply_damage_silent(winner, loser, winner_battle_dice, loser_no_crit)

    def battle_round_silent_multiple(self, char1, char2_list, max_engaged, char1_no_crit, char2_no_crit):
        """Εκτελεί έναν γύρο μάχης με πολλαπλούς αντιπάλους χωρίς output (με reserves)"""
        # Βρίσκουμε τους ζωντανούς εχθρούς
        alive_enemies = [char2 for char2 in char2_list if char2.wounds != 10]

        # Χωρίζουμε σε engaged και reserves
        engaged_enemies = alive_enemies[:max_engaged]

        # Ζαριά μάχης του χαρακτήρα 1
        battle1_dice, _, battle1_total = self.roll_d20(char1.get_effective_stat("Μάχη"))
        battle1_mod = char1.get_effective_stat("Μάχη")

        # Ζαριές μάχης μόνο των engaged χαρακτήρων 2
        char2_results = []
        char1_wins = True

        for char2 in engaged_enemies:
            battle2_dice, _, battle2_total = self.roll_d20(char2.get_effective_stat("Μάχη"))
            battle2_mod = char2.get_effective_stat("Μάχη")

            char2_results.append((char2, battle2_total, battle2_mod, battle2_dice))

            # Έλεγχος αν ο χαρακτήρας 1 νικάει αυτόν τον αντίπαλο
            if battle1_total < battle2_total:
                char1_wins = False
            elif battle1_total == battle2_total and battle1_mod <= battle2_mod:
                char1_wins = False

        if char1_wins:
            # Ο χαρακτήρας 1 ρίχνει ζημιά σε όλους (με πιθανό καίριο)
            for char2, _, _, _ in char2_results:
                battle_ended, winner = self.apply_damage_silent(char1, char2, battle1_dice, char2_no_crit)
                if battle_ended:
                    # Έλεγχος αν όλοι οι χαρακτήρες 2 νικήθηκαν
                    living_enemies = [c for c in char2_list if c.wounds != 10]
                    if len(living_enemies) == 0:
                        return True, char1

        else:
            # Όλοι οι engaged χαρακτήρες 2 ρίχνουν ζημιά (με πιθανά καίρια)
            for char2, _, _, battle2_dice in char2_results:
                battle_ended, winner = self.apply_damage_silent(char2, char1, battle2_dice, char1_no_crit)
                if battle_ended:
                    return True, char2_list[0]  # Οποιοσδήποτε από τους νικητές

        return False, None

    def simulate_battle_silent(self, char1_stats, char2_stats, char2_number=1, char2_engaged=1, char2_minion=False, char1_no_crit=False, char2_no_crit=False):
        """Προσομοιώνει μια μάχη χωρίς output"""
        char1 = Character("Χαρακτήρας 1", char1_stats)

        # Δημιουργία πολλαπλών χαρακτήρων 2
        char2_list = []
        for i in range(char2_number):
            char2 = Character(f"Χαρακτήρας 2.{i+1}", char2_stats, char2_minion)
            char2_list.append(char2)

        round_count = 0
        while round_count < 100:  # Safety limit
            round_count += 1

            if char2_number == 1:
                battle_ended, winner = self.battle_round_silent(char1, char2_list[0], char1_no_crit, char2_no_crit)
            else:
                battle_ended, winner = self.battle_round_silent_multiple(char1, char2_list, char2_engaged, char1_no_crit, char2_no_crit)

            if battle_ended:
                if winner == char1 or (hasattr(winner, 'name') and winner.name == "Χαρακτήρας 1"):
                    return 1, round_count
                else:
                    return 2, round_count

        return 0, round_count  # Draw

    def thousand_battles(self):
        """Εκτελεί 1000 μάχες και εμφανίζει στατιστικά"""
        char1_stats = self.get_character_stats(self.char1_entries)
        char2_stats = self.get_character_stats(self.char2_entries)
        char2_number = self.get_char2_number()
        char2_engaged = self.get_char2_engaged()

        char1_wins = 0
        char2_wins = 0
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
                char2_number, char2_engaged, self.char2_minion.get(),
                self.char1_no_crit.get(), self.char2_no_crit.get()
            )
            total_rounds += rounds
            min_rounds = min(min_rounds, rounds)
            max_rounds = max(max_rounds, rounds)
            if winner == 1:
                char1_wins += 1
            elif winner == 2:
                char2_wins += 1

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
                char2_number, char2_engaged, self.char2_minion.get(),
                self.char1_no_crit.get(), self.char2_no_crit.get()
            )
            total_rounds += rounds
            min_rounds = min(min_rounds, rounds)
            max_rounds = max(max_rounds, rounds)
            if winner == 1:
                char1_wins += 1
            elif winner == 2:
                char2_wins += 1

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
        char2_engaged = self.get_char2_engaged()

        # Clear previous results
        self.result_text.delete(1.0, tk.END)

        # Δημιουργία χαρακτήρων
        char1 = Character("Χαρακτήρας 1", char1_stats)

        # Δημιουργία πολλαπλών χαρακτήρων 2
        char2_list = []
        for i in range(char2_number):
            char2 = Character(f"Χαρακτήρας 2.{i+1}", char2_stats, self.char2_minion.get())
            char2_list.append(char2)

        if char2_number == 1:
            result = "=== ΜΑΧΗ ΧΑΡΑΚΤΗΡΩΝ - ΕΝΑΛΛΑΚΤΙΚΟ ΣΥΣΤΗΜΑ ===\n\n"
        else:
            result = f"=== ΜΑΧΗ ΧΑΡΑΚΤΗΡΩΝ - ΕΝΑΛΛΑΚΤΙΚΟ ΣΥΣΤΗΜΑ ===\n"
            result += f"Χαρακτήρας 1 εναντίον {char2_number} αντιπάλων (max {char2_engaged} engaged)!\n\n"

        round_count = 0
        while round_count < 50:  # Safety limit
            round_count += 1
            result += f"Γύρος {round_count}:\n"

            if char2_number == 1:
                round_result, battle_ended, winner = self.battle_round(char1, char2_list[0])
            else:
                round_result, battle_ended, winner = self.battle_round_multiple(char1, char2_list, char2_engaged)

            result += round_result

            if battle_ended:
                if char2_number == 1:
                    result += f"\n🏆 ΝΙΚΗΤΗΣ: {winner.name}! 🏆\n"
                else:
                    if winner == char1:
                        result += f"\n🏆 ΝΙΚΗΤΗΣ: {winner.name}! 🏆\n"
                    else:
                        result += f"\n🏆 ΝΙΚΗΤΕΣ: Οι αντίπαλοι! 🏆\n"
                result += f"Συνολικοί γύροι μάχης: {round_count}\n"
                break

        if round_count >= 50:
            result += "\nΗ μάχη διαρκεί πολύ! Ισοπαλία.\n"
            result += f"Συνολικοί γύροι μάχης: {round_count}\n"

        self.result_text.insert(tk.END, result)

def main():
    root = tk.Tk()
    app = CharacterBattleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
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
        self.root.title("Μάχη Χαρακτήρων - Εναλλακτικό Σύστημα (Ζεύγη 1v1)")
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

        # Battle buttons
        single_battle_btn = ttk.Button(main_frame, text="Μονομαχία", command=self.single_battle)
        single_battle_btn.grid(row=len(self.stats) + 4, column=0, columnspan=3, pady=10)

        thousand_battles_btn = ttk.Button(main_frame, text="1000 μάχες", command=self.thousand_battles)
        thousand_battles_btn.grid(row=len(self.stats) + 5, column=0, columnspan=3, pady=10)

        hundred_thousand_battles_btn = ttk.Button(main_frame, text="100000 μάχες", command=self.hundred_thousand_battles)
        hundred_thousand_battles_btn.grid(row=len(self.stats) + 6, column=0, columnspan=3, pady=10)

        # Result text area
        result_frame = ttk.LabelFrame(main_frame, text="Αποτέλεσμα", padding="10")
        result_frame.grid(row=len(self.stats) + 7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

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

    def battle_round_multiple(self, char1, char2_list, max_engaged):
        """Εκτελεί έναν γύρο μάχης με πολλαπλούς αντιπάλους - ΖΕΥΓΗ 1v1"""
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

        # ΝΕΟΣ ΚΑΝΟΝΑΣ: Ζεύγη 1v1
        # Ο Χαρ1 ρίχνει Ν ζαριές (όσοι οι engaged), κάθε εχθρός ρίχνει 1 ζαριά
        num_engaged = len(engaged_enemies)

        # Ποινή για πολλαπλούς εχθρούς: -N για N εχθρούς (από -2 για 2 εχθρούς και πάνω)
        outnumbered_penalty = 0
        if num_engaged >= 2:
            outnumbered_penalty = -num_engaged

        result += f"=== ΖΑΡΙΕΣ ΜΑΧΗΣ (ζεύγη 1v1) ===\n"
        if outnumbered_penalty < 0:
            result += f"ΠΟΙΝΗ ΥΠΕΡΑΡΙΘΜΙΑΣ: {outnumbered_penalty} για {num_engaged} εχθρούς\n"

        # Ο Χαρ1 ρίχνει Ν ζαριές μάχης (με ποινή)
        char1_rolls = []
        char1_base_mod = char1.get_effective_stat("Μάχη")
        char1_effective_mod = char1_base_mod + outnumbered_penalty

        for i in range(num_engaged):
            battle1_dice, _, battle1_total = self.roll_d20(char1_effective_mod)
            char1_rolls.append((battle1_dice, char1_effective_mod, battle1_total))
            if outnumbered_penalty < 0:
                result += f"{char1.name} (vs εχθρός #{i+1}): d20({battle1_dice}) + {char1_base_mod}{outnumbered_penalty} = {battle1_total}\n"
            else:
                result += f"{char1.name} (vs εχθρός #{i+1}): d20({battle1_dice}) + {char1_effective_mod} = {battle1_total}\n"

        result += "\n"

        # Κάθε engaged εχθρός ρίχνει 1 ζαριά
        enemy_rolls = []
        for idx, char2 in enumerate(engaged_enemies):
            battle2_dice, battle2_mod, battle2_total = self.roll_d20(char2.get_effective_stat("Μάχη"))
            original_index = char2_list.index(char2)
            enemy_rolls.append((char2, original_index, battle2_dice, battle2_mod, battle2_total))
            result += f"Χαρακτήρας 2.{original_index+1}: d20({battle2_dice}) + {battle2_mod} = {battle2_total}\n"

        result += "\n=== ΑΠΟΤΕΛΕΣΜΑΤΑ ΖΕΥΓΩΝ ===\n"

        # Συγκρίνουμε κάθε ζεύγος και ρίχνουμε ζημιά
        for idx in range(num_engaged):
            char1_dice, char1_mod, char1_total = char1_rolls[idx]
            char2, original_index, char2_dice, char2_mod, char2_total = enemy_rolls[idx]

            result += f"\nΖεύγος {idx+1}: {char1.name} ({char1_total}) vs Χαρ2.{original_index+1} ({char2_total})\n"

            # Καθορισμός νικητή του ζεύγους
            if char1_total > char2_total:
                winner_name = char1.name
                char1_wins_pair = True
            elif char2_total > char1_total:
                winner_name = f"Χαρ2.{original_index+1}"
                char1_wins_pair = False
            else:
                # Ισοβαθμία - συντελεστής
                if char1_mod > char2_mod:
                    winner_name = f"{char1.name} (συντελεστής)"
                    char1_wins_pair = True
                elif char2_mod > char1_mod:
                    winner_name = f"Χαρ2.{original_index+1} (συντελεστής)"
                    char1_wins_pair = False
                else:
                    result += "Πλήρης ισοβαθμία - κανένας δεν ρίχνει ζημιά\n"
                    continue

            result += f"Νικητής: {winner_name}\n"

            # Ο νικητής ρίχνει ζημιά
            if char1_wins_pair:
                # Ο Χαρ1 ρίχνει ζημιά στον εχθρό
                dmg_dice, dmg_mod, damage_roll = self.roll_d20(char1.get_effective_stat("Ζημιά"))
                end_dice, end_mod, endurance_roll = self.roll_d20(char2.get_effective_stat("Αντοχή"))

                damage_display = self.format_dice_roll("Ζημιά", dmg_dice, dmg_mod, damage_roll)
                endurance_display = self.format_dice_roll("Αντοχή", end_dice, end_mod, endurance_roll)

                result += f"{damage_display} vs {endurance_display}\n"

                damage_diff = damage_roll - endurance_roll
                had_two_wounds = char2.wounds >= 2

                # Τσιράκι: πεθαίνει με οποιαδήποτε επιτυχή ζημιά
                if char2.is_minion and damage_diff >= 0:
                    result += f"Τσιράκι! (+{damage_diff}) Ο Χαρακτήρας 2.{original_index+1} νικιέται!\n"
                    char2.wounds = 10
                elif damage_diff >= 10:
                    result += f"ΘΑΝΑΤΗΦΟΡΟ ΧΤΥΠΗΜΑ! (+{damage_diff}) Ο Χαρακτήρας 2.{original_index+1} νικιέται!\n"
                    char2.wounds = 10
                elif damage_diff >= 5:
                    result += f"Σοβαρή ζημιά! (+{damage_diff}) 2 λαβωματιές\n"
                    char2.wounds += 2
                elif damage_diff >= 0:
                    result += f"Ζημιά! (+{damage_diff}) 1 λαβωματιά\n"
                    char2.wounds += 1
                else:
                    result += f"Αντέχει τη ζημιά! ({damage_diff})\n"

                # Έλεγχος αν ο char2 είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά
                if not char2.is_minion and had_two_wounds and damage_diff >= 0:
                    result += f"Ο Χαρακτήρας 2.{original_index+1} έχει πάρει πολλές λαβωματιές και νικιέται!\n"
                    char2.wounds = 10
                elif char2.wounds != 10:
                    result += f"Κατάσταση Χαρ2.{original_index+1}: {char2.wounds} λαβωματιές\n"
            else:
                # Ο εχθρός ρίχνει ζημιά στον Χαρ1
                dmg_dice, dmg_mod, damage_roll = self.roll_d20(char2.get_effective_stat("Ζημιά"))
                end_dice, end_mod, endurance_roll = self.roll_d20(char1.get_effective_stat("Αντοχή"))

                damage_display = self.format_dice_roll("Ζημιά", dmg_dice, dmg_mod, damage_roll)
                endurance_display = self.format_dice_roll("Αντοχή", end_dice, end_mod, endurance_roll)

                result += f"{damage_display} vs {endurance_display}\n"

                damage_diff = damage_roll - endurance_roll
                had_two_wounds = char1.wounds >= 2

                if damage_diff >= 10:
                    result += f"ΘΑΝΑΤΗΦΟΡΟ ΧΤΥΠΗΜΑ! (+{damage_diff}) Ο {char1.name} νικιέται!\n"
                    return result, True, char2_list[0]
                elif damage_diff >= 5:
                    result += f"Σοβαρή ζημιά! (+{damage_diff}) 2 λαβωματιές\n"
                    char1.wounds += 2
                elif damage_diff >= 0:
                    result += f"Ζημιά! (+{damage_diff}) 1 λαβωματιά\n"
                    char1.wounds += 1
                else:
                    result += f"Αντέχει τη ζημιά! ({damage_diff})\n"

                # Έλεγχος αν ο char1 είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά
                if had_two_wounds and damage_diff >= 0:
                    result += f"Ο {char1.name} έχει πάρει πολλές λαβωματιές και νικιέται!\n"
                    return result, True, char2_list[0]

        result += f"\nΚατάσταση {char1.name}: {char1.wounds} λαβωματιές\n\n"

        # Έλεγχος αν όλοι οι εχθροί νικήθηκαν
        living_enemies = [char2 for char2 in char2_list if char2.wounds != 10]
        if len(living_enemies) == 0:
            return result, True, char1

        return result, False, None

    def battle_round(self, char1, char2):
        """Εκτελεί έναν γύρο μάχης 1v1 με το νέο σύστημα"""
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

        if battle1_total > battle2_total:
            winner = char1
            loser = char2
            result += f"{char1.name} νικάει τον γύρο!\n"
        elif battle2_total > battle1_total:
            winner = char2
            loser = char1
            result += f"{char2.name} νικάει τον γύρο!\n"
        else:
            # Ισοβαθμία - νικάει όποιος έχει μεγαλύτερο συντελεστή
            if battle1_mod > battle2_mod:
                winner = char1
                loser = char2
                result += f"Ισοβαθμία! {char1.name} νικάει λόγω μεγαλύτερου συντελεστή ({battle1_mod} vs {battle2_mod})!\n"
            elif battle2_mod > battle1_mod:
                winner = char2
                loser = char1
                result += f"Ισοβαθμία! {char2.name} νικάει λόγω μεγαλύτερου συντελεστή ({battle2_mod} vs {battle1_mod})!\n"
            else:
                result += f"Πλήρης ισοβαθμία (ζάρι και συντελεστές)! Ξαναρίχνουμε...\n\n"
                return result, False, None  # Ξαναρίχνουμε

        # Ο νικητής ρίχνει ζημιά
        result += f"\n{winner.name} ρίχνει ζημιά...\n"

        dmg_dice, dmg_mod, damage_roll = self.roll_d20(winner.get_effective_stat("Ζημιά"))
        end_dice, end_mod, endurance_roll = self.roll_d20(loser.get_effective_stat("Αντοχή"))

        damage_display = self.format_dice_roll("Ζημιά", dmg_dice, dmg_mod, damage_roll)
        endurance_display = self.format_dice_roll("Αντοχή", end_dice, end_mod, endurance_roll)

        result += f"{damage_display} vs {endurance_display}\n"

        damage_diff = damage_roll - endurance_roll
        had_two_wounds = loser.wounds >= 2

        # Τσιράκι: πεθαίνει με οποιαδήποτε επιτυχή ζημιά
        if loser.is_minion and damage_diff >= 0:
            result += f"Τσιράκι! (+{damage_diff}) Ο {loser.name} νικιέται!\n"
            return result, True, winner
        elif damage_diff >= 10:
            result += f"ΘΑΝΑΤΗΦΟΡΟ ΧΤΥΠΗΜΑ! (+{damage_diff}) Ο {loser.name} νικιέται!\n"
            return result, True, winner
        elif damage_diff >= 5:
            result += f"Σοβαρή ζημιά! (+{damage_diff}) 2 λαβωματιές\n"
            loser.wounds += 2
        elif damage_diff >= 0:
            result += f"Ζημιά! (+{damage_diff}) 1 λαβωματιά\n"
            loser.wounds += 1
        else:
            result += f"Αντέχει τη ζημιά! ({damage_diff})\n"

        # Έλεγχος αν ο loser είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά (μόνο αν δεν είναι τσιράκι)
        if not loser.is_minion and had_two_wounds and damage_diff >= 0:
            result += f"Ο {loser.name} έχει πάρει πολλές λαβωματιές και νικιέται!\n"
            return result, True, winner

        result += f"Κατάσταση {loser.name}: {loser.wounds} λαβωματιές\n\n"
        return result, False, None

    def battle_round_silent(self, char1, char2):
        """Εκτελεί έναν γύρο μάχης χωρίς output"""
        # Ζαριές μάχης
        _, _, battle1_total = self.roll_d20(char1.get_effective_stat("Μάχη"))
        _, _, battle2_total = self.roll_d20(char2.get_effective_stat("Μάχη"))

        winner = None
        loser = None

        if battle1_total > battle2_total:
            winner = char1
            loser = char2
        elif battle2_total > battle1_total:
            winner = char2
            loser = char1
        else:
            # Ισοβαθμία - ελέγχουμε συντελεστές
            char1_mod = char1.get_effective_stat("Μάχη")
            char2_mod = char2.get_effective_stat("Μάχη")
            if char1_mod > char2_mod:
                winner = char1
                loser = char2
            elif char2_mod > char1_mod:
                winner = char2
                loser = char1
            else:
                return False, None  # Ξαναρίχνουμε

        # Ζημιά
        _, _, damage_roll = self.roll_d20(winner.get_effective_stat("Ζημιά"))
        _, _, endurance_roll = self.roll_d20(loser.get_effective_stat("Αντοχή"))

        damage_diff = damage_roll - endurance_roll
        had_two_wounds = loser.wounds >= 2

        # Τσιράκι: πεθαίνει με οποιαδήποτε επιτυχή ζημιά
        if loser.is_minion and damage_diff >= 0:
            return True, winner
        elif damage_diff >= 10:
            return True, winner
        elif damage_diff >= 5:
            loser.wounds += 2
        elif damage_diff >= 0:
            loser.wounds += 1

        # Έλεγχος αν ο loser είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά (μόνο αν δεν είναι τσιράκι)
        if not loser.is_minion and had_two_wounds and damage_diff >= 0:
            return True, winner

        return False, None

    def battle_round_silent_multiple(self, char1, char2_list, max_engaged):
        """Εκτελεί έναν γύρο μάχης με πολλαπλούς αντιπάλους χωρίς output - ΖΕΥΓΗ 1v1"""
        # Βρίσκουμε τους ζωντανούς εχθρούς
        alive_enemies = [char2 for char2 in char2_list if char2.wounds != 10]

        # Χωρίζουμε σε engaged και reserves
        engaged_enemies = alive_enemies[:max_engaged]
        num_engaged = len(engaged_enemies)

        # Ποινή για πολλαπλούς εχθρούς: -N για N εχθρούς (από -2 για 2 εχθρούς και πάνω)
        outnumbered_penalty = 0
        if num_engaged >= 2:
            outnumbered_penalty = -num_engaged

        # Ο Χαρ1 ρίχνει Ν ζαριές μάχης (με ποινή)
        char1_base_mod = char1.get_effective_stat("Μάχη")
        char1_effective_mod = char1_base_mod + outnumbered_penalty

        char1_rolls = []
        for i in range(num_engaged):
            _, _, battle1_total = self.roll_d20(char1_effective_mod)
            char1_rolls.append(battle1_total)

        char1_mod = char1_effective_mod

        # Κάθε engaged εχθρός ρίχνει 1 ζαριά
        enemy_data = []
        for char2 in engaged_enemies:
            _, _, battle2_total = self.roll_d20(char2.get_effective_stat("Μάχη"))
            battle2_mod = char2.get_effective_stat("Μάχη")
            enemy_data.append((char2, battle2_total, battle2_mod))

        # Συγκρίνουμε κάθε ζεύγος και ρίχνουμε ζημιά
        for idx in range(num_engaged):
            char1_total = char1_rolls[idx]
            char2, char2_total, char2_mod = enemy_data[idx]

            # Καθορισμός νικητή του ζεύγους
            char1_wins_pair = False
            if char1_total > char2_total:
                char1_wins_pair = True
            elif char1_total == char2_total:
                if char1_mod > char2_mod:
                    char1_wins_pair = True
                elif char1_mod == char2_mod:
                    continue  # Πλήρης ισοβαθμία - κανένας δεν ρίχνει ζημιά

            # Ο νικητής ρίχνει ζημιά
            if char1_wins_pair:
                # Ο Χαρ1 ρίχνει ζημιά στον εχθρό
                _, _, damage_roll = self.roll_d20(char1.get_effective_stat("Ζημιά"))
                _, _, endurance_roll = self.roll_d20(char2.get_effective_stat("Αντοχή"))

                damage_diff = damage_roll - endurance_roll
                had_two_wounds = char2.wounds >= 2

                # Τσιράκι: πεθαίνει με οποιαδήποτε επιτυχή ζημιά
                if char2.is_minion and damage_diff >= 0:
                    char2.wounds = 10
                elif damage_diff >= 10:
                    char2.wounds = 10
                elif damage_diff >= 5:
                    char2.wounds += 2
                elif damage_diff >= 0:
                    char2.wounds += 1

                # Έλεγχος αν ο char2 είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά
                if not char2.is_minion and had_two_wounds and damage_diff >= 0:
                    char2.wounds = 10
            else:
                # Ο εχθρός ρίχνει ζημιά στον Χαρ1
                _, _, damage_roll = self.roll_d20(char2.get_effective_stat("Ζημιά"))
                _, _, endurance_roll = self.roll_d20(char1.get_effective_stat("Αντοχή"))

                damage_diff = damage_roll - endurance_roll
                had_two_wounds = char1.wounds >= 2

                if damage_diff >= 10:
                    return True, char2_list[0]
                elif damage_diff >= 5:
                    char1.wounds += 2
                elif damage_diff >= 0:
                    char1.wounds += 1

                # Έλεγχος αν ο char1 είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά
                if had_two_wounds and damage_diff >= 0:
                    return True, char2_list[0]

        # Έλεγχος αν όλοι οι εχθροί νικήθηκαν
        living_enemies = [char2 for char2 in char2_list if char2.wounds != 10]
        if len(living_enemies) == 0:
            return True, char1

        return False, None

    def simulate_battle_silent(self, char1_stats, char2_stats, char2_number=1, char2_engaged=1, char2_minion=False):
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
                battle_ended, winner = self.battle_round_silent(char1, char2_list[0])
            else:
                battle_ended, winner = self.battle_round_silent_multiple(char1, char2_list, char2_engaged)

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
                char2_number, char2_engaged, self.char2_minion.get()
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
        result = f"=== ΑΠΟΤΕΛΕΣΜΑΤΑ 1000 ΜΑΧΩΩΝ ===\n"
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
                char2_number, char2_engaged, self.char2_minion.get()
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
        result = f"=== ΑΠΟΤΕΛΕΣΜΑΤΑ 100000 ΜΑΧΩΩΝ ===\n"
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
            result = "=== ΜΑΧΗ ΧΑΡΑΚΤΗΡΩΝ - ΕΝΑΛΛΑΚΤΙΚΟ ΣΥΣΤΗΜΑ (Ζεύγη 1v1) ===\n\n"
        else:
            result = f"=== ΜΑΧΗ ΧΑΡΑΚΤΗΡΩΝ - ΕΝΑΛΛΑΚΤΙΚΟ ΣΥΣΤΗΜΑ (Ζεύγη 1v1) ===\n"
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

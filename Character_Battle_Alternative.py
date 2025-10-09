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

    def get_effective_stat(self, stat_name):
        """Υπολογίζει το τελικό stat με penalties"""
        base_value = self.current_stats[stat_name]

        # Penalty από λαβωματιές για αντοχή
        if stat_name in ["Αντοχή"]:
            base_value -= self.wounds

        # Penalty από κόπωση για μάχη/ζημιά
        if stat_name in ["Μάχη", "Ζημιά"]:
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

        # Τσιράκι checkbox
        minion_row = len(self.stats) + 5
        ttk.Label(main_frame, text="Τσιράκι").grid(row=minion_row, column=0, sticky=tk.E, padx=(0, 10), pady=5)

        # Empty space for Character 1 column
        ttk.Label(main_frame, text="").grid(row=minion_row, column=1, padx=10, pady=5)

        # Minion checkbox for Character 2
        self.char2_minion = tk.BooleanVar()
        minion_checkbox2 = ttk.Checkbutton(main_frame, variable=self.char2_minion)
        minion_checkbox2.grid(row=minion_row, column=2, padx=10, pady=5)

        # Battle buttons
        single_battle_btn = ttk.Button(main_frame, text="Μονομαχία", command=self.single_battle)
        single_battle_btn.grid(row=len(self.stats) + 6, column=0, columnspan=3, pady=10)

        thousand_battles_btn = ttk.Button(main_frame, text="1000 μάχες", command=self.thousand_battles)
        thousand_battles_btn.grid(row=len(self.stats) + 7, column=0, columnspan=3, pady=10)

        ten_thousand_battles_btn = ttk.Button(main_frame, text="10000 μάχες", command=self.ten_thousand_battles)
        ten_thousand_battles_btn.grid(row=len(self.stats) + 8, column=0, columnspan=3, pady=10)

        # Result text area
        result_frame = ttk.LabelFrame(main_frame, text="Αποτέλεσμα", padding="10")
        result_frame.grid(row=len(self.stats) + 9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

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
        main_frame.rowconfigure(len(self.stats) + 9, weight=1)

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

    def battle_round_multiple(self, char1, char2_list):
        """Εκτελεί έναν γύρο μάχης με πολλαπλούς αντιπάλους"""
        result = f"--- Γύρος Μάχης ---\n"

        # Ζαριά μάχης του χαρακτήρα 1
        battle1_dice, battle1_mod, battle1_total = self.roll_d20(char1.get_effective_stat("Μάχη"))
        battle1_display = self.format_dice_roll("Μάχη", battle1_dice, battle1_mod, battle1_total)
        result += f"{char1.name}: {battle1_display}\n"

        # Ζαριές μάχης όλων των χαρακτήρων 2
        char2_results = []
        char1_wins = True

        for i, char2 in enumerate(char2_list):
            if char2.wounds == 10:  # Νεκρός χαρακτήρας (θανατηφόρο χτύπημα)
                continue

            battle2_dice, battle2_mod, battle2_total = self.roll_d20(char2.get_effective_stat("Μάχη"))
            battle2_display = self.format_dice_roll("Μάχη", battle2_dice, battle2_mod, battle2_total)
            result += f"Χαρακτήρας 2.{i+1}: {battle2_display}\n"

            char2_results.append((char2, battle2_total, battle2_mod))

            # Έλεγχος αν ο χαρακτήρας 1 νικάει αυτόν τον αντίπαλο
            if battle1_total < battle2_total:
                char1_wins = False
            elif battle1_total == battle2_total and battle1_mod <= battle2_mod:
                char1_wins = False

        if char1_wins:
            result += f"\n{char1.name} νικάει όλους!\n"

            # Ο χαρακτήρας 1 ρίχνει ζημιά σε όλους
            result += f"\n{char1.name} ρίχνει ζημιά σε όλους...\n"

            dmg_dice, dmg_mod, damage_roll = self.roll_d20(char1.get_effective_stat("Ζημιά"))
            damage_display = self.format_dice_roll("Ζημιά", dmg_dice, dmg_mod, damage_roll)

            defeated_chars = []

            for i, (char2, _, _) in enumerate(char2_results):
                end_dice, end_mod, endurance_roll = self.roll_d20(char2.get_effective_stat("Αντοχή"))
                endurance_display = self.format_dice_roll("Αντοχή", end_dice, end_mod, endurance_roll)

                result += f"Χαρακτήρας 2.{i+1}: {damage_display} vs {endurance_display}\n"

                damage_diff = damage_roll - endurance_roll
                had_two_wounds = char2.wounds >= 2

                # Τσιράκι: πεθαίνει με οποιαδήποτε επιτυχή ζημιά
                if char2.is_minion and damage_diff >= 0:
                    result += f"Τσιράκι! (+{damage_diff}) Ο Χαρακτήρας 2.{i+1} νικιέται!\n"
                    char2.wounds = 10  # Σημάδι νίκης
                    defeated_chars.append(char2)
                elif damage_diff >= 10:
                    result += f"ΘΑΝΑΤΗΦΟΡΟ ΧΤΥΠΗΜΑ! (+{damage_diff}) Ο Χαρακτήρας 2.{i+1} νικιέται!\n"
                    char2.wounds = 10  # Σημάδι νίκης
                    defeated_chars.append(char2)
                elif damage_diff >= 5:
                    result += f"Σοβαρή ζημιά! (+{damage_diff}) 2 λαβωματιές, 1 κόπωση\n"
                    char2.wounds += 2
                    char2.add_fatigue()
                elif damage_diff >= 0:
                    result += f"Ζημιά! (+{damage_diff}) 1 λαβωματιά, 1 κόπωση\n"
                    char2.add_wound()
                else:
                    result += f"Αντέχει τη ζημιά! ({damage_diff})\n"

                # Έλεγχος αν ο char2 είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά (μόνο αν δεν είναι τσιράκι)
                if not char2.is_minion and had_two_wounds and damage_diff >= 0:
                    result += f"Ο Χαρακτήρας 2.{i+1} έχει πάρει πολλές λαβωματιές και νικιέται!\n"
                    char2.wounds = 10  # Σημάδι νίκης
                    defeated_chars.append(char2)
                elif char2.wounds != 10:  # Μόνο αν δεν νικήθηκε ήδη
                    result += f"Κατάσταση Χαρακτήρας 2.{i+1}: {char2.wounds} λαβωματιές, {char2.fatigue} κόπωση\n"

                result += "\n"

            # Έλεγχος αν όλοι οι χαρακτήρες 2 νικήθηκαν (θανατηφόρα χτυπήματα)
            living_enemies = [char2 for char2 in char2_list if char2.wounds != 10]
            if len(living_enemies) == 0:
                return result, True, char1

        else:
            result += f"\nΟι αντίπαλοι νικούν!\n"

            # Όλοι οι χαρακτήρες 2 ρίχνουν ζημιά
            result += f"\nΌλοι οι αντίπαλοι ρίχνουν ζημιά...\n"

            total_damage_taken = 0

            for i, (char2, _, _) in enumerate(char2_results):
                dmg_dice, dmg_mod, damage_roll = self.roll_d20(char2.get_effective_stat("Ζημιά"))
                end_dice, end_mod, endurance_roll = self.roll_d20(char1.get_effective_stat("Αντοχή"))

                damage_display = self.format_dice_roll("Ζημιά", dmg_dice, dmg_mod, damage_roll)
                endurance_display = self.format_dice_roll("Αντοχή", end_dice, end_mod, endurance_roll)

                result += f"Χαρακτήρας 2.{i+1}: {damage_display} vs {endurance_display}\n"

                damage_diff = damage_roll - endurance_roll
                had_two_wounds = char1.wounds >= 2

                if damage_diff >= 10:
                    result += f"ΘΑΝΑΤΗΦΟΡΟ ΧΤΥΠΗΜΑ! (+{damage_diff}) Ο {char1.name} νικιέται!\n"
                    return result, True, char2_list[0]  # Οποιοσδήποτε από τους νικητές
                elif damage_diff >= 5:
                    result += f"Σοβαρή ζημιά! (+{damage_diff}) 2 λαβωματιές, 1 κόπωση\n"
                    char1.wounds += 2
                    char1.add_fatigue()
                elif damage_diff >= 0:
                    result += f"Ζημιά! (+{damage_diff}) 1 λαβωματιά, 1 κόπωση\n"
                    char1.add_wound()
                else:
                    result += f"Αντέχει τη ζημιά! ({damage_diff})\n"

                # Έλεγχος αν ο char1 είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά
                if had_two_wounds and damage_diff >= 0:
                    result += f"Ο {char1.name} έχει πάρει πολλές λαβωματιές και νικιέται!\n"
                    return result, True, char2_list[0]  # Οποιοσδήποτε από τους νικητές

                result += "\n"

            result += f"Κατάσταση {char1.name}: {char1.wounds} λαβωματιές, {char1.fatigue} κόπωση\n\n"

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
            result += f"Σοβαρή ζημιά! (+{damage_diff}) 2 λαβωματιές, 1 κόπωση\n"
            loser.wounds += 2
            loser.add_fatigue()
        elif damage_diff >= 0:
            result += f"Ζημιά! (+{damage_diff}) 1 λαβωματιά, 1 κόπωση\n"
            loser.add_wound()
        else:
            result += f"Αντέχει τη ζημιά! ({damage_diff})\n"

        # Έλεγχος αν ο loser είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά (μόνο αν δεν είναι τσιράκι)
        if not loser.is_minion and had_two_wounds and damage_diff >= 0:
            result += f"Ο {loser.name} έχει πάρει πολλές λαβωματιές και νικιέται!\n"
            return result, True, winner

        result += f"Κατάσταση {loser.name}: {loser.wounds} λαβωματιές, {loser.fatigue} κόπωση\n\n"
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
            loser.add_fatigue()
        elif damage_diff >= 0:
            loser.add_wound()

        # Έλεγχος αν ο loser είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά (μόνο αν δεν είναι τσιράκι)
        if not loser.is_minion and had_two_wounds and damage_diff >= 0:
            return True, winner

        return False, None

    def battle_round_silent_multiple(self, char1, char2_list):
        """Εκτελεί έναν γύρο μάχης με πολλαπλούς αντιπάλους χωρίς output"""
        # Ζαριά μάχης του χαρακτήρα 1
        _, _, battle1_total = self.roll_d20(char1.get_effective_stat("Μάχη"))
        battle1_mod = char1.get_effective_stat("Μάχη")

        # Ζαριές μάχης όλων των χαρακτήρων 2
        char2_results = []
        char1_wins = True

        for char2 in char2_list:
            if char2.wounds == 10:  # Νεκρός χαρακτήρας (θανατηφόρο χτύπημα)
                continue

            _, _, battle2_total = self.roll_d20(char2.get_effective_stat("Μάχη"))
            battle2_mod = char2.get_effective_stat("Μάχη")

            char2_results.append((char2, battle2_total, battle2_mod))

            # Έλεγχος αν ο χαρακτήρας 1 νικάει αυτόν τον αντίπαλο
            if battle1_total < battle2_total:
                char1_wins = False
            elif battle1_total == battle2_total and battle1_mod <= battle2_mod:
                char1_wins = False

        if char1_wins:
            # Ο χαρακτήρας 1 ρίχνει ζημιά σε όλους
            _, _, damage_roll = self.roll_d20(char1.get_effective_stat("Ζημιά"))

            for char2, _, _ in char2_results:
                _, _, endurance_roll = self.roll_d20(char2.get_effective_stat("Αντοχή"))

                damage_diff = damage_roll - endurance_roll
                had_two_wounds = char2.wounds >= 2

                # Τσιράκι: πεθαίνει με οποιαδήποτε επιτυχή ζημιά
                if char2.is_minion and damage_diff >= 0:
                    char2.wounds = 10  # Σημάδι νίκης
                elif damage_diff >= 10:
                    char2.wounds = 10  # Σημάδι νίκης
                elif damage_diff >= 5:
                    char2.wounds += 2
                    char2.add_fatigue()
                elif damage_diff >= 0:
                    char2.add_wound()

                # Έλεγχος αν ο char2 είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά (μόνο αν δεν είναι τσιράκι)
                if not char2.is_minion and had_two_wounds and damage_diff >= 0:
                    char2.wounds = 10  # Σημάδι νίκης

            # Έλεγχος αν όλοι οι χαρακτήρες 2 νικήθηκαν (θανατηφόρα χτυπήματα)
            living_enemies = [char2 for char2 in char2_list if char2.wounds != 10]
            if len(living_enemies) == 0:
                return True, char1

        else:
            # Όλοι οι χαρακτήρες 2 ρίχνουν ζημιά
            for char2, _, _ in char2_results:
                _, _, damage_roll = self.roll_d20(char2.get_effective_stat("Ζημιά"))
                _, _, endurance_roll = self.roll_d20(char1.get_effective_stat("Αντοχή"))

                damage_diff = damage_roll - endurance_roll
                had_two_wounds = char1.wounds >= 2

                if damage_diff >= 10:
                    return True, char2_list[0]  # Οποιοσδήποτε από τους νικητές
                elif damage_diff >= 5:
                    char1.wounds += 2
                    char1.add_fatigue()
                elif damage_diff >= 0:
                    char1.add_wound()

                # Έλεγχος αν ο char1 είχε >=2 λαβωματιές και μόλις λαβώθηκε ξανά
                if had_two_wounds and damage_diff >= 0:
                    return True, char2_list[0]  # Οποιοσδήποτε από τους νικητές

        return False, None

    def simulate_battle_silent(self, char1_stats, char2_stats, char1_indomitable, char2_indomitable, char1_overexertion, char2_overexertion, char1_never_stunned, char2_never_stunned, char2_number=1, char2_minion=False):
        """Προσομοιώνει μια μάχη χωρίς output"""
        char1 = Character("Χαρακτήρας 1", char1_stats, char1_indomitable, char1_overexertion, char1_never_stunned)

        # Δημιουργία πολλαπλών χαρακτήρων 2
        char2_list = []
        for i in range(char2_number):
            char2 = Character(f"Χαρακτήρας 2.{i+1}", char2_stats, char2_indomitable, char2_overexertion, char2_never_stunned, char2_minion)
            char2_list.append(char2)

        round_count = 0
        while round_count < 100:  # Safety limit
            round_count += 1

            if char2_number == 1:
                battle_ended, winner = self.battle_round_silent(char1, char2_list[0])
            else:
                battle_ended, winner = self.battle_round_silent_multiple(char1, char2_list)

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
            self.result_text.insert(tk.END, f"Εκτελούνται 1000 μάχες (1 vs {char2_number})...\n\n")
        self.root.update()

        for i in range(1000):
            winner, rounds = self.simulate_battle_silent(
                char1_stats, char2_stats,
                self.char1_indomitable.get(), self.char2_indomitable.get(),
                self.char1_overexertion.get(), self.char2_overexertion.get(),
                self.char1_never_stunned.get(), self.char2_never_stunned.get(),
                char2_number, self.char2_minion.get()
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

    def ten_thousand_battles(self):
        """Εκτελεί 10000 μάχες και εμφανίζει στατιστικά"""
        char1_stats = self.get_character_stats(self.char1_entries)
        char2_stats = self.get_character_stats(self.char2_entries)
        char2_number = self.get_char2_number()

        char1_wins = 0
        char2_wins = 0
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
            winner, rounds = self.simulate_battle_silent(
                char1_stats, char2_stats,
                self.char1_indomitable.get(), self.char2_indomitable.get(),
                self.char1_overexertion.get(), self.char2_overexertion.get(),
                self.char1_never_stunned.get(), self.char2_never_stunned.get(),
                char2_number, self.char2_minion.get()
            )
            total_rounds += rounds
            min_rounds = min(min_rounds, rounds)
            max_rounds = max(max_rounds, rounds)
            if winner == 1:
                char1_wins += 1
            elif winner == 2:
                char2_wins += 1

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
            result = "=== ΜΑΧΗ ΧΑΡΑΚΤΗΡΩΝ - ΕΝΑΛΛΑΚΤΙΚΟ ΣΥΣΤΗΜΑ ===\n\n"
        else:
            result = f"=== ΜΑΧΗ ΧΑΡΑΚΤΗΡΩΝ - ΕΝΑΛΛΑΚΤΙΚΟ ΣΥΣΤΗΜΑ ===\n"
            result += f"Χαρακτήρας 1 εναντίον {char2_number} αντιπάλων!\n\n"

        round_count = 0
        while round_count < 50:  # Safety limit
            round_count += 1
            result += f"Γύρος {round_count}:\n"

            if char2_number == 1:
                round_result, battle_ended, winner = self.battle_round(char1, char2_list[0])
            else:
                round_result, battle_ended, winner = self.battle_round_multiple(char1, char2_list)

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
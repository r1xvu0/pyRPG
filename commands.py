from main import *
from items import *
from skills import *
from mobs import *
import random

lowkey_lvl = 0


# Basic commands
def commands(comm):
    global lowkey_lvl
    if in_battle == 0:
        if comm == "inventory" or comm == "inv":
            check_inv()
        elif comm == "skill" or comm == "skills":
            check_skill()
        elif comm == "stats" or comm == "stat":
            check_stats()
        elif comm == "equip" or comm == "eq":
            equip()
        # DELETE LVLUP COMM
        elif comm == "lvlup":
            if int(p_exp) >= int(level_threshold[lowkey_lvl]):
                lowkey_lvl += 1
                print("LEVEL UP!")
                lvlup()
                print("")
            else:
                print(f"You need {int(level_threshold[lowkey_lvl]) - int(p_exp)} more EXP to level up!")
                print("")
        elif comm == "battle":
            battle()
        elif comm == "randomloot":
            randomloot()
        elif comm == "uskill":
            use_skill()
        elif comm == "sell":
            sell()
        elif comm == "show":
            show()
        elif comm == "info":
            info()
        elif comm == "about":
            about()


# Check inventory
def check_inv():
    i = 0
    for item in inventory:
        print(f"{i}. {item}")
        i += 1
    print(f"{p_gold} Gold")
    name = input("Item Name: >> ")
    if name in inventory:
        if name in items["Weapons"] and name in inventory:
            wName = items["Weapons"][name]["Name"]
            wDamage = items["Weapons"][name]["Damage"]
            wPrice = items["Weapons"][name]["Price"]

            print(f"Name: {wName}\nDamage: {wDamage}\nPrice: {wPrice}")
        elif name in items["Shields"] and name in inventory:
            sName = items["Shields"][name]["Name"]
            sDefense = items["Shields"][name]["Defense"]
            sPrice = items["Shields"][name]["Price"]

            print(f"Name: {sName}\nDefense: {sDefense}\nPrice: {sPrice}")
        elif name in items["Armors"] and name in inventory:
            aName = items["Armors"][name]["Name"]
            aDefense = items["Armors"][name]["Defense"]
            aPrice = items["Armors"][name]["Price"]

            print(f"Name: {aName}\nDefense: {aDefense}\nPrice: {aPrice}")

        else:
            return
    else:
        return


# Check available skills
def check_skill():
    i = 0
    for skill in p_skills:
        print(f"{i}. {skill}")
        i += 1
    skill = input("Skill Name: >> ")

    if skill in p_skills and skill in skills:
        skill_mult = skills[skill]["Damage_Multiplier"]
        skill_cost = skills[skill]["Stamina_Cost"]
        print(f"Skill: {skill}\nDamage Multiplier: {skill_mult}\nStamina Cost: {skill_cost}")
    else:
        print("Skill not learned, or exists")


# Show stats
def check_stats():
    combined_defense = p_defense + p_eqADefenseNum[0] + p_eqSDefenseNum[0]

    print(f"Player EXP: {p_exp} | Level: {p_level}")
    print(f"Player Max Health: {p_health_max}HP ({p_vitality * 2.5}HP from Vitality)")
    print(f"Player Health: {p_health_current}HP")
    print(f"Damage: {p_eqWPowerNum[0]} ({p_eqWeapon[0]})")
    print(f"Strength: {p_strength} STR")
    print(f"Vitality: {p_vitality} VIT")
    print(f"Stamina: {p_stamina} STA")
    print(f"Defense: {combined_defense} DEF ({p_eqArmor[0]} + {p_eqADefenseNum[0]} | {p_eqShield[0]} + {p_eqSDefenseNum[0]} | Base + {p_defense})")
    print(f"Critical Multiplier: {p_critmulti}x")


# Roll the dice for BATTLES
def rtd():
    global p_health_current
    global en_hp
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    self_flagellation = random.randint(2, 5)
    combined_str = dice1 + dice2 + (p_strength * 0.5) + p_eqWPowerNum[0]
    flag_combined = (p_eqWPowerNum[0] + p_strength) / self_flagellation
    print(dice1, dice2)
    if dice1 == 1 or dice2 == 1:
        if dice1 == 1 and dice2 == 1:
            print("Aw snap! Weak Hands")
            print(f"You hurt yourself for {flag_combined} points of Damage")
            print("")
            p_health_current -= flag_combined
            return p_health_current
        else:
            print(f"Your attack has missed the {en_name[0]}")
            print("")
    elif dice1 == dice2:
        print("Critical Hit!")
        print(f"You hit {en_name[0]} for {combined_str*p_critmulti} points of Damage")
        print("")
        en_hp[0] -= combined_str*p_critmulti
    else:
        print(f"You hit for {combined_str} points of Damage")
        print("")
        en_hp[0] -= combined_str


def en_rtd():
    global p_health_current
    global en_str, en_sta
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    skill_dice = random.randint(1, 12)
    self_flagellation = (dice1 + dice2 + (en_str[0] * 0.5)) / 2
    enemy_dmg = (dice1 + dice2 + en_str[0]) - p_totalDefense
    reduced_dmg = (dice1 + dice2 + en_str[0]) - p_totalDefense
    print(f"Enemy has RTD'd {dice1} and {dice2}!")
    if dice1 == 1 or dice2 == 1:
        if dice1 == 1 and dice2 == 1:
            print(f"The {en_name[0]} is confused and hit itself for {self_flagellation}")
            print("")
            en_hp[0] -= self_flagellation
            return en_hp
        else:
            print(f"{en_name[0]} has missed it's attack!")
            print("")
    elif dice1 == dice2:
        if reduced_dmg <= 0:
            print(f"{en_name[0]} has Criticaly Hit you for 0 points of damage! (reduced by {p_totalDefense})")
            print("")
            p_health_current -= 0
        else:
            print(f"{en_name[0]} has Criticaly Hit you for {reduced_dmg*1.6} points of damage! (reduced by {p_totalDefense})")
            print("")
            p_health_current -= reduced_dmg * 1.6
            return p_health_current
    else:
        if reduced_dmg <= 0:
            print(f"{en_name[0]} hits you for 0 points of damage! (reduced by {p_totalDefense})")
            print("")
            p_health_current -= 0
        else:
            print(f"{en_name[0]} hits you for {reduced_dmg} points of damage! (reduced by {p_totalDefense})")
            print("")
            p_health_current -= enemy_dmg
            return p_health_current


# Use available skill
def use_skill():
    global p_stamina
    global p_stamina_max
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    i = 0
    sta_cost = []
    skill_damage = []
    for skill in p_skills:
        skill_cost = skills[skill]["Stamina_Cost"]
        sk_damage = skills[skill]["STR_Multiplier"]
        print(f"{i}. {skill} - Costs {skill_cost} STA per use")
        sta_cost.append(skill_cost)
        skill_damage.append(sk_damage)
        i += 1
    print(f"You have {p_stamina} / {p_stamina_max} Stamina")

    try:
        try:
            use = int(input("Which skill you want to use?: >> "))
            print(use)
            if p_skills[use] in p_skills:
                dmg_cnt = (dice1 + dice2 + p_eqWPowerNum[0] + (p_strength * 0.5)) * skill_damage[use]
                if p_stamina < sta_cost[use]:
                    print("Not enough Stamina!")
                    print("")
                    use_skill()
                else:
                    print(f"Using {p_skills[use]} for {sta_cost[use]} Stamina point/s!")
                    print(f"{p_skills[use]} dealt {dmg_cnt} points of damage to {en_name[0]}")
                    print("")
                    en_hp[0] -= dmg_cnt
                    p_stamina -= sta_cost[use]
                    return en_hp[0], p_stamina
        except ValueError:
            print("No such Skill in your Skill List!")
            print("")
            use_skill()
    except IndexError:
        print("No such Skill in your Skill List!")
        print("")
        use_skill()


def use_item():
    global p_health_current
    global p_stamina
    global p_eqWPowerNum
    global consumables_quant
    print("")
    i = 0
    q_items = []
    hp_restore = []
    sta_restore = []
    dmg_mult = []
    desc = []
    for item in consumables:
        hp_restore.append(items["Consumables"][item]["HP_Restore"])
        sta_restore.append(items["Consumables"][item]["STA_Restore"])
        dmg_mult.append(items["Consumables"][item]["Damage_Multiplier"])
        desc.append(items["Consumables"][item]["Desc"])
        quant = consumables_quant[item]["quant"]
        print(f"{i}. {item} {quant}x - {desc[0]}")
        q_items.append(quant)
        i += 1

    print("")
    use = int(input("Which item you want to use? >> "))
    if consumables[use] in consumables:
        p_health_current += hp_restore[use]
        p_stamina += sta_restore[use]
        p_eqWPowerNum[0] += (p_eqWPowerNum[0] / 100) * 0.25
        hp_restore.clear()
        sta_restore.clear()
        dmg_mult.clear()
        desc.clear()
        consumables.pop(use)

        print("")
        return p_health_current, p_stamina, p_eqWPowerNum, consumables_quant
    else:
        hp_restore.clear()
        sta_restore.clear()
        dmg_mult.clear()
        desc.clear()
        print(f"Such item does not exist in your inventory")



    print("")

# Equip item from inventory
def equip():
    select = int(input("Weapon[1], Armor[2], Shield[3]: >> "))
    print("")
    eq_me = []
    i = 0
    if select == 1:
        for item in items["Weapons"]:
            if item in inventory:
                eq_me.append(item)
                inventory.pop()

        for item in eq_me:
            print(f"{i}. {item}")
            i += 1
        try:
            equip = input("Choose number of item to equip: >> ")
            print("")
            eq_int = int(equip)
            equip_name = eq_me[eq_int]
            if equip_name in eq_me:
                p_eqWeapon.pop()
                p_eqWeapon.append(equip_name)
                p_eqWPowerNum.pop()
                p_eqWPower = items["Weapons"][p_eqWeapon[0]]["Damage"]
                p_eqWPowerNum.append(p_eqWPower)
                for item in eq_me:
                    inventory.append(item)
                print(f"You equipped {eq_me[eq_int]}")
                print("")
                eq_me.clear()
            else:
                print("No such weapon with that name")
                print("")
        except IndexError:
            print("No such weapon with that name!")
            print("")

    if select == 2:
        for item in items["Armors"]:
            if item in inventory:
                eq_me.append(item)

        for item in eq_me:
            print(f"{i}. {item}")
            i += 1
        try:
            equip = input("Choose number of item to equip: >> ")
            print("")
            eq_int = int(equip)
            equip_name = eq_me[eq_int]
            if equip_name in eq_me:
                p_eqArmor.pop()
                p_eqArmor.append(equip_name)
                p_eqADefenseNum.pop()
                p_eqADefense = items["Armors"][p_eqArmor[0]]["Defense"]
                p_eqADefenseNum.append(p_eqADefense)
                print(f"You equipped {eq_me[eq_int]} with {p_eqADefenseNum[0]} defense")
                print("")
                return p_eqADefense
            else:
                print("No such armor with that name!")
                print("")
        except IndexError:
            print("No such armor with that name!")
            print("")

    if select == 3:
        for item in items["Shields"]:
            if item in inventory:
                eq_me.append(item)

        for item in eq_me:
            print(f"{i}. {item}")
            i += 1
        try:
            equip = input("Choose number of item to equip: >> ")
            print("")
            eq_int = int(equip)
            equip_name = eq_me[eq_int]
            if equip_name in eq_me:
                p_eqShield.pop()
                p_eqShield.append(equip_name)
                p_eqSDefenseNum.pop()
                p_eqSDefense = items["Shields"][p_eqShield[0]]["Defense"]
                p_eqSDefenseNum.append(p_eqSDefense)
                print(f"You equipped {eq_me[eq_int]}")
                print("")
                eq_me.clear()
            else:
                print("No such shield with that name!")
                print("")
        except IndexError:
            print("No such shield with that name!")
            print("")


# DELETE LVLUP FUNC LATER
def lvlup():
    global p_strength, p_level, p_health_max, p_defense, p_stamina_max, p_vitality, p_health_current, p_stamina
    p_level += 1
    p_strength += 2
    p_health_max += 5
    p_defense += 1
    p_stamina_max += 1
    p_stamina = p_stamina_max
    p_vitality += 3
    p_health_current = p_health_max
    return p_strength, p_level, p_health_max, p_defense, p_stamina, p_vitality, p_health_current, p_stamina


# Show Equipped items
def show():
    print(f"{p_eqWeapon[0]} - Damage {p_eqWPowerNum}")
    print(f"{p_eqArmor[0]} - Defense {p_eqADefenseNum}")
    print(f"{p_eqShield[0]} - Defense {p_eqSDefenseNum}")


# Sell from inventory
def sell():
    global inventory
    global p_gold
    global p_health_current
    global p_eqWeapon
    i = 0
    sell_me = []
    price = []
    temp_inv = []
    try:
        try:
            for item in items["Weapons"]:

                if item in inventory:

                    sell_me.append(item)
                    sell_price = items["Weapons"][item]["Price"]
                    sell_name = items["Weapons"][item]["Name"]
                    price.append(sell_price)
                    temp_inv.append(item)
                    print(f"{i}. {item} - {sell_price}")
                    i += 1

            for item in items["Armors"]:

                if item in inventory:

                    sell_me.append(item)
                    sell_price = items["Armors"][item]["Price"]
                    price.append(sell_price)
                    temp_inv.append(item)
                    print(f"{i}. {item} - {sell_price}")
                    i += 1

            for item in items["Shields"]:

                if item in inventory:

                    sell_me.append(item)
                    sell_price = items["Shields"][item]["Price"]
                    price.append(sell_price)
                    temp_inv.append(item)
                    print(f"{i}. {item} - {sell_price}")
                    i += 1

            sell = int(input("Which item you want to sell? >> "))
            p_gold += price[sell]
            print(f"Sold {sell_me[sell]} for {price[sell]}")
            temp_inv.pop(sell)
            inventory.clear()

            for x in temp_inv:
                inventory.append(x)

            return inventory, p_gold
        except ValueError:
            print("I don't speak gibberish!")
    except IndexError:
        print("Trying to scam me ya fool?!")
        print("*HEAVY PUNCH*")
        heavy_punch = random.randint(5, 20)
        p_health_current -= heavy_punch
        print(f"You've taken {heavy_punch} points of damage!")


# Showcase of commands
def info():
    i = 0
    for cmd in comms:
        print(f"{i}. {cmd}")
        i += 1


# Simple About
def about():
    print('''
    pyRPG v0.2
    Programmed by Yannick
    ''')


def target():
    try:
        print(f"Your target is {p_target[0]} ({rarity_perc[0]}%)")
        print()
    except IndexError:
        print("You have no target")


def battle():
    global p_health_current
    global p_exp, p_stamina
    generate = 1

    if generate == 1:
        generate_enemy()
        generate -= 1
    enemy_hp = monsters[en_rarity[0]][p_target[0]]["HP"]
    enemy_str = monsters[en_rarity[0]][p_target[0]]["STR"]
    #print(f"{p_health_current} / {p_health_max} HP, {p_stamina} / {p_stamina_max} STA")
    #print(f"Enemy HP {enemy_hp}, STR {enemy_str}")
    #print(f"Awards {true_exp} EXPs")
    # BATTLE ITSELF
    while en_hp[0] >= 1 or p_health_current >= 1:

        if p_health_current > p_health_max:
            p_health_current = p_health_max
        if p_stamina > p_stamina_max:
            p_stamina = p_stamina_max
        if p_health_current > p_health_max and p_stamina > p_stamina_max:
            p_health_current = p_health_max
            p_stamina = p_stamina_max

        print("======")
        print(f"Enemy: {en_name[0]}")
        print(f"HP: {en_hp[0]} | STR: {en_str[0]}")
        print("======")
        print(f"HP: {p_health_current} / {p_health_max} | STA: {p_stamina} / {p_stamina_max}")
        print(f"{btl_comms}")

        btl_console = input(f"What will you do to {en_name[0]}? >> ")
        if btl_console == "rtd":
            rtd()
            if en_hp[0] <= 0:
                print(f"Enemy {en_name[0]} has perished!")
                print(f"You have gained {en_exp[0]} points of Experience!")
                print("")
                p_exp += en_exp[0]
                p_stamina = p_stamina_max
                randomloot()
                return p_exp, p_stamina
            else:
                en_rtd()
        elif btl_console == "uskill":
            use_skill()
            if en_hp[0] <= 0:
                print(f"Enemy {en_name[0]} has perished!")
                print(f"You have gained {en_exp[0]} points of Experience!")
                p_exp += en_exp[0]
                p_stamina = p_stamina_max
                randomloot()
                return p_exp, p_stamina
            else:
                en_rtd()
        elif btl_console == "escape":
            p_health_current = p_health_current / 100
            p_stamina = p_stamina_max
            return print(f"You escaped like a fool! {p_health_current}"), p_stamina
        elif btl_console == "uitem":
            use_item()

        if en_hp[0] <= 0:
            print(f"Enemy {en_name[0]} has perished!")
            print(f"You have gained {en_exp[0]} points of Experience!")
            p_exp += en_exp[0]
            p_stamina = p_stamina_max
            randomloot()
        elif p_health_current <= 0:
            print(f"You have died, because your HP has reached {p_health_current}!")
            p_stamina = p_stamina_max
            p_health_current = (p_health_max / 100) * 25
            return p_health_current, p_stamina

    target()
    return


def generate_enemy():
    global p_target
    global en_name ,en_hp, en_str, en_exp, en_rarity, rarity_perc
    global true_exp
    rarity = random.randint(0, 100)
    en_name.clear()
    en_hp.clear()
    en_str.clear()
    en_exp.clear()
    en_rarity.clear()
    rarity_perc.clear()
    p_target.clear()
    print(f"Rarity level {100 - rarity}%")
    rarity_perc.append(rarity)
    if rarity <= 40:
        enem = random.choice(commons_list)
        en_name.append(monsters["Common"][enem]["Name"])
        en_hp.append(monsters["Common"][enem]["HP"])
        en_str.append(monsters["Common"][enem]["STR"])
        en_exp.append(monsters["Common"][enem]["EXP"])
        true_exp = en_exp[0] * (rarity / 100)
        print(f"Your enemy is Common {enem}")
        print(f"Stats: {en_hp[0]} HP, {en_str[0]} STR")
        p_target.append(enem)
        en_rarity.append("Common")
        return p_target, en_rarity, true_exp, rarity_perc

    elif rarity <= 60:
        enem = random.choice(uncommons_list)
        en_name.append(monsters["Uncommon"][enem]["Name"])
        en_hp.append(monsters["Uncommon"][enem]["HP"])
        en_str.append(monsters["Uncommon"][enem]["STR"])
        en_exp.append(monsters["Uncommon"][enem]["EXP"])
        true_exp = en_exp[0] * (rarity / 100)
        print(f"Your enemy is Uncommon {enem}")
        print(f"Stats: {en_hp[0]} HP, {en_str[0]} STR")
        p_target.append(enem)
        en_rarity.append("Uncommon")
        return p_target, en_rarity, true_exp

    elif rarity <= 75:
        enem = random.choice(rares_list)
        en_name.append(monsters["Rare"][enem]["Name"])
        en_hp.append(monsters["Rare"][enem]["HP"])
        en_str.append(monsters["Rare"][enem]["STR"])
        en_exp.append(monsters["Rare"][enem]["EXP"])
        true_exp = en_exp[0] * (rarity / 100)
        print(f"Your enemy is Rare {enem}")
        print(f"Stats: {en_hp[0]} HP, {en_str[0]} STR")
        p_target.append(enem)
        en_rarity.append("Rare")
        return p_target, en_rarity, true_exp

    elif rarity <= 99:
        enem = random.choice(elites_list)
        en_name.append(monsters["Elite"][enem]["Name"])
        en_hp.append(monsters["Elite"][enem]["HP"])
        en_str.append(monsters["Elite"][enem]["STR"])
        en_exp.append(monsters["Elite"][enem]["EXP"])
        true_exp = en_exp[0] * (rarity / 100)
        print(f"Your enemy is Elite {enem}")
        print(f"Stats: {en_hp} HP, {en_str} STR")
        p_target.append(enem)
        en_rarity.append("Elite")
        return p_target, en_rarity, true_exp

    elif rarity == 100:
        enem = random.choice(legendaries_list)
        en_name.append(monsters["Legendary"][enem]["Name"])
        en_hp.append(monsters["Legendary"][enem]["HP"])
        en_str.append(monsters["Legendary"][enem]["STR"])
        en_exp.append(monsters["Legendary"][enem]["EXP"])
        true_exp = en_exp[0] * (rarity / 100)
        print(f"Your enemy is Legendary {enem}")
        print(f"Stats: {en_hp[0]} HP, {en_str[0]} STR")
        print("======")
        p_target.append(enem)
        en_rarity.append("Legendary")
        return p_target, en_rarity, true_exp

    else:
        print("UNEXPECTED ERROR/S")

# Add random loot to inventory
def randomloot():
    global inventory

    for x in range(0, 6, 2):
        loot = random.choice(item_loot_list)

        if loot in inventory:
            print(f"{loot} already in inventory, you leave {loot} forgotten behind!")
        elif loot in consumables:

            consumables.append(loot)
            print(f"{loot} added to your Pouch!")
        else:
            inventory.append(loot)
            print(f"Item {loot} was added to your Inventory!")


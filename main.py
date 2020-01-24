# pyRPG by Yannick
from commands import *
from items import *
from classes import *
from skills import *
from battle import *
from level import *

in_battle = 0

p_level = 1
p_exp = 3200
p_strength = 10
p_intelligence = 2
p_vitality = 5
p_stamina = 5
p_stamina_max = 5
p_defense = 5
p_critmulti = 1.5
p_health_base = 100
p_health_max = p_health_base + (p_vitality * 2.5)
p_health_current = p_health_base + (p_vitality * 2.5)
p_gold = 0


p_skills = ["Bash", "Shield Charge"]

inventory = ["Wooden Shield", "Broadsword", "Zweihander", "Leather Jacket"]
consumables = ["Small HP Potion", "Small DMG Potion"]
consumables_quant = {"Small HP Potion": {"quant": 1}, "Small DMG Potion": {"quant": 1}}

comms = ["inv", "equip", "inventory", "skills", "stats", "info", "about"]
btl_comms = ["rtd", "uskill", "uitem","escape"]

p_eqWeapon = ["Broadsword"]
p_eqWPower = items["Weapons"][p_eqWeapon[0]]["Damage"]
p_eqWPowerNum = [p_eqWPower]
p_eqShield = ["Wooden Shield"]
p_eqSDefense = items["Shields"][p_eqShield[0]]["Defense"]
p_eqSDefenseNum = [p_eqSDefense]
p_eqArmor = ["Leather Jacket"]
p_eqADefense = items["Armors"][p_eqArmor[0]]["Defense"]
p_eqADefenseNum = [p_eqADefense]
p_totalDefense = p_defense + p_eqADefenseNum[0] + p_eqSDefenseNum[0]

p_target = []
en_name = []
en_hp = []
en_str = []
en_sta = []
en_exp = []
en_rarity = []
rarity_perc = []
true_exp = 0


def main():
    global p_eqArmor
    global p_eqWeapon
    runtime = 1

    while runtime == 1:

        choice = input("Commands Test: >> ").lower()
        print("")
        commands(choice)

    if runtime == 2:
        battle()


if __name__ == "__main__":
    main()

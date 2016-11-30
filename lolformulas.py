# Mathmatical formulas and ideas taken straight from the league of legends wiki page.
from random import randint

# Class defines all functions that calculate armor values based on penetration values
class ArmorPenetration():

	# Will get flat armor reduction. Base and bonus armor are split
	# proportionally so we need to account for that.
	# This also causes the player to actually have a reduced armor value.
	def flat_armor_reduction(self, armor_reduction, base_armor, bonus_armor):
		total_armor = base_armor + bonus_armor
		base_armor_proportion = base_armor / total_armor
		bonus_armor_proportion = bonus_armor / total_armor
		base_armor -= (armor_reduction * base_armor_proportion)
		bonus_armor -= (armor_reduction * bonus_armor_proportion)
		return [base_armor, bonus_armor, base_armor + bonus_armor]

	# Percent armor reduction causes the player taking damage to take
	# that damage as if their armor was multiplied by (100 - % reduced)
	# This also causes the player to actually have a reduced armor value.
	def percent_armor_reduction(self, percent_reduction, base_armor, bonus_armor):
		base_armor *= ((100 - percent_reduction) / 100)
		bonus_armor *= ((100 - percent_reduction) / 100)
		return [base_armor, bonus_armor, base_armor + bonus_armor]

	# Percent armor penetration does the same as armor reduction but only
	# effects the targeting player's bonus armor. This is ignored if the 
	# targeted player's base armor is less than 0
	# This is only applied to the damage taken by the player, in other words it does
	# not actually cause the player to lose any armor.
	def percent_armor_pen(self, percent_pen, percent_bonus_pen, base_armor, bonus_armor):
		if (base_armor + bonus_armor) > 0:
			if percent_pen > 0:
				base_armor *= ((100 - percent_pen) / 100)
				bonus_armor *= ((100 - percent_pen) / 100)

			print(str(base_armor) + "   " + str(bonus_armor))
			if percent_bonus_pen > 0:
				bonus_armor *= ((100 - percent_bonus_pen) / 100)

			return [base_armor, bonus_armor, base_armor + bonus_armor]
		else:
			return [base_armor, bonus_armor, base_armor + bonus_armor]

	# Will get the value of a players flat armor penetration based on lethality,
	# Lethality's value is based on the oppopnent being at level 18, so we need
	# to scale it down to the appropriate level in order to get the correct flat pen value.
	def get_lethality_pen(self, base_lethality, enemy_level, total_armor):
		lethality = (0.4 * base_lethality) + ((0.6 * base_lethality * enemy_level) / 18)
		flat_pen = (((0.6 * lethality) * enemy_level) / 18)
		total_flat_pen = (0.4 * lethality) * flat_pen
		return total_flat_pen

	# Will simply deduct the amount of penetration from the amount of armor
	# This is only applied to the damage taken by the player, in other words it does
	# not actually cause the player to lose any armor.
	def flat_armor_pen(self, total_armor, flat_pen):
		if total_armor > 0 and (total_armor - flat_pen) > 0:
			return (total_armor - flat_pen)
		elif total_armor > 0 and (total_armor - flat_pen) <= 0:
			return 0
		else:
			return total_armor

	# Will calculate the total armor value that will be used to calculate the 
	# actual damage that a given player will take
	def calculate_total_armor(self, base_armor, bonus_armor, flat_reduct, 
		percent_reduct, percent_pen, percent_bonus_pen, flat_pen):
		armor_values = self.flat_armor_reduction(flat_reduct, base_armor, bonus_armor)
		armor_values = self.percent_armor_reduction(percent_reduct, armor_values[0], armor_values[1])
		armor_values = self.percent_armor_pen(percent_pen, percent_bonus_pen, armor_values[0], armor_values[1])
		armor_value = self.flat_armor_pen(armor_values[0] + armor_values[1], flat_pen)
		return armor_value

# Class defines all functions that calculate magic resistance based on reduction values
class MagicPenetration():

	# Simply subtracts the magic reduction value from a players magic resist.
	# Flat magic reduction can cause magic resistance to fall below zero.
	# This also causes the player's actual magic resistance to decrease.
	def flat_magic_reduction(self, magic_resist, magic_reduction):
		return (magic_resist - magic_reduction)

	# Multiplies magic resistance by the percent amount we are reducing it to
	# This also causes the player's actual magic resistance to decrease.
	def percent_magic_reduction(self, magic_resist, percent_reduction):
		return magic_resist * ((100 - percent_reduction) / 100)

	# Multiplies magic resistance by the percent amount we are reducing it to
	# Main difference between this and reduction is that pen will not decrease
	# a player's magic resistance below zero.
	# This is only applied to the damage taken by the player, in other words it does
	# not actually cause the player to lose any magic resistance.
	def percent_magic_pen(self, magic_resist, percent_pen):
		if magic_resist > 0 and (magic_resist * ((100 - percent_pen) / 100)) > 0:
			return magic_resist * ((100 - percent_pen) / 100)
		elif magic_resist <= 0:
			return magic_resist

	def flat_magic_pen(self, magic_resist, magic_pen):
		if magic_resist > 0 and (magic_resist - magic_pen) > 0:
			return magic_resist - magic_pen
		elif magic_resist > 0 and (magic_resist - magic_pen) < 0:
			return 0
		else:
			return magic_resist

	# Will calculate the appropriate magic resist values in its proper order
	def calculate_total_mr(self, magic_resist, magic_reduction, percent_reduction, percent_pen, magic_pen):
		total_mr = self.flat_magic_reduction(magic_resist, magic_reduction)
		total_mr = self.percent_magic_reduction(total_mr, percent_reduction)
		total_mr = self.percent_magic_pen(total_mr, percent_pen)
		total_mr = self.flat_magic_pen(total_mr, magic_pen)
		return total_mr

class Damage():

	def auto_attack(self, attack_damage, armor_reduction, percent_reduction, 
		percent_pen, percent_bonus_pen, flat_pen, base_armor, bonus_armor):

		total_armor = ArmorPenetration().calculate_total_armor(base_armor, bonus_armor, 
			armor_reduction, percent_reduction, percent_pen, percent_bonus_pen, flat_pen)
		damage_reduction = 0
		if total_armor > 0:
			damage_reduction = (100 / (100 + total_armor))
		else:
			damage_reduction = 2 - (100 - (100 - total_armor))

		return (attack_damage / 100) * (100 - damage_reduction)

print(Damage().auto_attack(101.0, 0.0, 0.0, 30.0, -1.0, 0.0, 5.0, 10.0))

print(MagicPenetration().calculate_total_mr(80.0, 20.0, 30.0, 35.0, 10.0))






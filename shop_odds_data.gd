class_name ShopOddsData
extends Resource

# Index 0 is intentionally empty, so the array index matches the player level.
@export var rates_by_level: Array[Dictionary] = []

func get_rates(player_level: int) -> Dictionary:
	assert(player_level > 0 and player_level < rates_by_level.size())
	return rates_by_level[player_level]

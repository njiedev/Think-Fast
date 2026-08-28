extends SceneTree

func _init() -> void:
	var database: UnitDatabase = load("res://unit_database.tres")
	var shop_odds: ShopOddsData = load("res://shop_odds.tres")

	assert(database != null)
	assert(database.units.size() == 62)
	assert(database.get_by_id("TFT17_Aatrox").unit_name == "Aatrox")

	for unit in database.units:
		assert(unit.id.begins_with("TFT17_"))
		assert(unit.unit_image != null)

	assert(shop_odds != null)
	assert(shop_odds.rates_by_level.size() == 12)
	for player_level in range(1, shop_odds.rates_by_level.size()):
		assert(shop_odds.get_rates(player_level).size() == 5)
		assert(Array(shop_odds.get_rates(player_level)).reduce(func(total, rate): return total + rate, 0) == 100)

	print("Verified 62 units, their textures, and shop odds for levels 1-11.")
	quit()

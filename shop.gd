
class_name	Shop extends Resource

@export var shop: Array[UnitData] = []
func _init() -> void:
	shop.resize(5)



func randRarity(shopOddData,playerLevel):
	var rng =  RandomNumberGenerator.new()
	var rarities = []
	var rareEnum = UnitData.Rarity
	for i in rareEnum:
		rarities.append(rareEnum[i])
		#[ONECOST,TWOCOST,THREECOST,FOURCOST,FIVECOST]
	var shopWeights = []
	var odds = shopOddData.get_rates(playerLevel)
	for i in odds:
		shopWeights.append(odds[i])
	return rarities[rng.rand_weighted(shopWeights)]
func randUnit(runtime_pool, rarity):
	var rng =  RandomNumberGenerator.new()
	
	var currUnitPool = runtime_pool.currentPool[rarity]
	var unit_ids = currUnitPool.keys()
	var weights = currUnitPool.values()
	var selected_index = rng.rand_weighted(weights)
	return unit_ids[selected_index]
func reroll(playerLevel, runtime_pool,shopOddData,unitDB):
	for i in len(shop):
		var rarity = randRarity(shopOddData, playerLevel)
		var unitID = randUnit(runtime_pool, rarity)
		var unit = unitDB.get_by_id(unitID)
		shop[i] = unit 
	return
func buy_unit(slot_index: int) -> void:
	var unit = shop[slot_index]
	if unit == null:
		return
	#add_unit_to_bench(unit)
	self.shop[slot_index] = null
	

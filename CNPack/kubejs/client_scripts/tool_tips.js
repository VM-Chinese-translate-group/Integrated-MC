ItemEvents.tooltip(event => {
  event.add([global.itemsToRemove], Text.red('此物品已被禁用')),
  event.add('sophisticatedbackpacks:feeding_upgrade', Text.red('此物品已因BUg而被禁用。')),
  event.add('sophisticatedbackpacks:advanced_feeding_upgrade', Text.red('此物品已因BUg而被禁用。')),
  event.add('create_enchantment_industry:disenchanter', Text.red('思索会使你的游戏崩溃。'))
})
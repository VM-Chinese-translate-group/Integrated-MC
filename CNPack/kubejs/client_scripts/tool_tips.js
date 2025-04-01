ItemEvents.tooltip(event => {
  event.add([global.itemsToRemove], Text.red('此物品已被禁用')),
  event.add('sophisticatedbackpacks:feeding_upgrade', Text.red('This was disabled due to an item voiding bug.')),
  event.add('sophisticatedbackpacks:advanced_feeding_upgrade', Text.red('This was disabled due to an item voiding bug.')),
  event.add('create_enchantment_industry:disenchanter', Text.red('Pondering this will crash your game.'))
})
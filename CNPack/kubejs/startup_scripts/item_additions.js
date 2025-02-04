// Listen to item registry event
StartupEvents.registry('item', event => {
  // The texture for this item has to be placed in kubejs/assets/kubejs/textures/item/test_item.png
  // If you want a custom item model, you can create one in Blockbench and put it in kubejs/assets/kubejs/models/item/test_item.json
  event.create('dormant_locator_eye'),
  event.create('ignitium_armor_plate'),
  event.create('cursium_armor_plate'),
  event.create('terrible_armor_plate'),
  event.create('abyssal_armor_plate'),
  event.create('draco_arcanus_armor_plate')
})
scoreboard objectives add MCAL_RUNTIME_STACKPTR dummy
scoreboard players set @e[tag=MCAL_RUNTIME_VARMANAGER] MCAL_RUNTIME_STACKPTR -1
data remove storage mcal_core:stack {}
data remove storage mcal_core:functionargs {}
data modify storage mcal_core:stack {} set value {stack_registry:[],stack_ptr:0}
data modify storage mcal_core:functionargs {} set value {}
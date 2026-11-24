Combat system contains a lot of mechanics since Helium engine aims to make combat more dynamic. 
## Initiative
Obviously, when a fight starts, casual RPG turns into turn-based strategy. Initiative is sequence of turns of all entities that are included in fight. Depending on situation, even neutral entities can be included in initiative (such as some players who are not directly fighting or attacked by enemies but help those players that are fighting). Initiative is issued by DM when fight starts or situation requires turn-based environment (such as fast-paced chase, time-limited trap escape, etc). Initiative is ended manually by DM when either all entities came to peace (all aggressive towards each other entities were killed, neutralized or fled) or fight ended abruptly due to some condition (f.e. falling boulders, ship cracking in two, volcano eruption, etc)
### Turn
Turn is `initiative time unit`. Its equal exactly to `4 seconds` which is enough to do either simple actions without rushing or complex moves with full focus.
### Round
Round is one iteration of initiative circle of all entities and their turns, while turn is applied locally (f.e. "This entity's turn"), round groups all turns of all entities in that iteration.
### Group turns
To add more teamwork Helium engine uses group turns: if a few allied entities stay together (physically together on the neighbouring cells) then they're grouped, meaning that they share grouped turn (while preserving their own initiative resources) and can communicate what to do. Max size of initiative group is 4 entities (doesnt relate to supergroups of entities (when 1 entity on board resemble many entities like army or big group)), if amount of entities to be grouped is higher than 4 then either players (if player characters) or DM (if npcs) decide how to split them. To determine order of turns, each group rolls `1d20` with bonus from the highest [[Character sheet#Speed|Agility]] in the group. If some groups have the same roll, they roll `1d2` or `1d4` (depending on how many groups got the same roll) until there's exact order.

#### Dynamic grouping
Obviously, characters are moving during initiative. Thats why Helium engine also uses dynamic grouping as method of managing group turns. Each entity in initiative has exactly 1 turn and they spend it to make a turn in that round. When grouped, all of grouped entities use their turns to make a group turn in that round. If entity at the end of their group turn moves away, they dynamically move out from that group, rolling their own initiative for next round or join new group and inherit group's initiative roll. Important note that even if they join new group, if they used their personal turn resource, they cant take another turn in that round.

## Initiative resources
To prevent offhand being useless and make fights more dynamic, Helium engine uses seconds as unified initiative resource. Since [[#Round]] is `4 seconds`, each character gets `4 unified seconds` that they can spend however they want for any action done by any part of the body. Quick cheat sheet of seconds cost for module makers:
- Walk `Ns=N*2m + floor(AGL/3)m`
- Jump `1s` = `2m + floor(AGL/3)m` horizontally and `0.5m` vertically
- Sprint `3s=Walk(3s)*2`
- Light attack/Offhand attack `1s`
- Basic weapon attack `2s`
- Object throw `2s`
- Heavy attack `3s`
- Dodge `2s`
- Hotbar draw `1s`
- Coldbar draw `4s`

## Attack rolls
Attack roll is check if attack hits or not. There are 2 types of attack rolls: ignored and dodged.
- If defender doesnt dodge in their turn, attack roll is `1d20+SKILL` and it put against 10 (if proficient with used weapon) or 14 (if not proficient). If attack roll is higher or equal, attack does hit.
- If defender dodges in their turn before next attack, that next attack will be put against dodge roll, so attack roll `1d20+SKILL` has to be greater than or equal to defender's dodge roll `1d20+DEX` to hit.

## Flat armor
Flat armor is physical or magical armor that prevents weak enough attacks from damaging character. Flat armor reduces incoming Kinetic damage and obtained by wearing armor pieces (f.e. chestplate, helmet, etc). It can also protect from other types of damage if armor piece has tag to do so or if its specialized magical armor spell.

## Dodging
Dodge is the active way to attempt to not be hit by either simple attack (just raise chances of not getting hit) or guaranteed to hit attack (attacking entity with a special tag). While failing attack roll just doesnt hit you, dodge serves as active way to defend against attacks. It consumes `2 seconds` in entity's own turn and upon being attacked it rolls `1d20+DEX` and if its higher than attack roll then defender succeeds and attack doesnt hit them, otherwise it does. Using dodge only affects `1 next attack` (entity may use few dodges to dodge a few attacks if they have enough seconds).


## Damage types
Damage is split into types that enable [[Tags]] to affect combat and whole game's damage directly. Damage types are split into 3 categories: [[#Kinetic]], [[#Elemental]] and [[#Body]].


| **Category**  | Type 1   | Type 2   | Type 3    | Type 4   | Type 5 | Type 6 |
| ------------- | -------- | -------- | --------- | -------- | ------ | ------ |
| **Kinetic**   | Piercing | Slashing | Blunt     |          |        |        |
| **Elemental** | Fire     | Cold     | Lightning | Acid     | Light  | Sound  |
| **Body**      | Bleeding | Poison   | Psychic   | Necrotic |        |        |


### Kinetic
Kinetic damage type applies to physical attacks that directly affect entities and objects.
### Elemental
Elemental damage type applies to different elemental attacks, can be either magical or item-related (f.e. fire type can be used by wizard as spell or fire archer as arrow with lit-up tip).
### Body
Body damage type applies to attacks that only affect living entities.
Combat system contains a lot of mechanics since Helium engine aims to make combat more dynamic. 
## Initiative
Obviously, when fight starts, casual RPG turns into turn-based strategy. Initiative is sequence of turns of all entities that are included in fight. Depending on situation, even neutral entities can be included in initiative (such as some players who are not directly fighting or attacked by enemies but help those players that are fighting). Initiative is issued by DM when fight starts or situation requires turn-based environment (such as fast-paced chase, time-limited trap escape, etc). Initiative is ended manually by DM when either all entities came to peace (all aggressive towards each other entities were killed, neutralized or did flee) or fight ended abruptly due to some condition (f.e. falling boulders, ship cracking in two, volcano eruption, etc)
### Round
Round is 1 initiative time unit. Its equal exactly to 4 seconds which is enough to do either simple actions without rushing or complex moves with full focus.
### Group turns
To add more teamwork Helium engine uses group turns: if a few allied entities stay together (physically together on the neighbouring cells) then they're grouped, meaning that they share 1 turn and can communicate what to do. Max size of initiative group is 4 entities (doesnt relate to supergroups of entities (when 1 entity on board resemble many entities like army or big group)), if amount of entities to be grouped is higher than 4 then either players (if player characters) or DM (if npcs) decide how to split them. To determinate order of turns, each group rolls `1d20` with bonus from the highest [[Character sheet#Speed|Agility]] in the group. If some groups have the same roll, they roll `1d2` or `1d4` (depending on how many groups got the same roll) until there's exact order.

#### Dynamic grouping
Obviously, characters are moving during initiative. Thats why Helium engine also uses dynamic grouping as method of managing group turns. Each entity in initiative have exactly 1 turn and they spend it to make a turn in that round. When grouped, all of grouped entities use their turns to make a group turn in that round. If entity at the end of their group turn moves away, they dynamically move out from that group, rolling their own initiative for next round or join new group and inherit group's initiative roll. Important note that even if they join new group, if they used their personal turn resource, they cant take another turn in that round.

## Initiative resources
To prevent offhand being useless and make fights more dynamic, Helium engine uses seconds as unified initiative resource. Since [[#Round]] is 4 seconds, each character gets 4 unified seconds that they can spend however they want for any action done by any part of the body. Quick cheat sheet for second cost:
- Walk 1s=2m
- Jump 1s= 1m horizontally and 1m vertically
- Sprint 3s=8m
- Light attack/Offhand attack 1s
- Basic weapon attack 2s
- Object throw 2s
- Heavy attack 3s
## Attack rolls


## Flat armor
Flat armor is physical or magical armor that prevents weak enough attacks from damaging character. Flat armor reduces any incoming damage of Kinetic damage and obtained by wearing armor pieces (f.e. chestplate, helmet, etc). It can also protect from other damage types if armor piece has tag to do so or if its specialized magical armor spell
## Dodging



## Damage types
Damage is split into types that enable [[Tags]] to affect combat and whole game's damage directly. Damage types are split into 3 categories: [[#Kinetic]], [[#Elemental]] and [[#Body]].


| **Category**  | Type 1   | Type 2   | Type 3    | Type 4   | Type 5 | Type 6 |
| ------------- | -------- | -------- | --------- | -------- | ------ | ------ |
| **Kinetic**   | Piercing | Slashing | Blunt     |          |        |        |
| **Elemental** | Fire     | Cold     | Lightning | Acid     | Light  | Sound  |
| **Body**      | Bleeding | Poison   | Psychic   | Necrotic |        |        |


### Kinetic
Kinetic damage type responds to physical attacks that directly affect entities and objects.
### Elemental
Elemental damage type responds to different elemental attacks, can be either magical or item-related (f.e. fire type can be used by wizard as spell or fire archer as arrow with lit-up tip).
### Body
Body damage type responds to attacks that only affect living entities
# Wetenschappenlijke analyse van het project
## Wat valt je op aan de oplossingen, hoe kun je dat verwerken in het algoritme?

###### Birgit
Als je de paden random legt, kun je zelf voor de simpelste netlist vaak geen oplossing vinden.

![example random algoritm](./images/random_chip_0_net_1.png "Example image")

In bovenstaande afbeelding zie je een voorbeeld van hoe het random algoritme probeert de eerste netlist op de kleinste chip te leggen.
Hierin is 1 van de 5 netlist geslaagd gelegd.

Het viel het op dat een pad soms 'faalt' terwijl er wel een weg mogelijk is.
Om dit te ondervangen is een bepaalde herhaling in het random algoritme geïmplementeerd.
Als een net faalt, probeert hij het nog 50 keer opnieuw voordat hij het opgeeft.
Op basis hiervan krijg je oplossingen zoals hieronder.

![example 2 random algorithm](./images/random2_chip_0_net_1.png "Example image")

We zien nu dat voor chip 0 en netlist 1, het random algoritme opzich relatief vaak een oplossing genereert.
Voor netlist 2 komt dit echter al bijna niet meer voor, omdat netlist 2 ingewikkelder is doordat meer paden elkaar kruisen.

Al hoewel het logisch is dat een random algoritme weinig 'goede' oplossingen genereert, waarom gaat het nou fout?
* Als je random kanten op gaat, leg je hele lange paden aan waardoor je voor andere paden minder mogelijkheden overhoudt.
* Je zou perongeluk met je pad andere gates kunnen insluiten, waardoor er voor die gates geen enkele mogelijkheid meer is.
* Met de random paden leg je ontzettend veel kruispunten, waaronder met jezelf, wat hoge kosten oplevert.

Wat kan beter?

* Probeer richting je eindgate te lopen
* Probeer de ruimte die je hebt efficient te gebruiken, de voorkeur is om zo laag mogelijk te zitten
* Leg de nets die de korste afstand moeten overbruggen eerst

Aan de hand van bovenstaande punten heb ik een 'steered random' algoritm geschreven, dat produceerde oplossingen zoals hieronder.

![example steered random algoritm](./images/steered_random_chip_0_net_1.png "Example image")

Nu zie je bij deze oplossing bijvoorbeeld, dat het pad nu te snel naar beneden getrokken wordt.
Het zou dus veel toegevoegde waarde hebben, als het algoritme een plek vooruit kon kijken.
Als hij toch vooruit kijkt, gaat hij ook proberen intersecties te vermijden.
Een voorbeeld van een oplossing die hij dan voor de eerste netlist genereert staat hieronder.

![example 2 steered random algoritm](./images/steered_random2_chip_0_net_1.png "Example image")


# Programmeertheorie

 ## Chips & Circuits

 Chips en circuits is een optimalisatie probleem.
 Er zijn 9 verschillende 'puzzels', van varierende moeilijkheidsgraad, maar het principe komt bij allemaal op hetzelfde neer.

 Je hebt een 'chip' in de vorm van een rooster in een ruitjespatroon, waarop 'gates' zijn geplaatst.
 Om de gates van elkaar te onderscheiden, zijn ze genummerd.
 Er zijn in totaal 3 verschillende chips voor dit probleem aan ons opgeleverd.
 Bij elke chip, worden eveneens 3 'netlists' gegeven.
 Een netlist is een lijst die opsomt welke gates met elkaar verbonden moeten worden om de chip werkend te krijgen.
 Het doel is om alle gates die volgens de netlist verbonden moeten worden, te verbinden.

 ![lege chip](./data/images/voorbeeld_chip.gif "Lege chip")

 Hier zitten wel wat randvoorwaarden aan verbonden, die het ingewikkeld maken.
 Zo zitten er kosten verbonden aan het maken van een chip.
 De draden waarmee de gates verbonden moeten worden, kosten geld, dus hoe meer draad je nodig hebt, hoe hoger te kosten.
 Per lengte eenheid, gelijk aan de afstand tussen twee kruispunten in het rooster, zijn de kosten van een draad 1.

 Deze draden mogen elkaar wel kruisen, maar niet overlappen, want dat zou kortsluiting geven.
 Dit houdt in dat bij een kruispunt in het rooster er twee draden mogen zijn die allebei van een andere kant komen en die allebei ook weer een andere richting op gaan.
 Om kortsluiting op een kruispunt van draden te voorkomen, moeten deze op een speciale manier gemaakt worden.
 De kosten van het leggen van meerdere draden op een kruispunt is 300.

 Naast het verbinden van alle gates, geeft het probleem de extra uitdaging om de kosten van de chip te minimaliseren.

 ## Algoritmen

 ## Reproductie resultaten
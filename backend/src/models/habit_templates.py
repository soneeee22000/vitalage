from dataclasses import dataclass


@dataclass(frozen=True)
class HabitTemplate:
    """Definition of a micro-habit from the evidence-based library."""

    id: str
    name: str
    dimension: str
    description_fr: str


HABIT_TEMPLATES: dict[str, HabitTemplate] = {
    "sleep-before-23h": HabitTemplate(
        id="sleep-before-23h",
        name="Dormir avant 23h",
        dimension="sleep",
        description_fr="Se coucher avant 23 heures chaque soir",
    ),
    "no-screens-30min": HabitTemplate(
        id="no-screens-30min",
        name="Pas d'ecran 30 min avant le coucher",
        dimension="sleep",
        description_fr="Eteindre les ecrans 30 minutes avant de dormir",
    ),
    "wake-same-time": HabitTemplate(
        id="wake-same-time",
        name="Se lever a la meme heure",
        dimension="sleep",
        description_fr="Se reveiller a la meme heure chaque jour",
    ),
    "fruit-before-noon": HabitTemplate(
        id="fruit-before-noon",
        name="1 fruit avant midi",
        dimension="nutrition",
        description_fr="Manger un fruit avant le dejeuner",
    ),
    "water-every-meal": HabitTemplate(
        id="water-every-meal",
        name="Eau a chaque repas",
        dimension="nutrition",
        description_fr="Boire un verre d'eau avec chaque repas",
    ),
    "vegetable-at-lunch": HabitTemplate(
        id="vegetable-at-lunch",
        name="Legumes au dejeuner",
        dimension="nutrition",
        description_fr="Manger au moins une portion de legumes au dejeuner",
    ),
    "walk-after-lunch": HabitTemplate(
        id="walk-after-lunch",
        name="Marcher 10 min apres le dejeuner",
        dimension="activity",
        description_fr="Faire une promenade de 10 minutes apres le repas de midi",
    ),
    "morning-stretch": HabitTemplate(
        id="morning-stretch",
        name="Etirements 5 min le matin",
        dimension="activity",
        description_fr="Faire 5 minutes d'etirements au reveil",
    ),
    "daily-steps-5000": HabitTemplate(
        id="daily-steps-5000",
        name="5000 pas aujourd'hui",
        dimension="activity",
        description_fr="Atteindre 5000 pas dans la journee",
    ),
    "gratitude-note": HabitTemplate(
        id="gratitude-note",
        name="1 chose positive aujourd'hui",
        dimension="mood",
        description_fr="Ecrire une chose pour laquelle vous etes reconnaissant",
    ),
    "outdoor-10min": HabitTemplate(
        id="outdoor-10min",
        name="10 min dehors en plein jour",
        dimension="mood",
        description_fr="Passer 10 minutes a l'exterieur pendant la journee",
    ),
    "call-a-friend": HabitTemplate(
        id="call-a-friend",
        name="Appeler un proche cette semaine",
        dimension="mood",
        description_fr="Prendre des nouvelles d'un ami ou d'un membre de la famille",
    ),
}

# VitalAge — Concierge Pilot

## Overview

- **Duration:** 5 days (Apr 6-10)
- **Participants:** 5-8 adults aged 45+
- **Tool:** Google Form (daily) + WhatsApp/SMS (reminders)
- **Goal:** One proof line for the application

---

## Recruitment Message (WhatsApp/SMS)

### French

> Bonjour [Prénom],
>
> Je développe une application de santé préventive pour un challenge VivaTech avec Nestlé. J'aurais besoin de votre aide pour un test rapide.
>
> Le principe : chaque matin pendant 5 jours, vous remplissez un formulaire de 60 secondes sur votre sommeil, énergie et humeur. C'est tout.
>
> À la fin, je vous envoie une mini-analyse personnalisée de vos données.
>
> Ça vous intéresse ? C'est 100% anonyme et ça m'aiderait énormément.

### English (for bilingual contacts)

> Hi [Name],
>
> I'm building a preventive health app for a VivaTech challenge with Nestlé. I need your help with a quick test.
>
> The idea: every morning for 5 days, you fill out a 60-second form about your sleep, energy, and mood. That's it.
>
> At the end, I'll send you a personalized mini-analysis of your data.
>
> Interested? It's 100% anonymous and would help me a lot.

---

## Daily Check-in Form (Google Form)

### Form Title

**VitalAge — Bilan du matin**

### Form Description

> Ce formulaire prend moins de 60 secondes. Remplissez-le chaque matin, idéalement après votre café.
>
> Vos réponses sont anonymes et servent uniquement à tester le concept.

### Questions

**1. Prénom ou pseudo**

- Type: Short text
- Required: Yes
- Help text: "Toujours le même pour qu'on suive vos données sur 5 jours"

**2. Comment avez-vous dormi cette nuit ?**

- Type: Linear scale (1-5)
- 1 = Très mal
- 2 = Mal
- 3 = Correct
- 4 = Bien
- 5 = Très bien
- Required: Yes

**3. Quel est votre niveau d'énergie ce matin ?**

- Type: Linear scale (1-5)
- 1 = Épuisé(e)
- 2 = Fatigué(e)
- 3 = Normal
- 4 = En forme
- 5 = Plein(e) d'énergie
- Required: Yes

**4. Comment décririez-vous votre humeur ?**

- Type: Multiple choice
- Options:
  - Bien / Content(e)
  - Calme / Serein(e)
  - Normal / Neutre
  - Fatigué(e) / Mou(e)
  - Stressé(e) / Anxieux(se)
  - Irritable / Agacé(e)
- Required: Yes

**5. Avez-vous des douleurs ou gênes ce matin ?**

- Type: Multiple choice
- Options:
  - Aucune
  - Douleurs articulaires
  - Maux de tête
  - Problèmes digestifs
  - Douleurs musculaires
  - Autre (précisez)
- Required: Yes

**6. Une remarque ou un détail sur votre journée d'hier ? (optionnel)**

- Type: Long text
- Required: No
- Help text: "Ex: j'ai beaucoup marché, j'ai mal mangé, j'ai bien ri avec des amis..."

---

## Daily Reminder Message (send at participant's chosen time)

### Day 1

> Bonjour ! C'est le jour 1 de votre bilan VitalAge. Ça prend 60 secondes :
> [lien Google Form]

### Day 2-4

> Bonjour ! Jour [X]/5 — votre bilan du matin :
> [lien Google Form]
> (Merci pour votre régularité !)

### Day 5

> Dernier jour ! Jour 5/5 — votre dernier bilan :
> [lien Google Form]
> Je vous envoie votre analyse personnalisée demain.

---

## Tracking Spreadsheet (Google Sheets)

| Participant | Age | Jour 1 | Jour 2 | Jour 3 | Jour 4 | Jour 5 | Completion Rate |
| ----------- | --- | ------ | ------ | ------ | ------ | ------ | --------------- |
| Prénom A    | 58  | Yes    | Yes    | Yes    | No     | Yes    | 4/5 = 80%       |
| Prénom B    | 63  | Yes    | Yes    | Yes    | Yes    | Yes    | 5/5 = 100%      |
| ...         |     |        |        |        |        |        |                 |

Track per response:

- Timestamp (did they do it in the morning or at 11pm?)
- Sleep score
- Energy score
- Mood
- Symptoms

---

## Day 6: Personal Insight Messages

After 5 days of data, write each participant a personalized message.

### Template

> Bonjour [Prénom],
>
> Merci d'avoir participé pendant 5 jours ! Voici ce que vos données révèlent :
>
> **Sommeil :** Votre qualité moyenne était de [X]/5. [Observation — e.g., "Vos meilleures nuits étaient en début de semaine."]
>
> **Énergie :** Votre énergie moyenne était de [X]/5. [Correlation — e.g., "Les jours où vous avez dormi 4+/5, votre énergie était systématiquement plus haute."]
>
> **Humeur :** Votre humeur dominante était "[X]". [Pattern — e.g., "Votre humeur était plus positive les jours avec une bonne énergie."]
>
> **Observation personnelle :** [The most interesting correlation — e.g., "Quand vous avez noté des douleurs articulaires, votre énergie du lendemain était plus basse. Quelque chose à surveiller."]
>
> Est-ce que ces observations vous parlent ? Est-ce que ça vous semble utile ?

### What to look for in the data

- Sleep → next-day energy correlation (most common, most compelling)
- Mood patterns by day of week
- Symptom clusters (do symptoms correlate with bad sleep?)
- Energy trends across the 5 days
- Any outlier days — what did they mention in the free text?

---

## Day 7: Exit Survey (Google Form)

### Form Title

**VitalAge — Retour d'expérience**

### Questions

**1. Prénom ou pseudo**

- Type: Short text

**2. Le bilan quotidien était-il facile à maintenir ?**

- Type: Linear scale (1-5)
- 1 = Très contraignant
- 5 = Très facile
- Required: Yes

**3. Combien de temps le formulaire vous prenait-il ?**

- Type: Multiple choice
- Options:
  - Moins de 30 secondes
  - 30 secondes à 1 minute
  - 1 à 2 minutes
  - Plus de 2 minutes

**4. L'analyse personnalisée vous a-t-elle semblé utile ?**

- Type: Multiple choice
- Options:
  - Oui, très utile — je n'avais pas remarqué ces tendances
  - Oui, assez utile — ça confirme ce que je ressentais
  - Pas vraiment — les observations étaient évidentes
  - Non, pas utile du tout

**5. Utiliseriez-vous une application qui fait ça automatiquement chaque jour ?**

- Type: Multiple choice
- Options:
  - Oui, certainement
  - Probablement oui
  - Peut-être
  - Probablement non
  - Non

**6. Qu'est-ce qui vous a le plus plu ? (optionnel)**

- Type: Long text

**7. Qu'est-ce qui manquait ou pourrait être amélioré ? (optionnel)**

- Type: Long text

**8. Votre âge (approximatif)**

- Type: Multiple choice
- Options:
  - 40-49 ans
  - 50-59 ans
  - 60-69 ans
  - 70+ ans

---

## Success Metrics

### For the application (what to write)

**Minimum viable proof (3+ participants):**

> "In a 5-day concierge pilot with [N] adults aged 45-65, [X]% completed 4+ daily check-ins and [Y]% reported the personalized insights were useful."

**Strong proof (5+ participants, good data):**

> "In a 5-day pilot with [N] adults (ages 48-67), average check-in completion was [X]%, average time-to-complete was under 60 seconds, and [Y] of [N] participants said they would use an automated version daily. The most valued feature was personalized correlations between sleep and next-day energy."

### Internal decision metrics

| Metric                                  | Target  | Action if missed          |
| --------------------------------------- | ------- | ------------------------- |
| Completion rate (5-day avg)             | 70%+    | Rethink check-in friction |
| Time to complete                        | <90 sec | Simplify questions        |
| "Would you use the app?" — Yes/Probably | 60%+    | Rethink value prop        |
| "Insights useful?" — Yes                | 50%+    | Core concept validated    |

---

## Timeline

| Date          | Action                                           |
| ------------- | ------------------------------------------------ |
| Apr 5 (today) | Create Google Forms, recruit participants        |
| Apr 6         | Day 1 — first check-in, send reminders           |
| Apr 7-9       | Days 2-4 — daily reminders, track in spreadsheet |
| Apr 10        | Day 5 — last check-in                            |
| Apr 11        | Write personal insights, send to participants    |
| Apr 12        | Send exit survey, compile results                |
| Apr 13        | Write proof paragraph for application            |

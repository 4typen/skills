# Jira Outcome Work Management – Agent-Skill

Dieser Skill unterstützt die fachliche Organisation von SaaS-Entwicklungsarbeit in Jira. Der Einstiegspunkt `SKILL.md` und die Referenzdateien sind auf Englisch geschrieben, damit sie sich in unterschiedlichen KI-Agent-Umgebungen einheitlich einsetzen lassen. Der Skill weist den Agenten ausdrücklich an, in der Sprache des Benutzers zu antworten und Jira-Artefakte in der im Projekt üblichen Sprache zu verfassen.

## Installation und Verwendung

1. Das ZIP entpacken und das Verzeichnis `jira-outcome-work-management` in die Skill-Struktur des eingesetzten Agenten legen. Falls dessen Skill-System keine Ordner unterstützt, `SKILL.md` als Hauptanweisung verwenden und die Referenzdateien als zusätzliche Wissensbasis einbinden.
2. Dem Agenten bei Bedarf lesenden Zugriff auf relevante Jira-Artefakte geben. Ohne Jira-Zugriff kennzeichnet der Agent Duplikatsuchen und Statusprüfungen ausdrücklich als nicht verifiziert.
3. Schreibzugriffe nur nach klarer Berechtigungs- und Freigaberegel aktivieren. Besonders bei Massenänderungen sollte der Agent zuerst eine Änderungsübersicht vorlegen.

## Beispielanfragen

- „Prüfe diese neue Kundenanforderung. Handelt es sich um eine Opportunity, ein Epic, eine Story, einen Task oder einen Bug? Erstelle einen geeigneten Jira-Entwurf.“
- „Das Epic 'User Management' enthält 60 Tickets. Entwickle eine outcome-orientierte Zielstruktur mit einer Zuordnungstabelle. Ändere noch nichts in Jira.“
- „Überprüfe diese User Story. Sind Ziel, Akzeptanzkriterien, Berechtigungen und Fehlerfälle klar genug?“
- „Erkenne im Engineering Backlog veraltete Ideen, Duplikate und Sammel-Tickets. Schlage eine Bereinigung vor, ohne etwas zu löschen.“
- „Zerlege dieses Epic in wenige sinnvolle vertikale Stories. Lege keine eigenen Frontend-, Backend- oder Test-Stories an, wenn sie zusammen ein einziges Verhalten umsetzen.“

## Dateien

- `SKILL.md`: Steuerlogik und zentrale Regeln
- `references/issue-taxonomy.md`: Definition und Abgrenzung der Artefakte
- `references/intake-and-backlog.md`: Intake und Backlog-Trennung
- `references/templates.md`: Vorlagen für Jira-Tickets
- `references/restructure.md`: Sicheres Vorgehen beim Umbau
- `references/edge-cases.md`: Grenzfälle aus der SaaS-Entwicklung
- `references/quality-gates.md`: Qualitätsbewertung und Review
- `references/ai-guidance.md`: Regeln für KI-Unterstützung
- `examples/scenarios.md`: End-to-End-Beispiele

## Geltungsbereich

Der Skill definiert Arbeitskonventionen. Er richtet weder Jira-Boards noch Sprints ein und ist nicht an eine bestimmte Jira-Lizenz gebunden. Echte Jira-Aktionen sind nur mit einer angeschlossenen Integration und passenden Berechtigungen möglich.

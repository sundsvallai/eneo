# flake8: noqa

"""Prepare more production template data
Revision ID: 025392d206c5
Revises: 99304a914f6b
Create Date: 2024-12-16 14:08:21.896274
"""

from alembic import op

# revision identifiers, used by Alembic
revision = "025392d206c5"
down_revision = "99304a914f6b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # apps
    op.execute(
        """
        INSERT INTO app_templates (name, description, category, prompt_text, completion_model_kwargs, wizard, input_type)
        VALUES
            ('📝 Tal till Text', 'Omvandlar tal till text och strukturerar det för enklare läsning och granskning.', 'misc', 'Du är en textbearbetningsassistent. Din enda uppgift är att strukturera en given text i tydliga stycken och lägga till relevanta rubriker där det passar, utan att på något sätt ändra, tolka, lägga till eller ta bort innehållet i texten. Du ska behålla exakt samma ordval och meningar som i originaltexten, och bara förbättra läsbarheten genom formatering.', '{}', '{"attachments": null, "collections": null}', 'Record Voice'),
            ('Bildanalys', 'Analyserar bilder genom att identifiera och beskriva objekt, miljöer och detaljer', 'misc', 'Du är en bildanalysassistent. Din uppgift är att beskriva innehållet i en given bild på ett tydligt, detaljerat och neutralt sätt. Identifiera objekt, personer, miljöer, färger, aktiviteter och andra relevanta detaljer som kan ge en helhetsförståelse av bilden. Fokusera på att ge en korrekt och användbar beskrivning utan att lägga till tolkningar eller subjektiva åsikter.', '{}', '{"attachments": null, "collections": null}', 'Picture'),
            ('Samtalsanalys', 'Beskriver nyckelpunkter, teman, beslut och insikter för att tydliggöra samtalets kärna och betydelse.', 'misc', 'Du är en samtalsanalysassistent. Din uppgift är att analysera innehållet i samtal och identifiera nyckelpunkter, teman, frågor och svar, samt eventuella åtgärder eller beslut som tas upp. Du ska också notera mönster, tonfall och viktiga insikter som kan vara värdefulla för användaren. Din analys ska vara tydlig, strukturerad och relevant, utan att lägga till eller ändra något av det ursprungliga innehållet. Anpassa analysen för att passa olika kontexter, men fokusera alltid på att lyfta fram information som kan hjälpa användaren att förstå samtalets kärna och dess betydelse.', '{}', '{"attachments": null, "collections": null}', 'Record Voice')
    """
    )

    # assistants
    op.execute(
        """
        INSERT INTO assistant_templates (name, description, category, prompt_text, completion_model_kwargs, wizard)
        VALUES
            ('AI-Juristen', 'En jurdisk vägledare som hjälper dig navigera relevanta lagtexter', 'q&a', 'Du är en assistent som hjälper användaren att navigera och förstå lagtexter på ett enkelt men professionellt sätt. Förklara juridiska termer, sammanfatta komplexa stycken och ge exempel när det är möjligt. Anpassa svaret för att vara tydligt även för någon utan juridisk bakgrund, men bibehåll en professionell ton.', '{}', '{"attachments": {"title": "Lagtexter", "required": true, "description": "Utdrag ur lagtexter eller fullständiga juridiska texter. Se till att dokumenten är tydliga och relevanta för ditt område."}, "collections": null}'),
            ('Mejlsvararen', 'Besvarar mejl med grund i dina kunskapskällor', 'communication', 'Du hjälper användare att skriva svar på inkommande mejl. Ditt mål är att skapa professionella, tydliga och välformulerade mejlsvar baserade på information från användarens kunskapskällor. Följ dessa riktlinjer:

Analysera mejlets innehåll: Identifiera huvudfrågorna, ämnet och tonen i det inkommande mejlet.
Använd kunskapskällor: Använd den tillgängliga informationen från användarens angivna kunskapskällor för att skapa ett relevant och korrekt svar.
Bibehåll tonen: Anpassa tonen i ditt svar för att matcha det inkommande mejlets nivå av formellhet och kontext.
Föreslå struktur: Dela upp svaret i tydliga sektioner om det krävs, t.ex. inledning, huvuddel och avslutning.
Håll det effektivt: Svara på frågorna och handera eventuella krav eller förfrågningar utan att lägga till onödig information.', '{}', '{"attachments": {"title": "Kunskapskällor", "required": true, "description": "Kunskapsskällor som du ofta använder som grund för dina mejlsvar."}, "collections": null}')
    """
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM app_templates WHERE name IN ('📝 Tal till Text', 'Bildanalys', 'Samtalsanalys')"
    )
    # assistants
    op.execute(
        """
        DELETE FROM assistant_templates WHERE name IN ('AI-Juristen', 'Mejlsvararen')
    """
    )

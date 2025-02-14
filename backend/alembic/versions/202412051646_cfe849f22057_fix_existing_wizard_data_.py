# flake8: noqa

"""Fix existing wizard data
Revision ID: cfe849f22057
Revises: 62e4b4c3882c
Create Date: 2024-12-05 16:46:55.109605
"""

from alembic import op


# revision identifiers, used by Alembic
revision = "cfe849f22057"
down_revision = "62e4b4c3882c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Assistant wizard field
    op.execute(
        """
        update assistant_templates
        set wizard =  '{"attachments": {"title": "Riktlinjer: kommunikation", "required": true, "description": "Kommunikationsriktlinjer, stilguider, tonalitetsmanualer och exempeltexter som reflekterar organisationens önskade språkliga och visuella stil."}, "collections": null}'
        where name = '📝 Kommunikation';
        """
    )
    op.execute(
        """
        UPDATE assistant_templates
        SET wizard = '{"collections": {"required": true, "title": "Styrdokument och arbetsguider", "description": "Övergripande riktlinjer, rutiner och snabbguider som beskriver arbetsprocesser, regler och instruktioner för att säkerställa enhetligt och effektivt arbete inom vård och omsorg."}, "attachments": null}'
        WHERE name = 'Vårdmentorn ';
        """
    )
    op.execute(
        """
        UPDATE assistant_templates
        SET wizard = '{"collections": {"required": true, "title": "Styrdokument", "description": "Ladda upp dina styrdokument"}, "attachments": null}'
        WHERE name = '📄 Styrdokument';
        """
    )
    op.execute(
        """
        UPDATE assistant_templates
        SET wizard = '{"collections": {"required": true, "title": "HR Dokument", "description": "Policydokument, personalhandböcker, arbetsavtal, riktlinjer och formulär som reglerar lön, förmåner, arbetsmiljö och rekryteringsprocesser."}, "attachments": null}'
        WHERE name = '🧑‍💼 Fråga HR';
        """
    )
    op.execute(
        """
        UPDATE assistant_templates
        SET wizard = '{"collections": {"required": true, "title": "IT Rutiner", "description": "Interna IT-guider, användarmanualer, IT-policyer, felsökningsinstruktioner och resurser för systemåtkomst och säkerhetshantering."}, "attachments": null}'
        WHERE name = '🧑‍💼 Fråga IT';
        """
    )
    op.execute(
        """
        UPDATE assistant_templates
        SET wizard = '{"collections": {"required": true, "title": "Intern Regel- och Policydata", "description": "Assistenten kräver tillgång till interna policyer, handböcker, riktlinjer, standardavtal, juridiska tolkningar, eskaleringsrutiner och historiska ärenden för att kunna ge korrekta svar, praktiska exempel och säkerställa efterlevnad av organisationens regelverk."}, "attachments": null}'
        WHERE name = '💡 Idégenerering & Kreativt Stöd';
        """
    )

    # App wizard field
    op.execute(
        """
        update app_templates 
        set wizard =  '{"attachments": {"title": "Mall: Mötesprotokoll", "required": true, "description": "Ladda upp en mall för hur du vill att dina möten ska sammanställas."}, "collections": null}' where name = '🎙️ Mötestranskription';
        """
    )
    op.execute(
        """
        update app_templates 
        set wizard =  '{"attachments": {"title": "Kontoplan och/eller konteringsriktlinjer", "required": true, "description": "Ladda upp en guide för att kategorisera och bokföra fakturor korrekt enligt organisationens regler och standard."}, "collections": null}'
        where name = '📊 Fakturakontering';
        """
    )


def downgrade() -> None:
    # Downgrade assistant
    op.execute(
        """
        update assistant_templates
        set wizard =  '{"attachments": {"title": "Riktlinjer: kommunikation", "required": true, "description": "Kommunikationsriktlinjer, stilguider, tonalitetsmanualer och exempeltexter som reflekterar organisationens önskade språkliga och visuella stil."}, "collections": {"title": null, "required": false, "description": null}}'
        where name = '📝 Kommunikation';
        """
    )
    op.execute(
        """
        UPDATE assistant_templates
        SET wizard = '{"attachments": null, "collections": null}'
        WHERE name = 'Vårdmentorn ';
        """
    )
    op.execute(
        """
        UPDATE assistant_templates
        SET wizard = '{"attachments": null, "collections": null}'
        WHERE name = '📄 Styrdokument';
        """
    )
    op.execute(
        """
        UPDATE assistant_templates
        SET wizard = '{"attachments": null, "collections": null}'
        WHERE name = '🧑‍💼 Fråga HR';
        """
    )
    op.execute(
        """
        UPDATE assistant_templates
        SET wizard = '{"attachments": null, "collections": null}'
        WHERE name = '🧑‍💼 Fråga IT';
        """
    )
    op.execute(
        """
        UPDATE assistant_templates
        SET wizard = '{"attachments": null, "collections": null}'
        WHERE name = '💡 Idégenerering & Kreativt Stöd';
        """
    )

    # Downgrade app
    op.execute(
        """
        update app_templates 
        set wizard =  '{"attachments": {"title": "Mall: Mötesprotokoll", "required": true, "description": "Ladda upp en mall för hur du vill att dina möten ska sammanställas."}}'
        where name = '🎙️ Mötestranskription';
        """
    )
    op.execute(
        """
        update app_templates 
        set wizard =  '{"attachments": {"title": "Kontoplan och/eller konteringsriktlinjer", "required": true, "description": "Ladda upp en guide för att kategorisera och bokföra fakturor korrekt enligt organisationens regler och standard."}}'
        where name = '📊 Fakturakontering';
        """
    )

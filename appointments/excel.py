from openpyxl_templates import TemplatedWorkbook
from openpyxl_templates.table_sheet import TableSheet
from openpyxl_templates.table_sheet.columns import IntColumn, CharColumn, DatetimeColumn, TextColumn
from openpyxl_templates.styles import ExtendedStyle


CUSTOM_DATE = ExtendedStyle(
        base='Row',
        name='Row, custom_date',
        alignment={'horizontal': 'center'},
        number_format='dd/mm/yyyy hh:mm',
    )


class PersonSheet(TableSheet):
    id = IntColumn(header='ID', cell_style='Row, string')
    name = CharColumn(header='Nome', width=30)
    surname = CharColumn(header='Cognome', width=30)
    tax_code = CharColumn(header='Codice Fiscale', width=30)


class AppointmentSheet(TableSheet):
    id = IntColumn(header='ID', cell_style='Row, string')
    doctor = CharColumn(header='Dottore', width=30)
    patient = CharColumn(header='Paziente', width=30)
    date_from = DatetimeColumn(header='Da', width=30, cell_style=CUSTOM_DATE)
    date_to = DatetimeColumn(header='A', width=30, cell_style=CUSTOM_DATE)
    notes = TextColumn(header='Note', width=30)


class ExportWorkbook(TemplatedWorkbook):
    doctors = PersonSheet()
    patients = PersonSheet()
    appointments = AppointmentSheet()

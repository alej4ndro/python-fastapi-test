import pytest
from app.services.practitioner_service import parse_practitioner_html


@pytest.mark.parametrize("html_content, expected", [
    ("""
    <table class='resultados'>
        <tr><td class='tdLabel'>Número colegiado</td><td>123456789</td></tr>
        <tr><td class='tdLabel'>Nombre y Apellidos</td><td>Dr. John Doe</td></tr>
        <tr><td class='tdLabel'>Provincia colegiación</td><td>New York</td></tr>
        <tr><td class='tdLabel'>Especialidad</td><td>Pediatrics</td></tr>
        <tr><td class='tdLabel'>Estado de colegiación</td><td>Active</td></tr>
        <tr><td class='tdLabel'>Dirección de trabajo</td><td>123 Main St, New York, NY</td></tr>
    </table>
    """, {
        'memberId': '123456789',
        'fullName': 'Dr. John Doe',
        'membershipProvince': 'New York',
        'medicalSpecialty': 'Pediatrics',
        'membershipState': 'Active',
        'workAddress': '123 Main St, New York, NY'
    }),
    ("""
    <table class='resultados'>
        <tr><td class='tdLabel'>Número colegiado</td><td>2983529874</td></tr>
        <tr><td class='tdLabel'>Nombre y Apellidos</td><td>Dr. Gerard Solanes Hernández</td></tr>
        <tr><td class='tdLabel'>Provincia colegiación</td><td>Cerdanyola del Vallès</td></tr>
        <tr><td class='tdLabel'>Especialidad</td><td>Química Computacional</td></tr>
        <tr><td class='tdLabel'>Estado de colegiación</td><td>ALTA</td></tr>
        <tr><td class='tdLabel'>Dirección de trabajo</td><td>C/ Oreneta num.41</td></tr>
    </table>
    """, {
        'memberId': '2983529874',
        'fullName': 'Dr. Gerard Solanes Hernández',
        'membershipProvince': 'Cerdanyola del Vallès',
        'medicalSpecialty': 'Química Computacional',
        'membershipState': 'ALTA',
        'workAddress': 'C/ Oreneta num.41'
    }),
    ("""
    <table class='resultados'>
        <tr><td class='tdLabel'>Número colegiado</td><td>4852923</td></tr>
        <tr><td class='tdLabel'>Nombre y Apellidos</td><td>  Ian Malcolm</td></tr>
        <tr><td class='tdLabel'>Provincia colegiación</td><td>Isla Nublar</td></tr>
        <tr><td class='tdLabel'>Especialidad</td><td>Chaotician  </td></tr>
        <tr><td class='tdLabel'>Estado de colegiación</td><td></td></tr>
        <tr><td class='tdLabel'>Dirección de trabajo</td><td></td></tr>
    </table>
    """, {
        'memberId': '4852923',
        'fullName': 'Ian Malcolm',
        'membershipProvince': 'Isla Nublar',
        'medicalSpecialty': 'Chaotician',
        'membershipState': 'undefined',
        'workAddress': 'undefined'
    }),
])
def test_parse_practitioner_html(html_content, expected):
    result = parse_practitioner_html(html_content)
    assert result == expected

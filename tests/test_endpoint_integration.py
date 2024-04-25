from fastapi.testclient import TestClient
from httpx import Response, Request
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_practitioner_endpoint_integration():
    mock_request = Request(
        method="GET", url="https://cgcom-interno.cgcom.es/RegistroMedicos/PUBBusquedaPublica_busquedaDetalle_ajax.action?numeroColegiado=123456789")

    mock_html_response = '''
    <table class='resultados'>
        <tr><td class='tdLabel'>Número colegiado</td><td>123456789</td></tr>
        <tr><td class='tdLabel'>Nombre y Apellidos</td><td>Dr. John Doe</td></tr>
        <tr><td class='tdLabel'>Provincia colegiación</td><td>New York</td></tr>
        <tr><td class='tdLabel'>Especialidad</td><td>Pediatrics</td></tr>
        <tr><td class='tdLabel'>Estado de colegiación</td><td>Active</td></tr>
        <tr><td class='tdLabel'>Dirección de trabajo</td><td>123 Main St, New York, NY</td></tr>
    </table>
    '''

    mock_response = Response(
        status_code=200, text=mock_html_response, request=mock_request)

    with patch('httpx.get', return_value=mock_response):
        response = client.get("/practitioner?member_id=123456789")
        assert response.status_code == 200
        assert response.json() == {
            "memberId": "123456789",
            "fullName": "Dr. John Doe",
            "membershipProvince": "New York",
            "medicalSpecialty": "Pediatrics",
            "membershipState": "Active",
            "workAddress": "123 Main St, New York, NY"
        }

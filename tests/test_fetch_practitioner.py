import pytest
from unittest.mock import patch, Mock
import httpx
from fastapi import HTTPException
from app.services.practitioner_service import fetch_practitioner_data
from app.models.practitioner import Practitioner


def test_fetch_practitioner_data_success():
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
    with patch('httpx.get') as mock_get:
        mock_get.return_value = Mock(status_code=200, text=mock_html_response)
        result = fetch_practitioner_data("123456789")
        assert isinstance(result, Practitioner)
        assert result.memberId == "123456789"
        assert result.fullName == "Dr. John Doe"


def test_fetch_practitioner_data_http_error():
    with patch('httpx.get') as mock_get:
        mock_get.side_effect = httpx.HTTPStatusError(
            message="Not Found",
            request=httpx.Request(
                method="GET", url="https://cgcom-interno.cgcom.es/RegistroMedicos/PUBBusquedaPublica_busquedaDetalle_ajax.action?numeroColegiado=invalid"),
            response=httpx.Response(status_code=404)
        )
        with pytest.raises(HTTPException) as excinfo:
            fetch_practitioner_data("invalid")
        assert excinfo.value.status_code == 404


def test_fetch_practitioner_data_request_error():
    with patch('httpx.get') as mock_get:
        mock_get.side_effect = httpx.RequestError(
            message="Network error",
            request=httpx.Request(
                method="GET", url="https://cgcom-interno.cgcom.es/RegistroMedicos/PUBBusquedaPublica_busquedaDetalle_ajax.action?numeroColegiado=invalid")
        )
        with pytest.raises(HTTPException) as excinfo:
            fetch_practitioner_data("error")
        assert excinfo.value.status_code == 500

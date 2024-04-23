# PYTHON FAST API TEST

## Contexto
La [Organización médica colegial de España](https://www.cgcom.es/) (OMC) ofrece un [buscador de médicos colegiados](https://www.cgcom.es/servicios/consulta-publica-de-colegiados) habilitados para el ejercicio en España, consultable públicamente. El buscador permite buscar colegiados por nombre, apellidos, provincia número de colegiado o especialización. Al realizar una búsqueda, el buscador devuelve una tabla de médicos colegiados que cumplen con el criterio de búsqueda. En cada fila de la tabla, la última celda es un botón que carga a la información detallada del médico correspondiente. Este botón invoca una URL utilizando el número de colegiado como parámetro (en adelante, nos referiremos a esta URL como URL detalle de colegiado). 

 El buscador está protegido por un captcha o código de verificación, para evitar la consulta automatizada por agentes no humanos. Sin embargo, un fallo de diseño en la página permite realizar consultas por número de colegiado sin necesidad de rellenar el captcha, mediante los siguientes pasos:

1. Cargar la URL del iframe con el formulario de consulta y obtener la Cookie JSESSIONID

2. Invocar la URL detalle de colegiado injectando la Cookie JSSESIONID en la petición.

Si se ejecuta correctamente, el resultado de invocar el paso 2 es una tabla HTML con la siguiente información:

|Datos del colegiado||
|-----------------------|--------------------------------------------------------|
|Número colegiado	| 123456789 |
|Nombre y Apellidos	| José García García |
|Provincia colegiación |	Madrid |
|Especialidad |	Médico especialista en Pediatría  |
|Estado de colegiación |	Médico colegiado de ALTA |
|Dirección de trabajo |	Calle singular Nº 0 |

## Prueba de código

Utiliza Python FastAPI para implementar una API que, a partir de un número de colegiado, devuelva la información del colegiado en formato JSON. La API debe ejecutar la secuencia de pasos descrita en "Contexto", y parsear la respuesta para mapear los campos de la tabla HTML al formato JSON del resultado de la API. Concretamente, la especificación de la API es la siguiente:

```yaml
openapi: 3.0.0
info:
  description: |
    This is the specication for the practitioner API.
  version: "1.0.0"
  title: Practitioner API
paths:
  /practitioner:
    get:
      tags:
        - practitioner
      summary: Finds Practitioner by member ID
      description: Get practitioner info by member ID
      operationId: findPractitionerByNumber
      parameters:
        - name: memberId
          in: query
          description: Member ID to be considered for filter
          required: true
          explode: true
          schema:
            type: string
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                type: object
                properties:
                  memberId:
                    type: string
                    example: "123456789"
                  fullName:
                    type: string
                    example: "Dr. John Doe"
                  membershipProvince:
                    type: string
                    example: "New York"
                  medicalSpecialty:
                    type: string
                    example: "Pediatrics"
                  membershipState:
                    type: string
                    example: "Active"
                  workAddress:
                    type: string
                    example: "123 Main St, New York, NY"    
        '400':
          description: Invalid member ID value

```

Genera en este repositorio la estructura de proyecto que consideres adecuada para el objetivo propuesto. Utiliza herramientas de IA generativa si lo consideras oportuno para la implementación. 

Del resultado entregado, se valorará:

* La defensa del proyecto por parte del candidato,
* La aplicación de buenas prácticas de programación (clean code)
* La implementación de algún test unitario y, si procede, de integración.  

## Installation Instructions

To install the required packages, please ensure that you have Python installed on your system. Then, follow these steps:

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Create a virtual environment (recommended):
  ```bash
   python -m venv venv
   source venv/bin/activate 
   ````
4. Install dependencies
  ```bash
  pip3 install -r requirements.txt
  ```

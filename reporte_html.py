import unittest
from datetime import datetime
from io import StringIO
import sys


class GeneradorReporteHTML(unittest.TextTestResult):
    """Generador de reportes en HTML para pruebas unitarias"""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_cases = []
        self.start_time = None
        self.end_time = None
    
    def startTest(self, test):
        super().startTest(test)
        if self.start_time is None:
            self.start_time = datetime.now()
    
    def stopTest(self, test):
        super().stopTest(test)
        self.end_time = datetime.now()
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_cases.append({
            'name': str(test),
            'status': 'exitoso',
            'error': None,
            'traceback': None
        })
    
    def addError(self, test, err):
        super().addError(test, err)
        self.test_cases.append({
            'name': str(test),
            'status': 'error',
            'error': err[1],
            'traceback': self._exc_info_to_string(err, test)
        })
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_cases.append({
            'name': str(test),
            'status': 'fallido',
            'error': err[1],
            'traceback': self._exc_info_to_string(err, test)
        })


class GeneradorHTMLTestRunner(unittest.TextTestRunner):
    """Test Runner que genera reportes en HTML"""
    
    def __init__(self, archivo_html='reporte_pruebas.html', verbosity=2):
        self.archivo_html = archivo_html
        stream = StringIO()
        super().__init__(stream=stream, verbosity=verbosity, resultclass=GeneradorReporteHTML)
    
    def run(self, test):
        resultado = super().run(test)
        self._generar_html(resultado)
        return resultado
    
    def _generar_html(self, resultado):
        """Genera el reporte HTML"""
        
        total_pruebas = resultado.testsRun
        exitosas = total_pruebas - len(resultado.failures) - len(resultado.errors)
        fallidas = len(resultado.failures)
        errores = len(resultado.errors)
        
        # Calcular tiempo de ejecución
        if resultado.start_time and resultado.end_time:
            tiempo_ejecucion = (resultado.end_time - resultado.start_time).total_seconds()
        else:
            tiempo_ejecucion = 0
        
        # Determinar color de estado general
        if errores > 0:
            estado_general = 'error'
            color_estado = '#dc3545'
        elif fallidas > 0:
            estado_general = 'fallido'
            color_estado = '#ffc107'
        else:
            estado_general = 'exitoso'
            color_estado = '#28a745'
        
        # Porcentaje de éxito
        porcentaje_exito = (exitosas / total_pruebas * 100) if total_pruebas > 0 else 0
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Pruebas - Sauce Demo</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .contenedor {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }}
        
        .encabezado {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}
        
        .encabezado h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .encabezado p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .resumen {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .tarjeta-resumen {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .tarjeta-resumen:hover {{
            transform: translateY(-5px);
        }}
        
        .tarjeta-resumen .numero {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .tarjeta-resumen .etiqueta {{
            color: #6c757d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .exitoso .numero {{
            color: #28a745;
        }}
        
        .fallido .numero {{
            color: #ffc107;
        }}
        
        .error .numero {{
            color: #dc3545;
        }}
        
        .total .numero {{
            color: #667eea;
        }}
        
        .barra-progreso {{
            width: 100%;
            height: 30px;
            background: #e9ecef;
            border-radius: 15px;
            overflow: hidden;
            margin-top: 15px;
        }}
        
        .barra-progreso-relleno {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            width: {porcentaje_exito}%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
            transition: width 0.5s ease;
        }}
        
        .estado-general {{
            padding: 20px;
            background: {color_estado};
            color: white;
            text-align: center;
            font-size: 1.3em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .detalles {{
            padding: 30px;
        }}
        
        .seccion-pruebas {{
            margin-bottom: 40px;
        }}
        
        .seccion-pruebas h2 {{
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .prueba {{
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 5px;
            transition: all 0.3s ease;
        }}
        
        .prueba:hover {{
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .prueba.exitosa {{
            border-left-color: #28a745;
            background: #f0fdf4;
        }}
        
        .prueba.fallida {{
            border-left-color: #ffc107;
            background: #fffbf0;
        }}
        
        .prueba.error {{
            border-left-color: #dc3545;
            background: #fef2f2;
        }}
        
        .nombre-prueba {{
            font-weight: bold;
            font-size: 1.1em;
            color: #333;
            margin-bottom: 10px;
        }}
        
        .estado-badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            text-transform: uppercase;
            margin-top: 10px;
        }}
        
        .badge-exitosa {{
            background: #d4edda;
            color: #155724;
        }}
        
        .badge-fallida {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .badge-error {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .traceback {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
            margin-top: 10px;
            max-height: 300px;
            overflow-y: auto;
        }}
        
        .pie {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
            border-top: 1px solid #e9ecef;
        }}
        
        .metadata {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        
        .metadata-item {{
            padding: 10px 0;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .metadata-item:last-child {{
            border-bottom: none;
        }}
        
        .metadata-label {{
            color: #6c757d;
            font-weight: bold;
            font-size: 0.9em;
            text-transform: uppercase;
        }}
        
        .metadata-valor {{
            color: #333;
            font-size: 1.1em;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <div class="encabezado">
            <h1>📊 Reporte de Pruebas</h1>
            <p>Automation - Sauce Demo</p>
        </div>
        
        <div class="resumen">
            <div class="tarjeta-resumen total">
                <div class="etiqueta">Total de Pruebas</div>
                <div class="numero">{total_pruebas}</div>
            </div>
            <div class="tarjeta-resumen exitoso">
                <div class="etiqueta">Exitosas</div>
                <div class="numero">{exitosas}</div>
            </div>
            <div class="tarjeta-resumen fallido">
                <div class="etiqueta">Fallidas</div>
                <div class="numero">{fallidas}</div>
            </div>
            <div class="tarjeta-resumen error">
                <div class="etiqueta">Errores</div>
                <div class="numero">{errores}</div>
            </div>
        </div>
        
        <div class="resumen">
            <div class="tarjeta-resumen">
                <div class="etiqueta">Tasa de Éxito</div>
                <div class="numero">{porcentaje_exito:.1f}%</div>
                <div class="barra-progreso">
                    <div class="barra-progreso-relleno"></div>
                </div>
            </div>
            <div class="tarjeta-resumen">
                <div class="etiqueta">Tiempo de Ejecución</div>
                <div class="numero">{tiempo_ejecucion:.2f}s</div>
            </div>
        </div>
        
        <div class="estado-general">
            ✓ Estado: {estado_general.upper()}
        </div>
        
        <div class="detalles">
            <div class="metadata">
                <div class="metadata-item">
                    <div class="metadata-label">Fecha y Hora</div>
                    <div class="metadata-valor">{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">Duración Total</div>
                    <div class="metadata-valor">{tiempo_ejecucion:.2f} segundos</div>
                </div>
            </div>
        </div>
"""
        
        # Agregar detalles de pruebas exitosas
        if exitosas > 0:
            html += """
            <div class="detalles">
                <div class="seccion-pruebas">
                    <h2>✓ Pruebas Exitosas ({count})</h2>
""".format(count=exitosas)
            
            for prueba in resultado.test_cases:
                if prueba['status'] == 'exitoso':
                    html += f"""
                    <div class="prueba exitosa">
                        <div class="nombre-prueba">{prueba['name']}</div>
                        <div class="estado-badge badge-exitosa">Exitosa</div>
                    </div>
"""
            
            html += """
                </div>
            </div>
"""
        
        # Agregar detalles de pruebas fallidas
        if fallidas > 0:
            html += """
            <div class="detalles">
                <div class="seccion-pruebas">
                    <h2>✗ Pruebas Fallidas ({count})</h2>
""".format(count=fallidas)
            
            for prueba in resultado.test_cases:
                if prueba['status'] == 'fallido':
                    traceback_html = f"<pre class='traceback'>{prueba['traceback']}</pre>" if prueba['traceback'] else ""
                    html += f"""
                    <div class="prueba fallida">
                        <div class="nombre-prueba">{prueba['name']}</div>
                        <div class="estado-badge badge-fallida">Fallida</div>
                        {traceback_html}
                    </div>
"""
            
            html += """
                </div>
            </div>
"""
        
        # Agregar detalles de errores
        if errores > 0:
            html += """
            <div class="detalles">
                <div class="seccion-pruebas">
                    <h2>⚠ Pruebas con Error ({count})</h2>
""".format(count=errores)
            
            for prueba in resultado.test_cases:
                if prueba['status'] == 'error':
                    traceback_html = f"<pre class='traceback'>{prueba['traceback']}</pre>" if prueba['traceback'] else ""
                    html += f"""
                    <div class="prueba error">
                        <div class="nombre-prueba">{prueba['name']}</div>
                        <div class="estado-badge badge-error">Error</div>
                        {traceback_html}
                    </div>
"""
            
            html += """
                </div>
            </div>
"""
        
        # Pie de página
        html += f"""
        <div class="pie">
            <p>Reporte generado el {datetime.now().strftime('%d de %B de %Y a las %H:%M:%S')}</p>
            <p>Automation Testing - Sauce Demo</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Guardar el archivo HTML
        with open(self.archivo_html, 'w', encoding='utf-8') as archivo:
            archivo.write(html)
        
        print(f"\n✓ Reporte HTML generado: {self.archivo_html}")

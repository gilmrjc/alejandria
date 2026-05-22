#!/usr/bin/env python3
"""
Servidor HTTP simple para servir el grafo de dependencias.
Genera el JSON dinámicamente usando query_docs.py
"""

import http.server
import socketserver
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Agregar el directorio scripts al path para importar query_docs
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from query_docs import CLI


class GraphHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personalizado que genera el JSON dinámicamente."""
    
    def __init__(self, *args, **kwargs):
        # Configurar el directorio base para servir archivos (docs/)
        self.docs_dir = script_dir.parent / 'docs'
        super().__init__(*args, directory=str(self.docs_dir), **kwargs)
    
    def guess_type(self, path):
        """Asegurar MIME type correcto para ES6 modules."""
        mimetype = super().guess_type(path)
        if path.endswith('.js'):
            return 'application/javascript'
        return mimetype
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # Endpoint para generar el JSON dinámicamente
        if parsed_path.path == '/dependency-graph.json':
            self.send_json()
        else:
            # Servir archivos estáticos normalmente
            super().do_GET()
    
    def send_json(self):
        """Genera y envía el JSON del grafo."""
        try:
            # Usar query_docs para generar el grafo
            docs_dir = str(self.docs_dir)
            cli = CLI(docs_dir)
            
            # Usar el GraphExporter para generar el grafo
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
                tmp_path = tmp.name
            
            try:
                cli.exporter.export(tmp_path)
                
                # Leer el JSON generado
                with open(tmp_path, 'r', encoding='utf-8') as f:
                    graph_data = json.load(f)
                
                # Enviar respuesta JSON
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Expires', '0')
                self.end_headers()
                self.wfile.write(json.dumps(graph_data, indent=2, ensure_ascii=False).encode('utf-8'))
            finally:
                # Limpiar archivo temporal
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_data = {'error': str(e), 'nodes': [], 'edges': []}
            self.wfile.write(json.dumps(error_data).encode('utf-8'))


def main():
    PORT = 8000
    
    with socketserver.TCPServer(("", PORT), GraphHandler) as httpd:
        print(f"🚀 Servidor corriendo en http://localhost:{PORT}")
        print(f"📊 Grafo disponible en http://localhost:{PORT}/dependency-graph.json")
        print(f"🌐 Visualización en http://localhost:{PORT}/dependency-graph-interactive.html")
        print(f"\nPresiona Ctrl+C para detener el servidor")
        httpd.serve_forever()


if __name__ == '__main__':
    main()

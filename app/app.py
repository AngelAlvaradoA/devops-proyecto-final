import os
import platform
from datetime import datetime
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

HOSTNAME = platform.node()
ENVIRONMENT = os.getenv("ENVIRONMENT", "desarrollo")

INVENTORY = [
    {"id": "TEC-001", "nombre": "Laptop ProBook 450 G10", "categoria": "Laptops", "stock": 45, "estado": "Disponible", "precio_unitario": 8499.00},
    {"id": "TEC-002", "nombre": "Monitor UltraSharp 27\" 4K", "categoria": "Monitores", "stock": 3, "estado": "Stock Bajo", "precio_unitario": 5299.00},
    {"id": "TEC-003", "nombre": "Teclado Mecánico RGB K95", "categoria": "Periféricos", "stock": 0, "estado": "Agotado", "precio_unitario": 1899.00},
    {"id": "TEC-004", "nombre": "Mouse Logitech MX Master 3S", "categoria": "Periféricos", "stock": 128, "estado": "Disponible", "precio_unitario": 1299.00},
    {"id": "TEC-005", "nombre": "Servidor Dell PowerEdge R750", "categoria": "Servidores", "stock": 7, "estado": "Disponible", "precio_unitario": 125000.00},
    {"id": "TEC-006", "nombre": "Switch Cisco Catalyst 9200", "categoria": "Redes", "stock": 15, "estado": "Disponible", "precio_unitario": 23400.00},
    {"id": "TEC-007", "nombre": "Disco SSD Samsung 870 EVO 1TB", "categoria": "Almacenamiento", "stock": 2, "estado": "Stock Bajo", "precio_unitario": 1599.00},
    {"id": "TEC-008", "nombre": "Webcam Logitech StreamCam", "categoria": "Periféricos", "stock": 0, "estado": "Agotado", "precio_unitario": 1899.00},
]

METRICS = {
    "total_productos": 1284,
    "stock_critico": 23,
    "proveedores": 47,
    "valor_inventario": 2847392,
}

MOVEMENTS = [
    {"fecha": "2025-05-28", "producto": "Laptop ProBook 450 G10", "tipo": "Entrada", "cantidad": 12},
    {"fecha": "2025-05-27", "producto": "Monitor UltraSharp 27\" 4K", "tipo": "Salida", "cantidad": 5},
    {"fecha": "2025-05-26", "producto": "Teclado Mecánico RGB K95", "tipo": "Salida", "cantidad": 8},
    {"fecha": "2025-05-25", "producto": "Mouse Logitech MX Master 3S", "tipo": "Entrada", "cantidad": 50},
    {"fecha": "2025-05-24", "producto": "Servidor Dell PowerEdge R750", "tipo": "Salida", "cantidad": 2},
]

ALERTS = [
    {"tipo": "warning", "mensaje": "Stock crítico en Monitor UltraSharp 27\" 4K (3 unidades restantes)"},
    {"tipo": "error", "mensaje": "Teclado Mecánico RGB K95 agotado - solicitar reabastecimiento urgente"},
    {"tipo": "success", "mensaje": "Pedido #ORD-8923 recibido y verificado correctamente"},
    {"tipo": "info", "mensaje": "Actualización de plataforma v2.1 programada para el 01/06/2025"},
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TECNA | Inventory Management Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; }
        body { background: #f0f2f5; color: #1f2937; display: flex; min-height: 100vh; }
        .sidebar { width: 240px; background: #ffffff; border-right: 1px solid #e5e7eb; display: flex; flex-direction: column; position: fixed; top: 0; left: 0; height: 100vh; z-index: 100; }
        .sidebar-logo { padding: 20px 24px; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; gap: 10px; }
        .sidebar-logo span { font-size: 22px; font-weight: 700; color: #1f6feb; letter-spacing: 1px; }
        .sidebar-logo small { font-size: 11px; color: #6b7280; display: block; margin-top: 2px; }
        .sidebar-menu { flex: 1; padding: 12px 0; }
        .sidebar-menu a { display: flex; align-items: center; gap: 12px; padding: 12px 24px; color: #6b7280; text-decoration: none; font-size: 14px; transition: all 0.2s; border-left: 3px solid transparent; }
        .sidebar-menu a:hover, .sidebar-menu a.active { background: #f9fafb; color: #1f2937; border-left-color: #1f6feb; }
        .sidebar-menu a.active { color: #1f6feb; font-weight: 600; }
        .sidebar-menu .icon { width: 18px; text-align: center; font-size: 16px; }
        .main { flex: 1; margin-left: 240px; display: flex; flex-direction: column; min-height: 100vh; }
        .navbar { background: #ffffff; border-bottom: 1px solid #e5e7eb; padding: 0 32px; height: 64px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 50; }
        .navbar-left { display: flex; align-items: center; gap: 16px; }
        .navbar-left h2 { font-size: 18px; font-weight: 600; color: #1f2937; }
        .navbar-left .env-badge { background: #1f6feb; color: #fff; font-size: 10px; padding: 2px 10px; border-radius: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
        .navbar-right { display: flex; align-items: center; gap: 20px; }
        .navbar-right .user-info { display: flex; align-items: center; gap: 10px; }
        .navbar-right .avatar { width: 34px; height: 34px; border-radius: 50%; background: #1f6feb; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; color: #fff; }
        .navbar-right .user-detail .name { font-size: 14px; font-weight: 600; color: #1f2937; }
        .navbar-right .user-detail .status { font-size: 12px; color: #16a34a; display: flex; align-items: center; gap: 5px; }
        .navbar-right .user-detail .status::before { content: ''; width: 7px; height: 7px; background: #16a34a; border-radius: 50%; display: inline-block; }
        .content { padding: 28px 32px; flex: 1; }
        .metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 28px; }
        .metric-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 22px 24px; transition: border-color 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
        .metric-card:hover { border-color: #1f6feb; }
        .metric-card .label { font-size: 13px; color: #6b7280; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
        .metric-card .value { font-size: 28px; font-weight: 700; color: #1f2937; }
        .metric-card .change { font-size: 13px; margin-top: 6px; }
        .metric-card .change.up { color: #16a34a; }
        .metric-card .change.warn { color: #d97706; }
        .metric-card .change.ok { color: #16a34a; }
        .section-title { font-size: 16px; font-weight: 600; color: #1f2937; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
        .section-title .count { font-size: 12px; font-weight: 400; color: #6b7280; background: #f3f4f6; padding: 2px 10px; border-radius: 10px; }
        .table-container { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; overflow: hidden; margin-bottom: 28px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
        table { width: 100%; border-collapse: collapse; }
        thead { background: #f9fafb; }
        th { text-align: left; padding: 12px 20px; font-size: 12px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #e5e7eb; }
        td { padding: 14px 20px; font-size: 14px; border-bottom: 1px solid #f3f4f6; }
        tr:last-child td { border-bottom: none; }
        tr:hover td { background: #f9fafb; }
        .status-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
        .status-badge.available { background: rgba(22,163,74,0.1); color: #16a34a; }
        .status-badge.low { background: rgba(217,119,6,0.1); color: #d97706; }
        .status-badge.out { background: rgba(220,38,38,0.1); color: #dc2626; }
        .panels { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 28px; }
        .panel { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 20px 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
        .panel-title { font-size: 14px; font-weight: 600; color: #1f2937; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 1px solid #f3f4f6; }
        .movement-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #f3f4f6; font-size: 13px; }
        .movement-item:last-child { border-bottom: none; }
        .movement-item .date { color: #6b7280; min-width: 85px; }
        .movement-item .prod { flex: 1; color: #1f2937; padding: 0 12px; }
        .movement-item .qty { font-weight: 600; }
        .movement-item .qty.in { color: #16a34a; }
        .movement-item .qty.out { color: #dc2626; }
        .alert-item { display: flex; align-items: flex-start; gap: 12px; padding: 10px 0; border-bottom: 1px solid #f3f4f6; font-size: 13px; }
        .alert-item:last-child { border-bottom: none; }
        .alert-item .icon { font-size: 18px; flex-shrink: 0; margin-top: 1px; }
        .alert-item .icon.warning { color: #d97706; }
        .alert-item .icon.error { color: #dc2626; }
        .alert-item .icon.success { color: #16a34a; }
        .alert-item .icon.info { color: #2563eb; }
        .alert-item .msg { color: #1f2937; line-height: 1.4; }
        .footer { text-align: center; padding: 20px 32px; border-top: 1px solid #e5e7eb; font-size: 13px; color: #9ca3af; margin-top: auto; }
        .footer strong { color: #6b7280; }
        @media (max-width: 1024px) { .metrics { grid-template-columns: repeat(2, 1fr); } .panels { grid-template-columns: 1fr; } }
        @media (max-width: 768px) { .sidebar { width: 60px; } .sidebar-logo span, .sidebar-logo small, .sidebar-menu a span:not(.icon) { display: none; } .sidebar-menu a { justify-content: center; padding: 12px; } .main { margin-left: 60px; } .metrics { grid-template-columns: 1fr; } .navbar { padding: 0 16px; } .content { padding: 16px; } }
    </style>
</head>
<body>
    <nav class="sidebar">
        <div class="sidebar-logo">
            <div><span>TECNA</span><small>Inventory Platform</small></div>
        </div>
        <div class="sidebar-menu">
            <a href="#" class="active"><span class="icon">📊</span> <span>Dashboard</span></a>
            <a href="#"><span class="icon">📦</span> <span>Inventario</span></a>
            <a href="#"><span class="icon">🏷️</span> <span>Productos</span></a>
            <a href="#"><span class="icon">🤝</span> <span>Proveedores</span></a>
            <a href="#"><span class="icon">📈</span> <span>Reportes</span></a>
            <a href="#"><span class="icon">⚙️</span> <span>Configuración</span></a>
        </div>
    </nav>
    <div class="main">
        <header class="navbar">
            <div class="navbar-left">
                <h2>Dashboard</h2>
                <span class="env-badge">{{ environment }}</span>
            </div>
            <div class="navbar-right">
                <div class="user-info">
                    <div class="avatar">A</div>
                    <div class="user-detail">
                        <div class="name">Admin</div>
                        <div class="status">En línea</div>
                    </div>
                </div>
            </div>
        </header>
        <div class="content">
            <div class="metrics">
                <div class="metric-card">
                    <div class="label">Total Productos</div>
                    <div class="value" style="color:#58a6ff;">{{ metrics.total_productos | format_number }}</div>
                    <div class="change up">↑ 12% este mes</div>
                </div>
                <div class="metric-card">
                    <div class="label">Stock Crítico</div>
                    <div class="value" style="color:#d29922;">{{ metrics.stock_critico }} items</div>
                    <div class="change warn">⚠ Requiere atención</div>
                </div>
                <div class="metric-card">
                    <div class="label">Proveedores Activos</div>
                    <div class="value" style="color:#3fb950;">{{ metrics.proveedores }}</div>
                    <div class="change ok">✓ Todos operativos</div>
                </div>
                <div class="metric-card">
                    <div class="label">Valor en Inventario</div>
                    <div class="value" style="color:#e6edf3;">Q {{ "{:,.0f}".format(metrics.valor_inventario) }}</div>
                    <div class="change up">↑ 8% vs mes anterior</div>
                </div>
            </div>
            <div class="section-title">Inventario Reciente <span class="count">{{ inventory | length }} productos</span></div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Producto</th>
                            <th>Categoría</th>
                            <th>Stock</th>
                            <th>Estado</th>
                            <th>Última actualización</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in inventory %}
                        <tr>
                            <td style="color:#58a6ff; font-weight:600;">{{ item.id }}</td>
                            <td>{{ item.nombre }}</td>
                            <td style="color:#8b949e;">{{ item.categoria }}</td>
                            <td>{{ item.stock }}</td>
                            <td>
                                {% if item.estado == "Disponible" %}
                                <span class="status-badge available">{{ item.estado }}</span>
                                {% elif item.estado == "Stock Bajo" %}
                                <span class="status-badge low">{{ item.estado }}</span>
                                {% else %}
                                <span class="status-badge out">{{ item.estado }}</span>
                                {% endif %}
                            </td>
                            <td style="color:#8b949e;">2025-05-28</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <div class="panels">
                <div class="panel">
                    <div class="panel-title">Movimientos Recientes</div>
                    {% for m in movements %}
                    <div class="movement-item">
                        <span class="date">{{ m.fecha }}</span>
                        <span class="prod">{{ m.producto }}</span>
                        <span class="qty {{ 'in' if m.tipo == 'Entrada' else 'out' }}">{{ '+' if m.tipo == 'Entrada' else '-' }}{{ m.cantidad }}</span>
                    </div>
                    {% endfor %}
                </div>
                <div class="panel">
                    <div class="panel-title">Alertas del Sistema</div>
                    {% for a in alerts %}
                    <div class="alert-item">
                        <span class="icon {{ a.tipo }}">{% if a.tipo == 'warning' %}⚠️{% elif a.tipo == 'error' %}🔴{% elif a.tipo == 'success' %}✅{% else %}ℹ️{% endif %}</span>
                        <span class="msg">{{ a.mensaje }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
            <div class="section-title">Hostname: <span style="color:#8b949e;font-weight:400;">{{ hostname }}</span></div>
        </div>
        <footer class="footer">
            <strong>TECNA</strong> &copy; 2025 | Inventory Management Platform v2.1
        </footer>
    </div>
</body>
</html>"""

@app.template_filter()
def format_number(value):
    return "{:,}".format(value)

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE,
        hostname=HOSTNAME,
        environment=ENVIRONMENT,
        metrics=METRICS,
        inventory=INVENTORY,
        movements=MOVEMENTS,
        alerts=ALERTS)

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "TECNA Inventory API",
        "hostname": HOSTNAME,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/info")
def info():
    return jsonify({
        "app": "TECNA Inventory Platform",
        "version": "2.1.0",
        "hostname": HOSTNAME,
        "environment": ENVIRONMENT,
        "stack": ["Flask", "Docker", "PostgreSQL", "Docker Swarm", "GCP"]
    })

@app.route("/api/inventory")
def api_inventory():
    return jsonify(INVENTORY)

@app.route("/api/metrics")
def api_metrics():
    return jsonify(METRICS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

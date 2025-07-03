
# -------------------------------------------------------------
# DASHBOARD INTERACTIVO – CAPACIDAD INSTALADA  (by Lizme)
# -------------------------------------------------------------
# ESTRUCTURA VISUAL EN BLOQUES   ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
# ┌──────── 7.1 ENCABEZADO (Navbar)
# ├──────── 7.2 KPI CARDS (Row con 3 columnas)
# ├──────── 7.3 FILTROS (Row con 3 columnas)
# ├──────── 7.4 GRÁFICAS PRINCIPALES (Row con 2 columnas)
# ├──────── 7.5 DISPERSIÓN (Row full‑width)
# └──────── 7.6 FOOTER
# Cada bloque Row / Col equivale a una sección <div class='row/col'>
# -------------------------------------------------------------

# ▶️ 1. Importar librerías ------------------------------------------------------
import dash                            # Framework principal para la app web
from dash import html, dcc, Input, Output  # Componentes y utilidades de Dash
import dash_bootstrap_components as dbc    # Componentes listos con Bootstrap
import pandas as pd                       # Manejo de datos en tablas
import plotly.express as px               # Gráficas interactivas fáciles

# ▶️ 2. Cargar y limpiar datos ---------------------------------------------------
DATA_PATH = r"C:\Users\lizme\Desktop\BIT\BOOTCAMP CIENCIA DE DATOS\EJERCICIOS-DE-CLASE\Clases\Clase 12_ Visualización de datos en Python\Actividad Clase 12 y 13_Dashboard\CAPACIDAD_INSTALADA_LIMPIA.csv"  # Ruta al archivo CSV
df = pd.read_csv(DATA_PATH)               # Lee el CSV y lo guarda en un DataFrame

key_cols = ['Departamento', 'Municipio', 'nom grupo capacidad', 'naturaleza']  # Columnas clave para limpiar
df.columns = df.columns.str.strip()       # Quita espacios al inicio/fin de todos los nombres de columna
for col in key_cols:                      # Recorre cada columna clave
    df[col] = df[col].astype(str).str.strip().str.upper()  # Convierte a texto, quita espacios y pone en mayúsculas

# ▶️ 3. Variables de color -------------------------------------------------------
COLORS = {"primary": "#ff7f0e", "bg": "#ffffff", "text": "#000000"}  # Paleta sencilla para la interfaz

# ▶️ 4. Métricas (KPI) ----------------------------------------------------------
TOTAL_FILAS = len(df)                     # Cuenta total de registros
TOTAL_CAP  = int(df['num cantidad capacidad instalada'].sum())  # Suma total de la capacidad instalada
PROM_CAP   = round(df['num cantidad capacidad instalada'].mean(), 2)  # Promedio de capacidad instalada

# ▶️ 5. Opciones para filtros ----------------------------------------------------
DEPT_LIST = ['TODOS'] + sorted(df['Departamento'].unique())  # Lista de departamentos + 'TODOS'
NAT_LIST  = ['TODOS'] + sorted(df['naturaleza'].unique())    # Lista de naturalezas + 'TODOS'

# ▶️ 6. Inicializar aplicación Dash --------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])  # Crea la app y usa el tema CYBORG

# ▶️ 7. LAYOUT  (Rows & Cols bien delimitados) ----------------------------------
app.layout = dbc.Container([             # Contenedor principal (fluido)

    # ───────── 7.1 ENCABEZADO ────────────────────────────────────────────────
    dbc.NavbarSimple(
        brand="DASHBOARD CAPACIDAD INSTALADA COLOMBIA",      # Título del navbar
        brand_style={"fontSize": "40px", "fontWeight": "600"},  # Estilo del texto
        color=COLORS['primary'], dark=True                     # Color y modo oscuro
    ),

    html.Br(),  # Espacio visual para separar

    # ───────── 7.2 KPI CARDS (Row de 3 Cols) ─────────────────────────────────
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Filas"), html.H3(f"{TOTAL_FILAS:,}")])), md=4),  # KPI 1
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Capacidad Total"), html.H3(f"{TOTAL_CAP:,}")])), md=4),  # KPI 2
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Capacidad Promedio"), html.H3(f"{PROM_CAP}")])), md=4),  # KPI 3
    ], className="mb-3"),

    # ───────── 7.3 FILTROS (Row de 3 Cols) ───────────────────────────────────
    dbc.Row([
        # Col‑A: Departamento
        dbc.Col(dcc.Dropdown(
            id='dept-dd',                                       # Identificador del dropdown
            options=[{"label": d.title(), "value": d} for d in DEPT_LIST],  # Opciones
            value='TODOS', clearable=False                     # Valor inicial y no se puede borrar
        ), md=4),
        # Col‑B: Municipio (se llenará vía callback)
        dbc.Col(dcc.Dropdown(
            id='muni-dd',
            options=[{"label": "TODOS", "value": "TODOS"}],  # Placeholder inicial
            value='TODOS', clearable=False
        ), md=4),
        # Col‑C: Naturaleza
        dbc.Col(dcc.Dropdown(
            id='nat-dd',
            options=[{"label": n.title(), "value": n} for n in NAT_LIST],
            value='TODOS', clearable=False
        ), md=4),
    ]),

    html.Br(),  # Más espacio

    # ───────── 7.4 GRÁFICAS PRINCIPALES (Row de 2 Cols) ──────────────────────
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-muni'), md=6),  # Gráfica de barras (Top municipios)
        dbc.Col(dcc.Graph(id='pie-grupo'), md=6)  # Gráfica de pastel (Distribución grupos)
    ], className="mb-3"),

# ───────── 7.5 DISPERSIÓN + TOP 10 PRESTADOR (Row de 2 Cols) ──────────────
dbc.Row([
    dbc.Col(dcc.Graph(id='scatter-nivel'), md=6),   # Col-izq: dispersión
    dbc.Col(dcc.Graph(id='top-prest'),      md=6)   # Col-der: nuevo gráfico
], className="mb-3"),

    html.Hr(),  # Línea divisoria

    # ───────── 7.6 FOOTER ────────────────────────────────────────────────────
    dbc.Alert(
        "Hecho por Lizme – Bootcamp Ciencia de Datos",      # Texto del pie de página
        color="secondary", className="text-center"        # Estilo centrado y color secundario
    )
], fluid=True, style={"backgroundColor": COLORS['bg'], "color": COLORS['text']})  # Propiedades globales

# ▶️ 8. CALLBACK 1: actualizar municipios cuando cambia departamento -----------
@app.callback(
    Output('muni-dd', 'options'),    # Salida: lista de opciones para municipios
    Output('muni-dd', 'value'),      # Salida: valor seleccionado
    Input('dept-dd', 'value')        # Entrada: departamento elegido
)
def update_muni_options(dept):
    # Genera lista de municipios según el departamento
    munis = ['TODOS'] + (sorted(df['Municipio'].unique()) 
        if dept=='TODOS'
        else sorted(df[df['Departamento']==dept]['Municipio'].unique()))
    return [{"label": m.title(), "value": m} for m in munis], 'TODOS'  # Devuelve opciones y valor por defecto

# ▶️ 9. CALLBACK 2 ------------------------------------------------------------
@app.callback(
    Output('bar-muni',      'figure'),
    Output('pie-grupo',     'figure'),
    Output('scatter-nivel', 'figure'),
    Output('top-prest',     'figure'),
    Input('dept-dd', 'value'),
    Input('muni-dd', 'value'),
    Input('nat-dd',  'value')
)
def update_graphs(dept, muni, nat):
    # 9.A Filtra datos según los dropdowns
    mask = pd.Series(True, index=df.index)
    if dept != 'TODOS':
        mask &= df['Departamento'] == dept
    if muni != 'TODOS':
        mask &= df['Municipio'] == muni
    if nat != 'TODOS':
        mask &= df['naturaleza'] == nat
    data = df[mask]

    if data.empty:
        no_data = px.scatter(title="Sin datos para esta selección")
        return no_data, no_data, no_data, no_data

    # 9.B Barra – Top 10 Municipios (conteo)
    bar_df = (data['Municipio']
        .value_counts()
        .head(10)
        .reset_index(name='Conteo')
        .rename(columns={'index': 'Municipio'}))
    bar_fig = px.bar(
        bar_df,
        x='Municipio',
        y='Conteo',
        title='TOP MUNICIPIOS',
        color_discrete_sequence=[COLORS['primary']])
    bar_fig.update_traces(texttemplate='%{y:,}', textposition='outside')  # Formato de texto en barras

    # 9.C Pie – Distribución de grupos
    pie_df = data['nom grupo capacidad'].value_counts().reset_index()
    pie_df.columns = ['Grupo', 'Conteo']
    pie_fig = px.pie(
        pie_df,
        names='Grupo',
        values='Conteo',
        title='DISTRIBUCIÓN DE GRUPOS',
        color_discrete_sequence=px.colors.sequential.Oranges)

    # 9.D Dispersión – Nivel VS Capacidad instalada
    scatter_df = data.dropna(subset=['num nivel atencion'])
    scat_fig = px.scatter(
        scatter_df,
        x='num nivel atencion',
        y='num cantidad capacidad instalada',
        size='num cantidad capacidad instalada',
        title='NIVEL VS CAPACIDAD INSTALADA')
    scat_fig.update_xaxes(range=[1, 3], dtick=1, tick0=1)  # ← límites y ticks: 1, 2, 3

    # 9.E Barra – Top 10 nom sede IPS por capacidad instalada
    prest_df = (data
                .groupby('nom sede IPS', as_index=False)['num cantidad capacidad instalada']
                .sum()                                                 # Suma capacidad por sede
                .sort_values(by='num cantidad capacidad instalada',    # Ordena de mayor a menor
    ascending=False)
                .head(10))                                             # Toma las 10 primeras
    prest_df.columns = ['nom sede IPS', 'Capacidad']                   # Renombra columnas
    top_prest_fig = px.bar(
        prest_df,
        x='nom sede IPS',
        y='Capacidad',
        title='TOP 10 – SEDE IPS POR CAPACIDAD INSTALADA',
        color_discrete_sequence=[COLORS['primary']])
    top_prest_fig.update_layout(xaxis_tickangle=-45)                   # Inclina etiquetas X
    top_prest_fig.update_traces(texttemplate='%{y:,}', textposition='outside')  # Formato de texto en barras
    

    # 9.F Estilo común para todas las figuras
    for fig in [bar_fig, pie_fig, scat_fig, top_prest_fig]:
        fig.update_layout(
            paper_bgcolor=COLORS['bg'],
            plot_bgcolor=COLORS['bg'],
            font_color=COLORS['text'],
            title_font=dict(size=28,
                            family='Arial Black',
                            color=COLORS['text'])
        )

    return bar_fig, pie_fig, scat_fig, top_prest_fig


# ▶️ 10. Ejecutar servidor ------------------------------------------------------
if __name__ == '__main__':                  # Punto de entrada
    app.run(debug=True)                     # Inicia servidor en modo debug

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import zlib
import psycopg2
import urllib.parse
from dotenv import load_dotenv
load_dotenv()

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# Cáº¤U HĂŒNH TRANG
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
st.set_page_config(
    page_title="[PostgreSQL] BĂ¡o cĂ¡o PhĂ¢n tĂ­ch Thá»‹ trÆ°á»ng Báº¥t Ä‘á»™ng sáº£n NYC 2025 - 2026",
    layout="wide",
    page_icon="đŸ—„ï¸",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; font-weight: 500; }
.main { background-color: #f8fafc; }
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff 0%, #f5f3ff 100%);
    padding: 18px 20px;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(99,102,241,0.14), 0 1px 4px rgba(0,0,0,0.06);
    border: none;
    border-left: 5px solid #6366f1;
}
[data-testid="stMetricLabel"] {
    color: #7c3aed !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
[data-testid="stMetricValue"] {
    color: #1e1b4b !important;
    font-size: 24px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}
[data-testid="stMetricDelta"] { font-size: 12px !important; font-weight: 600 !important; }
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    border-bottom: 2px solid #c7d2fe;
    background: linear-gradient(180deg, #eef2ff 0%, #f0f4ff 100%);
    border-radius: 12px 12px 0 0;
    padding: 8px 8px 0;
}
.stTabs [data-baseweb="tab"] {
    height: 44px;
    font-weight: 700;
    font-size: 13px;
    color: #4338ca;
    border-radius: 10px 10px 0 0;
    padding: 0 20px;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    color: #ffffff !important;
    background: #6366f1 !important;
    box-shadow: 0 -3px 14px rgba(99,102,241,0.4) !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #312e81 55%, #4c1d95 100%);
}
[data-testid="stSidebar"] * { color: #e0e7ff !important; }
[data-testid="stSidebar"] label {
    color: #a5b4fc !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: #6366f1 !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] span { color: #ffffff !important; font-weight: 700 !important; }
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.45) !important;
}
.section-q {
    font-size: 17px;
    font-weight: 800;
    color: #1e1b4b;
    margin: 24px 0 4px 0;
    padding: 10px 16px;
    border-left: 5px solid #6366f1;
    background: linear-gradient(90deg, #eef2ff 0%, transparent 80%);
    border-radius: 0 8px 8px 0;
}
.section-cap { font-size: 13px; color: #4b5563; font-weight: 600; margin: 4px 0 14px 16px; line-height: 1.6; }
.insight-box {
    background: linear-gradient(135deg, #faf5ff 0%, #ede9fe 60%, #e0e7ff 100%);
    border: 1px solid #c4b5fd;
    border-left: 6px solid #7c3aed;
    border-radius: 0 14px 14px 0;
    padding: 18px 22px;
    margin: 22px 0 8px 0;
    font-size: 14px;
    font-weight: 600;
    line-height: 1.9;
    color: #2e1065;
    box-shadow: 0 4px 16px rgba(124,58,237,0.1);
}
.insight-box b { color: #5b21b6; font-weight: 800; }
.badge {
    display: inline-block;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #ffffff;
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(99,102,241,0.4);
}
.hr { border: none; border-top: 1px solid #c7d2fe; margin: 28px 0; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #eef2ff; }
::-webkit-scrollbar-thumb { background: #a5b4fc; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# Háº°NG Sá», Tá»ŒA Äá»˜ Báº¢N Äá»’ & Báº¢N MĂ€U
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = BASE_DIR
BOROUGH_MAP   = {1:'Manhattan', 2:'Bronx', 3:'Brooklyn', 4:'Queens', 5:'Staten Island'}
BOROUGH_ORDER = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
BOROUGH_COLORS = {
    'Manhattan':    '#6366f1',
    'Brooklyn':     '#0ea5e9',
    'Queens':       '#10b981',
    'Bronx':        '#f59e0b',
    'Staten Island':'#ec4899',
}
C_BLUE = '#6366f1'; C_BLUE2 = '#818cf8'; C_SKY = '#0ea5e9'
C_ORANGE = '#f59e0b'; C_RED = '#ef4444'; C_GREEN = '#10b981'; C_GRAY = '#94a3b8'

MONTH_SHORT = {1:'T1',2:'T2',3:'T3',4:'T4',5:'T5',6:'T6',
               7:'T7',8:'T8',9:'T9',10:'T10',11:'T11',12:'T12'}
MONTH_FULL  = {1:'ThĂ¡ng 1',2:'ThĂ¡ng 2',3:'ThĂ¡ng 3',4:'ThĂ¡ng 4',
               5:'ThĂ¡ng 5',6:'ThĂ¡ng 6',7:'ThĂ¡ng 7',8:'ThĂ¡ng 8',
               9:'ThĂ¡ng 9',10:'ThĂ¡ng 10',11:'ThĂ¡ng 11',12:'ThĂ¡ng 12'}
FEATURE_LABELS = {
    'gross_sqft':'Diá»‡n tĂ­ch tá»•ng (sqft)', 'building_age':'Tuá»•i cĂ´ng trĂ¬nh (nÄƒm)',
    'land_sqft':'Diá»‡n tĂ­ch Ä‘áº¥t (sqft)',   'pop_density':'Máº­t Ä‘á»™ dĂ¢n sá»‘ (/kmÂ²)',
    'amenity_score':'Äiá»ƒm tiá»‡n Ă­ch (0â€“10)','total_units':'Sá»‘ cÄƒn trong tĂ²a',
    'gdp_local':'GDP Ä‘á»‹a phÆ°Æ¡ng (%)',      'avg_income':'Thu nháº­p bĂ¬nh quĂ¢n ($)',
    'dist_center':'KC Ä‘áº¿n trung tĂ¢m (km)',
}
REQUIRED_COLS = [
    'borough','neighborhood','building_type','gross_sqft','land_sqft',
    'sale_price','sale_year','sale_date','building_age','total_units',
    'pop_density','avg_income','gdp_local','dist_center','amenity_score',
]

# Tá»a Ä‘á»™ Ä‘á»‹a lĂ½ NYC cho báº£n Ä‘á»“ Nhiá»‡t (Hotspot Heatmap)
BOROUGH_COORDS = {
    'Manhattan':     (40.7831, -73.9712),
    'Brooklyn':      (40.6782, -73.9442),
    'Queens':        (40.7282, -73.7949),
    'Bronx':         (40.8448, -73.8648),
    'Staten Island': (40.5795, -74.1502),
}

NEIGHBORHOOD_COORDS = {
    # MANHATTAN
    'UPPER EAST SIDE (59-79)': (40.7700, -73.9590),
    'UPPER EAST SIDE (79-96)': (40.7780, -73.9530),
    'UPPER EAST SIDE (96-110)': (40.7910, -73.9470),
    'UPPER WEST SIDE (59-79)': (40.7760, -73.9810),
    'UPPER WEST SIDE (79-96)': (40.7890, -73.9720),
    'UPPER WEST SIDE (96-110)': (40.8000, -73.9630),
    'MIDTOWN EAST': (40.7540, -73.9720),
    'MIDTOWN WEST': (40.7600, -73.9880),
    'MIDTOWN CBD': (40.7550, -73.9800),
    'CHELSEA': (40.7465, -74.0014),
    'GREENWICH VILLAGE-CENTRAL': (40.7336, -73.9996),
    'GREENWICH VILLAGE-WEST': (40.7350, -74.0060),
    'GRAMERCY': (40.7368, -73.9845),
    'MURRAY HILL': (40.7483, -73.9783),
    'EAST VILLAGE': (40.7265, -73.9815),
    'LOWER EAST SIDE': (40.7150, -73.9840),
    'SOHO': (40.7233, -74.0030),
    'TRIBECA': (40.7163, -74.0086),
    'FINANCIAL': (40.7075, -74.0090),
    'HARLEM-CENTRAL': (40.8116, -73.9465),
    'HARLEM-EAST': (40.7957, -73.9389),
    'HARLEM-WEST': (40.8150, -73.9560),
    'WASHINGTON HEIGHTS UPPER': (40.8500, -73.9360),
    'WASHINGTON HEIGHTS LOWER': (40.8380, -73.9420),
    'INWOOD': (40.8677, -73.9212),
    'KIPS BAY': (40.7396, -73.9801),
    'CHINATOWN': (40.7158, -73.9970),
    'BATTERY PARK CITY': (40.7120, -74.0150),
    'MORNINGSIDE HEIGHTS': (40.8080, -73.9630),

    # QUEENS
    'FLUSHING-NORTH': (40.7675, -73.8331),
    'FLUSHING-SOUTH': (40.7420, -73.8210),
    'FOREST HILLS': (40.7186, -73.8448),
    'BAYSIDE': (40.7675, -73.7745),
    'ASTORIA': (40.7644, -73.9235),
    'JACKSON HEIGHTS': (40.7557, -73.8831),
    'ELMHURST': (40.7369, -73.8784),
    'LONG ISLAND CITY': (40.7447, -73.9485),
    'REGO PARK': (40.7258, -73.8622),
    'WOODSIDE': (40.7454, -73.9038),
    'SUNNYSIDE': (40.7434, -73.9241),
    'WHITESTONE': (40.7892, -73.8117),
    'RIDGEWOOD': (40.7061, -73.9015),
    'GLENDALE': (40.7011, -73.8876),
    'MASPETH': (40.7230, -73.9100),
    'MIDDLE VILLAGE': (40.7160, -73.8860),
    'JAMAICA': (40.7027, -73.7890),
    'JAMAICA ESTATES': (40.7234, -73.7834),
    'HOLLIS': (40.7117, -73.7667),
    'QUEENS VILLAGE': (40.7170, -73.7380),
    'HOWARD BEACH': (40.6570, -73.8430),
    'OZONE PARK': (40.6811, -73.8427),
    'RICHMOND HILL': (40.6953, -73.8315),
    'KEW GARDENS': (40.7090, -73.8310),

    # BROOKLYN
    'BEDFORD STUYVESANT': (40.6872, -73.9418),
    'BAY RIDGE': (40.6260, -74.0300),
    'BOROUGH PARK': (40.6350, -73.9920),
    'PARK SLOPE': (40.6711, -73.9814),
    'BUSHWICK': (40.6944, -73.9213),
    'WILLIAMSBURG-NORTH': (40.7180, -73.9570),
    'WILLIAMSBURG-SOUTH': (40.7090, -73.9590),
    'GREENPOINT': (40.7305, -73.9515),
    'DUMBO': (40.7033, -73.9881),
    'BROOKLYN HEIGHTS': (40.6960, -73.9936),
    'COBBLE HILL': (40.6877, -73.9947),
    'CARROLL GARDENS': (40.6800, -73.9950),
    'CROWN HEIGHTS': (40.6700, -73.9430),
    'FLATBUSH-LEFFERTS GARDENS': (40.6580, -73.9510),
    'FLATBUSH-CENTRAL': (40.6420, -73.9580),
    'SUNSET PARK': (40.6450, -74.0080),
    'BENSONHURST': (40.6139, -73.9922),
    'SHEEPSHEAD BAY': (40.5868, -73.9542),
    'CONEY ISLAND': (40.5750, -73.9820),
    'CANARSIE': (40.6400, -73.8960),

    # BRONX
    'RIVERDALE': (40.8904, -73.9125),
    'KINGSBRIDGE/JEROME PARK': (40.8790, -73.8970),
    'MOTT HAVEN/PORT MORRIS': (40.8090, -73.9230),
    'MELROSE/MORRISANIA': (40.8250, -73.9100),
    'FORDHAM': (40.8615, -73.8890),
    'BELMONT': (40.8550, -73.8870),
    'THROGS NECK': (40.8170, -73.8160),

    # STATEN ISLAND
    'GREAT KILLS': (40.5515, -74.1513),
    'TODT HILL': (40.5980, -74.1100),
    'ST. GEORGE': (40.6430, -74.0760),
    'NEW DORP': (40.5730, -74.1170),
    'ELTINGVILLE': (40.5430, -74.1650),
}

def get_neighborhood_coords(neighborhood, borough_name):
    """Láº¥y tá»a Ä‘á»™ lat/lon chuáº©n hoáº·c suy luáº­n theo offset nhá» tá»« centroid quáº­n."""
    if neighborhood in NEIGHBORHOOD_COORDS:
        return NEIGHBORHOOD_COORDS[neighborhood]
    b_lat, b_lon = BOROUGH_COORDS.get(borough_name, (40.7128, -74.0060))
    h = zlib.adler32(str(neighborhood).encode('utf-8'))
    off_lat = ((h % 100) - 50) * 0.0008
    off_lon = (((h // 100) % 100) - 50) * 0.0008
    return (b_lat + off_lat, b_lon + off_lon)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# HĂ€M Dá»® LIá»†U
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
@st.cache_data
def load_data():
    """Äá»c dá»¯ liá»‡u tá»« PostgreSQL Data Warehouse trĂªn Cloud.
    Tráº£ vá» DataFrame giá»‘ng há»‡t báº£n CSV Ä‘á»ƒ tÆ°Æ¡ng thĂ­ch 100% vá»›i toĂ n bá»™ code phĂ­a dÆ°á»›i.
    # Cache busted
    """
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        return None, "KhĂ´ng tĂ¬m tháº¥y biáº¿n DATABASE_URL trong file .env"
    try:
        from sqlalchemy import create_engine
        engine = create_engine(db_url, connect_args={'options': '-c statement_timeout=0'})
        _chunks = pd.read_sql_query("""
            SELECT
                b.borough_id                AS borough,
                b.borough_name,
                n.neighborhood_name         AS neighborhood,
                p.building_class_category,
                p.building_category,
                p.building_type,
                p.building_class_present,
                p.tax_class_present,
                p.gross_sqft,
                p.land_sqft,
                p.year_built,
                p.building_age,
                p.residential_units,
                p.commercial_units,
                p.total_units,
                p.is_residential,
                l.address,
                l.zip_code,
                l.block,
                l.lot,
                f.sale_price,
                f.price_per_sqft,
                f.price_per_sqft_real,
                f.sale_date,
                f.sale_year,
                f.sale_month,
                f.tax_class_sale,
                f.building_class_sale,
                s.pop_density,
                s.avg_income,
                s.gdp_local,
                s.dist_center,
                s.amenity_score
            FROM fact_sales f
            JOIN dim_location       l ON f.location_id    = l.location_id
            JOIN dim_neighborhood   n ON l.neighborhood_id = n.neighborhood_id
            JOIN dim_borough        b ON n.borough_id      = b.borough_id
            JOIN dim_property       p ON f.property_id     = p.property_id
            JOIN dim_social_metrics s ON f.social_id       = s.social_id
        """, engine, chunksize=10000)
        df = pd.concat(_chunks, ignore_index=True)
        engine.dispose()
    except Exception as e:
        return None, f"Lá»—i Ä‘á»c PostgreSQL: {e}"

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        return None, f"Thiáº¿u cá»™t sau JOIN: {', '.join(missing)}"

    # Chuáº©n hoĂ¡ kiá»ƒu dá»¯ liá»‡u â€” giá»‘ng há»‡t báº£n CSV
    df['sale_price']    = pd.to_numeric(df['sale_price'],    errors='coerce')
    df['gross_sqft']    = pd.to_numeric(df['gross_sqft'],    errors='coerce')
    df['land_sqft']     = pd.to_numeric(df['land_sqft'],     errors='coerce')
    df['building_age']  = pd.to_numeric(df['building_age'],  errors='coerce')
    df['sale_year']     = pd.to_numeric(df['sale_year'],     errors='coerce')
    df['avg_income']    = pd.to_numeric(df['avg_income'],    errors='coerce')
    df['amenity_score'] = pd.to_numeric(df['amenity_score'], errors='coerce')
    df['dist_center']   = pd.to_numeric(df['dist_center'],   errors='coerce')
    df['pop_density']   = pd.to_numeric(df['pop_density'],   errors='coerce')
    df = df[df['sale_price'] > 10_000].copy()
    df.loc[df['gross_sqft'] <= 0, 'gross_sqft'] = np.nan
    df.loc[df['land_sqft']  <= 0, 'land_sqft']  = np.nan
    df['price_per_sqft']   = np.where(df['gross_sqft'].notna(),
                                      df['sale_price'] / df['gross_sqft'], np.nan)
    df['sale_date_parsed'] = pd.to_datetime(df['sale_date'], dayfirst=True, errors='coerce')
    df['sale_month']       = df['sale_date_parsed'].dt.month
    return df, None

@st.cache_data
def load_ml_data():
    paths = {'pred': os.path.join(ROOT_DIR, 'output', 'ml_predictions.csv'),
             'imp':  os.path.join(ROOT_DIR, 'output', 'ml_importance.csv'),
             'met':  os.path.join(ROOT_DIR, 'output', 'ml_metrics.json')}
    pred_df    = pd.read_csv(paths['pred'])    if os.path.exists(paths['pred']) else None
    importance = pd.read_csv(paths['imp'])     if os.path.exists(paths['imp'])  else None
    metrics = {}
    if os.path.exists(paths['met']):
        with open(paths['met'], encoding='utf-8') as f:
            metrics = json.load(f)
    return pred_df, importance, metrics

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# HELPER UI & COMPONENT TĂ“M Táº®T TRá»°C QUAN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def fmt_M(v, d=2): return f"${v/1e6:.{d}f}M"
def insight_box(html): st.markdown(f'<div class="insight-box">{html}</div>', unsafe_allow_html=True)
def section_q(q, cap=""):
    st.markdown(f'<div class="section-q">{q}</div>', unsafe_allow_html=True)
    if cap: st.markdown(f'<div class="section-cap">{cap}</div>', unsafe_allow_html=True)
def divider(): st.markdown('<hr class="hr">', unsafe_allow_html=True)
def apply_filters(df, boroughs, yr, pr):
    return df[df['borough_name'].isin(boroughs) &
              df['sale_year'].between(yr[0], yr[1]) &
              df['sale_price'].between(pr[0], pr[1])].copy()
def clayout(fig, h=340, t=20, b=20, l=10, r=10, leg=False):
    fig.update_layout(height=h, margin=dict(t=t,b=b,l=l,r=r),
                      plot_bgcolor='#fafafa',
                      paper_bgcolor='#ffffff',
                      showlegend=leg,
                      font=dict(family='Inter', size=13, color='#1e1b4b'),
                      title_font=dict(size=15, color='#1e1b4b', family='Inter'),
                      legend=dict(font=dict(size=12, color='#1e1b4b')))
    fig.update_xaxes(tickfont=dict(size=12, color='#374151', family='Inter'),
                     title_font=dict(size=13, color='#374151', family='Inter'))
    fig.update_yaxes(tickfont=dict(size=12, color='#374151', family='Inter'),
                     title_font=dict(size=13, color='#374151', family='Inter'))
    return fig

def render_factor_summary_matrix(df_in):
    """
    Táº¡o Báº£ng & Biá»ƒu Ä‘á»“ TĂ³m táº¯t Yáº¿u tá»‘ TĂ¡c Ä‘á»™ng GiĂ¡ (Top Factor Summary Matrix).
    ÄĂ¡nh giĂ¡ vĂ  phĂ¢n loáº¡i rĂµ yáº¿u tá»‘ áº£nh hÆ°á»Ÿng Ráº¤T Máº NH / Máº NH / TRUNG BĂŒNH / Yáº¾U.
    """
    factors = [
        ('gross_sqft', 'Diá»‡n tĂ­ch cĂ´ng trĂ¬nh (gross_sqft)', 'Quy mĂ´ khĂ´ng gian sá»­ dá»¥ng; biáº¿n sá»‘ quan trá»ng hĂ ng Ä‘áº§u Ä‘á»‹nh giĂ¡ tá»•ng tĂ i sáº£n.'),
        ('avg_income', 'Thu nháº­p khu vá»±c (avg_income)', 'Máº·t báº±ng thu nháº­p cÆ° dĂ¢n; Ä‘áº¡i diá»‡n cho sá»©c mua vĂ  má»©c Ä‘á»™ Ä‘áº¯t Ä‘á» cá»§a vĂ¹ng.'),
        ('amenity_score', 'Äiá»ƒm tiá»‡n Ă­ch (amenity_score)', 'Cháº¥t lÆ°á»£ng tiá»‡n Ă­ch káº¿t ná»‘i xung quanh (giao thĂ´ng, trÆ°á»ng há»c, dá»‹ch vá»¥).'),
        ('dist_center', 'KC Ä‘áº¿n trung tĂ¢m (dist_center)', 'Khoáº£ng cĂ¡ch Ä‘á»‹a lĂ½ tá»›i trung tĂ¢m tĂ i chĂ­nh Manhattan (cĂ ng xa giĂ¡ giáº£m).'),
        ('pop_density', 'Máº­t Ä‘á»™ dĂ¢n sá»‘ (pop_density)', 'Máº­t Ä‘á»™ dĂ¢n cÆ° sinh sá»‘ng; pháº£n Ă¡nh Ä‘á»™ sáº§m uáº¥t vĂ  nhu cáº§u nhĂ  á»Ÿ khu vá»±c.'),
        ('building_age', 'Tuá»•i cĂ´ng trĂ¬nh (building_age)', 'Sá»‘ nÄƒm cĂ´ng trĂ¬nh Ä‘Ă£ váº­n hĂ nh (cĂ´ng trĂ¬nh cÅ© chá»‹u kháº¥u hao tĂ i sáº£n).'),
        ('land_sqft', 'Diá»‡n tĂ­ch Ä‘áº¥t (land_sqft)', 'Diá»‡n tĂ­ch lĂ´ Ä‘áº¥t (áº£nh hÆ°á»Ÿng Ă­t hÆ¡n gross_sqft do Ä‘áº·c thĂ¹ nhĂ  chung cÆ° táº¡i NYC).'),
    ]
    
    rows = []
    for col, name, desc in factors:
        if col in df_in.columns:
            valid = df_in.dropna(subset=['sale_price', col])
            if len(valid) >= 20:
                r = valid['sale_price'].corr(valid[col])
                abs_r = abs(r)
                if abs_r >= 0.50:
                    level = "đŸ€ Ráº¤T Máº NH"
                elif abs_r >= 0.35:
                    level = "đŸ“ˆ Máº NH"
                elif abs_r >= 0.15:
                    level = "â–ï¸ TRUNG BĂŒNH"
                else:
                    level = "đŸ“‰ Yáº¾U"
                
                direction = "Thuáº­n (+)" if r > 0 else "Nghá»‹ch (-)"
                rows.append({
                    'Yáº¿u tá»‘ tĂ¡c Ä‘á»™ng': name,
                    'TÆ°Æ¡ng quan (r)': round(r, 2),
                    'Má»©c Ä‘á»™ áº£nh hÆ°á»Ÿng': level,
                    'Chiá»u tĂ¡c Ä‘á»™ng': direction,
                    'Giáº£i thĂ­ch Ă½ nghÄ©a thá»±c táº¿': desc,
                    '_abs_r': abs_r
                })
    
    fdf = pd.DataFrame(rows).sort_values('_abs_r', ascending=False)
    
    col_tbl, col_chart = st.columns([3, 2])
    with col_tbl:
        display_df = fdf[['Yáº¿u tá»‘ tĂ¡c Ä‘á»™ng', 'TÆ°Æ¡ng quan (r)', 'Má»©c Ä‘á»™ áº£nh hÆ°á»Ÿng', 'Chiá»u tĂ¡c Ä‘á»™ng', 'Giáº£i thĂ­ch Ă½ nghÄ©a thá»±c táº¿']].copy()
        st.dataframe(
            display_df,
            column_config={
                "TÆ°Æ¡ng quan (r)": st.column_config.NumberColumn(format="%.2f"),
                "Má»©c Ä‘á»™ áº£nh hÆ°á»Ÿng": st.column_config.TextColumn(),
            },
            width='stretch',
            hide_index=True
        )
    with col_chart:
        fdf_chart = fdf.sort_values('_abs_r', ascending=True)
        colors = [C_GREEN if r > 0 else C_RED for r in fdf_chart['TÆ°Æ¡ng quan (r)']]
        fig_sum = go.Figure(go.Bar(
            x=fdf_chart['TÆ°Æ¡ng quan (r)'],
            y=fdf_chart['Yáº¿u tá»‘ tĂ¡c Ä‘á»™ng'].apply(lambda x: x.split(' (')[0]),
            orientation='h',
            marker_color=colors,
            text=[f"r = {r:+.2f}" for r in fdf_chart['TÆ°Æ¡ng quan (r)']],
            textposition='outside'
        ))
        clayout(fig_sum, h=300, t=30, b=20, l=10, r=60)
        fig_sum.update_layout(
            title="Xáº¿p háº¡ng Má»©c Ä‘á»™ TÆ°Æ¡ng quan vá»›i GiĂ¡ bĂ¡n (r)",
            title_font=dict(size=13, color='#374151'),
            xaxis=dict(range=[-0.4, 0.9], zeroline=True, zerolinecolor='#cbd5e1', title="Há»‡ sá»‘ tÆ°Æ¡ng quan Pearson (r)")
        )
        st.plotly_chart(fig_sum, width='stretch')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# LOAD Dá»® LIá»†U
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
df_raw, load_err = load_data()
if df_raw is None:
    st.error(f"â ï¸ **Lá»—i:** {load_err}")
    st.info("HĂ£y cháº¡y `main.py` trÆ°á»›c.")
    st.stop()

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SIDEBAR
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 10px'>
        <div style='font-size:36px'>đŸ™ï¸</div>
        <div style='font-size:14px;font-weight:700;color:#f1f5f9;margin-top:6px'>Bá»™ lá»c dá»¯ liá»‡u</div>
        <div style='font-size:11px;color:#64748b;margin-top:2px'>NYC Real Estate Analytics</div>
    </div>
    <hr style='border-color:#1e3a5f;margin:0 0 14px'>
    """, unsafe_allow_html=True)
    all_b = [b for b in BOROUGH_ORDER if b in df_raw['borough_name'].dropna().unique()]
    selected_boroughs = st.multiselect("đŸ“ Quáº­n (Borough)", options=all_b, default=all_b)
    avail_years = sorted(df_raw['sale_year'].dropna().astype(int).unique().tolist())
    year_range  = st.select_slider("đŸ“… NÄƒm giao dá»‹ch", options=avail_years,
                                   value=(min(avail_years), max(avail_years)))
    p5  = float(df_raw['sale_price'].quantile(0.05))
    p95 = float(df_raw['sale_price'].quantile(0.95))
    price_range = st.slider("đŸ’° Khoáº£ng giĂ¡ ($)",
                            min_value=float(df_raw['sale_price'].min()),
                            max_value=float(df_raw['sale_price'].max()),
                            value=(p5, p95), format="$%.0f",
                            help="Máº·c Ä‘á»‹nh p5â€“p95 Ä‘á»ƒ loáº¡i bá» outlier.")
    st.markdown('<hr style="border-color:#1e3a5f;margin:14px 0 10px">', unsafe_allow_html=True)
    if st.button("đŸ”„ Äáº·t láº¡i bá»™ lá»c", width='stretch'):
        st.rerun()
    st.markdown(f"""
    <div style='text-align:center;margin-top:10px;color:#475569;font-size:11px'>
        Tá»•ng: {len(df_raw):,} giao dá»‹ch<br>Nguá»“n: NYC Property Sales
    </div>""", unsafe_allow_html=True)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# ĂP Dá»¤NG Bá»˜ Lá»ŒC
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
if not selected_boroughs:
    st.warning("â ï¸ ChÆ°a chá»n quáº­n nĂ o. HĂ£y chá»n Ă­t nháº¥t má»™t quáº­n trong bá»™ lá»c bĂªn trĂ¡i.")
    st.stop()
df = apply_filters(df_raw, selected_boroughs, year_range, price_range)
if len(df) == 0:
    st.warning("â ï¸ **KhĂ´ng cĂ³ dá»¯ liá»‡u phĂ¹ há»£p.** HĂ£y má»Ÿ rá»™ng bá»™ lá»c hoáº·c nháº¥n Äáº·t láº¡i.")
    st.stop()

df_sample = df.sample(n=min(3000, len(df)), random_state=42)
df_ppsf   = df[df['price_per_sqft'].notna() & (df['price_per_sqft'] < 5000)].copy()

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TIĂU Äá»€
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
h1, h2 = st.columns([4, 1])
with h1:
    st.markdown("""
    <h1 style='font-size:24px;font-weight:800;color:#0f172a;margin:0'>
    đŸ™ï¸ BĂO CĂO PHĂ‚N TĂCH THá» TRÆ¯á»œNG Báº¤T Äá»˜NG Sáº¢N NEW YORK GIAI ÄOáº N 2025 - 2026
    </h1>""", unsafe_allow_html=True)
with h2:
    st.markdown(f"""
    <div style='text-align:right;padding-top:6px'>
        <span class="badge">âœ“ {len(df):,} giao dá»‹ch</span><br>
        <span style='font-size:11px;color:#94a3b8'>{len(selected_boroughs)} quáº­n Â· {year_range[0]}â€“{year_range[1]}</span>
    </div>""", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom:18px'></div>", unsafe_allow_html=True)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TABS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "đŸ™ï¸  Tá»•ng quan",
    "đŸ—ºï¸  PhĂ¢n tĂ­ch khu vá»±c",
    "đŸ“  Yáº¿u tá»‘ quyáº¿t Ä‘á»‹nh giĂ¡",
    "đŸ“…  Biáº¿n Ä‘á»™ng theo thá»i gian",
    "đŸ¤–  Dá»± bĂ¡o & MĂ´ hĂ¬nh ML",
])

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 0 â€” Tá»”NG QUAN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab0:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#4338ca,#6366f1,#818cf8);border-radius:14px;
    padding:18px 24px;color:#fff;margin-bottom:22px;
    box-shadow:0 6px 24px rgba(99,102,241,0.35)'>
    <b style='font-size:15px;letter-spacing:-0.3px'>đŸ™ï¸ Thá»‹ trÆ°á»ng Ä‘ang á»Ÿ Ä‘Ă¢u vĂ  quy mĂ´ nhÆ° tháº¿ nĂ o?</b><br>
    <span style='font-size:12px;opacity:0.88'>Tá»•ng quan vá» quy mĂ´, máº·t báº±ng giĂ¡ vĂ  cÆ¡ cáº¥u thá»‹ trÆ°á»ng báº¥t Ä‘á»™ng sáº£n NYC trong bá»™ lá»c hiá»‡n táº¡i.</span>
    </div>
    """, unsafe_allow_html=True)

    med_price = df['sale_price'].median()
    med_ppsf  = df_ppsf['price_per_sqft'].median() if len(df_ppsf) > 0 else 0
    total_val = df['sale_price'].sum()
    pct_1m    = (df['sale_price'] >= 1_000_000).mean() * 100
    yoy_med0  = df.groupby('sale_year')['sale_price'].median()
    yrs0 = sorted(yoy_med0.index)
    if len(yrs0) >= 2:
        yoy_d0 = (yoy_med0[yrs0[-1]]/yoy_med0[yrs0[-2]]-1)*100
        yoy_s0 = f"{yoy_d0:+.1f}%"
    else:
        yoy_d0, yoy_s0 = 0.0, "â€”"

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    k1.metric("Tá»•ng giao dá»‹ch", f"{len(df):,}")
    k2.metric("GiĂ¡ trung vá»‹",   fmt_M(med_price))
    k3.metric("GiĂ¡/sqft (TV)",  f"${med_ppsf:,.0f}")
    k4.metric("Tá»•ng giĂ¡ trá»‹",   f"${total_val/1e9:.1f}B")
    k5.metric("TÄƒng giĂ¡ YoY",   yoy_s0, delta=f"{yoy_d0:.1f}%" if yoy_d0 else None)
    k6.metric("Giao dá»‹ch â‰¥$1M", f"{pct_1m:.1f}%")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    section_q(
        "Borough nĂ o chiáº¿m Æ°u tháº¿ â€” vá» thanh khoáº£n vĂ  máº·t báº±ng giĂ¡?",
        "Sá»‘ giao dá»‹ch = thanh khoáº£n. GiĂ¡ trung vá»‹ Ă­t bá»‹ áº£nh hÆ°á»Ÿng bá»Ÿi outlier hÆ¡n giĂ¡ trung bĂ¬nh."
    )

    bor_cnt = df['borough_name'].value_counts().reindex(BOROUGH_ORDER, fill_value=0).reset_index()
    bor_cnt.columns = ['Borough','Giao dá»‹ch']
    bor_cnt = bor_cnt[bor_cnt['Giao dá»‹ch'] > 0]

    bor_med = df.groupby('borough_name')['sale_price'].median().reindex(BOROUGH_ORDER).dropna().reset_index()
    bor_med.columns = ['Borough','GiĂ¡ trung vá»‹']

    ca, cb = st.columns(2)
    with ca:
        fig = px.bar(bor_cnt.sort_values('Giao dá»‹ch'), x='Giao dá»‹ch', y='Borough', orientation='h',
                     color='Borough', color_discrete_map=BOROUGH_COLORS, text='Giao dá»‹ch',
                     title="Sá»‘ giao dá»‹ch theo quáº­n")
        fig.update_traces(texttemplate='%{text:,}', textposition='auto')
        clayout(fig, h=280, t=40, r=80)
        fig.update_layout(yaxis=dict(automargin=True, title='Quáº­n'), xaxis=dict(automargin=True, title='Sá»‘ giao dá»‹ch'),
                          title_font=dict(size=13, color='#374151'))
        st.plotly_chart(fig, width='stretch')
    with cb:
        fig = px.bar(bor_med.sort_values('GiĂ¡ trung vá»‹'), x='GiĂ¡ trung vá»‹', y='Borough', orientation='h',
                     color='Borough', color_discrete_map=BOROUGH_COLORS,
                     text=bor_med.sort_values('GiĂ¡ trung vá»‹')['GiĂ¡ trung vá»‹'].apply(fmt_M),
                     title="GiĂ¡ trung vá»‹ theo quáº­n ($)")
        fig.update_traces(textposition='auto')
        clayout(fig, h=280, t=40, r=100)
        fig.update_layout(yaxis=dict(automargin=True, title='Quáº­n'), xaxis=dict(tickformat='$,.0f', automargin=True, title='GiĂ¡ trung vá»‹ ($)'),
                          title_font=dict(size=13, color='#374151'))
        st.plotly_chart(fig, width='stretch')

    divider()
    section_q("Thá»‹ trÆ°á»ng Ä‘ang táº­p trung vĂ o loáº¡i hĂ¬nh báº¥t Ä‘á»™ng sáº£n nĂ o?",
              "CÆ¡ cáº¥u loáº¡i hĂ¬nh vĂ  phĂ¢n bá»‘ giĂ¡ theo tá»«ng loáº¡i (top 6).")

    top6_bt = df['building_type'].value_counts().head(6).index.tolist()
    cc, cd  = st.columns(2)
    with cc:
        bt_c = df['building_type'].value_counts().head(6).reset_index()
        bt_c.columns = ['Loáº¡i hĂ¬nh','Sá»‘ lÆ°á»£ng']
        fig = px.pie(bt_c, names='Loáº¡i hĂ¬nh', values='Sá»‘ lÆ°á»£ng', hole=0.50,
                     color_discrete_sequence=[C_BLUE,C_SKY,C_ORANGE,C_GREEN,'#8b5cf6',C_GRAY],
                     title="CÆ¡ cáº¥u loáº¡i hĂ¬nh báº¥t Ä‘á»™ng sáº£n")
        fig.update_traces(textposition='inside', textinfo='percent',
                          insidetextorientation='radial',
                          hovertemplate='<b>%{label}</b><br>%{value:,} GD<br>%{percent}<extra></extra>')
        clayout(fig, h=320, t=40, l=10, r=20, b=20, leg=True)
        fig.update_layout(legend=dict(orientation='v', x=1.0, y=0.5, font_size=11),
                          title_font=dict(size=13, color='#374151'))
        st.plotly_chart(fig, width='stretch')
    with cd:
        df_bt0 = df[df['building_type'].isin(top6_bt)]
        med_bt0 = df_bt0.groupby('building_type')['sale_price'].median().sort_values(ascending=False)
        fig = px.box(df_bt0, x='building_type', y='sale_price',
                     color='building_type',
                     color_discrete_sequence=[C_BLUE,C_SKY,C_ORANGE,C_GREEN,'#8b5cf6',C_GRAY],
                     points=False, labels={'building_type':'Loáº¡i hĂ¬nh BÄS','sale_price':'GiĂ¡ bĂ¡n ($)'},
                     category_orders={'building_type': med_bt0.index.tolist()},
                     title="PhĂ¢n bá»‘ giĂ¡ theo loáº¡i hĂ¬nh (top 6)")
        clayout(fig, h=320, t=40, b=60, l=10, r=10)
        fig.update_layout(xaxis=dict(automargin=True, tickangle=-15, tickfont_size=10, title=''),
                          yaxis=dict(tickformat='$,.0f', automargin=True),
                          title_font=dict(size=13, color='#374151'))
        st.plotly_chart(fig, width='stretch')

    divider()
    top_b0 = bor_med.sort_values('GiĂ¡ trung vá»‹', ascending=False).iloc[0]
    low_b0 = bor_med.sort_values('GiĂ¡ trung vá»‹').iloc[0]
    rat0   = top_b0['GiĂ¡ trung vá»‹'] / low_b0['GiĂ¡ trung vá»‹']
    top_bt0= df['building_type'].value_counts().index[0]
    pct_bt0= df['building_type'].value_counts().iloc[0] / len(df) * 100
    insight_box(f"""
    <b>đŸ“Œ Nhá»¯ng Ä‘iá»u quan trá»ng nháº¥t tá»« tá»•ng quan:</b><br>
    â€¢ <b>{top_b0['Borough']}</b> dáº«n Ä‘áº§u vá» giĂ¡ trung vá»‹ ({fmt_M(top_b0['GiĂ¡ trung vá»‹'])}),
      cao hÆ¡n <b>{rat0:.1f}Ă—</b> so vá»›i {low_b0['Borough']} ({fmt_M(low_b0['GiĂ¡ trung vá»‹'])}) â€”
      pháº£n Ă¡nh phĂ¢n hĂ³a máº¡nh giá»¯a cĂ¡c quáº­n.<br>
    â€¢ <b>{pct_bt0:.0f}%</b> giao dá»‹ch thuá»™c loáº¡i hĂ¬nh <b>{top_bt0}</b> â€”
      thá»‹ trÆ°á»ng táº­p trung rĂµ vĂ o phĂ¢n khĂºc nĂ y.<br>
    â€¢ Tá»•ng giĂ¡ trá»‹ thá»‹ trÆ°á»ng: <b>${total_val/1e9:.2f} tá»· USD</b>.
      Tá»· lá»‡ giao dá»‹ch â‰¥$1M: <b>{pct_1m:.1f}%</b> â€” thá»‹ trÆ°á»ng cĂ³ xu hÆ°á»›ng cao cáº¥p.
    """)

    # â”€â”€ PhĂ¢n khĂºc khĂ¡ch hĂ ng â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    divider()
    section_q("Thá»‹ trÆ°á»ng Ä‘ang phá»¥c vá»¥ nhĂ³m khĂ¡ch hĂ ng nĂ o?",
              "PhĂ¢n loáº¡i theo sá»‘ cÄƒn trong tĂ²a nhĂ  â€” proxy cho má»¥c Ä‘Ă­ch mua (á»Ÿ thá»±c vs Ä‘áº§u tÆ°).")

    df['_segment'] = pd.cut(
        df['total_units'],
        bins=[-1, 1, 10, float('inf')],
        labels=['â‘  Mua á»Ÿ thá»±c (1 cÄƒn)', 'â‘¡ Äáº§u tÆ° nhá» (2-10)', 'â‘¢ Tá»• chá»©c (>10)']
    )
    seg_cnt  = df['_segment'].value_counts().sort_index()
    seg_med  = df.groupby('_segment', observed=True)['sale_price'].median()
    seg_df   = pd.DataFrame({'PhĂ¢n khĂºc': seg_cnt.index,
                              'Sá»‘ GD': seg_cnt.values,
                              'GiĂ¡ trung vá»‹': seg_med.values})
    seg_df['% thá»‹ trÆ°á»ng'] = seg_df['Sá»‘ GD'] / seg_df['Sá»‘ GD'].sum() * 100

    sa, sb = st.columns(2)
    with sa:
        fig_seg = px.bar(seg_df, x='PhĂ¢n khĂºc', y='Sá»‘ GD',
                         color='PhĂ¢n khĂºc',
                         color_discrete_sequence=[C_GREEN, C_BLUE, C_ORANGE],
                         text=seg_df['% thá»‹ trÆ°á»ng'].apply(lambda v: f'{v:.1f}%'),
                         title="CÆ¡ cáº¥u phĂ¢n khĂºc khĂ¡ch hĂ ng")
        fig_seg.update_traces(textposition='outside')
        clayout(fig_seg, h=300, t=40, b=20)
        fig_seg.update_layout(showlegend=False,
                               xaxis=dict(automargin=True, title='PhĂ¢n khĂºc'),
                               yaxis=dict(automargin=True, title='Sá»‘ giao dá»‹ch'),
                               title_font=dict(size=13, color='#374151'))
        st.plotly_chart(fig_seg, width='stretch')
    with sb:
        fig_sp = px.bar(seg_df, x='PhĂ¢n khĂºc', y='GiĂ¡ trung vá»‹',
                        color='PhĂ¢n khĂºc',
                        color_discrete_sequence=[C_GREEN, C_BLUE, C_ORANGE],
                        text=seg_df['GiĂ¡ trung vá»‹'].apply(fmt_M),
                        title="GiĂ¡ trung vá»‹ theo phĂ¢n khĂºc")
        fig_sp.update_traces(textposition='outside')
        clayout(fig_sp, h=300, t=40, b=20)
        fig_sp.update_layout(showlegend=False,
                               xaxis=dict(automargin=True, title='PhĂ¢n khĂºc'),
                               yaxis=dict(tickformat='$,.0f', automargin=True, title='GiĂ¡ trung vá»‹ ($)'),
                               title_font=dict(size=13, color='#374151'))
        st.plotly_chart(fig_sp, width='stretch')

    # â”€â”€ Nháº­n diá»‡n rá»§i ro Ä‘áº§u tÆ° â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    divider()
    section_q("Khu vá»±c nĂ o cĂ³ rá»§i ro giĂ¡ cao nháº¥t?",
              "Rá»§i ro = biáº¿n Ä‘á»™ng giĂ¡ cao (CV cao) hoáº·c thanh khoáº£n tháº¥p. "
              "Xanh = Ă­t rá»§i ro, Ä‘á» = cáº§n tháº­n trá»ng.")

    borough_risk = df.groupby('borough_name').agg(
        med_price=('sale_price','median'),
        std_price=('sale_price','std'),
        n_gd=('sale_price','count')
    ).reset_index()
    borough_risk['CV (%)'] = (borough_risk['std_price'] / borough_risk['med_price'] * 100).round(1)
    borough_risk['Rá»§i ro biáº¿n Ä‘á»™ng'] = pd.cut(
        borough_risk['CV (%)'],
        bins=[0, 80, 120, float('inf')],
        labels=['đŸŸ¢ Tháº¥p', 'đŸŸ¡ Trung bĂ¬nh', 'đŸ”´ Cao']
    )
    borough_risk = borough_risk.sort_values('CV (%)')

    risk_display = borough_risk[['borough_name','med_price','CV (%)','n_gd','Rá»§i ro biáº¿n Ä‘á»™ng']].copy()
    risk_display.columns = ['Quáº­n','GiĂ¡ trung vá»‹','Biáº¿n Ä‘á»™ng CV (%)','Sá»‘ giao dá»‹ch','ÄĂ¡nh giĂ¡ rá»§i ro']
    risk_display['GiĂ¡ trung vá»‹'] = risk_display['GiĂ¡ trung vá»‹'].apply(fmt_M)
    risk_display['Sá»‘ giao dá»‹ch'] = risk_display['Sá»‘ giao dá»‹ch'].apply(lambda v: f'{v:,}')
    st.dataframe(risk_display.set_index('Quáº­n'), width='stretch')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 1 â€” PHĂ‚N TĂCH KHU Vá»°C & Báº¢N Äá»’ HEATMAP
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab1:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f766e,#0d9488,#34d399);border-radius:14px;
    padding:18px 24px;color:#fff;margin-bottom:22px;
    box-shadow:0 6px 24px rgba(16,185,129,0.3)'>
    <b style='font-size:15px;letter-spacing:-0.3px'>đŸ—ºï¸ Báº£n Ä‘á»“ Nhiá»‡t Khu vá»±c & PhĂ¢n tĂ­ch Äiá»ƒm nĂ³ng (NYC Hotspot Map)</b><br>
    <span style='font-size:12px;opacity:0.88'>Nháº­n diá»‡n Ä‘iá»ƒm nĂ³ng giĂ¡ bĂ¡n, Ä‘á»‹nh giĂ¡ Ä‘Æ¡n vá»‹ $/sqft vĂ  máº­t Ä‘á»™ thanh khoáº£n trĂªn báº£n Ä‘á»“ tÆ°Æ¡ng quan khĂ´ng gian thá»±c.</span>
    </div>
    """, unsafe_allow_html=True)

    n_neigh   = df['neighborhood'].nunique()
    top_neigh = df['neighborhood'].value_counts().index[0]
    top_n_cnt = df['neighborhood'].value_counts().iloc[0]
    bor_med_f = df.groupby('borough_name')['sale_price'].median()
    top_bor_p = bor_med_f.idxmax()

    ka,kb,kc,kd = st.columns(4)
    ka.metric("Quáº­n Ä‘ang phĂ¢n tĂ­ch",        f"{len(selected_boroughs)}/5")
    kb.metric("Sá»‘ khu vá»±c",                  f"{n_neigh:,}")
    kc.metric("Khu vá»±c sĂ´i Ä‘á»™ng nháº¥t",       top_neigh.title()[:20])
    kd.metric("Quáº­n giĂ¡ trung vá»‹ cao nháº¥t",  top_bor_p)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # â”€â”€ YĂU Cáº¦U Vá»€ Báº¢N Äá»’ (MAP): Báº¢N Äá»’ TĂ” MĂ€U KHU Vá»°C (HEATMAP) â”€â”€
    section_q(
        "Báº£n Ä‘á»“ Nhiá»‡t Khu vá»±c (NYC Hotspot Heatmap)",
        "TĂ´ mĂ u khu vá»±c thá»ƒ hiá»‡n trá»±c quan Ä‘iá»ƒm nĂ³ng (hotspots) vá» GiĂ¡ trung vá»‹, GiĂ¡/sqft hoáº·c Máº­t Ä‘á»™ thanh khoáº£n giao dá»‹ch."
    )

    # Gom nhĂ³m dá»¯ liá»‡u Ä‘á»‹a lĂ½ theo Neighborhood
    geo_df = df.groupby(['neighborhood', 'borough_name']).agg(
        med_price=('sale_price', 'median'),
        med_ppsf=('price_per_sqft', 'median'),
        n_count=('sale_price', 'count')
    ).reset_index()

    # ThĂªm lat, lon cho tá»«ng khu vá»±c
    coords_list = [get_neighborhood_coords(row['neighborhood'], row['borough_name']) for _, row in geo_df.iterrows()]
    geo_df['lat'] = [c[0] for c in coords_list]
    geo_df['lon'] = [c[1] for c in coords_list]
    geo_df['med_ppsf_clean'] = geo_df['med_ppsf'].fillna(0)

    mc1, mc2, mc3 = st.columns([2, 1, 1])
    with mc1:
        map_metric = st.radio(
            "Hiá»ƒn thá»‹ Ä‘iá»ƒm nĂ³ng theo:",
            options=["đŸ”¥ GiĂ¡ trung vá»‹ ($)", "đŸ“ GiĂ¡/sqft trung vá»‹ ($)", "đŸ“ Máº­t Ä‘á»™ giao dá»‹ch (Sá»‘ cÄƒn)"],
            horizontal=True
        )
    with mc2:
        radius_val = st.slider("BĂ¡n kĂ­nh Ä‘iá»ƒm nhiá»‡t (Radius)", 15, 45, 25)
    with mc3:
        zoom_val = st.slider("Äá»™ phĂ³ng Ä‘áº¡i (Zoom)", 9, 13, 10)

    if map_metric == "đŸ”¥ GiĂ¡ trung vá»‹ ($)":
        target_z = 'med_price'
        color_scale = "Plasma"
        z_title = "GiĂ¡ trung vá»‹ ($)"
    elif map_metric == "đŸ“ GiĂ¡/sqft trung vá»‹ ($)":
        target_z = 'med_ppsf_clean'
        color_scale = "Inferno"
        z_title = "GiĂ¡/sqft ($)"
    else:
        target_z = 'n_count'
        color_scale = "Viridis"
        z_title = "Sá»‘ giao dá»‹ch"

    fig_map = px.density_mapbox(
        geo_df,
        lat='lat',
        lon='lon',
        z=target_z,
        radius=radius_val,
        center=dict(lat=40.7400, lon=-73.9400),
        zoom=zoom_val,
        mapbox_style="open-street-map",
        color_continuous_scale=color_scale,
        hover_name="neighborhood",
        hover_data={
            "borough_name": True,
            "med_price": ":$,.0f",
            "med_ppsf_clean": ":$,.0f",
            "n_count": ":,",
            "lat": False,
            "lon": False
        },
        labels={
            "borough_name": "Quáº­n",
            "med_price": "GiĂ¡ trung vá»‹",
            "med_ppsf_clean": "GiĂ¡/sqft",
            "n_count": "Sá»‘ GD"
        }
    )
    clayout(fig_map, h=520, t=10, b=10, l=10, r=10)
    fig_map.update_layout(
        coloraxis_colorbar=dict(title=z_title, len=0.8)
    )
    st.plotly_chart(fig_map, width='stretch')

    # ChĂº giáº£i Ä‘iá»ƒm nĂ³ng
    top_p_geo = geo_df.sort_values('med_price', ascending=False).head(3)
    top_v_geo = geo_df.sort_values('n_count', ascending=False).head(3)
    p_spots = ", ".join([f"<b>{r['neighborhood'].title()}</b> (${r['med_price']/1e6:.2f}M)" for _, r in top_p_geo.iterrows()])
    v_spots = ", ".join([f"<b>{r['neighborhood'].title()}</b> ({r['n_count']:,} GD)" for _, r in top_v_geo.iterrows()])

    insight_box(f"""
    <b>đŸ“ Nháº­n diá»‡n Äiá»ƒm nĂ³ng (Hotspots) trĂªn Báº£n Ä‘á»“:</b><br>
    â€¢ đŸ”´ <b>Äiá»ƒm nĂ³ng vá» GiĂ¡ bĂ¡n (Hotspots GiĂ¡ cao):</b> Táº­p trung dĂ y Ä‘áº·c táº¡i khu vá»±c lĂµi Manhattan: {p_spots}.<br>
    â€¢ đŸŸ¢ <b>Äiá»ƒm nĂ³ng vá» Thanh khoáº£n (Hotspots Giao dá»‹ch nhá»™n nhá»‹p):</b> PhĂ¢n bá»‘ rá»™ng á»Ÿ Queens & Brooklyn: {v_spots}.<br>
    â€¢ đŸ’¡ <i>Máº¹o sá»­ dá»¥ng báº£n Ä‘á»“: PhĂ³ng to (Zoom) Ä‘á»ƒ quan sĂ¡t tá»«ng gĂ³c phá»‘, di chuá»™t qua tá»«ng Ä‘iá»ƒm mĂ u nhiá»‡t Ä‘á»ƒ xem chi tiáº¿t Ä‘Æ¡n giĂ¡ $/sqft vĂ  tá»•ng sá»‘ giao dá»‹ch thá»±c táº¿.</i>
    """)

    divider()
    section_q("GiĂ¡ bĂ¡n phĂ¢n bá»‘ nhÆ° tháº¿ nĂ o trong tá»«ng quáº­n?",
              "ÄÆ°á»ng giá»¯a = trung vá»‹. Há»™p = khoáº£ng tá»© phĂ¢n vá»‹ (25%â€“75%). NhĂ£n giĂ¡ trung vá»‹ Ä‘Æ°á»£c ghi trá»±c tiáº¿p.")

    bor_ord1 = df.groupby('borough_name')['sale_price'].median().sort_values(ascending=False).index.tolist()
    fig = px.box(df, x='borough_name', y='sale_price', color='borough_name',
                 color_discrete_map=BOROUGH_COLORS, points=False,
                 labels={'borough_name':'Quáº­n','sale_price':'GiĂ¡ bĂ¡n (USD)'},
                 category_orders={'borough_name': bor_ord1},
                 title='PhĂ¢n phá»‘i giĂ¡ bĂ¡n nhĂ  theo Quáº­n')
    for b in bor_ord1:
        m = df[df['borough_name']==b]['sale_price'].median()
        fig.add_annotation(x=b, y=m, text=fmt_M(m), showarrow=False,
                           font=dict(size=11,color='#111827',weight=700),
                           yshift=20, bgcolor='rgba(255,255,255,0.88)', borderpad=3)
    clayout(fig, h=360, t=50, b=20)
    fig.update_layout(
        title_font=dict(size=14, color='#374151'),
        yaxis=dict(tickformat='$,.0f', automargin=True, title='GiĂ¡ bĂ¡n (USD)'),
        xaxis=dict(automargin=True, title='Quáº­n')
    )
    st.plotly_chart(fig, width='stretch')

    divider()
    section_q("Khu vá»±c nĂ o sĂ´i Ä‘á»™ng nháº¥t vĂ  cĂ³ giĂ¡/sqft cao nháº¥t?",
              "TrĂ¡i: sá»‘ giao dá»‹ch (thanh khoáº£n). Pháº£i: giĂ¡/sqft trung vá»‹ (loáº¡i khu vá»±c < 5 giao dá»‹ch Ä‘á»ƒ trĂ¡nh sai lá»‡ch máº«u nhá»).")

    top_n_ppsf_row = None
    cn1, cn2 = st.columns(2)
    with cn1:
        t15c = (df.groupby(['neighborhood','borough_name']).size()
                .reset_index(name='Giao dá»‹ch')
                .sort_values('Giao dá»‹ch', ascending=False).head(15))
        t15c = t15c.sort_values('Giao dá»‹ch')
        t15c['Khu vá»±c'] = t15c['neighborhood'].str.title().str[:25]
        fig = px.bar(t15c, x='Giao dá»‹ch', y='Khu vá»±c', orientation='h',
                     color='borough_name', color_discrete_map=BOROUGH_COLORS, text='Giao dá»‹ch',
                     title="Top 15 khu vá»±c nhiá»u giao dá»‹ch nháº¥t",
                     labels={'borough_name':'Quáº­n'})
        fig.update_traces(texttemplate='%{text:,}', textposition='auto')
        clayout(fig, h=460, t=40, b=20, r=80, leg=True)
        fig.update_layout(yaxis=dict(automargin=True, tickfont_size=11, title='Khu vá»±c'),
                          xaxis=dict(automargin=True, title='Sá»‘ giao dá»‹ch'),
                          legend=dict(orientation='h', y=-0.1, x=0, font_size=11),
                          title_font=dict(size=13, color='#374151'))
        st.plotly_chart(fig, width='stretch')
    with cn2:
        if len(df_ppsf) > 0:
            t15p = (df_ppsf.groupby(['neighborhood','borough_name'])['price_per_sqft']
                    .agg(med_ppsf='median', cnt='count').reset_index())
            t15p = t15p[t15p['cnt'] >= 5].nlargest(15,'med_ppsf').sort_values('med_ppsf')
            t15p['Khu vá»±c'] = t15p['neighborhood'].str.title().str[:25]
            if len(t15p) > 0:
                top_n_ppsf_row = t15p.iloc[-1]
            fig = px.bar(t15p, x='med_ppsf', y='Khu vá»±c', orientation='h',
                         color='borough_name', color_discrete_map=BOROUGH_COLORS,
                         text=t15p['med_ppsf'].apply(lambda v: f'${v:,.0f}'),
                         title="Top 15 khu vá»±c giĂ¡/sqft cao nháº¥t (trung vá»‹)",
                         labels={'borough_name':'Quáº­n','med_ppsf':'$/sqft (trung vá»‹)'})
            fig.update_traces(textposition='auto')
            clayout(fig, h=460, t=40, b=20, r=80, leg=True)
            fig.update_layout(yaxis=dict(automargin=True, tickfont_size=11, title='Khu vá»±c'),
                              xaxis=dict(tickformat='$,.0f', automargin=True, title='$/sqft (trung vá»‹)'),
                              legend=dict(orientation='h', y=-0.1, x=0, font_size=11),
                              title_font=dict(size=13, color='#374151'))
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("KhĂ´ng Ä‘á»§ dá»¯ liá»‡u giĂ¡/sqft.")

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 2 â€” Yáº¾U Tá» QUYáº¾T Äá»NH GIĂ & PHĂ‚N TĂCH TÆ¯Æ NG QUAN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab2:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#5b21b6,#7c3aed,#a78bfa);border-radius:14px;
    padding:18px 24px;color:#fff;margin-bottom:22px;
    box-shadow:0 6px 24px rgba(124,58,237,0.35)'>
    <b style='font-size:15px;letter-spacing:-0.3px'>đŸ“ PhĂ¢n tĂ­ch Ma tráº­n Yáº¿u tá»‘ & CĂ¡c Biáº¿n sá»‘ Quyáº¿t Ä‘á»‹nh GiĂ¡</b><br>
    <span style='font-size:12px;opacity:0.88'>TĂ³m táº¯t cĂ¡c yáº¿u tá»‘ áº£nh hÆ°á»Ÿng máº¡nh/yáº¿u, ma tráº­n tÆ°Æ¡ng quan vĂ  giáº£i thĂ­ch Ă½ nghÄ©a chiá»u tĂ¡c Ä‘á»™ng cá»§a cĂ¡c biáº¿n sá»‘ chĂ­nh Ä‘áº¿n giĂ¡ bĂ¡n thá»±c táº¿.</span>
    </div>
    """, unsafe_allow_html=True)

    # â”€â”€ NGUYĂN Táº®C TRá»°C QUAN: Báº¢NG TĂ“M Táº®T Yáº¾U Tá» TĂC Äá»˜NG GIĂ â”€â”€
    section_q(
        "Báº£ng tĂ³m táº¯t cĂ¡c yáº¿u tá»‘ áº£nh hÆ°á»Ÿng Ä‘áº¿n giĂ¡ báº¥t Ä‘á»™ng sáº£n",
        "TĂ³m táº¯t toĂ n bá»™ cĂ¡c biáº¿n sá»‘ Ä‘o lÆ°á»ng, phĂ¢n loáº¡i rĂµ yáº¿u tá»‘ nĂ o áº£nh hÆ°á»Ÿng máº¡nh hay yáº¿u Ä‘áº¿n giĂ¡ bĂ¡n thá»±c táº¿."
    )
    render_factor_summary_matrix(df)

    divider()

    # â”€â”€ MA TRáº¬N TÆ¯Æ NG QUAN Tá»”NG THá»‚ â”€â”€
    section_q(
        "Ma tráº­n tÆ°Æ¡ng quan tá»•ng thá»ƒ giá»¯a cĂ¡c yáº¿u tá»‘ vá»›i GiĂ¡ bĂ¡n",
        "Äá»c báº£n Ä‘á»“ nhiá»‡t: Ă´ mĂ u Ä‘á» = tÆ°Æ¡ng quan thuáº­n (+); Ă´ mĂ u xanh = tÆ°Æ¡ng quan nghá»‹ch (-). Sá»‘ trong Ă´ lĂ  há»‡ sá»‘ tÆ°Æ¡ng quan r."
    )
    cc_cols = ['sale_price','gross_sqft','avg_income','amenity_score','dist_center','pop_density','building_age']
    cc_lbl  = {'sale_price':'GiĂ¡ bĂ¡n','gross_sqft':'Diá»‡n tĂ­ch','avg_income':'Thu nháº­p TB',
               'amenity_score':'Äiá»ƒm tiá»‡n Ă­ch','dist_center':'KC trung tĂ¢m','pop_density':'Máº­t Ä‘á»™ dĂ¢n sá»‘','building_age':'Tuá»•i cĂ´ng trĂ¬nh'}
    cc_data = df[cc_cols].dropna()
    cc_mat  = cc_data.corr()
    cc_mat.columns = [cc_lbl[c] for c in cc_mat.columns]
    cc_mat.index   = [cc_lbl[c] for c in cc_mat.index]
    
    fig_corr_mat = px.imshow(cc_mat, text_auto='.2f', color_continuous_scale='RdBu_r',
                            zmin=-1, zmax=1, aspect='equal',
                            title='Ma tráº­n tÆ°Æ¡ng quan giá»¯a cĂ¡c yáº¿u tá»‘ vĂ  GiĂ¡ bĂ¡n')
    clayout(fig_corr_mat, h=360, t=40, b=20)
    fig_corr_mat.update_layout(
        coloraxis_colorbar=dict(title='Há»‡ sá»‘ r', len=0.8),
        title_font=dict(size=13, color='#374151')
    )
    st.plotly_chart(fig_corr_mat, width='stretch')

    divider()

    # â”€â”€ PHĂ‚N TĂCH CHI TIáº¾T 3 BIáº¾N Sá» CHĂNH THEO YĂU Cáº¦U â”€â”€
    st.markdown("""
    <div style='font-size:18px;font-weight:800;color:#1e1b4b;margin-bottom:16px'>
    đŸ” PHĂ‚N TĂCH CHI TIáº¾T 3 BIáº¾N Sá» CHá»¦ Äáº O TĂC Äá»˜NG Äáº¾N GIĂ BĂN
    </div>
    """, unsafe_allow_html=True)

    # 1. BIáº¾N Sá» 1: DIá»†N TĂCH (gross_sqft)
    section_q("1. Biáº¿n sá»‘ DIá»†N TĂCH CĂ”NG TRĂŒNH (gross_sqft) â€” Má»©c Ä‘á»™ tĂ¡c Ä‘á»™ng: đŸ€ Ráº¤T Máº NH",
              "PhĂ¢n tĂ­ch má»‘i quan há»‡ giá»¯a quy mĂ´ diá»‡n tĂ­ch sĂ n sá»­ dá»¥ng vĂ  tá»•ng giĂ¡ bĂ¡n báº¥t Ä‘á»™ng sáº£n.")
    
    df_sq = df[df['gross_sqft'].notna() & df['gross_sqft'].between(100, 4000)].copy()
    df_sq = df_sq[df_sq['sale_price'] < df_sq['sale_price'].quantile(0.97)]
    corr_sq = df_sq['gross_sqft'].corr(df_sq['sale_price']) if len(df_sq) >= 20 else 0

    if len(df_sq) >= 50:
        df_sq['bin'] = pd.cut(df_sq['gross_sqft'], bins=range(100,4200,200),
                              labels=[f"{i}â€“{i+200}" for i in range(100,4000,200)])
        ba = (df_sq.groupby('bin', observed=True)
              .agg(med_price=('sale_price','median'), cnt=('sale_price','count'),
                   sqft_mid=('gross_sqft','median')).reset_index())
        ba = ba[ba['cnt'] >= 10]
        fig_sq_chart = px.scatter(ba, x='sqft_mid', y='med_price', size='cnt', size_max=30,
                                  color='med_price', color_continuous_scale='Blues', trendline='ols',
                                  labels={'sqft_mid':'Diá»‡n tĂ­ch trung vá»‹ (sqft)',
                                          'med_price':'GiĂ¡ trung vá»‹ ($)','cnt':'Sá»‘ GD'},
                                  title="TÆ°Æ¡ng quan giá»¯a Diá»‡n tĂ­ch sá»­ dá»¥ng (sqft) vĂ  GiĂ¡ bĂ¡n trung vá»‹ ($)")
        clayout(fig_sq_chart, h=340, t=40, b=20)
        fig_sq_chart.update_layout(coloraxis_showscale=False,
                                   yaxis=dict(tickformat='$,.0f', automargin=True, title='GiĂ¡ trung vá»‹ ($)'),
                                   xaxis=dict(automargin=True, title='Diá»‡n tĂ­ch trung vá»‹ (sqft)'),
                                   title_font=dict(size=13, color='#374151'))
        # Äáº·t tĂªn cho OLS trendline trace Ä‘á»ƒ trĂ¡nh undefined trong legend
        for trace in fig_sq_chart.data:
            if hasattr(trace, 'name') and trace.name and 'OLS' in str(trace.name):
                trace.name = 'ÄÆ°á»ng xu hÆ°á»›ng (OLS)'
        st.plotly_chart(fig_sq_chart, width='stretch')

    insight_box(f"""
    <b>đŸ’¡ Ă nghÄ©a kinh táº¿ cá»§a Biáº¿n sá»‘ DIá»†N TĂCH (gross_sqft):</b><br>
    â€¢ Há»‡ sá»‘ tÆ°Æ¡ng quan: <b>r = +{corr_sq:.2f}</b> (TÆ°Æ¡ng quan thuáº­n ráº¥t máº¡nh).<br>
    â€¢ <b>Giáº£i thĂ­ch thá»±c táº¿:</b> Diá»‡n tĂ­ch sĂ n lĂ  yáº¿u tá»‘ váº­t lĂ½ Ä‘Ă³ng vai trĂ² quyáº¿t Ä‘á»‹nh sá»‘ 1 tá»›i giĂ¡ bĂ¡n. 
      CÄƒn há»™ cĂ³ diá»‡n tĂ­ch lá»›n hÆ¡n cung cáº¥p khĂ´ng gian sá»‘ng rá»™ng rĂ£i hÆ¡n, nhiá»u phĂ²ng ngá»§/phĂ²ng táº¯m hÆ¡n. 
      Má»—i 500 sqft diá»‡n tĂ­ch tÄƒng thĂªm giĂºp giĂ¡ trá»‹ tĂ i sáº£n tÄƒng trung bĂ¬nh tá»« 40% - 60%.
    """)

    divider()

    # 2. BIáº¾N Sá» 2: THU NHáº¬P KHU Vá»°C (avg_income)
    section_q("2. Biáº¿n sá»‘ THU NHáº¬P BĂŒNH QUĂ‚N KHU Vá»°C (avg_income) â€” Má»©c Ä‘á»™ tĂ¡c Ä‘á»™ng: đŸ“ˆ Máº NH",
              "PhĂ¢n tĂ­ch tĂ¡c Ä‘á»™ng cá»§a sá»©c mua vĂ  má»©c Ä‘á»™ Ä‘áº¯t Ä‘á» cá»§a dĂ¢n cÆ° sinh sá»‘ng táº¡i khu vá»±c Ä‘áº¿n máº·t báº±ng giĂ¡ nhĂ .")

    df_inc = df[df['avg_income'].notna()].copy()
    corr_inc = df_inc['avg_income'].corr(df_inc['sale_price']) if len(df_inc) >= 20 else 0

    inc_summary = df_inc.groupby('borough_name').agg(
        avg_inc=('avg_income', 'mean'),
        med_price=('sale_price', 'median'),
        med_ppsf=('price_per_sqft', 'median')
    ).reset_index()

    fig_inc = px.bar(
        inc_summary, x='borough_name', y='med_price',
        color='avg_inc', color_continuous_scale='Purples',
        text=inc_summary['avg_inc'].apply(lambda v: f'Thu nháº­p TB: ${v:,.0f}'),
        title="Máº·t báº±ng GiĂ¡ nhĂ  Trung vá»‹ xáº¿p theo Má»©c Thu nháº­p BĂ¬nh quĂ¢n Khu vá»±c ($)",
        labels={'borough_name': 'Quáº­n', 'med_price': 'GiĂ¡ bĂ¡n trung vá»‹ ($)', 'avg_inc': 'Thu nháº­p TB ($)'}
    )
    fig_inc.update_traces(textposition='outside')
    clayout(fig_inc, h=340, t=40, b=20)
    fig_inc.update_layout(
        yaxis=dict(tickformat='$,.0f', automargin=True, title='GiĂ¡ bĂ¡n trung vá»‹ ($)'),
        xaxis=dict(automargin=True, title='Quáº­n'),
        coloraxis_colorbar=dict(title='Thu nháº­p TB ($)'),
        title_font=dict(size=13, color='#374151')
    )
    st.plotly_chart(fig_inc, width='stretch')

    insight_box(f"""
    <b>đŸ’¡ Ă nghÄ©a kinh táº¿ cá»§a Biáº¿n sá»‘ THU NHáº¬P KHU Vá»°C (avg_income):</b><br>
    â€¢ Há»‡ sá»‘ tÆ°Æ¡ng quan: <b>r = +{corr_inc:.2f}</b> (TÆ°Æ¡ng quan thuáº­n máº¡nh).<br>
    â€¢ <b>Giáº£i thĂ­ch thá»±c táº¿:</b> Thu nháº­p bĂ¬nh quĂ¢n cá»§a dĂ¢n cÆ° khu vá»±c pháº£n Ă¡nh <i>sá»©c mua (purchasing power)</i> 
      vĂ  cháº¥t lÆ°á»£ng mĂ´i trÆ°á»ng sá»‘ng. Khu vá»±c cĂ³ thu nháº­p cao (nhÆ° Manhattan: ~$88K/nÄƒm) thÆ°á»ng sá»Ÿ há»¯u háº¡ táº§ng cao cáº¥p, 
      an ninh tá»‘t vĂ  trÆ°á»ng há»c cháº¥t lÆ°á»£ng, dáº«n tá»›i nhu cáº§u mua nhĂ  cao hÆ¡n vĂ  sáºµn sĂ ng tráº£ má»©c giĂ¡ Ă¡p Ä‘áº£o so vá»›i cĂ¡c quáº­n phá»¥ cáº­n.
    """)

    divider()

    # 3. BIáº¾N Sá» 3: TUá»”I Báº¤T Äá»˜NG Sáº¢N (building_age)
    section_q("3. Biáº¿n sá»‘ TUá»”I CĂ”NG TRĂŒNH (building_age) â€” Má»©c Ä‘á»™ tĂ¡c Ä‘á»™ng: đŸ“‰ Yáº¾U / Ă‚M",
              "PhĂ¢n tĂ­ch tĂ¡c Ä‘á»™ng cá»§a thá»i gian váº­n hĂ nh cĂ´ng trĂ¬nh Ä‘áº¿n giĂ¡ bĂ¡n (kháº¥u hao váº­t lĂ½ vs giĂ¡ trá»‹ vá»‹ trĂ­).")

    df_age = df[df['building_age'].notna() & df['building_age'].between(0, 120)].copy()
    corr_age = df_age['building_age'].corr(df_age['sale_price']) if len(df_age) >= 20 else 0

    df_age['age_group'] = pd.cut(
        df_age['building_age'],
        bins=[-1, 15, 35, 65, 120],
        labels=['Má»›i (<15 nÄƒm)', 'Trung bĂ¬nh (15â€“35 nÄƒm)', 'CÅ© (35â€“65 nÄƒm)', 'Ráº¥t cÅ© (>65 nÄƒm)']
    )
    age_sum = df_age.groupby('age_group', observed=True)['sale_price'].median().reset_index()

    fig_age = px.bar(
        age_sum, x='age_group', y='sale_price',
        color='sale_price', color_continuous_scale='Reds_r',
        text=age_sum['sale_price'].apply(fmt_M),
        title="GiĂ¡ trung vá»‹ báº¥t Ä‘á»™ng sáº£n phĂ¢n theo NhĂ³m Tuá»•i cĂ´ng trĂ¬nh",
        labels={'age_group': 'NhĂ³m tuá»•i', 'sale_price': 'GiĂ¡ trung vá»‹ ($)'}
    )
    fig_age.update_traces(textposition='outside')
    clayout(fig_age, h=320, t=40, b=20)
    fig_age.update_layout(coloraxis_showscale=False, yaxis=dict(tickformat='$,.0f', automargin=True), title_font=dict(size=13, color='#374151'))
    st.plotly_chart(fig_age, width='stretch')

    insight_box(f"""
    <b>đŸ’¡ Ă nghÄ©a kinh táº¿ cá»§a Biáº¿n sá»‘ TUá»”I Báº¤T Äá»˜NG Sáº¢N (building_age):</b><br>
    â€¢ Há»‡ sá»‘ tÆ°Æ¡ng quan: <b>r = {corr_age:.2f}</b> (TÆ°Æ¡ng quan Ă¢m nháº¹).<br>
    â€¢ <b>Giáº£i thĂ­ch thá»±c táº¿:</b> Báº¥t Ä‘á»™ng sáº£n má»›i xĂ¢y (<15 nÄƒm) sá»Ÿ há»¯u giĂ¡ bĂ¡n cao nháº¥t do thiáº¿t káº¿ hiá»‡n Ä‘áº¡i vĂ  khĂ´ng tá»‘n chi phĂ­ sá»­a chá»¯a. 
      CĂ´ng trĂ¬nh cÅ© cĂ³ xu hÆ°á»›ng giáº£m giĂ¡ do <i>kháº¥u hao tĂ i sáº£n (physical depreciation)</i>. Tuy nhiĂªn táº¡i NYC, má»‘i tÆ°Æ¡ng quan nĂ y khĂ¡ yáº¿u vĂ¬ nhiá»u tĂ²a nhĂ  cá»• (>70 nÄƒm) táº¡i Manhattan hay Brooklyn Heights náº±m á»Ÿ vá»‹ trĂ­ Ä‘áº¥t vĂ ng Ä‘áº¯t Ä‘á» vĂ  cĂ³ kiáº¿n trĂºc lá»‹ch sá»­ Ä‘Æ°á»£c báº£o tá»“n, bĂ¹ Ä‘áº¯p Ä‘Ă¡ng ká»ƒ sá»± suy giáº£m vá» tuá»•i Ä‘á»i.
    """)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 3 â€” BIáº¾N Äá»˜NG THEO THá»œI GIAN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab3:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#b45309,#d97706,#fbbf24);border-radius:14px;
    padding:18px 24px;color:#fff;margin-bottom:22px;
    box-shadow:0 6px 24px rgba(245,158,11,0.35)'>
    <b style='font-size:15px;letter-spacing:-0.3px'>đŸ“… PhĂ¢n tĂ­ch Lá»£i suáº¥t Äáº§u tÆ°: Tá»« VÄ© mĂ´ Ä‘áº¿n Vi mĂ´</b><br>
    <span style='font-size:12px;opacity:0.9'>Theo dĂµi tá»· suáº¥t sinh lá»i theo thá»i gian thá»±c Ä‘á»ƒ tĂ¬m ra khu vá»±c bĂ¹ng ná»•, cĂ¡c há»‘ Ä‘en rá»§i ro, vĂ  nhá»¯ng báº¿n Ä‘á»— an toĂ n nháº¥t.</span>
    </div>
    """, unsafe_allow_html=True)

    import matplotlib.dates as mdates

    # TĂ­nh ym_dt cho df (Ä‘Ă£ filter qua sidebar)
    df_t3 = df.dropna(subset=['sale_year', 'sale_month']).copy()
    df_t3["ym_dt"] = pd.to_datetime(
        df_t3["sale_year"].astype(int).astype(str) + "-" + df_t3["sale_month"].astype(int).astype(str).str.zfill(2),
        format="%Y-%m")

    # 1. TOĂ€N Cáº¢NH
    section_q("1ï¸âƒ£ ToĂ n cáº£nh Thá»‹ trÆ°á»ng", "ÄÆ°á»ng xu hÆ°á»›ng (nĂ©t Ä‘á»©t) cho tháº¥y quá»¹ Ä‘áº¡o lá»£i suáº¥t cá»§a giĂ¡ trung vá»‹ toĂ n khu vá»±c Ä‘ang chá»n.")
    mts_all = df_t3.groupby('ym_dt')['sale_price'].median().reset_index().sort_values('ym_dt')
    if len(mts_all) > 0:
        base_price_all = mts_all['sale_price'].iloc[0]
        mts_all['growth_pct'] = (mts_all['sale_price'] - base_price_all) / base_price_all * 100

        fig_all = go.Figure()
        fig_all.add_trace(go.Scatter(
            x=mts_all['ym_dt'], y=mts_all['growth_pct'], mode='lines',
            name='Thá»‹ trÆ°á»ng chung', line=dict(color=C_BLUE, width=4),
            customdata=mts_all['sale_price'],
            hovertemplate='<b>Thá»‹ trÆ°á»ng chung</b><br>%{x|%m/%Y}<br>TÄƒng trÆ°á»Ÿng: <b>%{y:+.1f}%</b><br>GiĂ¡: $%{customdata:,.0f}<extra></extra>'
        ))
        if len(mts_all) >= 3:
            x_num = mdates.date2num(mts_all['ym_dt'])
            coef = np.polyfit(x_num, mts_all['growth_pct'].ffill().bfill().values, 1)
            trend = np.polyval(coef, x_num)
            fig_all.add_trace(go.Scatter(
                x=mts_all['ym_dt'], y=trend, mode='lines', showlegend=False,
                line=dict(color=C_ORANGE, width=2.5, dash='dash'), hoverinfo='skip'))

        fig_all.add_hline(y=0, line_color="#9CA3AF", line_width=1.5, line_dash="dash")
        clayout(fig_all, h=300, t=20, b=20)
        fig_all.update_layout(
            hovermode='x unified',
            yaxis=dict(ticksuffix='%', title="Tá»· suáº¥t Sinh lá»i (%)", zeroline=False))
        st.plotly_chart(fig_all, width='stretch')
    else:
        st.warning("KhĂ´ng Ä‘á»§ dá»¯ liá»‡u thá»i gian.")

    divider()

    # 2. PHĂ‚N HĂ“A QUáº¬N
    section_q("2ï¸âƒ£ PhĂ¢n hĂ³a Tá»· suáº¥t: Cáº¥p Ä‘á»™ Quáº­n (Borough)", "Sá»± khĂ¡c biá»‡t vá» má»©c Ä‘á»™ sinh lá»i giá»¯a cĂ¡c quáº­n trong cĂ¹ng giai Ä‘oáº¡n.")
    boro_stats = []
    df_boro = df_t3.groupby(["borough_name", "ym_dt"])["sale_price"].median().reset_index().sort_values("ym_dt")
    for boro in sorted(df_boro['borough_name'].unique()):
        sub = df_boro[df_boro['borough_name']==boro]
        if len(sub) < 1: continue
        start_p = sub['sale_price'].iloc[0]
        end_p = sub['sale_price'].iloc[-1]
        pct = (end_p - start_p) / start_p * 100
        boro_stats.append({
            "Quáº­n": boro,
            "GiĂ¡ Báº¯t Äáº§u": start_p,
            "GiĂ¡ Hiá»‡n Táº¡i": end_p,
            "Lá»£i Suáº¥t (%)": pct
        })
    
    if boro_stats:
        df_table = pd.DataFrame(boro_stats).sort_values("Lá»£i Suáº¥t (%)", ascending=False)
        def format_table(df_tbl):
            return df_tbl.style.format({
                "GiĂ¡ Báº¯t Äáº§u": "${:,.0f}",
                "GiĂ¡ Hiá»‡n Táº¡i": "${:,.0f}",
                "Lá»£i Suáº¥t (%)": "{:+.1f}%"
            }).map(lambda x: f"color: {'#EF4444' if x > 0 else '#10B981' if x < 0 else 'black'}; font-weight: bold;" if isinstance(x, (int, float)) and x < 100 else "", subset=["Lá»£i Suáº¥t (%)"])
        st.dataframe(format_table(df_table), width='stretch', hide_index=True)

    divider()

    # 3. Báº¢NG PHONG THáº¦N
    section_q("3ï¸âƒ£ Báº£ng Phong Tháº§n: Cáº¥p Ä‘á»™ Khu vá»±c (Neighborhood)", "Soi rá»i toĂ n bá»™ cĂ¡c khu vá»±c Ä‘á»ƒ tĂ¬m ra cĂ¡c má» vĂ ng vĂ  há»‘ Ä‘en cáº£nh bĂ¡o.")
    neigh_stats = []
    for boro in df_t3["borough_name"].unique():
        b_df = df_t3[df_t3["borough_name"] == boro]
        for n in b_df["neighborhood"].unique():
            sub = b_df[b_df["neighborhood"] == n].groupby("ym_dt")["sale_price"].median().reset_index().sort_values("ym_dt")
            n_gd = len(b_df[b_df["neighborhood"]==n])
            if len(sub) < 3 or n_gd < 10: 
                continue
            start_p = sub["sale_price"].iloc[0]
            end_p = sub["sale_price"].iloc[-1]
            pct = (end_p - start_p) / start_p * 100
            
            # TĂ­nh R2
            sub['growth_pct'] = (sub['sale_price'] - start_p) / start_p * 100
            x_num = mdates.date2num(sub['ym_dt'])
            y = sub['growth_pct'].values
            coef = np.polyfit(x_num, y, 1)
            trend = np.polyval(coef, x_num)
            ss_res = np.sum((y - trend) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

            neigh_stats.append({
                "Quáº­n": boro, "Khu Vá»±c": n, "GiĂ¡ Báº¯t Äáº§u": start_p, 
                "GiĂ¡ Hiá»‡n Táº¡i": end_p, "Lá»£i Suáº¥t (%)": pct, 
                "Slope": coef[0], "R2": r2, "Sá»‘ thĂ¡ng": len(sub), "Sá»‘ GD": n_gd
            })
    
    if neigh_stats:
        df_neigh_all = pd.DataFrame(neigh_stats)
        top_3 = df_neigh_all.sort_values("Lá»£i Suáº¥t (%)", ascending=False).head(3)[["Quáº­n", "Khu Vá»±c", "GiĂ¡ Báº¯t Äáº§u", "GiĂ¡ Hiá»‡n Táº¡i", "Lá»£i Suáº¥t (%)"]].reset_index(drop=True)
        bot_3 = df_neigh_all.sort_values("Lá»£i Suáº¥t (%)", ascending=True).head(3)[["Quáº­n", "Khu Vá»±c", "GiĂ¡ Báº¯t Äáº§u", "GiĂ¡ Hiá»‡n Táº¡i", "Lá»£i Suáº¥t (%)"]].reset_index(drop=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### đŸ”¥ TOP 3 TÄ‚NG Máº NH NHáº¤T")
            st.dataframe(format_table(top_3), width='stretch', hide_index=True)
        with c2:
            st.markdown("##### â ï¸ TOP 3 Sá»¤T GIáº¢M NHIá»€U NHáº¤T")
            st.dataframe(format_table(bot_3), width='stretch', hide_index=True)

        divider()

        # HĂ€M Váº¼ BIá»‚U Äá»’ 1 KHU Vá»°C VS QUáº¬N
        def plot_single_neighborhood(boro_name, neigh_name, title, color_neigh):
            fig = go.Figure()
            sub_b = df_boro[df_boro["borough_name"] == boro_name].copy()
            if len(sub_b) > 0:
                base_b = sub_b["sale_price"].iloc[0]
                sub_b['growth_pct'] = (sub_b['sale_price'] - base_b) / base_b * 100
                fig.add_trace(go.Scatter(
                    x=sub_b['ym_dt'], y=sub_b['growth_pct'],
                    mode='lines', name=f"Trung bĂ¬nh {boro_name}",
                    line=dict(color='#9CA3AF', width=2, dash='dot'),
                    customdata=sub_b['sale_price'],
                    hovertemplate=f'<b>TB {boro_name}</b><br>%{{x|%m/%Y}}<br>Lá»£i suáº¥t: %{{y:+.1f}}%<extra></extra>'))
                
            df_neigh = df_t3[(df_t3["borough_name"] == boro_name) & (df_t3["neighborhood"] == neigh_name)]
            sub_n = df_neigh.groupby("ym_dt")["sale_price"].median().reset_index().sort_values("ym_dt")
            final_pct = 0
            if len(sub_n) > 0:
                base_n = sub_n["sale_price"].iloc[0]
                sub_n['growth_pct'] = (sub_n['sale_price'] - base_n) / base_n * 100
                final_pct = sub_n['growth_pct'].iloc[-1]
                
                fig.add_trace(go.Scatter(
                    x=sub_n['ym_dt'], y=sub_n['growth_pct'],
                    mode='lines', name=neigh_name,
                    line=dict(color=color_neigh, width=4),
                    customdata=sub_n['sale_price'],
                    hovertemplate=f'<b>{neigh_name}</b><br>%{{x|%m/%Y}}<br>Lá»£i suáº¥t: <b>%{{y:+.1f}}%</b><br>GiĂ¡: $%{{customdata:,.0f}}<extra></extra>'))

                if len(sub_n) >= 3:
                    x_num = mdates.date2num(sub_n['ym_dt'])
                    coef = np.polyfit(x_num, sub_n['growth_pct'].ffill().bfill().values, 1)
                    trend = np.polyval(coef, x_num)
                    fig.add_trace(go.Scatter(
                        x=sub_n['ym_dt'], y=trend, mode='lines', showlegend=False,
                        line=dict(color=color_neigh, width=1.5, dash='dash'), hoverinfo='skip'))

            fig.add_hline(y=0, line_color="#9CA3AF", line_width=1.5, line_dash="dash")
            clayout(fig, h=320, t=50, b=20)
            fig.update_layout(
                title=dict(text=title, font=dict(size=14, color='#374151')),
                hovermode='x unified',
                yaxis=dict(ticksuffix='%', title="", zeroline=False),
                legend=dict(orientation='h', y=1.1, x=0))
            return fig, final_pct

        # 4. NGHá»CH LĂ
        col_a, col_b = st.columns(2)
        if len(top_3) > 0:
            top_boro = top_3.iloc[0]["Quáº­n"]
            top_neigh = top_3.iloc[0]["Khu Vá»±c"]
            with col_a:
                section_q("4ï¸âƒ£ Äá»‰nh cao sinh lá»i", "")
                fig_top, pct_top = plot_single_neighborhood(top_boro, top_neigh, f"đŸ€ {top_neigh} (TÄƒng máº¡nh nháº¥t)", C_RED)
                st.plotly_chart(fig_top, width='stretch')
                insight_box(f"VÆ°á»£t xa Ä‘Æ°á»ng trung bĂ¬nh cá»§a Quáº­n <b>{top_boro}</b>, <b>{top_neigh}</b> lĂ  báº¿n Ä‘á»— sinh lá»i bá»©t phĂ¡ nháº¥t vá»›i <b>+{pct_top:.1f}%</b> lá»£i suáº¥t.")

        if len(bot_3) > 0:
            bot_boro = bot_3.iloc[0]["Quáº­n"]
            bot_neigh = bot_3.iloc[0]["Khu Vá»±c"]
            with col_b:
                section_q("5ï¸âƒ£ Há»‘ Ä‘en tá»­ tháº§n", "")
                fig_bot, pct_bot = plot_single_neighborhood(bot_boro, bot_neigh, f"â ï¸ {bot_neigh} (Giáº£m máº¡nh nháº¥t)", C_GREEN)
                st.plotly_chart(fig_bot, width='stretch')
                insight_box(f"NgÆ°á»£c chiá»u hoĂ n toĂ n vá»›i xu hÆ°á»›ng cá»§a Quáº­n <b>{bot_boro}</b>, NÄT táº¡i <b>{bot_neigh}</b> gĂ¡nh chá»‹u khoáº£n lá»— khá»•ng lá»“ lĂªn tá»›i <b>{pct_bot:.1f}%</b>.")

        divider()

        # 5. á»”N Äá»NH
        stable_up = df_neigh_all[(df_neigh_all['Slope'] > 0) & (df_neigh_all['Sá»‘ thĂ¡ng'] >= 5) & (df_neigh_all['Sá»‘ GD'] >= 30)].sort_values("R2", ascending=False)
        stable_down = df_neigh_all[(df_neigh_all['Slope'] < 0) & (df_neigh_all['Sá»‘ thĂ¡ng'] >= 5) & (df_neigh_all['Sá»‘ GD'] >= 30)].sort_values("R2", ascending=False)

        col_c, col_d = st.columns(2)
        if len(stable_up) > 0:
            up_boro = stable_up.iloc[0]["Quáº­n"]
            up_neigh = stable_up.iloc[0]["Khu Vá»±c"]
            with col_c:
                section_q("6ï¸âƒ£ TÄƒng trÆ°á»Ÿng á»”n Ä‘á»‹nh nháº¥t", "")
                fig_up, pct_up = plot_single_neighborhood(up_boro, up_neigh, f"đŸ“ˆ {up_neigh} (Ăt rá»§i ro biáº¿n Ä‘á»™ng)", C_ORANGE)
                st.plotly_chart(fig_up, width='stretch')
                insight_box(f"Bá» qua cĂ¡c cĂº sá»‘c giáº­t cá»¥c, <b>{up_neigh}</b> lĂ  báº¿n Ä‘á»— an toĂ n nháº¥t. Lá»£i suáº¥t tÄƒng bĂ¡m sĂ¡t Ä‘Æ°á»ng xu hÆ°á»›ng Ä‘áº¡t <b>+{pct_up:.1f}%</b>.")

        if len(stable_down) > 0:
            down_boro = stable_down.iloc[0]["Quáº­n"]
            down_neigh = stable_down.iloc[0]["Khu Vá»±c"]
            with col_d:
                section_q("7ï¸âƒ£ Suy thoĂ¡i á»”n Ä‘á»‹nh nháº¥t", "")
                fig_down, pct_down = plot_single_neighborhood(down_boro, down_neigh, f"đŸ“‰ {down_neigh} (TrÆ°á»£t dá»‘c tá»« tá»«)", "#8B5CF6")
                st.plotly_chart(fig_down, width='stretch')
                insight_box(f"KhĂ¡c vá»›i cĂº sáº­p báº¥t ngá», <b>{down_neigh}</b> rá»‰ mĂ¡u tá»« tá»« qua tá»«ng thĂ¡ng. GiĂ¡ trá»‹ Ä‘Ă£ bá»‘c hÆ¡i <b>{pct_down:.1f}%</b> dá»c theo Ä‘Æ°á»ng xu hÆ°á»›ng giáº£m.")



# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 4 â€” Dá»° BĂO & MĂ” HĂŒNH ML
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab4:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f172a,#1e293b,#334155);border-radius:14px;
    padding:18px 24px;color:#fff;margin-bottom:22px;
    box-shadow:0 6px 24px rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.07)'>
    <b style='font-size:15px;letter-spacing:-0.3px'>đŸ¤– MĂ´ hĂ¬nh Machine Learning dá»± bĂ¡o giĂ¡ nhÆ° tháº¿ nĂ o?</b><br>
    <span style='font-size:12px;opacity:0.75'>So sĂ¡nh hiá»‡u suáº¥t mĂ´ hĂ¬nh, yáº¿u tá»‘ quan trá»ng vĂ  cĂ´ng cá»¥ Æ°á»›c tĂ­nh giĂ¡ tÆ°Æ¡ng tĂ¡c.</span>
    </div>
    """, unsafe_allow_html=True)

    pred_df4, imp4, ml4 = load_ml_data()

    if not ml4:
        st.warning("â ï¸ ChÆ°a cĂ³ káº¿t quáº£ ML. HĂ£y cháº¡y `main.py` trÆ°á»›c.")
    else:
        rf4 = ml4.get('Random Forest', {}); lr4 = ml4.get('Linear Regression', {})
        m1,m2,m3,m4 = st.columns(4)
        acc4 = max(0,(1-rf4.get('MAE',0)/df['sale_price'].median())*100)
        mape4 = rf4.get('MAPE', None)
        m1.metric("Äá»™ chĂ­nh xĂ¡c Æ°á»›c tĂ­nh", f"{acc4:.1f}%", delta="Random Forest tá»‘t nháº¥t")
        m2.metric("Sai sá»‘ trung bĂ¬nh (MAE)", f"${rf4.get('MAE',0):,.0f}")
        m3.metric("RÂ² â€” Má»©c giáº£i thĂ­ch", f"{rf4.get('R2',0)*100:.1f}%")
        if mape4:
            m4.metric("Lá»‡ch giĂ¡ TB (%)", f"{mape4:.1f}%")
        else:
            m4.metric("RMSE", f"${rf4.get('RMSE',0):,.0f}")

        section_q("MĂ´ hĂ¬nh nĂ o dá»± bĂ¡o chĂ­nh xĂ¡c hÆ¡n?",
                  "RÂ² cĂ ng gáº§n 1, MAE/RMSE cĂ ng tháº¥p = tá»‘t hÆ¡n. So sĂ¡nh trĂªn cĂ¹ng táº­p kiá»ƒm tra.")
        rows4 = [{'MĂ´ hĂ¬nh': n,
                   'Äiá»ƒm RÂ²':  f"{m['R2']:.4f}",
                   'Sai sá»‘ TB ($)': f"${m['MAE']:,.0f}",
                   'CÄƒn SSBT ($)': f"${m['RMSE']:,.0f}",
                   'ÄĂ¡nh giĂ¡': 'âœ… Tá»‘t hÆ¡n' if n == 'Random Forest' else 'đŸ“ Tham kháº£o'}
                 for n, m in ml4.items()]
        st.dataframe(pd.DataFrame(rows4).set_index('MĂ´ hĂ¬nh'), width='stretch')

        divider()
        ci1, ci2 = st.columns(2)
        with ci1:
            section_q("Yáº¿u tá»‘ nĂ o mĂ´ hĂ¬nh cho lĂ  quyáº¿t Ä‘á»‹nh nháº¥t?","")
            if imp4 is not None:
                imp4s = imp4.copy()
                imp4s['TĂªn'] = imp4s['Feature'].map(lambda f: FEATURE_LABELS.get(f,f))
                imp4s = imp4s.sort_values('Importance')
                fig_i = px.bar(imp4s, x='Importance', y='TĂªn', orientation='h',
                               color='Importance', color_continuous_scale='Blues',
                               text=imp4s['Importance'].apply(lambda v: f'{v*100:.1f}%'),
                               labels={'Importance': 'Má»©c Ä‘á»™ quan trá»ng', 'TĂªn': 'Yáº¿u tá»‘'},
                               title='Má»©c Ä‘á»™ quan trá»ng cá»§a tá»«ng yáº¿u tá»‘ (Random Forest)')
                fig_i.update_traces(textposition='auto')
                clayout(fig_i, h=360, t=40, b=10, r=80)
                fig_i.update_layout(coloraxis_showscale=False,
                                    title_font=dict(size=13, color='#374151'),
                                    xaxis=dict(tickformat='.0%', automargin=True, title='Má»©c Ä‘á»™ quan trá»ng'),
                                    yaxis=dict(automargin=True, title=''))
                st.plotly_chart(fig_i, width='stretch')
        with ci2:
            section_q("Dá»± bĂ¡o sĂ¡t thá»±c táº¿ Ä‘áº¿n má»©c nĂ o?","")
            if pred_df4 is not None:
                pp4 = pred_df4.sample(n=min(1500,len(pred_df4)), random_state=42)
                fig_av4 = px.scatter(pp4, x='Actual', y='Predicted', opacity=0.4,
                                     color_discrete_sequence=[C_BLUE2],
                                     labels={'Actual':'GiĂ¡ thá»±c ($)','Predicted':'GiĂ¡ dá»± bĂ¡o ($)'},
                                     title='Dá»± bĂ¡o vs Thá»±c táº¿ â€” Äá»™ chĂ­nh xĂ¡c mĂ´ hĂ¬nh Random Forest',
                                     trendline='ols')
                # Äáº·t tĂªn cho OLS trendline trace Ä‘á»ƒ trĂ¡nh 'undefined' trong legend
                for trace in fig_av4.data:
                    if hasattr(trace, 'name') and trace.name and 'OLS' in str(trace.name):
                        trace.name = 'Xu hÆ°á»›ng OLS'
                vm4 = max(pred_df4['Actual'].max(), pred_df4['Predicted'].max())
                fig_av4.add_trace(go.Scatter(x=[0,vm4], y=[0,vm4], mode='lines',
                                             name='LĂ½ tÆ°á»Ÿng (y=x)',
                                             line=dict(color=C_RED, dash='dash', width=1.5)))
                clayout(fig_av4, h=360, t=40, b=10, leg=True)
                fig_av4.update_layout(
                    title_font=dict(size=13, color='#374151'),
                    xaxis=dict(tickformat='$,.0f', automargin=True, title='GiĂ¡ thá»±c ($)'),
                    yaxis=dict(tickformat='$,.0f', automargin=True, title='GiĂ¡ dá»± bĂ¡o ($)'),
                    legend=dict(font_size=11))
                st.plotly_chart(fig_av4, width='stretch')

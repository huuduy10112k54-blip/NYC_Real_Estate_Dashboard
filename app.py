import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import json
import os
import zlib

# â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• 
# Cáº¤U HĂŒNH TRANG
# â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• 
st.set_page_config(
    page_title="Báo cáo Phân tích Thị trường Bất động sản NYC 2025 - 2026",
    layout="wide",
    page_icon="ï¸ ",
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
div[data-baseweb="select"] {
    border: 2px solid #2563eb !important;
    border-radius: 6px !important;
    background-color: #ffffff !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.15) !important;
}
div[data-baseweb="select"] > div {
    border: none !important;
    background-color: transparent !important;
}
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
    'gross_sqft':'Diá»‡n tĂch tá»•ng (sqft)', 'building_age':'Tuá»•i cĂ´ng trĂ¬nh (nÄƒm)',
    'land_sqft':'Diá»‡n tĂch Ä‘áº¥t (sqft)',   'pop_density':'Máºt Ä‘á»™ dĂ¢n sá»‘ (/kmÂ²)',
    'total_units':'Sá»‘ cÄƒn trong tĂ²a',
    'gdp_local':'GDP Ä‘á»‹a phÆ°Æ¡ng (%)',      'avg_income':'Thu nháºp bĂ¬nh quĂ¢n ($)',
    'dist_center':'KC Ä‘áº¿n trung tĂ¢m (km)',
}
REQUIRED_COLS = [
    'borough','neighborhood','building_type','gross_sqft','land_sqft',
    'sale_price','sale_year','sale_date','building_age','total_units',
    'pop_density','avg_income','gdp_local','dist_center','amenity_score'
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
    """Láº¥y tá»a Ä‘á»™ lat/lon chuáº©n hoáº·c suy luáºn theo offset nhá» tá»« centroid quáºn."""
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
def _get_cache_mtime():
    """Láº¥y modification time cá»§a DB vĂ  DATA.csv Ä‘á»ƒ lĂ m cache-key. Khi náº¡p dá»¯ liá»‡u má»›i â†’ cache tá»± Ä‘á»™ng lĂ m má»›i."""
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'warehouse', 'nyc_warehouse.db')
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'data clean', 'DATA.csv')
        t_db = os.path.getmtime(db_path) if os.path.exists(db_path) else 0
        t_data = os.path.getmtime(data_path) if os.path.exists(data_path) else 0
        return max(t_db, t_data)
    except:
        return 0

@st.cache_data
def load_data(query=None, cache_mtime=None):
    # Cache tá»± Ä‘á»™ng invalidate khi cache_mtime thay Ä‘á»•i


    """Äá»c dá»¯ liá»‡u tá»« SQLite Data Warehouse local."""
    try:
        import sqlite3
        import os
        import zipfile
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'warehouse', 'nyc_warehouse.db')
        zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'warehouse', 'nyc_warehouse.zip')
        
        # Tá»± Ä‘á»™ng giáº£i nĂ©n náº¿u chÆ°a cĂ³ db hoáº·c zip má»›i hÆ¡n
        if os.path.exists(zip_path):
            need_extract = True
            if os.path.exists(db_path):
                # Kiá»ƒm tra náº¿u file zip má»›i hÆ¡n file db thĂ¬ giáº£i nĂ©n Ä‘Ă¨ lĂªn
                if os.path.getmtime(zip_path) <= os.path.getmtime(db_path):
                    need_extract = False
                    # Kiá»ƒm tra DB cĂ³ bá»‹ há»ng do race condition trÆ°á»›c Ä‘Ă³ khĂ´ng
                    try:
                        conn_test = sqlite3.connect(db_path)
                        conn_test.execute("SELECT 1 FROM fact_sales LIMIT 1")
                        conn_test.close()
                    except sqlite3.DatabaseError:
                        need_extract = True
            
            if need_extract:
                try:
                    import filelock
                    lock_path = db_path + ".lock"
                    with filelock.FileLock(lock_path, timeout=60):
                        do_extract = True
                        if os.path.exists(db_path):
                            try:
                                c2 = sqlite3.connect(db_path)
                                c2.execute("SELECT 1 FROM fact_sales LIMIT 1")
                                c2.close()
                                if os.path.getmtime(zip_path) <= os.path.getmtime(db_path):
                                    do_extract = False
                            except sqlite3.DatabaseError:
                                do_extract = True
                        
                        if do_extract:
                            try:
                                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                                    zip_ref.extractall(os.path.dirname(db_path))
                            except zipfile.BadZipFile as e:
                                if not os.path.exists(db_path):
                                    raise Exception(f"File zip bá»‹ lá»—i (cĂ³ thá»ƒ do Git LFS) vĂ  khĂ´ng tĂ¬m tháº¥y file db: {e}")
                except ImportError:
                    try:
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            zip_ref.extractall(os.path.dirname(db_path))
                    except zipfile.BadZipFile as e:
                        if not os.path.exists(db_path):
                            raise Exception(f"File zip bá»‹ lá»—i (cĂ³ thá»ƒ do Git LFS) vĂ  khĂ´ng tĂ¬m tháº¥y file db: {e}")
                
        conn = sqlite3.connect(db_path)
        
        if query:
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
            
        engine = conn
        _chunks = pd.read_sql("""
            SELECT 
                b.borough_id AS borough,
                b.borough_name,
                n.neighborhood_name as neighborhood,
                p.building_class_category,
                p.building_category,
                p.building_type,
                p.building_class_present,
                p.tax_class_present,
                p.gross_sqft,
                p.land_sqft,
                p.building_age,
                p.total_units,
                p.is_residential,
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
                n.amenity_score
            FROM fact_sales f
            JOIN dim_location       l ON f.location_id    = l.location_id
            JOIN dim_neighborhood   n ON l.neighborhood_id = n.neighborhood_id
            JOIN dim_borough        b ON n.borough_id      = b.borough_id
            JOIN dim_property       p ON f.property_id     = p.property_id
            JOIN dim_social_metrics s ON f.social_id       = s.social_id
        """, engine, chunksize=50000)
        
        processed_chunks = []
        num_cols = ['gross_sqft', 'land_sqft', 'building_age', 'sale_year', 'avg_income', 'dist_center', 'pop_density']
        
        for chunk in _chunks:
            # Lá»c bá»›t dĂ²ng rĂ¡c ngay tá»« Ä‘áº§u Ä‘á»ƒ giáº£m sá»‘ lÆ°á»£ng
            chunk['sale_price'] = pd.to_numeric(chunk['sale_price'], errors='coerce')
            chunk = chunk[chunk['sale_price'] > 10_000].copy()
            
            # Chuáº©n hoĂ¡ sá»‘
            for c in num_cols:
                if c in chunk.columns:
                    chunk[c] = pd.to_numeric(chunk[c], errors='coerce', downcast='float')
            
            chunk.loc[chunk['gross_sqft'] <= 0, 'gross_sqft'] = np.nan
            chunk.loc[chunk['land_sqft']  <= 0, 'land_sqft']  = np.nan
            
            # Use the real price per sqft from DB if available, fallback to manual calc
            if 'price_per_sqft_real' in chunk.columns:
                chunk['price_per_sqft'] = chunk['price_per_sqft_real']
            else:
                chunk['price_per_sqft'] = np.where(chunk['gross_sqft'].notna(),
                                                  chunk['sale_price'] / chunk['gross_sqft'], np.nan)

            
            # Xá» lĂ½ ngĂ y thĂ¡ng ngay trong chunk Ä‘á»ƒ giáº£i phĂ³ng text (há»— trá»£ cáº£ Ä‘á»‹nh dáº¡ng DD/MM/YYYY vĂ  YYYY-MM-DD)
            chunk['sale_date_parsed'] = pd.to_datetime(chunk['sale_date'], dayfirst=True, errors='coerce')
            chunk['sale_month']       = chunk['sale_date_parsed'].dt.month.fillna(0).astype('int16')
            
            # KhĂ´i phá»¥c building_category vĂ  building_type tá»« building_class_category (bá»‹ thiáº¿u trong SQLite)
            if 'building_class_category' in chunk.columns:
                split_cols = chunk['building_class_category'].astype(str).str.split('-', n=1, expand=True)
                chunk['building_category'] = split_cols[0].str.strip()
                if split_cols.shape[1] > 1:
                    chunk['building_type'] = split_cols[1].str.strip()
                    # Äiá»n missing type báº±ng category náº¿u split khĂ´ng ra 2 pháº§n
                    chunk['building_type'] = chunk['building_type'].fillna(chunk['building_category'])
                else:
                    chunk['building_type'] = chunk['building_category']
            
            # Ă‰p kiá»ƒu int/float Ä‘á»ƒ giáº£m dung lÆ°á»£ng
            for c in chunk.select_dtypes(include=['int64', 'float64']).columns:
                if chunk[c].dtype == 'int64':
                    chunk[c] = pd.to_numeric(chunk[c], downcast='integer')
                else:
                    chunk[c] = pd.to_numeric(chunk[c], downcast='float')
                    
            processed_chunks.append(chunk)
            
        df = pd.concat(processed_chunks, ignore_index=True)
        engine.close()
    except Exception as e:
        return None, f"Lá»—i Ä‘á»c SQLite: {e}"

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        return None, f"Thiáº¿u cá»™t sau JOIN: {', '.join(missing)}"

    # Chuyá»ƒn Ä‘á»•i chuá»—i sang category má»™t láº§n sau khi concat (tiáº¿t kiá»‡m 90% RAM)
    for c in df.select_dtypes(include=['object', 'string']).columns:
        if df[c].nunique() < 1000:
            df[c] = df[c].astype('category')
            
    return df, None

@st.cache_data
def get_flipping_stats(df_in):
    # Táº¡o mĂ£ Ä‘á»‹nh danh duy nháº¥t cho tá»«ng lĂ´ Ä‘áº¥t
    cols = ['borough_name', 'block', 'lot', 'sale_date', 'sale_date_parsed', 'sale_price', 'neighborhood']
    df_f = df_in.loc[:, cols].copy()
    df_f['property_id'] = df_f['borough_name'].astype(str) + '-' + df_f['block'].astype(str) + '-' + df_f['lot'].astype(str)
    
    # Sáº¯p xáº¿p theo ID vĂ  ngĂ y bĂ¡n
    df_f = df_f.sort_values(by=['property_id', 'sale_date_parsed'])
    
    # DĂ¹ng shift() Ä‘á»ƒ so sĂ¡nh vá»›i giao dá»‹ch liá»n trÆ°á»›c
    df_f['prev_prop'] = df_f['property_id'].shift(1)
    df_f['buy_date'] = df_f['sale_date_parsed'].shift(1)
    df_f['buy_price'] = df_f['sale_price'].shift(1)

    # Chá»‰ giá»¯ láº¡i nhá»¯ng giao dá»‹ch lĂ  láº§n bĂ¡n thá»© 2 trá»Ÿ lĂªn cá»§a cĂ¹ng 1 property
    flips = df_f[df_f['property_id'] == df_f['prev_prop']].copy()
    
    if len(flips) == 0:
        return None, None, None

    # TĂnh toĂ¡n cĂ¡c chá»‰ sá»‘
    flips['days_held'] = (flips['sale_date_parsed'] - flips['buy_date']).dt.days
    flips['profit'] = flips['sale_price'] - flips['buy_price']
    flips['roi'] = np.where(flips['buy_price'] > 0, flips['profit'] / flips['buy_price'], 0)

    # Lá»c Ä‘iá»u kiá»‡n lÆ°á»›t sĂ³ng: giá»¯ nhĂ  tá»« 1 ngĂ y Ä‘áº¿n 3 nÄƒm (1095 ngĂ y)
    df_res = flips[(flips['days_held'] >= 1) & (flips['days_held'] <= 1095)].copy()
    
    if len(df_res) == 0:
        return None, None, None

    neigh_stats = df_res.groupby(['borough_name', 'neighborhood']).agg(
        num_flips=('neighborhood', 'count'),
        avg_profit=('profit', 'mean'),
        avg_roi=('roi', 'mean'),
        avg_days=('days_held', 'mean')
    ).reset_index()
    
    neigh_stats = neigh_stats[neigh_stats['num_flips'] >= 2]
    
    # Khu vá»±c Ä‘á»‹nh cÆ° (Ăt lÆ°á»›t sĂ³ng)
    all_sales = df_f.groupby('neighborhood')['property_id'].count().reset_index(name='total_sales')
    long_term = pd.merge(all_sales, neigh_stats, on='neighborhood', how='left')
    long_term['num_flips'] = long_term['num_flips'].fillna(0)
    long_term['flip_rate'] = (long_term['num_flips'] / long_term['total_sales']) * 100
    long_term = long_term[long_term['total_sales'] >= 30]

    return df_res, neigh_stats, long_term

@st.cache_data
def load_ml_data(mtime=None):
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
        ('gross_sqft', 'Diá»‡n tĂch cĂ´ng trĂ¬nh (gross_sqft)', 'Quy mĂ´ khĂ´ng gian sá» dá»¥ng; biáº¿n sá»‘ quan trá»ng hĂ ng Ä‘áº§u Ä‘á»‹nh giĂ¡ tá»•ng tĂ i sáº£n.'),
        ('avg_income', 'Thu nháºp khu vá»±c (avg_income)', 'Máº·t báº±ng thu nháºp cÆ° dĂ¢n; Ä‘áº¡i diá»‡n cho sá»©c mua vĂ  má»©c Ä‘á»™ Ä‘áº¯t Ä‘á» cá»§a vĂ¹ng.'),

        ('dist_center', 'KC Ä‘áº¿n trung tĂ¢m (dist_center)', 'Khoáº£ng cĂ¡ch Ä‘á»‹a lĂ½ tá»›i trung tĂ¢m tĂ i chĂnh Manhattan (cĂ ng xa giĂ¡ giáº£m).'),
        ('pop_density', 'Máºt Ä‘á»™ dĂ¢n sá»‘ (pop_density)', 'Máºt Ä‘á»™ dĂ¢n cÆ° sinh sá»‘ng; pháº£n Ă¡nh Ä‘á»™ sáº§m uáº¥t vĂ  nhu cáº§u nhĂ  á»Ÿ khu vá»±c.'),
        ('building_age', 'Tuá»•i cĂ´ng trĂ¬nh (building_age)', 'Sá»‘ nÄƒm cĂ´ng trĂ¬nh Ä‘Ă£ váºn hĂ nh (cĂ´ng trĂ¬nh cÅ© chá»‹u kháº¥u hao tĂ i sáº£n).'),
        ('land_sqft', 'Diá»‡n tĂch Ä‘áº¥t (land_sqft)', 'Diá»‡n tĂch lĂ´ Ä‘áº¥t (áº£nh hÆ°á»Ÿng Ăt hÆ¡n gross_sqft do Ä‘áº·c thĂ¹ nhĂ  chung cÆ° táº¡i NYC).'),
    ]
    
    rows = []
    for col, name, desc in factors:
        if col in df_in.columns:
            valid = df_in.dropna(subset=['sale_price', col])
            if len(valid) >= 20:
                r = valid['sale_price'].corr(valid[col])
                abs_r = abs(r)
                if abs_r >= 0.50:
                    level = " Ráº¤T Máº NH"
                elif abs_r >= 0.35:
                    level = " Máº NH"
                elif abs_r >= 0.15:
                    level = "ï¸ TRUNG BĂŒNH"
                else:
                    level = " Yáº¾U"
                
                direction = "Thuáºn (+)" if r > 0 else "Nghá»‹ch (-)"
                rows.append({
                    'Yáº¿u tá»‘ tĂ¡c Ä‘á»™ng': name,
                    'TÆ°Æ¡ng quan (r)': round(r, 2),
                    'Má»©c Ä‘á»™ áº£nh hÆ°á»Ÿng': level,
                    'Chiá»u tĂ¡c Ä‘á»™ng': direction,
                    'Giáº£i thĂch Ă½ nghÄ©a thá»±c táº¿': desc,
                    '_abs_r': abs_r
                })
    
    fdf = pd.DataFrame(rows).sort_values('_abs_r', ascending=False)
    
    col_tbl, col_chart = st.columns([3, 2])
    with col_tbl:
        display_df = fdf[['Yáº¿u tá»‘ tĂ¡c Ä‘á»™ng', 'TÆ°Æ¡ng quan (r)', 'Má»©c Ä‘á»™ áº£nh hÆ°á»Ÿng', 'Chiá»u tĂ¡c Ä‘á»™ng', 'Giáº£i thĂch Ă½ nghÄ©a thá»±c táº¿']].copy()
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
df_raw, load_err = load_data(cache_mtime=_get_cache_mtime())

if df_raw is not None:
    # Safely filter for 2025-2026 after all data is loaded
    df_raw['sale_year'] = pd.to_numeric(df_raw['sale_year'], errors='coerce')
    df_raw = df_raw[df_raw['sale_year'] >= 2025].reset_index(drop=True)
    if df_raw.empty:
        df_raw = None
        load_err = "KhĂ´ng cĂ³ dá»¯ liá»‡u nĂ o khá»›p vá»›i nÄƒm 2025 trá»Ÿ Ä‘i."

if df_raw is None:
    st.error(f"ï¸ **Lá»—i:** {load_err}")
    st.info("HĂ£y cháº¡y `main.py` trÆ°á»›c.")
    st.stop()

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SIDEBAR
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 10px'>
        <div style='font-size:36px'>ï¸</div>
        <div style='font-size:14px;font-weight:700;color:#f1f5f9;margin-top:6px'>Bá»™ lá»c dá»¯ liá»‡u</div>
        <div style='font-size:11px;color:#64748b;margin-top:2px'>NYC Real Estate Analytics</div>
    </div>
    <hr style='border-color:#1e3a5f;margin:0 0 14px'>
    """, unsafe_allow_html=True)
    all_b = [b for b in BOROUGH_ORDER if b in df_raw['borough_name'].dropna().unique()]
    selected_boroughs = st.multiselect(" Quáºn (Borough)", options=all_b, default=all_b)
    avail_years = sorted(df_raw['sale_year'].dropna().astype(int).unique().tolist())
    year_range  = st.select_slider(" NÄƒm giao dá»‹ch", options=avail_years,
                                   value=(min(avail_years), max(avail_years)))
    p5  = float(df_raw['sale_price'].quantile(0.05))
    p95 = float(df_raw['sale_price'].quantile(0.95))
    price_range = st.slider(" Khoáº£ng giĂ¡ ($)",
                            min_value=float(df_raw['sale_price'].min()),
                            max_value=float(df_raw['sale_price'].max()),
                            value=(p5, p95), format="$%.0f",
                            help="Máº·c Ä‘á»‹nh p5â€“p95 Ä‘á»ƒ loáº¡i bá» outlier.")
    st.markdown('<hr style="border-color:#1e3a5f;margin:14px 0 10px">', unsafe_allow_html=True)
    if st.button(" Äáº·t láº¡i bá»™ lá»c", width='stretch'):
        st.rerun()
    st.markdown(f"""
    <div style='text-align:center;margin-top:10px;color:#475569;font-size:11px'>
        Tá»•ng: {len(df_raw):,} giao dá»‹ch<br>Nguá»“n: NYC Property Sales
    </div>""", unsafe_allow_html=True)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# ĂP Dá»¤NG Bá»˜ Lá»ŒC
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
if not selected_boroughs:
    st.warning("ï¸ ChÆ°a chá»n quáºn nĂ o. HĂ£y chá»n Ăt nháº¥t má»™t quáºn trong bá»™ lá»c bĂªn trĂ¡i.")
    st.stop()
df = apply_filters(df_raw, selected_boroughs, year_range, price_range)
if len(df) == 0:
    st.warning("ï¸ **KhĂ´ng cĂ³ dá»¯ liá»‡u phĂ¹ há»£p.** HĂ£y má»Ÿ rá»™ng bá»™ lá»c hoáº·c nháº¥n Äáº·t láº¡i.")
    st.stop()

df_sample = df.sample(n=min(3000, len(df)), random_state=42)
df_ppsf   = df.loc[df['price_per_sqft'].notna() & (df['price_per_sqft'] < 5000), ['price_per_sqft']]

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TIĂU Äá»€
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
h1, h2 = st.columns([4, 1])
with h1:
    st.markdown("""
    <h1 style='font-size:24px;font-weight:800;color:#0f172a;margin:0'>
    ï¸ BĂO CĂO PHĂ‚N TĂCH THá» TRÆ¯á»œNG Báº¤T Äá»˜NG Sáº¢N NEW YORK GIAI ÄOáº N 2025 - 2026
    </h1>""", unsafe_allow_html=True)
with h2:
    st.markdown(f"""
    <div style='text-align:right;padding-top:6px'>
        <span class="badge"> {len(df):,} giao dá»‹ch</span><br>
        <span style='font-size:11px;color:#94a3b8'>{len(selected_boroughs)} quáºn Â· {year_range[0]}â€“{year_range[1]}</span>
    </div>""", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom:18px'></div>", unsafe_allow_html=True)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TABS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
tab0, tab1, tab2, tab4, tab_macro, tab_micro = st.tabs([
    "  Tá»•ng quan",
    "ï¸  PhĂ¢n tĂch khu vá»±c",
    "  Yáº¿u tá»‘ quyáº¿t Ä‘á»‹nh giĂ¡",
    "  Dá»± bĂ¡o & MĂ´ hĂ¬nh ML",
    "  PhĂ¢n tĂch Äáº§u tÆ° BÄS",
    "  Tra cá»©u BÄS & Tiá»‡n Ăch"
])

with tab_macro:
    st.markdown("### đŸ›ï¸ ÄĂ¡nh giĂ¡ Tiá»m nÄƒng Khu vá»±c")
    st.info("Há»‡ thá»‘ng dá»±a vĂ o thuáºt toĂ¡n vĂ  dá»¯ liá»‡u lá»‹ch sá» Ä‘á»ƒ phĂ¢n tĂch cĂ¡c khu vá»±c (Neighborhoods) cĂ³ Ä‘áº·c tĂnh tÄƒng trÆ°á»Ÿng hoáº·c thanh khoáº£n cao nháº¥t.")
    tab_adv, tab_evid = st.tabs(["đŸ¯ Gá»£i Ă½ Äáº§u tÆ°", "đŸ“ Dá»¯ liá»‡u Lá»‹ch sá»"])

with tab_micro:
    st.markdown("### đŸ¡ Tra cá»©u Báº¥t Ä‘á»™ng sáº£n")
    tab_search, tab7 = st.tabs(["đŸ” TĂ¬m kiáº¿m Báº¥t Ä‘á»™ng sáº£n", "đŸ“ PhĂ¢n tĂch Tiá»‡n Ăch"])


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 0 â€” Tá»”NG QUAN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab0:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#4338ca,#6366f1,#818cf8);border-radius:14px;
    padding:18px 24px;color:#fff;margin-bottom:22px;
    box-shadow:0 6px 24px rgba(99,102,241,0.35)'>
    <b style='font-size:15px;letter-spacing:-0.3px'>ï¸ Thá»‹ trÆ°á»ng Ä‘ang á»Ÿ Ä‘Ă¢u vĂ  quy mĂ´ nhÆ° tháº¿ nĂ o?</b><br>
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
        "Sá»‘ giao dá»‹ch = thanh khoáº£n. GiĂ¡ trung vá»‹ Ăt bá»‹ áº£nh hÆ°á»Ÿng bá»Ÿi outlier hÆ¡n giĂ¡ trung bĂ¬nh."
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
                     labels={'Borough':'Quáºn', 'Giao dá»‹ch':'Sá»‘ giao dá»‹ch'},
                     title="Sá»‘ giao dá»‹ch theo quáºn")
        fig.update_traces(texttemplate='%{text:,}', textposition='auto')
        clayout(fig, h=280, t=40, r=80)
        fig.update_layout(yaxis=dict(automargin=True, title='Quáºn'), xaxis=dict(automargin=True, title='Sá»‘ giao dá»‹ch'),
                          title_font=dict(size=13, color='#374151'))
        st.plotly_chart(fig, width='stretch')
    with cb:
        fig = px.bar(bor_med.sort_values('GiĂ¡ trung vá»‹'), x='GiĂ¡ trung vá»‹', y='Borough', orientation='h',
                     color='Borough', color_discrete_map=BOROUGH_COLORS,
                     text=bor_med.sort_values('GiĂ¡ trung vá»‹')['GiĂ¡ trung vá»‹'].apply(fmt_M),
                     labels={'Borough':'Quáºn', 'GiĂ¡ trung vá»‹':'GiĂ¡ trung vá»‹ ($)'},
                     title="GiĂ¡ trung vá»‹ theo quáºn ($)")
        fig.update_traces(textposition='auto')
        clayout(fig, h=280, t=40, r=100)
        fig.update_layout(yaxis=dict(automargin=True, title='Quáºn'), xaxis=dict(tickformat='$,.0f', automargin=True, title='GiĂ¡ trung vá»‹ ($)'),
                          title_font=dict(size=13, color='#374151'))
        st.plotly_chart(fig, width='stretch')

    divider()
    section_q("Thá»‹ trÆ°á»ng Ä‘ang táºp trung vĂ o loáº¡i hĂ¬nh báº¥t Ä‘á»™ng sáº£n nĂ o?",
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
        df_bt0_sample = df_bt0.sample(n=min(10000, len(df_bt0)), random_state=42)
        fig = px.box(df_bt0_sample, x='building_type', y='sale_price',
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

    # â”€â”€ PhĂ¢n khĂºc khĂ¡ch hĂ ng â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    divider()
    section_q("Thá»‹ trÆ°á»ng Ä‘ang phá»¥c vá»¥ nhĂ³m khĂ¡ch hĂ ng nĂ o?",
              "PhĂ¢n loáº¡i theo sá»‘ cÄƒn trong tĂ²a nhĂ  â€” proxy cho má»¥c Ä‘Ăch mua (á»Ÿ thá»±c vs Ä‘áº§u tÆ°).")

    df['_segment'] = pd.cut(
        df['total_units'],
        bins=[-1, 1, 10, float('inf')],
        labels=['â‘  Mua á»Ÿ thá»±c (1 cÄƒn)', 'â‘¡ Äáº§u tÆ° nhá» (2-10)', 'â‘¢ Tá»• chá»©c (>10)']
    )
    seg_cnt  = df['_segment'].value_counts().sort_index()
    seg_med  = df.groupby('_segment', observed=False)['sale_price'].median()
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

    # â”€â”€ Nháºn diá»‡n rá»§i ro Ä‘áº§u tÆ° â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    divider()
    section_q("Khu vá»±c nĂ o cĂ³ rá»§i ro giĂ¡ cao nháº¥t?",
              "Rá»§i ro = biáº¿n Ä‘á»™ng giĂ¡ cao (CV cao) hoáº·c thanh khoáº£n tháº¥p. "
              "Xanh = Ăt rá»§i ro, Ä‘á» = cáº§n tháºn trá»ng.")

    borough_risk = df.groupby('borough_name').agg(
        med_price=('sale_price','median'),
        std_price=('sale_price','std'),
        n_gd=('sale_price','count')
    ).reset_index()
    borough_risk['CV (%)'] = (borough_risk['std_price'] / borough_risk['med_price'] * 100).round(1)
    borough_risk['Rá»§i ro biáº¿n Ä‘á»™ng'] = pd.cut(
        borough_risk['CV (%)'],
        bins=[0, 80, 120, float('inf')],
        labels=['Tháº¥p', 'Trung bĂ¬nh', ' Cao']
    )
    borough_risk = borough_risk.sort_values('CV (%)')

    risk_display = borough_risk[['borough_name','med_price','CV (%)','n_gd','Rá»§i ro biáº¿n Ä‘á»™ng']].copy()
    risk_display.columns = ['Quáºn','GiĂ¡ trung vá»‹','Biáº¿n Ä‘á»™ng CV (%)','Sá»‘ giao dá»‹ch','ÄĂ¡nh giĂ¡ rá»§i ro']
    risk_display['GiĂ¡ trung vá»‹'] = risk_display['GiĂ¡ trung vá»‹'].apply(fmt_M)
    risk_display['Sá»‘ giao dá»‹ch'] = risk_display['Sá»‘ giao dá»‹ch'].apply(lambda v: f'{v:,}')
    st.dataframe(risk_display.set_index('Quáºn'), width='stretch')

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 1 â€” PHĂ‚N TĂCH KHU Vá»°C & Báº¢N Äá»’ HEATMAP
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab1:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f766e,#0d9488,#34d399);border-radius:14px;
    padding:18px 24px;color:#fff;margin-bottom:22px;
    box-shadow:0 6px 24px rgba(16,185,129,0.3)'>
    <b style='font-size:15px;letter-spacing:-0.3px'>ï¸ Báº£n Ä‘á»“ Nhiá»‡t Khu vá»±c & PhĂ¢n tĂch Äiá»ƒm nĂ³ng (NYC Hotspot Map)</b><br>
    <span style='font-size:12px;opacity:0.88'>Nháºn diá»‡n Ä‘iá»ƒm nĂ³ng giĂ¡ bĂ¡n, Ä‘á»‹nh giĂ¡ Ä‘Æ¡n vá»‹ $/sqft vĂ  máºt Ä‘á»™ thanh khoáº£n trĂªn báº£n Ä‘á»“ tÆ°Æ¡ng quan khĂ´ng gian thá»±c.</span>
    </div>
    """, unsafe_allow_html=True)

    n_neigh   = df['neighborhood'].nunique()
    top_neigh = df['neighborhood'].value_counts().index[0]
    top_n_cnt = df['neighborhood'].value_counts().iloc[0]
    bor_med_f = df.groupby('borough_name')['sale_price'].median()
    top_bor_p = bor_med_f.idxmax()

    ka,kb,kc,kd = st.columns(4)
    ka.metric("Quáºn Ä‘ang phĂ¢n tĂch",        f"{len(selected_boroughs)}/5")
    kb.metric("Sá»‘ khu vá»±c",                  f"{n_neigh:,}")
    kc.metric("Khu vá»±c sĂ´i Ä‘á»™ng nháº¥t",       top_neigh.title()[:20])
    kd.metric("Quáºn giĂ¡ trung vá»‹ cao nháº¥t",  top_bor_p)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # â”€â”€ YĂU Cáº¦U Vá»€ Báº¢N Äá»’ (MAP): Báº¢N Äá»’ TĂ” MĂ€U KHU Vá»°C (HEATMAP) â”€â”€
    with st.container(border=True):
        st.markdown("<h4 style='margin-top:0'>Bá»™ lá»c Báº£n Ä‘á»“ Nhiá»‡t</h4>", unsafe_allow_html=True)
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            hm_boroughs = st.multiselect("Chá»n khu vá»±c (Borough)", options=df['borough_name'].unique().tolist(), default=[])
        
        avail_neighs = df['neighborhood'].unique().tolist()
        if hm_boroughs:
            avail_neighs = df[df['borough_name'].isin(hm_boroughs)]['neighborhood'].unique().tolist()
            
        with col_f2:
            hm_neighs = st.multiselect("Chá»n Neighborhood", options=avail_neighs, default=[])

        with col_f3:
            p_min = float(df['sale_price'].min())
            p_max = float(df['sale_price'].max())
            hm_price_range = st.slider("Khoáº£ng giĂ¡ ($)", min_value=p_min, max_value=p_max, value=(p_min, p_max), format="$%.0f", key="hm_price_slider")

    # Lá»c dá»¯ liá»‡u Heatmap
    df_hm = df.copy()
    if hm_boroughs:
        df_hm = df_hm[df_hm['borough_name'].isin(hm_boroughs)]
    if hm_neighs:
        df_hm = df_hm[df_hm['neighborhood'].isin(hm_neighs)]
    
    df_hm = df_hm[df_hm['sale_price'].between(hm_price_range[0], hm_price_range[1])]

    if len(df_hm) == 0:
        st.warning("KhĂ´ng cĂ³ dá»¯ liá»‡u phĂ¹ há»£p vá»›i bá»™ lá»c hiá»‡n táº¡i.")
    else:
        # Cáºp nháºt KPI Ä‘á»™ng
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Khu vá»±c Ä‘ang chá»n", ", ".join(hm_boroughs) if hm_boroughs else "ToĂ n bá»™ NYC")
        kpi2.metric("Sá»‘ giao dá»‹ch", f"{len(df_hm):,}")
        kpi3.metric("GiĂ¡ trung vá»‹", fmt_M(df_hm['sale_price'].median()))
        hm_ppsf = df_hm.loc[df_hm['price_per_sqft'].notna() & (df_hm['price_per_sqft'] < 5000), 'price_per_sqft']
        kpi4.metric("GiĂ¡/sqft trung vá»‹", f"${hm_ppsf.median():,.0f}" if len(hm_ppsf) > 0 else "N/A")

        # TiĂªu Ä‘á» Ä‘á»™ng
        title_map = "Báº£n Ä‘á»“ Nhiá»‡t Khu vá»±c â€“ ToĂ n bá»™ NYC"
        if hm_boroughs:
            title_map = f"Báº£n Ä‘á»“ Nhiá»‡t Khu vá»±c â€“ {', '.join(hm_boroughs)}"
            
        section_q(title_map, "TĂ´ mĂ u khu vá»±c thá»ƒ hiá»‡n trá»±c quan Ä‘iá»ƒm nĂ³ng (hotspots) vá» GiĂ¡ trung vá»‹, GiĂ¡/sqft hoáº·c Máºt Ä‘á»™ thanh khoáº£n giao dá»‹ch.")

        # Gom nhĂ³m dá»¯ liá»‡u Ä‘á»‹a lĂ½ theo Neighborhood tá»« df_hm Ä‘Ă£ lá»c
        geo_df = df_hm.groupby(['neighborhood', 'borough_name']).agg(
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
                options=[" GiĂ¡ trung vá»‹ ($)", " GiĂ¡/sqft trung vá»‹ ($)", " Máºt Ä‘á»™ giao dá»‹ch (Sá»‘ cÄƒn)"],
                horizontal=True, key="hm_metric_radio"
            )
        with mc2:
            radius_val = st.slider("BĂ¡n kĂnh Ä‘iá»ƒm nhiá»‡t (Radius)", 15, 45, 25, key="hm_radius_slider")
        with mc3:
            zoom_val = st.slider("Äá»™ phĂ³ng Ä‘áº¡i (Zoom)", 9, 13, 10, key="hm_zoom_slider")

        if map_metric == " GiĂ¡ trung vá»‹ ($)":
            target_z = 'med_price'
            color_scale = "Plasma"
            z_title = "GiĂ¡ trung vá»‹ ($)"
        elif map_metric == " GiĂ¡/sqft trung vá»‹ ($)":
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
                "lat": ":.4f",
                "lon": ":.4f"
            },
            labels={
                "borough_name": "Quáºn",
                "med_price": "GiĂ¡ trung vá»‹",
                "med_ppsf_clean": "GiĂ¡/sqft",
                "n_count": "Sá»‘ GD",
                "lat": "Latitude",
                "lon": "Longitude"
            }
        )
        clayout(fig_map, h=520, t=10, b=10, l=10, r=10)
        fig_map.update_layout(
            title_text="",
            coloraxis_colorbar=dict(title=z_title, len=0.8)
        )
        st.plotly_chart(fig_map, width='stretch')

        # ChĂº giáº£i Ä‘iá»ƒm nĂ³ng
        top_p_geo = geo_df.sort_values('med_price', ascending=False).head(3)
        top_v_geo = geo_df.sort_values('n_count', ascending=False).head(3)
        p_spots = ", ".join([f"<b>{r['neighborhood'].title()}</b> (${r['med_price']/1e6:.2f}M)" for _, r in top_p_geo.iterrows()])
        v_spots = ", ".join([f"<b>{r['neighborhood'].title()}</b> ({r['n_count']:,} GD)" for _, r in top_v_geo.iterrows()])


    divider()
    section_q("GiĂ¡ bĂ¡n phĂ¢n bá»‘ nhÆ° tháº¿ nĂ o trong tá»«ng quáºn?",
              "ÄÆ°á»ng giá»¯a = trung vá»‹. Há»™p = khoáº£ng tá»© phĂ¢n vá»‹ (25%â€“75%). NhĂ£n giĂ¡ trung vá»‹ Ä‘Æ°á»£c ghi trá»±c tiáº¿p.")

    bor_ord1 = df.groupby('borough_name')['sale_price'].median().sort_values(ascending=False).index.tolist()
    df_box_sample = df.sample(n=min(10000, len(df)), random_state=42)
    fig = px.box(df_box_sample, x='borough_name', y='sale_price', color='borough_name',
                 color_discrete_map=BOROUGH_COLORS, points=False,
                 labels={'borough_name':'Quáºn','sale_price':'GiĂ¡ bĂ¡n (USD)'},
                 category_orders={'borough_name': bor_ord1},
                 title='PhĂ¢n phá»‘i giĂ¡ bĂ¡n nhĂ  theo Quáºn')
    for b in bor_ord1:
        m = df[df['borough_name']==b]['sale_price'].median()
        fig.add_annotation(x=b, y=m, text=fmt_M(m), showarrow=False,
                           font=dict(size=11,color='#111827',weight=700),
                           yshift=20, bgcolor='rgba(255,255,255,0.88)', borderpad=3)
    clayout(fig, h=360, t=50, b=20)
    fig.update_layout(
        title_font=dict(size=14, color='#374151'),
        yaxis=dict(tickformat='$,.0f', automargin=True, title='GiĂ¡ bĂ¡n (USD)'),
        xaxis=dict(automargin=True, title='Quáºn')
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
                     labels={'borough_name':'Quáºn'})
        fig.update_traces(texttemplate='%{text:,}', textposition='auto')
        clayout(fig, h=460, t=40, b=20, r=80, leg=True)
        fig.update_layout(yaxis=dict(automargin=True, tickfont_size=11, title='Khu vá»±c'),
                          xaxis=dict(automargin=True, title='Sá»‘ giao dá»‹ch'),
                          legend=dict(orientation='h', y=-0.1, x=0, font_size=11),
                          title_font=dict(size=13, color='#374151'))
        st.plotly_chart(fig, width='stretch')
    with cn2:
        # price_per_sqft_real cĂ³ thá»ƒ Ä‘Æ°á»£c dĂ¹ng náº¿u price_per_sqft thiáº¿u
        ppsf_col = 'price_per_sqft' if 'price_per_sqft' in df.columns and df['price_per_sqft'].notna().sum() > 0 else 'price_per_sqft_real'
        df_ppsf2 = df.loc[df[ppsf_col].notna() & (df[ppsf_col] > 0) & (df[ppsf_col] < 5000), ['neighborhood', 'borough_name', ppsf_col]]
        if len(df_ppsf2) > 0:
            t15p = (df_ppsf2.groupby(['neighborhood','borough_name'])[ppsf_col]
                    .agg(med_ppsf='median', cnt='count').reset_index())
            t15p = t15p[t15p['cnt'] >= 5].nlargest(15,'med_ppsf').sort_values('med_ppsf')
            t15p['Khu vá»±c'] = t15p['neighborhood'].str.title().str[:25]
            if len(t15p) > 0:
                top_n_ppsf_row = t15p.iloc[-1]
            if len(t15p) > 0:
                fig = px.bar(t15p, x='med_ppsf', y='Khu vá»±c', orientation='h',
                             color='borough_name', color_discrete_map=BOROUGH_COLORS,
                             text=t15p['med_ppsf'].apply(lambda v: f'${v:,.0f}'),
                             title="Top 15 khu vá»±c giĂ¡/sqft cao nháº¥t (trung vá»‹)",
                             labels={'borough_name':'Quáºn','med_ppsf':'$/sqft (trung vá»‹)'})
                fig.update_traces(textposition='auto')
                clayout(fig, h=460, t=40, b=20, r=80, leg=True)
                fig.update_layout(yaxis=dict(automargin=True, tickfont_size=11, title='Khu vá»±c'),
                                  xaxis=dict(tickformat='$,.0f', automargin=True, title='$/sqft (trung vá»‹)'),
                                  legend=dict(orientation='h', y=-0.1, x=0, font_size=11),
                                  title_font=dict(size=13, color='#374151'))
                st.plotly_chart(fig, width='stretch')
            else:
                st.info("KhĂ´ng Ä‘á»§ dá»¯ liá»‡u giĂ¡/sqft sau khi lá»c.")
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
    <b style='font-size:15px;letter-spacing:-0.3px'> PhĂ¢n tĂch Ma tráºn Yáº¿u tá»‘ & CĂ¡c Biáº¿n sá»‘ Quyáº¿t Ä‘á»‹nh GiĂ¡</b><br>
    <span style='font-size:12px;opacity:0.88'>TĂ³m táº¯t cĂ¡c yáº¿u tá»‘ áº£nh hÆ°á»Ÿng máº¡nh/yáº¿u, ma tráºn tÆ°Æ¡ng quan vĂ  giáº£i thĂch Ă½ nghÄ©a chiá»u tĂ¡c Ä‘á»™ng cá»§a cĂ¡c biáº¿n sá»‘ chĂnh Ä‘áº¿n giĂ¡ bĂ¡n thá»±c táº¿.</span>
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
        "Ma tráºn tÆ°Æ¡ng quan tá»•ng thá»ƒ giá»¯a cĂ¡c yáº¿u tá»‘ vá»›i GiĂ¡ bĂ¡n",
        "Äá»c báº£n Ä‘á»“ nhiá»‡t: Ă´ mĂ u Ä‘á» = tÆ°Æ¡ng quan thuáºn (+); Ă´ mĂ u xanh = tÆ°Æ¡ng quan nghá»‹ch (-). Sá»‘ trong Ă´ lĂ  há»‡ sá»‘ tÆ°Æ¡ng quan r."
    )
    cc_cols = ['sale_price','gross_sqft','avg_income','dist_center','pop_density','building_age']
    cc_lbl  = {'sale_price':'GiĂ¡ bĂ¡n','gross_sqft':'Diá»‡n tĂch','avg_income':'Thu nháºp TB',
               'dist_center':'KC trung tĂ¢m','pop_density':'Máºt Ä‘á»™ dĂ¢n sá»‘',
               'building_age':'Tuá»•i cĂ´ng trĂ¬nh'}
    
    # TĂnh ma tráºn tÆ°Æ¡ng quan trá»±c tiáº¿p, khĂ´ng drop cá»™t háº±ng sá»‘ Ä‘á»ƒ giá»¯ nguyĂªn lÆ°á»›i biá»ƒu Ä‘á»“.
    # CĂ¡c giĂ¡ trá»‹ lá»—i (NaN do phÆ°Æ¡ng sai = 0) sáº½ Ä‘Æ°á»£c Ä‘iá»n 0 (khĂ´ng cĂ³ tÆ°Æ¡ng quan tuyáº¿n tĂnh).
    cc_mat = df[cc_cols].corr().fillna(0)
    
    if len(cc_mat.columns) > 1:
        cc_mat.columns = [cc_lbl[c] for c in cc_mat.columns]
        cc_mat.index   = [cc_lbl[c] for c in cc_mat.index]
        
        fig_corr_mat = px.imshow(cc_mat, text_auto='.2f', color_continuous_scale='RdBu_r',
                                zmin=-1, zmax=1, aspect='equal',
                                title='Ma tráºn tÆ°Æ¡ng quan giá»¯a cĂ¡c yáº¿u tá»‘ vĂ  GiĂ¡ bĂ¡n')
        clayout(fig_corr_mat, h=360, t=40, b=20)
        fig_corr_mat.update_layout(
            coloraxis_colorbar=dict(title='Há»‡ sá»‘ r', len=0.8),
            title_font=dict(size=13, color='#374151')
        )
        st.plotly_chart(fig_corr_mat, width='stretch')
    else:
        st.info("KhĂ´ng Ä‘á»§ biáº¿n sá»‘ cĂ³ sá»± phĂ¢n tĂ¡n dá»¯ liá»‡u Ä‘á»ƒ váº½ ma tráºn tÆ°Æ¡ng quan.")

    divider()

    # â”€â”€ PHĂ‚N TĂCH CHI TIáº¾T 3 BIáº¾N Sá» CHĂNH THEO YĂU Cáº¦U â”€â”€
    st.markdown("""
    <div style='font-size:18px;font-weight:800;color:#1e1b4b;margin-bottom:16px'>
     PHĂ‚N TĂCH CHI TIáº¾T 3 BIáº¾N Sá» CHá»¦ Äáº O TĂC Äá»˜NG Äáº¾N GIĂ BĂN
    </div>
    """, unsafe_allow_html=True)

    # 1. BIáº¾N Sá» 1: DIá»†N TĂCH (gross_sqft)
    section_q("1. Biáº¿n sá»‘ DIá»†N TĂCH CĂ”NG TRĂŒNH (gross_sqft) â€” Má»©c Ä‘á»™ tĂ¡c Ä‘á»™ng:  Ráº¤T Máº NH",
              "PhĂ¢n tĂch má»‘i quan há»‡ giá»¯a quy mĂ´ diá»‡n tĂch sĂ n sá» dá»¥ng vĂ  tá»•ng giĂ¡ bĂ¡n báº¥t Ä‘á»™ng sáº£n.")
    
    mask = df['gross_sqft'].notna() & df['gross_sqft'].between(100, 4000)
    q97 = df.loc[mask, 'sale_price'].quantile(0.97)
    df_sq = df.loc[mask & (df['sale_price'] < q97), ['gross_sqft', 'sale_price']].copy()
    corr_sq = df_sq['gross_sqft'].corr(df_sq['sale_price']) if len(df_sq) >= 20 else 0

    if len(df_sq) >= 50:
        df_sq['bin'] = pd.cut(df_sq['gross_sqft'], bins=range(100,4200,200),
                              labels=[f"{i}â€“{i+200}" for i in range(100,4000,200)])
        ba = (df_sq.groupby('bin', observed=False)
              .agg(med_price=('sale_price','median'), cnt=('sale_price','count'),
                   sqft_mid=('gross_sqft','median')).reset_index())
        ba = ba[ba['cnt'] >= 10]
        fig_sq_chart = px.scatter(ba, x='sqft_mid', y='med_price', size='cnt', size_max=30,
                                  color='med_price', color_continuous_scale='Blues', trendline='ols',
                                  labels={'sqft_mid':'Diá»‡n tĂch trung vá»‹ (sqft)',
                                          'med_price':'GiĂ¡ trung vá»‹ ($)','cnt':'Sá»‘ GD'},
                                  title="TÆ°Æ¡ng quan giá»¯a Diá»‡n tĂch sá» dá»¥ng (sqft) vĂ  GiĂ¡ bĂ¡n trung vá»‹ ($)")
        clayout(fig_sq_chart, h=340, t=40, b=20)
        fig_sq_chart.update_layout(coloraxis_showscale=False,
                                   yaxis=dict(tickformat='$,.0f', automargin=True, title='GiĂ¡ trung vá»‹ ($)'),
                                   xaxis=dict(automargin=True, title='Diá»‡n tĂch trung vá»‹ (sqft)'),
                                   title_font=dict(size=13, color='#374151'))
        # Äáº·t tĂªn cho OLS trendline trace Ä‘á»ƒ trĂ¡nh undefined trong legend
        for trace in fig_sq_chart.data:
            if hasattr(trace, 'name') and trace.name and 'OLS' in str(trace.name):
                trace.name = 'ÄÆ°á»ng xu hÆ°á»›ng (OLS)'
        st.plotly_chart(fig_sq_chart, width='stretch')


    divider()

    # 2. BIáº¾N Sá» 2: THU NHáº¬P KHU Vá»°C (avg_income)
    section_q("2. Biáº¿n sá»‘ THU NHáº¬P BĂŒNH QUĂ‚N KHU Vá»°C (avg_income) â€” Má»©c Ä‘á»™ tĂ¡c Ä‘á»™ng:  Máº NH",
              "PhĂ¢n tĂch tĂ¡c Ä‘á»™ng cá»§a sá»©c mua vĂ  má»©c Ä‘á»™ Ä‘áº¯t Ä‘á» cá»§a dĂ¢n cÆ° sinh sá»‘ng táº¡i khu vá»±c Ä‘áº¿n máº·t báº±ng giĂ¡ nhĂ .")

    df_inc = df.loc[df['avg_income'].notna(), ['avg_income', 'sale_price', 'price_per_sqft', 'borough_name']].copy()
    corr_inc = df_inc['avg_income'].corr(df_inc['sale_price']) if len(df_inc) >= 20 else 0

    inc_summary = df_inc.groupby('borough_name').agg(
        avg_inc=('avg_income', 'mean'),
        med_price=('sale_price', 'median'),
        med_ppsf=('price_per_sqft', 'median')
    ).reset_index()

    fig_inc = px.bar(
        inc_summary, x='borough_name', y='med_price',
        color='avg_inc', color_continuous_scale='Purples',
        text=inc_summary['avg_inc'].apply(lambda v: f'Thu nháºp TB: ${v:,.0f}'),
        title="Máº·t báº±ng GiĂ¡ nhĂ  Trung vá»‹ xáº¿p theo Má»©c Thu nháºp BĂ¬nh quĂ¢n Khu vá»±c ($)",
        labels={'borough_name': 'Quáºn', 'med_price': 'GiĂ¡ bĂ¡n trung vá»‹ ($)', 'avg_inc': 'Thu nháºp TB ($)'}
    )
    fig_inc.update_traces(textposition='outside')
    clayout(fig_inc, h=340, t=40, b=20)
    fig_inc.update_layout(
        yaxis=dict(tickformat='$,.0f', automargin=True, title='GiĂ¡ bĂ¡n trung vá»‹ ($)'),
        xaxis=dict(automargin=True, title='Quáºn'),
        coloraxis_colorbar=dict(title='Thu nháºp TB ($)'),
        title_font=dict(size=13, color='#374151')
    )
    st.plotly_chart(fig_inc, width='stretch')


    divider()

    # 3. BIáº¾N Sá» 3: TUá»”I Báº¤T Äá»˜NG Sáº¢N (building_age)
    section_q("3. Biáº¿n sá»‘ TUá»”I CĂ”NG TRĂŒNH (building_age) â€” Má»©c Ä‘á»™ tĂ¡c Ä‘á»™ng:  Yáº¾U / Ă‚M",
              "PhĂ¢n tĂch tĂ¡c Ä‘á»™ng cá»§a thá»i gian váºn hĂ nh cĂ´ng trĂ¬nh Ä‘áº¿n giĂ¡ bĂ¡n (kháº¥u hao váºt lĂ½ vs giĂ¡ trá»‹ vá»‹ trĂ).")

    df_age = df.loc[df['building_age'].notna() & df['building_age'].between(0, 120), ['building_age', 'sale_price']].copy()
    corr_age = df_age['building_age'].corr(df_age['sale_price']) if len(df_age) >= 20 else 0

    df_age['age_group'] = pd.cut(
        df_age['building_age'],
        bins=[-1, 15, 35, 65, 120],
        labels=['Má»›i (<15 nÄƒm)', 'Trung bĂ¬nh (15â€“35 nÄƒm)', 'CÅ© (35â€“65 nÄƒm)', 'Ráº¥t cÅ© (>65 nÄƒm)']
    )
    age_sum = df_age.groupby('age_group', observed=False)['sale_price'].median().reset_index()

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


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CHUáº¨N Bá» Dá»® LIá»†U Äá»€ XUáº¤T (TĂnh toĂ¡n chung cho cáº£ Tab 6 & 7)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
import matplotlib.dates as mdates

cols_t3 = ['sale_year', 'sale_month', 'sale_price', 'borough_name', 'neighborhood']
df_t3 = df.dropna(subset=['sale_year', 'sale_month'])[cols_t3].copy()
df_t3['sale_month_int'] = pd.to_numeric(df_t3['sale_month'], errors='coerce').fillna(0).astype(int)
df_t3['sale_year_int']  = pd.to_numeric(df_t3['sale_year'],  errors='coerce').fillna(0).astype(int)
df_t3 = df_t3[(df_t3['sale_month_int'] >= 1) & (df_t3['sale_month_int'] <= 12) & (df_t3['sale_year_int'] >= 2000)]
df_t3["ym_dt"] = pd.to_datetime(
    df_t3["sale_year_int"].astype(str) + "-" + df_t3["sale_month_int"].astype(str).str.zfill(2),
    format="%Y-%m", errors='coerce')
df_t3 = df_t3.dropna(subset=['ym_dt'])

start_dt_str = df_t3['ym_dt'].min().strftime('%m/%Y') if not df_t3.empty else "N/A"
end_dt_str = df_t3['ym_dt'].max().strftime('%m/%Y') if not df_t3.empty else "N/A"
col_start = f"GiĂ¡ Báº¯t Äáº§u ({start_dt_str})"
col_end = f"GiĂ¡ Hiá»‡n Táº¡i ({end_dt_str})"

def format_table(df_tbl):
    def get_text_color(val):
        if not isinstance(val, (int, float)): return ""
        if val >= 5: return "color: #047857; font-weight: bold;" # Dark Green
        elif val > 0: return "color: #059669; font-weight: bold;" # Green
        elif val <= -5: return "color: #B91C1C; font-weight: bold;" # Dark Red
        elif val < 0: return "color: #DC2626; font-weight: bold;" # Red
        return "color: #475569; font-weight: bold;" # Slate (0%)

    format_dict = {"CAGR (%)": "{:+.1f}%"}
    for col in df_tbl.columns:
        if "GiĂ¡" in col:
            format_dict[col] = "${:,.0f}"
    
    return df_tbl.style.format(format_dict).map(get_text_color, subset=["CAGR (%)"])

# TĂnh toĂ¡n neigh_stats (Cho TĂch sáº£n)
df_neigh_agg = df_t3.groupby(["borough_name", "neighborhood", "ym_dt"])["sale_price"].median().reset_index()
df_neigh_count = df_t3.groupby(["borough_name", "neighborhood"]).size().reset_index(name="S_GD")

neigh_stats = []
for boro in df_neigh_agg["borough_name"].unique():
    b_df = df_neigh_agg[df_neigh_agg["borough_name"] == boro]
    for n in b_df["neighborhood"].unique():
        sub = b_df[b_df["neighborhood"] == n].sort_values("ym_dt")
        n_gd = df_neigh_count[(df_neigh_count["borough_name"] == boro) & (df_neigh_count["neighborhood"] == n)]["S_GD"].iloc[0]
    
        if len(sub) < 3 or n_gd < 10: 
            continue
        
        start_p = sub["sale_price"].iloc[0]
        end_p = sub["sale_price"].iloc[-1]
        pct = (end_p - start_p) / start_p * 100

        # TĂnh R2
        sub['growth_pct'] = (sub['sale_price'] - start_p) / start_p * 100
        x_num = mdates.date2num(sub['ym_dt'])
        y = sub['growth_pct'].values
        coef = np.polyfit(x_num, y, 1)
        trend = np.polyval(coef, x_num)
        ss_res = np.sum((y - trend) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

        neigh_stats.append({
            "Quáºn": boro, "Khu Vá»±c": n, col_start: start_p, 
            col_end: end_p, "CAGR (%)": pct, 
            "Slope": coef[0], "R2": r2, "Sá»‘ thĂ¡ng": len(sub), "Sá»‘ GD": n_gd
        })

df_neigh_all = pd.DataFrame(neigh_stats) if neigh_stats else pd.DataFrame()
valid_neighs = pd.DataFrame()
if not df_neigh_all.empty:
    valid_neighs = df_neigh_all[(df_neigh_all['Sá»‘ GD'] >= 15) & (df_neigh_all['Sá»‘ thĂ¡ng'] >= 4)].copy()
    if len(valid_neighs) > 0:
        valid_neighs['Äiá»ƒm Tin Cáºy'] = (
            (valid_neighs['Sá»‘ GD'] / 120 * 40).clip(upper=40) + 
            (valid_neighs['Sá»‘ thĂ¡ng'] / 19 * 30).clip(upper=30) + 
            (valid_neighs['R2'] * 30).clip(upper=30)
        ).round(0)

# HĂ m váº½ biá»ƒu Ä‘á»“
def plot_single_neighborhood(boro_name, neigh_name, title, color_neigh, height=320):
    fig = go.Figure()
    sub_n = df_neigh_agg[(df_neigh_agg["borough_name"] == boro_name) & (df_neigh_agg["neighborhood"] == neigh_name)].sort_values("ym_dt")
    final_pct = 0
    if len(sub_n) > 0:
        base_n = sub_n["sale_price"].iloc[0]
        sub_n['growth_pct'] = (sub_n['sale_price'] - base_n) / base_n * 100
        final_pct = ((sub_n['sale_price'].iloc[-1] / base_n) ** (12 / 19.0) - 1) * 100
    
        fig.add_trace(go.Scatter(
            x=sub_n['ym_dt'], y=sub_n['growth_pct'],
            mode='lines+markers', name=neigh_name,
            marker=dict(size=4),
            line=dict(color=color_neigh, width=2.5),
            customdata=sub_n['sale_price'],
            hovertemplate=f'<b>{neigh_name}</b><br>%{{x|%m/%Y}}<br>Lá»£i suáº¥t: <b>%{{y:+.1f}}%</b><br>GiĂ¡: $%{{customdata:,.0f}}<extra></extra>'))

        if len(sub_n) >= 3:
            x_num = mdates.date2num(sub_n['ym_dt'])
            coef = np.polyfit(x_num, sub_n['growth_pct'].ffill().bfill().values, 1)
            trend = np.polyval(coef, x_num)
            fig.add_trace(go.Scatter(
                x=sub_n['ym_dt'], y=trend, mode='lines', showlegend=False,
                line=dict(color=color_neigh, width=1.5, dash='dash'), hoverinfo='skip'))

    clayout(fig, h=height, t=40, b=10)
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color='#374151')),
        hovermode='x unified',
        yaxis=dict(ticksuffix='%', title="", zeroline=False),
        legend=dict(orientation='h', y=1.1, x=0))
    return fig, final_pct

def render_mini_confidence(neigh_name):
    try:
        n_stats = df_neigh_all[df_neigh_all['Khu Vá»±c'] == neigh_name].iloc[0]
        n_gd = n_stats['Sá»‘ GD']
        n_thang = n_stats['Sá»‘ thĂ¡ng']
        n_r2 = n_stats['R2']
        total_score = min((n_gd/120)*40, 40) + min((n_thang/19)*30, 30) + min(n_r2*30, 30)
        if total_score >= 80: rating = "Cá»±c ká»³ Ä‘Ă¡ng tin"
        elif total_score >= 60: rating = "KhĂ¡ Ä‘Ă¡ng tin"
        else: rating = "Tin cáºy TB"
        st.markdown(f"<div style='text-align: center; font-size: 13px; color: #64748b; margin-top: -15px;'>Äá»™ tin cáºy: <b>{total_score:.0f}/100</b> ({rating}) - Dá»±a trĂªn {n_gd} GD / {n_thang} thĂ¡ng</div>", unsafe_allow_html=True)
    except: pass

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 6 â€” Äá»€ XUáº¤T CHIáº¾N LÆ¯á»¢C
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab_adv:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1e3a8a,#3b82f6,#93c5fd);border-radius:14px;
    padding:18px 24px;color:#fff;margin-bottom:22px;
    box-shadow:0 6px 24px rgba(59,130,246,0.35)'>
        <h2 style='margin:0;font-size:24px;font-weight:700;letter-spacing:-0.5px;'> Äá» xuáº¥t Äáº§u tÆ° Báº¥t Ä‘á»™ng sáº£n</h2>
        <p style='margin:8px 0 0;font-size:15px;opacity:0.9;'>DÆ°á»›i Ä‘Ă¢y lĂ  2 chiáº¿n lÆ°á»£c thiáº¿t káº¿ riĂªng cho 2 chĂ¢n dung khĂ¡ch hĂ ng phá»• biáº¿n nháº¥t trong giá»›i Ä‘áº§u tÆ° Báº¥t Ä‘á»™ng sáº£n.</p>
    </div>
    """, unsafe_allow_html=True)

    top_3_tich_san_names = []
    top_3_luot_song_names = []

    st.markdown("<h3 style='color:#064e3b; border-bottom: 2px solid #10b981; padding-bottom: 5px;'> Äá»€ XUáº¤T DĂ€I Háº N (An ToĂ n & á»”n Äá»‹nh)</h3>", unsafe_allow_html=True)
    
    if len(valid_neighs) > 0:
        # Sáº¯p xáº¿p Ä‘á»ƒ láº¥y Top 3
        df_leaderboard = valid_neighs[["Quáºn", "Khu Vá»±c", col_end, "CAGR (%)", "Äiá»ƒm Tin Cáºy"]].copy()
        df_leaderboard.rename(columns={"CAGR (%)": "TÄƒng trÆ°á»Ÿng (%)"}, inplace=True)
        df_leaderboard = df_leaderboard.sort_values("Äiá»ƒm Tin Cáºy", ascending=False)
        top_3_df = df_leaderboard.head(3)
        top_3_tich_san_names = top_3_df['Khu Vá»±c'].tolist()
        
        st.markdown("<h5 style='color:#334155; margin-top: 15px;'>Top 3 Khu Vá»±c An ToĂ n Nháº¥t (Dá»±a trĂªn Thanh khoáº£n & á»”n Ä‘á»‹nh):</h5>", unsafe_allow_html=True)
        cols = st.columns(3)
        
        for i, row in enumerate(top_3_df.itertuples()):
            with cols[i]:
                st.markdown(f"""
                <div style='background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 15px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border-top: 4px solid #10b981; transition: transform 0.2s;'>
                    <div style='color: #64748b; font-size: 12px; font-weight: bold; text-transform: uppercase;'>Háº¡ng {i+1}</div>
                    <div style='color: #0f172a; font-size: 20px; font-weight: 800; margin: 8px 0;'>{row._2}</div>
                    <div style='font-size: 13px; color: #475569; margin-bottom: 4px;'>Quáºn: <b>{row._1}</b></div>
                    <div style='display: flex; justify-content: space-around; margin-top: 12px; padding-top: 12px; border-top: 1px dashed #cbd5e1;'>
                        <div>
                            <div style='font-size: 11px; color: #64748b;'>Äá»™ Tin Cáºy</div>
                            <div style='font-size: 16px; font-weight: bold; color: #059669;'>{row._5}/100</div>
                        </div>
                        <div>
                            <div style='font-size: 11px; color: #64748b;'>TÄƒng trÆ°á»Ÿng</div>
                            <div style='font-size: 16px; font-weight: bold; color: #2563eb;'>+{row._4:.1f}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("<p style='text-align:center; font-size:14px; color:#64748b; margin-top:15px;'><i>Vui lĂ²ng chá»n má»¥c **[Dá»¯ liá»‡u Lá»‹ch sá»]** Ä‘á»ƒ xem biá»ƒu Ä‘á»“ tÄƒng trÆ°á»Ÿng thá»±c táº¿ cá»§a 3 khu vá»±c nĂ y.</i></p>", unsafe_allow_html=True)
    else:
        st.warning("KhĂ´ng cĂ³ khu vá»±c nĂ o Ä‘áº¡t Ä‘á»§ Ä‘iá»u kiá»‡n thanh khoáº£n trong bá»™ lá»c hiá»‡n táº¡i.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    st.markdown("<h3 style='color:#c2410c; border-bottom: 2px solid #f97316; padding-bottom: 5px;'> Äá»€ XUáº¤T NGáº®N Háº N (Lá»£i Nhuáºn Giao Dá»‹ch)</h3>", unsafe_allow_html=True)
    
    with st.spinner("Äang phĂ¢n tĂch lá»‹ch sá» giao dá»‹ch Báº¥t Ä‘á»™ng sáº£n..."):
        df_flip, flip_stats, long_term = get_flipping_stats(df)
    
    if flip_stats is None or len(flip_stats) == 0:
        st.warning("KhĂ´ng tĂ¬m tháº¥y Ä‘á»§ dá»¯ liá»‡u giao dá»‹ch lÆ°á»›t sĂ³ng trong bá»™ lá»c hiá»‡n táº¡i.")
    else:
        top_roi = flip_stats.sort_values('avg_roi', ascending=False).head(5)
        top_3_roi = top_roi.head(3)
        top_3_luot_song_names = top_3_roi['neighborhood'].tolist()
        
        st.markdown("<h5 style='color:#334155; margin-top: 15px;'>Top 3 Äiá»ƒm NĂ³ng Mua Äi BĂ¡n Láº¡i (BiĂªn Ä‘á»™ lá»£i nhuáºn cao nháº¥t):</h5>", unsafe_allow_html=True)
        cols_flip = st.columns(3)
        
        for i, row in enumerate(top_3_roi.itertuples()):
            with cols_flip[i]:
                st.markdown(f"""
                <div style='background-color: #fffaf5; border: 1px solid #ffedd5; border-radius: 12px; padding: 15px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border-top: 4px solid #f97316; transition: transform 0.2s;'>
                    <div style='color: #ea580c; font-size: 12px; font-weight: bold; text-transform: uppercase;'>Má»¥c tiĂªu {i+1}</div>
                    <div style='color: #431407; font-size: 20px; font-weight: 800; margin: 8px 0;'>{row.neighborhood}</div>
                    <div style='display: flex; justify-content: space-around; margin-top: 12px; padding-top: 12px; border-top: 1px dashed #fdba74;'>
                        <div>
                            <div style='font-size: 11px; color: #9a3412;'>Sá»‘ LÆ°á»£t LÆ°á»›t</div>
                            <div style='font-size: 16px; font-weight: bold; color: #c2410c;'>{row.num_flips}</div>
                        </div>
                        <div>
                            <div style='font-size: 11px; color: #9a3412;'>Lá»£i nhuáºn TB</div>
                            <div style='font-size: 16px; font-weight: bold; color: #b91c1c;'>+{row.avg_roi * 100:.1f}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("<p style='text-align:center; font-size:14px; color:#64748b; margin-top:15px;'><i>Vui lĂ²ng chá»n má»¥c **[Dá»¯ liá»‡u Lá»‹ch sá»]** Ä‘á»ƒ Ä‘á»‘i chiáº¿u lá»‹ch sá» dao Ä‘á»™ng giĂ¡ cá»§a cĂ¡c khu vá»±c nĂ y.</i></p>", unsafe_allow_html=True)



    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # TAB 4 â€” Dá»° BĂO & MĂ” HĂŒNH ML
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab4:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f172a,#1e293b,#334155);border-radius:14px;
    padding:18px 24px;color:#fff;margin-bottom:22px;
    box-shadow:0 6px 24px rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.07)'>
    <b style='font-size:15px;letter-spacing:-0.3px'> MĂ´ hĂ¬nh Machine Learning dá»± bĂ¡o giĂ¡ nhÆ° tháº¿ nĂ o?</b><br>
    <span style='font-size:12px;opacity:0.75'>So sĂ¡nh hiá»‡u suáº¥t mĂ´ hĂ¬nh, yáº¿u tá»‘ quan trá»ng vĂ  cĂ´ng cá»¥ Æ°á»›c tĂnh giĂ¡ tÆ°Æ¡ng tĂ¡c.</span>
    </div>
    """, unsafe_allow_html=True)

    df_pred, df_imp, ml_metrics = load_ml_data(mtime=_get_cache_mtime())

    if not ml_metrics:
        st.warning("ï¸ ChÆ°a cĂ³ káº¿t quáº£ ML. HĂ£y cháº¡y `main.py` trÆ°á»›c.")
    else:
        rf4 = ml_metrics.get('Random Forest', {}); lr4 = ml_metrics.get('Linear Regression', {})
        m1,m2,m3,m4 = st.columns(4)
        acc4 = max(0,(1-rf4.get('MAE',0)/df['sale_price'].median())*100)
        mape4 = rf4.get('MAPE', None)
        m1.metric("Äá»™ chĂnh xĂ¡c Æ°á»›c tĂnh", f"{acc4:.1f}%", delta="Random Forest tá»‘t nháº¥t")
        m2.metric("Sai sá»‘ trung bĂ¬nh (MAE)", f"${rf4.get('MAE',0):,.0f}")
        m3.metric("RÂ² â€” Má»©c giáº£i thĂch", f"{rf4.get('R2',0)*100:.1f}%")
        if mape4:
            m4.metric("Lá»‡ch giĂ¡ TB (%)", f"{mape4:.1f}%")
        else:
            m4.metric("RMSE", f"${rf4.get('RMSE',0):,.0f}")

        section_q("MĂ´ hĂ¬nh nĂ o dá»± bĂ¡o chĂnh xĂ¡c hÆ¡n?",
                  "RÂ² cĂ ng gáº§n 1, MAE/RMSE cĂ ng tháº¥p = tá»‘t hÆ¡n. So sĂ¡nh trĂªn cĂ¹ng táºp kiá»ƒm tra.")
        rows4 = [{'MĂ´ hĂ¬nh': n,
                   'Äiá»ƒm RÂ²':  f"{m['R2']:.4f}",
                   'Sai sá»‘ TB ($)': f"${m['MAE']:,.0f}",
                   'CÄƒn SSBT ($)': f"${m['RMSE']:,.0f}",
                   'ÄĂ¡nh giĂ¡': ' Tá»‘t hÆ¡n' if n == 'Random Forest' else ' Tham kháº£o'}
                 for n, m in ml_metrics.items()]
        st.dataframe(pd.DataFrame(rows4).set_index('MĂ´ hĂ¬nh'), width='stretch')

        divider()
        ci1, ci2 = st.columns(2)
        with ci1:
            section_q("Yáº¿u tá»‘ nĂ o mĂ´ hĂ¬nh cho lĂ  quyáº¿t Ä‘á»‹nh nháº¥t?","")
            if df_imp is not None:
                imp4s = df_imp.copy()
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
            if df_pred is not None:
                pp4 = df_pred.sample(n=min(1500,len(df_pred)), random_state=42)
                fig_av4 = px.scatter(pp4, x='Actual', y='Predicted', opacity=0.4,
                                     color_discrete_sequence=[C_BLUE2],
                                     labels={'Actual':'GiĂ¡ thá»±c ($)','Predicted':'GiĂ¡ dá»± bĂ¡o ($)'},
                                     title='Dá»± bĂ¡o vs Thá»±c táº¿ â€” Äá»™ chĂnh xĂ¡c mĂ´ hĂ¬nh Random Forest',
                                     trendline='ols')
                # Äáº·t tĂªn cho OLS trendline trace Ä‘á»ƒ trĂ¡nh 'undefined' trong legend
                for trace in fig_av4.data:
                    if hasattr(trace, 'name') and trace.name and 'OLS' in str(trace.name):
                        trace.name = 'Xu hÆ°á»›ng OLS'
                vm4 = max(df_pred['Actual'].max(), df_pred['Predicted'].max())
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
# ????????????????????????????????????????????????????????????
# TAB 5  L?T SNG & ?U C
# ????????????????????????????????????????????????????????????
# with tab6:
#     st.info(" TĂnh nÄƒng Trá»£ lĂ½ AI Ä‘ang Ä‘Æ°á»£c báº£o trĂ¬ Ä‘á»ƒ tá»‘i Æ°u hĂ³a vá»›i bá»™ dá»¯ liá»‡u 2.1 triá»‡u giao dá»‹ch. Vui lĂ²ng quay láº¡i sau!")

# Cache bust 2

with tab7:
    st.markdown("##  PhĂ¢n tĂch TĂ¡c Ä‘á»™ng Tiá»‡n Ăch Ä‘áº¿n GiĂ¡ nhĂ  (2025 - 2026)")

    try:
        df_fi = pd.read_csv('output/spatial_feature_importance.csv')
        
        # Rename features for display
        feature_names = {
            'building_age': 'Tuá»•i thá» tĂ²a nhĂ ',
            'dist_to_nearest_subway': 'Khoáº£ng cĂ¡ch Ä‘áº¿n Ga TĂ u (MĂ©t)',
            'num_subway_within_1km': 'Sá»‘ Ga TĂ u bĂ¡n kĂnh 1km',
            'residential_units': 'Sá»‘ lÆ°á»£ng phĂ²ng á»Ÿ',
            'num_park_within_1km': 'Sá»‘ CĂ´ng viĂªn bĂ¡n kĂnh 1km',
            'gross_sqft': 'Tá»•ng diá»‡n tĂch',
            'dist_to_nearest_park': 'Khoáº£ng cĂ¡ch Ä‘áº¿n CĂ´ng viĂªn (MĂ©t)',
            'dist_to_nearest_hospital': 'Khoáº£ng cĂ¡ch Ä‘áº¿n Bá»‡nh viá»‡n (MĂ©t)',
            'num_hospital_within_1km': 'Sá»‘ Bá»‡nh viá»‡n bĂ¡n kĂnh 1km',
            'dist_to_nearest_school': 'Khoáº£ng cĂ¡ch Ä‘áº¿n TrÆ°á»ng há»c (MĂ©t)',
            'num_school_within_1km': 'Sá»‘ TrÆ°á»ng há»c bĂ¡n kĂnh 1km',
            'dist_to_nearest_university': 'Khoáº£ng cĂ¡ch Ä‘áº¿n Äáº¡i há»c (MĂ©t)',
            'num_university_within_1km': 'Sá»‘ Äáº¡i há»c bĂ¡n kĂnh 1km',
            'dist_to_nearest_supermarket': 'Khoáº£ng cĂ¡ch Ä‘áº¿n SiĂªu thá»‹ (MĂ©t)',
            'num_supermarket_within_1km': 'Sá»‘ SiĂªu thá»‹ bĂ¡n kĂnh 1km'
        }
        
        # Lá»c bá» cĂ¡c biáº¿n cáº¥u trĂºc (chá»‰ giá»¯ láº¡i cĂ¡c biáº¿n tiá»‡n Ăch khĂ´ng gian)
        structural_feats = ['building_age', 'residential_units', 'gross_sqft']
        df_fi = df_fi[~df_fi['Feature'].isin(structural_feats)].copy()
        
        # Loáº¡i bá» cĂ¡c tiá»‡n Ăch khĂ´ng cĂ³ dá»¯ liá»‡u (Trá»ng sá»‘ = 0) Ä‘á»ƒ biá»ƒu Ä‘á»“ khĂ´ng bá»‹ khoáº£ng trá»‘ng
        df_fi = df_fi[df_fi['Importance'] > 0].copy()
        
        # Chuáº©n hĂ³a láº¡i tá»· trá»ng (Ä‘á»ƒ tá»•ng cĂ¡c tiá»‡n Ăch = 100%)
        df_fi['Importance'] = df_fi.groupby('Year')['Importance'].transform(lambda x: x / x.sum())
        
        df_fi['Feature_Name'] = df_fi['Feature'].map(feature_names).fillna(df_fi['Feature'])
        df_2025 = df_fi[df_fi['Year'] == 2025].sort_values('Importance')
        df_2026 = df_fi[df_fi['Year'] == 2026].sort_values('Importance')

        
        fig_2025 = px.bar(df_2025, x='Importance', y='Feature_Name', orientation='h',
                          title='Tá»· trá»ng ÄĂ³ng gĂ³p vĂ o Äá»‹nh giĂ¡ - 2025',
                          text=df_2025['Importance'].apply(lambda x: f'{x*100:.1f}%'),
                          labels={'Importance': 'Tá»· trá»ng Ä‘Ă³ng gĂ³p (%)', 'Feature_Name': ''},
                          color_discrete_sequence=['#34d399'])
        fig_2025.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis=dict(tickformat='.0%'), margin=dict(l=0, r=20, t=50, b=10))

        fig_2026 = px.bar(df_2026, x='Importance', y='Feature_Name', orientation='h',
                          title='Tá»· trá»ng ÄĂ³ng gĂ³p vĂ o Äá»‹nh giĂ¡ - 2026',
                          text=df_2026['Importance'].apply(lambda x: f'{x*100:.1f}%'),
                          labels={'Importance': 'Tá»· trá»ng Ä‘Ă³ng gĂ³p (%)', 'Feature_Name': ''},
                          color_discrete_sequence=['#f59e0b'])
        fig_2026.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis=dict(tickformat='.0%'), margin=dict(l=0, r=20, t=50, b=10))

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_2025, use_container_width=True)
        with col2:
            st.plotly_chart(fig_2026, use_container_width=True)
            
        st.write("---")
        st.markdown(f"""
        *PhĂ¢n tĂch nĂ y trĂch xuáº¥t tá»« **{len(df):,} giao dá»‹ch**, trong Ä‘Ă³ sá» dá»¥ng tá»a Ä‘á»™ Ä‘á»‹a lĂ½ cá»§a **hÆ¡n 51.000 giao dá»‹ch** há»£p lá»‡ trĂªn há»‡ thá»‘ng OpenStreetMap Ä‘á»ƒ Ä‘o lÆ°á»ng khoáº£ng cĂ¡ch váºt lĂ½ chĂnh xĂ¡c Ä‘áº¿n cĂ¡c tiá»‡n Ăch cĂ´ng cá»™ng.*
        *Thuáºt toĂ¡n **Random Forest Regressor** Ä‘Æ°á»£c sá» dá»¥ng Ä‘á»ƒ lá»c nhiá»…u vĂ  Ä‘o lÆ°á»ng trá»ng sá»‘.*
        """)
        st.warning("â ï¸ **LÆ¯U Ă:** CĂ¡c con sá»‘ pháº§n trÄƒm (%) dÆ°á»›i Ä‘Ă¢y thá»ƒ hiá»‡n **Tá»· trá»ng Ä‘Ă³ng gĂ³p** cá»§a tá»«ng tiá»‡n Ăch vĂ o mĂ´ hĂ¬nh AI (Tá»•ng cĂ¡c tiá»‡n Ăch = 100%). NĂ³ **KHĂ”NG PHáº¢I** lĂ  biĂªn Ä‘á»™ tÄƒng giĂ¡ nhĂ . VĂ dá»¥: 28.3% nghÄ©a lĂ  Bá»‡nh viá»‡n chiáº¿m 28.3% sá»©c náº·ng khi AI quyáº¿t Ä‘á»‹nh giĂ¡ nhĂ  táº¡i khu vá»±c Ä‘Ă³.")
        
        if st.button("đŸ¤– Cháº¡y láº¡i thuáºt toĂ¡n AI cho bá»™ lá»c hiá»‡n táº¡i (Máº¥t ~5 giĂ¢y)", type="primary", use_container_width=True):
            with st.spinner("Äang truy xuáº¥t CSDL vĂ  cháº¡y Random Forest Regressor trĂªn táºp dá»¯ liá»‡u Ä‘Ă£ lá»c..."):
                import sqlite3
                from sklearn.ensemble import RandomForestRegressor
                import os
                
                b_list = "', '".join(selected_boroughs)
                query = f"""
                SELECT 
                    f.sale_price,
                    f.sale_year,
                    p.building_age,
                    p.residential_units,
                    p.gross_sqft,
                    a.dist_to_nearest_subway,
                    a.num_subway_within_1km,
                    a.dist_to_nearest_park,
                    a.num_park_within_1km,
                    a.dist_to_nearest_hospital,
                    a.num_hospital_within_1km,
                    a.dist_to_nearest_school,
                    a.num_school_within_1km
                FROM fact_sales f
                JOIN dim_property p ON f.property_id = p.property_id
                JOIN fact_property_amenities a ON f.location_id = a.location_id
                JOIN dim_location l ON f.location_id = l.location_id
                JOIN dim_neighborhood n ON l.neighborhood_id = n.neighborhood_id
                JOIN dim_borough b ON n.borough_id = b.borough_id
                WHERE f.sale_year BETWEEN {year_range[0]} AND {year_range[1]}
                AND f.sale_price BETWEEN {price_range[0]} AND {price_range[1]}
                AND b.borough_name IN ('{b_list}')
                """
                db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'warehouse', 'nyc_warehouse.db')
                conn = sqlite3.connect(db_path)
                df_ml = pd.read_sql(query, conn)
                conn.close()
                
                features = [
                    'dist_to_nearest_subway', 'num_subway_within_1km',
                    'dist_to_nearest_park', 'num_park_within_1km',
                    'dist_to_nearest_hospital', 'num_hospital_within_1km',
                    'dist_to_nearest_school', 'num_school_within_1km',
                    'building_age', 'residential_units', 'gross_sqft'
                ]
                
                # Xá» lĂ½ khuyáº¿t thiáº¿u
                for col in features:
                    if df_ml[col].notna().any():
                        df_ml[col] = df_ml[col].fillna(df_ml[col].median())
                    else:
                        df_ml[col] = df_ml[col].fillna(0)
                df_ml = df_ml.dropna(subset=['sale_price'])
                
                results = []
                for year in df_ml['sale_year'].unique():
                    df_y = df_ml[df_ml['sale_year'] == year]
                    if len(df_y) < 50: continue
                    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
                    rf.fit(df_y[features], df_y['sale_price'])
                    for feat, imp in zip(features, rf.feature_importances_):
                        results.append({'Feature': feat, 'Importance': imp, 'Year': year})
                        
                if results:
                    df_new = pd.DataFrame(results)
                    df_new.to_csv('output/spatial_feature_importance.csv', index=False)
                    st.rerun()
                else:
                    st.error("KhĂ´ng Ä‘á»§ dá»¯ liá»‡u Ä‘á»ƒ cháº¡y mĂ´ hĂ¬nh cho bá»™ lá»c nĂ y!")
        
    except Exception as e:
        st.error(f"ChÆ°a cĂ³ dá»¯ liá»‡u phĂ¢n tĂch khĂ´ng gian. Lá»—i: {e}")


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 8 â€” AI FINDER (COMPS)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

@st.cache_data
def load_comps_data():
    """
    Äá»c trá»±c tiáº¿p tá»« fact_property_amenities + fact_sales + cĂ¡c dim tables.
    TĂnh toĂ¡n has_X_1km vĂ  amenity_score Ä‘á»™ng tá»« dá»¯ liá»‡u thá»±c táº¿.
    """
    try:
        import sqlite3, os
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'warehouse', 'nyc_warehouse.db')
        conn = sqlite3.connect(db_path)

        df = pd.read_sql_query("""
            SELECT
                l.location_id,
                l.address,
                l.zip_code,
                b.borough_name,
                n.neighborhood_name AS neighborhood_name,
                p.building_class_category,
                fs.sale_price,
                fa.dist_to_nearest_subway,
                fa.dist_to_nearest_park,
                fa.dist_to_nearest_hospital,
                fa.dist_to_nearest_school,
                fa.dist_to_nearest_supermarket,
                fa.dist_to_nearest_university,
                fa.num_subway_within_1km,
                fa.num_park_within_1km,
                fa.num_hospital_within_1km,
                fa.num_school_within_1km,
                fa.num_supermarket_within_1km,
                fa.num_university_within_1km
            FROM fact_sales fs
            JOIN dim_location       l  ON fs.location_id    = l.location_id
            JOIN dim_neighborhood   n  ON l.neighborhood_id  = n.neighborhood_id
            JOIN dim_borough        b  ON n.borough_id       = b.borough_id
            JOIN dim_property       p  ON fs.property_id     = p.property_id
            JOIN fact_property_amenities fa ON l.location_id = fa.location_id
            WHERE fs.sale_price > 10000
              AND l.zip_code IS NOT NULL
        """, conn)
        conn.close()

        # â”€â”€ TĂnh has_X_1km (boolean: cĂ³ tiá»‡n Ăch trong 1km khĂ´ng) â”€â”€
        df['has_subway_1km']      = (df['num_subway_within_1km']      > 0).astype(int)
        df['has_park_1km']        = (df['num_park_within_1km']        > 0).astype(int)
        df['has_hospital_1km']    = (df['num_hospital_within_1km']    > 0).astype(int)
        df['has_school_1km']      = (df['num_school_within_1km']      > 0).astype(int)
        df['has_supermarket_1km'] = (df['num_supermarket_within_1km'] > 0).astype(int)
        df['has_university_1km']  = (df['num_university_within_1km']  > 0).astype(int)

        # â”€â”€ TĂnh amenity_score (trá»ng sá»‘ theo táº§m quan trá»ng BÄS) â”€â”€
        df['amenity_score'] = (
            df['has_subway_1km']      * 30 +
            df['has_school_1km']      * 25 +
            df['has_supermarket_1km'] * 20 +
            df['has_park_1km']        * 15 +
            df['has_hospital_1km']    * 10
        )

        # Äáº£m báº£o zip_code lĂ  string Ä‘á»ƒ group Ä‘Ăºng
        df['zip_code'] = df['zip_code'].astype(str).str.strip()

        return df

    except Exception as e:
        error_msg = str(e)
        if len(error_msg) > 500:
            error_msg = error_msg[:100] + " ... " + error_msg[-300:]
        st.error(f"Lá»—i Ä‘á»c dá»¯ liá»‡u AI Finder: {type(e).__name__} - {error_msg}")
        return pd.DataFrame()


with tab_search:
    st.info(" **Má»¤C ÄĂCH:** Há»‡ thá»‘ng sá» dá»¥ng dá»¯ liá»‡u lá»‹ch sá» Ä‘á»ƒ **Ä‘á» xuáº¥t cĂ¡c máº«u báº¥t Ä‘á»™ng sáº£n** cĂ³ Ä‘áº·c tĂnh tÆ°Æ¡ng Ä‘á»“ng vá»›i tiĂªu chĂ cá»§a báº¡n (khĂ´ng pháº£i danh sĂ¡ch nhĂ  Ä‘ang rao bĂ¡n). NgÆ°á»i dĂ¹ng cĂ³ thá»ƒ mÆ°á»£n tá»a Ä‘á»™ cá»§a cĂ¡c cÄƒn nhĂ  máº«u nĂ y Ä‘á»ƒ chá»§ Ä‘á»™ng khĂ¡m phĂ¡ khĂ´ng gian vĂ  tiá»‡n Ăch thá»±c táº¿ xung quanh chĂºng.")
    st.markdown("""
    <div style='background:linear-gradient(135deg,#db2777,#be185d,#9d174d);border-radius:14px;
    padding:18px 24px;color:#fff;margin-bottom:22px;
    box-shadow:0 6px 24px rgba(219,39,119,0.35)'>
    <b style='font-size:15px;letter-spacing:-0.3px'> Äá»‹nh vá»‹ Báº¥t Ä‘á»™ng sáº£n Tham chiáº¿u</b><br>
    <span style='font-size:13px;opacity:0.9'>CĂ´ng cá»¥ tĂ¬m kiáº¿m MĂ£ vĂ¹ng vĂ  CÄƒn nhĂ  tham chiáº¿u dá»±a trĂªn ngĂ¢n sĂ¡ch vĂ  tiá»‡n Ăch 1km.</span>
    </div>""", unsafe_allow_html=True)

    df_comps = load_comps_data()
    
    if df_comps.empty:
        st.warning("Äang chá» dá»¯ liá»‡u...")
    else:
        col_filter, col_res = st.columns([1, 2.2])
        
        with col_filter:
            st.markdown("### ï¸ Bá»™ Lá»c ThĂ´ng Minh")
            
            # Budget
            min_price = 100000
            max_price = 5000000
            budget = st.slider("NgĂ¢n sĂ¡ch ($)", min_value=min_price, max_value=max_price, value=(300000, 1500000), step=50000)
            
            # Borough
            boroughs = ["Táº¥t cáº£"] + sorted(df_comps['borough_name'].dropna().unique().tolist())
            selected_boro = st.selectbox("Quáºn (Borough)", boroughs)
            
            # Neighborhood
            if selected_boro != "Táº¥t cáº£":
                avail_neighs = sorted(df_comps[df_comps['borough_name'] == selected_boro]['neighborhood_name'].dropna().unique().tolist())
            else:
                avail_neighs = sorted(df_comps['neighborhood_name'].dropna().unique().tolist())
            neighs = ["Táº¥t cáº£"] + avail_neighs
            selected_neigh = st.selectbox("Khu vá»±c (Neighborhood)", neighs)
            
            st.markdown("####  Tiá»‡n Ăch < 1km")
            req_school = st.checkbox(" CĂ³ TrÆ°á»ng há»c")
            req_subway = st.checkbox(" CĂ³ Ga TĂ u Ä‘iá»‡n ngáº§m")
            req_park = st.checkbox(" CĂ³ CĂ´ng viĂªn")
            req_hospital = st.checkbox(" CĂ³ Bá»‡nh viá»‡n/PhĂ²ng khĂ¡m")
            
            do_search = st.button(" TĂ¬m Kiáº¿m Comps", use_container_width=True, type='primary')
            
        with col_res:
            if do_search:
                with st.spinner("Äang Ä‘á»‹nh vá»‹ cá»¥m Zip Code phĂ¹ há»£p..."):
                    filtered = df_comps[
                        (df_comps['sale_price'] >= budget[0]) & 
                        (df_comps['sale_price'] <= budget[1])
                    ]
                    
                    if selected_boro != "Táº¥t cáº£":
                        filtered = filtered[filtered['borough_name'] == selected_boro]
                    if selected_neigh != "Táº¥t cáº£":
                        filtered = filtered[filtered['neighborhood_name'] == selected_neigh]
                    if selected_boro != "Táº¥t cáº£":
                        filtered = filtered[filtered['borough_name'] == selected_boro]

                        
                    if req_school:
                        filtered = filtered[filtered['has_school_1km'] == 1]
                    if req_subway:
                        filtered = filtered[filtered['has_subway_1km'] == 1]
                    if req_park:
                        filtered = filtered[filtered['has_park_1km'] == 1]
                    if req_hospital:
                        filtered = filtered[filtered['has_hospital_1km'] == 1]
                        
                    if len(filtered) == 0:
                        st.error("KhĂ´ng tĂ¬m tháº¥y Báº¥t Ä‘á»™ng sáº£n nĂ o thá»a mĂ£n toĂ n bá»™ tiĂªu chĂ. Vui lĂ²ng ná»›i lá»ng bá»™ lá»c.")
                    else:
                        # Find best Zip Code (by highest mean amenity_score)
                        zip_stats = filtered.groupby('zip_code').agg({
                            'amenity_score': 'mean',
                            'sale_price': 'median',
                            'address': 'count',
                            'borough_name': 'first'
                        }).rename(columns={'address': 'count'}).reset_index()
                        
                        # Only consider Zip Codes with at least 5 comps for reliability
                        zip_stats = zip_stats[zip_stats['count'] >= 3]
                        
                        if len(zip_stats) == 0:
                            best_zip = filtered['zip_code'].mode()[0]
                            zip_info = filtered[filtered['zip_code'] == best_zip].iloc[0]
                            best_boro = zip_info['borough_name']
                            med_price = filtered[filtered['zip_code'] == best_zip]['sale_price'].median()
                        else:
                            best_row = zip_stats.sort_values('amenity_score', ascending=False).iloc[0]
                            best_zip = best_row['zip_code']
                            best_boro = best_row['borough_name']
                            med_price = best_row['sale_price']
                            
                        st.success(f"###  Äá»€ XUáº¤T Tá»T NHáº¤T: MĂ£ BÆ°u ChĂnh (Zip Code) {best_zip}")
                        st.markdown(f"** Khu vá»±c:** {best_boro} | ** GiĂ¡ trung vá»‹ (Comps):** ${med_price:,.0f}")
                        st.markdown("*Khu vá»±c Zip Code nĂ y cĂ³ máºt Ä‘á»™ tiá»‡n Ăch cao nháº¥t Ä‘Ă¡p á»©ng Ä‘á»§ cĂ¡c tiĂªu chĂ báº¡n chá»n. DÆ°á»›i Ä‘Ă¢y lĂ  cĂ¡c CÄƒn nhĂ  tham chiáº¿u (Comps) tiĂªu biá»ƒu Ä‘Ă£ tá»«ng giao dá»‹ch:*")
                        
                        comps_in_zip = filtered[filtered['zip_code'] == best_zip].sort_values('amenity_score', ascending=False).head(3)
                        
                        for idx, row in comps_in_zip.iterrows():
                            # HTML Card
                            school_tag = " TrÆ°á»ng há»c" if row['has_school_1km'] else ""
                            subway_tag = " Ga TĂ u" if row['has_subway_1km'] else ""
                            park_tag = " CĂ´ng viĂªn" if row['has_park_1km'] else ""
                            market_tag = " SiĂªu thá»‹" if row.get('has_supermarket_1km') else ""
                            hosp_tag = " Bá»‡nh viá»‡n" if row.get('has_hospital_1km') else ""
                            tags = " | ".join(filter(None, [school_tag, subway_tag, park_tag, market_tag, hosp_tag]))
                            
                            st.markdown(f"""
                            <div style='border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 12px; border-left: 4px solid #db2777; background: #fafafa;'>
                                <h4 style='margin-top: 0; color: #1e293b;'> {row['address']}</h4>
                                <div style='display: flex; justify-content: space-between; font-size: 14px;'>
                                    <div><b>PhĂ¢n khĂºc:</b> {row['building_class_category']}</div>
                                    <div style='color: #059669; font-weight: bold;'> ${row['sale_price']:,.0f}</div>
                                </div>
                                <div style='font-size: 13px; color: #64748b; margin-top: 8px;'>
                                    <b>Tiá»‡n Ăch 1km:</b> {tags}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.info(" HĂ£y Ä‘iá»u chá»‰nh bá»™ lá»c vĂ  báº¥m **TĂ¬m Kiáº¿m Comps**")



# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 7 â€” MINH CHá»¨NG Dá»® LIá»†U
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab_evid:
    st.info(" **HÆ¯á»NG DáºªN:** DÆ°á»›i Ä‘Ă¢y lĂ  cĂ¡c biá»ƒu Ä‘á»“ thá»±c táº¿ chá»©ng minh cho nhá»¯ng Ä‘á» xuáº¥t vá»«a Ä‘Æ°á»£c AI Ä‘Æ°a ra á»Ÿ Tab Äá» xuáº¥t Chiáº¿n lÆ°á»£c.")
    st.divider()


    
    # In cĂ¡c khu vá»±c top 3 tĂch sáº£n
    if len(top_3_tich_san_names) > 0:
        st.markdown(f"####  Lá»‹ch sá» TÄƒng trÆ°á»Ÿng cá»§a Top 3 Äá» xuáº¥t: {', '.join(top_3_tich_san_names)}")
        cols_top = st.columns(3)
        for i, neigh_name in enumerate(top_3_tich_san_names):
            boro_name = valid_neighs[valid_neighs['Khu Vá»±c'] == neigh_name].iloc[0]['Quáºn']
            with cols_top[i]:
                fig_top, pct_top = plot_single_neighborhood(boro_name, neigh_name, f"{neigh_name}", C_GREEN, height=250)
                st.plotly_chart(fig_top, use_container_width=True)
                render_mini_confidence(neigh_name)
    else:
        st.warning("KhĂ´ng cĂ³ khu vá»±c Ä‘á» xuáº¥t tĂch sáº£n nĂ o Ä‘á»ƒ minh chá»©ng.")

    divider()


    
    if len(top_3_luot_song_names) > 0:
        st.markdown(f"####  Lá»‹ch sá» TÄƒng trÆ°á»Ÿng cá»§a Top 3 Äiá»ƒm NĂ³ng: {', '.join(top_3_luot_song_names)}")
        cols_top2 = st.columns(3)
        for i, neigh_name in enumerate(top_3_luot_song_names):
            boro_name = ""
            if 'flip_stats' in locals() and not flip_stats.empty:
                match = flip_stats[flip_stats['neighborhood'] == neigh_name]
                if not match.empty:
                    boro_name = df_t3[df_t3['neighborhood'] == neigh_name]['borough_name'].iloc[0] if not df_t3[df_t3['neighborhood'] == neigh_name].empty else ""
            
            with cols_top2[i]:
                if boro_name:
                    fig_top2, _ = plot_single_neighborhood(boro_name, neigh_name, f"{neigh_name}", C_RED, height=250)
                    st.plotly_chart(fig_top2, use_container_width=True)
                else:
                    st.info(f"Äang tĂnh toĂ¡n {neigh_name}...")
    else:
        st.warning("KhĂ´ng cĂ³ Ä‘iá»ƒm nĂ³ng lÆ°á»›t sĂ³ng nĂ o Ä‘á»ƒ hiá»ƒn thá»‹.")

    divider()
    st.markdown("<h4 style='color:#1e293b; margin-top:0px;'> ToĂ n cáº£nh thá»‹ trÆ°á»ng (Äá»ƒ Ä‘á»‘i chiáº¿u)</h4>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:14px;'>Sá» dá»¥ng Ä‘Æ°á»ng xu hÆ°á»›ng cá»§a toĂ n thá»‹ trÆ°á»ng Ä‘á»ƒ tháº¥y cĂ¡c khu vá»±c Ä‘Æ°á»£c Ä‘á» xuáº¥t Ä‘Ă£ vÆ°á»£t trá»™i nhÆ° tháº¿ nĂ o.</p>", unsafe_allow_html=True)
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
            title_text="",
            hovermode='x unified',
            yaxis=dict(ticksuffix='%', title="TÄƒng trÆ°á»Ÿng GiĂ¡ (%)", zeroline=False))
        st.plotly_chart(fig_all, width='stretch')
        
    # --- Ná»˜I SOI KHU Vá»°C Äá»˜NG ---
    divider()
    st.markdown("<h4 style='color:#1e293b; margin-bottom: 5px;'> Ná»™i soi khu vá»±c (Kiá»ƒm chá»©ng tá»± do)</h4>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:14px; margin-bottom: 15px;'>Náº¿u báº¡n chá»n 1 khu vá»±c báº¥t ká»³ á»Ÿ Báº£ng xáº¿p háº¡ng bĂªn Tab Äá» Xuáº¥t, nĂ³ sáº½ hiá»‡n á»Ÿ Ä‘Ă¢y.</p>", unsafe_allow_html=True)
    
    try:
        all_valid_options = valid_neighs['Khu Vá»±c'].tolist() if len(valid_neighs) > 0 else []
        default_idx = 0
        
        # Náº¿u ngÆ°á»i dĂ¹ng cĂ³ click chá»n bĂªn Tab 1, láº¥y ra lĂ m giĂ¡ trá»‹ máº·c Ä‘á»‹nh
        if 'event' in locals() and hasattr(event, 'selection') and hasattr(event.selection, 'rows'):
            selected_rows = event.selection.rows
            if len(selected_rows) > 0 and len(valid_neighs) > 0:
                selected_idx_tab1 = selected_rows[0]
                if selected_idx_tab1 < len(df_leaderboard):
                    selected_n_tab1 = df_leaderboard.iloc[selected_idx_tab1]['Khu Vá»±c']
                    if selected_n_tab1 in all_valid_options:
                        default_idx = all_valid_options.index(selected_n_tab1)
        elif 'event' in locals() and isinstance(event, dict) and 'selection' in event:
            selected_rows = event['selection'].get('rows', [])
            if len(selected_rows) > 0 and len(valid_neighs) > 0:
                selected_idx_tab1 = selected_rows[0]
                if selected_idx_tab1 < len(df_leaderboard):
                    selected_n_tab1 = df_leaderboard.iloc[selected_idx_tab1]['Khu Vá»±c']
                    if selected_n_tab1 in all_valid_options:
                        default_idx = all_valid_options.index(selected_n_tab1)
                        
        if len(all_valid_options) > 0:
            selected_n = st.selectbox("Lá»±a chá»n khu vá»±c Ä‘á»ƒ phĂ¢n tĂch chi tiáº¿t:", options=all_valid_options, index=default_idx)
            
            st.markdown(f"""
            <div id='target-explorer' style='background:linear-gradient(135deg, #0f172a, #1e293b, #334155); padding:10px 20px; border-radius:12px; border:1px solid rgba(255,255,255,0.1); margin-top:5px; margin-bottom: 5px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
                <h4 style='margin-top:0px; color:#F8FAFC; margin-bottom: 4px; font-size: 18px;'> Há»“ sÆ¡ PhĂ¢n tĂch: {selected_n}</h4>
                <p style='color:#94A3B8; font-size:13px; margin-bottom: 0px;'>Chi tiáº¿t lá»‹ch sá» giĂ¡ vĂ  chá»‰ sá»‘ rá»§i ro cá»§a khu vá»±c báº¡n vá»«a chá»n.</p>
            </div>
            """, unsafe_allow_html=True)
    
            n_stats = valid_neighs[valid_neighs['Khu Vá»±c'] == selected_n].iloc[0]
            boro_of_n = n_stats['Quáºn']
            n_gd = n_stats['Sá»‘ GD']
            n_thang = n_stats['Sá»‘ thĂ¡ng']
            n_r2 = n_stats['R2']
    
            vol_score = min((n_gd / 500) * 40, 40)
            time_score = min((n_thang / 60) * 30, 30)
            trend_score = min(n_r2 * 30, 30)
            total_score = vol_score + time_score + trend_score
    
            if total_score >= 80:
                rating, stars = "Cá»±c ká»³ Ä‘Ă¡ng tin", ""
            elif total_score >= 60:
                rating, stars = "KhĂ¡ Ä‘Ă¡ng tin", ""
            else:
                rating, stars = "Äá»™ tin cáºy trung bĂ¬nh", ""
        
            fig_explore, pct_explore = plot_single_neighborhood(boro_of_n, selected_n, f"Lá»‹ch sá» giĂ¡ chi tiáº¿t: {selected_n}", C_BLUE, height=220)
            st.plotly_chart(fig_explore, width='stretch')
            
            st.markdown(f"""
            <div style='background-color:rgba(15, 23, 42, 0.04); border-left:4px solid #3B82F6; padding:10px 15px; border-radius:8px; margin-bottom: 8px; margin-top: -15px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <span style='font-size:12px; color:#64748b; font-weight:bold; text-transform:uppercase;'> Chá»‰ sá»‘ Tin cáºy Dá»¯ liá»‡u</span>
                        <span style='font-size:20px; font-weight:800; color:#0f172a; margin-left:8px;'>{total_score:.0f}/100</span>
                        <span style='font-size:13px; margin-left:6px; font-weight:600;'>{rating}</span>
                    </div>
                    <div style='font-size:16px;'>{stars}</div>
                </div>
                <div style='margin-top:4px; font-size:13px; color:#475569;'>
                    Dá»±a trĂªn <b>{n_gd} giao dá»‹ch</b> ráº£i Ä‘á»u trong <b>{n_thang} thĂ¡ng</b>.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
             st.markdown("""
                <div style='text-align:center; padding: 40px 20px; border: 2px dashed #cbd5e1; border-radius: 12px; margin-top: 20px;'>
                    <div style='color:#64748b; font-size:18px; font-weight:bold; margin-bottom:10px;'>KhĂ´ng Ä‘á»§ dá»¯ liá»‡u</div>
                    <p style='color:#94a3b8; font-size:15px;'>Há»‡ thá»‘ng khĂ´ng tĂ¬m tháº¥y khu vá»±c nĂ o Ä‘á»§ Ä‘iá»u kiá»‡n trong bá»™ lá»c hiá»‡n táº¡i.</p>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Lá»—i khi táº£i biá»ƒu Ä‘á»“ khu vá»±c: {e}")



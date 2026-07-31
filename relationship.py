"""
relationship.py
===============
Mô hình quan hệ cơ sở dữ liệu dự án NYC Real Estate Analytics.
Kiến trúc: Star-Schema (Data Warehouse) — 5 bảng Dimension + 1 bảng Fact.

Chạy:
    python relationship.py
"""

import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# ═══════════════════════════════════════════════════════════════════
# SƠ ĐỒ KIẾN TRÚC TỔNG THỂ (Data Pipeline)
# ═══════════════════════════════════════════════════════════════════
PIPELINE_DIAGRAM = """
================================================================================
           KIẾN TRÚC DATA PIPELINE — NYC Real Estate Analytics
================================================================================

  [WEB / API]                    [Python Scripts]            [Lưu trữ]
  ─────────────                  ────────────────            ──────────
  NYC Open Data  ──► scraper.py ──►  data/Data crawl/       (Data Lake)
  NYPD / Census                      Crawl_data_NYC.csv
  OpenStreetMap                           │
                                          │ preprocess.py
                                          ▼
                                   data/data clean/          (Data Lake Sạch)
                                   Dulieu_Cleaned.csv
                                          │
                                          │ etl_to_sqlite.py
                                          ▼
                                   data/warehouse/           (Data Warehouse)
                                   nyc_warehouse.db  ◄────── STAR-SCHEMA
                                          │
                                          │ SQL Queries
                                          ▼
                                    src/dashboard.py         (Presentation)
                                    (Streamlit App)

================================================================================
"""

# ═══════════════════════════════════════════════════════════════════
# SƠ ĐỒ STAR-SCHEMA (ASCII ERD)
# ═══════════════════════════════════════════════════════════════════
ASCII_ERD = """
================================================================================
             MÔ HÌNH STAR-SCHEMA — SQLite Data Warehouse (3NF)
================================================================================

                   ┌─────────────────────┐
                   │   dim_social_metrics │
                   │─────────────────────│
                   │ PK social_id        │
                   │ FK borough_id       │
                   │    pop_density      │
                   │    avg_income       │
                   │    gdp_local        │
                   │    dist_center      │
                   │    amenity_score    │
                   └──────────┬──────────┘
                              │ N:1
                              │
   ┌─────────────┐      ┌─────▼────────────────────────┐
   │ dim_property│      │           fact_sales          │     ┌──────────────┐
   │─────────────│      │──────────────────────────────│     │ dim_location  │
   │ PK prop_id  │      │ PK sale_id                   │     │──────────────│
   │ class_categ.│      │ FK location_id  ─────────────┼────►│ PK loc_id    │
   │ building_   │      │ FK property_id  ─────────────┼──┐  │ address      │
   │   category  │◄─────┤ FK social_id                 │  │  │ zip_code     │
   │ gross_sqft  │      │ sale_price                   │  │  │ block / lot  │
   │ land_sqft   │      │ price_per_sqft               │  │  │ FK neighbor_ │
   │ year_built  │      │ price_per_sqft_real          │  │  │     hood_id  │
   │ building_age│      │ sale_date                    │  │  └──────┬───────┘
   │ res_units   │      │ sale_year / sale_month       │  │         │ N:1
   │ com_units   │      │ tax_class_sale               │  │         │
   │ is_resident.│      │ building_class_sale          │  │  ┌──────▼───────────┐
   └─────────────┘      └──────────────────────────────┘  │  │ dim_neighborhood  │
                                                           │  │──────────────────│
                                                           │  │ PK neighbor_id   │
                                                           │  │ neighborhood_name │
                                                           │  │ FK borough_id    │
                                                           │  └──────┬───────────┘
                                                           │         │ N:1
                                                           │         │
                                                           │  ┌──────▼──────────┐
                                                           │  │   dim_borough    │
                                                           │  │─────────────────│
                                                           │  │ PK borough_id   │
                                                           │  │ borough_name    │
                                                           │  └─────────────────┘
                                                           │
                                                           └──► (qua dim_location
                                                                  → dim_neighborhood
                                                                  → dim_borough)

================================================================================
"""

# ═══════════════════════════════════════════════════════════════════
# MERMAID ERD (Copy vào https://mermaid.live/ để vẽ đồ thị đẹp)
# ═══════════════════════════════════════════════════════════════════
MERMAID_ERD = """
================================================================================
                    SƠ ĐỒ DẠNG MERMAID ERD
   (Copy đoạn erDiagram vào https://mermaid.live/ để xem hình)
================================================================================

erDiagram
    dim_borough {
        int     borough_id   PK
        string  borough_name
    }
    dim_neighborhood {
        int     neighborhood_id  PK
        string  neighborhood_name
        int     borough_id       FK
    }
    dim_location {
        int     location_id      PK
        string  address
        string  zip_code
        string  block
        string  lot
        int     neighborhood_id  FK
    }
    dim_property {
        int     property_id              PK
        string  building_class_category
        string  building_category
        string  building_type
        string  building_class_present
        string  tax_class_present
        real    gross_sqft
        real    land_sqft
        int     year_built
        int     building_age
        int     residential_units
        int     commercial_units
        int     total_units
        int     is_residential
    }
    dim_social_metrics {
        int     social_id     PK
        int     borough_id    FK
        real    pop_density
        real    avg_income
        real    gdp_local
        real    dist_center
        real    amenity_score
    }
    fact_sales {
        int     sale_id             PK
        int     location_id         FK
        int     property_id         FK
        int     social_id           FK
        real    sale_price
        real    price_per_sqft
        real    price_per_sqft_real
        string  sale_date
        int     sale_year
        int     sale_month
        string  tax_class_sale
        string  building_class_sale
    }

    dim_borough         ||--o{ dim_neighborhood    : "chứa (1:N)"
    dim_neighborhood    ||--o{ dim_location         : "định vị (1:N)"
    dim_location        ||--o{ fact_sales           : "giao dịch tại (1:N)"
    dim_property        ||--o{ fact_sales           : "tính chất vật lý (1:N)"
    dim_social_metrics  ||--o{ fact_sales           : "chỉ số xã hội (1:N)"
    dim_borough         ||--|| dim_social_metrics   : "đặc trưng (1:1)"

================================================================================
"""

# ═══════════════════════════════════════════════════════════════════
# CHI TIẾT RÀNG BUỘC KHÓA NGOẠI
# ═══════════════════════════════════════════════════════════════════
RELATIONSHIP_DETAILS = """
================================================================================
              CHI TIẾT RÀNG BUỘC KHÓA NGOẠI (FOREIGN KEYS)
================================================================================

1. dim_neighborhood.borough_id  ─────► dim_borough.borough_id
   Ràng buộc: Mỗi Khu phố (Neighborhood) bắt buộc thuộc về một Quận (Borough).
   Cardinality: Một Quận có thể chứa NHIỀU Khu phố (1:N).

2. dim_location.neighborhood_id ─────► dim_neighborhood.neighborhood_id
   Ràng buộc: Mỗi Địa chỉ/Thửa đất bắt buộc nằm trong một Khu phố cụ thể.
   Cardinality: Một Khu phố có thể chứa NHIỀU Địa chỉ (1:N).

3. fact_sales.location_id ───────────► dim_location.location_id
   Ràng buộc: Mỗi Giao dịch bắt buộc diễn ra tại một Địa chỉ xác định.
   Cardinality: Một Địa chỉ có thể có NHIỀU lượt giao dịch mua bán (1:N).

4. fact_sales.property_id ───────────► dim_property.property_id
   Ràng buộc: Mỗi Giao dịch bắt buộc liên kết với thông tin vật lý của tài sản.
   Cardinality: Một tài sản vật lý có thể được giao dịch NHIỀU lần (1:N).

5. fact_sales.social_id ─────────────► dim_social_metrics.social_id
   Ràng buộc: Mỗi Giao dịch liên kết với bộ chỉ số kinh tế-xã hội của Quận.
   Cardinality: Một bộ chỉ số áp dụng cho NHIỀU giao dịch trong cùng Quận (1:N).

6. dim_social_metrics.borough_id ────► dim_borough.borough_id
   Ràng buộc: Mỗi bộ chỉ số xã hội ánh xạ 1:1 với một Quận duy nhất.
   Cardinality: Quan hệ một-một (1:1) giữa Quận và bộ chỉ số của nó.

================================================================================
THỐNG KÊ CƠ SỞ DỮ LIỆU (nyc_warehouse.db):
  • dim_borough         :      5 dòng (5 quận NYC)
  • dim_neighborhood    :    252 dòng (khu phố, unique theo cặp tên + quận)
  • dim_location        : 47,039 dòng (địa chỉ giao dịch)
  • dim_property        : 47,039 dòng (thông tin vật lý tài sản)
  • dim_social_metrics  :      5 dòng (chỉ số kinh tế-xã hội theo quận)
  • fact_sales          : 47,039 dòng (giao dịch BĐS 2022-2025)
================================================================================
"""


def main():
    print(PIPELINE_DIAGRAM)
    print(ASCII_ERD)
    print(RELATIONSHIP_DETAILS)
    print(MERMAID_ERD)


if __name__ == '__main__':
    main()

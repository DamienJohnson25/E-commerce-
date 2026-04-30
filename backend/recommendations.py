import sqlite3
import os
from collections import defaultdict

DATABASE = os.path.join(os.path.dirname(__file__), 'shop.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_recommendations(product_id=None, session_id=None, limit=8, filter_type=None, filter_value=None):
    conn = get_db()
    scores = defaultdict(float)

    # 1. Load context and all available products
    all_products = [dict(p) for p in conn.execute('SELECT * FROM products WHERE stock > 0').fetchall()]
    product_map = {p['id']: p for p in all_products}
    
    # FIX: Handle cases where product_id might be None or the string 'null' from the frontend
    try:
        pid_int = int(product_id) if (product_id and str(product_id) != 'null') else None
    except (ValueError, TypeError):
        pid_int = None

    exclude_ids = {pid_int} if pid_int else set()
    
    # FIX: Guard against pid_int not existing in the product_map to prevent 500 errors
    source_category = None
    if pid_int and pid_int in product_map:
        source_category = product_map[pid_int].get('category')

    # 2. Strict Routing Logic 
    # If filter_type is provided, we use specific scoring; otherwise, we default to category match.
    if filter_type == 'brand':
        scores = _score_by_brand(all_products, exclude_ids, filter_value)
    
    elif filter_type == 'price_range':
        # FIXED: Uses source_category to lock the price hunt to the same genre for accuracy
        scores = _score_by_price_range(all_products, exclude_ids, filter_value, source_category)
    
    elif filter_type == 'trending':
        # Uses provided filter_value or falls back to the current product's category
        scores = _score_by_trending(all_products, exclude_ids, filter_value or source_category, conn)
    
    elif filter_type == 'tags':
        scores = _score_by_tags(all_products, exclude_ids, filter_value)
    
    else:
        # Default / Category Row logic
        scores = _score_default(all_products, exclude_ids, filter_value or source_category)

    conn.close()

    # 3. Final Ranking & Formatting
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    results = []
    for pid, score in ranked[:limit]:
        if pid in product_map:
            p = dict(product_map[pid])
            p['recommendation_score'] = round(score, 2)
            results.append(p)
            
    return results

# ─── HELPER FUNCTIONS ───

def _score_default(all_products, exclude_ids, category):
    """Signals: Category Match (10pts) + Rating Tie-breaker."""
    scores = defaultdict(float)
    if not category: return scores
    for p in all_products:
        if p['id'] in exclude_ids: continue
        
        if p.get('category') == category:
            scores[p['id']] += 10.0 
            scores[p['id']] += (p.get('rating') or 0)
    return scores

def _score_by_price_range(all_products, exclude_ids, price_value, category):
    """Signals: Strict Proximity (15pts max) within the same category."""
    scores = defaultdict(float)
    try: 
        base_price = float(price_value)
    except: 
        return scores
    
    # 15% window for high accuracy
    low, high = base_price * 0.85, base_price * 1.15

    for p in all_products:
        if p['id'] in exclude_ids: continue
        
        # Genre Lock: Only compare prices within the same category
        if p.get('category') == category:
            price = p.get('price') or 0
            if low <= price <= high:
                diff = abs(price - base_price)
                # Items closer to the exact price score higher
                proximity = 1 - (diff / (base_price * 0.15 + 0.01))
                scores[p['id']] += (proximity * 15.0) + (p.get('rating') or 0)
    return scores

def _score_by_trending(all_products, exclude_ids, category, conn):
    """Signals: Order Frequency (3pts/sale) within the genre."""
    scores = defaultdict(float)
    if not category: return scores
    
    try:
        rows = conn.execute('''
            SELECT oi.product_id, COUNT(*) as cnt FROM order_items oi 
            JOIN products p ON oi.product_id = p.id 
            WHERE p.category = ? GROUP BY oi.product_id
        ''', (category,)).fetchall()
        counts = {r['product_id']: r['cnt'] for r in rows}
    except sqlite3.OperationalError:
        # Falls back gracefully if order_items table doesn't exist yet
        counts = {}

    for p in all_products:
        if p['id'] in exclude_ids: continue
        if p.get('category') == category:
            scores[p['id']] += (counts.get(p['id'], 0) * 3.0) + (p.get('rating') or 0)
    return scores

def _score_by_brand(all_products, exclude_ids, brand):
    """Signals: Brand Match (10pts) + Rating."""
    scores = defaultdict(float)
    if not brand: return scores
    for p in all_products:
        if p['id'] in exclude_ids: continue
        if (p.get('brand') or '').lower() == brand.lower():
            scores[p['id']] += 10.0 + (p.get('rating') or 0)
    return scores

def _score_by_tags(all_products, exclude_ids, tags_value):
    """Signals: Keyword Overlap (5pts/tag) + Rating."""
    scores = defaultdict(float)
    if not tags_value: return scores
    
    source_tags = set(t.strip().lower() for t in str(tags_value).split(',') if t.strip())
    for p in all_products:
        if p['id'] in exclude_ids: continue
        
        raw_tags = p.get('tags') or ''
        # Handle stringified lists from DB
        clean_tags = str(raw_tags).replace('[','').replace(']','').replace('"','')
        p_tags = set(t.strip().lower() for t in clean_tags.split(',') if t.strip())
        
        overlap = len(source_tags & p_tags)
        if overlap > 0:
            scores[p['id']] += (overlap * 5.0) + (p.get('rating') or 0)
    return scores

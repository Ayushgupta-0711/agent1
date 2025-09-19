import pandas as pd
import io
import base64
import matplotlib.pyplot as plt

class DataAgent:
    def __init__(self):
        pass

    def _read_file(self, filename, file_bytes):
        if not filename or not file_bytes:
            return None
        if filename.lower().endswith('.csv'):
            return pd.read_csv(io.BytesIO(file_bytes))
        if filename.lower().endswith(('.xls', '.xlsx')):
            return pd.read_excel(io.BytesIO(file_bytes))
        return None

    def _generate_chart_base64(self, fig):
        import io
        buf = io.BytesIO()
        fig.savefig(buf, bbox_inches='tight')
        buf.seek(0)
        encoded = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return encoded

    def handle(self, query, filename, file_bytes):
        df = self._read_file(filename, file_bytes) if file_bytes else None
        q = (query or "").lower()
        if df is None:
            return {"text": "No tabular file provided. Upload a CSV/XLSX to use Data Intelligence Agent."}

        # columns to lowercase for easier checks
        df.columns = [c.lower() for c in df.columns]

        # Example: total sales in Q2
        if 'total' in q and 'q2' in q:
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                q2 = df[df['date'].dt.quarter == 2]
                val_col = 'sales' if 'sales' in df.columns else ('revenue' if 'revenue' in df.columns else None)
                if val_col:
                    total = q2[val_col].sum()
                    return {"type":"text","text": f"Total {val_col} in Q2: {total}"}
            return {"text":"Couldn't find date or sales/revenue columns. Ensure CSV has 'date' and 'sales' or 'revenue'."}

        # Example: Plot revenue trends for top 5 products
        if 'top 5' in q or 'top5' in q:
            if 'product' in df.columns and ('revenue' in df.columns or 'sales' in df.columns):
                value_col = 'revenue' if 'revenue' in df.columns else 'sales'
                grouped = df.groupby('product')[value_col].sum().reset_index().sort_values(value_col, ascending=False).head(5)
                fig = plt.figure(figsize=(8,4))
                plt.bar(grouped['product'], grouped[value_col])
                plt.xticks(rotation=45, ha='right')
                plt.title('Top 5 products by ' + value_col)
                chart_b64 = self._generate_chart_base64(fig)
                return {"type":"chart","chart_base64":chart_b64}
            else:
                return {"text":"CSV must contain 'product' and 'revenue' (or 'sales') columns for this query."}

        # Fallback: return first 10 rows
        sample = df.head(10)
        return {"type":"table","data": sample.to_dict(orient='records')}

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import webbrowser
import os

COLORS = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]

_DASHBOARD_CHARTS = {}

def _register(name, fig):
    _DASHBOARD_CHARTS[name] = fig

def plot_rolling_volatility(vol_30, vol_90):
    fig = make_subplots(rows=1, cols=1)
    for i, col in enumerate(vol_30.columns):
        fig.add_trace(go.Scatter(
            x=vol_30.index, y=vol_30[col],
            name=f"{col} 30d",
            line=dict(color=COLORS[i], width=1.5)
        ))
        fig.add_trace(go.Scatter(
            x=vol_90.index, y=vol_90[col],
            name=f"{col} 90d",
            line=dict(color=COLORS[i], width=1.5, dash="dash")
        ))
    fig.update_layout(
        title="Rolling Annualized Volatility",
        xaxis_title="Date",
        yaxis_title="Volatility",
        hovermode="x unified",
        template="plotly_dark",
        height=500
    )
    _register("Rolling Volatility", fig)

def plot_drawdown(drawdown):
    fig = go.Figure()
    for i, col in enumerate(drawdown.columns):
        fig.add_trace(go.Scatter(
            x=drawdown.index, y=drawdown[col],
            name=col,
            line=dict(color=COLORS[i], width=1.5),
            fill="tozeroy"
        ))
    fig.update_layout(
        title="Drawdown Over Time",
        xaxis_title="Date",
        yaxis_title="Drawdown",
        hovermode="x unified",
        template="plotly_dark",
        height=500
    )
    _register("Drawdown", fig)

def plot_cumulative_returns(cumulative):
    fig = px.line(
        cumulative,
        title="Cumulative Returns (2010-2025)",
        labels={"value": "Growth of $1", "variable": "Ticker"},
        color_discrete_sequence=COLORS,
        template="plotly_dark"
    )
    fig.update_layout(hovermode="x unified", height=500)
    _register("Cumulative Returns", fig)

def plot_return_distribution(returns):
    fig = make_subplots(
        rows=1, cols=len(returns.columns),
        subplot_titles=list(returns.columns)
    )
    for i, col in enumerate(returns.columns):
        fig.add_trace(
            go.Histogram(
                x=returns[col],
                nbinsx=70,
                name=col,
                marker_color=COLORS[i],
                opacity=0.75
            ),
            row=1, col=i+1
        )
    fig.update_layout(
        title="Return Distributions",
        template="plotly_dark",
        showlegend=False,
        height=400
    )
    _register("Return Distributions", fig)

def plot_correlation_heatmap(returns):
    corr = returns.corr().round(2)
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale="RdBu",
        zmid=0,
        text=corr.values,
        texttemplate="%{text}",
        hovertemplate="x: %{x}<br>y: %{y}<br>corr: %{z}<extra></extra>"
    ))
    fig.update_layout(
        title="Correlation Heatmap",
        template="plotly_dark",
        height=500
    )
    _register("Correlation Heatmap", fig)

def plot_sharpe_ranking(results):
    ranking = results["Sharpe Ratio"].sort_values(ascending=True)
    fig = go.Figure(go.Bar(
        x=ranking.values,
        y=ranking.index,
        orientation="h",
        marker_color=COLORS,
        text=ranking.round(3).values,
        textposition="outside"
    ))
    fig.update_layout(
        title="Sharpe Ratio Ranking",
        xaxis_title="Sharpe Ratio",
        template="plotly_dark",
        height=400
    )
    _register("Sharpe Ranking", fig)

def plot_momentum_strategy(buy_hold, momentum):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=buy_hold.index, y=buy_hold,
        name="Buy & Hold SPY",
        line=dict(color="#636EFA", width=2)
    ))
    fig.add_trace(go.Scatter(
        x=momentum.index, y=momentum,
        name="Momentum Strategy",
        line=dict(color="#00CC96", width=2)
    ))
    fig.update_layout(
        title="Momentum Strategy vs Buy & Hold SPY",
        xaxis_title="Date",
        yaxis_title="Growth of $1",
        hovermode="x unified",
        template="plotly_dark",
        height=500
    )
    _register("Momentum Strategy", fig)

def plot_min_variance_weights(weights):
    fig = go.Figure(go.Bar(
        x=weights.index,
        y=weights.values * 100,
        marker_color=COLORS,
        text=[f"{w*100:.1f}%" for w in weights.values],
        textposition="outside"
    ))
    fig.update_layout(
        title="Minimum Variance Portfolio — Optimal Weights",
        xaxis_title="Asset",
        yaxis_title="Weight (%)",
        template="plotly_dark",
        height=400
    )
    _register("Min Variance Weights", fig)

def save_dashboard(path="dashboard.html"):
    tabs = list(_DASHBOARD_CHARTS.keys())

    chart_divs = {}
    for i, (name, fig) in enumerate(_DASHBOARD_CHARTS.items()):
        fig.update_layout(autosize=True, height=None, margin=dict(l=40, r=40, t=50, b=40))
        chart_divs[name] = fig.to_html(
            full_html=False,
            include_plotlyjs=(i == 0),
            config={"responsive": True},
            div_id=f"chart-{i}",
        )

    tab_buttons = "\n".join(
        f'<button class="tab-btn {"active" if i == 0 else ""}" onclick="showTab({i})">{name}</button>'
        for i, name in enumerate(tabs)
    )
    tab_panels = "\n".join(
        f'<div class="tab-panel" id="panel-{i}" style="display:{"block" if i == 0 else "none"}">{chart_divs[name]}</div>'
        for i, name in enumerate(tabs)
    )

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Quant Risk Dashboard</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; }}
  html, body {{
    margin: 0; padding: 0; height: 100%;
    background: #111; color: #eee; font-family: sans-serif; overflow: hidden;
  }}
  .tab-bar {{
    display: flex; flex-wrap: wrap; gap: 6px;
    padding: 10px 12px; background: #111; border-bottom: 1px solid #333;
  }}
  .tab-btn {{
    background: #222; color: #aaa; border: 1px solid #444;
    padding: 7px 16px; cursor: pointer; border-radius: 4px; font-size: 13px;
  }}
  .tab-btn.active {{ background: #636EFA; color: #fff; border-color: #636EFA; }}
  .tab-btn:hover:not(.active) {{ background: #333; color: #fff; }}
  .tab-panel {{
    position: absolute; top: 52px; left: 0; right: 0; bottom: 0;
  }}
  .tab-panel .plotly-graph-div {{
    width: 100% !important;
    height: 100% !important;
  }}
</style>
</head>
<body>
<div class="tab-bar">{tab_buttons}</div>
{tab_panels}
<script>
function showTab(i) {{
  document.querySelectorAll('.tab-panel').forEach((p, j) => p.style.display = j === i ? 'block' : 'none');
  document.querySelectorAll('.tab-btn').forEach((b, j) => b.classList.toggle('active', j === i));
  var panel = document.getElementById('panel-' + i);
  var gd = panel.querySelector('.plotly-graph-div');
  if (gd && window.Plotly) Plotly.relayout(gd, {{autosize: true}});
}}
window.addEventListener('resize', function() {{
  document.querySelectorAll('.tab-panel[style*="block"] .plotly-graph-div').forEach(function(gd) {{
    if (window.Plotly) Plotly.relayout(gd, {{autosize: true}});
  }});
}});
</script>
</body>
</html>"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open(f"file://{os.path.abspath(path)}")
    print(f"Dashboard saved to {path}")

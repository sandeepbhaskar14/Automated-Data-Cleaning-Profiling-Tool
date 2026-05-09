"""
frontend/ui/pages/cleaning_page.py
────────────────────────────────────
Cleaning page widget — Phase 3.

Layout
──────
┌─────────────────────────────────────────────────────────────────┐
│  Header: "Cleaning"  ·  filename  ·  current rows × cols       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─ Left panel (operations) ──────────┐ ┌─ Right panel ──────┐ │
│  │  Missing Values   [strategy ▾][▶] │ │  Changelog log     │ │
│  │  Drop Null Cols   [thresh  ▾][▶]  │ │  (scrollable)      │ │
│  │  Duplicates       [keep    ▾][▶]  │ │                    │ │
│  │  Outliers         [method  ▾][▶]  │ │                    │ │
│  │  Type Correction              [▶] │ │                    │ │
│  │  Normalize        [ops     ▾][▶]  │ │                    │ │
│  │  ─────────────────────────────    │ │                    │ │
│  │  [Run Full Pipeline]              │ │                    │ │
│  └───────────────────────────────────┘ └────────────────────┘ │
│                                                                 │
│  [Refresh Dashboard]                                            │
└─────────────────────────────────────────────────────────────────┘

All network calls run in QThread workers so the UI never blocks.
"""

from __future__ import annotations

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QComboBox, QScrollArea, QTextEdit,
    QSizePolicy, QSpacerItem,
)

from services.api_client import ApiClient
from services.logger import get_logger

log    = get_logger(__name__)
client = ApiClient()


# ══════════════════════════════════════════════════════════════════════════════
#  Palette
# ══════════════════════════════════════════════════════════════════════════════
class _P:
    BG         = "#FFFFFF"
    BG_PANEL   = "#F8FAFC"
    BORDER     = "#E2E8F0"
    TEXT_DARK  = "#1E293B"
    TEXT_MID   = "#64748B"
    TEXT_LIGHT = "#94A3B8"
    ACCENT     = "#0158CB"
    ACCENT_H   = "#003EBA"
    SUCCESS    = "#166534"
    SUCCESS_BG = "#F0FDF4"
    ERROR      = "#991B1B"
    ERROR_BG   = "#FEF2F2"
    WARN       = "#92400E"
    WARN_BG    = "#FFFBEB"
    INFO_BG    = "#EFF6FF"
    INFO_FG    = "#1E40AF"

    COMBO_SS = (
        "QComboBox{border:1px solid #CBD5E1;border-radius:6px;"
        "padding:4px 8px;background:#FFFFFF;color:#1E293B;font-size:9pt;}"
        "QComboBox:hover{border-color:#94A3B8;}"
        "QComboBox::drop-down{border:none;width:18px;}"
    )
    BTN_RUN = (
        "QPushButton{border:none;border-radius:6px;color:#FFFFFF;"
        "background-color:#0158CB;padding:5px 14px;font-size:9pt;}"
        "QPushButton:hover{background-color:#003EBA;}"
        "QPushButton:disabled{background-color:#A0AEC0;}"
    )
    BTN_FULL = (
        "QPushButton{border:none;border-radius:8px;color:#FFFFFF;"
        "background-color:#0158CB;padding:8px 22px;font-size:10pt;font-weight:600;}"
        "QPushButton:hover{background-color:#003EBA;}"
        "QPushButton:disabled{background-color:#A0AEC0;}"
    )
    BTN_GHOST = (
        "QPushButton{border:1px solid #CBD5E1;border-radius:8px;"
        "color:#1E293B;background:none;padding:8px 22px;font-size:10pt;}"
        "QPushButton:hover{background-color:#F1F5F9;}"
        "QPushButton:disabled{color:#94A3B8;}"
    )


# ══════════════════════════════════════════════════════════════════════════════
#  Generic worker
# ══════════════════════════════════════════════════════════════════════════════
class _Worker(QThread):
    done = pyqtSignal(str, bool, dict)   # (op_name, success, payload)

    def __init__(self, op: str, fn, **kwargs):
        super().__init__()
        self._op  = op
        self._fn  = fn
        self._kw  = kwargs

    def run(self):
        ok, data = self._fn(**self._kw)
        self.done.emit(self._op, ok, data)


# ══════════════════════════════════════════════════════════════════════════════
#  Operation row widget
# ══════════════════════════════════════════════════════════════════════════════
class _OpRow(QFrame):
    """A single cleaning-operation row: label + optional combo + Run button."""

    run_clicked = pyqtSignal()

    def __init__(self, label: str, combo_items: list[str] | None = None,
                 parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"QFrame{{background:{_P.BG_PANEL};border:1px solid {_P.BORDER};"
            "border-radius:8px;}}"
        )
        self.setFixedHeight(52)

        row = QHBoxLayout(self)
        row.setContentsMargins(12, 0, 12, 0)
        row.setSpacing(10)

        lbl = QLabel(label)
        lbl.setFont(QFont("Roboto Medium", 9))
        lbl.setStyleSheet(f"border:none;color:{_P.TEXT_DARK};background:none;")
        lbl.setFixedWidth(170)
        row.addWidget(lbl)

        self._combo: QComboBox | None = None
        if combo_items:
            self._combo = QComboBox()
            self._combo.addItems(combo_items)
            self._combo.setFixedWidth(155)
            self._combo.setFont(QFont("Roboto", 9))
            self._combo.setStyleSheet(_P.COMBO_SS)
            row.addWidget(self._combo)
        else:
            row.addStretch()

        row.addStretch()

        self._btn = QPushButton("Run")
        self._btn.setFixedSize(58, 32)
        self._btn.setFont(QFont("Roboto Medium", 9))
        self._btn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self._btn.setStyleSheet(_P.BTN_RUN)
        self._btn.clicked.connect(self.run_clicked)
        row.addWidget(self._btn)

    def combo_value(self) -> str:
        return self._combo.currentText() if self._combo else ""

    def set_enabled(self, enabled: bool):
        self._btn.setEnabled(enabled)
        if self._combo:
            self._combo.setEnabled(enabled)


# ══════════════════════════════════════════════════════════════════════════════
#  Cleaning page
# ══════════════════════════════════════════════════════════════════════════════
class CleaningPage(QWidget):
    """
    Signals
    -------
    dataset_updated(dataset_id)
        Emitted after any cleaning operation writes back to session_store,
        so DashboardPage can refresh its stats.
    """

    dataset_updated = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dataset_id: str | None = None
        self._workers: list[QThread] = []
        self._build_ui()

    # ── UI assembly ───────────────────────────────────────────────────────────

    def _build_ui(self):
        self.setStyleSheet(f"background-color:{_P.BG};")
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())

        body = QHBoxLayout()
        body.setContentsMargins(22, 14, 22, 14)
        body.setSpacing(16)
        body.addWidget(self._build_ops_panel(), stretch=3)
        body.addWidget(self._build_log_panel(), stretch=2)

        root.addLayout(body)
        root.addWidget(self._build_footer())

        self._set_controls_enabled(False)

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self) -> QFrame:
        bar = QFrame()
        bar.setFixedHeight(56)
        bar.setStyleSheet(f"QFrame{{background-color:{_P.BG};}}")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(22, 12, 22, 0)

        title = QLabel("Cleaning")
        title.setFont(QFont("Roboto Medium", 14))
        title.setStyleSheet(
            f"color:{_P.TEXT_DARK};"
            f"border-bottom:1px solid {_P.BORDER};"
        )
        layout.addWidget(title)
        layout.addStretch()

        self._hdr_meta = QLabel("No dataset loaded")
        self._hdr_meta.setFont(QFont("Roboto", 9))
        self._hdr_meta.setStyleSheet(f"color:{_P.TEXT_MID};")
        self._hdr_meta.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self._hdr_meta)
        return bar

    # ── Operations panel ──────────────────────────────────────────────────────

    def _build_ops_panel(self) -> QFrame:
        panel = QFrame()
        panel.setStyleSheet(
            f"QFrame{{background:{_P.BG};border:1px solid {_P.BORDER};"
            "border-radius:10px;}}"
        )
        vbox = QVBoxLayout(panel)
        vbox.setContentsMargins(16, 14, 16, 16)
        vbox.setSpacing(8)

        sec = QLabel("Operations")
        sec.setFont(QFont("Roboto Medium", 10))
        sec.setStyleSheet(f"border:none;color:{_P.TEXT_MID};")
        vbox.addWidget(sec)

        # ── Missing values ────────────────────────────────────────────────────
        self._row_missing = _OpRow(
            "Missing Values",
            ["mean", "median", "mode", "drop", "ffill", "bfill", "zero", "unknown"],
        )
        self._row_missing.run_clicked.connect(self._run_missing)
        vbox.addWidget(self._row_missing)

        # ── Drop null columns ─────────────────────────────────────────────────
        self._row_null_cols = _OpRow(
            "Drop Null Columns",
            ["50% threshold", "60% threshold", "70% threshold",
             "80% threshold", "90% threshold"],
        )
        self._row_null_cols.run_clicked.connect(self._run_null_cols)
        vbox.addWidget(self._row_null_cols)

        # ── Duplicates ────────────────────────────────────────────────────────
        self._row_dupes = _OpRow(
            "Duplicates",
            ["keep first", "keep last", "drop all"],
        )
        self._row_dupes.run_clicked.connect(self._run_duplicates)
        vbox.addWidget(self._row_dupes)

        # ── Outliers ──────────────────────────────────────────────────────────
        self._row_outliers = _OpRow(
            "Outliers",
            ["IQR — clip", "IQR — drop",
             "Z-score — clip", "Z-score — drop"],
        )
        self._row_outliers.run_clicked.connect(self._run_outliers)
        vbox.addWidget(self._row_outliers)

        # ── Type correction ───────────────────────────────────────────────────
        self._row_types = _OpRow("Type Correction")
        self._row_types.run_clicked.connect(self._run_types)
        vbox.addWidget(self._row_types)

        # ── Normalise ─────────────────────────────────────────────────────────
        self._row_norm = _OpRow(
            "Normalize Strings",
            ["trim + collapse",
             "trim + lower",
             "trim + upper",
             "trim + title",
             "strip punctuation",
             "strip digits"],
        )
        self._row_norm.run_clicked.connect(self._run_normalize)
        vbox.addWidget(self._row_norm)

        # ── Divider ───────────────────────────────────────────────────────────
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet(f"color:{_P.BORDER};")
        vbox.addWidget(div)

        # ── Full pipeline ─────────────────────────────────────────────────────
        self._btn_pipeline = QPushButton("⚡  Run Full Pipeline")
        self._btn_pipeline.setFont(QFont("Roboto Medium", 10))
        self._btn_pipeline.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self._btn_pipeline.setStyleSheet(_P.BTN_FULL)
        self._btn_pipeline.setFixedHeight(42)
        self._btn_pipeline.clicked.connect(self._run_pipeline)
        vbox.addWidget(self._btn_pipeline)

        vbox.addStretch()
        return panel

    # ── Change-log panel ──────────────────────────────────────────────────────

    def _build_log_panel(self) -> QFrame:
        panel = QFrame()
        panel.setStyleSheet(
            f"QFrame{{background:{_P.BG};border:1px solid {_P.BORDER};"
            "border-radius:10px;}}"
        )
        vbox = QVBoxLayout(panel)
        vbox.setContentsMargins(14, 14, 14, 14)
        vbox.setSpacing(6)

        hdr = QHBoxLayout()
        lbl = QLabel("Change Log")
        lbl.setFont(QFont("Roboto Medium", 10))
        lbl.setStyleSheet(f"border:none;color:{_P.TEXT_MID};")
        hdr.addWidget(lbl)
        hdr.addStretch()

        clr = QPushButton("Clear")
        clr.setFont(QFont("Roboto", 8))
        clr.setFixedHeight(24)
        clr.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        clr.setStyleSheet(
            f"QPushButton{{border:1px solid {_P.BORDER};border-radius:4px;"
            f"color:{_P.TEXT_MID};background:none;padding:0 8px;}}"
            f"QPushButton:hover{{background:{_P.BG_PANEL};}}"
        )
        clr.clicked.connect(self._clear_log)
        hdr.addWidget(clr)
        vbox.addLayout(hdr)

        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 8))
        self._log.setStyleSheet(
            f"QTextEdit{{border:1px solid {_P.BORDER};border-radius:6px;"
            f"background:{_P.BG_PANEL};color:{_P.TEXT_DARK};"
            "padding:8px;line-height:1.4;}}"
        )
        self._log.setPlaceholderText(
            "Changes will appear here after each operation…"
        )
        vbox.addWidget(self._log, stretch=1)
        return panel

    # ── Footer ────────────────────────────────────────────────────────────────

    def _build_footer(self) -> QFrame:
        bar = QFrame()
        bar.setFixedHeight(56)
        bar.setStyleSheet(f"QFrame{{background:{_P.BG};border-top:1px solid {_P.BORDER};}}")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(22, 0, 22, 0)

        self._status_lbl = QLabel("")
        self._status_lbl.setFont(QFont("Roboto", 9))
        self._status_lbl.setStyleSheet(f"color:{_P.TEXT_MID};")
        layout.addWidget(self._status_lbl)
        layout.addStretch()

        self._btn_refresh = QPushButton("↺  Refresh Dashboard")
        self._btn_refresh.setFont(QFont("Roboto", 9))
        self._btn_refresh.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self._btn_refresh.setStyleSheet(_P.BTN_GHOST)
        self._btn_refresh.setEnabled(False)
        self._btn_refresh.clicked.connect(self._on_refresh)
        layout.addWidget(self._btn_refresh)
        return bar

    # ── Public API ────────────────────────────────────────────────────────────

    def load_dataset(self, dataset_id: str, filename: str, rows: int, cols: int):
        """Called by MainWindow when a dataset is successfully uploaded."""
        self._dataset_id = dataset_id
        self._hdr_meta.setText(
            f"{filename}    {rows:,} rows  ×  {cols} columns"
        )
        self._set_controls_enabled(True)
        self._btn_refresh.setEnabled(True)
        self._append_log("info",
            f"Dataset ready — {filename}  ({rows:,} × {cols})\n"
            "Select an operation and click Run, or use the full pipeline."
        )
        log.info("CleaningPage loaded dataset id=%s", dataset_id)

    # ── Operation handlers ────────────────────────────────────────────────────

    def _run_missing(self):
        strategy = self._row_missing.combo_value()
        self._dispatch("missing", client.clean_missing,
                       dataset_id=self._dataset_id, strategy=strategy)

    def _run_null_cols(self):
        label = self._row_null_cols.combo_value()   # e.g. "50% threshold"
        pct   = int(label.split("%")[0]) / 100.0
        self._dispatch("missing_cols", client.clean_missing_cols,
                       dataset_id=self._dataset_id, threshold=pct)

    def _run_duplicates(self):
        val = self._row_dupes.combo_value()
        keep = {"keep first": "first", "keep last": "last",
                "drop all": "false"}.get(val, "first")
        self._dispatch("duplicates", client.clean_duplicates,
                       dataset_id=self._dataset_id, keep=keep)

    def _run_outliers(self):
        val    = self._row_outliers.combo_value()    # e.g. "IQR — clip"
        parts  = val.split(" — ")
        method = "iqr" if "IQR" in parts[0] else "zscore"
        action = parts[1].strip().lower() if len(parts) > 1 else "clip"
        self._dispatch("outliers", client.clean_outliers,
                       dataset_id=self._dataset_id,
                       method=method, threshold=1.5, action=action)

    def _run_types(self):
        self._dispatch("types", client.clean_types,
                       dataset_id=self._dataset_id)

    def _run_normalize(self):
        val = self._row_norm.combo_value()
        ops_map = {
            "trim + collapse":   ["trim", "collapse_ws"],
            "trim + lower":      ["trim", "lower"],
            "trim + upper":      ["trim", "upper"],
            "trim + title":      ["trim", "title"],
            "strip punctuation": ["trim", "strip_punct"],
            "strip digits":      ["trim", "strip_digits"],
        }
        ops = ops_map.get(val, ["trim", "collapse_ws"])
        self._dispatch("normalize", client.clean_normalize,
                       dataset_id=self._dataset_id, ops=ops)

    def _run_pipeline(self):
        """Run the recommended full pipeline via the /pipeline endpoint."""
        steps = [
            {"op": "normalize",  "ops": ["trim", "collapse_ws"]},
            {"op": "types"},
            {"op": "duplicates", "keep": "first"},
            {"op": "missing",    "strategy": "mean"},
            {"op": "outliers",   "method": "iqr",
             "threshold": 1.5,   "action": "clip"},
        ]
        self._dispatch("pipeline", client.clean_pipeline,
                       dataset_id=self._dataset_id, steps=steps)

    # ── Worker dispatch ───────────────────────────────────────────────────────

    def _dispatch(self, op: str, fn, **kwargs):
        if not self._dataset_id:
            return
        self._set_controls_enabled(False)
        self._status_lbl.setText(f"Running {op}…")
        w = _Worker(op, fn, **kwargs)
        w.done.connect(self._on_done)
        w.start()
        self._workers.append(w)

    @pyqtSlot(str, bool, dict)
    def _on_done(self, op: str, ok: bool, data: dict):
        self._set_controls_enabled(True)
        self._btn_refresh.setEnabled(True)

        if not ok:
            err = data.get("error", "Unknown error")
            self._status_lbl.setText(f"✗  {op} failed")
            self._append_log("error", f"[{op}] ERROR: {err}")
            log.warning("Cleaning op '%s' failed: %s", op, err)
            return

        summary = data.get("summary", {})
        rows_b  = summary.get("rows_before", "?")
        rows_a  = summary.get("rows_after",  "?")
        removed = summary.get("rows_removed", 0)
        cols_b  = summary.get("cols_before", "?")
        cols_a  = summary.get("cols_after",  "?")
        changes = summary.get("changes", [])

        self._status_lbl.setText(
            f"✓  {op} — {removed} row(s) removed  |  "
            f"{cols_b - cols_a if isinstance(cols_b, int) and isinstance(cols_a, int) else 0}"
            f" col(s) removed  |  {len(changes)} change(s)"
        )

        # Build log entry
        lines = [
            f"[{op.upper()}]  rows {rows_b}→{rows_a}  cols {cols_b}→{cols_a}",
        ]
        for ch in changes[:30]:       # cap at 30 for readability
            detail = ch.get("detail", ch.get("operation", ""))
            lines.append(f"  • {detail}")
        if len(changes) > 30:
            lines.append(f"  … and {len(changes) - 30} more change(s)")

        self._append_log("success", "\n".join(lines))
        self.dataset_updated.emit(self._dataset_id)
        log.info("Cleaning '%s' done  rows=%s→%s  changes=%d",
                 op, rows_b, rows_a, len(changes))

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _set_controls_enabled(self, enabled: bool):
        for row in (self._row_missing, self._row_null_cols, self._row_dupes,
                    self._row_outliers, self._row_types, self._row_norm):
            row.set_enabled(enabled)
        self._btn_pipeline.setEnabled(enabled)

    def _append_log(self, kind: str, text: str):
        colours = {
            "info":    _P.INFO_FG,
            "success": _P.SUCCESS,
            "error":   _P.ERROR,
            "warn":    _P.WARN,
        }
        colour = colours.get(kind, _P.TEXT_DARK)
        html   = (
            f'<span style="color:{colour};font-family:Consolas;font-size:8pt;">'
            f'{text.replace(chr(10), "<br>")}'
            "</span><br>"
        )
        self._log.append(html)
        # Scroll to bottom
        sb = self._log.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _clear_log(self):
        self._log.clear()

    def _on_refresh(self):
        if self._dataset_id:
            self.dataset_updated.emit(self._dataset_id)
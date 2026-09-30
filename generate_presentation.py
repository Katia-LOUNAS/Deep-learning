#!/usr/bin/env python3
"""Generate Task B presentation slides (PowerPoint)."""

from itertools import product
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent
PPTX_PATH = OUT_DIR / "presentation_task_b.pptx"
FIG_DIR = OUT_DIR / "presentation_figures"

# 12 configs: product(hidden_size, num_layers, dropout) — same order as task_b notebook
ALL_CONFIGS = [
    {
        "run": i,
        "hidden_size": h,
        "num_layers": l,
        "dropout": d,
        "embed_dim": 64,
        "lr": 0.001,
        "batch_size": 32,
    }
    for i, (h, l, d) in enumerate(product([64, 128, 256], [1, 2], [0.0, 0.2]))
]

# Metrics by run index (from executed task_b_sequence_modelling.ipynb)
RNN_BY_RUN: dict[int, tuple[float, float, int]] = {
    2: (0.373991, 0.891298, 31),
    3: (0.375501, 0.890841, 33),
    4: (0.373583, 0.891573, 26),
    5: (0.376852, 0.890841, 15),
    6: (0.374277, 0.891298, 23),
    7: (0.374846, 0.891298, 26),
    8: (0.374698, 0.891298, 26),
    9: (0.375876, 0.891573, 13),
    10: (0.375364, 0.890932, 14),
    11: (0.374529, 0.891298, 15),
}

LSTM_BY_RUN: dict[int, tuple[float, float, int]] = {
    0: (0.374263, 0.890932, 28),
    1: (0.374379, 0.891298, 39),
    2: (0.374369, 0.890932, 22),
    3: (0.374103, 0.890932, 34),
    6: (0.374972, 0.890383, 20),
    7: (0.374295, 0.891024, 23),
    8: (0.374189, 0.890383, 14),
    9: (0.375398, 0.890383, 15),
    10: (0.374524, 0.890383, 17),
    11: (0.374422, 0.891024, 15),
}

RNN_RESULTS = sorted(
    [
        (c["hidden_size"], c["num_layers"], c["dropout"], m[0], m[1], m[2])
        for c in ALL_CONFIGS
        if (m := RNN_BY_RUN.get(c["run"]))
    ],
    key=lambda x: x[3],
)

LSTM_RESULTS = sorted(
    [
        (c["hidden_size"], c["num_layers"], c["dropout"], m[0], m[1], m[2])
        for c in ALL_CONFIGS
        if (m := LSTM_BY_RUN.get(c["run"]))
    ],
    key=lambda x: x[3],
)

ACCENT = RGBColor(0x1A, 0x56, 0x8E)
DARK = RGBColor(0x22, 0x22, 0x22)


def add_title_slide(prs: Presentation, title: str, subtitle: str = "") -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    if subtitle and len(slide.placeholders) > 1:
        slide.placeholders[1].text = subtitle
    slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = ACCENT


def add_section_slide(prs: Presentation, title: str) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[2])
    slide.shapes.title.text = title
    slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = ACCENT


def add_bullet_slide(prs: Presentation, title: str, bullets: list[str]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    body = slide.shapes.placeholders[1].text_frame
    body.clear()
    for i, line in enumerate(bullets):
        p = body.paragraphs[0] if i == 0 else body.add_paragraph()
        p.text = line
        p.level = 0
        p.font.size = Pt(18)
        p.font.color.rgb = DARK


def add_table_slide(
    prs: Presentation,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[float] | None = None,
    font_size: int = 10,
    row_height: float = 0.35,
) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = title
    n_rows, n_cols = len(rows) + 1, len(headers)
    left, top, width, height = Inches(0.35), Inches(1.25), Inches(9.3), Inches(row_height * n_rows)
    table = slide.shapes.add_table(n_rows, n_cols, left, top, width, height).table

    if col_widths:
        for j, w in enumerate(col_widths):
            table.columns[j].width = Inches(w)

    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(font_size + 1)

    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(font_size)
                if val in ("★", "R", "L", "R,L"):
                    p.font.bold = True


def add_image_slide(prs: Presentation, title: str, image_path: Path) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = title
    slide.shapes.add_picture(str(image_path), Inches(0.6), Inches(1.35), width=Inches(8.8))


def make_val_loss_chart(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 4.5))
    labels_rnn = [f"h{h} L{l} d{d}" for h, l, d, *_ in RNN_RESULTS[:6]]
    labels_lstm = [f"h{h} L{l} d{d}" for h, l, d, *_ in LSTM_RESULTS[:6]]
    x_rnn = range(len(labels_rnn))
    x_lstm = range(len(labels_lstm))
    ax.bar([i - 0.2 for i in x_rnn], [r[3] for r in RNN_RESULTS[:6]], width=0.4, label="RNN (top 6)", color="#1A568E")
    ax.bar([i + 0.2 for i in x_lstm], [r[3] for r in LSTM_RESULTS[:6]], width=0.4, label="LSTM (top 6)", color="#E07A2F")
    ax.set_xticks(range(6))
    ax.set_xticklabels([f"#{i+1}" for i in range(6)], fontsize=9)
    ax.set_ylabel("Validation loss (lower is better)")
    ax.set_title("Top hyperparameter configs — validation loss")
    ax.legend()
    ax.set_ylim(0.372, 0.378)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def make_comparison_chart(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    models = ["RNN (best)", "LSTM (best)"]
    val_acc = [0.891573, 0.890932]
    test_acc = [0.887076, 0.888182]
    x = range(len(models))
    w = 0.35
    ax.bar([i - w / 2 for i in x], val_acc, width=w, label="Val accuracy", color="#1A568E")
    ax.bar([i + w / 2 for i in x], test_acc, width=w, label="Test accuracy", color="#4A9E6F")
    ax.set_xticks(list(x))
    ax.set_xticklabels(models)
    ax.set_ylim(0.85, 0.90)
    ax.set_ylabel("Accuracy")
    ax.set_title("Best RNN vs best LSTM")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    for i, (va, ta) in enumerate(zip(val_acc, test_acc)):
        ax.text(i - w / 2, va + 0.001, f"{va:.3f}", ha="center", fontsize=9)
        ax.text(i + w / 2, ta + 0.001, f"{ta:.3f}", ha="center", fontsize=9)
    plt.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _fmt_metric(metrics: tuple[float, float, int] | None) -> tuple[str, str, str]:
    if metrics is None:
        return "—", "—", "—"
    vloss, vacc, epochs = metrics
    return f"{vloss:.4f}", f"{vacc:.3f}", str(epochs)


def all_configs_table_rows() -> list[list[str]]:
    rows = []
    for c in ALL_CONFIGS:
        rows.append(
            [
                str(c["run"] + 1),
                str(c["hidden_size"]),
                str(c["num_layers"]),
                str(c["dropout"]),
                str(c["embed_dim"]),
                str(c["lr"]),
                str(c["batch_size"]),
            ]
        )
    return rows


def combined_results_table_rows() -> list[list[str]]:
    best_rnn_run = min(RNN_BY_RUN, key=lambda r: RNN_BY_RUN[r][0])
    best_lstm_run = min(LSTM_BY_RUN, key=lambda r: LSTM_BY_RUN[r][0])
    rows = []
    for c in ALL_CONFIGS:
        run = c["run"]
        rnn = _fmt_metric(RNN_BY_RUN.get(run))
        lstm = _fmt_metric(LSTM_BY_RUN.get(run))
        marks = []
        if run == best_rnn_run:
            marks.append("R")
        if run == best_lstm_run:
            marks.append("L")
        mark = ",".join(marks)
        rows.append(
            [
                str(run + 1),
                str(c["hidden_size"]),
                str(c["num_layers"]),
                str(c["dropout"]),
                rnn[0],
                rnn[1],
                lstm[0],
                lstm[1],
                mark,
            ]
        )
    return rows


def model_results_table_rows(metrics_by_run: dict) -> list[list[str]]:
    best_run = min(metrics_by_run, key=lambda r: metrics_by_run[r][0])
    rows = []
    for c in ALL_CONFIGS:
        run = c["run"]
        m = metrics_by_run.get(run)
        vloss, vacc, epochs = _fmt_metric(m)
        rows.append(
            [
                str(run + 1),
                str(c["hidden_size"]),
                str(c["num_layers"]),
                str(c["dropout"]),
                vloss,
                vacc,
                epochs,
                "★" if run == best_run else "",
            ]
        )
    return rows


def build_presentation() -> Path:
    FIG_DIR.mkdir(exist_ok=True)
    chart1 = FIG_DIR / "val_loss_top6.png"
    chart2 = FIG_DIR / "best_comparison.png"
    make_val_loss_chart(chart1)
    make_comparison_chart(chart2)

    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    add_title_slide(
        prs,
        "E-commerce User Behavior",
        "Data exploration, preprocessing & sequence modelling (Task B)\nKatia Louanas — Deep Learning Project",
    )

    add_bullet_slide(
        prs,
        "Project pipeline",
        [
            "Raw Kaggle data → exploratory analysis → preprocessing → artifacts.pkl",
            "Task B: predict the next event in a synthetic session sequence",
            "Models: vanilla RNN vs LSTM (PyTorch), 12 hyperparameter configs each",
            "Selection criterion: lowest validation loss; final comparison on test set",
        ],
    )

    add_section_slide(prs, "1. The data")

    add_bullet_slide(
        prs,
        "Dataset",
        [
            "Source: Kaggle — e-commerce user behavior (~8 000 users, 14 columns)",
            "One row = one browsing session (aggregated features, not a click-by-click log)",
            "Features: demographics, device, engagement (time, pages, bounce), commerce flags",
            "Target (tabular): purchase (0/1) — extreme imbalance (~99.8% class 1)",
        ],
    )

    add_bullet_slide(
        prs,
        "Data quality & limitations",
        [
            "After cleaning: 6 138 sessions (missing values dropped, mainly ad_clicked)",
            "No native event log → sequences are built from session aggregates (important caveat)",
            "Event vocabulary: view, discount, click_ad, cart, purchase (+ padding token)",
            "Exploration: redundant avg_session_time vs time_on_site; user_id dropped for modelling",
        ],
    )

    add_section_slide(prs, "2. Data exploration (summary)")

    add_bullet_slide(
        prs,
        "EDA highlights",
        [
            "Structure: dtypes, missing values, duplicates, univariate distributions",
            "Target purchase: severe class imbalance; few non-purchase sessions",
            "Numerical features: skew, outliers (IQR), correlation heatmap",
            "Categorical / flags: gender, device, discount, ad click vs purchase patterns",
            "Outcome: preprocessing plan (clean, encode, scale, stratified split)",
        ],
    )

    add_section_slide(prs, "3. Data preprocessing")

    add_bullet_slide(
        prs,
        "Tabular pipeline (Task A & shared splits)",
        [
            "Drop missing rows → separate X / y (purchase)",
            "Drop user_id and avg_session_time; one-hot gender & device_type",
            "Outliers → median replacement (IQR rule on numeric columns)",
            "Stratified split 70% / 15% / 15% (random_state=42)",
            "MinMaxScaler fit on train only; saved with splits in processed/artifacts.pkl",
        ],
    )

    add_bullet_slide(
        prs,
        "Sequence construction (Task B)",
        [
            "From each session: pages_viewed → repeated view; optional discount & click_ad",
            "cart_items → cart events; purchase flag → purchase at end if applicable",
            "Keep sessions with length ≥ 2; same train/val/test indices as tabular data",
            "Sequences — train: 4 296 | val: 921 | test: 921",
            "Vocabulary: <pad>, cart, click_ad, discount, purchase, view (6 types incl. pad)",
        ],
    )

    add_section_slide(prs, "4. Task B — problem & architecture")

    add_bullet_slide(
        prs,
        "Next-event prediction",
        [
            "Input: variable-length event ID sequence (padded batches)",
            "Output: logits over event types for the next token at each step",
            "Loss: CrossEntropyLoss (ignore padding index)",
            "Metrics: validation loss (model selection), top-1 next-event accuracy",
        ],
    )

    add_bullet_slide(
        prs,
        "Model architecture & training",
        [
            "Embedding(embed_dim) → RNN or LSTM(hidden_size, num_layers, dropout) → Linear(num_events)",
            "Optimizer: Adam, lr = 0.001 | batch_size = 32 | max 40 epochs",
            "Early stopping on validation loss (patience = 6)",
            "Same random seed (42) for every configuration run",
        ],
    )

    add_section_slide(prs, "5. Hyperparameter search")

    add_table_slide(
        prs,
        "Hyperparameter grid (what we varied)",
        ["Hyperparameter", "Values tested", "Fixed in all runs"],
        [
            ["hidden_size", "64, 128, 256", "—"],
            ["num_layers", "1, 2", "—"],
            ["dropout", "0.0, 0.2", "—"],
            ["embed_dim", "64", "64"],
            ["learning_rate", "0.001", "0.001"],
            ["batch_size", "32", "32"],
        ],
        col_widths=[2.2, 2.8, 2.5],
    )

    add_table_slide(
        prs,
        "All 12 configurations tested (same grid for RNN and LSTM)",
        ["Run", "hidden", "layers", "dropout", "embed", "lr", "batch"],
        all_configs_table_rows(),
        col_widths=[0.55, 0.85, 0.75, 0.85, 0.65, 0.75, 0.65],
        font_size=9,
        row_height=0.28,
    )

    add_bullet_slide(
        prs,
        "Search design",
        [
            "3 × 2 × 2 = 12 combinations per architecture (RNN and LSTM each trained on all 12)",
            "Run numbers match the notebook enumeration order (run 1 = first grid point)",
            "Best model selected by lowest validation loss per architecture",
            "In combined results: R = best RNN | L = best LSTM (by validation loss)",
        ],
    )

    add_table_slide(
        prs,
        "Results — all configurations (RNN vs LSTM)",
        [
            "Run",
            "hidden",
            "L",
            "drop",
            "RNN loss",
            "RNN acc",
            "LSTM loss",
            "LSTM acc",
            "Best",
        ],
        combined_results_table_rows(),
        col_widths=[0.45, 0.65, 0.4, 0.55, 0.85, 0.75, 0.85, 0.75, 0.45],
        font_size=8,
        row_height=0.26,
    )

    add_section_slide(prs, "6. RNN — results")

    add_table_slide(
        prs,
        "RNN — all 12 configurations (metrics per run)",
        ["Run", "hidden", "layers", "dropout", "val loss", "val acc", "epochs", ""],
        model_results_table_rows(RNN_BY_RUN),
        col_widths=[0.55, 0.75, 0.65, 0.75, 0.95, 0.85, 0.65, 0.4],
        font_size=8,
        row_height=0.26,
    )

    add_bullet_slide(
        prs,
        "Best RNN configuration",
        [
            "hidden_size = 128 | num_layers = 1 | dropout = 0.0 | embed_dim = 64",
            "Validation loss = 0.3736 | Validation accuracy = 89.16%",
            "Test loss = 0.3810 | Test accuracy = 88.71%",
            "Training stopped at epoch 26 (early stopping)",
        ],
    )

    add_section_slide(prs, "7. LSTM — results")

    add_table_slide(
        prs,
        "LSTM — all 12 configurations (metrics per run)",
        ["Run", "hidden", "layers", "dropout", "val loss", "val acc", "epochs", ""],
        model_results_table_rows(LSTM_BY_RUN),
        col_widths=[0.55, 0.75, 0.65, 0.75, 0.95, 0.85, 0.65, 0.4],
        font_size=8,
        row_height=0.26,
    )

    add_bullet_slide(
        prs,
        "Best LSTM configuration",
        [
            "hidden_size = 64 | num_layers = 2 | dropout = 0.2 | embed_dim = 64",
            "Validation loss = 0.3741 | Validation accuracy = 89.09%",
            "Test loss = 0.3811 | Test accuracy = 88.82%",
            "Training stopped at epoch 34 (early stopping)",
        ],
    )

    add_section_slide(prs, "8. Analysis & comparison")

    add_image_slide(prs, "Hyperparameter search — validation loss (top 6 per model)", chart1)

    add_bullet_slide(
        prs,
        "What we learn from the grid",
        [
            "All configs reach ~89% val accuracy — task is partly easy (many view → view steps)",
            "Larger hidden size (256) does not consistently beat 64 or 128",
            "Dropout 0.2 helps some LSTM runs; best RNN uses no dropout",
            "Val losses are very close (0.373–0.376); differences are small but systematic",
        ],
    )

    add_table_slide(
        prs,
        "Best RNN vs best LSTM (validation + test)",
        ["Model", "Config", "Val loss", "Val acc", "Test loss", "Test acc"],
        [
            [
                "RNN",
                "h128, L1, d0",
                "0.3736",
                "89.16%",
                "0.3810",
                "88.71%",
            ],
            [
                "LSTM",
                "h64, L2, d0.2",
                "0.3741",
                "89.09%",
                "0.3811",
                "88.82%",
            ],
        ],
        col_widths=[1.0, 1.5, 1.2, 1.2, 1.2, 1.2],
    )

    add_image_slide(prs, "Accuracy comparison — best models", chart2)

    add_bullet_slide(
        prs,
        "Head-to-head interpretation",
        [
            "Performance is nearly identical: ~0.1 percentage point on test accuracy",
            "LSTM wins on test accuracy in this run; RNN has slightly lower validation loss",
            "LSTM best: deeper (2 layers) + dropout — more regularization for sequences",
            "RNN best: wider hidden state (128) — sufficient for synthetic funnel data",
            "See notebook for confusion matrices and qualitative prediction examples",
        ],
    )

    add_section_slide(prs, "9. Conclusion")

    add_bullet_slide(
        prs,
        "Summary & takeaways",
        [
            "Cleaned 6 138 sessions; reusable preprocessing in processed/artifacts.pkl",
            "Synthetic sequences enable next-event modelling without raw clickstream data",
            "Systematic search: 12 RNN + 12 LSTM configs; best ~89% next-event accuracy",
            "RNN and LSTM are comparable on this dataset; choice can be based on stability or runtime",
            "Future work: real event logs, class weights, richer hyperparameter search, Transformer baseline",
        ],
    )

    add_title_slide(
        prs,
        "Thank you",
        "Questions?\nNotebooks: data_exploration.ipynb | data_preprocessing.ipynb | task_b_sequence_modelling.ipynb",
    )

    prs.save(PPTX_PATH)
    return PPTX_PATH


if __name__ == "__main__":
    path = build_presentation()
    print(f"Saved: {path}")

# visit_path — 多工人訪問路徑模擬器

> 使用「最近點優先」貪婪策略（Nearest-Neighbor Greedy），模擬一位或多位工人依序拜訪一組平面座標點，統計完成所有拜訪所需的總時間與各自的行走路徑，並可用 **Pillow 將路徑繪製成圖片**。

一個純 Python 的離散時間（tick-based）模擬程式。每一個時間單位（tick）代表一分鐘，模擬器會逐分鐘推進，替空閒的工人指派最近的未拜訪點，計算行走時間與停留拜訪時間，最終輸出總耗時、每位工人的完整路徑，並將路徑視覺化輸出成 PNG 圖檔。

---

## 目錄

- [專案特色](#專案特色)
- [運作原理](#運作原理)
- [專案結構](#專案結構)
- [環境需求](#環境需求)
- [快速開始](#快速開始)
- [設定說明](#設定說明)
- [座標檔格式](#座標檔格式)
- [路徑視覺化（Pillow）](#路徑視覺化pillow)
- [執行範例輸出](#執行範例輸出)
- [核心模組說明](#核心模組說明)
- [進階用法](#進階用法)

---

## 專案特色

- 🧭 **貪婪最近點演算法**：每次替空閒工人挑選離目前位置「歐幾里得距離最短」的未拜訪點。
- 👷 **支援多工人**：可同時加入多位工人平行拜訪（預設已啟用 worker A + worker B）。
- ⏱️ **離散時間模擬**：以一分鐘為單位逐格推進，清楚呈現「行走中 → 拜訪中 → 完成」的狀態轉換。
- 🎨 **路徑視覺化**：使用 Pillow 將每位工人的行走路徑畫成 PNG，每人一色、標示拜訪順序。
- 📄 **座標資料外部化**：拜訪點來自 `coordinates.txt`，可搭配 `build_coord.py` 隨機產生。

---

## 運作原理

模擬器採用「離散時間迴圈」，每一個 tick（可視為 1 分鐘）執行下列步驟：

1. **更新狀態**：檢查每位工人是否已抵達目標或完成拜訪，更新其狀態（`walking` / `visiting` / `idle`）。
2. **指派任務**：對每位 `idle` 的工人，從剩餘座標點中挑選距離最近者，計算行走時間並指派。
3. **推進時間**：`current_time += 1`，重複上述流程，直到「所有點都被拜訪完」且「所有工人都回到 idle」。
4. **繪製路徑**：模擬結束後，呼叫 `draw_paths()` 將所有工人的路徑輸出成圖片。

工人的狀態機如下：

```
idle ──set_task──▶ walking ──抵達──▶ visiting ──完成──▶ idle
   └──────(距離為 0 時直接進入 visiting)───────┘
```

- **行走時間** `travel_time = round(distance × WALK_SPEED)`（`distance` 為歐幾里得距離）。
- **拜訪時間** 固定為 `VISIT_TIME`（預設 30 分鐘）。

---

## 專案結構

```
visit_path/
├── main.py           # 程式進入點：建立模擬、載入座標、加入工人、執行、畫圖
├── simulation.py     # Simulation 類別：載入座標、任務指派、主迴圈、結果統計
├── worker.py         # Worker 類別：工人狀態機（idle/walking/visiting）
├── visualizer.py     # 用 Pillow 將工人路徑繪製成 PNG 圖片
├── config.py         # 全域參數設定（座標檔名、速度、拜訪時間、起點）
├── build_coord.py    # 工具：隨機產生 8 個不重複座標並寫入 coordinates.txt
├── coordinates.txt   # 拜訪點座標資料（每行一組 "x y"）
└── result/
    └── picture/      # 存放輸出的路徑圖（例如 two_workers.png）
```

---

## 環境需求

- **Python 3.8+**（使用了 `math.dist`，需 Python 3.8 以上）
- **Pillow**（路徑視覺化所需，需安裝）：

```bash
pip install pillow
```

---

## 快速開始

```bash
# 1. 取得專案
git clone https://github.com/kevinhuang09/visit_path.git
cd visit_path

# 2. 安裝繪圖套件
pip install pillow

# 3.（選用）重新隨機產生座標檔
python build_coord.py

# 4. 執行模擬（結束後會在 result/picture/ 產生路徑圖）
python main.py
```

---

## 設定說明

所有可調參數集中於 `config.py`：

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `COORDINATES_FILE` | `"coordinates.txt"` | 拜訪點座標檔案路徑 |
| `WALK_SPEED` | `5` | 行走時間係數；行走時間 = 距離 × 此值後四捨五入（值越大代表移動越慢） |
| `VISIT_TIME` | `30` | 每個點的停留拜訪時間（分鐘） |
| `START_POSITION` | `(0, 0)` | 工人的預設起始座標 |

> 💡 `WALK_SPEED` 命名為「speed」，但在公式中是作為「每單位距離所需時間」的乘數使用，數值越大移動越慢。

---

## 座標檔格式

`coordinates.txt` 為純文字檔，**每一行代表一個拜訪點**，格式為以空白分隔的兩個整數：

```
10 1
3 4
8 2
4 1
1 2
4 8
9 8
10 3
```

- 座標必須為整數（程式以 `int` 解析）。
- 以單一空白字元分隔 `x` 與 `y`。

### 自動產生座標

執行 `build_coord.py` 會隨機產生 **8 個不重複**、範圍在 `1~10` 之間的整數座標並覆寫 `coordinates.txt`：

```bash
python build_coord.py
```

---

## 路徑視覺化（Pillow）

模擬結束後，`visualizer.py` 中的 `draw_paths()` 會把每位工人的路徑畫成一張 PNG 圖片。

### 函式簽名

```python
draw_paths(workers, filename="path.png", img_size=600, margin=60, dot_r=8)
```

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `workers` | — | 工人清單（`sim.workers`），每個工人需有 `.path` 屬性 |
| `filename` | `"path.png"` | 輸出圖片路徑；若含資料夾會自動建立 |
| `img_size` | `600` | 輸出圖片的邊長（像素，正方形） |
| `margin` | `60` | 畫布四周留白（像素） |
| `dot_r` | `8` | 每個拜訪點圓點的半徑（像素） |

### 繪圖規則

- **自動縮放**：先找出所有座標的最小/最大值，把資料範圍等比例縮放填滿畫布（扣除 `margin`）。
- **Y 軸翻轉**：數學座標 y 往上、圖片像素 y 往下，程式以 `(max_y - y)` 翻轉，確保圖形方向正確。
- **每位工人一種顏色**：內建 4 色循環 `#e63946`、`#1d7874`、`#f4a261`、`#457b9d`。
- **標示拜訪順序**：每個圓點旁標上數字（`0` 為起點，依序遞增）。
- **自動建立輸出資料夾**：若 `filename` 含目錄（如 `result/picture/`）會自動 `makedirs`。

### 使用方式

`main.py` 已在模擬結束後自動呼叫：

```python
from visualizer import draw_paths
...
sim.run()
draw_paths(sim.workers, "result/picture/two_workers.png")
```

執行後即可在 `result/picture/two_workers.png` 看到兩位工人各自的彩色路徑圖。

---

## 執行範例輸出

以預設的 `coordinates.txt` 與兩位工人（`worker A`、`worker B`，皆起點 `(0, 0)`）執行 `python main.py`，輸出型態如下（實際數值依座標與距離計算而定）：

```
success read 8 visit points
Start simulation
time : 0, worker A will go to (1, 2), need 11 minutes
time : 0, worker B will go to (4, 1), need 21 minutes
time : 11, worker A arrival (1, 2), start visit 30 minutes
...
====================
total use time : XXX
====================
the path of worker A : [(0, 0), (1, 2), (3, 4), ...]
the path of worker B : [(0, 0), (4, 1), (8, 2), ...]
the picture already store with result/picture/two_workers.png
```

- `total use time`：完成所有拜訪所耗費的總時間（tick 數）。
- `the path of worker X`：該工人依序經過的座標路徑（含起點）。
- 最後一行代表路徑圖已成功輸出。

---

## 核心模組說明

### `main.py` — 進入點
建立 `Simulation` 物件、載入座標、加入兩位工人、啟動模擬，並在結束後繪製路徑圖：

```python
sim.add_worker("worker A", start_pos=config.START_POSITION)
sim.add_worker("worker B", start_pos=config.START_POSITION)
sim.run()
draw_paths(sim.workers, "result/picture/two_workers.png")
```

### `simulation.py` — 模擬核心（`Simulation` 類別）

| 方法 | 功能 |
|------|------|
| `load_coordinates()` | 讀取座標檔並存入 `self.points`；讀取失敗時印出提示 |
| `add_worker(name, start_pos)` | 建立並加入一位 `Worker` |
| `_assign_tasks()` | 為每位 idle 工人挑選最近的未拜訪點並指派任務 |
| `run()` | 主迴圈：逐 tick 更新狀態、指派任務，直到全部完成 |
| `_print_summary()` | 印出總耗時與各工人路徑 |

### `worker.py` — 工人狀態機（`Worker` 類別）

| 方法 | 功能 |
|------|------|
| `is_idle()` | 是否為空閒狀態 |
| `set_task(target, current_time, travel_time)` | 指派目標點，進入 walking 或 visiting |
| `update_status(current_time)` | 依時間推進更新狀態（抵達 / 完成拜訪） |

### `visualizer.py` — 路徑繪圖（`draw_paths` 函式）
使用 Pillow 將工人的 `.path` 轉換成圖片：座標縮放 → Y 軸翻轉 → 畫線 → 畫點 → 標順序 → 自動建立資料夾 → 存檔。

### `config.py` — 全域設定
集中管理所有可調參數（見 [設定說明](#設定說明)）。

### `build_coord.py` — 座標產生器
以集合去重，隨機產生 8 個不重複、範圍 `1~10` 的整數座標並寫入 `coordinates.txt`。

---

## 進階用法

### 調整工人數量
在 `main.py` 中增減 `add_worker`。多位空閒工人會各自搶佔離自己最近的點，達成平行拜訪、縮短總耗時：

```python
sim.add_worker("worker A", start_pos=(0, 0))
sim.add_worker("worker B", start_pos=(10, 10))  # 可給不同起點
```

### 自訂圖片大小與輸出位置
```python
draw_paths(sim.workers, "result/picture/my_run.png", img_size=900, dot_r=10)
```

### 調整移動速度與拜訪時間
修改 `config.py` 的 `WALK_SPEED`（移動快慢）與 `VISIT_TIME`（停留長短），即可觀察不同參數對總耗時的影響。
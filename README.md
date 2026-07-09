# visit_path — 多工人訪問路徑模擬器

> 使用「最近點優先」貪婪策略（Nearest-Neighbor Greedy），模擬一位或多位工人依序拜訪一組平面座標點，並統計完成所有拜訪所需的總時間與各自的行走路徑。

一個純 Python、零第三方依賴的離散時間（tick-based）模擬程式。每一個時間單位（tick）代表一分鐘，模擬器會逐分鐘推進，替空閒的工人指派最近的未拜訪點，計算行走時間與停留拜訪時間，最終輸出總耗時與每位工人的完整路徑。

---

## 目錄

- [專案特色](#專案特色)
- [運作原理](#運作原理)
- [專案結構](#專案結構)
- [環境需求](#環境需求)
- [快速開始](#快速開始)
- [設定說明](#設定說明)
- [座標檔格式](#座標檔格式)
- [執行範例輸出](#執行範例輸出)
- [核心模組說明](#核心模組說明)
- [進階用法](#進階用法)

---

## 專案特色

- 🧭 **貪婪最近點演算法**：每次替空閒工人挑選離目前位置「歐幾里得距離最短」的未拜訪點。
- 👷 **支援多工人**：可同時加入多位工人平行拜訪（透過 `add_worker` 加入即可）。
- ⏱️ **離散時間模擬**：以一分鐘為單位逐格推進，清楚呈現「行走中 → 拜訪中 → 完成」的狀態轉換。
- 📄 **座標資料外部化**：拜訪點來自 `coordinates.txt`，可搭配 `build_coord.py` 隨機產生。
- 🪶 **零依賴**：僅使用 Python 標準函式庫（`math`、`random`），免安裝任何套件。

---

## 運作原理

模擬器採用「離散時間迴圈」，每一個 tick（可視為 1 分鐘）執行下列步驟：

1. **更新狀態**：檢查每位工人是否已抵達目標或完成拜訪，更新其狀態（`walking` / `visiting` / `idle`）。
2. **指派任務**：對每位 `idle` 的工人，從剩餘座標點中挑選距離最近者，計算行走時間並指派。
3. **推進時間**：`current_time += 1`，重複上述流程，直到「所有點都被拜訪完」且「所有工人都回到 idle」。

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
├── main.py           # 程式進入點：建立模擬、載入座標、加入工人、執行
├── simulation.py     # Simulation 類別：載入座標、任務指派、主迴圈、結果統計
├── worker.py         # Worker 類別：工人狀態機（idle/walking/visiting）
├── config.py         # 全域參數設定（座標檔名、速度、拜訪時間、起點）
├── build_coord.py    # 工具：隨機產生不重複座標並寫入 coordinates.txt
└── coordinates.txt   # 拜訪點座標資料（每行一組 "x y"）
```

---

## 環境需求

- **Python 3.8+**（使用了 `math.dist`，需 Python 3.8 以上）
- 無需安裝任何第三方套件

---

## 快速開始

```bash
# 1. 取得專案
git clone https://github.com/kevinhuang09/visit_path.git
cd visit_path

# 2.（選用）重新隨機產生座標檔
python build_coord.py

# 3. 執行模擬
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

## 執行範例輸出

以預設的 `coordinates.txt` 與單一工人（`worker A`，起點 `(0, 0)`）執行 `python main.py`，輸出型態如下（實際數值依座標與距離計算而定）：

```
success read 8 visit points
Start simulation
time : 0, worker A will go to (1, 2), need 11 minutes
time : 11, worker A arrival (1, 2), start visit 30 minutes
time : 41, worker A complete visit point (1, 2)
...
====================
total use time : XXX
====================
the path of worker A : [(0, 0), (1, 2), (3, 4), ...]
```

- `total use time`：完成所有拜訪所耗費的總時間（tick 數）。
- `the path of worker A`：該工人依序經過的座標路徑（含起點）。

---

## 核心模組說明

### `main.py` — 進入點
建立 `Simulation` 物件、載入座標、加入工人並啟動模擬。若要加入第二位工人，取消對應註解即可：

```python
sim.add_worker("worker A", start_pos=config.START_POSITION)
# sim.add_worker("worker B", start_pos=config.START_POSITION)
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

### `config.py` — 全域設定
集中管理所有可調參數（見 [設定說明](#設定說明)）。

### `build_coord.py` — 座標產生器
隨機產生 8 個不重複整數座標並寫入 `coordinates.txt`。

---

## 進階用法

### 加入多位工人平行拜訪
在 `main.py` 中加入多個 `add_worker`，模擬器會讓每位空閒工人各自搶佔離自己最近的點，達成平行拜訪、縮短總耗時：

```python
sim.add_worker("worker A", start_pos=(0, 0))
sim.add_worker("worker B", start_pos=(10, 10))
```

### 調整移動速度與拜訪時間
修改 `config.py` 的 `WALK_SPEED`（移動快慢）與 `VISIT_TIME`（停留長短），即可觀察不同參數對總耗時的影響。
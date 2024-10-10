# 太空生存戰

一款使用 Pygame 開發的 2D 太空射擊遊戲，玩家需要操控飛船消滅隕石，躲避障礙，獲取道具，挑戰高分。

## 目錄

- [安裝與運行](#安裝與運行)
- [遊戲玩法](#遊戲玩法)
- [遊戲特性](#遊戲特性)
- [代碼結構](#代碼結構)
  - [主程序](#主程序)
  - [類定義](#類定義)
    - [Player 類](#player-類)
    - [ROCK 類](#rock-類)
    - [Bullet 類](#bullet-類)
    - [Explosion 類](#explosion-類)
    - [Power 類](#power-類)
  - [輔助函數](#輔助函數)
- [資源文件](#資源文件)
- [操作說明](#操作說明)
- [致謝](#致謝)

## 安裝與運行

1. **環境要求**：
   - Python 3.x
   - Pygame 庫
   - Numpy 庫

2. **安裝依賴**：

   ```bash
   pip install pygame numpy
   ```

3. **克隆或下載項目代碼**。

4. **運行遊戲**：

   ```bash
   python game.py
   ```

## 遊戲玩法

- 使用左右方向鍵或 `A`、`D` 鍵控制飛船移動。
- 按下空格鍵 `SPACE` 發射子彈。
- 獲取道具提升武器等級或增加護盾值。
- 消滅隕石獲取分數，挑戰更高得分。
- 當生命值耗盡時，遊戲結束，可選擇重新開始。

## 遊戲特性

- **多樣的隕石**：隕石有不同的外觀和移動軌跡，增加遊戲趣味性。
- **豐富的道具**：包括護盾和武器升級兩種道具，提升玩家生存能力。
- **炫酷的特效**：爆炸效果和聲音增強遊戲體驗。
- **暫停功能**：按下 `Q` 鍵暫停遊戲，`W` 鍵繼續遊戲。

## 代碼結構

### 主程序

```python
# 遊戲初始化和創建窗口
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME")
clock = pygame.time.Clock()
```

- 初始化 Pygame 模塊，設置遊戲窗口大小和標題。

### 類定義

#### Player 類

```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # 初始化玩家屬性，包括圖像、位置、速度、生命值等
    def update(self):
        # 更新玩家位置和狀態
    def shoot(self):
        # 玩家射擊方法
    def hide(self):
        # 玩家隱藏（重生）方法
    def gunup(self):
        # 武器升級方法
```

- **功能**：控制玩家飛船的屬性和行為，包括移動、射擊、受傷和獲取道具等。

#### ROCK 類

```python
class ROCK(pygame.sprite.Sprite):
    def __init__(self):
        # 初始化隕石屬性，包括圖像、位置、速度等
    def rotate(self):
        # 隕石旋轉方法
    def update(self):
        # 更新隕石位置和狀態
```

- **功能**：生成並控制隕石的運動和旋轉，使其在屏幕上隨機出現和移動。

#### Bullet 類

```python
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # 初始化子彈屬性，包括圖像、位置、速度等
    def update(self):
        # 更新子彈位置，超出屏幕則銷毀
```

- **功能**：控制子彈的生成和移動，用於擊毀隕石。

#### Explosion 類

```python
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        # 初始化爆炸效果，包括動畫幀、位置等
    def update(self):
        # 更新爆炸動畫幀，播放完畢後銷毀
```

- **功能**：處理隕石和玩家爆炸時的動畫效果，增強視覺體驗。

#### Power 類

```python
class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        # 初始化道具屬性，包括類型、圖像、位置、速度等
    def update(self):
        # 更新道具位置，超出屏幕則銷毀
```

- **功能**：生成遊戲道具，玩家獲取後可提升武器等級或恢復生命值。

### 輔助函數

- `draw_text(surf, text, size, x, y)`：在屏幕上繪製文字。
- `new_rock()`：生成新的隕石並加入精靈組。
- `draw_health(surf, hp, x, y)`：繪製玩家生命值條。
- `draw_lives(surf, lives, img, x, y)`：繪製剩餘生命數。
- `draw_init()`：顯示遊戲開始界面。
- `draw_end(score)`：顯示遊戲結束界面。
- `game_stop()` 和 `game_go()`：控制遊戲暫停和繼續。

## 資源文件

- **圖像資源**：
  - 玩家飛船：`player.png`
  - 子彈：`bullet.png`
  - 隕石：`rock0.png` 至 `rock6.png`
  - 爆炸效果：`expl0.png` 至 `expl8.png`
  - 玩家爆炸效果：`player_expl0.png` 至 `player_expl8.png`
  - 道具：`shield.png`（護盾），`gun.png`（武器升級）

- **音頻資源**：
  - 背景音樂：`background.ogg`
  - 射擊聲音：`shoot.wav`
  - 爆炸聲音：`expl0.wav`，`expl1.wav`
  - 道具聲音：`pow0.wav`（護盾），`pow1.wav`（武器升級）
  - 玩家死亡聲音：`rumble.ogg`

## 操作說明

- **移動**：按下左/右方向鍵或 `A`/`D` 鍵移動飛船。
- **射擊**：按下空格鍵 `SPACE` 發射子彈。
- **暫停/繼續**：
  - 暫停遊戲：按下 `Q` 鍵。
  - 繼續遊戲：按下 `W` 鍵。
- **退出遊戲**：點擊窗口關閉按鈕或在遊戲結束界面選擇“不”。

## 致謝

- 感謝 Pygame 社區提供的優秀遊戲開發庫。
- 音頻和圖像資源來源於網絡，版權歸原作者所有。



Practice using python to write a simple 2D game, refer to this youtube video
https://www.youtube.com/watch?v=61eX0bFAsYs&t=382&ab_channel=GrandmaCan-%E6%88%91%E9%98%BF%E5%AC%A4%E9%83%BD%E6%9C%83

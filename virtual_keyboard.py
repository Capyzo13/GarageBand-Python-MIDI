import pygame
import mido
import time

# MIDIポートの設定
# 'virtual=True' を指定することで、MacのCoreMIDI上に仮想MIDIポートを作成します
try:
    # midoは内部でpython-rtmidi等を使用して仮想ポートを作成します
    port = mido.open_output('Python Virtual Keyboard', virtual=True)
    print("仮想MIDIポート 'Python Virtual Keyboard' を作成しました。")
except Exception as e:
    print(f"MIDIポートの作成に失敗しました: {e}")
    print("ヒント: pip install mido python-rtmidi pygame を実行して必要なライブラリをインストールしてください。")
    exit(1)

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("GarageBand Virtual Keyboard")

# キーボード(PC)からMIDIノートへのマッピング (ドレミファソラシド)
# Z, X, C, V, B, N, M, , などを白鍵に見立てる
# S, D, G, H, J などを黒鍵に見立てる
key_mapping = {
    pygame.K_z: 60, # C4 (ド)
    pygame.K_s: 61, # C#4
    pygame.K_x: 62, # D4 (レ)
    pygame.K_d: 63, # D#4
    pygame.K_c: 64, # E4 (ミ)
    pygame.K_v: 65, # F4 (ファ)
    pygame.K_g: 66, # F#4
    pygame.K_b: 67, # G4 (ソ)
    pygame.K_h: 68, # G#4
    pygame.K_n: 69, # A4 (ラ)
    pygame.K_j: 70, # A#4
    pygame.K_m: 71, # B4 (シ)
    pygame.K_COMMA: 72, # C5 (ド)
}

pressed_keys = set()

print("ウィンドウをアクティブにして、Z, X, C... キーを押してみてください。")
print("終了するにはウィンドウを閉じてください。")

running = True
font = pygame.font.SysFont(None, 24)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key in key_mapping and event.key not in pressed_keys:
                note = key_mapping[event.key]
                # ノートオン (音を鳴らす) velocityは音の強さ(0-127)
                msg = mido.Message('note_on', note=note, velocity=100)
                port.send(msg)
                pressed_keys.add(event.key)
                print(f"Note ON: {note} (Key: {pygame.key.name(event.key)})")
                
        elif event.type == pygame.KEYUP:
            if event.key in key_mapping and event.key in pressed_keys:
                note = key_mapping[event.key]
                # ノートオフ (音を止める)
                msg = mido.Message('note_off', note=note, velocity=0)
                port.send(msg)
                pressed_keys.remove(event.key)
                print(f"Note OFF: {note} (Key: {pygame.key.name(event.key)})")

    screen.fill((30, 30, 30))
    # 画面に状態を表示
    text1 = font.render("Python -> GarageBand MIDI Keyboard", True, (255, 255, 255))
    text2 = font.render("Press Z,X,C,V,B,N,M for Piano Keys", True, (200, 200, 200))
    
    active_keys_str = " ".join([pygame.key.name(k).upper() for k in pressed_keys])
    text3 = font.render(f"Pressing: {active_keys_str}", True, (100, 255, 100))
    
    screen.blit(text1, (30, 50))
    screen.blit(text2, (30, 90))
    screen.blit(text3, (30, 150))
    
    pygame.display.flip()
    time.sleep(0.01)

pygame.quit()
port.close()
print("終了しました。")

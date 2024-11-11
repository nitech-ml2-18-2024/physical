import pyaudio
import numpy as np
from scipy.io.wavfile import write

# 設定
RATE = 44100 # サンプリングレート
CHUNK = 1024  # フレームサイズ
THRESHOLD = 0.04  # インパルス検出の閾値（ノイズに応じて調整）

# PyAudioの初期化
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Listening for impulse...")
prevolume = 0
try:
    while True:
        # 音声データの取得
        data = stream.read(CHUNK, exception_on_overflow=False)
        # numpy配列に変換
        audio_data = np.frombuffer(data, dtype=np.float32)
        
        # 音量の絶対値の平均を計算
        volume = np.linalg.norm(audio_data) / np.sqrt(len(audio_data))
        
        # 閾値と比較してインパルスを検出
        if prevolume - volume > THRESHOLD:
            print("Impulse detected! Volume:", volume)
        prevolume = volume
except KeyboardInterrupt:
    print("Stopped listening.")

# 終了処理
stream.stop_stream()
stream.close()
p.terminate()
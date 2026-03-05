from flask import Flask, jsonify, request, send_from_directory
import random
import os

app = Flask(__name__, static_folder='.')

# 每個 session 用 session_id 區分，這裡用簡單的 dict 存遊戲狀態
games = {}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/new', methods=['POST'])
def new_game():
    """開始新遊戲，回傳 game_id"""
    game_id = str(random.randint(100000, 999999))
    answer = random.randint(1, 100)
    games[game_id] = {
        'answer': answer,
        'min': 1,
        'max': 100,
        'attempts': 0,
        'done': False
    }
    print(f"[新遊戲] ID={game_id}  秘密答案={answer}")  # 只有你看得到
    return jsonify({'game_id': game_id})

@app.route('/api/guess', methods=['POST'])
def guess():
    """接收猜測，回傳結果"""
    data = request.json
    game_id = data.get('game_id')
    guess_val = data.get('guess')

    if game_id not in games:
        return jsonify({'error': '遊戲不存在，請重新開始'}), 404

    game = games[game_id]

    if game['done']:
        return jsonify({'error': '遊戲已結束'}), 400

    if not isinstance(guess_val, int) or guess_val < 1 or guess_val > 100:
        return jsonify({'error': '請輸入 1~100 的整數'}), 400

    game['attempts'] += 1
    answer = game['answer']

    if guess_val > answer:
        game['max'] = guess_val - 1
        result = 'too_high'
        message = f'{guess_val} 太大了！往下猜'
    elif guess_val < answer:
        game['min'] = guess_val + 1
        result = 'too_low'
        message = f'{guess_val} 太小了！往上猜'
    else:
        game['done'] = True
        result = 'correct'
        message = f'答對了！你猜了 {game["attempts"]} 次！'

    return jsonify({
        'result': result,
        'message': message,
        'min': game['min'],
        'max': game['max'],
        'attempts': game['attempts'],
        'done': game['done']
    })

if __name__ == '__main__':
    print("=" * 45)
    print("  🎯 猜數字遊戲 Server 啟動中...")
    print("=" * 45)
    print("  本機玩：  http://localhost:5000")
    print("  區網玩：  先查你的 IP，例如 http://192.168.1.x:5000")
    print("  查 IP：   Windows 用 ipconfig | Mac/Linux 用 ifconfig")
    print("=" * 45)
    app.run(host='0.0.0.0', port=5000, debug=False)

"""終極密碼客戶端：輸入整數猜答案，輸入 q 離開。"""

import socket

HOST = "127.0.0.1"
PORT = 5000


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            with client.makefile("rb") as reader:
                while True:
                    raw = reader.readline()
                    if not raw or not raw.endswith(b"\n"):
                        print("伺服器已斷線。")
                        return
                    parts = raw.decode("utf-8").split()
                    if len(parts) == 2 and parts[0] == "CORRECT":
                        print(f"猜中了！答案是 {int(parts[1])}。")
                        return
                    if len(parts) != 3 or parts[0] not in {
                        "READY", "HIGHER", "LOWER", "INVALID"
                    }:
                        raise ValueError("不認識的伺服器訊息")
                    status, low, high = parts[0], int(parts[1]), int(parts[2])
                    messages = {
                        "READY": "遊戲開始！",
                        "HIGHER": "答案更大。",
                        "LOWER": "答案更小。",
                        "INVALID": "輸入無效，請輸入目前範圍內的整數。",
                    }
                    print(f"{messages[status]} 目前範圍：{low}～{high}")
                    guess = input("請猜數字（q 離開）：").strip()
                    if guess.lower() == "q":
                        print("已離開遊戲。")
                        return
                    # 交給伺服器驗證，客戶端不保管答案或決定猜測是否合法。
                    client.sendall((guess + "\n").encode("utf-8"))
    except (KeyboardInterrupt, EOFError):
        print("\n已離開遊戲。")
    except OSError as exc:
        print(f"連線錯誤：{exc}")
    except (UnicodeDecodeError, ValueError) as exc:
        print(f"協定錯誤：{exc}")


if __name__ == "__main__":
    main()

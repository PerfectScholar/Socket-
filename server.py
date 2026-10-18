"""終極密碼伺服器：一次接受一位玩家，遊戲結束後關閉。"""

import random
import socket

HOST = "127.0.0.1"
PORT = 5000


def play(conn):
    answer = random.randint(1, 100)
    low, high = 1, 100
    # readline 會保留未讀完的資料，直到收到換行才交出完整一行。
    with conn.makefile("rb") as reader:
        conn.sendall(f"READY {low} {high}\n".encode("utf-8"))
        while True:
            raw = reader.readline()
            if not raw or not raw.endswith(b"\n"):
                print("玩家已離線。")
                return

            try:
                guess = int(raw.decode("utf-8").strip())
            except (UnicodeDecodeError, ValueError):
                reply = f"INVALID {low} {high}"
            else:
                if not low <= guess <= high:
                    reply = f"INVALID {low} {high}"
                elif guess == answer:
                    conn.sendall(f"CORRECT {answer}\n".encode("utf-8"))
                    print("玩家猜中了！")
                    return
                elif guess < answer:
                    low = guess + 1
                    reply = f"HIGHER {low} {high}"
                else:
                    high = guess - 1
                    reply = f"LOWER {low} {high}"
            conn.sendall((reply + "\n").encode("utf-8"))


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(1)
            print(f"等待玩家連線：{HOST}:{PORT}")
            conn, address = server.accept()
            with conn:
                print(f"玩家已連線：{address}")
                play(conn)
    except KeyboardInterrupt:
        print("\n伺服器已停止。")
    except OSError as exc:
        print(f"網路錯誤：{exc}")


if __name__ == "__main__":
    main()

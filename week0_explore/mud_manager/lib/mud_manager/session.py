import socket
import threading
import time
import re
import sys

class MudManagerError(Exception):
    pass

class ConnectionError(MudManagerError):
    pass

class LoginError(MudManagerError):
    pass

class Timeout(MudManagerError):
    pass

class Session:
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 4000
    DEFAULT_TIMEOUT = 10.0

    IAC = 0xFF
    DONT = 0xFE
    DO = 0xFD
    WONT = 0xFC
    WILL = 0xFB
    SB = 0xFA
    SE = 0xF0

    PROMPT_SENTINEL = "> "

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, timeout=DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.reader_thread = None
        self.buffer = ""
        self.buffer_lock = threading.Lock()
        self.buffer_cv = threading.Condition(self.buffer_lock)
        self.closed = True
        self.last_recv_at = None

    def open(self):
        if self.socket and not self.closed:
            raise MudManagerError("already open")
        try:
            self.socket = socket.create_connection((self.host, self.port), timeout=self.timeout)
            self.closed = False
            self.buffer = ""
            self.last_recv_at = None
            self.start_reader()
            return self
        except Exception as e:
            raise ConnectionError(f"connect {self.host}:{self.port} failed: {str(e)}")

    def is_open(self):
        return self.socket is not None and not self.closed

    def close(self):
        if self.closed:
            return
        self.closed = True
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
        with self.buffer_lock:
            self.buffer_cv.notify_all()
        if self.reader_thread:
            self.reader_thread.join(timeout=1.0)
        self.socket = None
        self.reader_thread = None

    def send_command(self, command):
        if not self.is_open():
            raise MudManagerError("session not open")
        if command == "return" or command == "enter" or command is None:
            line = ""
        else:
            line = str(command)
        
        try:
            self.socket.sendall((line + "\r\n").encode("utf-8", errors="ignore"))
        except Exception as e:
            self.close()
            raise ConnectionError(f"write failed: {str(e)}")
        return line

    def drain(self):
        with self.buffer_lock:
            out = self.buffer
            self.buffer = ""
            return out

    def read_until_quiet(self, quiet_seconds=1.0, timeout=None):
        if not self.is_open():
            raise MudManagerError("session not open")
        
        limit = timeout if timeout is not None else self.timeout
        deadline = time.monotonic() + limit
        
        with self.buffer_lock:
            while True:
                now = time.monotonic()
                remaining_total = deadline - now
                if remaining_total <= 0:
                    break

                if self.last_recv_at and (now - self.last_recv_at) >= quiet_seconds and self.buffer:
                    break

                if self.last_recv_at and self.buffer:
                    wait_for = quiet_seconds - (now - self.last_recv_at)
                else:
                    wait_for = remaining_total

                wait_for = min(wait_for, remaining_total)
                if wait_for <= 0:
                    break
                
                self.buffer_cv.wait(timeout=wait_for)
                if self.closed:
                    break
            
            out = self.buffer
            self.buffer = ""
            return out

    def read_until(self, pattern, timeout=None):
        if not self.is_open():
            raise MudManagerError("session not open")
        
        if isinstance(pattern, str):
            regex = re.compile(re.escape(pattern))
        else:
            regex = pattern

        limit = timeout if timeout is not None else self.timeout
        deadline = time.monotonic() + limit

        with self.buffer_lock:
            while True:
                m = regex.search(self.buffer)
                if m:
                    cut = m.end()
                    out = self.buffer[:cut]
                    self.buffer = self.buffer[cut:]
                    return out
                
                now = time.monotonic()
                remaining = deadline - now
                if remaining <= 0:
                    raise Timeout(f"read_until {pattern} after {limit}s")
                if self.closed:
                    raise ConnectionError("socket closed while waiting")
                
                self.buffer_cv.wait(timeout=remaining)

    def read_until_prompt(self, timeout=None):
        try:
            return self.read_until(self.PROMPT_SENTINEL, timeout=timeout)
        except Timeout:
            print("[MudManager::Session] prompt not detected within timeout; returning buffered content", file=sys.stderr)
            return self.drain()

    def login(self, username, password):
        self.read_until(re.compile(r"By what name do you wish to be known.*\?", re.IGNORECASE))
        self.send_command(username)
        
        self.read_until(re.compile(r"Password", re.IGNORECASE))
        self.send_command(password)
        
        output = self.read_until(re.compile(r"Welcome|Reconnecting|Wrong password", re.IGNORECASE))
        if re.search(r"Reconnecting", output, re.IGNORECASE):
            pass
        elif re.search(r"Welcome", output, re.IGNORECASE):
            self.send_command("") # return
            self.send_command("1") # enter the game
            self.read_until_quiet()
        elif re.search(r"Wrong password", output, re.IGNORECASE):
            raise LoginError("wrong password")

    def start_reader(self):
        def reader_job():
            try:
                while not self.closed:
                    try:
                        chunk = self.socket.recv(4096)
                    except (socket.timeout, TimeoutError):
                        continue
                    except Exception as ex:
                        print(f"[DEBUG] recv exception: {type(ex).__name__}: {ex}", file=sys.stderr)
                        break
                    if not chunk:
                        print("[DEBUG] recv returned empty bytes (connection closed by server)", file=sys.stderr)
                        break
                    text = self.strip_iac(chunk)
                    if text:
                        with self.buffer_lock:
                            self.buffer += text
                            self.last_recv_at = time.monotonic()
                            self.buffer_cv.notify_all()
            except Exception as e:
                print(f"[MudManager::Session] reader error: {type(e).__name__}: {str(e)}", file=sys.stderr)
            finally:
                with self.buffer_lock:
                    self.closed = True
                    self.buffer_cv.notify_all()

        self.socket.settimeout(0.5) # Non-blocking recv with timeout
        self.reader_thread = threading.Thread(target=reader_job, daemon=True)
        self.reader_thread.start()

    def strip_iac(self, data):
        out = bytearray()
        i = 0
        n = len(data)
        while i < n:
            b = data[i]
            if b == self.IAC:
                if i + 1 >= n:
                    break
                nxt = data[i + 1]
                if nxt == self.IAC:
                    out.append(self.IAC)
                    i += 2
                elif nxt in (self.WILL, self.WONT, self.DO, self.DONT):
                    i += 3
                elif nxt == self.SB:
                    j = i + 2
                    while j < n and not (data[j] == self.IAC and j + 1 < n and data[j + 1] == self.SE):
                        j += 1
                    i = j + 2
                else:
                    i += 2
            else:
                out.append(b)
                i += 1
        return out.decode("utf-8", errors="ignore")

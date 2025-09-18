import subprocess
import pyautogui
import time
import os
import sys
import ctypes

import pyscreeze
import PIL

# ✅ ย่อหน้าต่างดำ (cmd) ทันทีเมื่อเริ่มต้น
def minimize_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)  # SW_MINIMIZE = 6
    except:
        pass

def load_accounts(filepath):
    accounts = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split(',')
                if len(parts) == 2:
                    accounts.append((parts[0].strip(), parts[1].strip()))
    return accounts

# ฟังก์ชันคลิก พร้อมระบุ delay แยกตามขั้น
def click_image(image_name, confidence=0.9, timeout=30, delay_after=3):
    print(f"กำลังมองหา: {image_name}")
    image_path = f"images/{image_name}"
    start = time.time()
    while time.time() - start < timeout:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            print(f"เจอปุ่ม {image_name} ที่ตำแหน่ง {location}")
            pyautogui.moveTo(location)
            time.sleep(1)
            pyautogui.click(location)
            time.sleep(delay_after)
            return True
        time.sleep(1)
    print(f"❌ ไม่พบภาพ: {image_name}")
    return False

def start_game_by_taskbar():
    print("🔄 กำลังคลิกไอคอนเกมบน Taskbar...")
    success = click_image("game_icon_taskbar.png", confidence=0.9, timeout=10)
    if success:
        print("✅ เปิดเกมจาก Taskbar แล้ว รอกำลังโหลด...")
        time.sleep(7)
    else:
        print("❌ ไม่พบไอคอนเกมบน Taskbar")

def minimize_window():
    pyautogui.hotkey('win', 'down')

def login_account(username, password):
    print(f"🔐 กำลัง login ID: {username}")

    minimize_console()
    start_game_by_taskbar()

    click_image("patch_button.PNG", delay_after=5)  # ⏳ หน้าเช็คแพตช์
    click_image("next_button_1.PNG")
    click_image("ok_button.PNG")
    click_image("launcher_start.PNG")
    click_image("popup_close.PNG")
    click_image("welcome_click.PNG")

    print("🟡 กำลังพยายามคลิกปุ่มเลือกเซิร์ฟเวอร์...")
    server_btn = pyautogui.locateCenterOnScreen("images/server_ok.PNG", confidence=0.9)
    if server_btn:
        pyautogui.moveTo(server_btn)
        time.sleep(1)
        for _ in range(3):
            pyautogui.click()
            time.sleep(0.5)
        time.sleep(3)
    else:
        print("❌ ไม่พบปุ่มเลือกเซิร์ฟเวอร์")

    # ✅ ช่องไอดี: คลิก 2 ครั้ง + ลบ + พิมพ์ + delay 5 วิ
    click_image("id_box.PNG", delay_after=0.5)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.click()
    time.sleep(0.3)
    for _ in range(9):
        pyautogui.press('backspace')
    pyautogui.write(username)
    time.sleep(5)

    # ✅ ช่องพาสเวิร์ด: คลิก + พิมพ์ + delay 5 วิ
    click_image("password_box.PNG", delay_after=0.5)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.write(password)
    time.sleep(5)

    click_image("login_button.PNG")
    print("✅ เข้าสู่เกมแล้ว รอโหลด 7 วินาที...")
    time.sleep(7)
    minimize_window()
    print(f"✅ ย่อหน้าต่างของ ID {username} แล้ว\n")

if __name__ == "__main__":
    accounts = load_accounts("accounts.txt")
    for username, password in accounts:
        login_account(username, password)
        time.sleep(5)

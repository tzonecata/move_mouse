# keep_unlock.py - Documentație

## Descriere generală
`keep_unlock.py` este un script care mișcă mouse-ul automat la fiecare 60 de secunde pentru 2 secunde, pentru a ține activă o sesiune (de exemplu, pentru a preveni blocare automatică a ecranului). Mișcarea se face stânga-dreapta pe centrul orizontal al ecranului.

---

## Biblioteci utilizate

### 1. **time** (standard library)
```python
import time
```
- Utilizată pentru a măsura intervalele de timp și a introduce pauze (`time.sleep()`).
- În cod: calculează diferența dintre `now` și `last_burst` pentru a determina când să declanșeze următoarea mișcare.

### 2. **threading** (standard library)
```python
import threading
```
- Utilizată pentru a gestiona evenimentele (threadul principal).
- **threading.Event**: obiect care permite comunicarea între fire de execuție. Se folosește `stop_event` pentru a semna când trebuie oprit scriptul.
- În cod: `stop_event.set()` este apelat când se apasă Ctrl+T, iar `stop_event.is_set()` verifică dacă oprirea a fost cerută.

### 3. **pyautogui**
```python
import pyautogui
```
- Bibliotecă pentru controlul mouse-ului și tastaturii la nivel de sistem.
- Funcția principală: `pyautogui.moveTo(x, y, duration)` - mișcă mouse-ul la coordonatele (x, y).
- `pyautogui.size()` - obține rezoluția ecranului (lățime × înălțime).
- `pyautogui.FAILSAFE = True` - oprește scriptul dacă mișți mouse-ul în colțul din stânga sus.

### 4. **keyboard**
```python
import keyboard
```
- Bibliotecă pentru captarea și procesarea apăsărilor de taste la nivel global.
- Funcția: `keyboard.add_hotkey()` - înregistrează o combinație de taste (Ctrl+T) care apelează o funcție.
- **Nota**: Uneori nu funcționează pe toate sistemele, de aceea avem și `pynput` ca fallback.

### 5. **pynput** (mai specific: `pynput.keyboard`)
```python
from pynput import keyboard as pynput_keyboard
```
- O alternativă mai fiabilă la `keyboard` pentru captarea tastelor globale.
- `pynput_keyboard.GlobalHotKeys()` - creează un manager de taste globale.
- Avantaj: funcționează mai bine pe Windows și macOS.

---

## Structura codului și variabile de configurare

### Constante de configurare
```python
INTERVAL_SECONDS = 60       # Pauza între două mișcări (60 secunde)
BURST_DURATION = 2          # Cât timp durează fiecare mișcare (2 secunde)
OFFSET = 150                # Cât de departe stânga și dreapta de centru (150 pixeli)
STEP_PIXELS = 8             # Câți pixeli se mișcă la fiecare pas mic
STEP_DELAY = 0.02           # Pauza între pași (0.02 secunde = mișcare fluidă)
```

---

## Funcții

### 1. `burst_move_center(stop_event: threading.Event)`
**Ce face**: Mișcă mouse-ul stânga-dreapta pe centrul orizontal al ecranului pentru 2 secunde.

**Logica**:
1. Calculează centrul ecranului: `cx = width // 2`, `cy = height // 2`
2. Setează limitele stânga și dreapta: `left_x = cx - OFFSET`, `right_x = cx + OFFSET`
3. Într-o buclă (timp de 2 secunde):
   - Mișcă mouse-ul cu `pyautogui.moveTo(x, cy, duration=0)` (instantaneu, fără animație)
   - Inversează direcția când atinge limitele (`direction = -1` pentru stânga, `direction = 1` pentru dreapta)
   - Face pauze mici între pași pentru a crea o mișcare vizibilă și fluidă
4. Se termină când s-au scurs 2 secunde sau se apasă Ctrl+T.

**De ce `duration=0`?**: Mișcă instantaneu, deci mișcarea vizibilă vine din repetarea în buclă cu `STEP_DELAY`.

### 2. `keep_unlock_loop(stop_event: threading.Event)`
**Ce face**: Bucla principală care repetă `burst_move_center()` la fiecare 60 de secunde.

**Logica**:
1. Calculează `last_burst = time.time() - INTERVAL_SECONDS` (pentru a declanșa imediat în primul ciclu, opțional).
2. În buclă:
   - Verifică dacă au trecut 60 de secunde de la ultima mișcare
   - Dacă da, apelează `burst_move_center()` și actualizează `last_burst`
   - Pauze de 0.5 secunde între verificări (pentru a nu consuma CPU)
3. Se oprește când se apasă Ctrl+T.

### 3. `main()`
**Ce face**: Inițializează scriptul și pune în mișcare bucla principală.

**Pași**:
1. Creează `stop_event = threading.Event()` - evenimentul care semnalează oprire
2. Înregistrează hotkey-ul Ctrl+T:
   - Încearcă `keyboard.add_hotkey()` (dacă biblioteca e disponibilă)
   - De asemenea, înregistrează și cu `pynput_keyboard.GlobalHotKeys()` (mai sigur)
3. Apelează `keep_unlock_loop(stop_event)` - bucla unde se întâmplă magia
4. La oprire (Ctrl+T sau Ctrl+C), oprește hotkey-urile și tipărește "Stopped."

---

## Fluxul de execuție

```
START (main)
  ↓
Creează stop_event
  ↓
Înregistrează Ctrl+T pentru a apela stop_event.set()
  ↓
Intră în keep_unlock_loop():
  ├─ Asteaptă 60 secunde
  ├─ Apelează burst_move_center() → Mouse se mișcă stânga-dreapta pentru 2 secunde
  ├─ Asteaptă din nou 60 secunde
  ├─ Repetă până când se apasă Ctrl+T
  ↓
Oprire hotkey-uri
  ↓
END
```

---

## Cum se utilizează

### Din PowerShell
```powershell
python keep_unlock.py
```

### Din Explorer (dublu-click)
```
keep_unlock.bat
```

### Oprire
- Apasă **Ctrl+T** pentru a opri scriptul corect
- Sau apasă **Ctrl+C** în terminal pentru a opri rapid

---

## Comportament vizibil

- **Fiecare 60 secunde**: Mouse-ul se mișcă rapid stânga-dreapta pentru 2 secunde pe centrul orizontal al ecranului
- **Pauze**: 58 de secunde de inactivitate (mouse nu se mișcă)
- **Viteză**: `STEP_PIXELS = 8` și `STEP_DELAY = 0.02` creează o mișcare vizibilă și fluidă (nu prea rapid, nu prea lent)

---

## Personalizare

Dacă vrei să schimbi comportamentul, editează constantele din CONFIGURARE:

```python
INTERVAL_SECONDS = 120      # Crește pauza la 2 minute
BURST_DURATION = 3          # Mișcă pentru 3 secunde
OFFSET = 200                # Mișcă mai departe (200 pixeli)
STEP_PIXELS = 4             # Mișcare mai lentă (pași mai mici)
STEP_DELAY = 0.05           # Mișcare mai ușor vizibilă (pauze mai lungi)
```

---

## Tratarea erorilor

- **`try/except` la `keyboard.add_hotkey()`**: Dacă biblioteca `keyboard` nu e instalată, scriptul nu crapă, doar o ignoră.
- **`try/except` la `pyautogui.moveTo()`**: Dacă se întâmplă o problemă cu mișcarea, se ignora și se continuă.
- **`pyautogui.FAILSAFE = True`**: Dacă mișți manual mouse-ul în colțul din stânga sus, scriptul se oprește automat (măsură de siguranță).

---

## Cerințe

```
pyautogui
pynput
keyboard (opțional, dar recomandat)
```

Instalare:
```bash
pip install pyautogui pynput keyboard
```

# Turn-Based Battle Game (Python OOP)

Program simulasi pertarungan (battle) menggunakan CLI dan berbasis giliran (*turn-based*) antara dua karakter, dibangun menggunakan konsep **Object-Oriented Programming (OOP)** di Python.

**Identitas Pembuat**
- Nama : Pirlo Syabila Hafuza
- NIM : 2509106008
- Kelas : A1'25

---

## 1. Deskripsi Program

Program ini mensimulasikan pertarungan 1 vs 1 antara dua karakter yang masing-masing memiliki statistik (HP, attack, defence, mana) dan dapat mempelajari serta menggunakan *skill* khusus. Pertarungan berjalan secara bergiliran hingga salah satu karakter kalah (HP mencapai 0).

### Fitur Utama
- Sistem HP dengan validasi otomatis (tidak bisa melebihi 100 atau kurang dari 0).
- Sistem Mana untuk membatasi penggunaan skill.
- Skill dengan *damage multiplier* dan biaya mana masing-masing.
- Batas maksimal jumlah skill yang bisa dipelajari tiap karakter.
- Penghitung otomatis jumlah karakter yang pernah dibuat (`totalCharacter`).
- Alur pertarungan interaktif melalui input pengguna (Basic Attack atau Skill).

---

## 2. Struktur Class

### 2.1 `Character`
Merepresentasikan satu karakter dalam pertarungan.

**Atribut:**
| Atribut | Tipe | Keterangan |
|---|---|---|
| `name` | str | Nama karakter |
| `__health` | int (private) | HP karakter, diakses lewat property `health` |
| `attack` | int | Nilai serangan dasar |
| `defence` | int | Nilai pertahanan |
| `_mana` | int (protected) | Mana yang dimiliki karakter |
| `skills` | list | Kumpulan skill yang dipelajari |
| `totalCharacter` | int (class variable) | Jumlah total karakter yang pernah dibuat |

**Property:**
- `health` (getter) — mengembalikan nilai HP saat ini.
- `health` (setter) — memvalidasi nilai HP:
  - Jika `> 100` → HP diset ke `100`.
  - Jika `< 0` → HP diset ke `0`.
  - Selain itu → nilai disimpan apa adanya.

**Method:**
| Method | Tipe | Fungsi |
|---|---|---|
| `total_character()` | `@classmethod` | Mengembalikan string jumlah total karakter terdaftar |
| `calculate_damage(attack, defence)` | `@staticmethod` | Menghitung damage bersih, minimal `1` |
| `isAlive()` | instance | Mengembalikan `True` jika `health > 0` |
| `takeDamage(damage)` | instance | Mengurangi HP berdasarkan damage yang dihitung dari `defence` |
| `Attacking(target)` | instance | Melakukan basic attack ke `target` |
| `add_skill(skill)` | instance | Menambahkan skill baru (dibatasi `Skill.maxSkill`) |
| `use_skill(skill_name, target)` | instance | Menggunakan skill jika mana mencukupi dan skill dimiliki |

### 2.2 `Skill`
Merepresentasikan kemampuan khusus yang dapat dipelajari karakter.

**Atribut:**
| Atribut | Tipe | Keterangan |
|---|---|---|
| `maxSkill` | int (class variable) | Batas maksimal skill per karakter (default `3`) |
| `name` | str | Nama skill |
| `mana_cost` | int | Mana yang dibutuhkan untuk menggunakan skill |
| `damage_multiplier` | float | Pengali damage dasar saat skill digunakan |

### 2.3 `gameMaster`
Mengatur jalannya pertarungan antara dua objek `Character`.

**Atribut:**
| Atribut | Tipe | Keterangan |
|---|---|---|
| `gameRunning` | bool (class variable) | Status permainan |
| `character1`, `character2` | Character | Dua karakter yang bertarung |

**Method:**
| Method | Fungsi |
|---|---|
| `battleStart()` | Menjalankan loop pertarungan sampai salah satu karakter kalah, mengembalikan pemenang |
| `_Turn(current_character, opponent)` | Menangani satu giliran: menampilkan status, meminta input aksi (Basic Attack / Skill), lalu mengeksekusinya |

---

## 3. Alur Program

1. Dua objek `Skill` atau lebih dibuat, lalu dipelajari oleh masing-masing `Character` via `add_skill()`.
2. Dua objek `Character` dibuat dengan statistik awal (HP, attack, defence, mana).
3. Objek `gameMaster` dibuat dengan kedua karakter tersebut.
4. `battleStart()` dipanggil, memulai loop pertarungan:
   - Tiap giliran, karakter yang aktif diminta memilih aksi lewat input:
     - `1` → Basic Attack.
     - `2` → Menggunakan skill (nama skill diketik manual, atau `back` untuk batal).
   - Setelah aksi dilakukan, giliran berpindah ke karakter lawan.
   - Loop berhenti saat salah satu karakter HP-nya mencapai 0.
5. Program mencetak hasil akhir pertarungan dan total karakter yang pernah dibuat.

---

## 4. Cara Menjalankan

```bash
python nama_file.py
```

Program akan meminta input secara interaktif di terminal setiap giliran karakter (ketik `1`, `2`, nama skill, atau `back` sesuai instruksi yang tampil).

---

## 5. Panduan Pengujian

Berikut skenario yang disarankan untuk menguji fungsionalitas program:

### 5.1 Uji Basic Attack
- Pilih `1` pada giliran karakter aktif.
- **Ekspektasi:** Damage dihitung dari `attack` penyerang dikurangi `defence` target (minimal `1`), HP target berkurang sesuai perhitungan.

### 5.2 Uji Penggunaan Skill (Mana Cukup)
- Pilih `2`, lalu ketik nama skill yang dimiliki karakter (contoh: `Fireball`).
- **Ekspektasi:** Mana berkurang sesuai `mana_cost`, damage ke target dihitung dari `(attack - defence) * damage_multiplier`, giliran berpindah.

### 5.3 Uji Skill dengan Mana Tidak Cukup
- Gunakan skill berulang kali hingga mana karakter kurang dari `mana_cost` skill tersebut.
- **Ekspektasi:** Muncul pesan "Mana ... tidak cukup", giliran **tidak** berpindah (loop input berlanjut).

### 5.4 Uji Skill yang Tidak Dimiliki
- Ketik nama skill yang tidak pernah dipelajari karakter tersebut.
- **Ekspektasi:** Muncul pesan skill tidak dimiliki, giliran tetap berlanjut meminta input ulang.

### 5.5 Uji Batasan Jumlah Skill (`maxSkill`)
- Panggil `add_skill()` lebih dari 3 kali pada satu karakter.
- **Ekspektasi:** Skill ke-4 dan seterusnya ditolak dengan pesan batas maksimal skill tercapai.

### 5.6 Uji Validasi Batas HP
- Set `character.health` secara manual ke nilai `> 100` atau `< 0` (misal `character1.health = 150`).
- **Ekspektasi:** HP otomatis disesuaikan menjadi `100` atau `0`, disertai pesan peringatan.

### 5.7 Uji Kondisi Kemenangan
- Lanjutkan pertarungan hingga HP salah satu karakter mencapai 0.
- **Ekspektasi:** Loop `battleStart()` berhenti, nama pemenang dicetak dengan format `Victory <nama>`.

### 5.8 Uji Penghitung Total Karakter
- Buat beberapa objek `Character` baru, lalu panggil `Character.total_character()`.
- **Ekspektasi:** Nilai yang dikembalikan bertambah sesuai jumlah objek `Character` yang telah dibuat sejak program berjalan.

### 5.9 Uji Input Tidak Valid
- Masukkan input selain `1` atau `2` pada menu aksi.
- **Ekspektasi:** Muncul pesan "Input tidak valid, pilih 1 atau 2.", menu ditampilkan kembali.

---

## 6. Contoh Output (Ringkas)

```
========================================
Battle Start!
Nezha VS MengYa
========================================

=============== Cycle 1 ===============

Giliran Nezha
HP: [100]/[100] | Mana: [50]/[100]

Action
1. Basic Attack
2. Skill
Nezha, Pilih Aksi: 1
Nezha attacking MengYa
MengYa took 11 damage, remaining HP [89]/[100]
...
Nezha memenangkan pertarungan

HASIL PERTARUNGAN: Victory Nezha
Total karakter terdaftar ada: [2]
```

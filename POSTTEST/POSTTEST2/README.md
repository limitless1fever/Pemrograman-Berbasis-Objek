# Turn-Based Battle Game (Python OOP)

Program ini adalah simulasi pertarungan (battle) berbasis giliran atau turn-based antara dua karakter, yang saya buat menggunakan konsep Object-Oriented Programming (OOP) di Python. Lewat program ini saya mencoba menerapkan beberapa konsep OOP sekaligus, mulai dari encapsulation, inheritance, sampai polymorphism, bukan cuma class yang berdiri sendiri-sendiri.

**Identitas Pembuat**
- Nama : Pirlo Syabila Hafuza
- NIM : 2509106008
- Kelas : A1'25

---

## 1. Deskripsi Program

Secara garis besar, program ini mensimulasikan pertarungan 1 lawan 1 antara seorang `Player` dan seorang `Enemy`. Keduanya saya buat sebagai turunan (subclass) dari satu class dasar yang sama, yaitu `Character`, supaya statistik dasarnya (HP, attack, defence, mana) tidak perlu saya tulis ulang di masing-masing class.

Tiap karakter bisa mempelajari skill khusus dan membawa item lewat sistem inventory sendiri. Pertarungan berjalan bergantian antara Player dan Enemy, dan berhenti begitu salah satu dari mereka kehabisan HP.

Beberapa hal yang saya coba terapkan di program ini:
- Validasi otomatis untuk HP, supaya nilainya tidak pernah lebih dari 100 atau kurang dari 0.
- Sistem mana yang membatasi seberapa sering skill bisa dipakai.
- Skill yang punya damage multiplier dan biaya mana masing-masing.
- Batas jumlah skill yang bisa dipelajari satu karakter, diatur lewat `Skill.maxSkill`.
- Sistem Inventory sederhana untuk menyimpan dan memakai item pemulih HP.
- Inheritance antara `Character`, `Player`, dan `Enemy`, di mana masing-masing subclass punya kelakuan unik:
  - `Player` punya peluang Critical Hit (damage dikalikan dua) dan memulihkan sedikit mana setiap kali basic attack.
  - `Enemy` punya resistance yang mengurangi persentase damage yang ia terima.
- Penghitung otomatis berapa banyak karakter yang pernah dibuat selama program berjalan, lewat `totalCharacter`.
- Alur pertarungan yang interaktif, jadi pemain benar-benar memilih aksi lewat input di terminal.

---

## 2. Struktur Class

### 2.1 `Character` (Base Class)

Ini class dasar yang menyimpan semua hal umum yang dimiliki setiap karakter, baik itu Player maupun Enemy nantinya.

**Atribut:**
| Atribut | Tipe | Keterangan |
|---|---|---|
| `name` | str | Nama karakter |
| `__health` | int (private) | HP karakter, hanya bisa diakses lewat property `health` |
| `attack` | int | Nilai serangan dasar |
| `defence` | int | Nilai pertahanan |
| `_mana` | int (protected) | Mana yang dimiliki karakter, diakses lewat property `mana` |
| `skills` | list | Kumpulan skill yang sudah dipelajari karakter |
| `inventory` | Inventory | Objek inventory milik karakter tersebut |
| `totalCharacter` | int (class variable) | Jumlah total karakter yang pernah dibuat sejak program berjalan |

**Property:**
Saya sengaja membungkus `health` dengan property, bukan atribut biasa, karena nilainya perlu divalidasi tiap kali diubah:
- `health` (getter) — mengembalikan HP yang sedang berlaku.
- `health` (setter) — kalau nilainya lebih dari 100, otomatis dipaksa jadi 100 dan muncul pesan peringatan. Kalau kurang dari 0, dipaksa jadi 0 dengan peringatan juga. Selain itu, nilainya disimpan apa adanya.

**Method:**
| Method | Tipe | Fungsi |
|---|---|---|
| `total_character()` | classmethod | Mengembalikan string jumlah total karakter yang sudah pernah dibuat |
| `calculate_damage(attack, defence)` | staticmethod | Menghitung damage bersih dari selisih attack dan defence, minimal 1 supaya tidak pernah 0 atau negatif |
| `isAlive()` | instance | Mengecek apakah karakter masih hidup (`health > 0`) |
| `takeDamage(damage)` | instance | Mengurangi HP berdasarkan damage yang sudah dihitung lewat `calculate_damage` |
| `Attacking(target)` | instance | Melakukan basic attack ke target (nanti di-override di `Player`) |
| `add_skill(skill)` | instance | Menambahkan skill baru ke list `skills`, selama belum melewati batas `Skill.maxSkill` |
| `use_skill(skill_name, target)` | instance | Mencari skill berdasarkan nama, lalu memakainya kalau mana-nya cukup |
| `use_item(item_name)` | instance | Mengambil item dari inventory dan memakainya untuk memulihkan HP |

### 2.2 `Player(Character)`

Subclass dari `Character` yang mewakili karakter yang dikendalikan pemain.

**Atribut tambahan:**
| Atribut | Tipe | Keterangan |
|---|---|---|
| `crit` | float | Peluang terjadinya Critical Hit, defaultnya 0.3 (30%) |

**Method yang saya override:**
| Method | Fungsi |
|---|---|
| `Attacking(target)` | Basic attack versi Player: ada kemungkinan damage dikalikan dua kalau Critical Hit terjadi, dan mana Player otomatis pulih 5 setiap kali menyerang |

### 2.3 `Enemy(Character)`

Subclass dari `Character` yang mewakili karakter lawan.

**Atribut tambahan:**
| Atribut | Tipe | Keterangan |
|---|---|---|
| `resistance` | float | Persentase pengurangan damage yang diterima, defaultnya 0.2 (20%) |

**Method yang saya override:**
| Method | Fungsi |
|---|---|
| `takeDamage(damage)` | Damage yang masuk dikurangi dulu sesuai `resistance`, baru diteruskan ke `takeDamage` milik `Character` |

### 2.4 `Skill`

Class sederhana untuk merepresentasikan satu kemampuan khusus yang bisa dipelajari karakter.

**Atribut:**
| Atribut | Tipe | Keterangan |
|---|---|---|
| `maxSkill` | int (class variable) | Batas maksimal skill yang boleh dimiliki satu karakter, defaultnya 3 |
| `name` | str | Nama skill |
| `mana_cost` | int | Mana yang dibutuhkan untuk memakai skill ini |
| `damage_multiplier` | float | Pengali damage dasar saat skill ini digunakan |

### 2.5 `Inventory`

Saya pisah jadi class sendiri supaya logika penyimpanan item tidak numpuk di `Character`.

**Atribut:**
| Atribut | Tipe | Keterangan |
|---|---|---|
| `items` | dict | Menyimpan data tiap item, berisi `heal` dan `quantity` |

**Method:**
| Method | Fungsi |
|---|---|
| `add_item(name, heal, quantity)` | Menambahkan item baru, atau menambah jumlahnya kalau item itu sudah ada |
| `use_items(name)` | Mengurangi jumlah item dan mengembalikan nama serta nilai heal-nya, kalau stok masih ada |
| `isEmpty()` | Mengecek apakah semua item sudah habis |
| `show_items()` | Menampilkan daftar item yang masih tersisa |

### 2.6 `GameMaster`

Class yang bertugas menjalankan dan mengatur alur pertarungan antara `Player` dan `Enemy`.

**Atribut:**
| Atribut | Tipe | Keterangan |
|---|---|---|
| `gameRunning` | bool (class variable) | Menandai status permainan |
| `Player`, `Enemy` | Character | Dua karakter yang sedang bertarung |

**Method:**
| Method | Fungsi |
|---|---|
| `battleStart()` | Menjalankan loop pertarungan sampai salah satu karakter kalah, lalu mengembalikan hasil akhirnya |
| `_Turn(current_character, opponent)` | Mengurus satu giliran: menampilkan status HP/mana, meminta pemain memilih aksi, lalu mengeksekusinya |

---

## 3. Alur Program

Secara ringkas, begini urutan jalannya program dari awal sampai selesai:

1. Beberapa objek `Skill` dibuat terlebih dahulu, seperti `Fireball`, `Wind Slash`, dan `Ice Bullet`.
2. Objek `Player` dan `Enemy` dibuat dengan statistik awal masing-masing (HP, attack, defence, mana).
3. Skill-skill tadi "dipelajari" oleh karakter lewat `add_skill()`, dan item ditambahkan ke inventory Player lewat `inventory.add_item()`.
4. Objek `GameMaster` dibuat dengan membawa kedua karakter tersebut.
5. `battleStart()` dipanggil, dan pertarungan pun dimulai:
   - Setiap giliran, karakter yang sedang aktif akan diminta memilih aksi:
     - `1` untuk Basic Attack.
     - `2` untuk memakai skill (nama skill diketik manual, atau ketik `back` kalau mau batal).
     - `3` untuk memakai item (sama, bisa diketik `back`).
   - Kalau aksinya berhasil dilakukan, giliran langsung berpindah ke lawan.
   - Loop ini terus berjalan sampai salah satu karakter HP-nya habis.
6. Setelah pertarungan selesai, program mencetak hasil akhirnya beserta total karakter yang sudah pernah dibuat.

---

## 4. Cara Menjalankan

```bash
python nama_file.py
```

Setelah dijalankan, program akan meminta input secara interaktif di terminal pada setiap giliran karakter — bisa berupa angka (`1`, `2`, `3`), nama skill/item, atau `back` sesuai instruksi yang muncul di layar.

---

## 5. Panduan Pengujian

Berikut beberapa skenario yang saya gunakan untuk memastikan program ini berjalan sesuai yang saya rencanakan:

### 5.1 Uji Basic Attack (Player)
Pilih `1` pada giliran Player. Seharusnya damage dasar dihitung seperti biasa, tapi ada kemungkinan Critical Hit muncul (damage jadi dua kali lipat) sesuai nilai `crit`, dan mana Player akan bertambah 5.

### 5.2 Uji Basic Attack ke Enemy (Resistance)
Serang Enemy lewat basic attack atau skill, lalu perhatikan pesan yang muncul. Seharusnya ada pesan "Menahan X% Damage" sebelum HP Enemy berkurang, karena damage sudah dipotong sesuai `resistance` miliknya.

### 5.3 Uji Penggunaan Skill (Mana Cukup)
Pilih `2`, lalu ketik nama skill yang sudah dipelajari karakter, misalnya `Fireball`. Mana seharusnya berkurang sesuai `mana_cost`, dan damage ke target dihitung dari `(attack - defence) * damage_multiplier`.

### 5.4 Uji Skill dengan Mana Tidak Cukup
Pakai skill yang sama berkali-kali sampai mana karakter kurang dari `mana_cost`-nya. Harusnya muncul pesan bahwa mana tidak cukup, dan giliran tidak berpindah — pemain diminta memilih aksi lagi.

### 5.5 Uji Skill yang Tidak Dimiliki
Coba ketik nama skill yang tidak pernah dipelajari karakter tersebut. Seharusnya muncul pesan bahwa skill itu tidak dimiliki, dan giliran tetap berlanjut meminta input ulang.

### 5.6 Uji Penggunaan Item
Pilih `3`, lalu ketik nama item yang dimiliki, misalnya `Potion`. HP seharusnya bertambah sesuai nilai heal-nya (tapi tidak melebihi 100), dan jumlah item di inventory berkurang satu.

### 5.7 Uji Item Habis atau Tidak Dimiliki
Pakai item sampai stoknya habis, atau coba ketik nama item yang memang tidak ada. Kalau inventory sudah kosong, akan muncul pesan "belum memiliki Item"; kalau namanya salah, muncul pesan item tidak ditemukan — keduanya tidak memindahkan giliran.

### 5.8 Uji Batas Jumlah Skill
Panggil `add_skill()` lebih dari tiga kali pada satu karakter. Skill keempat dan seterusnya seharusnya ditolak, dengan pesan bahwa batas maksimal skill sudah tercapai.

### 5.9 Uji Validasi Batas HP
Coba set `health` karakter secara manual ke nilai di atas 100 atau di bawah 0, misalnya `Nezha.health = 150`. HP seharusnya otomatis disesuaikan jadi 100 atau 0, disertai pesan peringatan dari setter.

### 5.10 Uji Kondisi Kemenangan
Lanjutkan pertarungan sampai HP salah satu karakter benar-benar habis. Loop `battleStart()` seharusnya berhenti dan hasil pertarungan dicetak dengan format `Victory [nama pemenang]`.

### 5.11 Uji Penghitung Total Karakter
Buat beberapa objek `Character`, `Player`, atau `Enemy` baru, lalu panggil `Character.total_character()`. Nilainya seharusnya terus bertambah sesuai jumlah objek yang dibuat, termasuk objek `Player` dan `Enemy`, karena keduanya tetap memanggil `__init__` milik `Character` lewat `super()`.

### 5.12 Uji Input Tidak Valid
Masukkan input selain `1`, `2`, atau `3` di menu aksi. Program seharusnya menampilkan pesan bahwa input tidak valid, lalu menu ditampilkan kembali tanpa memindahkan giliran.

---

## 6. Relasi Antar Class

Selain hubungan inheritance antara `Character`, `Player`, dan `Enemy`, saya juga mencoba membedakan tiga jenis relasi "has-a" di program ini berdasarkan seberapa kuat satu objek "memiliki" objek lainnya.

### 6.1 Composition — `Character` dengan `Inventory`

```python
def __init__(self, name, health, attack, defence, mana):
    ...
    self.inventory = Inventory()
```

Objek `Inventory` saya buat langsung di dalam `__init__` milik `Character`, bukan dikirim dari luar. Menurut saya ini termasuk composition, karena `Inventory` tidak pernah berdiri sendiri — ia lahir bersamaan dengan karakter yang memilikinya, dan tidak ada karakter lain yang bisa memakai inventory yang sama. Kalau objek `Character`-nya hilang, otomatis `Inventory` miliknya ikut hilang juga.

### 6.2 Aggregation — `Character` dengan `Skill`

```python
fireball = Skill("Fireball", 20, 2.5)
Nezha.add_skill(fireball)
```

Berbeda dengan Inventory, objek `Skill` saya buat terlebih dahulu di luar class `Character`, baru kemudian "dititipkan" lewat `add_skill()`. Ini yang saya maksud sebagai aggregation — `Skill` bisa berdiri sendiri lepas dari karakter manapun, dan kalau dipikir-pikir, satu skill yang sama sebenarnya bisa saja dipelajari lebih dari satu karakter sekaligus. Jadi hubungannya lebih longgar dibanding Inventory tadi.

### 6.3 Association — `GameMaster` dengan `Player` dan `Enemy`

```python
Nezha = Player("Nezha", 100, 15, 5, 50)
Mengya = Enemy("MengYa", 100, 12, 4, 40)
game = GameMaster(Nezha, Mengya)
```

`GameMaster` hanya menerima dan menyimpan referensi ke `Player` dan `Enemy` yang sudah selesai dibuat sebelumnya. Saya anggap ini association, relasi paling longgar di antara ketiganya, karena `GameMaster` sama sekali tidak ikut membuat ataupun menentukan siklus hidup kedua karakter itu — ia cuma "memakai" mereka untuk menjalankan pertarungan. Seandainya objek `GameMaster`-nya dihapus, `Nezha` dan `Mengya` tetap ada dan masih bisa dipakai di pertarungan lain.

### Ringkasan

| Relasi | Pasangan Class | Siapa yang membuat objeknya | Seberapa kuat hubungannya |
|---|---|---|---|
| Composition | `Character` — `Inventory` | Dibuat sendiri di dalam `__init__` | Paling kuat, ikut hilang bersama pemiliknya |
| Aggregation | `Character` — `Skill` | Dibuat di luar, baru ditambahkan | Sedang, masih bisa lepas dari satu pemilik |
| Association | `GameMaster` — `Player`/`Enemy` | Dibuat independen, cuma direferensikan | Paling longgar, sekadar memakai |

---

## 7. Contoh Output (Ringkas)

```
========================================
Battle Start
Nezha VS MengYa
========================================

=============== Cycle 1 ===============

Giliran Nezha
HP: [100]/[100] | Mana: [50]/[100]

Action
1. Basic Attack
2. Skill
3. Item
Nezha, Pilih Aksi: 1
Nezha menyerang MengYa

MengYa Menahan 20% Damage
MengYa terkena damage sebesar 12, sisa HP [88]/[100]
...
Nezha memenangkan pertarungan

HASIL PERTARUNGAN: Victory [Nezha]
Total karakter terdaftar ada: [2]
```

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import random
import textwrap
from PIL import Image, ImageTk

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("GO-TICK Login")

        # Load gambar background
        self.bg_image = Image.open("Log in.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Set ukuran window sesuai gambar
        self.root.geometry(f"{self.bg_image.width}x{self.bg_image.height}")

        # Label untuk menampilkan gambar background
        self.canvas = tk.Canvas(self.root, width=self.bg_image.width, height=self.bg_image.height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Entry dan tombol login di atas gambar
        self.username = tk.StringVar()
        self.entry = tk.Entry(self.root, font=("Arial", 14), textvariable=self.username, justify="center")
        self.login_btn = tk.Button(self.root, text="LOGIN", font=("Courier", 14, "bold"), bg="#7f2641", fg="white",
                                   command=self.check_login)

        # Tempatkan elemen di posisi tertentu
        self.canvas.create_window(450, 325, window=self.entry, width=250, height=40)
        self.canvas.create_window(450, 400, window=self.login_btn, width=300, height=68)

    def check_login(self):
        if self.username.get().strip():
            self.root.destroy()
            main_root = tk.Tk()
            app = BioskopApp(main_root)
            main_root.mainloop()
        else:
            messagebox.showwarning("Login Gagal", "Silakan masukkan nama pengguna.")

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import random
import textwrap

class BioskopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pemesanan Tiket Bioskop")
        self.root.geometry("900x600")

        self.riwayat_pemesanan = []

        self.inisialisasi_data()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_pencarian = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pencarian, text="Pencarian & Pemesanan")
        self.buat_tab_pencarian()

        self.tab_struk = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_struk, text="Struk Pembelian")
        self.buat_tab_struk()

        self.tab_history = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_history, text="Riwayat Pemesanan")
        self.buat_tab_history()

        self.film_terpilih = None
        self.jadwal_terpilih = None
        self.kursi_terpilih = []
        self.total_harga = 0

    def inisialisasi_data(self):
        self.bioskop = {
            "CGV": {"lokasi": [f"CGV Cabang {i+1}" for i in range(20)]},
            "Cinepolis": {"lokasi": [f"Cinepolis Cabang {i+1}" for i in range(20)]},
            "XXI": {"lokasi": [f"XXI Cabang {i+1}" for i in range(20)]}
        }

        self.film_database = [
            {"judul": "Avengers: Endgame", "genre": "Action", "durasi": "181 menit", "rating": "PG-13"},
            {"judul": "The Lion King", "genre": "Animation", "durasi": "118 menit", "rating": "PG"},
            {"judul": "Joker", "genre": "Drama", "durasi": "122 menit", "rating": "R"},
            {"judul": "Frozen 2", "genre": "Animation", "durasi": "103 menit", "rating": "PG"},
            {"judul": "Spider-Man: No Way Home", "genre": "Action", "durasi": "148 menit", "rating": "PG-13"}
        ]

        for bioskop in self.bioskop.values():
            bioskop["film"] = random.sample(self.film_database, 3)
            bioskop["jadwal"] = {}

            for film in bioskop["film"]:
                jadwal_film = []
                for i in range(3):
                    waktu = datetime.now().replace(hour=random.randint(10, 22), minute=0, second=0, microsecond=0)
                    waktu += timedelta(days=random.randint(0, 7))
                    harga = random.randint(30000, 70000)
                    kursi_tersedia = []
                    rows = ['A', 'B', 'C', 'D', 'E', 'F']
                    cols = range(1, 11)
                    for row in rows:
                        for col in cols:
                            kursi_tersedia.append(f"{row}{col}")
                    jadwal_film.append({
                        "waktu": waktu,
                        "harga": harga,
                        "kursi_tersedia": kursi_tersedia
                    })
                bioskop["jadwal"][film["judul"]] = sorted(jadwal_film, key=lambda x: x["waktu"])

    def buat_tab_pencarian(self):
        frame_pencarian = ttk.LabelFrame(self.tab_pencarian, text="Pencarian Film", padding="5")
        frame_pencarian.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(frame_pencarian, text="Cari Film:").grid(row=0, column=0, sticky=tk.W)
        self.entry_pencarian = ttk.Entry(frame_pencarian, width=30)
        self.entry_pencarian.grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(frame_pencarian, text="Bioskop:").grid(row=1, column=0, sticky=tk.W)
        self.combo_bioskop = ttk.Combobox(frame_pencarian, values=list(self.bioskop.keys()), width=28)
        self.combo_bioskop.grid(row=1, column=1, sticky=tk.W, padx=5)
        self.combo_bioskop.set("Semua Bioskop")

        self.btn_cari = ttk.Button(frame_pencarian, text="Cari", command=self.cari_film, width=10)
        self.btn_cari.grid(row=0, column=2, rowspan=2, padx=5)
        self.combo_bioskop.bind("<<ComboboxSelected>>", lambda e: None)

        frame_hasil = ttk.LabelFrame(self.tab_pencarian, text="Hasil Pencarian", padding="5")
        frame_hasil.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree_hasil = ttk.Treeview(frame_hasil, columns=("judul", "bioskop", "waktu", "harga"), show="headings", height=6)
        self.tree_hasil.heading("judul", text="Judul Film")
        self.tree_hasil.heading("bioskop", text="Bioskop")
        self.tree_hasil.heading("waktu", text="Waktu Tayang")
        self.tree_hasil.heading("harga", text="Harga")
        self.tree_hasil.column("judul", width=200)
        self.tree_hasil.column("bioskop", width=100)
        self.tree_hasil.column("waktu", width=150)
        self.tree_hasil.column("harga", width=100)

        scrollbar = ttk.Scrollbar(frame_hasil, orient=tk.VERTICAL, command=self.tree_hasil.yview)
        self.tree_hasil.configure(yscrollcommand=scrollbar.set)

        self.tree_hasil.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.tree_hasil.bind("<<TreeviewSelect>>", self.pilih_film)

        frame_pemesanan = ttk.LabelFrame(self.tab_pencarian, text="Pemesanan Tiket", padding="5")
        frame_pemesanan.pack(fill=tk.BOTH, padx=5, pady=5)

        ttk.Label(frame_pemesanan, text="Film:").grid(row=0, column=0, sticky=tk.W)
        self.label_film = ttk.Label(frame_pemesanan, text="-", wraplength=300)
        self.label_film.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(frame_pemesanan, text="Waktu:").grid(row=1, column=0, sticky=tk.W)
        self.label_waktu = ttk.Label(frame_pemesanan, text="-")
        self.label_waktu.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(frame_pemesanan, text="Harga:").grid(row=2, column=0, sticky=tk.W)
        self.label_harga = ttk.Label(frame_pemesanan, text="-")
        self.label_harga.grid(row=2, column=1, sticky=tk.W)

        self.frame_kursi = ttk.Frame(frame_pemesanan)
        self.frame_kursi.grid(row=4, column=1, sticky=tk.W)

        self.btn_pesan = ttk.Button(frame_pemesanan, text="Pesan Tiket", command=self.pesan_tiket, state=tk.DISABLED)
        self.btn_pesan.grid(row=5, column=1, sticky=tk.E, pady=5)

    def buat_tab_struk(self):
        frame_struk = ttk.Frame(self.tab_struk)
        frame_struk.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.text_struk = tk.Text(frame_struk, wrap=tk.WORD, height=15)
        self.text_struk.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_struk, orient=tk.VERTICAL, command=self.text_struk.yview)
        self.text_struk.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.btn_cetak = ttk.Button(self.tab_struk, text="Cetak Struk", command=self.cetak_struk, state=tk.DISABLED)
        self.btn_cetak.pack(side=tk.BOTTOM, pady=5)

    def buat_tab_history(self):
        self.selected_history_index = tk.IntVar(value=-1)
        frame_history = ttk.Frame(self.tab_history)
        frame_history.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.text_history = tk.Text(frame_history, wrap=tk.WORD, height=20)
        self.text_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tombol simpan dan hapus
        btn_frame = ttk.Frame(self.tab_history)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        self.spin_index = ttk.Spinbox(btn_frame, from_=1, to=1, textvariable=self.selected_history_index, width=5)
        self.spin_index.pack(side=tk.LEFT, padx=5)

        self.btn_hapus_riwayat = ttk.Button(btn_frame, text="Hapus Riwayat", command=self.hapus_riwayat_terpilih)
        self.btn_hapus_riwayat.pack(side=tk.LEFT, padx=5)

        self.btn_simpan_riwayat = ttk.Button(btn_frame, text="Simpan ke File", command=self.simpan_riwayat_ke_file)
        self.btn_simpan_riwayat.pack(side=tk.LEFT, padx=5)

        scrollbar = ttk.Scrollbar(frame_history, orient=tk.VERTICAL, command=self.text_history.yview)
        self.text_history.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def tambah_riwayat(self, data_struk):
        self.riwayat_pemesanan.append(data_struk)
        self.perbarui_history()

    def perbarui_history(self):
        self.spin_index.config(to=len(self.riwayat_pemesanan))
        self.text_history.delete(1.0, tk.END)
        for i, item in enumerate(self.riwayat_pemesanan, 1):
            self.text_history.insert(tk.END, f"\n[Riwayat {i}]\n{textwrap.dedent(item).strip()}\n{'-'*40}\n")

    def hapus_riwayat_terpilih(self):
        idx = self.selected_history_index.get() - 1
        if 0 <= idx < len(self.riwayat_pemesanan):
            del self.riwayat_pemesanan[idx]
            messagebox.showinfo("Info", f"Riwayat ke-{idx+1} berhasil dihapus.")
            self.perbarui_history()
        else:
            messagebox.showerror("Error", "Indeks riwayat tidak valid.")

    def simpan_riwayat_ke_file(self):
        try:
            with open("riwayat_pemesanan.txt", "w", encoding="utf-8") as f:
                for i, item in enumerate(self.riwayat_pemesanan, 1):
                    f.write(f"[Riwayat {i}]\n{textwrap.dedent(item).strip()}\n{'-'*40}\n")
            messagebox.showinfo("Sukses", "Riwayat berhasil disimpan ke 'riwayat_pemesanan.txt'")
        except Exception as e:
            messagebox.showerror("Gagal", f"Gagal menyimpan file: {e}")

    def cari_film(self):
        for item in self.tree_hasil.get_children():
            self.tree_hasil.delete(item)

        keyword = self.entry_pencarian.get().lower()
        bioskop_terpilih = self.combo_bioskop.get()

        for bioskop_nama, bioskop_data in self.bioskop.items():
            if bioskop_terpilih != "Semua Bioskop" and bioskop_nama != bioskop_terpilih:
                continue
            for film in bioskop_data["film"]:
                if keyword in film["judul"].lower() or not keyword:
                    for jadwal in bioskop_data["jadwal"][film["judul"]]:
                        if jadwal["waktu"] > datetime.now():
                            self.tree_hasil.insert("", tk.END, values=(
                                film["judul"], bioskop_nama,
                                jadwal["waktu"].strftime("%d/%m/%Y %H:%M"),
                                f"Rp{jadwal['harga']:,}"
                            ))

    def pilih_film(self, event):
        selected_item = self.tree_hasil.selection()
        if not selected_item:
            return
        item = self.tree_hasil.item(selected_item[0])
        values = item["values"]

        self.film_terpilih = {"bioskop": values[1], "judul": values[0]}
        self.jadwal_terpilih = {
            "waktu": datetime.strptime(values[2], "%d/%m/%Y %H:%M"),
            "harga": int(values[3].replace("Rp", "").replace(",", ""))
        }

        self.label_film.config(text=values[0])
        self.label_waktu.config(text=values[2])
        self.label_harga.config(text=values[3])

        self.update_kursi_tersedia()
        self.btn_pesan["state"] = tk.NORMAL

    def update_kursi_tersedia(self):
        for widget in self.frame_kursi.winfo_children():
            widget.destroy()

        self.kursi_terpilih = []

        bioskop_data = self.bioskop[self.film_terpilih["bioskop"]]
        for jadwal in bioskop_data["jadwal"][self.film_terpilih["judul"]]:
            if jadwal["waktu"] == self.jadwal_terpilih["waktu"]:
                kursi_tersedia = sorted(jadwal["kursi_tersedia"])
                rows = ['A', 'B', 'C', 'D', 'E', 'F']
                cols = range(1, 11)
                for row in rows:
                    for col in cols:
                        kursi = f"{row}{col}"
                        btn = tk.Button(self.frame_kursi, text=kursi, width=5, height=2,
                                        command=lambda k=kursi: self.toggle_kursi(k))
                        btn.grid(row=rows.index(row), column=col-1, padx=2, pady=2)
                        btn.config(bg="green")
                break

    def toggle_kursi(self, kursi):
        for widget in self.frame_kursi.winfo_children():
            if widget.cget("text") == kursi:
                if kursi in self.kursi_terpilih:
                    self.kursi_terpilih.remove(kursi)
                    widget.config(bg="green")
                else:
                    self.kursi_terpilih.append(kursi)
                    widget.config(bg="yellow")

    def pesan_tiket(self):
        jumlah_tiket = len(self.kursi_terpilih)
        if jumlah_tiket < 1:
            messagebox.showerror("Error", "Pilih kursi terlebih dahulu")
            return

        self.total_harga = self.jadwal_terpilih["harga"] * jumlah_tiket
        struk = self.generate_struk()
        self.tambah_riwayat(struk)

        self.text_struk.delete(1.0, tk.END)
        self.text_struk.insert(tk.END, struk.strip())

        self.btn_cetak["state"] = tk.NORMAL
        self.notebook.select(self.tab_struk)
        messagebox.showinfo("Sukses", "Pemesanan tiket berhasil!")

    def generate_struk(self):
        return f"""
        {'='*40}
        {'STRUK PEMESANAN TIKET'.center(40)}
        {'='*40}
        Tanggal: {datetime.now().strftime("%d/%m/%Y %H:%M")}

        Bioskop: {self.film_terpilih['bioskop']}
        Film: {self.film_terpilih['judul']}

        Waktu: {self.jadwal_terpilih['waktu'].strftime("%d/%m/%Y %H:%M")}
        Kursi: {', '.join(self.kursi_terpilih)}
        Jumlah: {len(self.kursi_terpilih)} tiket
        Harga: Rp{self.jadwal_terpilih['harga']:,}/tiket
        
        {'-'*40}
        TOTAL: Rp{self.total_harga:,}
        {'='*40}
        
        Terima kasih telah memesan!
        """
        
        self.text_struk.delete(1.0, tk.END)
        self.text_struk.insert(tk.END, textwrap.dedent(struk_text).strip())
    
    def cetak_struk(self):
        messagebox.showinfo("Cetak Struk", "Struk berhasil dikirim ke printer")
        
if __name__ == '__main__':
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()

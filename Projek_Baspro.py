from tkinter import *
from tkinter import messagebox
import random

class KiosApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Kios Makanan Self Service')
        self.root.geometry('400x250')
        self.root.configure(bg="#f0f0f0")

        # --- DATABASE MENU ---
        self.data_menu = {
            "Makanan": [
                ("Nasi Goreng", 15000),
                ("Mie Ayam", 12000),
                ("Sate Ayam", 18000),
                ("Bakso", 13000)
            ],
            "Minuman": [
                ("Es Teh", 5000),
                ("Es Jeruk", 7000),
                ("Kopi Hitam", 4000),
                ("Air Mineral", 3000)
            ],
            "Snack": [
                ("Kentang Goreng", 10000),
                ("Roti Bakar", 12000),
                ("Sosis Bakar", 8000),
                ("Jamur Crispy", 9000)
            ]
        }
        
        self.nama_pelanggan = ""
        self.keranjang = []
        self.total_harga = 0
        self.struk_text_cache = "" 

        self.halaman_login()

    # ==========================================
    # 1. HALAMAN LOGIN
    # ==========================================
    def halaman_login(self):
        self.bersihkan_layar()
        self.root.geometry('400x250')
        
        Label(self.root, text='Selamat Datang', font=('Arial', 16, 'bold'), bg="#f0f0f0").pack(pady=20)
        Label(self.root, text='Silakan Masukkan Nama Anda:', font=('Arial', 11), bg="#f0f0f0").pack()
        
        self.entry_nama = Entry(self.root, width=30, font=('Arial', 12))
        self.entry_nama.pack(pady=10)
        
        Button(self.root, text='MULAI PESAN', width=20, bg="#4CAF50", fg="white", font=('Arial', 11, 'bold'), 
               command=self.proses_login).pack(pady=20)

    def proses_login(self):
        nama = self.entry_nama.get()
        if nama == "":
            messagebox.showwarning("Peringatan", "Nama tidak boleh kosong!")
        else:
            self.nama_pelanggan = nama
            self.halaman_menu()

    # ==========================================
    # 2. HALAMAN MENU
    # ==========================================
    def halaman_menu(self):
        self.bersihkan_layar()
        self.root.geometry('700x650')
        
        # Header
        header_frame = Frame(self.root, bg="#2196F3", height=50)
        header_frame.pack(fill=X)
        Label(header_frame, text=f"Hai, {self.nama_pelanggan}!", font=("Arial", 14, "bold"), bg="#2196F3", fg="white").pack(pady=10)

        # Tombol Kategori
        frame_kategori = Frame(self.root, bg="#f0f0f0")
        frame_kategori.pack(pady=10)
        
        Button(frame_kategori, text="MAKANAN", bg="#FFCDD2", width=15, command=lambda: self.muat_tombol_menu("Makanan")).pack(side=LEFT, padx=5)
        Button(frame_kategori, text="MINUMAN", bg="#C8E6C9", width=15, command=lambda: self.muat_tombol_menu("Minuman")).pack(side=LEFT, padx=5)
        Button(frame_kategori, text="SNACK", bg="#BBDEFB", width=15, command=lambda: self.muat_tombol_menu("Snack")).pack(side=LEFT, padx=5)

        # Area Tombol Menu
        self.frame_tombol_menu = Frame(self.root, bd=2, relief=GROOVE)
        self.frame_tombol_menu.pack(pady=5, padx=20, fill=X)

        # --- INPUT JUMLAH (+/-) ---
        frame_input = Frame(self.root, bg="#f0f0f0")
        frame_input.pack(pady=5)
        Label(frame_input, text="Atur Jumlah Porsi:", bg="#f0f0f0", font=("Arial", 10)).pack(side=LEFT, padx=5)

        Button(frame_input, text="-", width=3, bg="red", fg="white", font=("Arial", 10, "bold"), command=self.kurang_porsi).pack(side=LEFT, padx=2)
        self.entry_jumlah = Entry(frame_input, width=5, justify='center', font=("Arial", 12, "bold"))
        self.entry_jumlah.insert(0, "1")
        self.entry_jumlah.pack(side=LEFT, padx=2)
        Button(frame_input, text="+", width=3, bg="green", fg="white", font=("Arial", 10, "bold"), command=self.tambah_porsi).pack(side=LEFT, padx=2)

        # Default Menu
        self.muat_tombol_menu("Makanan")

        # Keranjang
        Label(self.root, text="Keranjang Pesanan Anda:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=(10,0))
        self.listbox_keranjang = Listbox(self.root, width=70, height=8)
        self.listbox_keranjang.pack(pady=5)

        Button(self.root, text="Hapus Item Terpilih", bg="red", fg="white", font=("Arial", 9), command=self.hapus_item).pack()

        self.label_total = Label(self.root, text="Total: Rp 0", font=("Arial", 16, "bold"), fg="green", bg="#f0f0f0")
        self.label_total.pack(pady=10)

        Button(self.root, text="SELESAI & BAYAR", bg="orange", width=30, font=("Arial", 12, "bold"), command=self.halaman_konfirmasi).pack(pady=10)

    # --- LOGIKA PENDUKUNG MENU ---
    def tambah_porsi(self):
        try:
            v = int(self.entry_jumlah.get())
            self.entry_jumlah.delete(0, END)
            self.entry_jumlah.insert(0, str(v + 1))
        except: self.entry_jumlah.insert(0, "1")

    def kurang_porsi(self):
        try:
            v = int(self.entry_jumlah.get())
            if v > 1:
                self.entry_jumlah.delete(0, END)
                self.entry_jumlah.insert(0, str(v - 1))
        except: self.entry_jumlah.insert(0, "1")

    def muat_tombol_menu(self, kategori):
        for widget in self.frame_tombol_menu.winfo_children():
            widget.destroy()
        Label(self.frame_tombol_menu, text=f"--- Menu {kategori} ---", font=("Arial", 10, "italic")).pack(pady=5)
        for nama, harga in self.data_menu[kategori]:
            Button(self.frame_tombol_menu, text=f"{nama} - Rp {harga:,}", width=40, 
                   command=lambda n=nama, h=harga: self.tambah_ke_keranjang(n, h)).pack(pady=2)

    def tambah_ke_keranjang(self, nama, harga):
        try:
            jml = int(self.entry_jumlah.get())
            if jml <= 0: return
            subtotal = harga * jml
            self.keranjang.append({"nama": nama, "jumlah": jml, "subtotal": subtotal})
            self.listbox_keranjang.insert(END, f"{nama} (x{jml}) = Rp {subtotal:,}")
            self.hitung_total()
        except: pass

    def hapus_item(self):
        try:
            idx = self.listbox_keranjang.curselection()[0]
            self.listbox_keranjang.delete(idx)
            self.keranjang.pop(idx)
            self.hitung_total()
        except: pass

    def hitung_total(self):
        self.total_harga = sum(item['subtotal'] for item in self.keranjang)
        self.label_total.config(text=f"Total: Rp {self.total_harga:,}")

    # ==========================================
    # 3. HALAMAN KONFIRMASI & PREVIEW STRUK
    # ==========================================
    def halaman_konfirmasi(self):
        if not self.keranjang:
            messagebox.showwarning("Kosong", "Keranjang masih kosong!")
            return
            
        self.win_bayar = Toplevel(self.root)
        self.win_bayar.title("Konfirmasi")
        self.win_bayar.geometry("350x250")
        
        Label(self.win_bayar, text="Total Tagihan:", font=("Arial", 12)).pack(pady=20)
        Label(self.win_bayar, text=f"Rp {self.total_harga:,}", font=("Arial", 24, "bold"), fg="blue").pack()
        
        Button(self.win_bayar, text="CETAK STRUK", bg="green", fg="white", font=("Arial", 12, "bold"), 
               command=self.tampilkan_preview_struk).pack(pady=30)

    # --- BAGIAN YANG DIRAPIKAN (RATA TENGAH/SEJAJAR) ---
    def tampilkan_preview_struk(self):
        self.win_bayar.destroy()

        kode = f"TRX-{random.randint(100,999)}"
        
        # Pembuatan Garis Pemisah
        garis = "=" * 42
        garis_tipis = "-" * 42
        
        teks  = f"{garis}\n"
        teks += "   KIOS MAKANAN SELF SERVICE    \n"
        teks += f"{garis}\n"
        teks += f"Pelanggan : {self.nama_pelanggan}\n"
        teks += f"Kode TRX  : {kode}\n"
        teks += f"{garis_tipis}\n"
        
        # --- LOGIKA PERATAAN SEJAJAR (PADDING) ---
        for item in self.keranjang:
            # Gabungkan nama dan jumlah dulu (misal: "Nasi Goreng x2")
            info_item = f"{item['nama']} x{item['jumlah']}"
            
            # Rumus: {teks:<26} artinya siapkan ruang 26 karakter rata kiri
            # Jika teksnya pendek, sisanya diisi spasi kosong sampai "="
            teks += f"{info_item:<26} = Rp {item['subtotal']:,}\n"
            
        teks += f"{garis_tipis}\n"
        
        # Bagian Total juga diratakan sejajar dengan atasnya
        teks += f"{'TOTAL TAGIHAN':<26} = Rp {self.total_harga:,}\n"
        teks += "\n"
        teks += "Status    : BELUM DIBAYAR\n"
        teks += f"{garis}\n"
        teks += "Silakan bawa struk ini ke kasir\n"
        teks += "untuk melakukan pembayaran.\n"
        teks += f"{garis}\n"

        self.struk_text_cache = teks

        self.win_struk = Toplevel(self.root)
        self.win_struk.title("Tampilan Struk")
        self.win_struk.geometry("400x550") # Diperlebar dikit biar muat
        self.win_struk.configure(bg="white")

        Label(self.win_struk, text="PREVIEW STRUK", font=("Arial", 12, "bold"), bg="white").pack(pady=10)

        # Pakai Font 'Courier New' supaya spasi-nya sama lebar (Rapi)
        area_struk = Text(self.win_struk, height=22, width=45, font=("Courier New", 10), bd=2, relief=SOLID)
        area_struk.pack(pady=5, padx=10)
        area_struk.insert(END, teks)
        area_struk.config(state=DISABLED)

        Button(self.win_struk, text="PRINT / SIMPAN", bg="blue", fg="white", font=("Arial", 12, "bold"),
               command=self.proses_print_file).pack(pady=15)

    def proses_print_file(self):
        nama_file = "Struk_Pembayaran.txt"
        with open(nama_file, 'w') as f:
            f.write(self.struk_text_cache)
            
        messagebox.showinfo("Sukses", f"Struk berhasil dicetak!\nFile: {nama_file}")
        
        self.win_struk.destroy()
        self.nama_pelanggan = ""
        self.keranjang = []
        self.total_harga = 0
        self.struk_text_cache = ""
        self.halaman_login()

    def bersihkan_layar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = Tk()
    app = KiosApp(root)
    root.mainloop()
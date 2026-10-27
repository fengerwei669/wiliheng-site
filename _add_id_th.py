# -*- coding: utf-8 -*-
"""给印尼语、泰语落地页写入文案（39 字段，与现有语种结构一致）。"""
import json
import os

B = r"C:\Users\Administrator\leadgen\site"
p = os.path.join(B, "ad_ads_i18n.json")
d = json.load(open(p, encoding="utf-8"))

ID = {
 "meta_title": "Grosir peralatan dapur & meja — pabrik sejak 2018 | Wiliheng",
 "meta_desc": "Gunting dapur, pengupas, talenan, alas silikon, dan peralatan makan 304 dari pabrik sendiri di Yangjiang. MOQ 500 per model, OEM dengan merek Anda.",
 "h1": "Peralatan dapur & meja grosir, langsung dari pabrik",
 "lede": "Kami memproduksi gunting dapur, pengupas, talenan, alas silikon, dan peralatan makan stainless 304 untuk importir, distributor, dan pemilik merek. Sejak 2018 di Yangjiang, Guangdong.",
 "chips": ["MOQ 500 pcs per model", "Logo Anda diukir laser", "Sampel ±1 minggu", "Dokumen ekspor lengkap"],
 "cta_wholesale": "Grosir: daftar harga",
 "cta_oem": "Bahas OEM / merek sendiri",
 "hero_ph": "Email perusahaan",
 "hero_btn": "Daftar harga + katalog (PDF)",
 "hero_note": "PDF + 3–5 model yang cocok, biasanya dalam 24 jam. Tanpa newsletter.",
 "hero_ok": "Terima kasih — kami balas dalam 24 jam.",
 "gallery_title": "Sebagian koleksi kami",
 "gallery_more": "Ini hanya sebagian — kami punya lebih dari 48 lini: peralatan dapur, gunting, alat makan, alas silikon.",
 "cards_title": "Cara kami bekerja",
 "cards_sub": "Inti bisnis kami adalah merek sendiri untuk merek Anda; kami juga menyediakan stok untuk grosir.",
 "card1_t": "Merek sendiri & OEM/ODM",
 "card1_b": "Logo Anda di produk, kemasan Anda, barcode siap jual.",
 "card2_t": "Grosir & distribusi",
 "card2_b": "Stok lini dengan harga pabrik, harga bertingkat dari 500 pcs, waktu kirim terencana.",
 "card3_t": "Ekspor & dokumen",
 "card3_b": "Dokumen ekspor, pengemasan, dan pemuatan kontainer kami urus.",
 "form_title": "Minta penawaran",
 "form_sub": "Sebutkan lini dan jumlah — harga dan model dalam 24 jam.",
 "f_company": "Perusahaan", "f_name": "Nama Anda", "f_email": "Email perusahaan",
 "f_country": "Negara", "f_line": "Lini produk", "f_qty": "Perkiraan jumlah", "f_msg": "Catatan",
 "form_btn": "Kirim permintaan", "form_ok": "Diterima — kami balas dalam 24 jam.",
 "consent": "Saya setuju data saya digunakan untuk menjawab pertanyaan saya.",
 "wa_intent": "Indonesia WhatsApp",
 "f_wa": "WhatsApp (opsional)",
 "privacy": "Kebijakan privasi",
 "foot_note": "MOQ 500 pcs per model. Harga dan waktu kirim dikonfirmasi tertulis. Hanya B2B.",
 "answer": "Wiliheng adalah pabrik peralatan dapur dan meja di Yangjiang, Guangdong, Tiongkok, sejak 2018. Kami memproduksi untuk importir, distributor, dan pemilik merek: material, kemasan, dan logo sesuai spesifikasi Anda, mulai 500 pcs per model.",
 "faq": [["Berapa minimum order?", "500 pcs per model. Untuk stok tersedia, jumlah lebih kecil bisa didiskusikan."],
         ["Berapa lama sampel?", "Biasanya dalam satu minggu setelah spesifikasi dikonfirmasi."],
         ["Bisa produksi dengan merek kami?", "Ya — OEM/ODM dengan logo, kemasan, dan barcode Anda."]],
 "faq_title": "Pertanyaan umum",
}

TH = {
 "meta_title": "ขายส่งอุปกรณ์ครัวและโต๊ะอาหาร — โรงงานตั้งแต่ปี 2018 | Wiliheng",
 "meta_desc": "กรรไกรครัว ที่ปอกเปลือก เขียง แผ่นซิลิโคน และภาชนะ 304 จากโรงงานของเราในหยางเจียง MOQ 500 ชิ้นต่อรุ่น OEM ภายใต้แบรนด์ของคุณ",
 "h1": "อุปกรณ์ครัวและโต๊ะอาหารขายส่ง ตรงจากโรงงาน",
 "lede": "เราผลิตกรรไกรครัว ที่ปอกเปลือก เขียง แผ่นซิลิโคน และภาชนะสแตนเลส 304 สำหรับผู้นำเข้า ผู้ค้าส่ง และเจ้าของแบรนด์ ตั้งแต่ปี 2018 ที่หยางเจียง มณฑลกวางตุ้ง",
 "chips": ["MOQ 500 ชิ้น/รุ่น", "สลักโลโก้ด้วยเลเซอร์", "ตัวอย่างประมาณ 1 สัปดาห์", "เอกสารส่งออกครบ"],
 "cta_wholesale": "ขายส่ง: ใบราคา",
 "cta_oem": "คุยเรื่อง OEM / แบรนด์ของคุณ",
 "hero_ph": "อีเมลบริษัท",
 "hero_btn": "ใบราคา + แคตตาล็อก (PDF)",
 "hero_note": "PDF + 3–5 รุ่นที่เหมาะ ปกติภายใน 24 ชั่วโมง ไม่มีจดหมายข่าว",
 "hero_ok": "ขอบคุณ — เราตอบกลับภายใน 24 ชั่วโมง",
 "gallery_title": "ตัวอย่างสินค้าของเรา",
 "gallery_more": "นี่เป็นเพียงตัวอย่าง — เรามีกว่า 48 ไลน์: อุปกรณ์ครัว กรรไกร เครื่องใช้บนโต๊ะ แผ่นซิลิโคน",
 "cards_title": "วิธีที่เราทำงาน",
 "cards_sub": "ธุรกิจหลักของเราคือ OEM ให้แบรนด์ของคุณ และมีสินค้าพร้อมส่งสำหรับผู้ค้าส่ง",
 "card1_t": "แบรนด์ของคุณ & OEM/ODM",
 "card1_b": "โลโก้บนสินค้า บรรจุภัณฑ์ของคุณ บาร์โค้ดพร้อมขาย",
 "card2_t": "ขายส่ง & ตัวแทนจำหน่าย",
 "card2_b": "สินค้าในสต็อกราคาโรงงาน ราคาขั้นบันไดตั้งแต่ 500 ชิ้น กำหนดเวลาส่งได้",
 "card3_t": "ส่งออก & เอกสาร",
 "card3_b": "เอกสารส่งออก บรรจุภัณฑ์ และการโหลดตู้คอนเทนเนอร์ เราจัดการให้",
 "form_title": "ขอใบเสนอราคา",
 "form_sub": "แจ้งไลน์สินค้าและจำนวน — ราคาและรุ่นภายใน 24 ชั่วโมง",
 "f_company": "บริษัท", "f_name": "ชื่อของคุณ", "f_email": "อีเมลบริษัท",
 "f_country": "ประเทศ", "f_line": "ไลน์สินค้า", "f_qty": "จำนวนโดยประมาณ", "f_msg": "หมายเหตุ",
 "form_btn": "ส่งคำขอ", "form_ok": "ได้รับแล้ว — เราตอบกลับภายใน 24 ชั่วโมง",
 "consent": "ฉันยินยอมให้ใช้ข้อมูลของฉันเพื่อตอบคำถาม",
 "wa_intent": "Thailand WhatsApp",
 "f_wa": "WhatsApp (ไม่บังคับ)",
 "privacy": "นโยบายความเป็นส่วนตัว",
 "foot_note": "MOQ 500 ชิ้นต่อรุ่น ราคาและเวลาจัดส่งยืนยันเป็นลายลักษณ์อักษร B2B เท่านั้น",
 "answer": "Wiliheng เป็นโรงงานอุปกรณ์ครัวและโต๊ะอาหารในหยางเจียง กวางตุ้ง จีน ตั้งแต่ปี 2018 เราผลิตให้ผู้นำเข้า ผู้ค้าส่ง และเจ้าของแบรนด์: วัสดุ บรรจุภัณฑ์ และโลโก้ตามสเปกของคุณ เริ่ม 500 ชิ้นต่อรุ่น",
 "faq": [["จำนวนสั่งซื้อขั้นต่ำเท่าไหร่", "500 ชิ้นต่อรุ่น สำหรับสินค้าพร้อมส่ง สอบถามรุ่นที่มีได้"],
         ["ได้ตัวอย่างเร็วแค่ไหน", "ปกติภายในหนึ่งสัปดาห์หลังยืนยันสเปก"],
         ["ผลิตภายใต้แบรนด์เราได้ไหม", "ได้ — OEM/ODM พร้อมโลโก้ บรรจุภัณฑ์ และบาร์โค้ดของคุณ"]],
 "faq_title": "คำถามที่พบบ่อย",
}

d["id"] = ID
d["th"] = TH
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("id 字段:", len(ID), "｜ th 字段:", len(TH))

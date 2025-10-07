# -*- coding: utf-8 -*-
from lxml import etree
from pathlib import Path
import sys

xml_path = Path(__file__).resolve().parent / "quanlybanan.xml"
print(f"Đang tìm file XML ở: {xml_path}")
if not xml_path.exists():
    sys.exit("❌ Không tìm thấy file quanlybanan.xml! Hãy đặt file cùng thư mục với script này.")

doc = etree.parse(str(xml_path))
print("Đọc file XML thành công!\n")

# ==== DANH SÁCH CÂU XPATH ====
queries = {
    # 1. Lấy tất cả bàn
    "1. Tất cả bàn": "//BANS/BAN",

    # 2. Lấy tất cả nhân viên
    "2. Tất cả nhân viên": "//NHANVIENS/NHANVIEN",

    # 3. Lấy tất cả tên món
    "3. Tên tất cả món": "//MONS/MON/TENMON/text()",

    # 4. Lấy tên nhân viên có mã NV02
    "4. Tên nhân viên có mã NV02": "//NHANVIENS/NHANVIEN[MANV='NV02']/TENV/text()",

    # 5. Lấy tên và số điện thoại của nhân viên NV03
    "5. Tên & SDT nhân viên NV03": "//NHANVIENS/NHANVIEN[MANV='NV03']/TENV/text() | //NHANVIENS/NHANVIEN[MANV='NV03']/SDT/text()",

    # 6. Lấy tên món có giá > 50000
    "6. Tên món có giá > 50000": "//MONS/MON[number(GIA)>50000]/TENMON/text()",

    # 7. Lấy số bàn của hóa đơn HD03
    "7. Số bàn của hóa đơn HD03": "//HOADONS/HOADON[SOHD='HD03']/SOBAN/text()",

    # 8. Lấy tên món có mã M02
    "8. Tên món có mã M02": "//MONS/MON[MAMON='M02']/TENMON/text()",

    # 9. Lấy ngày lập của hóa đơn HD03
    "9. Ngày lập hóa đơn HD03": "//HOADONS/HOADON[SOHD='HD03']/NGAYLAP/text()",

    # 10. Lấy tất cả mã món trong hóa đơn HD01
    "10. Mã món trong hóa đơn HD01": "//HOADONS/HOADON[SOHD='HD01']//CTHD/MAMON/text()",

    # 11. Lấy tên món trong hóa đơn HD01
    "11. Tên món trong hóa đơn HD01": "//MONS/MON[MAMON = //HOADONS/HOADON[SOHD='HD01']//CTHD/MAMON]/TENMON/text()",

    # 12. Lấy tên nhân viên lập hóa đơn HD02
    "12. Tên nhân viên lập hóa đơn HD02": "//NHANVIENS/NHANVIEN[MANV = //HOADONS/HOADON[SOHD='HD02']/MANV]/TENV/text()",

    # 13. Đếm số bàn
    "13. Đếm số bàn": "count(//BANS/BAN)",

    # 14. Đếm số hóa đơn lập bởi NV01
    "14. Đếm hóa đơn do NV01 lập": "count(//HOADONS/HOADON[MANV='NV01'])",

    # 15. Lấy tên tất cả món có trong hóa đơn của bàn số 2
    "15. Tên món trong hóa đơn bàn số 2": "//MONS/MON[MAMON = //HOADONS/HOADON[SOBAN='2']//CTHD/MAMON]/TENMON/text()",

    # 16. Lấy tất cả nhân viên từng lập hóa đơn cho bàn số 3
    "16. Nhân viên lập hóa đơn cho bàn 3": "//NHANVIENS/NHANVIEN[MANV = //HOADONS/HOADON[SOBAN='3']/MANV]/TENV/text()",

    # 17. Lấy tất cả hóa đơn mà nhân viên nữ lập
    "17. Hóa đơn do nhân viên NỮ lập": "//HOADONS/HOADON[MANV = //NHANVIENS/NHANVIEN[GIOITINH='Nữ']/MANV]/SOHD/text()",

    # 18. Lấy tất cả nhân viên từng phục vụ bàn số 1
    "18. Nhân viên lập hóa đơn cho bàn 1": "//NHANVIENS/NHANVIEN[MANV = //HOADONS/HOADON[SOBAN='1']/MANV]/TENV/text()",

    # 19. Lấy tất cả món được gọi nhiều hơn 1 lần trong các hóa đơn
    # (gồm 2 trường hợp: có bất kỳ CTHD nào SOLUONG>1, hoặc cùng món xuất hiện ở >=2 CTHD)
    "19. Món được gọi > 1 lần": "//MONS/MON[ MAMON = //HOADONS//CTHD[SOLUONG>1]/MAMON or MAMON = //HOADONS//CTHD/MAMON[. = preceding::CTHD/MAMON] ]/TENMON/text()",

    # 20. Lấy tên bàn + ngày lập hóa đơn tương ứng SOHD='HD02'
    # (trả về 1 chuỗi 'Tên bàn - Ngày')
    "20. Tên bàn + ngày lập của HD02": "concat(//BANS/BAN[SOBAN=//HOADONS/HOADON[SOHD='HD02']/SOBAN]/TENBAN, ' - ', //HOADONS/HOADON[SOHD='HD02']/NGAYLAP/text())",

}

for title, xp in queries.items():
    try:
        res = doc.xpath(xp)
        if isinstance(res, float):
            print(f"{title}: {res:.0f}")
        elif isinstance(res, list):
            if all(isinstance(x, str) for x in res):
                print(f"{title}: {res}")
            else:
                print(f"{title}:")
                for node in res:
                    print(etree.tostring(node, pretty_print=True, encoding='unicode'))
        else:
            print(f"{title}: {res}")
    except Exception as e:
        print(f"⚠️ Lỗi khi chạy {title}: {e}")

print("\n✅ Hoàn tất kiểm tra XPath cho quanlybanan.xml")

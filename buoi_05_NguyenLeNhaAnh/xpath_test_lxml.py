from lxml import etree
from pathlib import Path
import sys

xml_path = Path(__file__).resolve().parent / "sv.xml"
print(f"Đang tìm file XML ở: {xml_path}")
if not xml_path.exists():
    sys.exit("❌ Không tìm thấy file sv.xml! Hãy đặt file cùng thư mục với script này.")

try:
    tree = etree.parse(str(xml_path))
    print("Đọc file XML thành công!\n")
except Exception as e:
    sys.exit(f"❌ Lỗi đọc XML: {e}")

queries = {
    "1. Tổng số sinh viên (đếm qua node-set)": "//student",
    "2. Tên các sinh viên": "//student/name/text()",
    "3. ID các sinh viên": "//student/id/text()",
    "4. Ngày sinh SV01": "//student[id='SV01']/date/text()",
    "5. Các khoá học (có thể lặp)": "//enrollment/course/text()",
    "6. Thông tin sinh viên đầu tiên (position()=1)": "//student[position()=1]",
    "7. Mã SV đăng ký Vatly203": "//student[id=//enrollment[course='Vatly203']/studentRef]/id/text()",
    "8. Sinh viên học Toan101": "//student[id=//enrollment[course='Toan101']/studentRef]/name/text()",
    "9. Sinh viên học Vatly203": "//student[id=//enrollment[course='Vatly203']/studentRef]/name/text()",
    "10a. Tên SV sinh năm 1997": "//student[starts-with(date,'1997')]/name/text()",
    "10b. Ngày sinh tương ứng (1997)": "//student[starts-with(date,'1997')]/date/text()",
    "11. SV sinh trước 1998": "//student[number(substring(date,1,4)) < 1998]/name/text()",
    "12. Tổng số SV (XPath count)": "count(//student)",
    "13. SV chưa đăng ký môn": "//student[not(id=//enrollment/studentRef)]/name/text()",
    "14. <date> ngay sau <name> của SV01": "//student[id='SV01']/name/following-sibling::date[1]/text()",
    "15. <id> ngay trước <name> của SV02": "//student[id='SV02']/name/preceding-sibling::id[1]/text()",
    "16. Course của SV03": "//enrollment[studentRef='SV03']/course/text()",
    "17. Sinh viên họ Trần": "//student[starts-with(normalize-space(name),'Trần ')]/name/text()",
    "18. Năm sinh SV01": "substring(//student[id='SV01']/date,1,4)",
}

postprocessors = {
    "1. Tổng số sinh viên (đếm qua node-set)": lambda res: f"{len(res)}",
    "5. Các khoá học (có thể lặp)": lambda res: sorted(set(res)),
}

for title, xp in queries.items():
    try:
        res = tree.xpath(xp)
        if title in postprocessors:
            res = postprocessors[title](res)

        if isinstance(res, float):  
            print(f"{title}: {int(res)}")
        elif isinstance(res, list):
            if all(isinstance(x, str) for x in res):
                print(f"{title}: {res}")
            else:
                if title.startswith("1. Tổng số sinh viên"):
                    print(f"{title}: {res}")
                else:
                    print(f"{title}:")
                    for node in res:
                        print(etree.tostring(node, pretty_print=True, encoding="unicode"))
        else:
            print(f"{title}: {res}")

    except Exception as e:
        print(f"⚠️ Lỗi khi chạy {title}: {e}")

print("\n✅ Hoàn tất kiểm tra XPath cho sv.xml")
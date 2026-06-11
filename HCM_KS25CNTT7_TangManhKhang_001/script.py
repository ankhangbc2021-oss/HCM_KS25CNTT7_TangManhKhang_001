"""Hackthon 001"""


def display_menu() -> str:
    """Hiện menu

    Returns:
        str: trả về lựa chọn
    """
    print(
        f"\n{"="*50}\n"
        f"{'quản lý đặt phòng'.upper():^50}\n"
        f"{"="*50}\n"
        "1. Hiển thị danh sách\n"
        "2. Đăng ký lịch đặt phòng mới\n"
        "3. Cập nhật thông tin lịch hẹn\n"
        "4. Hủy/Xóa lịch đặt phòng\n"
        "5. Tìm kiếm lịch đặt phòng\n"
        "6. Thống kê mật độ sử dụng\n"
        "7. Phân loại khung giờ tự động\n"
        "8. Thoát chương trình\n"
        f"{"="*50}"
    )
    return input("Chọn chức năng 1-8: ")


def display_list(my_list: list):
    """Hiển thị có trong list"""
    if not my_list:
        print("Danh sách hiện đang rỗng!")
        return

    title = "{:<7} | {:<25} | {:<25} | {:<15} | {:<15} | {:<15} | {:<25} |".format(
        "Mã BK",
        "Tên phòng",
        "Người đặt",
        "Giờ bắt đầu",
        "Giờ kết thúc",
        "Thời lượng",
        "Phân loại",
    )

    print(f"{"Danh sách đặt phòng".upper():^147}")
    print(title)
    print(f"{'-' * len(title)}")
    for room in my_list:
        print(
            "{:<7} | {:<25} | {:<25} | {:<15} | {:<15} | {:<15} | {:<25} |".format(
                room.get("id"),
                room.get("name"),
                room.get("name_order"),
                room.get("time_start"),
                room.get("time_end"),
                room.get("total_time", "Chưa tính"),
                room.get("status", "Chưa phân loại"),
            )
        )


def get_data_input(prompt: str, type_text: str = "text") -> str:
    """Nhập tự động

    Args:
        prompt (str): Câu hỏi
        type_text (str, optional): Loại type. Defaults to "text".

    Returns:
        str: Trả về số hoặc chữ
    """
    while True:
        user_input = input(prompt).strip()

        if not user_input:
            print("Dữ liệu không được trống")
            continue
        if type_text == "time":
            try:
                value_num = int(user_input)

                if 0 < value_num > 24:
                    print("Giờ phải từ 0-24. Vui lòng nhập lại")
                    continue
                return value_num
            except ValueError:
                print("Vui lòng nhập số")
                continue

        return user_input


def class_room(value: int) -> str:
    """Phân loại

    Args:
        value (int): Tổng giờ

    Returns:
        str: Phân loại
    """
    if value > 6:
        return "Quá tải (Cần xem xét lại)"
    elif value > 4:
        return "Dài"
    elif value > 2:
        return "Tiêu chuẩn"
    else:
        return "Ngắn"


def add_room(my_list: list):
    """Thêm booking"""

    id = get_data_input("Nhập mã BK để thêm: ")
    check_id = [room for room in my_list if id.upper() == room.get("id").upper()]
    if check_id:
        print(f"Mã [{id.upper()}] này đã có rồi")
        return

    name = get_data_input("Nhập tên phòng đặt: ")
    name_order = get_data_input("Nhập tên người đặt: ")
    time_start = get_data_input("Nhập giờ bắt đầu: ", "time")
    time_end = get_data_input("Nhập giờ kết thúc: ", "time")

    total_time = time_end - time_start

    new_room = {
        "id": id.upper(),
        "name": name.title(),
        "name_order": name_order.title(),
        "time_start": time_start,
        "time_end": time_end,
        "total_time": total_time,
        "status": class_room(total_time),
    }

    my_list.append(new_room)
    print("Đã thêm thành công")


def update_room(my_list: list):
    """Cập nhật"""
    if not my_list:
        print("Danh sách hiện đang rỗng!")
        return

    search_id_input = get_data_input("Nhập mã cần cập nhật: ")

    for room in my_list:
        if room.get("id") == search_id_input.upper():
            print("Đã tìm thấy mã:", room.get("id"))
            new_name = get_data_input("Nhập tên phòng đặt mới: ")
            new_time_start = get_data_input("Nhập giờ bắt đầu mới: ", "time")
            new_time_end = get_data_input("Nhập giờ kết thúc mới: ", "time")
            new_total_time = new_time_end - new_time_start

            room["name"] = new_name
            room["time_start"] = new_time_start
            room["time_end"] = new_time_end
            room["total_time"] = new_total_time
            room["status"] = class_room(new_total_time)
            break
    else:
        print("Không tìm thấy")


def delete_room(my_list: list):
    """Xóa booking"""
    if not my_list:
        print("Danh sách hiện đang rỗng!")
        return

    search_id_input = get_data_input("Nhập mã cần xóa: ")

    for room in my_list:
        if room.get("id") == search_id_input.upper():
            print("Đã tìm thấy mã:", room.get("id"))
            choice = get_data_input(
                "Bạn có chắc muốn xóa hủy lịch đặt phòng này không?(Y/N)"
            )
            if choice in ["Y", "y"]:
                my_list.remove(room)
                print("Đã xóa thành công")
                break
            else:
                print("Đã hủy xóa")
    else:
        print("Không tìm thấy")


def search_room(my_list: list):
    """Tìm kiếm theo mã và tên phòng"""

    if not my_list:
        print("Danh sách hiện đang rỗng!")
        return

    search_id = get_data_input("Nhập mã hoặc tên phòng để tìm: ")
    room_list = [
        room
        for room in my_list
        if search_id.lower() in room.get("id").lower()
        or search_id.lower() in room.get("name").lower()
    ]

    if not room_list:
        print("Không tìm thấy phòng nào!")
    else:
        display_list(room_list)


def classify_density(my_list: list):
    """Phân loại mật độ"""
    if not my_list:
        print("Danh sách hiện đang rỗng!")
        return

    full = 0
    long = 0
    nor = 0
    short = 0
    for room in my_list:
        status = room.get("status")

        if status == "Quá tải (Cần xem xét lại)":
            full += 1
        elif status == "Dài":
            long += 1
        elif status == "Tiêu chuẩn":
            nor += 1
        else:
            short += 1

    print("Đã phân loại xong")
    print("Tổng lượt quá tải là:", full)
    print("Tổng lượt dài là:", long)
    print("Tổng lượt tiêu chuẩn là:", nor)
    print("Tổng lượt ngắn là:", short)


def classify_status_auto(my_list: list):
    """Phân loại khung giờ tự động"""
    if not my_list:
        print("Danh sách hiện đang rỗng!")
        return

    for room in my_list:
        time_start = room.get("time_start")
        time_end = room.get("time_end")
        total_time = time_end - time_start

        room["total_time"] = total_time

        room["status"] = class_room(total_time)

    print("Đã phân khung giờ xong")


def main():
    """Thực thi chương trình"""
    booking_room = [
        {
            "id": "BK001",
            "name": "Phòng Thảo Luận A",
            "name_order": "Phòng Marketing",
            "time_start": 9,
            "time_end": 12,
            "total_time": 3,
            "status": "Tiêu chuẩn",
        },
        {
            "id": "BK002",
            "name": "Phòng Thảo Luận B",
            "name_order": "Phòng Tài Chính",
            "time_start": 7,
            "time_end": 12,
            "total_time": 5,
            "status": "Dài",
        },
    ]
    while True:
        choice = display_menu()

        match choice:
            case "1":
                display_list(booking_room)

            case "2":
                add_room(booking_room)

            case "3":
                update_room(booking_room)

            case "4":
                delete_room(booking_room)

            case "5":
                search_room(booking_room)

            case "6":
                classify_density(booking_room)

            case "7":
                classify_status_auto(booking_room)

            case "8":
                print("Bạn đã thoát")
                break

            case _:
                print("Vui lòng chọn 1-8")


if __name__ == "__main__":
    main()

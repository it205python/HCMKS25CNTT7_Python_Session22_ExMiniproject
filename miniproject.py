import logging

logging.basicConfig(
    filename='history.log',
    level=logging.DEBUG,  # Nhìn thấy toàn bộ luồng điều tra từ mức DEBUG trở lên
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def show_menu():
    print("=" * 50)
    print("      SMART ENERGY MONITOR - PHÒNG CƠ ĐIỆN      ")
    print("="*50)
    print("1. Xem danh sách thiết bị giám sát")
    print("2. Cập nhật chỉ số điện tiêu thụ (Check-in)")
    print("3. Kích hoạt trạng thái cảnh báo quá tải")
    print("4. Tính tổng lượng điện & Chi phí năng lượng")
    print("5. Thoát chương trình")
    print("=" * 50)


def show_devices(devices):
    logger.debug(f"Đang tính toán chi phí năng lượng cho {len(devices)} thiết bị")

    if (len(devices) == 0):
        print("Hệ thống hiện chưa có thiết bị giám sát nào!")
        logger.warning("Device list is empty.")
        return

    print("--- DANH SÁCH THIẾT BỊ GIÁM SÁT ---")
    print(f"{'MÃ TB':<8} | {'VỊ TRÍ PHÂN XƯỞNG':<22} | {'CHỈ SỐ CŨ':>10} | {'CHỈ SỐ MỚI':>10} | {'TRẠNG THÁI'}")
    print("-" * 70)

    for item in devices:
        print(f"{item['id']:<8} | {item['location']:<22} | {item['old_index']:>10} | {item['new_index']:>10} | {item['status']}")
    logger.info("Displayed device list successfully.")


def update_indices(devices):
    logger.debug("Starting update indices.")

    device_id = input("Nhập mã thiết bị cần cập nhật chỉ số: ").strip().upper()

    target_device = None

    for item in devices:
        if (item["id"] == device_id):
            target_device = item
            break

    if (target_device is None):
        print("[Lỗi] (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống")
        logger.error(f"Device ID {device_id} not found.")
        return

    while True:
        try:
            old_index = float(input("Nhập chỉ số cũ: "))

            if (old_index < 0):
                print("[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!")
                continue
            break

        except ValueError:
            print("[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!")
            logger.error("Invalid old index input.")

    while True:
        try:
            new_index = float(input("Nhập chỉ số mới: "))

            if (new_index < 0):
                print("[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!")
                continue

            if (new_index < old_index):
                print("[Lỗi] (ERR-E02): Số liệu lỗi! Chỉ số mới không được nhỏ hơn chỉ số cũ!")
                logger.error(
                    f"ERR-E02: new_index={new_index} < old_index={old_index}"
                )
                continue

            break

        except ValueError:
            print("[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!")
            logger.error("Invalid new index input.")

    target_device["old_index"] = old_index
    target_device["new_index"] = new_index

    print(f"[Thành công]: Thiết bị {device_id} đã được cập nhật số liệu mới.")
    logger.info(f"Successfully updated indices for device {device_id}.")


def trigger_overload_alert(devices):
    logger.debug("Starting trigger_overload_alert function.")

    device_id = input("Nhập mã thiết bị cần kích hoạt cảnh báo: ").strip().upper()

    target_device = None

    for item in devices:
        if item["id"] == device_id:
            target_device = item
            break

    if target_device is None:
        print("[Lỗi] (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống!")
        logger.error(f"ERR-E01: Device ID {device_id} not found.")
        return

    if target_device["status"] == "Overload":
        print("[Lỗi] (ERR-E04): Thao tác bị hủy! Thiết bị này đã được kích hoạt trạng thái OVERLOAD từ trước!")
        logger.warning(
            f"ERR-E04: Device {device_id} is already in OVERLOAD state.")
        return

    energy_consumption = (target_device["new_index"] - target_device["old_index"])

    if energy_consumption > 5000:
        target_device["status"] = "Overload"
        print(f"[Thành công]: Thiết bị {device_id} đã được chuyển sang trạng thái OVERLOAD.")
        logger.warning(
            f"Device {device_id} exceeded 5000 kWh. Status changed to OVERLOAD.")
    else:
        print(f"[Thông báo]: Thiết bị {device_id} chưa vượt ngưỡng 5000 kWh nên không cần kích hoạt cảnh báo.")
        logger.info(
            f"Device {device_id} consumption is {energy_consumption} kWh. No overload detected.")


def calculate_energy_financials(devices):
    logger.debug(f"Calculating energy financials for {len(devices)} devices.")

    if (not devices):
        logger.warning("Financial calculation requested with empty device list.")
        return (0.0, 0.0, 0.0)

    total_kwh = 0

    for item in devices:
        total_kwh += (item["new_index"] - item["old_index"])

    base_cost = total_kwh * 3000
    discount_percent = 0

    if (total_kwh >= 50000):
        discount_percent = 3

    final_cost = base_cost * (1 - discount_percent / 100)
    return (total_kwh, discount_percent, final_cost)


def main():
    devices = [
        {'id': 'M01', 'location': 'Mechanical Shop A', 'old_index': 1200, 'new_index': 4500, 'status': 'Normal'},
        {'id': 'M02', 'location': 'Assembly Line B', 'old_index': 2300, 'new_index': 8500, 'status': 'Overload'}
    ]

    while True:
        show_menu()

        choice = input("Mời chọn chức năng (1-5): ")

        match choice:
            case "1":
                show_devices(devices)
            case "2":
                update_indices(devices)
            case "3":
                trigger_overload_alert(devices)
            case "4":
                total_kwh, discount_percent, final_cost = (calculate_energy_financials(devices))

                print("\n===== BÁO CÁO NĂNG LƯỢNG =====")
                print(f"Tổng điện tiêu thụ : {total_kwh:,.0f} kWh")
                print(f"Chiết khấu áp dụng : {discount_percent}%")
                print(f"Tổng tiền thanh toán: {final_cost:,.0f} VND")
            case "5":
                print("Cảm ơn bạn đã sử dụng phần mềm Smart Energy Monitor!")
                print("[Chương trình kết thúc]")
                break
            case _:
                print("[LỖI] Lựa chọn không hợp lệ! Vui lòng chọn lại từ 1 đến 5.")

if __name__ == "__main__":
    main()
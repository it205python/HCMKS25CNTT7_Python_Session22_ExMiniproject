# Test danh sách rỗng
from miniproject import show_devices
def test_empty_devices_list():
    assert show_devices("") == (0.0, 0.0, 0.0)


# Test mốc đạt chiết khấu
from miniproject import calculate_energy_financials
def test_financials_with_discount():
    devices = [
        {"old_index": 0, "new_index": 30000},
        {"old_index": 0, "new_index": 20000}
    ]
    assert calculate_energy_financials(devices)[1] == 3
    assert calculate_energy_financials(devices)[2] == 145500000


# Test mốc không đạt chiết khấu
def test_financials_no_discount():
    devices = [
        {"old_index": 0, "new_index": 20000},
        {"old_index": 0, "new_index": 20000}
    ]
    assert calculate_energy_financials(devices)[1] == 0
    assert calculate_energy_financials(devices)[2] == 120000000.0
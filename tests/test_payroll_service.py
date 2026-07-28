from app.services.payroll_service import calculate_payroll


class FakePosition:
    base_salary = 6000000


class FakeEmployee:
    id = 1
    position = FakePosition()


def make_attendance_class(overtime_hours=5, work_days=22, absent_days=0):
    """Factory to create a fake Attendance class with given attributes."""

    class FakeAttendance:
        query = type(
            "FakeQuery",
            (),
            {
                "filter_by": lambda cls, **kw: type(
                    "FakeFirst",
                    (),
                    {
                        "first": lambda self: type(
                            "FakeAttendanceObj",
                            (),
                            {
                                "overtime_hours": overtime_hours,
                                "work_days": work_days,
                                "absent_days": absent_days,
                            },
                        )()
                    },
                )()
            },
        )()

    return FakeAttendance


def make_salary_component_class():
    """Factory to create a fake SalaryComponent class."""

    class FakeSalaryComponent:
        query = type(
            "FakeQuery",
            (),
            {
                "filter_by": lambda cls, **kw: (
                    type(
                        "FakeAll",
                        (),
                        {
                            "all": lambda self: [
                                type("C", (), {"default_amount": 500000})(),
                                type("C", (), {"default_amount": 750000})(),
                            ]
                        },
                    )()
                    if kw.get("component_type") == "ALLOWANCE"
                    else type(
                        "FakeAll",
                        (),
                        {
                            "all": lambda self: [
                                type("C", (), {"default_amount": 100000})()
                            ]
                        },
                    )()
                )
            },
        )()

    return FakeSalaryComponent


def test_payroll_calculation(monkeypatch):
    """Test with no absent days — full salary."""
    monkeypatch.setattr(
        "app.services.payroll_service.Attendance",
        make_attendance_class(overtime_hours=5, work_days=22, absent_days=0),
    )
    monkeypatch.setattr(
        "app.services.payroll_service.SalaryComponent",
        make_salary_component_class(),
    )

    result = calculate_payroll(FakeEmployee(), "2026-07", bonus=250000)

    # With 0 absent days and 22 work days, base_salary should be full (6000000)
    assert result["base_salary"] == 6000000
    assert result["allowance"] == 1250000
    assert result["overtime"] == 250000
    assert result["bonus"] == 250000
    assert result["gross_salary"] == 7750000
    assert result["net_salary"] < result["gross_salary"]


def test_payroll_calculation_with_absent_days(monkeypatch):
    """Test that absent days reduce base salary proportionally."""
    monkeypatch.setattr(
        "app.services.payroll_service.Attendance",
        make_attendance_class(overtime_hours=5, work_days=22, absent_days=2),
    )
    monkeypatch.setattr(
        "app.services.payroll_service.SalaryComponent",
        make_salary_component_class(),
    )

    result = calculate_payroll(FakeEmployee(), "2026-07", bonus=250000)

    # 2 absent out of 22 days → base = 6000000 * 20/22 ≈ 5454545.45
    expected_base = 6000000 * 20 / 22
    assert abs(result["base_salary"] - expected_base) < 1
    assert result["allowance"] == 1250000
    assert result["net_salary"] < result["gross_salary"]


def test_payroll_calculation_all_absent(monkeypatch):
    """Test that all absent days result in zero base salary."""
    monkeypatch.setattr(
        "app.services.payroll_service.Attendance",
        make_attendance_class(overtime_hours=0, work_days=22, absent_days=22),
    )
    monkeypatch.setattr(
        "app.services.payroll_service.SalaryComponent",
        make_salary_component_class(),
    )

    result = calculate_payroll(FakeEmployee(), "2026-07", bonus=0)

    # 22 absent out of 22 days → base = 0
    assert result["base_salary"] == 0
    assert result["gross_salary"] == 1250000  # only allowance
    assert result["net_salary"] < result["gross_salary"]

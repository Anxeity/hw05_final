from datetime import date


def year(request):
    """Добавляет переменную с текущим годом."""
    today = date.today()
    return {
        'year': today.year
    }

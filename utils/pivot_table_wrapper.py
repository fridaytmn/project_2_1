import templates.flash


def pivot_table_wrapper(func):
    def wrapper(*args, **kwargs):
        table = func(*args, **kwargs)
        if len(table.data) == 0:
            return templates.flash.render("", "По вашему запросу ничего не найдено")
        return table

    return wrapper

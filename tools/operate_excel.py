# 导入模块 ---------------------------------
# pip install
import xlwings as xw
from decimal import Decimal

# 定义函数 ---------------------------------


def init_data():
    # 打开Excel程序，默认设置：程序可见，只打开不新建工作薄，屏幕更新关闭
    app = xw.App(visible=True, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    return app


def init_data_hide():
    # 打开Excel程序，默认设置：程序不可见，只打开不新建工作薄，屏幕更新关闭
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    return app


def get_rng(sht, td, func=None, func_parms=None):
    # 获取单元格
    rng = sht.range(f'{td}')
    if(rng and func):
        # 回调函数
        func_parms and func(rng, func_parms) or func(rng)
    return rng


def clear(rng):
    # 清除内容和格式
    rng.clear()


def style_autofit_col(rng):
    # 设置自动宽度
    rng.columns.autofit()


def style_autofit_row(rng):
    # 设置自动高度
    rng.rows.autofit()


def style_bg_color(rng, color='#336699'):
    # 样式 背景颜色
    rng.color = str(color)


def style_font_color(rng, color='#ffffff'):
    # 样式 字体颜色
    rng.font.color = str(color)


def style_font_bold(rng):
    # 样式 字体粗细
    rng.font.bold = True


def style_font_name(rng, name='等线'):
    # 样式 字体主题
    rng.font.name = str(name)


def get_wb(app, filepath):
    # 获取 工作簿
    wb = app.books.open(filepath)
    return wb


def add_wb(app):
    # 新建 工作簿
    wb = app.books.add()
    return wb


def get_sht(wb, sheet_name='Sheet1'):
    # 获取 工作表
    sht = wb.sheets[sheet_name]
    return sht


def add_sht(wb, sheet_name=None):
    # 新建 工作表
    sht = wb.sheets.add(sheet_name)
    return sht


def get_count_all_shape(sht):
    # 获取 所有 行数 and 列数
    return sht.used_range.shape


def get_count_all_rows(sht):
    # 获取 所有 行数
    return sht.used_range.last_cell.row


def get_count_all_cols(sht):
    # 获取 所有 列数
    return sht.used_range.last_cell.column


def get_count_shape(rng):
    # 获取行数
    return rng.shape


def get_count_rows(rng):
    # 获取行数
    return rng.rows.count


def get_count_cols(rng):
    # 获取行数
    return rng.columns.count


def write_td(sht, data, td):
    # 写入 单元格数据
    sht.range(f'{td}').options(transpose=True).value = data


def get_td_value(sht, th, row, end_row=None):
    # 获取 单元格数据
    rng = sht.range(f'{th}1').expand('table')
    end_row = end_row or rng.rows.count
    td_val = sht.range(f'{th}{row}:{th}{end_row}').value
    return td_val


def calculate_storage(x, float_count="0.1"):
    # 计算 val / 1024  四舍五入 保留一位小数
    return float(Decimal(x/1024).quantize(Decimal(f"{float_count}"), rounding="ROUND_HALF_UP"))


def init_th(sht, data):
    # 初始化表头（第一行）
    col = str(chr(96+len(data)))
    sht.range('A1').value = data
    rng = get_rng(sht, f'A1:{col}1')
    style_autofit_col(rng)
    style_bg_color(rng)
    style_font_color(rng)
    style_font_bold(rng)
    style_font_name(rng)
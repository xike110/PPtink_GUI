from app.WebDemo.utils.WebFunction import Function
import logging
import os
import sys
import time
import json
import re
import datetime


class Verify(Function):
    """
    运行的具体业务代码类
    """

    def __init__(self):
        super().__init__()  # 调用父类构造函数

    def validate_form_field(self, field_name, field_value, validate_method):
        """
        通用表单字段验证函数
        :param field_name: 字段名称
        :param field_value: 字段值
        :param validate_method: 验证方法名称
        :return: (bool, str) 验证结果和错误信息
        """
        if not validate_method:
            return True, None

        # 获取验证方法
        if hasattr(self, validate_method) and callable(getattr(self, validate_method)):
            verify_func = getattr(self, validate_method)
            result = verify_func(field_name, field_value)
            if result is True:
                return True, None
            return False, result
        else:
            self.runlog(f"未找到验证方法: {validate_method}", "warning")
            return True, None

    def get_field_validate_method(self, field_name):
        """
        根据字段名获取验证方法
        :param field_name: 字段名称
        :return: 验证方法名称或None
        """
        if not self.gui_config:
            return None

        # 遍历所有菜单和组件查找匹配的字段
        for menu in self.gui_config.menus:
            # 检查菜单中的组件
            for component in menu.components:
                if component.get("name") == field_name:
                    return component.get("validate")

            # 检查菜单中的分组组件
            for group in menu.groups:
                for component in group.get("components", []):
                    if component.get("name") == field_name:
                        return component.get("validate")

        return None

    def validate_form_data(self, form_data):
        """
        验证表单数据
        :param form_data: 表单数据字典
        :return: (bool, str) 验证结果和错误信息
        """
        if not form_data:
            return True, None

        for field_name, field_value in form_data.items():
            # 获取字段的验证方法
            validate_method = self.get_field_validate_method(field_name)
            if validate_method:
                is_valid, error_msg = self.validate_form_field(field_name, field_value, validate_method)
                if not is_valid:
                    return False, f"{field_name}: {error_msg}"

        return True, None

    def customize_verify(self, key, value):
        """
        文本输入框验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')

        # 长度检查
        if key == 'name':
            if not value or not isinstance(value, str):
                return '请输入有效的文本'
            if len(value) < 1:
                self.runlog(f'验证失败: 输入文字不能少于1个', 'warning')
                return '输入文字不能少于1个'
            if len(value) > 50:
                self.runlog(f'验证失败: 输入文字不能超过50个', 'warning')
                return '输入文字不能超过50个'

        # self.runlog(f'验证通过: {key}', 'info')
        return True

    def password_verify(self, key, value):
        """
        密码框验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}=******', 'info')
        # 密码强度检查
        if key == 'password':
            if len(value) < 6:
                return '密码长度不能少于6个字符'
            if len(value) > 20:
                return '密码长度不能超过20个字符'
            # 检查密码复杂度
            has_digit = any(char.isdigit() for char in value)
            has_letter = any(char.isalpha() for char in value)
            has_special = any(not char.isalnum() for char in value)

            if not (has_digit and has_letter):
                return '密码必须包含数字和字母'
            if not has_special and len(value) < 8:
                return '简单密码长度至少需要8个字符'
        return True

    def integer_verify(self, key, value):
        """
        整数框验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        try:
            # 确保值是整数
            int_value = int(value)

            # 根据不同字段进行范围检查
            if key == 'integer':
                if int_value < 0 or int_value > 100:
                    return '整数值必须在0-100之间'
            return True
        except (ValueError, TypeError):
            return '请输入有效的整数'

    def decimal_verify(self, key, value):
        """
        浮点数框验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        try:
            # 确保值是浮点数
            float_value = float(value)

            # 根据不同字段进行范围检查
            if key == 'decimal':
                if float_value < -5.0 or float_value > 5.0:
                    return '浮点数值必须在-5.0到5.0之间'
                # 检查小数位数
                decimal_places = len(str(float_value).split('.')[-1]) if '.' in str(float_value) else 0
                if decimal_places > 2:
                    return '小数位数不能超过2位'
            return True
        except (ValueError, TypeError):
            return '请输入有效的浮点数'

    def textarea_verify(self, key, value):
        """
        文本域验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        # 长度检查
        if key == 'texts':
            if len(value) < 5:
                return '文本内容不能少于5个字符'
            if len(value) > 500:
                return '文本内容不能超过500个字符'
        return True

    def file_verify(self, key, value):
        """
        文件选择验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        # 检查文件是否存在
        if not os.path.isfile(value):
            return '文件不存在'

        # 检查文件扩展名
        if key == '--Filepath':
            valid_extensions = ['.xlsx', '.xls', '.csv']
            ext = os.path.splitext(value)[1].lower()
            if ext not in valid_extensions:
                return f'文件类型必须是 {", ".join(valid_extensions)}'
        return True

    def multifile_verify(self, key, value):
        """
        多文件选择验证
        参数:
            key (str): 属性名
            value: 属性值列表
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        # 检查是否至少选择了一个文件
        if not value or len(value) == 0:
            return '请至少选择一个文件'

        # 检查每个文件是否存在
        for file_path in value:
            if not os.path.isfile(file_path):
                return f'文件不存在: {file_path}'

        # 检查文件扩展名
        if key == '--allpath':
            valid_extensions = ['.xlsx', '.xls', '.csv', '.txt']
            for file_path in value:
                ext = os.path.splitext(file_path)[1].lower()
                if ext not in valid_extensions:
                    return f'文件类型必须是 {", ".join(valid_extensions)}'
        return True

    def directory_verify(self, key, value):
        """
        目录选择验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        # 检查目录是否存在
        if not os.path.isdir(value):
            # 尝试创建目录
            try:
                os.makedirs(value, exist_ok=True)
                return True
            except Exception as e:
                return f'目录不存在且无法创建: {str(e)}'

        # 检查目录是否可写
        if not os.access(value, os.W_OK):
            return '目录没有写入权限'
        return True

    def filesaver_verify(self, key, value):
        """
        文件保存验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        # 检查目录是否存在
        dir_path = os.path.dirname(value)
        if dir_path and not os.path.isdir(dir_path):
            # 尝试创建目录
            try:
                os.makedirs(dir_path, exist_ok=True)
            except Exception as e:
                return f'保存目录不存在且无法创建: {str(e)}'

        # 检查文件扩展名
        if key == '--saveFile':
            valid_extensions = ['.txt', '.csv', '.xlsx', '.json']
            ext = os.path.splitext(value)[1].lower()
            if ext not in valid_extensions:
                return f'文件类型必须是 {", ".join(valid_extensions)}'
        return True

    def date_verify(self, key, value):
        """
        日期选择验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        try:
            # 验证日期格式
            date_obj = datetime.datetime.strptime(value, '%Y-%m-%d').date()

            # 检查日期范围
            today = datetime.date.today()
            if key == '--date':
                # 示例：不允许选择过去的日期
                if date_obj < today:
                    return '不能选择过去的日期'
                # 示例：不允许选择超过一年后的日期
                max_date = today + datetime.timedelta(days=365)
                if date_obj > max_date:
                    return '不能选择超过一年后的日期'
            return True
        except ValueError:
            return '日期格式无效，请使用YYYY-MM-DD格式'

    def time_verify(self, key, value):
        """
        时间选择验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        try:
            # 验证时间格式
            time_obj = datetime.datetime.strptime(value, '%H:%M:%S').time()

            # 检查时间范围
            if key == '--time':
                # 示例：限制工作时间 9:00-18:00
                min_time = datetime.time(9, 0, 0)
                max_time = datetime.time(18, 0, 0)
                if time_obj < min_time or time_obj > max_time:
                    return '请选择工作时间范围内的时间(9:00-18:00)'
            return True
        except ValueError:
            return '时间格式无效，请使用HH:MM:SS格式'

    def datetime_verify(self, key, value):
        """
        日期时间选择验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        try:
            # 验证日期时间格式
            datetime_obj = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

            # 检查日期时间范围
            now = datetime.datetime.now()
            if key == '--datetime':
                # 示例：不允许选择过去的日期时间
                if datetime_obj < now:
                    return '不能选择过去的日期时间'
                # 示例：不允许选择超过一年后的日期时间
                max_datetime = now + datetime.timedelta(days=365)
                if datetime_obj > max_datetime:
                    return '不能选择超过一年后的日期时间'
            return True
        except ValueError:
            return '日期时间格式无效，请使用YYYY-MM-DD HH:MM:SS格式'

    def select_verify(self, key, value):
        """
        列表选择框验证
        参数:
            key (str): 属性名
            value: 属性值列表
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        # 检查是否选择了至少一项
        if not value or len(value) == 0:
            return '请至少选择一项'

        # 检查选择数量限制
        if key == '--filteroption':
            if len(value) > 3:
                return '最多只能选择3项'
        return True

    def dropdown_verify(self, key, value):
        """
        下拉选择框验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        # 检查是否选择了有效选项
        valid_options = ["选择一", "选择二", "选项三", "选项四", "选项五"]
        if key == '--dropdownbox' and value not in valid_options:
            return '请选择有效的选项'
        return True

    def color_verify(self, key, value):
        """
        颜色选择器验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        # 验证颜色格式
        if key == '--color':
            # 检查十六进制颜色格式
            hex_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{8}|[A-Fa-f0-9]{3})$'
            if not re.match(hex_pattern, value):
                return '颜色格式无效，请使用十六进制格式(如#FF0000)'
        return True

    def switch_verify(self, key, value):
        """
        开关组件验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        # 检查值是否为布尔类型
        if not isinstance(value, bool):
            return '开关值必须是布尔类型'
        return True

    def radio_verify(self, key, value):
        """
        单选框组验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        # 检查是否选择了有效选项
        valid_options = ["单选1", "单选2", "单选3"]
        if key == '--radio' and value not in valid_options:
            return '请选择有效的选项'
        return True

    def checkbox_verify(self, key, value):
        """
        复选框组验证
        参数:
            key (str): 属性名
            value: 属性值列表
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        # 检查是否选择了至少一项
        if not value or len(value) == 0:
            return '请至少选择一项'

        # 检查选择数量限制
        if key == '--checkbox':
            if len(value) < 1:
                return '至少选择1项'
            if len(value) > 2:
                return '最多只能选择2项'

            # 检查是否选择了有效选项
            valid_options = ["复选1", "复选2", "复选3"]
            for item in value:
                if item not in valid_options:
                    return f'选项 {item} 不是有效选项'
        return True

    def slider_verify(self, key, value):
        """
        滑块组件验证
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            True = 验证通过
            返回任意字符串=不通过
        """
        # self.runlog(f'正在验证参数: {key}={value}', 'info')
        try:
            # 确保值是数字
            num_value = float(value)

            # 检查范围
            if key == '--slider':
                if num_value < 0 or num_value > 100:
                    return '滑块值必须在0-100之间'
            return True
        except (ValueError, TypeError):
            return '请输入有效的数字'

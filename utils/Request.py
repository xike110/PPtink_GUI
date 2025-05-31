import json
import logging
# import oss2
import os
import subprocess

import requests


class Task:
    def __init__(self, uid: str = None, token: str = None, url=None):
        # 配置 OSS 相关信息
        self.__uid = uid
        self.__token = token
        self.__url = url

    def aivideo_ceshi(self, data=None):
        """
        获取信息。
        # todo_m : Request_api [GET] 测试网络正常
        """
        try:
            # 构造请求URL，包括服务器地址和查询参数
            url = f"{self.__url}"
            # 初始化请求的payload（本例中不需要传递任何数据）
            payload = {}
            # GET请求参数
            params = {
            }
            # 设置请求头，包括身份验证信息和用户代理
            headers = {
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'application/json'
            }
            # 发送GET请求并获取响应
            response = requests.request("GET", url, params=params, headers=headers, data=payload, timeout=10)
            if response.status_code == 200:  # 检查状态码是否为200
                logging.info(f"检查网络成功，状态代码为: {response.status_code}")
                return True
            else:
                logging.error(f"检查网络失败，状态代码为: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return False

    def chat_api(self, query, prompt_name="智能对话", wenan_language="中文", wenan_timbre="普通叙述"):
        """
        # todo_m : Request_api [POST] AI生成对话
        :param query:
        :param prompt_name:
        :param wenan_language:
        :param wenan_timbre:
        :return:
        """
        api_base_url = F'http://{self.__url}:{self.__port}'

        api = "/dngadmin/aivideo_api"
        # api = "/chat/chat"
        url = f"{api_base_url}{api}"
        headers = {
            # 'accept': 'application/json',
            'Content-Type': 'application/json',
            'uid': self.__uid,
            'token': self.__token,
        }

        data = {
            "query": query,  # 提问的问题，例子： 发财树摆办公室什么位置? #音频课程在哪领取?
            "ai_type": 0,  # 选项 0-1 ：0 大模型智能回答 1 向量库精准匹配返回（不走大模型）
            "model_type": "all_model",  # 私有训练模型选择 all_model=私有综合模型
            "knowledge_base_name": "all_base",  # 选择向量库种类  all_base=综合向量库 zhanbu_base=占卜向量库 bazi_base=八字向量库 miangxiang_base=面相向量库 kecheng_base=课程向量库
            "top_k": 3,  # 匹配向量数
            "score_threshold": 0.5,  # 向量库匹配相关度阈值，取值范围在0-1之间，SCORE越小，相关度越高，取到1相当于不筛选，建议设置在0.5左右
            "model_name": "default",  # 选择通用GPT模型  default =默认模型 openai-api=chatgpt通用大模型
            "temperature": 0,  # 0-1.0 选择数值 , 数值越低越精准但是回答保守，数值越高回会更加发散性,多样性和创造性
            "max_tokens": 0,  # 用于限制模型生成token的数量，默认None代表模型最大值，max_tokens设置的是生成上限,并不表示一定会生成这么多的token数量
            "prompt_name": prompt_name,  # 客服模型 default=默认角色客服  exclusive=专属个性化客服 broken1=破冰
            "wenan_language": wenan_language,  # 文案语言
            "wenan_timbre": wenan_timbre,  # 文案风格
            "stream": "True",  # True开启流式响应输出 , False 开启等待完整一次性输出

        }
        # logging.info(data)
        response = requests.post(url, headers=headers, json=data, stream=True)

        for line in response.iter_content(None, decode_unicode=True):
            # logging.info(line)

            if "answer" in line:
                json_part = line.split(':', 1)[1]  # 分割字符串，并取冒号后面的部分
                # 去除可能存在的开头和结尾的空格以及引号
                json_part = json_part.strip()
                # 使用 json.loads() 解析 JSON 数据
                data = json.loads(json_part)
                if "answer" in data:
                    print(data["answer"], end="", flush=True)

    def download_file(self, dist_key=None, dpwname=None, base_dir="/file", timeout=10):
        """
        下载远程图片并保存到本地
        # todo_m: Request_api [dow] 下载文件请求
        参数:
        url (str): 图片的URL地址。
        base_dir (str): 保存图片的本地基础目录。
        timeout : 超时10秒
        返回:
        bool: 如果下载成功返回True，否则返回False。
        """
        try:
            url = dist_key["finvideourl_str"]
            filename_part = url.rsplit('/', 1)[-1]
            # 然后，我们可以使用'.'来分割文件名，以获取文件名（不含扩展名）和扩展名
            # 注意：这里假设文件名中只有一个'.'用于分隔文件名和扩展名
            # 如果文件名中可能包含多个'.'，则需要考虑更复杂的逻辑
            filename, file_extension = filename_part.rsplit('.', 1)
            # 输出结果
            file_extension = F".{file_extension}"
            if '?' in file_extension:
                file_extension = file_extension[:file_extension.index('?')]
            if dpwname:
                ename, extension = dpwname.rsplit('.', 1)  # 传参自定义名称
                filename = ename  # 传参自定义名称
            # logging.info("文件名中的哈希值:", filename)
            # logging.info("文件扩展名:", file_extension)
            # 如果URL中没有明确的扩展名，则默认为.jpg
            if not file_extension:
                file_extension = '.txt'
            if dist_key["return_str"] == "有水印":
                random_int = random.randint(1, 100)  # 生成1到100之间的随机整数
                random_ints = random.randint(1, 1000)  # 生成1到100之间的随机整数
                # 构建完整的保存路径
                base_dir_s = F"./cache/a/{random_int}/{random_ints}"  # 构建完整目录路径
                save_path = os.path.join(base_dir_s, filename + file_extension)
                bendi_path = os.path.join("./Download", filename + file_extension)
                # print("下载地址", save_path)
                # 检查文件是否存在
                if os.path.exists(bendi_path):
                    print("文件已存在，跳过下载。")
                    return filename + file_extension
            else:
                # 构建完整的保存路径
                base_dir_s = "./Download"  # 构建完整目录路径
                save_path = os.path.join(base_dir_s, filename + file_extension)
                print("下载地址", save_path)
                # 检查文件是否存在
                if os.path.exists(save_path):
                    print("文件已存在，跳过下载。")
                    return filename + file_extension
            # 检查并创建本地目录
            os.makedirs(base_dir_s, exist_ok=True)

            # 发送GET请求获取图片内容
            response = requests.get(url, stream=True, timeout=timeout)

            # 检查请求是否成功
            if response.status_code == 200:
                # 以二进制写入模式打开文件
                with open(save_path, 'wb') as file:
                    # 将图片内容写入文件
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:  # 过滤掉keep-alive新发送的空包
                            file.write(chunk)

                if dist_key["return_str"] == "有水印":
                    self.get_file_content(F"{filename + file_extension}", save_path)  # 裁剪视频
                return filename + file_extension
            else:
                print(f"检索文件失败!状态代码: {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"下载文件时出错: {e}")
            return False

    def user_get(self, data=None):
        """
        """
        # 构造请求URL，包括服务器地址和查询参数
        try:
            url = f"http://{self.__url}:{self.__port}/dngadmin/userdata_api"
            # 初始化请求的payload（本例中不需要传递任何数据）
            payload = {}
            headers = {
                'uid': self.__uid,
                'token': self.__token,
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
            }
            # 发送GET请求并获取响应
            response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
            # response.raise_for_status()  # 如果响应状态码不是200，则抛出HTTPError异常
            json_data = json.loads(response.text)
            # logging.info(json_data)
            return json_data
        except requests.exceptions.RequestException as e:
            logging.info(e)
            return False

    def user_token(self, username, password):
        try:
            url = F"{self.__url}/dngadmin/login_api/"
            # .field("api_password", "SRftkyKaru")
            # .field("invalid", "99999")
            # .field("username", "xike110")
            # .field("password", "alangmeiwo110")
            payload = {
                "api_password": "SRftkyKaru",
                "invalid": "99999",
                "username": username,
                "password": password
            }

            headers = {
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
            }

            response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
            json_data = json.loads(response.text)
            logging.info(json_data)
            return json_data
        except requests.exceptions.RequestException as e:
            logging.info(e)
            return False

    def sysuser_get(self, data=None, uid_int=None):
        """
        """
        # 构造请求URL，包括服务器地址和查询参数
        try:
            url = f"http://{self.__url}:{self.__port}/dngadmin/adminuser_api"
            # 初始化请求的payload（本例中不需要传递任何数据）
            payload = {
                'limit': 1000,
                'offset': 0,
                'uid_int': uid_int,
            }
            headers = {
                'uid': self.__uid,
                'token': self.__token,
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
            }
            # 发送GET请求并获取响应
            response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            # response.raise_for_status()  # 如果响应状态码不是200，则抛出HTTPError异常
            json_data = json.loads(response.text)
            # logging.info(json_data)
            return json_data
        except requests.exceptions.RequestException as e:
            logging.info(e)
            return False

    def sysuser_put(self, data=None, integral_int=None):
        """
        """
        # 构造请求URL，包括服务器地址和查询参数
        try:
            if not data:
                return False
            if not integral_int:
                return False
            url = f"http://{self.__url}:{self.__port}/dngadmin/adminuser_api"
            # 初始化请求的payload（本例中不需要传递任何数据）
            payload = json.dumps({
                "id": data["id"],
                "integral_int": int(integral_int),
            })
            headers = {
                'uid': self.__uid,
                'token': self.__token,
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
            }
            logging.info(payload)
            # 发送GET请求并获取响应
            response = requests.request("PUT", url, headers=headers, data=payload, timeout=10)
            # response.raise_for_status()  # 如果响应状态码不是200，则抛出HTTPError异常
            json_data = json.loads(response.text)
            logging.info(json_data)
            return json_data
        except requests.exceptions.RequestException as e:
            logging.info(e)
            return False

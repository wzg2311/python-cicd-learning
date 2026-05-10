"""
项目配置模块 - 集中管理项目配置
企业级项目中，配置通常集中管理，便于维护和环境切换
"""

import os


class Config:
    """项目配置类 - 单例模式管理所有配置项"""
    
    # 项目基础信息
    PROJECT_NAME = "Python CI/CD Learning"
    VERSION = "1.0.0"
    AUTHOR = "CI/CD Learner"

    # 环境配置
    ENV = os.getenv('APP_ENV', 'development')  # development / staging / production
    DEBUG = ENV == 'development'

    # 计算精度
    DECIMAL_PLACES = 2

    # 日志级别
    LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'

    # 税费计算相关阈值（可通过环境变量覆盖）
    TAX_THRESHOLD = float(os.getenv('TAX_THRESHOLD', '5000'))  # 个税起征点

    @classmethod
    def get_env_info(cls) -> dict:
        """获取当前环境信息摘要"""
        return {
            'project': cls.PROJECT_NAME,
            'version': cls.VERSION,
            'environment': cls.ENV,
            'debug_mode': cls.DEBUG,
            'log_level': cls.LOG_LEVEL
        }


# 全局配置实例（推荐使用方式）
config = Config()

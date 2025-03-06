import toml
from pathlib import Path
from pydantic import Field, PrivateAttr
from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
   
    all_func_ready: bool
    registration_is_open: bool 
    count_matches_in_tour: int 
    count_tours: int 
    image_width: int 
    image_height: int 
    minimum_players: int 
    start_tour: int 
    finish_tour: int 
    url: str 
    
    MAIN_BOT_TOKEN: str
    TEST_BOT_TOKEN: str 
    ADMIN_ID: int 
    ADMIN_ID2: int 
    API_TOKEN: str 
    

    model_config = SettingsConfigDict(
        env_file="settings/.env",
        env_file_encoding="utf-8",
        extra="allow"
    )

    _toml_path: Path = PrivateAttr(default=Path("settings/settings.toml"))  # Приватный атрибут для пути к файлу
    _toml_data: dict = PrivateAttr(default={})  # Храним только TOML-данные

    @classmethod
    def load(cls):
        """Загружает конфигурацию из settings.toml и .env, но сохраняет только toml-данные"""
        toml_data = {}
        toml_data = toml.load("settings/settings.toml")

        instance = cls(**toml_data)
        instance._toml_data = toml_data  # Сохраняем только TOML-данные
        return instance
    
    
    def save(self):
        """Сохраняет только настройки из settings.toml, без переменных окружения"""
        self._toml_path.parent.mkdir(parents=True, exist_ok=True)

        # Фильтруем только те параметры, которые были загружены из TOML
        filtered_data = {key: getattr(self, key) for key in self._toml_data.keys()}

        with self._toml_path.open("w", encoding="utf-8") as f:
            toml.dump(filtered_data, f)
            
    def show(self):
        res = ""
        for key, value in self._toml_data.items():
            res += f"{key} = {value}\n"
        return res

config = Settings.load()

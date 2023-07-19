import configparser
import os


# here create class of config manager
class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._config = configparser.ConfigParser()
            config_file = os.path.join("conf", "config.ini")
            cls._instance._config.read(config_file)
            config_prompt_file = os.path.join("conf", "prompts.ini")
            cls._instance._config.read(config_prompt_file)
        return cls._instance
    
    def get_api_key(self):
        return self._config.get("OpenAI", "API_key")
    
    def get_system_prompts(self):

        maths = self._config.get("SystemPrompt", "Maths_prompt")
        english = self._config.get("SystemPrompt", "English_prompt")
        science = self._config.get("SystemPrompt", "Science_prompt")
        social_science = self._config.get("SystemPrompt", "Social_science_prompt")
        return maths, english, science, social_science
    
    def get_assistent_prompts(self):
        maths = self._config.get("AssistentPrompt", "Maths_assistent_prompt")
        english = self._config.get("AssistentPrompt", "English_assistent_prompt")
        science = self._config.get("AssistentPrompt", "Science_assistent_prompt")
        social_science = self._config.get("AssistentPrompt", "Social_science_assistent_prompt")
        return maths, english, science, social_science

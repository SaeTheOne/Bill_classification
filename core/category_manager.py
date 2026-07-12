import os
import json

CONFIG_FILE = "categories_config.json"

class CategoryManager:
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.categories = {}
        self.load()

    def load(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.categories = json.load(f)
                return True
            except Exception as e:
                print(f"加载配置失败: {e}")
                self.categories = {}
                return False
        self.categories = {}
        return False

    def save(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.categories, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

    def get_main_categories(self):
        return list(self.categories.keys()) if self.categories else []

    def add_main_category(self, main_cat):
        if not main_cat or main_cat in self.categories:
            return False
        self.categories[main_cat] = {}
        return True

    def delete_main_category(self, main_cat):
        if main_cat in self.categories:
            del self.categories[main_cat]
            return True
        return False

    def rename_main_category(self, old_name, new_name):
        if old_name in self.categories and new_name not in self.categories:
            self.categories[new_name] = self.categories.pop(old_name)
            return True
        return False

    def get_sub_categories(self, main_cat):
        if main_cat in self.categories and isinstance(self.categories[main_cat], dict):
            return list(self.categories[main_cat].keys())
        return []

    def add_sub_category(self, main_cat, sub_cat):
        if not main_cat or main_cat not in self.categories:
            return False
        if not sub_cat or sub_cat in self.categories[main_cat]:
            return False
        self.categories[main_cat][sub_cat] = {}
        return True

    def delete_sub_category(self, main_cat, sub_cat):
        if main_cat in self.categories and sub_cat in self.categories[main_cat]:
            del self.categories[main_cat][sub_cat]
            return True
        return False

    def rename_sub_category(self, main_cat, old_name, new_name):
        if main_cat in self.categories and old_name in self.categories[main_cat]:
            if new_name not in self.categories[main_cat]:
                self.categories[main_cat][new_name] = self.categories[main_cat].pop(old_name)
                return True
        return False

    def get_third_categories(self, main_cat, sub_cat):
        if main_cat in self.categories:
            if sub_cat in self.categories[main_cat]:
                if isinstance(self.categories[main_cat][sub_cat], dict):
                    return list(self.categories[main_cat][sub_cat].keys())
        return []

    def add_third_category(self, main_cat, sub_cat, third_cat):
        if main_cat not in self.categories:
            return False
        if sub_cat not in self.categories[main_cat]:
            return False
        if not third_cat or third_cat in self.categories[main_cat][sub_cat]:
            return False
        self.categories[main_cat][sub_cat][third_cat] = ""
        return True

    def delete_third_category(self, main_cat, sub_cat, third_cat):
        if main_cat in self.categories:
            if sub_cat in self.categories[main_cat]:
                if third_cat in self.categories[main_cat][sub_cat]:
                    del self.categories[main_cat][sub_cat][third_cat]
                    return True
        return False

    def rename_third_category(self, main_cat, sub_cat, old_name, new_name):
        if main_cat in self.categories:
            if sub_cat in self.categories[main_cat]:
                if old_name in self.categories[main_cat][sub_cat]:
                    if new_name not in self.categories[main_cat][sub_cat]:
                        self.categories[main_cat][sub_cat][new_name] = self.categories[main_cat][sub_cat].pop(old_name)
                        return True
        return False

    def get_rules(self, main_cat, sub_cat, third_cat):
        if main_cat in self.categories:
            if sub_cat in self.categories[main_cat]:
                if third_cat in self.categories[main_cat][sub_cat]:
                    rules = self.categories[main_cat][sub_cat][third_cat]
                    return rules if rules is not None else ""
        return ""

    def update_rules(self, main_cat, sub_cat, third_cat, rules):
        if main_cat in self.categories:
            if sub_cat in self.categories[main_cat]:
                if third_cat in self.categories[main_cat][sub_cat]:
                    self.categories[main_cat][sub_cat][third_cat] = rules
                    return True
        return False

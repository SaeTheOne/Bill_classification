import os
import json

USER_KEYWORDS_FILE = "user_keywords.json"

class UserKeywordsManager:
    def __init__(self, keywords_file=USER_KEYWORDS_FILE):
        self.keywords_file = keywords_file
        self.keywords = {}
        self.load()

    def load(self):
        if os.path.exists(self.keywords_file):
            try:
                with open(self.keywords_file, 'r', encoding='utf-8') as f:
                    self.keywords = json.load(f)
                return True
            except Exception as e:
                print(f"加载用户关键词失败: {e}")
                self.keywords = {}
                return False
        self.keywords = {}
        return True

    def save(self):
        try:
            with open(self.keywords_file, 'w', encoding='utf-8') as f:
                json.dump(self.keywords, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存用户关键词失败: {e}")
            return False

    def get_path(self, main_cat, sub_cat=None, third_cat=None, fourth_cat=None):
        parts = [main_cat]
        if sub_cat:
            parts.append(sub_cat)
        if third_cat:
            parts.append(third_cat)
        if fourth_cat:
            parts.append(fourth_cat)
        return "/".join(parts)

    def add_keywords(self, main_cat, sub_cat, third_cat, fourth_cat, keywords):
        path = self.get_path(main_cat, sub_cat, third_cat, fourth_cat)
        if path not in self.keywords:
            self.keywords[path] = []
        added = []
        for kw in keywords:
            if kw not in self.keywords[path]:
                self.keywords[path].append(kw)
                added.append(kw)
        return added

    def remove_keyword(self, main_cat, sub_cat, third_cat, fourth_cat, keyword):
        path = self.get_path(main_cat, sub_cat, third_cat, fourth_cat)
        if path in self.keywords and keyword in self.keywords[path]:
            self.keywords[path].remove(keyword)
            if not self.keywords[path]:
                del self.keywords[path]
            return True
        return False

    def get_keywords(self, main_cat, sub_cat, third_cat, fourth_cat):
        path = self.get_path(main_cat, sub_cat, third_cat, fourth_cat)
        return self.keywords.get(path, [])

    def get_all_keywords(self):
        return self.keywords

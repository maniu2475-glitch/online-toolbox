# -*- coding: utf-8 -*-
import io
s = io.open("README.md", encoding="utf-8").read()
s = s.replace("115 个工具", "120 个工具")
io.open("README.md", "w", encoding="utf-8").write(s)
print("ok:", "120 个工具" in s)

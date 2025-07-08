#!/usr/bin/env python3
"""
获取所有章节的实际标题并生成索引
"""

import os
import re
from pathlib import Path

def extract_title_from_md(filepath):
    """从markdown文件中提取标题"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 查找YAML frontmatter中的title
    title_match = re.search(r'^---\s*\n.*?title:\s*"([^"]+)"', content, re.MULTILINE | re.DOTALL)
    if title_match:
        return title_match.group(1)
    
    # 如果没有frontmatter，查找第一个#标题
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1)
        
    return None

def get_all_chapters(base_dir):
    """获取所有章节信息"""
    chapters = []
    
    # 扫描所有part目录
    for part_dir in sorted(Path(base_dir).glob("part-*")):
        if part_dir.is_dir():
            part_name = part_dir.name
            
            # 扫描part中的所有chapter文件
            for chapter_file in sorted(part_dir.glob("chapter-*.md")):
                # 提取章节号
                chapter_match = re.match(r'chapter-(\d+)-.*\.md', chapter_file.name)
                if chapter_match:
                    chapter_num = int(chapter_match.group(1))
                    title = extract_title_from_md(chapter_file)
                    
                    if title:
                        chapters.append({
                            'num': chapter_num,
                            'part': part_name,
                            'file': chapter_file.name,
                            'path': str(chapter_file.relative_to(base_dir)),
                            'title': title
                        })
    
    return sorted(chapters, key=lambda x: x['num'])

def main():
    """主函数"""
    # 获取文档根目录
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent / "docs" / "psi-constants"
    
    print("# PSI Constants Theory - Chapter Index")
    print("# 物理常数理论 - 章节索引\n")
    
    # 获取所有章节
    chapters = get_all_chapters(docs_dir)
    
    current_part = None
    for chapter in chapters:
        # 如果进入新的part，打印part标题
        if chapter['part'] != current_part:
            current_part = chapter['part']
            print(f"\n## {current_part.replace('-', ' ').title()}")
            print()
        
        # 提取物理概念部分（冒号后的内容）
        title_parts = chapter['title'].split(':', 1)
        if len(title_parts) > 1:
            chapter_label = title_parts[0].strip()
            physics_concept = title_parts[1].strip()
            
            # 分离主标题和副标题
            if ' — ' in physics_concept:
                main_concept, subtitle = physics_concept.split(' — ', 1)
            else:
                main_concept = physics_concept
                subtitle = ""
            
            print(f"- **{chapter_label}**: {main_concept}")
            if subtitle:
                print(f"  - {subtitle}")
        else:
            print(f"- **Chapter {chapter['num']:03d}**: {chapter['title']}")
        
        # 打印文件路径作为注释
        print(f"  <!-- {chapter['path']} -->")
    
    print("\n## Summary Statistics")
    print(f"- Total chapters: {len(chapters)}")
    
    # 统计每个part的章节数
    part_counts = {}
    for chapter in chapters:
        part = chapter['part']
        part_counts[part] = part_counts.get(part, 0) + 1
    
    print("\n### Chapters per Part:")
    for part, count in sorted(part_counts.items()):
        print(f"- {part}: {count} chapters")

if __name__ == "__main__":
    main()
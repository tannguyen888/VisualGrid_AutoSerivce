"""
TODO:
Assembly mapper.

What this file does:
- Maps repair/parts hierarchy into assembly structures.

Input:
- Parsed part and assembly data.

Output:
- Normalized assembly record.

Dependencies:
- models.part_schema

Future implementation steps:
- Link components to assemblies
- Preserve reference topology
"""


class AssemblyMapper:
    def map(self, assembly_data: dict) -> dict:
        # Bước 1: tạo biến mapped_assembly.
        # mapped_assembly = {}
        # Bước 2: link assembly với component.
        # Bước 3: trả payload chuẩn để loader lưu.
        return {}

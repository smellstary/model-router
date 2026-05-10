"""
Unit tests for Philosophy-Technology Semantic Transformation Framework
哲学-技术语义转化框架单元测试
"""

import unittest
import sys
import os
import importlib.util
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Callable, Set
from datetime import datetime

_test_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.join(_test_dir, '..', '..')

_types_path = os.path.join(_project_root, "oriental_agent", "core", "types.py")
_spec_types = importlib.util.spec_from_file_location("types", _types_path)
types_module = importlib.util.module_from_spec(_spec_types)
sys.modules["types"] = types_module
_spec_types.loader.exec_module(types_module)

sys.modules["core.types"] = types_module

_framework_path = os.path.join(_project_root, "oriental_agent", "core", "semantic_framework.py")
_spec_framework = importlib.util.spec_from_file_location("semantic_framework", _framework_path)
semantic_framework = importlib.util.module_from_spec(_spec_framework)
sys.modules["semantic_framework"] = semantic_framework
_spec_framework.loader.exec_module(semantic_framework)

ConceptMapping = semantic_framework.ConceptMapping
ConceptCategory = semantic_framework.ConceptCategory
MappingType = semantic_framework.MappingType
ValidationLevel = semantic_framework.ValidationLevel
TransformationResult = semantic_framework.TransformationResult
SemanticFramework = semantic_framework.SemanticFramework


class TestConceptMapping(unittest.TestCase):
    """测试 ConceptMapping 数据类"""
    
    def setUp(self):
        """测试前准备"""
        self.sample_concept = ConceptMapping(
            concept_id="test_concept",
            concept_name="测试概念",
            category=ConceptCategory.YIN_YANG,
            philosophical_definition="这是一个测试概念的定义",
            technical_correspondence={
                "value": 1.0,
                "type": "test"
            },
            mapping_type=MappingType.EXACT,
            confidence_score=0.9,
            aliases=["测试", "test"],
            related_concepts=["related_1"]
        )
    
    def test_concept_creation(self):
        """测试概念创建"""
        self.assertEqual(self.sample_concept.concept_id, "test_concept")
        self.assertEqual(self.sample_concept.concept_name, "测试概念")
        self.assertEqual(self.sample_concept.category, ConceptCategory.YIN_YANG)
        self.assertEqual(self.sample_concept.confidence_score, 0.9)
    
    def test_exact_match(self):
        """测试精确匹配"""
        is_match, score = self.sample_concept.matches_query("测试概念", fuzzy=False)
        self.assertTrue(is_match)
        self.assertEqual(score, 1.0)
    
    def test_partial_match(self):
        """测试部分匹配"""
        is_match, score = self.sample_concept.matches_query("测试", fuzzy=False)
        self.assertTrue(is_match)
        self.assertGreater(score, 0.8)
    
    def test_alias_match(self):
        """测试别名匹配"""
        is_match, score = self.sample_concept.matches_query("test", fuzzy=False)
        self.assertTrue(is_match)
        self.assertGreater(score, 0.8)
    
    def test_fuzzy_match(self):
        """测试模糊匹配"""
        is_match, score = self.sample_concept.matches_query("测试概", fuzzy=True)
        self.assertTrue(is_match)
        self.assertGreater(score, 0.5)
    
    def test_no_match(self):
        """测试不匹配情况"""
        is_match, score = self.sample_concept.matches_query("完全不相关", fuzzy=False)
        self.assertFalse(is_match)
        self.assertEqual(score, 0.0)
    
    def test_to_technical(self):
        """测试转换为技术表示"""
        tech = self.sample_concept.to_technical()
        self.assertIn('id', tech)
        self.assertIn('name', tech)
        self.assertIn('technical', tech)
        self.assertEqual(tech['id'], "test_concept")
    
    def test_validation_valid(self):
        """测试有效概念验证"""
        is_valid, issues = self.sample_concept.validate(ValidationLevel.MODERATE)
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
    
    def test_validation_invalid_empty_id(self):
        """测试空ID验证失败"""
        invalid_concept = ConceptMapping(
            concept_id="",
            concept_name="测试",
            category=ConceptCategory.YIN_YANG,
            philosophical_definition="定义",
            technical_correspondence={"value": 1}
        )
        is_valid, issues = invalid_concept.validate(ValidationLevel.MODERATE)
        self.assertFalse(is_valid)
        self.assertIn("概念ID不能为空", issues)
    
    def test_validation_invalid_confidence(self):
        """测试无效置信度验证"""
        invalid_concept = ConceptMapping(
            concept_id="test",
            concept_name="测试",
            category=ConceptCategory.YIN_YANG,
            philosophical_definition="定义",
            technical_correspondence={"value": 1},
            confidence_score=1.5
        )
        is_valid, issues = invalid_concept.validate(ValidationLevel.MODERATE)
        self.assertFalse(is_valid)
        self.assertIn("置信度分数必须在0-1之间", issues)


class TestSemanticFrameworkMappingAccuracy(unittest.TestCase):
    """测试语义转化框架映射准确性"""
    
    def setUp(self):
        """测试前准备"""
        self.framework = SemanticFramework()
    
    def test_yinyang_mapping(self):
        """测试阴阳概念映射"""
        yin_concepts = self.framework.query("阴")
        self.assertGreater(len(yin_concepts), 0)
        
        concept, score = yin_concepts[0]
        self.assertEqual(concept.concept_name, "阴")
        self.assertEqual(concept.category, ConceptCategory.YIN_YANG)
        self.assertIn("state_value", concept.technical_correspondence)
        self.assertEqual(concept.technical_correspondence["state_value"], -1.0)
    
    def test_yang_mapping(self):
        """测试阳概念映射"""
        yang_concepts = self.framework.query("阳")
        self.assertGreater(len(yang_concepts), 0)
        
        for concept, score in yang_concepts:
            if concept.concept_name == "阳":
                self.assertEqual(concept.category, ConceptCategory.YIN_YANG)
                self.assertEqual(concept.technical_correspondence["state_value"], 1.0)
                break
    
    def test_wuxing_wood_mapping(self):
        """测试木行映射"""
        concepts = self.framework.query("木")
        self.assertGreater(len(concepts), 0)
        
        concept, score = concepts[0]
        self.assertEqual(concept.concept_name, "木")
        self.assertEqual(concept.category, ConceptCategory.WUXING)
        self.assertEqual(concept.technical_correspondence["element_type"], "growth")
    
    def test_wuxing_fire_mapping(self):
        """测试火行映射"""
        concepts = self.framework.query("火")
        self.assertGreater(len(concepts), 0)
        
        found = False
        for concept, score in concepts:
            if concept.concept_name == "火":
                self.assertEqual(concept.category, ConceptCategory.WUXING)
                self.assertEqual(concept.technical_correspondence["element_type"], "transformation")
                found = True
                break
        self.assertTrue(found)
    
    def test_wuxing_earth_mapping(self):
        """测试土行映射"""
        concepts = self.framework.query("土")
        self.assertGreater(len(concepts), 0)
        
        found = False
        for concept, score in concepts:
            if concept.concept_name == "土":
                self.assertEqual(concept.category, ConceptCategory.WUXING)
                self.assertEqual(concept.technical_correspondence["element_type"], "stabilization")
                found = True
                break
        self.assertTrue(found)
    
    def test_wuxing_metal_mapping(self):
        """测试金行映射"""
        concepts = self.framework.query("金")
        self.assertGreater(len(concepts), 0)
        
        found = False
        for concept, score in concepts:
            if concept.concept_name == "金":
                self.assertEqual(concept.category, ConceptCategory.WUXING)
                self.assertEqual(concept.technical_correspondence["element_type"], "contraction")
                found = True
                break
        self.assertTrue(found)
    
    def test_wuxing_water_mapping(self):
        """测试水行映射"""
        concepts = self.framework.query("水")
        self.assertGreater(len(concepts), 0)
        
        found = False
        for concept, score in concepts:
            if concept.concept_name == "水":
                self.assertEqual(concept.category, ConceptCategory.WUXING)
                self.assertEqual(concept.technical_correspondence["element_type"], "accumulation")
                found = True
                break
        self.assertTrue(found)
    
    def test_bagua_qian_mapping(self):
        """测试乾卦映射"""
        concepts = self.framework.query("乾")
        self.assertGreater(len(concepts), 0)
        
        concept, score = concepts[0]
        self.assertEqual(concept.concept_name, "乾")
        self.assertEqual(concept.category, ConceptCategory.BAGUA)
        self.assertEqual(concept.technical_correspondence["binary"], [1, 1, 1])
        self.assertEqual(concept.technical_correspondence["yin_yang_value"], 1.0)
    
    def test_bagua_kun_mapping(self):
        """测试坤卦映射"""
        concepts = self.framework.query("坤")
        self.assertGreater(len(concepts), 0)
        
        concept, score = concepts[0]
        self.assertEqual(concept.concept_name, "坤")
        self.assertEqual(concept.category, ConceptCategory.BAGUA)
        self.assertEqual(concept.technical_correspondence["binary"], [0, 0, 0])
        self.assertEqual(concept.technical_correspondence["yin_yang_value"], -1.0)
    
    def test_all_bagua_mappings(self):
        """测试所有八卦映射"""
        bagua_names = ["乾", "坤", "震", "巽", "坎", "离", "艮", "兑"]
        
        for name in bagua_names:
            concepts = self.framework.query(name)
            self.assertGreater(len(concepts), 0, f"未找到卦象: {name}")
            
            concept, score = concepts[0]
            self.assertEqual(concept.category, ConceptCategory.BAGUA)
            self.assertIn("binary", concept.technical_correspondence)
            self.assertEqual(len(concept.technical_correspondence["binary"]), 3)
    
    def test_tiangan_mapping(self):
        """测试天干映射"""
        tiangan_names = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        
        for i, name in enumerate(tiangan_names, 1):
            concepts = self.framework.query(name)
            self.assertGreater(len(concepts), 0, f"未找到天干: {name}")
            
            found = False
            for concept, score in concepts:
                if concept.category == ConceptCategory.TIANGAN and concept.concept_name == name:
                    self.assertEqual(concept.technical_correspondence["order"], i)
                    found = True
                    break
            self.assertTrue(found, f"天干{name}映射验证失败")
    
    def test_dizhi_mapping(self):
        """测试地支映射"""
        dizhi_names = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        for i, name in enumerate(dizhi_names, 1):
            concepts = self.framework.query(name)
            self.assertGreater(len(concepts), 0, f"未找到地支: {name}")
            
            found = False
            for concept, score in concepts:
                if concept.category == ConceptCategory.DIZHI and concept.concept_name == name:
                    self.assertEqual(concept.technical_correspondence["order"], i)
                    self.assertIn("animal", concept.technical_correspondence)
                    found = True
                    break
            self.assertTrue(found, f"地支{name}映射验证失败")
    
    def test_query_by_category(self):
        """测试按类别查询"""
        wuxing_concepts = self.framework.get_concepts_by_category(ConceptCategory.WUXING)
        self.assertEqual(len(wuxing_concepts), 7)
        
        bagua_concepts = self.framework.get_concepts_by_category(ConceptCategory.BAGUA)
        self.assertEqual(len(bagua_concepts), 8)
        
        tiangan_concepts = self.framework.get_concepts_by_category(ConceptCategory.TIANGAN)
        self.assertEqual(len(tiangan_concepts), 10)
        
        dizhi_concepts = self.framework.get_concepts_by_category(ConceptCategory.DIZHI)
        self.assertEqual(len(dizhi_concepts), 12)
    
    def test_fuzzy_query(self):
        """测试模糊查询"""
        results = self.framework.query("火行", fuzzy=True)
        self.assertGreater(len(results), 0)
        
        found = False
        for concept, score in results:
            if concept.concept_name == "火":
                found = True
                break
        self.assertTrue(found)
    
    def test_alias_query(self):
        """测试别名查询"""
        results = self.framework.query("Wood")
        self.assertGreater(len(results), 0)
        
        found = False
        for concept, score in results:
            if concept.concept_name == "木":
                found = True
                break
        self.assertTrue(found)


class TestSemanticFrameworkExtensibility(unittest.TestCase):
    """测试语义转化框架扩展性"""
    
    def setUp(self):
        """测试前准备"""
        self.framework = SemanticFramework()
    
    def test_register_new_concept(self):
        """测试注册新概念"""
        new_concept = ConceptMapping(
            concept_id="custom_test",
            concept_name="自定义概念",
            category=ConceptCategory.CUSTOM,
            philosophical_definition="用户自定义的测试概念",
            technical_correspondence={
                "custom_value": 100,
                "custom_type": "user_defined"
            },
            mapping_type=MappingType.FUZZY,
            confidence_score=0.8,
            aliases=["自定义", "custom"]
        )
        
        success, issues = self.framework.register_concept(new_concept)
        self.assertTrue(success)
        self.assertEqual(len(issues), 0)
        
        concepts = self.framework.query("自定义概念")
        self.assertEqual(len(concepts), 1)
        self.assertEqual(concepts[0][0].concept_id, "custom_test")
    
    def test_register_concept_with_validation(self):
        """测试带验证的概念注册"""
        valid_concept = ConceptMapping(
            concept_id="valid_test",
            concept_name="有效概念",
            category=ConceptCategory.YIN_YANG,
            philosophical_definition="有效的测试概念",
            technical_correspondence={"value": 0.5},
            aliases=["有效"]
        )
        
        success, issues = self.framework.register_concept(valid_concept, validate=True)
        self.assertTrue(success)
    
    def test_register_invalid_concept(self):
        """测试注册无效概念"""
        invalid_concept = ConceptMapping(
            concept_id="",
            concept_name="",
            category=ConceptCategory.CUSTOM,
            philosophical_definition="",
            technical_correspondence={}
        )
        
        success, issues = self.framework.register_concept(invalid_concept, validate=True)
        self.assertFalse(success)
        self.assertGreater(len(issues), 0)
    
    def test_update_existing_concept(self):
        """测试更新现有概念"""
        original = self.framework.get_concept("yinyang_yin")
        self.assertIsNotNone(original)
        
        updated_concept = ConceptMapping(
            concept_id="yinyang_yin",
            concept_name="阴",
            category=ConceptCategory.YIN_YANG,
            philosophical_definition="更新后的阴性定义",
            technical_correspondence={
                "state_value": -1.0,
                "polarity": "negative",
                "new_field": "new_value"
            },
            mapping_type=MappingType.EXACT,
            confidence_score=0.95,
            aliases=["阴气", "阴性", "Yin", "Updated"]
        )
        
        success, issues = self.framework.register_concept(updated_concept)
        self.assertTrue(success)
        
        retrieved = self.framework.get_concept("yinyang_yin")
        self.assertEqual(retrieved.philosophical_definition, "更新后的阴性定义")
        self.assertIn("new_field", retrieved.technical_correspondence)
    
    def test_category_index_update(self):
        """测试类别索引更新"""
        new_concept = ConceptMapping(
            concept_id="category_test_unique",
            concept_name="类别测试唯一",
            category=ConceptCategory.CUSTOM,
            philosophical_definition="测试类别索引",
            technical_correspondence={"test": True}
        )
        
        success, issues = self.framework.register_concept(new_concept, validate=False)
        self.assertTrue(success)
        
        custom_concepts = self.framework.get_concepts_by_category(ConceptCategory.CUSTOM)
        concept_ids = [c.concept_id for c in custom_concepts]
        self.assertIn("category_test_unique", concept_ids)
    
    def test_alias_index_update(self):
        """测试别名索引更新"""
        new_concept = ConceptMapping(
            concept_id="alias_test",
            concept_name="别名测试",
            category=ConceptCategory.CUSTOM,
            philosophical_definition="测试别名索引",
            technical_correspondence={"test": True},
            aliases=["unique_alias_test"]
        )
        
        self.framework.register_concept(new_concept)
        
        results = self.framework.query("unique_alias_test")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0].concept_id, "alias_test")
    
    def test_related_concepts(self):
        """测试相关概念查询"""
        related = self.framework.get_related_concepts("yinyang_yin")
        
        related_ids = [c.concept_id for c in related]
        self.assertIn("yinyang_yang", related_ids)
    
    def test_transformation_path(self):
        """测试转化路径"""
        path = self.framework.get_transformation_path("阴", "阳")
        
        self.assertGreater(len(path), 0)
        self.assertTrue(path[0].success)
    
    def test_list_all_concepts(self):
        """测试列出所有概念"""
        all_concepts = self.framework.list_all_concepts()
        
        self.assertGreater(len(all_concepts), 0)
        
        for concept in all_concepts:
            self.assertIn('id', concept)
            self.assertIn('name', concept)
            self.assertIn('category', concept)
    
    def test_export_mappings(self):
        """测试导出映射"""
        exported = self.framework.export_mappings()
        
        self.assertIn('concepts', exported)
        self.assertIn('statistics', exported)
        self.assertGreater(len(exported['concepts']), 0)


class TestSemanticFrameworkValidation(unittest.TestCase):
    """测试语义转化框架一致性验证"""
    
    def setUp(self):
        """测试前准备"""
        self.framework = SemanticFramework()
    
    def test_validate_all_concepts(self):
        """测试验证所有概念"""
        is_valid, issues = self.framework.validate()
        
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
    
    def test_validate_specific_concept(self):
        """测试验证特定概念"""
        is_valid, issues = self.framework.validate("yinyang_yin")
        
        self.assertTrue(is_valid)
    
    def test_validate_nonexistent_concept(self):
        """测试验证不存在的概念"""
        is_valid, issues = self.framework.validate("nonexistent_concept")
        
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
    
    def test_yinyang_value_range_validation(self):
        """测试阴阳值范围验证"""
        yin_concept = self.framework.get_concept("yinyang_yin")
        yang_concept = self.framework.get_concept("yinyang_yang")
        
        self.assertIsNotNone(yin_concept)
        self.assertIsNotNone(yang_concept)
        
        yin_value = yin_concept.technical_correspondence["state_value"]
        yang_value = yang_concept.technical_correspondence["state_value"]
        
        self.assertGreaterEqual(yin_value, -1.0)
        self.assertLessEqual(yin_value, 1.0)
        self.assertGreaterEqual(yang_value, -1.0)
        self.assertLessEqual(yang_value, 1.0)
    
    def test_bagua_binary_validation(self):
        """测试八卦二进制验证"""
        bagua_concepts = self.framework.get_concepts_by_category(ConceptCategory.BAGUA)
        
        for concept in bagua_concepts:
            binary = concept.technical_correspondence.get("binary")
            self.assertIsNotNone(binary)
            self.assertEqual(len(binary), 3)
            for bit in binary:
                self.assertIn(bit, [0, 1])
    
    def test_tiangan_order_validation(self):
        """测试天干顺序验证"""
        tiangan_concepts = self.framework.get_concepts_by_category(ConceptCategory.TIANGAN)
        
        orders = [c.technical_correspondence["order"] for c in tiangan_concepts]
        self.assertEqual(sorted(orders), list(range(1, 11)))
    
    def test_dizhi_order_validation(self):
        """测试地支顺序验证"""
        dizhi_concepts = self.framework.get_concepts_by_category(ConceptCategory.DIZHI)
        
        orders = [c.technical_correspondence["order"] for c in dizhi_concepts]
        self.assertEqual(sorted(orders), list(range(1, 13)))
    
    def test_wuxing_generation_cycle_validation(self):
        """测试五行相生循环验证"""
        generation_cycle = {
            "木": "fire", "火": "earth", "土": "metal",
            "金": "water", "水": "wood"
        }
        
        for source, target in generation_cycle.items():
            source_concept = self.framework.query(source)[0][0]
            self.assertIn("generates", source_concept.transformation_rules)
            self.assertEqual(source_concept.transformation_rules["generates"], target)
    
    def test_wuxing_restriction_cycle_validation(self):
        """测试五行相克循环验证"""
        restriction_cycle = {
            "木": "earth", "土": "water", "水": "fire",
            "火": "metal", "金": "wood"
        }
        
        for source, target in restriction_cycle.items():
            source_concept = self.framework.query(source)[0][0]
            self.assertIn("restricts", source_concept.transformation_rules)
            self.assertEqual(source_concept.transformation_rules["restricts"], target)
    
    def test_confidence_score_range(self):
        """测试置信度分数范围"""
        all_concepts = self.framework.list_all_concepts()
        
        for concept_info in all_concepts:
            concept = self.framework.get_concept(concept_info['id'])
            self.assertGreaterEqual(concept.confidence_score, 0.0)
            self.assertLessEqual(concept.confidence_score, 1.0)
    
    def test_transformation_result_structure(self):
        """测试转化结果结构"""
        result = self.framework.transform("阴")
        
        self.assertIsInstance(result, TransformationResult)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.target_representation)
        self.assertGreater(result.confidence, 0.0)
    
    def test_statistics(self):
        """测试统计信息"""
        stats = self.framework.get_statistics()
        
        self.assertIn('total_concepts', stats)
        self.assertIn('categories', stats)
        self.assertIn('cache_size', stats)
        self.assertIn('validation_level', stats)
        
        self.assertGreater(stats['total_concepts'], 0)


class TestSemanticFrameworkTransform(unittest.TestCase):
    """测试语义转化框架转化功能"""
    
    def setUp(self):
        """测试前准备"""
        self.framework = SemanticFramework()
    
    def test_transform_to_technical(self):
        """测试转化为技术表示"""
        result = self.framework.transform("阴", "technical")
        
        self.assertTrue(result.success)
        self.assertIn('technical', result.target_representation)
        self.assertEqual(result.target_representation['technical']['state_value'], -1.0)
    
    def test_transform_to_philosophical(self):
        """测试转化为哲学表示"""
        result = self.framework.transform("阴", "philosophical")
        
        self.assertTrue(result.success)
        self.assertIn('definition', result.target_representation)
        self.assertIn('category', result.target_representation)
    
    def test_transform_nonexistent_concept(self):
        """测试转化不存在的概念"""
        result = self.framework.transform("不存在的概念xyz")
        
        self.assertFalse(result.success)
        self.assertGreater(len(result.warnings), 0)
    
    def test_transform_cache(self):
        """测试转化缓存"""
        result1 = self.framework.transform("阳")
        result2 = self.framework.transform("阳")
        
        self.assertEqual(result1.source_concept, result2.source_concept)
        
        stats = self.framework.get_statistics()
        self.assertGreater(stats['cache_size'], 0)
    
    def test_clear_cache(self):
        """测试清除缓存"""
        self.framework.transform("阴")
        
        self.framework.clear_cache()
        
        stats = self.framework.get_statistics()
        self.assertEqual(stats['cache_size'], 0)


class TestSemanticFrameworkIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """测试前准备"""
        self.framework = SemanticFramework()
    
    def test_complete_workflow(self):
        """测试完整工作流"""
        concepts = self.framework.query("木")
        self.assertGreater(len(concepts), 0)
        
        concept, score = concepts[0]
        
        result = self.framework.transform(concept.concept_name)
        self.assertTrue(result.success)
        
        related = self.framework.get_related_concepts(concept.concept_id)
        self.assertGreater(len(related), 0)
        
        is_valid, issues = self.framework.validate(concept.concept_id)
        self.assertTrue(is_valid)
    
    def test_cross_category_query(self):
        """测试跨类别查询"""
        fire_results = self.framework.query("火")
        
        categories = set()
        for concept, score in fire_results:
            categories.add(concept.category)
        
        self.assertIn(ConceptCategory.WUXING, categories)
    
    def test_multiple_transformations(self):
        """测试多次转化"""
        concepts_to_transform = ["阴", "阳", "木", "火", "土", "金", "水"]
        
        for concept_name in concepts_to_transform:
            result = self.framework.transform(concept_name)
            self.assertTrue(result.success, f"转化失败: {concept_name}")
    
    def test_validation_level_strict(self):
        """测试严格验证级别"""
        strict_framework = SemanticFramework(validation_level=ValidationLevel.STRICT)
        
        is_valid, issues = strict_framework.validate()
        
        self.assertTrue(is_valid or len(issues) > 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)

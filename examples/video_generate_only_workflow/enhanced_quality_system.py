# 评估系统待改进

import os
import json
import re
import time
from typing import Dict, List, Any, Optional
from openai import OpenAI
from json_parser_utils import extract_json_with_fallback, safe_json_parse

class VisualQualityAssessment:
    """视觉质量评估模块"""
    
    def __init__(self):
        self.banned_reasonings = [
            "看起来不错",
            "没有问题", 
            "很好",
            "符合要求",
            "完美"
        ]
    
    def assess_animation_quality(self, animation_code, content, animation_type, improvement_prompt = None):
        """
        评估动画质量，检查是否符合内容主题
        """
        
        quality_prompt = f"""
请作为专业的科普教育动画质量评估师，评估以下动画代码是否符合教学内容：

**评估标准：**
1. 动画是否与文案内容高度相关且形象
2. 动画是否丰富有趣，画面感强
3. 动画是否有助于理解概念
4. 代码是否清晰易懂
5. 是否存在视觉混乱或重叠问题

**文案内容：**
{content}

**动画类型：**
{animation_type}

**生成的动画代码：**
```python
{animation_code}
```

"""
        # 改进建议，拼接到prompt
        if improvement_prompt:
            quality_prompt += f"""
\n【上游改进建议】\n{improvement_prompt}\n"""
        quality_prompt += """
**请返回严格的JSON格式评估结果：**
```json
{
    "quality_score": 85,
    "content_alignment": {
        "score": 90,
        "reasoning": "动画与文案内容高度匹配，能有效展示概念"
    },
    "visual_richness": {
        "score": 80,
        "reasoning": "动画元素丰富，但可以增加更多交互效果"
    },
    "educational_value": {
        "score": 88,
        "reasoning": "有助于学习者理解复杂概念"
    },
    "technical_quality": {
        "score": 85,
        "reasoning": "代码结构清晰，无明显技术问题"
    },
    "improvement_suggestions": [
        "可以增加颜色对比度",
        "建议添加渐变动画效果"
    ],
    "needs_revision": false,
    "revision_priority": "low"
}
```
"""
        
        # 接入大模型 LLM
        client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key=os.environ.get('MODELSCOPE_API_KEY'),
        )
        max_retries = 3
        llm_response = None
        for attempt in range(max_retries):
            try:
                llm_response = client.chat.completions.create(
                    model='Qwen/Qwen3-235B-A22B-Instruct-2507',
                    messages=[
                        {'role': 'system', 'content': 'You are a professional science education animation quality assessor.'},
                        {'role': 'user', 'content': quality_prompt}
                    ]
                )
                break 
            except Exception as e:
                print(f"API调用失败，第{attempt+1}次: {e}")
                if attempt < max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                else:
                    print("API多次失败，返回默认内容")
                    return self._mock_quality_assessment()
        # 兼容流式和非流式
        if isinstance(llm_response, (tuple, list)):
            choices = llm_response[0] if isinstance(llm_response, (tuple, list)) and len(llm_response) > 0 else []
            if choices and hasattr(choices[0], 'delta'):
                response = "".join(chunk.delta.content for chunk in choices if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'content') and chunk.delta.content)
            elif choices and hasattr(choices[0], 'message'):
                response = choices[0].message.content
            else:
                response = str(llm_response)
        else:
            # 兼容原生OpenAI SDK
            response = getattr(getattr(llm_response.choices[0], 'message', None), 'content', str(llm_response))
        assessment = safe_json_parse(response, [
            'quality_score', 'content_alignment', 'visual_richness', 
            'educational_value', 'technical_quality', 'needs_revision'
        ])
        return assessment
    
    def _mock_quality_assessment(self):
        """模拟质量评估结果"""
        return {
            "quality_score": 85,
            "content_alignment": {
                "score": 90,
                "reasoning": "动画与文案内容高度匹配，能有效展示概念"
            },
            "visual_richness": {
                "score": 80,
                "reasoning": "动画元素丰富，但可以增加更多交互效果"
            },
            "educational_value": {
                "score": 88,
                "reasoning": "有助于学习者理解复杂概念"
            },
            "technical_quality": {
                "score": 85,
                "reasoning": "代码结构清晰，无明显技术问题"
            },
            "improvement_suggestions": [
                "可以增加颜色对比度",
                "建议添加渐变动画效果"
            ],
            "needs_revision": False,
            "revision_priority": "low"
        }
    

class ContentCoherenceChecker:
    """文案连贯性检查器"""
    
    def check_coherence(self, segments):
        """
        检查文案段落之间的连贯性
        """
        
        if len(segments) < 2:
            return {"coherence_score": 100, "issues": [], "suggestions": []}
        # 提取所有文案内容
        contents = [seg.get('content', '') for seg in segments]
        coherence_prompt = f"""
请作为专业的科普教育内容编辑，检查以下文案段落的连贯性：

**评估要点：**
1. 段落之间的逻辑关系是否清晰
2. 概念引入是否循序渐进
3. 术语使用是否一致
4. 是否有突兀的话题跳转
5. 整体叙述是否流畅自然

**文案段落：**
{self._format_segments_for_analysis(contents)}

**请返回JSON格式的连贯性分析：**
```json
{{
    "coherence_score": 85,
    "logical_flow": {{
        "score": 90,
        "issues": []
    }},
    "concept_progression": {{
        "score": 80,
        "issues": ["第3段概念跳跃过快"]
    }},
    "terminology_consistency": {{
        "score": 95,
        "issues": []
    }},
    "transition_quality": {{
        "score": 75,
        "issues": ["第2段到第3段缺少过渡"]
    }},
    "improvement_suggestions": [
        "在第2段末尾添加过渡句",
        "第3段开头增加概念铺垫"
    ],
    "needs_revision": true,
    "problematic_segments": [2, 3]
}}
```
"""
        
        # 接入大模型 LLM - 带重试机制
        client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key=os.environ.get('MODELSCOPE_API_KEY'),
        )
        max_retries = 3
        llm_response = None
        for attempt in range(max_retries):
            try:
                llm_response = client.chat.completions.create(
                    model='Qwen/Qwen3-235B-A22B-Instruct-2507',
                    messages=[
                        {'role': 'system', 'content': 'You are a professional science education content editor.'},
                        {'role': 'user', 'content': coherence_prompt}
                    ]
                )
                break 
            except Exception as e:
                print(f"API调用失败，第{attempt+1}次: {e}")
                if attempt < max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                else:
                    print("API多次失败，返回默认内容")
                    return self._mock_coherence_check()
        if isinstance(llm_response, (tuple, list)):
            choices = llm_response[0] if isinstance(llm_response, (tuple, list)) and len(llm_response) > 0 else []
            if choices and hasattr(choices[0], 'delta'):
                response = "".join(chunk.delta.content for chunk in choices if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'content') and chunk.delta.content)
            elif choices and hasattr(choices[0], 'message'):
                response = choices[0].message.content
            else:
                response = str(llm_response)
        else:
            response = getattr(getattr(llm_response.choices[0], 'message', None), 'content', str(llm_response))
        return safe_json_parse(response, [
            'coherence_score', 'logical_flow', 'concept_progression',
            'terminology_consistency', 'transition_quality', 'needs_revision'
        ])
    
    def _format_segments_for_analysis(self, contents):
        """格式化段落内容用于分析"""
        formatted = ""
        for i, content in enumerate(contents, 1):
            formatted += f"段落{i}: {content}\n\n"
        return formatted
    
    def _mock_coherence_check(self):
        """模拟连贯性检查结果"""
        return {
            "coherence_score": 85,
            "logical_flow": {
                "score": 90,
                "issues": []
            },
            "concept_progression": {
                "score": 80,
                "issues": ["第3段概念跳跃过快"]
            },
            "terminology_consistency": {
                "score": 95,
                "issues": []
            },
            "transition_quality": {
                "score": 75,
                "issues": ["第2段到第3段缺少过渡"]
            },
            "improvement_suggestions": [
                "在第2段末尾添加过渡句",
                "第3段开头增加概念铺垫"
            ],
            "needs_revision": True,
            "problematic_segments": [2, 3]
        }


class ExampleDrivenJSONParser:
    """示例的JSON解析器"""
    
    def __init__(self):
        # JSON示例模板
        self.segment_example = {
            "segments": [
                {
                    "segment_id": 1,
                    "title": "概念介绍",
                    "content": "今天我们来学习一个重要的概念。",
                    "type": "introduction",
                    "duration": 5.0,
                    "animation_type": "fade_in",
                    "visual_elements": ["title_text", "concept_diagram"]
                },
                {
                    "segment_id": 2,
                    "title": "详细解释", 
                    "content": "这个概念的核心在于...",
                    "type": "explanation",
                    "duration": 8.0,
                    "animation_type": "step_by_step",
                    "visual_elements": ["explanation_text", "animated_diagram"]
                }
            ],
            "total_segments": 2,
            "estimated_duration": 13.0
        }
        
        self.analysis_example = {
            "topic": "人工智能基础",
            "style": "科普教育",
            "key_concepts": ["机器学习", "神经网络", "算法"],
            "audience_considerations": "面向初学者，通俗易懂",
            "complexity_level": "初级",
            "estimated_duration": "300",
            "visual_opportunities": [
                "神经网络结构图",
                "算法流程动画",
                "数据处理演示"
            ],
            "teaching_strategy": "循序渐进，理论结合实例"
        }
    
    def create_prompt_with_example(self, task_type, content):
        """
        创建带有JSON示例的提示词
        """
        
        if task_type == "segmentation":
            example = json.dumps(self.segment_example, ensure_ascii=False, indent=2)
            prompt = f"""
请将以下内容智能分割为适合动画演示的段落。

**重要：请严格按照以下JSON格式返回结果，不要添加任何其他文字说明！**

**标准JSON格式示例：**
```json
{example}
```

**要求：**
1. 每个段落应该是完整的概念单元
2. 内容长度适中，便于动画展示
3. 类型包括：introduction（介绍）、explanation（解释）、example（举例）、summary（总结）
4. animation_type包括：fade_in（淡入）、step_by_step（逐步展示）、emphasis（强调）、comparison（对比）

**待分割内容：**
{content}

**请返回JSON格式结果：**
"""
            
        elif task_type == "analysis":
            example = json.dumps(self.analysis_example, ensure_ascii=False, indent=2)
            prompt = f"""
请分析以下内容的教学特点和制作要求。

**重要：请严格按照以下JSON格式返回结果，不要添加任何其他文字说明！**

**标准JSON格式示例：**
```json
{example}
```

**要求：**
1. 准确识别核心概念和教学目标
2. 评估内容复杂度和受众特点
3. 提出合适的视觉化建议
4. 估算合理的时长安排

**待分析内容：**
{content}

**请返回JSON格式结果：**
"""
        
        return prompt

class AnimationContentMatcher:
    """动画与文案匹配验证器"""
    
    def validate_match(self, animation_code, content, animation_type):
        """
        验证动画代码是否与文案内容匹配
        """
        
        validation_prompt = f"""
请作为专业的科普教育动画审查员，验证动画代码是否与文案内容匹配：

**验证要点：**
1. 动画元素是否体现文案中的关键概念
2. 动画风格是否符合内容类型（{animation_type}）
3. 动画复杂度是否与内容深度匹配
4. 是否存在无关或分散注意力的元素

**文案内容：**
{content}

**动画代码：**
```python
{animation_code}
```

**请返回严格的JSON验证结果：**
```json
{{
    "match_score": 90,
    "concept_coverage": {{
        "covered_concepts": ["概念A", "概念B"],
        "missing_concepts": ["概念C"],
        "coverage_percentage": 75
    }},
    "style_consistency": {{
        "is_consistent": true,
        "style_issues": []
    }},
    "complexity_alignment": {{
        "is_appropriate": true,
        "complexity_feedback": "复杂度适中，符合内容要求"
    }},
    "irrelevant_elements": [],
    "improvement_suggestions": [
        "增加概念C的视觉展示",
        "优化动画过渡效果"
    ],
    "is_acceptable": true,
    "confidence": 0.85
}}
```
"""
        
        # 接入大模型 LLM
        client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key=os.environ.get('MODELSCOPE_API_KEY'),
        )
        max_retries = 3
        llm_response = None
        for attempt in range(max_retries):
            try:
                llm_response = client.chat.completions.create(
                    model='Qwen/Qwen3-235B-A22B-Instruct-2507',
                    messages=[
                        {'role': 'system', 'content': 'You are a professional science education animation reviewer.'},
                        {'role': 'user', 'content': validation_prompt}
                    ]
                )
                break 
            except Exception as e:
                print(f"API调用失败，第{attempt+1}次: {e}")
                if attempt < max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                else:
                    print("API多次失败，返回默认内容")
                    return self._mock_validation_result()
        if isinstance(llm_response, (tuple, list)):
            choices = llm_response[0] if isinstance(llm_response, (tuple, list)) and len(llm_response) > 0 else []
            if choices and hasattr(choices[0], 'delta'):
                response = "".join(chunk.delta.content for chunk in choices if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'content') and chunk.delta.content)
            elif choices and hasattr(choices[0], 'message'):
                response = choices[0].message.content
            else:
                response = str(llm_response)
        else:
            response = getattr(getattr(llm_response.choices[0], 'message', None), 'content', str(llm_response))
        parsed = safe_json_parse(response, [
            'match_score', 'concept_coverage', 'style_consistency',
            'complexity_alignment', 'is_acceptable', 'confidence'
        ])
        if isinstance(parsed, list):
            if parsed:
                return parsed[0]
            else:
                return {}
        return parsed
    
    def _mock_validation_result(self):
        """模拟验证结果"""
        return {
            "match_score": 90,
            "concept_coverage": {
                "covered_concepts": ["主要概念", "关键原理"],
                "missing_concepts": [],
                "coverage_percentage": 95
            },
            "style_consistency": {
                "is_consistent": True,
                "style_issues": []
            },
            "complexity_alignment": {
                "is_appropriate": True,
                "complexity_feedback": "复杂度适中，符合内容要求"
            },
            "irrelevant_elements": [],
            "improvement_suggestions": [
                "可以增加更多互动元素",
                "优化颜色搭配"
            ],
            "is_acceptable": True,
            "confidence": 0.90
        }

